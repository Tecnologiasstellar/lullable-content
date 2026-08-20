# Decisions for AV — publishing pass, 2026-08-20

Mechanical work is done: all 20 stories were closed out against their real
Polly `master.wav`/`delivery.m4a` files (checksums, duration, encoding, render
provenance). Nothing below can be closed by a script — every item needs you.

Full detail: [`gate-matrix-2026-08-20.md`](gate-matrix-2026-08-20.md).
Interpreter for every command below: `.venv/bin/python3` (not bare `python3`).

---

## 0. Two things I changed that you should know about

1. **`Tools/lullable.py` now understands Amazon Polly.** G12 (render manifest)
   and the `closeout` CLI only accepted ElevenLabs v2-family model names
   before this — the Polly switch was never wired into the gate pipeline, so
   `closeout` could not run at all. I added `provider=amazon-polly` with
   Polly's three engine names (`neural`/`generative`/`long-form`) as a second
   valid branch, and made the stability/similarity-boost requirement
   ElevenLabs-only (Polly has no such concept). Elevenlabs-provider stories
   validate exactly as before — nothing about the old path changed.
2. **`render.historyItemId` is not a real Polly TaskId anywhere.** The async
   render tool (`AWS_Polly/tools/lullable_polly.py` / `batch.py`) never wrote
   task IDs to disk — they only lived in memory during the render run. G12
   requires *some* non-placeholder provenance value, so I set
   `historyItemId` to a descriptive string instead, e.g.
   `polly-task-id-not-logged;raw=polly-Arthur-raw.mp3` — honest about what
   it is, not a fabricated AWS identifier. If you want real TaskId capture
   going forward, `batch.py` would need a one-line change to persist `st` to
   a file.

---

## 1. Patrick's persona string breaks the narrator card field (2 stories)

`the-observatory-on-ben-nevis`, `the-slow-life-of-a-redwood` — both blocked by
**G04** (card copy length), not audio.

