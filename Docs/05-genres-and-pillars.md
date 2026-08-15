# Genres, pillars and palettes

## The four genres

These are fixed. Adding a fifth is a product decision — it touches the app's
browse UI and the catalog schema — so it is not something to do while writing an
episode. G03 rejects anything else.

| genreID | What belongs in it | Feels like |
|---|---|---|
| `gentle-nature` | Oceans, forests, weather, animals, geology, deep time on Earth | Cool, spacious, alive |
| `ancient-worlds` | Cities, libraries, trade, building, daily life in the distant past | Warm, dusty, lamplit |
| `cosmic-journeys` | Planets, moons, ice, orbits, distance, silence | Cold, vast, weightless |
| `cozy-tales` | Craft, quiet human work, small warm interiors, making things | Warm, close, hushed |

A story may carry **one or two** genre IDs. Two is for genuine overlap, not
hedging.

### Display names on the website

These four are canonical across both surfaces (D19). The website previously used
a separate, non-overlapping vocabulary — `Folklore`, `Nature & Weather`,
`Slow Fiction`, `Wandering` — which has been retired in favour of these.

| genreID | Website display |
|---|---|
| `gentle-nature` | Gentle Nature |
| `ancient-worlds` | Ancient Worlds |
| `cosmic-journeys` | Cosmic Journeys |
| `cozy-tales` | Cozy Tales |

`lullable.py website-export` applies the mapping automatically.

---

## Content pillars

Looser than genres — an editorial grouping for the pipeline sheet, not something
the app enforces.

| Pillar | Example episode |
|---|---|
| 3. Earth Science & Nature | The Deep Ocean Trenches |
| 4. Space & Cosmic Journeys | The Rings of Saturn |
| 5. History & Human Ingenuity | The Great Library of Alexandria |
| 6. Craft & Quiet Work | The Bakery Before Dawn |

---

## Palettes in use

Two six-character uppercase hex values per story: `colorHex` (the dark base) and
`accentHex` (the light note). They generate the gradient card artwork.

| Story | colorHex | accentHex | Drawn from |
|---|---|---|---|
| the-deep-ocean-trenches | `0B1F33` | `5FA8C4` | deep water / bioluminescence |
| the-great-library-of-alexandria | `3A2A18` | `D9A55C` | dark ink / lamplight |
| the-rings-of-saturn | `1B2436` | `E8C89A` | night sky / butterscotch |
| the-bakery-before-dawn | `2E1F14` | `E3B778` | oven wood / crust gold |

**How to pick.** Take the two colours the story actually describes — the base is
the dark the listener is sitting in, the accent is the one light source. Do not
pick a colour the narration never mentions.

Keep the base dark enough that white text sits on it comfortably, and the accent
light enough to read as a highlight rather than a second background.

---

## Catalogue coverage

Ask Claude to run `lullable.py status` for the live picture. As of the last
review: four episodes, one per genre, all four genres covered.

**Choosing the next topic.** Prefer whichever genre is thinnest. Depth in one
pillar is more valuable than one of everything once each genre has an episode —
a listener who liked the ocean wants another ocean, not a bakery.

---

## Runtime consistency

An open question, deliberately recorded rather than settled:

| Episode | Runtime |
|---|---|
| The Bakery Before Dawn | ~48 min |
| The Rings of Saturn | ~47 min |
| The Deep Ocean Trenches | ~43 min |
| The Great Library of Alexandria | ~23 min |

Three cluster near 45 minutes; Alexandria is half that. Either it is a format
inconsistency to fix before launch, or a short episode is genuinely useful for
people who fall asleep quickly. Worth deciding before the catalogue grows, since
it sets the word target for every future brief.
