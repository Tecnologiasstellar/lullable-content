# The eighteen gates

`lullable.py validate --all`

Each gate returns PASS or FAIL with a message that names the problem. Gates are
**staged**: a story only has to pass the subset required at its current
`workflowStatus`. `PUBLISH READY` means all eighteen pass (or are n/a).

The point of the design: these check **reality, not typing**. G09 hashes the
actual bytes, G10 shells out to `ffprobe`, G11 compares the card against the
measured audio. A wrong number cannot pass by being confidently entered.

---

## Which gates apply at which stage

| Stage | Required gates |
|---|---|
| `draft` | G01 G02 G03 G04 G05 G15 G17 |
| `rendered` | + G08 G09 G10 G11 G12 |
| `qa-approved` | + G13 |
| `staging` | + G16 G14 |
| `published` | all eighteen |

A fresh episode legitimately fails the audio gates. That is the system working.

---

## The gates

### G01 — manifest schema
Required top-level sections present, `schemaVersion` correct.
**Fix:** the manifest is malformed or hand-edited badly. Compare against a
working story's `story.yaml`.

### G02 — story identity
`storyID` matches `[a-z0-9-]{3,80}`, `identityResolved` is true, `supersedes` is
a valid ID and not equal to `storyID`.
**Fix:** decide whether the story replaces an existing card or is new, set
`storyID` accordingly, then `identityResolved: true`.

### G03 — allowed values
Every enum legal, every boolean an actual boolean (not the string `"true"`).
**Fix:** the message names the offending field and value.

### G04 — card copy lengths
All eight copy fields within editorial targets.
**Fix:** rewrite the field. Do not stretch the target. `narrator` is exempt while
the story is a draft.

### G05 — artwork colours
`colorHex` and `accentHex` are exactly six uppercase hex characters, no `#`.

### G06 — publish date
Strict ISO-8601 UTC: `2026-09-15T16:00:00Z`. A bare date fails.

### G07 — no placeholders
Nothing anywhere still reads `PENDING`, `VOICE_ID`, `TODO`, `XXX`, `CHANGEME`.
**Fix:** the message lists every path. Five are expected pre-render.

### G08 — files on disk
`audio/<master>` and `audio/<delivery>` exist, plus any file listed in
`rights.evidenceFiles`.
**Fix:** put the files in the story's `audio/` folder and re-run `closeout`.

### G09 — audio checksums
Recorded `sha256` matches the actual bytes, for both files.
**Fix:** if this fails after the files were replaced, re-run `closeout`. If it
fails unexpectedly, the audio changed without anyone recording it — **mint a new
`audioAssetID`**, since the old ID no longer describes these bytes.

### G10 — delivery encoding
Really AAC-LC, 44.1 kHz, mono, 58–140 kbps (96 nominal). Master must be
uncompressed PCM.
**Fix:** re-export from the approved master at the right settings.

### G11 — duration matches audio
`card.durationSeconds` equals the measured delivery duration within 1 second.
**Fix:** run `closeout`, which sets it from the file. Never type a duration.

### G12 — render manifest
Voice id, voice name, model, history item id and rendered-at all recorded;
model is v2-family; stability and similarity captured.
**Fix:** re-run `closeout` with the missing flags. If the model is v3, the render
itself is wrong — v3 ignores break tags, so the pauses are gone. Re-render.

### G13 — QA and device sign-off
`audioApproved` with a named approver and ISO timestamp, plus `deviceAccepted`.
**Fix:** listen to the whole thing on a real phone, then run `approve --device`.

### G14 — staging landed
`audioAssetID`, `bucketID` and `objectPath` minted, and
`publish.staging.uploadedAt` / `rowUpsertedAt` recorded.
**Fix:** `publish <story> --env staging`.
Reports **n/a**, not a failure, for stories carrying
`publish.legacyDirectToProduction: true` — the 26 that shipped before a staging
environment existed. See Docs/06-decisions.md D28. The flag is dropped the first
time a story actually goes through staging, and the gate starts applying to it.

### G18 — production landed
`publish.production.uploadedAt` / `rowUpsertedAt` recorded, **and**
`publish.staging.verifiedAt` non-empty.
**Fix:** `publish <story> --env staging`, `verify <story> --env staging`, then
`publish <story> --env production`.
That last condition is the whole point: production is only ever reached by
promoting something already proven in staging. `publish --env production`
refuses before it touches the network, so the error arrives in a readable form
rather than as a constraint violation.

### G15 — commercial rights
`rights.status` is `verified` and evidence is recorded.

### G16 — access decision final
`accessDecision` is no longer `PENDING`.
**Fix:** decide free vs premium. This is deliberately a separate decision from
production status.

### G17 — SSML integrity
Break tags only, opens on `Good evening.`, closes on `Goodnight.`, no section
marker leaked, no exclamation marks, words/break at or under 15.0.
**Fix:** re-run `compile`. If it refuses, split the sentences it names.

---

## Staleness warning

Not a gate, but `validate` prints it:

```
!! _generated/ is older than story.yaml — run lullable.py build <storyID>
```

The derived artifacts no longer match the manifest. Always `build` after editing
a manifest by hand.

---

## Proving the gates work

The gates were verified against a synthetic story with a real WAV master and a
real AAC-LC delivery. It passed all of them, then each fault was introduced
deliberately:

| Mutation | Caught by |
|---|---|
| one byte flipped in `delivery.m4a` | G09 checksum mismatch |
| card duration 2640s, audio 12s | G11, 2628s apart |
| model set to `eleven_v3` | G12 not v2-family |
| re-encoded 48 kHz stereo | G10 wrong rate and channels |
| `publishedAt` as a bare date | G06 not ISO-8601 UTC |
| `accessDecision` back to PENDING | G16 |
| genre typed as `made-up-genre` | G03 not an allowed value |
| device acceptance revoked | G13 |
| catalog row not upserted in staging | G14 |
| promoted to production with no staging verification | G18 |
| `master.wav` deleted | G08 missing file |

Re-run that test after any change to the gate logic.
