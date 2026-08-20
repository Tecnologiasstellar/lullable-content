# Decision log

Why the system is the way it is. Newest last. Two of these are reversals — kept
visible on purpose, because the reasoning matters more than the consistency.

---

## D1 — Editorial targets are tighter than database caps

The card has to stay calm and readable on an iPhone, and the first two tags sit
side by side. So `bestFor` is capped at 24 characters even though the column
holds 28, and 200-character titles are legal but useless.

**Consequence:** G04 enforces the editorial target, not the cap. A field over the
hard cap is reported separately as `OVER HARD CAP`.

---

## D2 — Duration is measured, never estimated

The compiler produces a runtime estimate. It is for planning only.

`card.durationSeconds` is written by `closeout` from the actual delivery file,
and G11 re-checks it against the file every time. An estimate on a card is a
wrong number that nobody will ever notice.

---

## D3 — Rights are verified by default

Lullable owns every input: scripts written in-house, narration rendered with
Lullable's own licensed ElevenLabs voice, no third-party text, music or sound.

So `rights.status` defaults to `verified` with a standing attestation, and there
is no per-episode rights investigation. This was previously a blocking checklist
item on every story, which was pure friction given the facts.

**Reverts if** an episode ever uses outside material — then back to
`pending-verification` with the real licence documented.

---

## D4 — The cadence gate refuses to write, and names the offenders

Words-per-break drifted upward across the first three episodes: 14.8 → 15.4 →
16.0. Nobody noticed, because nothing was watching.

A warning would have drifted too. The compiler now writes **nothing** above 15.0
and prints the twelve longest sentences, because "too long" is not actionable but
"these twelve sentences" is.

`--force` exists for a deliberate, explained exception.

**Evidence it was the right call:** the same gate immediately caught Alexandria
at 15.4, a pre-existing defect the spreadsheet could never have seen.

---

## D5 — Shorter sentences make longer episodes

Discovered while fixing D4, and worth stating because it is counter-intuitive.

Splitting 30 long sentences in Episode 16 took it from 16.0 to 13.7 words/break —
and the runtime went **up**, because more sentence breaks means more engineered
silence.

Shortening sentences is not a cost. It buys both cadence and length.

---

## D6 — The manifest is canonical; everything else is generated

The same facts previously lived in a spreadsheet, a YAML file, a TSV, a JSON
record and several script variants, kept in sync by hand. That always fails
eventually.

`story.yaml` is now the single source of truth. The tracker row, story card,
Supabase payload, Neon record and publish commands are all derived. The Excel
workbook became a **report**, not a form.

**Consequence:** editing the spreadsheet does nothing — it is overwritten on the
next `tracker` run.

---

## D7 — YAML is emitted by a parser, never a formula

The spreadsheet formula that built the card YAML did not escape quotes or
newlines. A description containing a double quote — entirely plausible in copy
about *"the singing loaf"* — would have produced invalid YAML that failed
silently downstream.

Generation moved into Python with PyYAML. Verified by round-tripping a
description containing quotes, newlines, tabs, colons, a hash and a backslash.

---

## D8 — Workflow status is separate from access tier

`access` was a single field, which meant a story could sit at `premium` before
anyone had decided that. Saturn did.

Split into `workflowStatus` (production) and `accessDecision` (commercial). The
`access` value the app sees is **derived** and stays `PENDING` until the story
reaches `staging` with a decision made.

Nothing can go live under a tier nobody chose.

---

## D9 — Gates check files, not fields

The old "publish ready" formula checked that cells were non-empty and
well-spelled. It could not tell whether the audio existed, whether it was the
right encoding, or whether the duration on the card matched the file.

The gates hash the bytes, run `ffprobe`, and compare the card against
the measurement. Verified with ten deliberate mutations, each caught by exactly
the gate that should catch it.

---

## D10 — Excel dropdowns now block, rather than advise

