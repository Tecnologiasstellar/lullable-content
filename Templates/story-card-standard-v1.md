# Lullable story card standard v1

This is the final content brief for the story-detail screen: the screen with the title, subtitle, narrator and duration, `Why this story tonight`, three small tags, and `About this story`.

## The simple workflow

1. Create a new folder with the story ID, for example `the-moonlit-forest`.
2. Copy `story-card.template.yaml` into that folder and rename it `story-card.yaml`.
3. Replace every value marked `PENDING` with the final copy. Keep the field names exactly as written.
4. Put the approved narration master, rights evidence, and the completed card in the same folder before handoff. Do not upload audio to Supabase from this folder; we validate and publish it through the controlled release process.

Your working folder should look like this:

```text
99_Working_Files/Content_Cards/
  the-moonlit-forest/
    story-card.yaml
    narration-master.wav                 # final, rights-cleared master
    rights-evidence.pdf                  # invoice, license, or permission
```

## What appears on the Lullable screen

| Field | Where it appears | Required | Editorial target | Hard technical limit |
|---|---|---:|---:|---:|
| `title` | Main heading and catalog cards | Yes | 18–48 characters; ideally 2–7 words | 200 |
| `subtitle` | Under the title and catalog cards | Yes | 35–90 characters; one calm promise | 300 |
| `narrator` | `Narrated by …` | Yes | 2–32 characters | 160 |
| `durationSeconds` | `• 44 min`; measured from final audio | Yes | Do not guess; `PENDING` is allowed until audio is final | — |
| `bedtimeNote` | `Why this story tonight` | Yes | 90–180 characters; 1–2 sentences | 320 (our publishing rule) |
| `bestFor` | First small tag, with sparkles | Yes | 10–24 characters; a benefit, not a diagnosis | 28 (our publishing rule) |
| `sleepPace` | Second small tag, with moon | Yes | 8–22 characters | 24 (our publishing rule) |
| `atmosphere` | Third small tag, with cloud | Yes | 10–28 characters; 2–4 mood words | 30 (our publishing rule) |
| `description` | `About this story` | Yes | 220–650 characters; 2–4 short sentences | 4,000 |

The editorial targets are deliberately tighter than the database limits so the card remains calm, readable, and consistent on an iPhone.

## Fields that control catalog placement and access

| Field | Allowed value / format | Notes |
|---|---|---|
| `storyID` | lower-case letters, numbers, hyphens; 3–80 characters | Example: `the-moonlit-forest`. It never changes after publication. |
| `genreIDs` | 1–2 existing genre IDs | `ancient-worlds`, `gentle-nature`, `cosmic-journeys`, or `cozy-tales`. Ask before inventing a new one. |
| `access` | `free` or `premium` | Free is a public sample; Premium needs a verified entitlement before playback. |
| `trialPreviewEligible` | `true` or `false` | Use `false` unless we deliberately select this Premium story for the limited launch-trial catalogue. |
| `isFeatured` | `true` or `false` | Featured means it can be placed prominently on Home. Keep this `false` unless selected. |
| `publishedAt` | ISO date in UTC | Use `PENDING` until the scheduled release is approved. Example: `2026-09-15T16:00:00Z`. |
| `colorHex`, `accentHex` | six uppercase hexadecimal characters, no `#` | These make the current gradient card artwork. Example: `203D38` and `8CB7A5`. |

## Audio, rights, and publication facts

These fields protect Lullable commercially. They are not decorative copy.

| Field | Requirement |
|---|---|
| `audioAssetID` | `PENDING` until we create a new immutable delivery ID. Never reuse an ID if the audio bytes change. |
| `audioMasterFilename` | Exact original master filename, preferably WAV. |
| `commercialRightsStatus` | Must be `verified` before a story can be published. Use `pending-verification` until source text, voice, music/sound, and output licences are documented. |
| `rightsEvidence` | One plain-language sentence plus the filename(s) that prove commercial rights. |
| `audioDelivery` | Lullable delivery format is AAC-LC `.m4a`, 44.1 kHz, mono, 96 kbps. We generate and validate it from the approved master. |

## Copy rules

- Write in calm, sensory, sleep-safe language: quiet, soft, measured, spacious, gentle.
- Describe the experience; do **not** promise sleep, treat insomnia/anxiety, or make medical claims.
- Keep the title specific and memorable. Avoid SEO-style titles and quotation marks.
- Avoid repeating the exact title in the subtitle or description.
- The three tags should be short fragments, not sentences. They should still read well with their icon.
- Duration is determined by the final audio file, not the script estimate.
- Use U.S. English for launch cards. One card = one language. Localized copy will be a later, separate card.

## Design decision: no visual redesign is required now

The current design already has every customer-facing card field needed for launch. The only layout rule is important: the first two tags sit side by side on iPhone, so their hard caps above must be respected. With those caps, the current screen remains balanced without a design change.

Future optional upgrade: replace the generated gradient artwork with licensed, original per-story cover art. That would add `coverImage` and image-rights fields, but it is **not** required for the launch card system and should not delay content production.

## Engineering item before remote publication

The iPhone model already supports `bedtimeNote`, `bestFor`, `sleepPace`, and `atmosphere`. The current hosted Supabase catalog does not yet store or return those four fields, so remote cards would fall back to generic copy. Before the first remotely published card, we need one small, tested backend migration and catalog-RPC update to carry these fields through. Your completed `story-card.yaml` files are the source material for that update.

## Handoff checklist

- [ ] All required customer-facing fields are complete and within the target lengths.
- [ ] `durationSeconds` is measured from the final audio.
- [ ] `genreIDs`, access, and feature status are selected.
- [ ] Both color values are valid six-character uppercase hex values.
- [ ] Rights are documented and marked `verified`, or the story is kept as draft.
- [ ] Final narration master is present; a delivery file is not treated as proof of rights.
- [ ] `publishedAt` is approved, or remains `PENDING`.
