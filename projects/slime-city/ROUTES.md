# Slime City routes (finalized 2026-11-11 PT)

Silas, 2026-11-11 PT: *"Clear roadmaps and finalize multiplayer and single player routes. All art
can be generated at high priority."* This is the canonical route map. CONTROL.md carries the
directive; kind_robots is the source for behaviour.

## Single player: `/play/slime-city`

`pages/play/slime-city.vue` mounts `pages/admin/slime-city.vue` (one game, two URLs). Tabs:

| Tab | What it is | Deck | Rewards |
| --- | --- | --- | --- |
| HOME | Title splash (`slime-city-splash.vue`) | n/a | n/a |
| VS | Leftmost hub. **VS CPU**: quick CLASH against the CPU (the retired PRACTICE tab) | Solo or Alliance, player's choice | Server-verified Meat/XP (10 paid fights a day) |
| JOURNEY | Each crew's five-chapter SOLO story (`campaign`), plus the open seven-district city (`city`) with street encounters, rivals and contracts | SOLO story deck built from encountered cards; Alliance in the city | Story card rewards, Meat |
| TOWER | Alliance tower climb (`slime-city-tower.vue`) | Alliance | Meat/XP |
| COLLECTION | Alliance deck library (add, copy, delete, edit), packs, card inspector, bounties | Alliance default | Packs cost earned Meat; daily, weekly and evergreen bounties |

Legacy arena formats (BLACKOUT, BLOODRUSH, TURF, FIVE ALLEYS) stay behind the LEGACY selector and
get no further balancing.

## Multiplayer: VS PLAYERS + `/play/slime-city-pvp?duel=<id>`

- Entry: the VS PLAYERS card on the VS hub (friends list, username/email lookup, open challenge,
  private link, join by link). The header shortcut and turn badge show waiting turns.
- Duel page: `pages/play/slime-city-pvp.vue` -> `components/slime-city-pvp-game.vue`, store
  `stores/slimeCityPvp.ts`, rules `utils/slimeCity/pvp.ts`, API `server/api/slime-city/pvp/**`.
- Rules: CLASH with 20-card starter decks, server-owned transcript, hidden-hand redaction, seat
  authorization, atomic command serialization, reconnect by duel id, participant-only forfeit,
  7-day invite and 30-day inactivity expiry.
- Ending: finished-duel panel with REMATCH (new private challenge to the same rival) and BACK TO VS;
  the VS card shows a W-L-D record.
- No Meat, XP or card rewards for PvP. No public matchmaking beyond signed-in open challenges;
  external promotion is slime-city/t-015 (human gate).

Contract tests: `npm run test:slime-city-pvp`, `npm run test:slime-city-lab`.

## Art

Every Slime City art ledger queues at `priority: 1000`. Open rounds: lizard Ironjaw evolutions and
non-creature cards (t-044), Anarkiss cards and evolutions (t-052), occult Meat Exchange cards and
evolutions (t-053), curation redo rounds (t-017).

## What is left

- t-009, t-022: Silas's subjective playthrough/acceptance (agents finished the reversible work).
- t-012: full coverage and visual QA at 390/768/1440 once t-010 lands; needs a signed-in test user.
- t-014 / t-015: acceptance and public launch, both human gates.
- Card and balance polish: t-028 layout pass, t-041 evolution effects, t-051 fighters-first
  candidate list, t-058 Catgirls constructed lift.
