# Prompt for Claude Code — Ship the Lullable catalogue: gates → closeout → Supabase

Copy everything below into Claude Code, run from `~/Documents/CLAUDE/02_LULLABLE/lullable_audio/`.

---

You are finishing the publishing pass for Lullable, a sleep-story iOS app. Production is
done; publishing is the bottleneck. Your job: find out exactly which of the 17 publish
gates block each story, close every gate that can be closed mechanically, prepare the
human-decision list for AV, and push approved episodes to Supabase — strictly through the
existing pipeline, never around it.

## Context — read these before acting (they are authoritative; where they disagree with
this prompt, they win)

1. `AWS_Polly/tools/PIPELINE-MEMORY.md` — what exists: AWS/Polly setup, casting,
   recipe, naming, current status.
2. `Docs/01-pipeline-runbook.md` — the seven stages and their commands.
3. `Docs/03-manifest-reference.md` — every `story.yaml` field.
4. `Docs/04-gates-reference.md` — all 17 gates (G01–G17) and how to fix each.
5. `Stories/casting.yaml` — voice/engine/persona/bio per category (confirmed by AV).

Ground rules: `Stories/<id>/story.yaml` is the single source of truth; everything in
`_generated/` is produced by `python3 Tools/lullable.py --root . build`. Never hand-edit
generated files, never write to the tracker by hand, never bypass `lullable.py` for
closeout/approve/publish. If `Tools/lullable.py` is missing, stop and tell AV.

## Current state (2026-08-20, verify rather than trust)

- 20 story folders. ALL have Polly-rendered audio per the new convention:
  `audio/polly-<Voice>-raw.mp3` + `audio/delivery.m4a` (AAC-LC 44.1k mono 96k) +
  `audio/master.wav` (44.1k 16-bit mono) + `_generated/polly.ssml`.
- Provider changed: audio is now Amazon Polly, NOT ElevenLabs. Most `story.yaml` files
  still carry ElevenLabs-era `render:` blocks and stale `audio:` hashes — expect gate
  failures there; that is the main mechanical work.
- Legacy-published episodes whose Supabase audio is now outdated and must be replaced:
  `the-rings-of-saturn` (re-voiced with Amy, AV approved), `aristotle-the-greatest-philosopher`
  (new text + Emma), `dinosaurs-from-rule-to-ruin` (new text + Arthur). Aristotle and
  Dinosaurs also have brand-new `narration.md` / `upload-to-elevenlabs.txt` — their
  `script:` stats in story.yaml are stale.
- Old ElevenLabs audio sits in `Stories/_to_delete/` — ignore it; AV deletes it.

## Do this, in order

### Phase 1 — Diagnose
1. `python3 Tools/lullable.py --root . status` and `validate --all`. Capture full output.
2. Build a gate matrix: stories × G01–G17, marking pass/fail and the failure reason.
   Save it as `Stories/_reports/gate-matrix-<date>.md` and show AV a summary table.

### Phase 2 — Mechanical fixes (no approval needed; follow Docs/04 for each gate)
3. Update every `story.yaml` to reflect reality, per Docs/03:
   - `render:` block → provider amazon-polly; voice, engine, language from
     `Stories/casting.yaml` for the story's category; renderedAt = the audio file's date.
   - `card.narrator` → the category persona string ("Read by … from …") from casting.yaml.
   - `audio:` block → recompute sha256, bytes, durationSeconds, codec/sampleRate/channels
     for the CURRENT master.wav and delivery.m4a (ffprobe + shasum). durationSeconds must
     match the real files.
   - `script:` stats (words, breaks, wordsPerBreak, silenceSeconds) → recompute from each
     `upload-to-elevenlabs.txt`; use `compile` if the runbook says so.
   - `card.durationSeconds` → the delivery.m4a duration.
4. `build --all`, then `validate --all` again. Iterate until the only failures left are
   ones requiring a human (QA listen, rights evidence, access decisions, identity).
5. Commit the content repo (lullable-content) after each clean build, small commits,
   clear messages. Never force-push.

### Phase 3 — Human-gated items (prepare, then STOP and ask AV)
6. Produce `Stories/_reports/decisions-for-AV.md` listing, per story: gates that need a
   human, what exactly AV must do (e.g. "listen and approve", "set accessDecision
   free/premium", "confirm rights note"), and the one-line command you will run once he
   says yes (`closeout … --voice-id <Voice> --model <engine> …`, `approve … --by "AV"`).
   For Polly, map closeout fields per Docs/03 (voice-id = Polly VoiceId, model = engine;
   history-id has no ElevenLabs meaning anymore — use the Polly TaskId from the render
   if the schema requires a value, and note this adaptation in the report).
7. Do NOT set accessDecision, do NOT approve QA, do NOT mark rights verified yourself.

### Phase 4 — Publish (only stories AV explicitly approves)
8. For each approved story, run the publish exactly as the runbook says — normally the
   generated `_generated/publish-commands.sh` after closeout+approve. Supabase specifics
   (bucket `sleep-stories-premium` or as the manifest says, storage path pattern, catalog
   upsert) come from the runbook and the generated files, not from memory.
9. For the three legacy-published stories, the new audio REPLACES the old asset: follow
   the runbook's re-publish/supersede path; keep the same storyID so favorites and
   progress survive. Never delete the old Supabase object until the new one is live and
   playing in the app.
10. After each publish: `tracker` to rebuild the spreadsheet, then verify in-app or via
    Supabase that the new audio streams. Report per-story before/after status.

## Deliverables back to AV
- The gate matrix, the decisions file, a per-story publish log, and a final `status`
  screenshot-style summary: how many published / staged / blocked and on what.

## Never do
- Never bypass lullable.py or hand-write generated files/tracker rows.
- Never publish a story AV has not approved in this session.
- Never change casting, recipe, or prose — that is settled config (casting.yaml).
- Never touch Apple/App Store credentials; Supabase only, via the pipeline.
- Never delete anything; move superseded files to `Stories/_to_delete/` if needed.