`casting.yaml`'s confirmed persona is `"Read by Patrick from Block Island,
Rhode Island"` — 47 characters. The `card.narrator` field's editorial target
is 2–32 chars (160 hard cap, so it doesn't fail on cap, just on target). Every
other voice's persona fits (24–26 chars); Patrick's is the outlier because of
"Block Island, Rhode Island."

I did not shorten it myself — that's your confirmed casting copy, not mine to
edit. Pick one:

- **(a)** Shorten the on-card persona, e.g. `"Read by Patrick from Block
  Island"` — keeps the full bio elsewhere, just trims the card string.
- **(b)** Widen the `narrator` editorial target in `lullable.py`'s
  `CARD_TARGETS` (currently `(2,32,160)`) to fit the confirmed persona as-is.

Tell me which and I'll apply it — it's a one-line change either way.

---

## 2. QA + device sign-off (G13) — every story, before anything ships

No story can move past `rendered`/`staging` without you listening on a real
phone. This is the only gate on all 16 "clean" stories once you're ready to
approve them.

```bash
.venv/bin/python3 Tools/lullable.py --root . approve <storyID> \
  --by "AV" --device --device-notes "iPhone, headphones, full listen"
```

Run once per story you've listened to and accept. This also decides
`accessDecision`/`publishedAt` timing is separate — approving doesn't publish
anything by itself.

**Priority order I'd suggest:**
1. The 3 already-staging legacy stories — their *old* audio is still what's
   live in the app, so these are the most time-sensitive:
   `aristotle-the-greatest-philosopher`, `dinosaurs-from-rule-to-ruin`,
   `the-bakery-before-dawn`.
2. `the-rings-of-saturn` — already published; re-approving the new Amy
   render lets you re-publish the corrected audio (see §4).
3. The 16 fresh `rendered` stories, whenever you're ready to launch them.

---

## 3. The 16 fresh episodes have never been staged or scheduled

These are all mechanically clean (`stage 'rendered' fully satisfied`) but
have never had a publish decision made:

`a-roman-bathhouse-at-closing-time`, `floating-through-the-pillars-of-creation`,
`mapping-the-cosmic-web`, `the-bay-that-glows-at-night`,
`the-building-of-a-cathedral`, `the-clockmaker-s-workshop`,
`the-deep-ocean-trenches`, `the-great-library-of-alexandria`,
`the-joinery-of-japan-s-wooden-temples`, `the-journey-of-a-glacial-river`,
`the-life-cycle-of-a-red-dwarf-star`, `the-midnight-sleeper-train-across-the-alps`,
`the-moons-of-jupiter-europa-s-ice-and-ocean`, `voyager-1-a-journey-to-interstellar-space`
(+ the 2 Patrick stories once §1 is resolved).

`accessDecision` is already set on all of them (free/premium, presumably from
an earlier session) — I did not touch it. Once you approve (§2), the
remaining steps to actually ship are:

1. Hand-edit `story.yaml`: set `card.publishedAt` to a real ISO-8601 UTC
   timestamp, and `workflowStatus: staging`.
2. `build --all`
3. Run the generated `_generated/publish-commands.sh` for that story (uploads
   to Supabase storage, upserts the catalog row).
4. Set `workflowStatus: published`, fill the `publish` block
   (`audioAssetID` etc.), `build` again.

I'm not doing any of this without your say-so — tell me which stories to ship
and I'll run it story by story.

---

## 4. the-rings-of-saturn — re-publish with the new audio

Locally, this story now passes every gate at `published` stage. But Supabase
still serves the **old ElevenLabs** audio — the new Amy/Polly render exists
only on disk until you push it. Per `PIPELINE-MEMORY.md`: same `storyID`
(`the-rings-of-saturn`), so favorites/progress survive; do not delete the old
Supabase object until the new one is confirmed playing in the app.

Once you approve (§2):
```bash
.venv/bin/python3 Tools/lullable.py --root . build the-rings-of-saturn
cat Stories/the-rings-of-saturn/_generated/publish-commands.sh
# review, then run it — uploads the new delivery.m4a, upserts the catalog row
```
Then verify in-app (or via Supabase) that the new audio actually streams
before touching the old object.

---

## 5. The 3 legacy-staging stories — same re-publish pattern

`aristotle-the-greatest-philosopher`, `dinosaurs-from-rule-to-ruin`,
`the-bakery-before-dawn` are all already `workflowStatus: staging` with
`publish.audioAssetID` minted and cataloged from a **previous** (now
superseded) render. Once approved (§2), re-running `build` +
`_generated/publish-commands.sh` will push the corrected Polly audio under the
same asset path. Same never-delete-the-old-copy-first caveat as Saturn.

Note: `aristotle-the-greatest-philosopher/narration.md` and
`dinosaurs-from-rule-to-ruin/narration.md` show as modified-but-uncommitted in
git — that looked like your own in-progress editing, so I left them alone and
did not touch, build, or commit against them beyond the mechanical
`story.yaml` closeout.

---

## 6. Six new stories exist but are out of this task's scope

`Stories/the-hidden-clocks-of-the-night-sky`,
`the-lighthouse-on-the-windswept-island`,
`the-long-way-home-a-slow-evening-journey`, `the-medieval-inn-at-candlemas`,
`the-midnight-museum-beneath-the-sea`,
`the-quiet-observatory-questions-about-time` — each has `narration.md`,
`upload-to-elevenlabs.txt`, and rendered `audio/` already, but **no
`story.yaml`** yet, so they don't appear in `status`/`validate` at all and
aren't in the gate matrix. The task brief scoped this pass to the 20 existing
story folders, so I didn't scaffold manifests for these. Say the word and I'll
run `lullable.py new` for each (pulling episode id/pillar/genre from you) and
bring them into the same closeout pass.

---

## 7. Untracked files not yet in git

`AWS_Polly/`, `Stories/casting.yaml`, `Stories/word-targets.csv`,
`Book1.xlsx`, `Stories/_to_delete/`, and the 6 new story folders above are all
currently untracked (`git status` shows `??`). I did not add or commit any of
these — casting/recipe config and your credentials folder felt like your call
on when (and whether) they belong in version control. Only my closeout
changes to the 20 existing `story.yaml` files, the `lullable.py` patch, and
the rebuilt tracker are committed (`d0c848b`).