The data validation lists existed but had error-blocking switched off, so an
invalid typed value passed silently. Now `showErrorMessage=True, errorStyle=stop`.

Largely belt-and-braces since the sheet is generated, but a human will eventually
type in it anyway.

---

## D11 — Story identity is blocked, not guessed  *(open)*

The app carries a card with storyID `edge-of-saturn`. The new Saturn narration
might replace it or might be additional. A storyID never changes after
publication, because favorites and progress hang off it — so guessing wrong
silently orphans user data.

`the-rings-of-saturn` is therefore marked `identityResolved: false` and **fails
G02 on purpose**. The catalog payload refuses to build.

**Still open.** Resolve by setting `storyID` to the intended value and
`identityResolved: true`.

---

## D12 — Code lives in the folder, not the skill  *(reversal of D12-a)*

**D12-a, earlier:** when the tooling was a ~100-line compiler, it lived only
inside the Claude skill. A copy in the folder would go stale, and the skill is
what actually runs.

**D12-b, now:** at 1,030 lines that reasoning no longer holds. A script this size
cannot be reliably reproduced from a document, and it needs to be versioned
alongside the data it validates. It lives at `../Tools/lullable.py`; the skill
describes the workflow and calls it.

The principle did not change — one copy, no duplicates. What changed is which
location can honestly hold it.

---

## D13 — Bitrate is a band, not a tolerance

G10 originally required 96 kbps ±24. A test render came back at 46 kbps and
failed — correctly by the letter, but the signal was a pure sine tone, which
compresses far below nominal.

Real VBR AAC on speech drifts too. The check is now a band of 58–140 kbps, which
still catches the mistakes that matter (a 32 kbps delivery, a 320 kbps stereo
export) without failing normal encoder variation. Codec, profile, sample rate and
channel count remain strict.

---

## D14 — `validate` warns when generated files are stale

Found while testing: editing a manifest by hand and then validating gives a green
result against **stale** derived files. The catalog payload still said
`access: PENDING` after the story had moved to published.

`validate` now compares mtimes and prints a warning, and exits non-zero in
`--strict` mode.

---

## D15 — Verified: this folder is outside the git repo

Checked with access to the whole `LULLABLE/` directory. `LULLABLE/` itself is not
a repository; the only repos are `llulable_website/` and its backup, both
siblings of this folder. Nothing here can enter the website's history.

The `.gitignore` stays as insurance — it activates automatically if anyone ever
runs `git init` at the `LULLABLE/` level, and git honours nested ignore files.

Also confirmed: `llulable_website/build.py` resolves everything from its own
directory and globs only `posts/`, `catalog/` and `legal/` beneath itself. There
is no Xcode project and no build step that can reach sideways into this folder.

---

## D16 — Two catalogs exist, and they do not agree  *(open)*

`llulable_website/catalog/` holds six stories this system has never seen. There
is no overlap with the four here, and the genre vocabularies do not intersect at
all: the website uses `Folklore`, `Nature & Weather`, `Slow Fiction`,
`Wandering`; this system uses `ancient-worlds`, `gentle-nature`,
`cosmic-journeys`, `cozy-tales`.

The website also declares `mins` rather than measuring duration, and carries a
single `premium` boolean rather than separating production status from
commercial tier — both problems this system has already solved (D2, D8).

This is D6's "several copies of the truth" recurring one level up.

**Still open.** The technical mapping is mechanical; the genre vocabulary is a
product decision. A `lullable.py website-export` command could make the manifests
the source for both surfaces once that decision is made.

---

## D17 — `edge-of-saturn` is not in this directory

Zero matches for "saturn" anywhere in `llulable_website`. The iOS app codebase is
not in `LULLABLE/`, so D11 cannot be resolved from here — the ID lives either in
the app repo or in Supabase.

D11 stays open and `the-rings-of-saturn` stays blocked at G02.

---

## D18 — The website's claim gate agrees with our house voice

