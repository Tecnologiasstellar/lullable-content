# Glossary

Plain definitions for every term this system uses.

---

**AAC-LC** — the audio format the app plays. "Low Complexity" AAC. Our delivery
spec is AAC-LC, 44.1 kHz, mono, ~96 kbps in an `.m4a` container. Small enough to
stream, good enough for a quiet voice.

**accessDecision** — the commercial question: is this episode `free` or
`premium`? Starts as `PENDING`. Kept deliberately separate from production
status.

**access** — what the app actually sees. **Derived**, never stored: it stays
`PENDING` until the story reaches `staging` with a decision made.

**audioAssetID** — the immutable ID for a specific set of audio bytes. If the
audio ever changes, mint a **new** ID. Reusing one means a listener's cached copy
no longer matches what the catalog claims.

**break tag** — `<break time="1.5s"/>`. The instruction that tells ElevenLabs to
pause. Roughly 1,100 of them across four episodes. Never hand-placed.

**card** — the story-detail screen in the app: title, subtitle, narrator,
duration, "Why this story tonight", three tags, "About this story".

**closeout** — the command run after a render. Reads the audio files, computes
checksums, measures duration and encoding, and fills the manifest. Nothing is
typed.

**delivery** — the `.m4a` file the app streams. Generated from the master.

**ffprobe** — the tool that reads real facts out of an audio file: codec, sample
rate, channels, bitrate, duration. Used by G10 and G11 so the gates measure the
file rather than trusting the manifest.

**gate** — one of eighteen automated checks. Each returns PASS or FAIL with a
message naming the problem.

**genreID** — one of four fixed values: `ancient-worlds`, `gentle-nature`,
`cosmic-journeys`, `cozy-tales`. A story carries one or two.

**hard cap** — the database column limit. Larger than the editorial target, and
not something to aim at.

**editorial target** — the length range copy should actually sit in, tighter than
the hard cap so the card stays readable on a phone.

**manifest** — `story.yaml`. The single source of truth for one episode. The only
file anyone edits.

**master** — the uncompressed `.wav` that comes back from the render. The
delivery file is generated from it. Never published directly.

**pillar** — an editorial grouping for planning, e.g. "4. Space & Cosmic
Journeys". Looser than a genre and not enforced by the app.

**seam** — a paragraph containing only `§` in the narration. Marks a section
boundary, and becomes a 3.0-second pause.

**sha256** — a fingerprint of a file's exact bytes. If one byte changes, the
fingerprint changes completely. This is how G09 proves the audio on disk is the
audio that was approved.

**SSML** — Speech Synthesis Markup Language. In our case, plain narration text
with break tags and nothing else.

**storyID** — the permanent identifier for an episode, e.g.
`the-rings-of-saturn`. Lowercase, hyphenated. **Never changes after
publication** — favorites and playback progress hang off it.

**supersedes** — the old storyID a new card replaces, recorded for traceability.

**v2-family model** — an ElevenLabs model that honours SSML break tags:
`eleven_multilingual_v2`, `eleven_english_v2`, `eleven_turbo_v2`,
`eleven_turbo_v2_5`. **v3 ignores break tags** and would silently discard every
pause in the file.

**words per break** — the cadence measure. Total spoken words divided by the
number of break tags. Target ~14; the compiler refuses to write above 15.0.

**workflowStatus** — where the episode is in production: `draft` → `rendered` →
`qa-approved` → `staging` → `published`.

**`_generated/`** — the folder of derived artifacts inside each story. Never
edited by hand; overwritten by `build`.
