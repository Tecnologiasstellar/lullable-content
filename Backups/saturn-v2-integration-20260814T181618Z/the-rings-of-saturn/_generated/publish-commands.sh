#!/usr/bin/env bash
# GENERATED FROM story.yaml — do not edit.
set -euo pipefail

# BLOCKED — 8 gate(s) failing for staging:
#   G02 story identity — story identity unresolved — UNRESOLVED: the app already carries a card with storyID 'edge-of-saturn'. If this narration REPLACES that card, set storyID to 'edge-of-saturn' and supersedes to null, so existing favorites and progress survive. If this is an ADDITIONAL story, keep 'the-rings-of-saturn' and set supersedes to null. Then set identityResolved: true. Publication is blocked until then.
#   G08 audio + rights files — master filename unset; delivery filename unset
#   G09 audio checksums — master not on disk; delivery not on disk
#   G10 delivery encoding — delivery file not available to probe
#   G11 duration matches audio — card.durationSeconds is not a number
#   G12 render manifest — render.voiceId unset; render.voiceName unset; render.model unset; render.historyItemId unset; render.renderedAt unset; render.settings stability/similarityBoost not recorded
#   G13 QA + device sign-off — audio QA not approved; not accepted on a physical device
#   G16 access decision final — accessDecision still PENDING — free vs premium must be settled before staging