`llulable_website/build.py` carries a `prohibited_claims_in()` hard gate for
health claims — "cures insomnia", "clinically proven", "dosage" and similar, with
a 40-character negation lookback so myth-debunking passes.

That gate was run over all four narrations and all four sets of card copy here.
**Clean, every one.** The sleep-safe rule in `02-house-voice.md` and the
website's legal gate agree in practice.

Worth re-running before any episode ships, since the website's list is the more
legally-motivated of the two and is maintained separately.

---

## D19 — The app's four genres are canonical

Two vocabularies existed. The website used `Folklore`, `Nature & Weather`,
`Slow Fiction`, `Wandering`; this system used `ancient-worlds`,
`gentle-nature`, `cosmic-journeys`, `cozy-tales`. They did not intersect.

**The app's four win.** They are spatial rather than literary — they describe
where the listener is, not what kind of story it is, which is the axis a person
actually browses on at bedtime.

Display names on the website:

| genreID | Website display |
|---|---|
| `gentle-nature` | Gentle Nature |
| `ancient-worlds` | Ancient Worlds |
| `cosmic-journeys` | Cosmic Journeys |
| `cozy-tales` | Cozy Tales |

`build.py`'s scaffold comment still lists the old four. It is only a comment in
a template, so nothing breaks, but it should be updated when the website next
gets touched.

---

## D20 — The website catalog is generated from these manifests

`lullable.py website-export` writes `llulable_website/catalog/<storyID>.md` from
the manifest, in the exact frontmatter the site's `validate_story()` requires.
Verified: a generated page passes the website's own validator with **zero errors
and zero warnings**, including its claim gate and its "sample must end on an
em-dash" rule.

Field mapping:

| Website | From |
|---|---|
| `title`, `narrator` | `card.title`, `card.narrator` |
| `mins` | `round(card.durationSeconds / 60)` — measured, never estimated |
| `genre` | display name of `card.genreIDs[0]` |
| `mood` | matched from `atmosphere` / `sleepPace` against the site's six moods |
| `premium` | `accessDecision == "premium"` |
| `date` | `card.publishedAt` |
| `blurb` | `card.bedtimeNote` |
| `sample` | a mid-body sentence, truncated on a word boundary, em-dash appended |
| body | `card.description`, the narration's opening ~100 words, and the bedtime note |

**The export refuses** a story with no measured duration, no assigned narrator,
no publish date, or an unresolved identity. A public page must never carry an
invented runtime. All four stories are correctly blocked today.

---

## D21 — The six website stories are aspirational and will be retired  *(open)*

`llulable_website/catalog/` holds six stories with narrators and runtimes that no
audio was ever made for, and none will be. They are marketing.

They are also **live and indexed**: six directories under `stories/`, tracked in
git, and present in `sitemap.xml`.

**Deleting them is an SEO action, not a file operation.** Removing indexed URLs
without redirects produces six 404s. The site has no `vercel.json` or
`_redirects` file today, so a redirect rule would need to be added.

Recommended sequence, not yet executed:

1. Render and ship at least one real episode.
2. `lullable.py website-export --all` to generate its page.
3. Add 301 redirects from the six retired slugs to `/stories/`.
4. Delete the six `catalog/*.md` files and their `stories/<slug>/` directories.
5. Rebuild; the sitemap regenerates from what exists on disk.

Doing step 4 before step 1 leaves the story catalog empty, which is worse than
leaving the aspirational pages up.

---

## D22 — The tool runs from a local virtualenv  *(settled 2026-08-14)*

`Tools/lullable.py` imports `pyyaml`, and `tracker` additionally imports
`openpyxl`. Neither system interpreter on this Mac has them:

- `/usr/bin/python3` — no pyyaml
- `/opt/homebrew/bin/python3` — no pyyaml, and refuses `pip install` under
  PEP 668 (externally managed environment)

So the folder carries its own `.venv/`, and every command is run as
`.venv/bin/python3 Tools/lullable.py …`. Rebuild with:

