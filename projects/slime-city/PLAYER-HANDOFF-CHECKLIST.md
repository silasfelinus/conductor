# Slime City: player handoff checklist (t-012)

Started 2026-11-19 PT. This is an agent-owned QA ledger. It is **not** a playtest verdict
(t-009, t-014) or publish authorization (t-015). Mark a row done only when its evidence is
merged on `kind_robots` main and you have rechecked it. A queued prompt or green CI on an
unmerged branch does not count.

Legend: ✅ automated evidence on main · 🟡 partial · ⬜ open

## Story and campaign routes

| Check | State | Evidence / next step |
| --- | --- | --- |
| Every crew × every one of the 32 choice paths finishes through the real Blackout engine, with multiple seeds and retry after loss | 🟡 | `utils/scripts/verifySlimeCityFullRoutes.test.ts` (kind_robots#5323): 576 routes, ~4.1k engine fights. Mark ✅ once it merges |
| Defeats and draws never advance the story or record decisions; stale, wrong-rival and post-finale results are ignored | 🟡 | Same test |
| Both endings (triumph or compromise) are reachable for every crew | 🟡 | Same test |
| Earned favour → story echo → crew legacy transitions | 🟡 | Same test, plus `verifySlimeCityCampaignPlaytest.test.ts` |
| Per-crew journey scene branches (left/right) | ✅ | `verifySlimeCity*Journey.test.ts` (six crews and alliance) |
| Story save and restore, guest and account | ✅ | `verifySlimeCityStorySave.test.ts`, `verifySlimeCityGuestStory.test.ts` |

## Cards and balance

| Check | State | Evidence / next step |
| --- | --- | --- |
| CLASH 300 L1/L2/L3 evolution coverage | 🟡 | t-041 is still `ready`. `verifySlimeCityEvolutions.test.ts` covers the crafted sets. Close it out when t-041 lands |
| Constructed-deck balance across crews | 🟡 | `verifySlimeCityClashConstructed.test.ts`, `verifySlimeCityFactionBalance.test.ts`; re-run `balance:slime-city-clash` and record win spreads |
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
| Real delivered ArtImages in every required slot (fallbacks otherwise) | ⬜ | Reconcile the art manifest against delivered ArtImage IDs |

## Human-owned, outside this checklist

- t-009 / t-014: subjective fun verdict and acceptance (Silas).
- t-015: public Play launch authorization (Silas).
