# Zuzu: Shifting Lands — design integration self-review (t-002), 2026-11-13 PT

Silas removed the early creative-review checkpoint on 2026-10-24: t-002 is an agent self-review of scope, cast and
quest taxonomy, design cohesion, follower paths, game feel and source-of-truth drift, with findings turned into
tasks. Only t-018 is creative approval. This review was written while preparing the playtest handoff
(Silas, 2026-11-13 PT: "help wrap up Shifting Lands ... Last step is to flip the project to playtest").

## Scope and cohesion

- **Shape.** Five lands, three locations each, 120 painted V6 encounter cards (8-card pools), five major trials with
  eight routes each, a moral ledger, cross-land echoes, spent deeds, a kitchen-sister follower arc, and V10
  character-aware journeys. Saves replay from seed and actions (V3 to V10 migrations).
- **Travelers.** There are 13 premades (Silas, 2026-11-13 PT: "Expand to 13 premades") plus custom travelers in 13
  species. Each premade has an identity deed, four own cards, three own choices on shared cards and three endings
  (hopeful / bittersweet / dark): 52 cards, 39 choices and 39 endings in all. Cameo and self-variant rules mean
  nobody meets themselves. kind_robots #5125.
- **Voice.** Player-facing text is second person. The 2026-11-13 audit found no text naming Zuzu as the player in
  the V6–V10 game. The legacy Homestead workshop text and the channel copy were rewritten (kind_robots #5125).
- **Images.** No plate defaults to Zuzu. Gamebook scenes that show Zuzu are filtered out of place and stranger art.
  The 19 shared ending plates and the 13 portraits ship, as do 530 outcome plates (kind_robots #5126). Card faces
  for 19 more V6 cards and every new traveler's portrait, own cards and endings are queued (ROUND-9 to ROUND-12).

## Findings and what became of them

| Finding | Outcome |
|---|---|
| Four moral-constellation endings (Lantern Commons, Book Nobody Owns, Ford With No Toll, Bridge Without Forgiveness) were unreachable from V8 on: the verifier checked the V7 trial targets that V8 had lowered. | Fixed in kind_robots #5125, with the endings-graph witness test (`verifyShiftingEndingsGraph`). All 19 shared and 39 own endings are witnessed and replay exactly; see `ENDINGS-GRAPH-2026-11-13.json`. |
| The personal-road art ledger named in #5069 never landed, so none of it was queued. | ROUND-9-PERSONAL queued at priority 1000 (conductor #7345). |
| 373 ROUND-7 outcome renders and 69 ROUND-3 img2img renders had sat DONE and uncurated. | Curated: 311 and 19 keepers shipped in #5126. The 65 rejected or missing outcomes are re-queued in ROUND-12 (#7347). |
| No title screen and no persistent scrapbook (main-game standard). | Title console and scrapbook added (traveler pages plus 19 shared plates, X of N). |
| Live-database world-membership tooling (t-004, t-012) and optional AI prose (t-014) are not used by the game, which plays from a committed world snapshot. | Cancelled by Silas, 2026-11-13 PT. |
| Recruitable followers beyond the kitchen sister (t-043). | Silas, 2026-11-13 PT: the kitchen-sister arc and the 13 personal roads are enough; t-043 closes. |

## Known limits for the playtest

- Rendering is asynchronous. Until the remaining ROUND-9 to ROUND-12 plates are curated and shipped, a new
  traveler's own cards show a non-Zuzu gamebook scene, and an outcome without a plate shows its card art.
- Hester Kell and Augustin are provisional names. Tamsin's family names (Corran, Wenna, Pip) and Augustin's ring
  history (Madam Ferrule, Nell) were invented for their roads.
- Dark endings for some travelers involve betraying children (Hester's writ, Wren's kit, the Coyote's runaways,
  Gideon's names). Harm stays off-screen per the world guardrails. This is a tone call for Silas at t-018.
