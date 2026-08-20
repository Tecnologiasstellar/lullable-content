# Lullable × Amazon Polly — Pipeline Memory
*State of the world as of 2026-08-20. Read this first. The companion file
`CLAUDE-INSTRUCTIONS.md` says how to run the process; this file says what exists and why.*

## What was decided (all confirmed by AV)

1. **Amazon Polly is the default narrator** (replacing ElevenLabs). Rationale: ~$0.40–$2.30
   per 40-min episode vs ~$5.50 on ElevenLabs Creator, no monthly cap, SSML break tags
   are billed at $0 so Lullable's silence-heavy style is free.
2. **One fixed voice per app category** ("official casting", stored machine-readably in
   `Stories/casting.yaml` — that file is the single source of truth for casting, personas,
   bios, recipe and naming):

   | Category | Voice | Accent | Polly engine | Measured pace | Persona |
   |---|---|---|---|---|---|
   | Long Ago | Arthur (M) | British | neural | 183 wpm | Read by Arthur from Ludlow |
   | Stars & Signs | Amy (F) | British | generative | 187 wpm | Read by Amy from Greenwich |
   | Wild Places | Patrick (M) | American | long-form | 167 wpm | Read by Patrick from Block Island, Rhode Island |
   | Big Questions | Emma (F) | British | neural | 162 wpm | Read by Emma from Oxford |
   | Deep Ocean | Brian (M) | British | generative | 152 wpm | Read by Brian from St Ives |
   | Slow Journeys | Niamh (F) | Irish | generative | 178 wpm | Read by Niamh from Kinsale |

   Notes: long-form engine exists ONLY for four en-US voices — that is why Emma is neural.
   The legacy "standard" engine is banned (robotic). Each voice has a 1–2 sentence bio in
   casting.yaml, used on story cards ("Read by …").
3. **The production recipe** (approved, apply to every episode, never deviate):
   - `pause_scale 1.25` — multiply every authored `<break>` duration before rendering.
     Silence is added structurally, proportions of the authored rhythm preserved.
   - Mastering: pitch-preserving `atempo 0.93` (floor 0.88) + low shelf +1.5 dB @180 Hz +
     −2 dB @7 kHz + gentle 2.5:1 compression + loudnorm to −20 LUFS (TP −2, LRA 7) → mono 44.1 kHz.
   - Never raw-stretch audio to lengthen it. Length comes from words + authored breaks.
4. **Target runtime 45:00** per episode — a goal, not a gate. Short episodes ship; texts get
   lengthened later by adding whole new sections (never longer sentences).
   `Stories/word-targets.csv` has per-story word counts needed at each voice's measured pace.
5. **File naming per story** (`Stories/<storyID>/`):
   - `audio/polly-<Voice>-raw.mp3` — raw Polly output, 24 kHz mono (archival source)
   - `audio/master.wav` — mastered, 44.1 kHz 16-bit mono PCM
   - `audio/delivery.m4a` — mastered, AAC-LC 44.1 kHz mono 96 kbps (app upload format)
   - `_generated/polly.ssml` — the exact SSML sent to Polly
6. **Story→category mapping** — approved list at the bottom of `casting.yaml`.
7. **the-rings-of-saturn** was re-voiced with Amy (AV approved) — new local audio exists,
   but Supabase still serves the old ElevenLabs audio until a publish-pipeline push.
8. ElevenLabs-era audio was moved to `Stories/_to_delete/` (bridge cannot hard-delete);
   AV trashes that folder manually.

## Where everything lives (on the MacBook Air)

Root: `~/Documents/CLAUDE/02_LULLABLE/lullable_audio/`
- `Stories/<storyID>/` — one folder per episode: `story.yaml` (canonical manifest),
  `narration.md` (§-sectioned prose), `upload-to-elevenlabs.txt` (prose + `<break>` tags —
  despite the legacy name, this is now the Polly source too), `audio/`, `_generated/`
- `Stories/casting.yaml` — casting/recipe/naming config (canonical)
- `Stories/word-targets.csv` — per-story 45-min word targets
- `AWS_Polly/` — AWS credentials CSV (`lullable-tts_accessKeys.csv`), voice audition mp3s,
  and `tools/` (the render scripts + these docs)
- `Tools/lullable.py` — the pre-existing story pipeline (validate/build/tracker; 17 gates).
  The Polly render step is NOT yet integrated into it.

## AWS facts

- Account 864981744724, region **us-east-1**
- IAM user `lullable-tts` with AmazonPollyFullAccess + AmazonS3FullAccess;
  access keys in `AWS_Polly/lullable-tts_accessKeys.csv`
- S3 bucket for async render output: `lullable-audio-864981744724` (prefix `stories/<storyID>/`)
- Full episodes MUST use `StartSpeechSynthesisTask` (async → S3): sync SynthesizeSpeech
  caps at 3,000 billed chars, episodes are ~23,000. Async caps: 100k billed / 200k total.
- Polly bills text characters only; SSML tags are free. `<break>` max 10s. Task APIs for
  generative/long-form voices are throttled to ~1 request/second — pace submissions.
- Cost reference: neural $16 / generative $30 / long-form $100 per 1M chars ⇒ roughly
  $0.37 / $0.70 / $2.30 per episode.

## Status snapshot (2026-08-20)

18 of 20 stories fully rendered and delivered per the naming convention (~11.1 h audio, ~$14).
Pending: `aristotle-the-greatest-philosopher` (Emma) and `dinosaurs-from-rule-to-ruin`
(Arthur) — narration texts being written now; both are legacy-published episodes whose old
Supabase audio must eventually be replaced through the publish pipeline. Word targets:
~4,600 (Emma) / ~5,000 (Arthur). Six new stories planned next, from YouTube-referenced
sample texts (see CLAUDE-INSTRUCTIONS.md §New stories).
