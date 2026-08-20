# Lullable — Claude Code instructions: text → finished Polly audio
*How to take a story text and produce the three canonical audio files. Read
`PIPELINE-MEMORY.md` first for what exists and why. Work from
`~/Documents/CLAUDE/02_LULLABLE/lullable_audio/`.*

## Prerequisites (one-time per machine)

```bash
pip3 install boto3            # AWS SDK
brew install ffmpeg           # if missing; `which ffmpeg` to check
```
Credentials: read Access Key ID + Secret from `AWS_Polly/lullable-tts_accessKeys.csv` and
export them (or write `~/.aws/credentials`):
```bash
export AWS_ACCESS_KEY_ID=...  AWS_SECRET_ACCESS_KEY=...  AWS_DEFAULT_REGION=us-east-1
```
The render tool is `AWS_Polly/tools/lullable_polly.py`. Region us-east-1,
bucket `lullable-audio-864981744724`.

## Step 0 — Look up the assignment

Open `Stories/casting.yaml`: find the story's category under `story_categories`, then the
category's `voice`, `engine`, `measured_wpm`, `persona`, `bio`. Never use another voice or
engine for that category. If the story is new, add it to `story_categories` first
(pick the category that fits; AV confirms).

## Step 1 — The text (house voice)

The source of truth for prose format is any existing story, e.g.
`Stories/the-bay-that-glows-at-night/`. Rules that the compiler and QA enforce:
- Fixed arc: `Good evening.` → settling → tonight's destination → permission to drift →
  factual body (14–20 sections, separated by a lone `§` line in narration.md) → dissolve →
  `You are held. You are safe. …` → `Sleep now. Easy, and unhurried, and deep.` → `Goodnight.`
- Short sentences: mean under 12 words, almost nothing over 22. Warm, second person, unhurried.
- Zero conflict, no danger/predation/death emphasis (reframe bleak facts gently),
  zero exclamation marks, never promise sleep or treat a condition.
- Every fact verified before drafting (web-check numbers, names, dates).
- Word count: hit the story's target in `Stories/word-targets.csv`, or compute it:
  `words = 45 * 0.93 / (1/wpm + 0.1405 * 1.25 / 60)` using the category voice's wpm
  (0.1405 = house seconds-of-authored-silence per word). Too short? Add whole sections.
- Break tags (the file with breaks is `upload-to-elevenlabs.txt` — legacy name, now feeds
  Polly): a `<break time="X.Xs"/>` after most sentences; 1.0–2.6s within sections, 3.0s at
  section ends; keep words-per-break ≤ 15 (aim ~12); max authored break 3.8s.
- Two files, same prose: `narration.md` (with `§` lines, no break tags) and
  `upload-to-elevenlabs.txt` (with break tags, no `§`).

### New stories from a sample text / YouTube reference
When AV supplies a sample text (e.g. a YouTube transcript) plus the URL:
1. Treat the sample as **research material only — never copy its sentences or structure.**
   Extract the facts and the topic arc; independently verify every fact via web search.
2. Rewrite from scratch in the Lullable house voice per the rules above, at the word target
   for the assigned category's voice. The result must be original Lullable prose.
3. Record the YouTube URL as a research source in the story's rights/notes (it is a
   reference, not a rights basis — the prose must be ours).
4. Scaffold the story folder like the existing ones (`story.yaml`, `narration.md`,
   `upload-to-elevenlabs.txt`, `audio/`, `_generated/`); use `Tools/lullable.py --root . new`
   if available, otherwise mirror an existing folder's structure.

## Step 2 — Convert (applies pause_scale 1.25)

```bash
cd ~/Documents/CLAUDE/02_LULLABLE/lullable_audio
python3 AWS_Polly/tools/lullable_polly.py convert \
  "Stories/<storyID>/upload-to-elevenlabs.txt" \
  --pause-scale 1.25 --out "Stories/<storyID>/_generated/polly.ssml"
```
It XML-escapes the prose, wraps `<speak>`, scales every break 1.25x (cap 10s), refuses on
exclamation marks / >15 words-per-break, and prints words, silence, runtime and cost
estimates. Fix the prose if it refuses — never the converter.

## Step 3 — Render (async, the category's voice)

```bash
python3 AWS_Polly/tools/lullable_polly.py render \
  "Stories/<storyID>/_generated/polly.ssml" \
  --voice <Voice> --engine <engine> \
  --bucket lullable-audio-864981744724 --prefix "stories/<storyID>/" \
  --download "Stories/<storyID>/audio/polly-<Voice>-raw.mp3"
```
Takes 1–3 min. For several stories, submit them all first, then poll (task APIs are
~1 req/s for generative/long-form). `AWS_Polly/tools/batch.py` is the reference batch
driver from the 2026-08-20 catalogue run — edit its `BASE`/`WORK` paths for local use.

## Step 4 — Master + formats (exact approved chain)

```bash
cd "Stories/<storyID>/audio"
ffmpeg -y -i "polly-<Voice>-raw.mp3" -af \
 "atempo=0.93,equalizer=f=180:t=q:w=0.9:g=1.5,equalizer=f=7000:t=q:w=1.0:g=-2,acompressor=threshold=-18dB:ratio=2.5:attack=25:release=400,loudnorm=I=-20:TP=-2:LRA=7,aresample=44100" \
 -ac 1 -c:a aac -profile:a aac_low -b:a 96k -ar 44100 delivery.m4a
ffmpeg -y -i delivery.m4a -ar 44100 -ac 1 -c:a pcm_s16le master.wav
```

## Step 5 — Verify, then close out

- `ffprobe` delivery.m4a: duration should land 36–45 min; mono 44.1 kHz AAC ~96k.
- Spot-listen: opening, one mid section, the `Sleep now… Goodnight.` ending.
- The story folder must now contain exactly: `audio/polly-<Voice>-raw.mp3`,
  `audio/delivery.m4a`, `audio/master.wav`, `_generated/polly.ssml`.
- Update `story.yaml` through the existing pipeline (`Tools/lullable.py`, its docs in `Docs/`):
  render provider is now amazon-polly, voice/engine from casting.yaml, narrator = the
  category persona ("Read by … from …"), then `build` + `validate`. Publishing to
  Supabase stays with the existing 17-gate pipeline — never bypass it.

## Never do

- Never use a non-cast voice/engine for a category, or the legacy "standard" engine.
- Never stretch audio to lengthen an episode; add sections instead.
- Never copy source/transcript sentences into a narration.
- Never hand-edit `_generated/` files (polly.ssml is written by the converter — fine).
- Never push to Supabase outside the 17-gate pipeline.
