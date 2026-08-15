# Lullable — start here

There is now exactly **one** file you ever edit per story: `story.yaml`.

Everything else — the tracker spreadsheet, the app card, the Supabase payload, the
publish commands — is generated from it. If two things ever disagree, `story.yaml`
is right and the other one is stale.

---

## Where to look things up

| I want to… | Read |
|---|---|
| Follow the process step by step | `Docs/01-pipeline-runbook.md` |
| Know how to write in the voice | `Docs/02-house-voice.md` |
| Understand a field in story.yaml | `Docs/03-manifest-reference.md` |
| Fix a failing gate | `Docs/04-gates-reference.md` |
| Pick a genre or a colour | `Docs/05-genres-and-pillars.md` |
| Know why something works this way | `Docs/06-decisions.md` |
| Look up a word | `Docs/07-glossary.md` |
| Know how this sits next to the app | `Docs/08-integration.md` |
| Choose the next episode | `Backlog/episode-backlog.md` |

## The folder

```
lullable_audio/
│
├── README.md                         the index
├── START_HERE.md                     ← this file
├── Lullable_Story_Card_Tracker.xlsx  ← a REPORT. Generated. Do not type in it.
├── Lullable_Production_Process.pptx  the deck explaining the process
│
├── Docs/                             how the system works (7 files)
├── Backlog/episode-backlog.md        the topic queue
├── Tools/lullable.py                 the one tool
│
├── Stories/
│   └── <storyID>/
│       ├── story.yaml                ← THE ONLY FILE YOU EDIT
│       ├── narration.md              the story as written
│       ├── upload-to-elevenlabs.txt  the story with pauses — upload this
│       ├── script.md                 clean readable copy
│       ├── audio/                    master.wav and delivery.m4a go here
│       └── _generated/               never edit anything in here
│           ├── story-card.yaml
│           ├── tracker-row.tsv
│           ├── catalog-payload.json
│           ├── neon-metadata.json
│           └── publish-commands.sh
│
└── Templates/                        the original standard, for reference
```

---

## The commands

Ask Claude to run these; you never need to type them yourself.

| Command | What it does |
|---|---|
| `new "<Title>" --genre <g>` | Scaffolds a new episode folder with a manifest and a narration skeleton. |
| `compile Stories/<id>` | Turns the narration into the paused upload file. Refuses if the cadence is off. |
| `validate --all` | Checks every story against 17 gates and says exactly what is blocking each one. |
| `status` | One screen: every story, its stage, and what is blocking it. |
| `build --all` | Regenerates everything in `_generated/` from the manifests. |
| `tracker` | Rebuilds the spreadsheet from all manifests. |
| `closeout <id>` | After the render: reads the audio files and fills in duration, checksums and encoding. |
| `approve <id> --by "AV" --device` | Records that a person listened on a real phone and approved it. |
| `website-export --all` | Writes the story's page for getlullable.com. Refuses without real audio. |

---

## Two different questions, kept apart

These used to be the same field, which meant a story could drift into being
"premium" before anyone had decided that.

**`workflowStatus`** — where the story is in production:

`draft` → `rendered` → `qa-approved` → `staging` → `published`

**`accessDecision`** — the commercial question, answered whenever you like:

`PENDING` → `free` or `premium`

The `access` value the app actually sees stays `PENDING` until the story reaches
`staging` **and** a decision has been made. Nothing can go live under a tier
nobody chose.

---

## The 17 gates

Each stage requires a subset. `PUBLISH READY` means all seventeen pass.

| | Gate | Checks |
|---|---|---|
| G01 | manifest schema | required sections present, schema version |
| G02 | story identity | storyID format, identity resolved, `supersedes` sane |
| G03 | allowed values | every enum and boolean is legal |
| G04 | card copy lengths | all eight copy fields within editorial targets |
| G05 | artwork colours | six uppercase hex characters |
| G06 | publish date | strict ISO-8601 UTC, not a bare date |
| G07 | no placeholders | nothing still says PENDING or VOICE_ID |
| G08 | files exist | master, delivery and any rights evidence are on disk |
| G09 | checksums | recorded sha256 matches the actual bytes |
| G10 | delivery encoding | really AAC-LC, 44.1 kHz, mono, ~96 kbps |
| G11 | duration matches | card duration equals measured audio, within 1s |
| G12 | render manifest | voice, model, settings, history ID all recorded; v2-family model |
| G13 | QA sign-off | audio approved by a named person, accepted on a physical device |
| G14 | Supabase | audio uploaded and catalog row upserted |
| G15 | rights | verified with evidence |
| G16 | access final | free vs premium settled |
| G17 | SSML integrity | break tags only, correct open/close, cadence within limit |

These check reality, not typing. G09 hashes the actual file. G10 runs `ffprobe`.
G11 compares the card against the measured audio. A wrong number cannot pass by
being confidently entered.

---

## Making a new episode

Ask Claude for a story. It researches, writes, compiles, and creates the folder
with a `story.yaml` already filled in. Then run `validate` to see what remains.

A fresh episode legitimately fails the later gates — there is no audio yet. That
is the system working, not a problem.

---

## After the render

Put `master.wav` and `delivery.m4a` into the story's `audio/` folder, then run
`closeout`. It reads the files themselves — computes both checksums, measures the
real duration and encoding, and fills the manifest. Nothing is typed, so nothing
can be mistyped.

Then listen to the whole episode on a real phone and run `approve`. A render can
be technically perfect and still wrong in the ear, which is why that sign-off is
a separate gate.

---

## Sending it to ElevenLabs

1. **ElevenLabs Studio / Projects**, not the small text box.
2. **A v2-family model.** Not v3 — v3 ignores the pauses, and G12 will reject it.
3. Upload `upload-to-elevenlabs.txt`. Nothing else.

---

## Rights

Lullable owns everything: scripts written in-house, voice licensed to you. So
`rights.status` is `verified` by default and there is nothing to check per episode.
If an episode ever uses outside material, set it back to `pending-verification`
and record the real licence.

---

## Open decision — Saturn's identity

`the-rings-of-saturn` currently **fails G02 on purpose** and cannot be published.

The app already carries a card with the storyID `edge-of-saturn`. Someone has to
say which of these is true:

- **It replaces that card.** Set `storyID: edge-of-saturn` so existing favorites and
  progress keep working, since a storyID never changes after publication.
- **It is an additional story.** Keep `the-rings-of-saturn`.

Either way, then set `identityResolved: true` and re-run `validate`. Until then the
catalog payload refuses to build, which is the safe outcome.

---

## Where's the code?

`Tools/lullable.py`. One copy, and this is it.

This reverses an earlier decision. When the tooling was a 100-line compiler it lived
inside the Claude skill, because a folder copy would only go stale. At over 1,000 lines that
no longer holds: a script this size cannot be reliably reproduced from a document, and
it needs to be versioned alongside the data it validates. So the skill now describes
the workflow and calls this file, rather than carrying a duplicate of it.

## Is this folder forever?

No. It is the working home while the catalogue is small. The plan is Supabase, and
`_generated/catalog-payload.json` is already shaped for that move.
