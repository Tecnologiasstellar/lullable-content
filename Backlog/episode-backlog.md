# Episode backlog

The queue. Keep it stocked so writing never waits on deciding.

**Status values:** `idea` → `researching` → `in production` (has a folder) →
`shipped` (remove from here; it lives in `Stories/`).

Pick the next topic from whichever genre is thinnest. Ask Claude to run
`lullable.py status` for the live catalogue picture.

---

## In production

| Story | Genre | Status | Blocking |
|---|---|---|---|
| the-deep-ocean-trenches | gentle-nature | in production | needs render |
| the-great-library-of-alexandria | ancient-worlds | in production | needs render |
| the-rings-of-saturn | cosmic-journeys | in production | **identity unresolved (G02)**, then render |
| the-bakery-before-dawn | cozy-tales | in production | needs render |
| the-observatory-on-ben-nevis | cozy-tales | in production | needs render |

---

## Ideas — gentle-nature

| Topic | Angle | Notes |
|---|---|---|
| The slow life of a redwood | Fog, bark, root systems, centuries | Very strong lane fit |
| A river from source to sea | One continuous journey downstream | Natural 45-min structure |
| How a coral reef is built | Polyps, calcium, time | Zero-conflict if predation is left out |
| The inside of a glacier | Blue ice, meltwater, compression | Cold + spacious |
| A night in a temperate forest | Owls, moss, soil, dew | Close-range, low-drama |

## Ideas — ancient-worlds

| Topic | Angle | Notes |
|---|---|---|
| The building of a cathedral | Stone, scaffolding, generations | Craft + deep time |
| A Roman bathhouse at closing time | Water, heat, tile, quiet | Very sensory |
| The Silk Road at a waystation | Rest, trade goods, night | Warm and slow |
| How papyrus and parchment were made | Material craft | Partly used in Alexandria — check overlap |
| A medieval monastery scriptorium | Copying, lamplight, routine | Close cousin of Alexandria; space them apart |

## Ideas — cosmic-journeys

| Topic | Angle | Notes |
|---|---|---|
| The Moon, close up | Regolith, low gravity, silence | Familiar and easy to picture |
| A comet's long orbit | Ice, sublimation, returning | Time-scale calm |
| The Voyager probes | Distance, patience, the quiet | Careful: avoid an ending |
| Inside a nebula | Dust, slow collapse, colour | Needs care to stay non-dramatic |
| Europa's ocean | Ice shell, tides, dark water | Pairs with the deep ocean episode |

## Ideas — cozy-tales

| Topic | Angle | Notes |
|---|---|---|
| A bookbindery | Thread, glue, paper, press | Craft mechanics are excellent |
| The night train | Rocking motion, corridors, dark fields | Motion aids sleep |
| A lighthouse keeper's winter | Routine, weather, lamp | Watch for isolation reading as lonely |
| A pottery studio | Clay, wheel, kiln, glaze chemistry | Strong factual body |
| A wool mill | Fleece to yarn, machines, lanolin | Warm and tactile |

---

## Rejected, and why

Keeping these so they do not get re-proposed.

| Topic | Why not |
|---|---|
| Shipwrecks | Death emphasis, unavoidable |
| Volcanoes erupting | Drama and danger are the whole subject |
| Polar expeditions | Survival jeopardy |
| Predators of the deep | Hunting is the story |
| The space race | Competition, countdowns |

---

## Before writing any of these

1. Check the genre balance — prefer the thinnest.
2. Confirm no heavy overlap with a shipped episode.
3. Confirm the factual body can carry 30+ minutes without drama.
4. Scaffold: `lullable.py new "<Title>" --genre <genre> --pillar "<pillar>"`
