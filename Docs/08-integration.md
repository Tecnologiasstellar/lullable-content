# How this folder sits next to the rest of Lullable

Verified by inspection on 2026-08-13, with access to the whole `LULLABLE/`
directory. Facts here were checked, not assumed.

## What is actually in `~/Documents/CLAUDE/LULLABLE/`

```
LULLABLE/                                  ← NOT a git repository
├── llulable_website/          41 MB       the marketing site + story catalog  ← IS a git repo (14 commits)
├── llulable_website.EMPTY-BACKUP-…  92 KB a backup, also a git repo
├── llulable_content/           0 B        empty
└── lullable_audio/           992 KB       this content system  ← NOT in any repo
```

The iOS app codebase is **not** in this directory.

---

## The repository question — resolved

**`lullable_audio` is not inside any git repository.** `LULLABLE/` has no
`.git`; the only repos are `llulable_website/` and its backup, both siblings.

So the audio-bloat risk does not currently apply. Nothing this system produces
can enter the website's history.

**It would apply** the moment anyone runs `git init` at the `LULLABLE/` level.
The `.gitignore` in this folder is kept as insurance: it excludes
`Stories/*/audio/`, every audio extension, and the regenerable `_generated/`
folders. Git honours nested ignore files, so the protection activates
automatically if a parent repo ever appears.

For reference: a 45-minute WAV master is ~240 MB. Twenty episodes is ~4.8 GB.
Masters belong in cloud storage; delivery files belong in Supabase.

**No interference with the website build.** `llulable_website/build.py` resolves
everything from `ROOT = Path(__file__).parent` and globs only `posts/`,
`catalog/` and `legal/` beneath itself. It cannot see this folder. There is no
Xcode project, no bundler, and no glob that reaches sideways.

---

## `edge-of-saturn` — not found

Zero matches for "saturn" anywhere in `llulable_website`. The string
`edge-of-saturn` does not exist in any file in this directory.

That does not resolve D11, because **the iOS app is not here**. The ID either
lives in the app's own codebase or in Supabase. Until someone checks one of
those, `the-rings-of-saturn` stays blocked at G02, which remains the safe
outcome.

---

## The real finding: two catalogs, two schemas

This is the thing worth acting on.

`llulable_website/catalog/` contains **six stories** that this system has never
seen, and there is **no overlap** with the four here.

| | Website `catalog/*.md` | This system `story.yaml` |
|---|---|---|
| Stories | 6 | 4 |
| Duration | `mins: 42` | `durationSeconds`, measured from the file |
| Access | `premium: true/false` | `accessDecision` + derived `access` |
| Genre | `Folklore`, `Nature & Weather`, `Slow Fiction`, `Wandering` | `ancient-worlds`, `gentle-nature`, `cosmic-journeys`, `cozy-tales` |
| Mood | `mood: Drifting` | `sleepPace` + `atmosphere` (two fields) |
| Copy | `blurb`, `sample` | `subtitle`, `bedtimeNote`, `description` |
| Narrators | Nora Vance, Ilya Sorensen, Marguerite Bell | all `PENDING` |
| Audio | none (only `audio/sample-aristotle.mp3`) | none yet |

**The genre vocabularies do not intersect at all.** A listener browsing the
website sees four genres; a listener in the app would see four different ones.

Neither catalog knows the other exists. This is the same "several copies of the
truth" problem that D6 solved *inside* this system, now recurring one level up.

---

## The convergence worth noticing

`llulable_website/build.py` was written independently and arrived at the same
principles:

> *"The generator (human or Claude) writes prose into typed slots. THIS script
> assembles pages, schema, and feeds — structure is never left to generation."*
>
> *"Hard gates for expensive failures (medical/sleep claims), warnings for cheap
> ones. Hard failures abort the whole build, loudly, before anything is
> written."*

That is our manifest-and-gates design, in a different medium. The two systems
are already philosophically compatible, which makes unifying them a schema
exercise rather than a rewrite.

### Cross-check already run

The website's `prohibited_claims_in()` gate — which blocks "cures insomnia",
"clinically proven", "dosage" and similar — was run over all four narrations and
all four sets of card copy in this system.

**Result: clean, every one.** The house-voice rule in `02-house-voice.md` and the
website's claim gate agree in practice. Worth re-running before any episode
ships, since the website's list is the more legally-motivated of the two.

---

## If the two systems are ever unified

The mapping is mechanical, and this system is the more precise of the two — it
measures duration rather than declaring it, and separates production status from
commercial tier.

| Website field | Comes from |
|---|---|
| `title`, `narrator` | `card.title`, `card.narrator` |
| `mins` | `round(card.durationSeconds / 60)` |
| `premium` | `accessDecision == "premium"` |
| `date` | `card.publishedAt` |
| `blurb` | `card.subtitle` |
| `mood` | `card.atmosphere` |
| `genre` | needs a decision — the vocabularies do not map |

The genre question is the only real work: either the app adopts the website's
four, the website adopts the app's four, or an explicit mapping table is agreed.
It is a product decision, not a technical one.

A `lullable.py website-export` command could then generate `catalog/*.md` from
the manifests, making this system the source for both surfaces — exactly what
D6 did for the tracker.

---

## The coupling that matters

Not files — **story IDs and schema.**

- A published `storyID` becomes the key favorites and progress hang off. It can
  never change afterwards.
- `_generated/catalog-<env>.sql` is the actual upsert against the deployed
  `stories`, `audio_assets`, `genres` and `story_genres` tables.
- `sigil`, `glow_hex` and `base_hex` are app-side design columns. This pipeline
  reads and writes neither — they would be nulled on every republish if it did.

Keep that interface explicit and the halves can move independently.
