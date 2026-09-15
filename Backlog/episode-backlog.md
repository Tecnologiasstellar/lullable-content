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

## Ideas — YouTube-first, keyed to a search phrase

Seeded 2026-09-10 for the channel (D29). Same house voice, same 45–65 minute
band, same gates minus Supabase. Each row targets one phrase the niche research
(`lullable-marketing/PLAYBOOK.md` v2 §3–4) found is typed and thinly served:
`black screen sleep story`, `sleep story no ads`, `no music sleep story`,
`boring bedtime story`, `history for sleep`, `bedtime story for adults`, plus a
topic noun. Never an age label, never "no AI". Scaffold with
`--channels youtube` (or leave the default `app,youtube` if it belongs in the app too).

### 1. Cosmology for Sleep

| Topic | Search phrase | Angle | Notes |
|---|---|---|---|
| Dusk on Mars, from a rover's camera | space sleep story | Thin air, long shadows, a blue sunset | Rover as a patient observer, never "alone" |
| The light from Andromeda | black screen sleep story space | 2.5 million years old when it reaches you | Time-scale calm; the galaxy is the whole plot |
| A year on Neptune | boring bedtime story space | 165 Earth years, wind, a blue haze | Long numbers read slowly |
| Pluto and the far edge | sleep story no ads space | New Horizons' slow approach, a heart-shaped plain | Keep the flyby unhurried |
| Inside the Sun, slowly | space sleep story | A photon's 100,000-year walk to the surface | Heat without danger |
| The asteroid belt, mostly empty | boring bedtime story space | Hundreds of thousands of kilometres between rocks | The emptiness is the comfort |
| Listening with a radio telescope | no music sleep story | A dish tilting through the night, hydrogen's hum | No signal-from-aliens angle |
| Waiting at a Lagrange point | space sleep story | Webb telescope parked in balance, unfolding | Engineering as patience |
| Aurora seen from orbit | black screen sleep story | Charged wind, curtains of green, silence | Colour kept dim in the telling |
| Starlight older than the trees | bedtime story for adults space | Which stars you see, how old each light is | Ties to the night-sky episodes without repeating them |
| The dark between the stars | space sleep story | The interstellar medium, thin and cold and vast | Voyager already exists — stay in the medium, not the probe |
| How an eclipse comes around | boring bedtime story | The 18-year saros cycle, shadow crossing a map | Mechanism, no crowds |
| The Kuiper belt | sleep story no ads space | Ice worlds turning slowly past Neptune | Pluto row above overlaps — pick one first |

### 2. Ancient History & Gentle Lore

| Topic | Search phrase | Angle | Notes |
|---|---|---|---|
| An evening in a Bronze Age village | history for sleep | Roundhouse, hearth, bronze cooling in a mould | Zero conflict; domestic craft |
| The stargazers of Babylon | history for sleep | Clay tablets, eclipse records, a night watch | Pairs with the eclipse row in pillar 1 |
| A Tang-dynasty tea house | sleep story no ads history | Water, leaves, porcelain, evening trade | Sensory lane |
| A Viking longhouse in winter | history sleep story | Turf roof, long fire, wool, stories | Keep it the farmstead, not the longship |
| A medieval mill on a river | bedtime story for adults history | Wheel, millstones, flour dust, the miller's evening | Bakery already exists — stay at the mill |
| Hadrian's Wall by lamplight | boring bedtime story history | A quiet night on the milecastle, letters home | Vindolanda tablets are the factual spine |
| Laying a Roman mosaic | history sleep story | Tesserae, lime, a pattern growing across a floor | Craft mechanics |

### 3. Earth Science & Nature

| Topic | Search phrase | Angle | Notes |
|---|---|---|---|
| How a cave forms | nature sleep story | One drip, one grain of limestone, a hundred thousand years | Stalactites as clocks |
| The slow drift of continents | boring bedtime story | Fingernail speed, oceans opening | Erosion-calm plot |
| A peat bog remembering | no music sleep story nature | Layers, pollen, a landscape kept in order | Avoid the bog-body angle |
| The life of a river delta | nature sleep story | Sediment settling, channels wandering | Glacial river exists — start where it ends |
| How snow forms in a cloud | black screen sleep story | Supercooled droplets, six-fold growth, the fall | Physics read softly |
| The Atacama at night | sleep story no ads nature | Driest place, clearest sky, salt flats | Overlaps the observatory episodes — stay on the ground |
| Tide pools between tides | nature sleep story | Anemones, limpets, the sea drawing back and returning | Leave predation out |
| A mangrove forest at dusk | bedtime story for adults nature | Roots in salt water, mud, the tide coming in | Warm and enclosed |
| The bristlecone pines | boring bedtime story nature | Five thousand years on a dry ridge | Redwood exists — this is the opposite tree |
| How a pearl forms | nature sleep story | Nacre, layer by layer, years in the dark | Small-scale calm |
| A pond through four seasons | no music sleep story | Ice, thaw, dragonflies, leaf fall | Close-range, low-drama |
| The making of chalk cliffs | history for sleep nature | Plankton shells, a shallow sea, ninety million years | Deep time |
| A kelp forest swaying | ocean sleep story | Holdfasts, fronds, light through water | Deep trenches and glowing bay exist — this is the shallows |
| A raindrop through an aquifer | nature sleep story | Soil, gravel, decades underground, a spring | Water's slow route |

### 4. Immersive Journeys & Slow Fiction

| Topic | Search phrase | Angle | Notes |
|---|---|---|---|
| A night ferry across a northern sea | sleep story no ads journey | Engine hum, a cabin bunk, the swell | Keep the weather kind |
| A canal boat through the locks | boring bedtime story | Water rising a few feet at a time, towpath, evening | Slowness is the mechanism |
| A candle maker's workshop | cozy sleep story | Wax, wicks, dipping, the smell of the room | Craft with a factual body |
| The bookshop after closing | bedtime story for adults | Shelving, order, one lamp | Quiet fiction with real bookselling facts |
| A night at a mountain hut | black screen sleep story | Wood stove, bunks, wind outside, dawn plans | No storm, no rescue |
| The paper mill | no music sleep story | Rags to pulp to sheet, the drying loft | Pairs with bookbinding idea above |
| A cheesemaker's cave | cozy sleep story | Wheels turning on shelves, humidity, months | Warm and tactile |
| A violin maker's bench | boring bedtime story | Spruce, maple, varnish, the long wait for the wood | Craft mechanics are excellent |
| A slow tram across an old city at night | sleep story no ads | Stops, bells, lit windows, last passengers | The long-way-home exists — different vehicle, different city |
| A tea plantation at dawn | cozy sleep story | Mist, terraces, plucking, withering | Pairs with the Tang tea house |
| The weaver's loom | no music sleep story | Warp, weft, shuttle, a pattern emerging | Wool mill idea overlaps — hand loom, not machines |
| A boat builder's shed | bedtime story for adults | Steam-bent planks, copper rivets, tide tables | Slow craft |
| The night watchman's round | boring bedtime story | Lanterns, keys, an old town asleep | Keep it uneventful on purpose |
| The seed vault in the permafrost | black screen sleep story | Cold shelves, sealed boxes, patience as policy | Svalbard; no doomsday framing |
| A hand printing press | cozy sleep story | Type set backwards, ink, the pull of the lever | Craft with a factual spine |

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