```
python3 -m venv .venv && .venv/bin/python3 -m pip install pyyaml openpyxl
```

The alternative — `pip install --break-system-packages` — was rejected because
it mutates the Homebrew interpreter that other projects on this machine use.

`.venv/` is local state, not source. It should not be committed if this folder
is ever put under version control.

---

## D23 — One system, one spreadsheet, one queue  *(settled 2026-08-15)*

A second workbook, `Lullable_audio_pipeline.xlsx`, appeared carrying a 20-episode
plan. It was deleted, and its topics moved into `Backlog/episode-backlog.md`.

Two spreadsheets means two answers to "what is the state of this story," and the
second one is always the stale one. The roles are now fixed:

| Role | The one thing |
|---|---|
| Truth | `Stories/<storyID>/story.yaml` |
| Report | `Lullable_Story_Card_Tracker.xlsx` — one sheet, generated |
| Control | `Tools/lullable.py` |
| Queue | `Backlog/episode-backlog.md` |

The truth is not, and cannot be, a spreadsheet: G09 hashes real bytes, G10 runs
`ffprobe`, G11 compares the card against measured audio. A workbook cannot check
reality, so it can only ever report it.

A topic lives in the backlog **or** the tracker, never both. Scaffolding moves it
across. That is what keeps them from disagreeing.

The tracker's "Read Me" sheet was dropped in the same pass. It duplicated
`START_HERE.md`, and its one load-bearing sentence — *this is a report, not a
form* — is already row 1 of the data sheet.

---

## D24 — Episodes run 45 to 65 minutes. No ambient beds.  *(settled 2026-08-15)*

The pipeline workbook proposed a `10-30m Story + 3hr Ambient` format. Both halves
were rejected.

**Runtime is 45–65 minutes**, enforced by `compile`, which now refuses to write
outside that band alongside its existing checks on words/break and exclamation
marks. At this cadence minutes ≈ words × 0.0109, so the band is roughly
4,150–6,000 words. Write to 4,600–5,200.

Enforcing it in `compile` rather than adding an eighteenth gate was deliberate.
`compile` is where the number is computed and where the writer is standing; a
gate would report the problem hours later, in a spreadsheet.

**There are no ambient beds.** Not 3-hour, not any length. A Lullable episode is
a narrated story and nothing else. Ambient audio is a second production pipeline,
a second asset type, a second set of rights questions and a second thing to keep
in one head — bought against a catalogue that has published exactly one episode.

This is recorded here so it does not return as a good idea in six weeks.

---

## D25 — Runtime exceptions live in the manifest, not in memory  *(settled 2026-08-15)*

`the-deep-ocean-trenches` runs 43.2 minutes, below the 45-minute floor set in D24.
AV accepted it as final rather than padding it.

A settled exception needs somewhere to live, or the next person to run `compile`
re-opens a closed question. `--force` was rejected for this: it is a flag someone
has to remember, it leaves no record of who decided or why, and it also silences
the words/break and exclamation-mark checks, which should stay live.

So the exception is data:

```yaml
episode:
  runtimeExempt: true
  runtimeExemptNote: 43.2 min accepted as final by AV, 2026-08-15. Do not pad.
```

`compile` reads it, skips only the runtime band, prints the note so the exception
is visible on every run, and leaves every other check enforced. The flag lives
under `episode:`, which `compile` preserves — `script:` is overwritten on every
compile and would have lost it.

**Use this sparingly.** One story carries it today. If a third or fourth appears,
the band is wrong and D24 should be revisited instead.

---

## D26 — Pillar strings on pre-rename stories are left alone  *(settled 2026-08-15)*

The five stories written before the pillar rename still carry the old strings:
`3. Earth Science & Nature`, `4. Space & Cosmic Journeys`, `5. History & Human
Ingenuity`, `6. Craft & Quiet Work`.

