# Slime City CLASH: constructed checkpoint, 2026-11-16 PT

**Task:** slime-city/t-041 (CLASH 300 evolutions). **Scope:** a read-only audit. No card, rule or CPU
code changed.

## Why this checkpoint

By 2026-11-16 PT every crew (Catgirls, Blood Fairies, Ironjaw, ANARKISS/Riot, Undertow, Exchange)
and both Mercenary halves had an editorial pass (kind_robots #5204, #5259, #5260, #5261), plus the
L2-to-L3 continuity fixes (#5221, #5226, #5255, #5262). The only t-041 item left that agents own is
constructed balance. This checkpoint re-runs the constructed suite on kind_robots `main` (c843ad9)
to see what is still open.

## Constructed suite (`npm run test:slime-city-clash-constructed`, main c843ad9): PASS

- 3,120 bouts across 30 legal 20-card decks (5 archetypes × 6 crews), 30 exact archetype replays.
- First seat 51.0%, 0 draws, 2 round-limit games, 8.87 rounds on average.
- Crew field: Catgirls 50.7, Blood Fairies 50.5, Ironjaw 50.0, Riot 44.3, Undertow 48.8,
  Exchange 55.7. All are inside the 42–58% guard, with a 13.4-point spread (guard: 15).
- Archetypes: starter 59.0, fighters 65.6, mercs 55.3, heavy 44.1, specials 26.0.
- Evolution reach: 179 cards reached L2 and 168 reached L3 in play. Crew cards covered: 184/240.

## Findings

1. **Every card that is never or almost never played costs two slots.** The suite counts 14 cards
   that were never played: Glitterglass Flood, Grease Oracle, Cathedral Noise, Union Reallocation,
   Furnace Overdrive, Foreman Crowbar, Wrong Side of the Blast, Backwater IOU, Long Drain Sting,
   Citywide Blackmail, Compound Interest Notice, Acquisition Clause, Stolen Bone Saw and Spare Nine
   Lives. I checked the low-selection list (≤5%) card by card: Friendly-Fire Rehearsal, Pounce Rig,
   Collection Badge, Compound Notice, Posthumous Saint Medal, Juggernaut, Chimera, Final
   Benediction, Union Owl and Tunnel Harpoon are all two-slot cards too. The one exception is
   Floodlight Leak, a one-slot scan spell that only pays off when the foe has traps down, which is
   working as designed. The 2026-11-11 A/B (in the suite's header comment) showed this is card
   weakness, not a CPU blind spot. That redesign is **slime-city/t-051** (fighters-first: fold the
   best gear and tech into fighters, with a candidate list for Silas before changing cards).
2. **The specials and heavy archetypes are weak because of the same two-slot set.** Riot/specials
   reads 17.3% and Riot/heavy 28.8%, and these two decks pull Riot's crew score down to 44.3%.
   Riot/fighters (64.9%) and Riot/starter (57.7%) are healthy. A per-card diagnostic on Riot's
   starter (400 bouts, 8 seeds × both seats against the field) showed no card whose win rate when
   played sits far below the deck's 60.5%. Low-Budget Grenade was lowest at 54%, from 127 plays.
3. **Ironjaw/fighters is the top deck at 82.7%, just under the 85% runaway guard.** A one-card swap
   diagnostic (400 bouts per variant) puts the edge in extra cheap one-slot fighters, not in one
   overtuned card. Swapping Union Bridgebearer out drops the deck to 72.8% and Union Millwright to
   76.0%. Every other swap stays between 79% and 84%. This matches Silas's fighters-first
   direction, so I am not proposing a nerf. If the guard ever trips, start with Bridgebearer's 1/6
   one-slot body.

## State decision

t-041 now also depends on t-051, and its status is `waiting`. What remains of t-041:

- constructed balance, which is blocked on t-051's two-slot redesign;
- per-level art, owned by t-044, t-052, t-053 and t-054;
- Silas's hands-on fun verdict. That verdict sits outside the finite roadmap, per AGENTS.md.

Rerunning t-041 every hour would just repeat this audit. When t-051 merges its two-slot redesign,
rerun the suite and look again at `deadTwoSlotCards`, the specials/heavy archetypes and Riot's
crew score.
