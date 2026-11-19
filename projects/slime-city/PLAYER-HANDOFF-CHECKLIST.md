# Slime City: player handoff checklist (t-012)

Started 2026-11-19 PT. This is an agent-owned QA ledger. It is **not** a playtest verdict
(t-009, t-014) or publish authorization (t-015). Mark a row done only when its evidence is
merged on `kind_robots` main and you have rechecked it. A queued prompt or green CI on an
unmerged branch does not count.

Legend: ✅ automated evidence on main · 🟡 partial · ⬜ open

## Story and campaign routes

| Check | State | Evidence / next step |
| --- | --- | --- |
| Every crew × every one of the 32 choice paths finishes through the real Blackout engine, with multiple seeds and retry after loss | ✅ | `utils/scripts/verifySlimeCityFullRoutes.test.ts` (kind_robots#5323, merged af20fd5): 576 routes, ~4.1k engine fights |
| Defeats and draws never advance the story or record decisions; stale, wrong-rival and post-finale results are ignored | ✅ | Same test |
| Both endings (triumph or compromise) are reachable for every crew | ✅ | Same test |
| Earned favour → story echo → crew legacy transitions | ✅ | Same test, plus `verifySlimeCityCampaignPlaytest.test.ts` |
| Per-crew journey scene branches (left/right) | ✅ | `verifySlimeCity*Journey.test.ts` (six crews and alliance) |
| Story save and restore, guest and account | ✅ | `verifySlimeCityStorySave.test.ts`, `verifySlimeCityGuestStory.test.ts` |

## Cards and balance

| Check | State | Evidence / next step |
| --- | --- | --- |
| CLASH 300 L1/L2/L3 evolution coverage | 🟡 | t-041 is still `ready`. `verifySlimeCityEvolutions.test.ts` covers the crafted sets. Close it out when t-041 lands |
| Constructed-deck balance across crews | 🟡 | Re-run 2026-11-18 PT on kind_robots main `be2745d`. `balance:slime-city-clash` (150 seeds × 9000 offset, 4,500 CPU games, both seats): first seat 51.2%, draws 0.0%, round-limit 0.1%, avg 9.3 rounds; crews catgirls 41.7 · bloodfairies 51.6 · ironjaw 50.7 · riot 50.5 · undertow 51.9 · exchange 53.6 (11.9-pt spread, all inside the 40–60% target, catgirls at the low edge). `verifySlimeCityClashConstructed.test.ts` PASS: 3,120 bouts over 30 legal 20-card decks, first seat 52.4%, crews 43.6–54.4%; 0 dead and 18 near-dead two-slot cards, held-out +5000 has 2 dead (`s2-bloodfairies-glitterglass-flood`, `s3-exchange-compound-notice`). Open: the `specials` archetype wins 26% overall (riot/specials 17.3%, ironjaw/specials 20.7%, under the 30% worst-case floor in PROGRESSION-AND-SETS.md) while `fighters` wins 69%. Re-run after t-041 lands before calling this ✅ |
| Resource exploits (double claims, pack duplication, wallet races) | ✅ | `verifySlimeCityStore.test.ts`, `verifySlimeCityAccountBoundary.test.ts`, `verifySlimeCityProgression.test.ts` |

## Multiplayer and accounts

| Check | State | Evidence / next step |
| --- | --- | --- |
| CPU and PvP reconnect, forfeit and expiry | 🟡 | `verifySlimeCityPvp.test.ts`, `verifySlimeCityVsResume.test.ts`; still needs a two-browser reconnect check |
| Account security and hidden-information redaction | ✅ | t-011 done; `verifySlimeCityPvp.test.ts` |

## Experience, art and layout

| Check | State | Evidence / next step |
| --- | --- | --- |
| Gamepad, keyboard and touch play a full match | ⬜ | Needs a browser-driven pass |
| Rendered 390 / 768 / 1440 / XL layouts | 🟡 | `audit:slime-city-clash-layout`; earlier captures are in `playtest/`. Re-capture on current main |
| Real delivered ArtImages in every required slot (fallbacks otherwise) | 🟡 | Manifest reconciled 2026-11-19 PT in `verifySlimeCityArtCoverage.test.ts` (kind_robots#5327, in `test:slime-city-lab`): 300/300 cards have base art; all 1,353 ArtImage ids are unique (none borrowed); every evolution key names a real card stage; every card at L1–L3 and on both branches resolves to its own painting. 66 cards still have no L2/L3 painting and show an earlier stage (bloodfairies 14, undertow 12, ironjaw/riot/exchange/mercenary 10 each, catgirls 0). A per-crew ratchet holds that count, so lower the baselines as renders land. Still open: an authenticated byte-delivery spot check, and the 66 pending evolution renders |

## Human-owned, outside this checklist

- t-009 / t-014: subjective fun verdict and acceptance (Silas).
- t-015: public Play launch authorization (Silas).
