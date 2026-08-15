# `story.yaml` — field reference

The canonical manifest. **The only file anyone edits.** Everything in
`_generated/` and every row of the tracker is produced from it.

After any change: `lullable.py build <storyID>` (and `tracker` to refresh the
spreadsheet). `validate` warns when the generated files are older than the
manifest.

---

## Identity

| Field | Type | Notes |
|---|---|---|
| `schemaVersion` | int | Currently `1`. G01 rejects anything else. |
| `storyID` | string | 3–80 chars, lowercase letters, digits, hyphens. **Never changes after publication** — favorites and progress hang off it. |
| `supersedes` | string / null | The old storyID this replaces, if any. |
| `identityResolved` | bool | Must be `true` to publish. |
| `identityNote` | string | Why identity is unresolved, if it is. Shown in the G02 failure. |

**The identity rule.** If a new narration replaces an existing card, reuse the
**old** storyID. If it is an additional story, mint a new one. When genuinely
unknown, set `identityResolved: false` with a note — G02 then blocks publication
and the catalog payload refuses to build. Never guess.

---

## Workflow and access

Deliberately two separate fields. They used to be one, which meant a story could
drift into being `premium` before anyone decided that.

| Field | Values |
|---|---|
| `workflowStatus` | `draft` → `rendered` → `qa-approved` → `staging` → `published` |
| `accessDecision` | `PENDING` → `free` or `premium` |

The `access` value the app sees is **derived**, never stored: it stays `PENDING`
until the story is at `staging` or `published` **and** a decision exists. Nothing
can go live under a tier nobody chose.

---

## `episode`

| Field | Notes |
|---|---|
| `id` | Episode number for the pipeline sheet. |
| `pillar` | Content pillar, e.g. `"4. Space & Cosmic Journeys"`. |
| `tags` | List of strings, for the Neon record. |

---

## `card` — what the listener sees

| Field | Target | Hard cap | Where it appears |
|---|---|---|---|
| `title` | 18–48 | 200 | Main heading, catalog cards |
| `subtitle` | 35–90 | 300 | Under the title |
| `narrator` | 2–32 | 160 | "Narrated by …" — set at render time, not authored |
| `genreIDs` | 1–2 items | — | From the four allowed genres |
| `bedtimeNote` | 90–180 | 320 | "Why this story tonight" |
| `bestFor` | 10–24 | 28 | First tag (sparkles) |
| `sleepPace` | 8–22 | 24 | Second tag (moon) |
| `atmosphere` | 10–28 | 30 | Third tag (cloud) |
| `description` | 220–650 | 4,000 | "About this story" |
| `colorHex` / `accentHex` | 6 chars | — | Uppercase hex, no `#` |
| `isFeatured` | bool | — | Home placement. Keep `false` unless chosen. |
| `trialPreviewEligible` | bool | — | Keep `false` unless deliberately selected. |
| `publishedAt` | ISO-8601 UTC | — | `2026-09-15T16:00:00Z`. `PENDING` until approved. |
| `durationSeconds` | int | — | **Written by `closeout` from the actual file.** Never type it. |

Editorial targets are tighter than the database caps on purpose — the card has to
stay calm and readable on an iPhone, and the first two tags sit side by side.

`narrator` is exempt from G04 while the story is a draft, because no voice has
been assigned yet.

---

## `script` — written by `compile`, do not edit

`narrationFile` · `ssmlFile` · `words` · `breaks` · `wordsPerBreak` ·
`silenceSeconds` · `estimatedMinutesAt118wpm`

The runtime figure is for planning only. The card's duration always comes from
the rendered file.

---

## `rights`

| Field | Notes |
|---|---|
| `status` | `pending-verification` \| `verified` \| `restricted` |
| `evidence` | One plain sentence describing what proves the rights. |
| `evidenceFiles` | Filenames in the story's `rights/` folder. Checked by G08. |

Default is `verified` with a standing attestation: scripts written in-house,
narration rendered with Lullable's own licensed voice, no third-party text, music
or sound. If an episode ever uses outside material, set it back to
`pending-verification` and document the real licence.

---

## `render` — written by `closeout`

| Field | Notes |
|---|---|
| `provider` | `elevenlabs` |
| `voiceId` / `voiceName` | The actual voice used. `VOICE_ID` is a placeholder and fails G12. |
| `model` | Must be v2-family: `eleven_multilingual_v2`, `eleven_english_v2`, `eleven_turbo_v2`, `eleven_turbo_v2_5`. **v3 ignores break tags.** |
| `settings` | `stability`, `similarityBoost`, `style`, `speakerBoost` — record what you actually used, so a re-render is reproducible. |
| `historyItemId` / `projectId` | ElevenLabs identifiers, so the exact render can be found again. |
| `renderedAt` | ISO-8601 UTC. |

---

## `audio` — written by `closeout`

Two blocks, `master` and `delivery`, each with `filename`, `sha256`, `bytes`,
`durationSeconds`, `codec`, `sampleRate`, `channels` (and `profile`,
`bitRateKbps` for delivery).

All of it is read from the files themselves via `ffprobe` and `hashlib`. **Never
copy these figures from a chat message or a filename.** The checksum is what
proves the bytes on disk are the bytes that were approved.

Delivery spec: AAC-LC, 44.1 kHz, mono, ~96 kbps (58–140 accepted, since VBR on
speech drifts). Master should be uncompressed PCM/WAV.

---

## `qa` — written by `approve`

`audioApproved` · `approvedBy` · `approvedAt` · `deviceAccepted` · `deviceNotes`

Two separate approvals on purpose. A render can be technically perfect and still
wrong in the ear — `deviceAccepted` means a person listened on a real phone.

---

## `publish`

| Field | Notes |
|---|---|
| `audioAssetID` | Immutable delivery ID. **Mint a new one if the audio bytes ever change.** |
| `supabaseAudioUploaded` | bool |
| `catalogRowUpserted` | bool |

---

## Anything marked `PENDING`

`PENDING`, `VOICE_ID`, `TODO`, `XXX` and `CHANGEME` are all treated as
placeholders. G07 fails on any of them at publish.

A fresh episode should have exactly five: `narrator`, `publishedAt`,
`durationSeconds`, `audioAssetID`, `audioMasterFilename`. More than five means a
copy field was left blank.
