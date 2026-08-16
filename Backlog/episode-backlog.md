# Episode backlog

The one queue. Absorbed `Lullable_audio_pipeline.xlsx`, which has been deleted (D23).

A topic lives **here or in the tracker, never both**. Scaffolding moves it across.
Once it has a folder it is a story, and `lullable.py status` is the live picture.

**Status values:** `idea` → `researching` → `in production` (has a folder) →
`shipped` (remove from here; it lives in `Stories/`).

Every episode runs **45–65 minutes**, ~4,600–5,200 words (D24). `compile` refuses
outside that band. There are no ambient beds and there never will be.

---

## In production

| Story | Pillar | Genre | Blocking |
|---|---|---|---|
| floating-through-the-pillars-of-creation | 1. Cosmology | cosmic-journeys | written, 49.7 min — needs render |
| the-moons-of-jupiter-europa-s-ice-and-ocean | 1. Cosmology | cosmic-journeys | written, 46.8 min — needs render |
| voyager-1-a-journey-to-interstellar-space | 1. Cosmology | cosmic-journeys | written, 46.7 min — needs render |
| the-life-cycle-of-a-red-dwarf-star | 1. Cosmology | cosmic-journeys | written, 47.1 min — needs render |
| mapping-the-cosmic-web | 1. Cosmology | cosmic-journeys | written, 47.1 min — needs render |
| the-joinery-of-japan-s-wooden-temples | 2. Ancient History | ancient-worlds | written, 46.3 min — needs render |
| the-slow-life-of-a-redwood | 3. Earth Science | gentle-nature | written, 45.8 min — needs render |
| the-midnight-sleeper-train-across-the-alps | 4. Immersive Journeys | cozy-tales | written, 47.2 min — needs render |
| a-roman-bathhouse-at-closing-time | 2. Ancient History | ancient-worlds | written, 47.2 min — needs render |
| the-journey-of-a-glacial-river | 3. Earth Science | gentle-nature | written, 45.5 min — needs render |
| the-building-of-a-cathedral | 2. Ancient History | ancient-worlds | written, 47.7 min — needs render |
| the-bay-that-glows-at-night | 3. Earth Science | gentle-nature | written, 46.1 min — needs render |
| the-clockmaker-s-workshop | 4. Immersive Journeys | cozy-tales | written, 47.1 min — needs render |
| the-deep-ocean-trenches | 3. Earth Science | gentle-nature | needs render · 43.2 min accepted as final (D25) · **no `narration.md` on disk** |
| the-great-library-of-alexandria | 2. Ancient History | ancient-worlds | needs render |
| the-bakery-before-dawn | 4. Immersive Journeys | cozy-tales | needs render |
| the-observatory-on-ben-nevis | 4. Immersive Journeys | cozy-tales | needs render |

Shipped: `the-rings-of-saturn` (published).

> The five stories that pre-date the pillar rename keep their old `pillar` strings.
> Settled, not pending — see D26. New episodes use the four pillars below.

---

## The four pillars

| Pillar | genreID |
|---|---|
| 1. Cosmology for Sleep | `cosmic-journeys` |
| 2. Ancient History & Gentle Lore | `ancient-worlds` |
| 3. Earth Science & Nature | `gentle-nature` |
| 4. Immersive Journeys & Slow Fiction | `cozy-tales` |

Pillars are editorial and free text. `genreIDs` is a hard enum of four and G03
rejects anything else. A fifth genre is a product decision, not a writing one.

---

## Ideas — 1. Cosmology for Sleep

| Topic | Angle | Notes |
|---|---|---|
| The Moon, close up | Regolith, low gravity, silence | Familiar and easy to picture |
| A comet's long orbit | Ice, sublimation, returning | Time-scale calm |
| Inside a nebula | Dust, slow collapse, colour | Needs care to stay non-dramatic |
| Titan's methane lakes | Orange haze, slow rain, thick air | Strong sensory lane |

## Ideas — 2. Ancient History & Gentle Lore

| Topic | Angle | Notes |
|---|---|---|
| Building the Silk Road trading post | Evening in a caravanserai, high desert stars | From the pipeline sheet |
| The craft of medieval bookbinding | Parchment, thread, leather tooling, scriptorium | Craft mechanics are excellent |
| Lighthouses of the ancient Mediterranean | Pharos, the quiet watch, coastal beacons | Watch that the watch reads calm, not lonely |
| How papyrus and parchment were made | Material craft | Overlaps Alexandria — check before writing |

## Ideas — 3. Earth Science & Nature

| Topic | Angle | Notes |
|---|---|---|
| The formation of cloud forests | Mist, elevation, self-sustaining canopy | From the pipeline sheet |
| Geology of the Appalachians | Deep time turning peaks into ridges | Erosion is the calmest possible plot |
| The winter migration of monarchs | Continents crossed, resting in fir forests | Avoid the population-decline angle |
| How a coral reef is built | Polyps, calcium, time | Zero-conflict if predation is left out |
| The inside of a glacier | Blue ice, meltwater, compression | Cold + spacious |
| A night in a temperate forest | Owls, moss, soil, dew | Close-range, low-drama |

## Ideas — 4. Immersive Journeys & Slow Fiction

| Topic | Angle | Notes |
|---|---|---|
| A rainy evening in a coastal timber cabin | Woodsmoke, hearth, waves on rock | Pure atmosphere; needs a factual spine |
| Sailing a wooden schooner across an atoll | Rigging creak, turquoise water, trade winds | Keep the weather kind |
| The gardener's greenhouse in autumn | Soil, winter bulbs, rain on panes | Warm and tactile |
| A pottery studio | Clay, wheel, kiln, glaze chemistry | Strong factual body |
| A wool mill | Fleece to yarn, machines, lanolin | Warm and tactile |

---

## Rejected, and why

Kept so they do not get re-proposed.

| Topic | Why not |
|---|---|
| Shipwrecks | Death emphasis, unavoidable |
| Volcanoes erupting | Drama and danger are the whole subject |
| Polar expeditions | Survival jeopardy |
| Predators of the deep | Hunting is the story |
| The space race | Competition, countdowns |
| 3-hour ambient beds | Not a story. Second pipeline, second rights surface, zero catalogue (D24) |

---

## Before writing any of these

1. Check the pillar balance — prefer the thinnest, unless deliberately going deep.
2. Confirm no heavy overlap with a story already in `Stories/`.
3. Confirm the factual body can carry 45+ minutes without drama.
4. Scaffold: `.venv/bin/python3 Tools/lullable.py new "<Title>" --genre <genre> --pillar "<pillar>" --id <n>`