They stay. `pillar` is free text, no gate reads it, and `the-rings-of-saturn` is
published — rewriting a published manifest for an editorial label would mean
re-publishing for no user-visible gain. New episodes use the current four pillars.

---

## D27 — Legacy staging rows adopted into the manifest pipeline  *(settled 2026-08-19)*

Staging Supabase carried three published rows that predated this pipeline:
`aristotle-the-greatest-philosopher` (free), `dinosaurs-from-rule-to-ruin`
(premium) and `the-bakery-before-dawn` (published free 2026-08-16 while its
manifest still said draft). App-repo DECISIONS.md §19 (founder, 2026-08-16)
decided adoption over archival. This pass executed it: all three now have
manifests whose audio blocks were computed by `closeout` from the actual bytes.

The adopted delivery files are **byte-identical to the uploaded assets** — the
masters still existed, and re-encoding with the recovered importer recipe
(ffmpeg native AAC, `aac_low`, 44.1 kHz mono 96k, `+faststart`) reproduced the
recorded sha256s exactly (`c57bee52…` aristotle, `c8ee4c8e…` dinosaurs; bakery's
prepared delivery matched `13ae9d81…` without re-encoding).

All three sit at `workflowStatus: staging` — true: the rows are live on staging —
with their real gaps visible instead of hidden: G12/G07 (render provenance was
never recorded; voice/model/history unknown for the two legacy renders, model +
history-id missing for bakery), G13 (no QA device sign-off has ever happened),
and for the two legacy episodes G17 (no narration text exists in the pipeline;
the scripts were never in this system). These stories reach `published` the
normal way or not at all.

Adoption rule this establishes: a legacy episode is adopted by scaffolding with
`new --story-id <existing-id>` (identity is the published ID, never a new one),
placing the recovered master + delivery in `audio/`, and running `closeout` —
never by typing audio figures into YAML. Card copy may be brought up to
editorial targets in the manifest; the staging row catches up at the next
publish sync.

---

## D28 — Two Supabase environments, and a promote step that is actually enforced  *(settled 2026-08-20)*

Until today `workflowStatus: staging` was a label on a manifest, not a place.
D27 used the word "staging" loosely for exactly this reason: there was one
database, and everything published went straight into it. All 26 stories reached
production by hand-written SQL, unreviewed anywhere first.

There are now two projects, and the pipeline knows the difference:

| env | ref | name |
|---|---|---|
| staging | `lpzejlunebjogkfvzzdk` | lullable-staging |
| production | `wamsqjzstezqfpemhucm` | lullable-production |

Refs live in `Tools/environments.json`, so no ref is ever typed into a command.

**Staging was eight migrations behind.** It had 4 of 12 — no `bedtime_note`,
`best_for`, `sleep_pace`, `atmosphere`, no `sigil`/`glow_hex`/`base_hex`, and no
`database_environment` table. Publishing to it would have failed on the first
insert. The remaining eight were pushed from the app repo, and staging's
one-row `database_environment` was set to `sandbox` per app-repo DECISIONS §26.
Staging is now schema-identical to production: same 12 migrations, same 23
`stories` columns, same two buckets.

**The publish block is now two-environment.** The old shape recorded two
booleans and no timestamps:

    publish: {audioAssetID, supabaseAudioUploaded, catalogRowUpserted}

The new one records where the object is and when each environment took it:

    publish:
      audioAssetID / bucketID / objectPath    # identical in both environments
      staging:    {uploadedAt, rowUpsertedAt, verifiedAt}
      production: {uploadedAt, rowUpsertedAt, verifiedAt}

`bucketID` and `objectPath` for the 26 were read out of the live production
catalog, not derived, so the manifests record what is actually there.

