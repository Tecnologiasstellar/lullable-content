# The seven-stage pipeline — runbook

The operational version. For the plain-language overview see `../START_HERE.md`.

Every command assumes you are in the `lullable_audio` folder. Ask Claude to run
them; you should never need to type them yourself.

**Interpreter.** Use `.venv/bin/python3`, not bare `python3`. The tool needs
`pyyaml` (all commands) and `openpyxl` (`tracker` only), and the system pythons
on this Mac either lack them or refuse installs under PEP 668. If `.venv/` is
missing, rebuild it once:

```
python3 -m venv .venv && .venv/bin/python3 -m pip install pyyaml openpyxl
```

```
Define → Research → Write → Compile → Structure → Validate → Ship
  1        2          3         4          5          6        7
```

Human judgement lives in stages 1–3 and in QA sign-off. Everything between is
mechanical and repeatable.

---

## Stage 1 — Define

Decide before writing:

| Decision | Notes |
|---|---|
| Topic & pillar | Prefer an empty or thin genre. See `05-genres-and-pillars.md`. |
| Target runtime | Sets the word count. ~4,400 words ≈ 45 min at 118 wpm. |
| Genre | One of four. A new genre is a product decision, not a writing one. |
| Story identity | New story, or a replacement for an existing card? See below. |

Scaffold it:

```bash
python3 Tools/lullable.py --root . new "The Rings of Saturn" \
  --genre cosmic-journeys --pillar "4. Space & Cosmic Journeys" --id 16 \
  --tags "sleep story,space,astronomy"
```

That creates `Stories/<storyID>/` with a manifest, a narration skeleton, and an
empty `audio/` folder.

**If the story replaces an existing card**, reuse the old `storyID` — it is the
key favorites and progress hang off, and it must never change after publication.
If you are unsure, scaffold with `--unresolved --identity-note "..."`; G02 will
then block publication until someone decides.

---

## Stage 2 — Research

Verify **before** drafting, never after. Search for every number, name, mechanism
and date. Where the science is genuinely unsettled, present the disagreement
calmly in the narration — an open question is restful; a false certainty is not.

Keep the sources; they get handed back with the episode.

Rule of thumb: if a sentence contains a figure, a proper noun, or a mechanism,
it needs a source behind it.

---

## Stage 3 — Write

Replace every `PENDING` in `narration.md`. Full rules in `02-house-voice.md`.

The one thing that will bite you: **short sentences**. Mean under 12 words,
almost nothing over 22. Write short the first time — splitting afterwards is
slow and mechanical.

Then write the card copy into `story.yaml` under `card:` while the story is
fresh. Seven fields, targets in `03-manifest-reference.md`. `narrator` is **not**
one of them — it is set at render time.

**Coming in short?** Add whole new *sections*, never longer sentences. A new
section adds a 3.0s seam and keeps the cadence right. Good material: how the
thing was discovered, what a component is made of, an unresolved argument, the
people or instruments that found it out.

---

## Stage 4 — Compile

```bash
python3 Tools/lullable.py --root . compile Stories/the-rings-of-saturn
```

Writes `upload-to-elevenlabs.txt` and `script.md`, and records words, breaks,
words/break and silence into the manifest.

**It refuses to write** above 15.0 words/break or on any exclamation mark, and
prints the twelve longest sentences. Fix the prose, not the compiler. `--force`
exists only for a deliberate, explained exception.

Healthy numbers: mean sentence 10–12 words · words/break 13–14 · ~10 min of
silence per 45 min.

---

## Stage 5 — Structure

```bash
python3 Tools/lullable.py --root . build --all
```

Regenerates `_generated/` from the manifest: the story card, the tracker row, the
Supabase upsert SQL and shipping commands for each environment, the Neon record.
Never edit anything in there — it is overwritten.

Run `build` after **any** manifest change. `validate` will warn you if you forget.

---

## Stage 6 — Validate

```bash
python3 Tools/lullable.py --root . validate --all
python3 Tools/lullable.py --root . status          # one-screen catalogue view
```

Seventeen gates, staged by `workflowStatus`. Full list and fixes in
`04-gates-reference.md`.

A fresh episode legitimately fails the audio gates — there is no audio yet. That
is the system working, not a problem.

---

## Stage 7 — Ship

**Render.** ElevenLabs Studio / Projects, not the short TTS box. A **v2-family**
model — never v3, which ignores break tags and fails G12. Upload
`upload-to-elevenlabs.txt` and nothing else.

**Bring the audio back.** Put `master.wav` and `delivery.m4a` in the story's
`audio/` folder. Delivery must be AAC-LC, 44.1 kHz, mono, ~96 kbps.

**Close out.** This reads the actual files — nothing is typed:

```bash
python3 Tools/lullable.py --root . closeout the-rings-of-saturn \
  --voice-id <id> --voice-name "Amelia Rhodes" --model eleven_multilingual_v2 \
  --history-id <elevenlabs history id> --stability 0.45 --similarity 0.75 \
  --speaker-boost --asset-id lull-aud-0016-v1
```

It computes both checksums, reads the real duration and encoding via `ffprobe`,
fills the render and audio blocks, sets `card.durationSeconds` from the file, and
moves the story to `rendered`.

**Sign off.**

```bash
python3 Tools/lullable.py --root . approve the-rings-of-saturn \
  --by "AV" --device --device-notes "iPhone 15, headphones, full listen"
```

Listen to the whole thing on a real device before running this. The gate exists
because a render can be technically perfect and still wrong.

**Decide access.** Set `accessDecision` to `free` or `premium` in the manifest,
and `publishedAt` to a strict ISO-8601 UTC timestamp. The bucket follows from the
access decision; you do not choose it.

**Publish to staging, look at it, then promote.** Two Supabase projects, one
catalogue — see Docs/06-decisions.md D28.

```bash
python3 Tools/lullable.py publish <id> --env staging --dry-run   # read the SQL first
python3 Tools/lullable.py publish <id> --env staging
python3 Tools/lullable.py verify  <id> --env staging             # stamps verifiedAt
# look at the staging row yourself, then:
python3 Tools/lullable.py publish <id> --env production
python3 Tools/lullable.py verify  <id> --env production
```

`publish` stamps the manifest and moves `workflowStatus` itself — do not fill the
`publish` block by hand. Promoting refuses outright until staging is verified, so
there is no path to production that skips it.

---

## Batching

Stages 1–5 parallelise well; stage 7 does not, because it costs render credits
and needs a human listen.

A sensible batch: scaffold four episodes, research and write them in one sitting,
compile all four, then `validate --all` and fix whatever is red before spending a
single credit on a render.

```bash
python3 Tools/lullable.py --root . validate --all --strict   # non-zero if anything is blocked
```

---

## After any change

```bash
python3 Tools/lullable.py --root . build --all
python3 Tools/lullable.py --root . tracker
```

The spreadsheet is a report, generated from the manifests. If it disagrees with a
manifest, the manifest is right and the spreadsheet is stale.
