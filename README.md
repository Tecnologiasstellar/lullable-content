# Lullable — content production system

Turns a topic into an upload-ready sleep narration plus every publishing
artifact, with a validator standing between the work and the catalogue.

**New here?** Read `START_HERE.md` — it explains the whole thing in plain
language. This file is the index.

---

## The folder

```
lullable_audio/
├── README.md                          this index
├── START_HERE.md                      plain-language guide
├── Lullable_Story_Card_Tracker.xlsx   a REPORT, generated. Do not type in it.
├── Lullable_Production_Process.pptx   the deck explaining the process
│
├── Docs/                              how the system works
│   ├── 01-pipeline-runbook.md         the seven stages, operationally
│   ├── 02-house-voice.md              the writing rules
│   ├── 03-manifest-reference.md       every story.yaml field
│   ├── 04-gates-reference.md          all 18 gates and how to fix each
│   ├── 05-genres-and-pillars.md       genre registry and palettes
│   ├── 06-decisions.md                why the system is like this
│   ├── 07-glossary.md                 every term, defined
│   └── 08-integration.md              how this sits next to the app
│
├── Backlog/episode-backlog.md         the topic queue
│
├── Templates/                         the original standard, for reference
│   ├── story-card-standard-v1.md
│   ├── story-card.template.yaml
│   └── narration-skeleton.md
│
├── Tools/lullable.py                  the one tool
│
└── Stories/<storyID>/
    ├── story.yaml                     ← THE ONLY FILE YOU EDIT
    ├── narration.md                   the story as written
    ├── upload-to-elevenlabs.txt       the story with pauses — upload this
    ├── script.md                      clean readable copy
    ├── audio/                         master.wav + delivery.m4a
    └── _generated/                    derived; never edit
```

---

## The one rule

`story.yaml` is the single source of truth. The tracker, the app card, the
Supabase payload and the publish commands are all generated from it. If two
things disagree, the manifest is right and the other is stale.

---

## Commands

Ask Claude to run these.

| Command | What it does |
|---|---|
| `new "<Title>" --genre <g> --pillar "<p>"` | Scaffold a new episode folder |
| `compile Stories/<id>` | Narration → SSML; refuses on bad cadence |
| `validate --all` | Run the 18 gates over every story |
| `status` | One-screen view of the whole catalogue |
| `build --all` | Regenerate every derived artifact |
| `tracker` | Rebuild the spreadsheet from the manifests |
| `closeout <id> --voice-id … --model …` | Fill render + audio blocks from the real files |
| `approve <id> --by "AV" --device` | Record QA and device sign-off |
| `publish <id> --env staging` | Upload the audio and upsert the catalog row in one environment |
| `verify <id> --env staging` | Check what actually landed there against the manifest |
| `website-export --all` | Generate the website's `catalog/*.md` from the manifests |

All take `--root .` from inside this folder. Full usage in
`Docs/01-pipeline-runbook.md`.

---

## The seven stages

```
Define → Research → Write → Compile → Structure → Validate → Ship
```

Human judgement lives in stages 1–3 and in QA sign-off. Everything between is
mechanical and repeatable.

---

## Two things kept apart

**`workflowStatus`** — `draft` → `rendered` → `qa-approved` → `staging` →
`published`

**`accessDecision`** — `PENDING` → `free` or `premium`

The `access` the app sees stays `PENDING` until a story reaches `staging` with a
decision made. Nothing goes live under a tier nobody chose.

---

## Open questions

Both recorded in `Docs/06-decisions.md`.

1. **Saturn's identity (D11).** The app carries a card called `edge-of-saturn`.
   If the new narration replaces it, reuse that ID so favorites and progress
   survive. `the-rings-of-saturn` fails G02 on purpose until this is settled.
2. **Runtime consistency (05).** Three episodes near 45 minutes, one at 23.
   Format inconsistency, or a useful short? It sets the word target for every
   future brief.

## Not in scope here

The app itself, and the Supabase schema. This repo generates the upsert
(`_generated/catalog-<env>.sql`) and runs it; the migrations that define the
columns live in the app repo.