**The backfill does not pretend.** The old schema never recorded upload times,
so they are not recoverable. `production.uploadedAt`/`rowUpsertedAt` were
backfilled from `card.publishedAt` — an editorial date standing in for an
unrecorded event, not a measurement — and `staging.*` was left empty for all 26,
because it is simply true that none of them ever passed through staging. Every
backfilled manifest carries `legacyDirectToProduction: true`, which is the
honest record of that bypass rather than a hole papered over with invented
timestamps. The flag is dropped the first time a story really goes through
staging, and G14 starts applying to it from then on.

**G14 was split and G18 added.** G14 is now "staging landed" (n/a for legacy
stories); G18 is "production landed", and it additionally requires
`staging.verifiedAt`. That single condition is the enforcement: production can
only be reached by promoting something already proven in staging. `publish --env
production` refuses before it touches the network so the error is readable.
G03 now validates the publish timestamps instead of the two removed booleans.

**Generated SQL replaced a payload that never matched the schema.**
`catalog_payload()` built a flat JSON body against columns that do not exist.
`catalog_sql(m, env)` emits the real thing, modelled on the hand-written publish
SQL that is known to work: a storage-object precheck, a genre upsert, the story
upsert, the audio-asset upsert, the genre links, the activation update, and a
post-publication assertion — all in one transaction. Every statement is
`ON CONFLICT DO UPDATE` (or `DO NOTHING`), because promoting to production means
running it against a row that already exists.

Three things it deliberately does not touch: `sigil`, `glow_hex` and `base_hex`
are owned by the app's design layer, appear in no manifest, and would be nulled
on every republish if this wrote them. `publication_status` is left out of the
story upsert's `DO UPDATE` so a live row is never momentarily demoted to draft.
Genre rows are `ON CONFLICT DO NOTHING` so publishing a story can never rewrite
the presentation of a genre that is already live.

**Storage objects are immutable.** `supabase storage cp` has no overwrite and
returns 409 when the key exists — which is the normal promote case, since the
bytes are already there. `publish` now checks the object first: absent, it
uploads; present with matching bytes, it skips; present with *different* bytes,
it refuses and says so. A re-render needs a new asset id, never a swap of bytes
underneath an id the catalog already points at.

**`--linked` is not optional** on every storage and db command. Without it the
CLI quietly addresses a local Docker shadow database instead of the project.
`supabase db query`, `storage cp` and `storage ls` have no `--project-ref` flag
in CLI 2.113.0, so `link` stays a separate step; storage commands additionally
require `--experimental`, and `db query` does not.

Both projects were renamed on 2026-08-20 (the old names were `lullable-production`
for what is now staging, and `sleep-stories-avp` for what is now production). A
rename changes only the dashboard label — ref, host and keys are untouched.

**Proven end to end** on `the-hidden-clocks-of-the-night-sky`: published to a
staging project that had never seen it (fresh insert), verified 11/11 against
the manifest, then promoted to production against the row that was already there
(`ON CONFLICT DO UPDATE`). Production's only actual change was gaining the
`story_genres` link it had been missing. The audit trigger fired in staging
(`story-created` + `publication-state-changed`) and correctly did not fire in
production, because `audit_story_publication_change()` guards on
`is distinct from` and none of the three audited columns changed.

**A gap this surfaced, since closed:** only 4 of 26 production stories had a
`story_genres` row — the hand-written publishes skipped the table entirely — and
the `gentle-nature` genre row had never been created anywhere. The 21 remaining
links were backfilled by `Tools/backfill_story_genres.py`, generated from
`card.genreIDs` rather than typed, every statement `ON CONFLICT DO NOTHING` so
the three genre rows that already existed kept their live presentation. All 26
stories are now linked, and each link was cross-checked against its manifest:
ancient-worlds 7, cosmic-journeys 8, cozy-tales 6, gentle-nature 5. Stories
published through `publish` fix their own link, so this script is a one-off for
the backlog, not part of the flow.

**The process from here.** `closeout` → `approve` (real device listen) →
`publish --env staging` → `verify --env staging` → look at staging →
`publish --env production` → `verify --env production`. Anything skipping
staging is refused by the tool, not by convention.
