# Slime City t-051: fighter-first ability conversion shortlist (2026-11-12 PT)

## Verified baseline

- Source: `kind_robots/utils/slimeCity/prototypes.ts`, the canonical `CARDS` roster; `utils/slimeCity/clash.ts` defines the five-lane, two-play CLASH rules.
- The already-merged `kind_robots#4965` increased each starter to **13 fighters in 20** and removed random-target selection and most coin flips. Do not repeat that work.
- The remaining request is not simply to delete gear: the player wants **fighters that do cool things**, with fewer detached effects and less rules vocabulary. Retain all card IDs and 300-card collection coverage until migration/replay consequences have been tested.

## First four conversions to prototype, NOT approved card rewrites

| Existing card | Verified present effect | Proposed fighter-first expression | Risk and acceptance experiment |
| --- | --- | --- | --- |
| Catgirls `ninthlife`, **Ninth Life Collar** | 2-cost equipment grants REGEN to another fighter | Make a new distinct regenerative fighter with a one-time ally repair/REGEN choice on entry, while retaining the original ID and its collection/evolution identity | Must not become a strictly better `calico`; compare Catgirls constructed fighters and specials against held-out crews |
| Catgirls `shredders`, **Patent Shredders** | 2-cost equipment permanently adds +1 attack | Turn the stolen-claw fantasy into a fragile fighter that sharpens an adjacent ally on entry, rather than a free permanent buff stapled onto a strong body | Test an empty board (no valid ally), a full board, and whether buff loops dominate tier III |
| Bloodfairies `spurs`, **Razor Spurs** | 2-cost equipment grants permanent +1 AP | Make a low-HP stage-diver that grants a one-turn lane tempo boost to an ally on entry | Avoid stacking permanent speed and runaway initiative; compare both seats in the starter sweep |
| Bloodfairies `choker`, **Spiked Choker** | 1-cost equipment grants SWARM | Make a vulnerable hype-singer that rewards having another Bloodfairy fighter, rather than an unconditional keyword dispenser | Do not double-count SWARM or make the existing `sprite`/ `pogo` redundant |

## Proposed experiment

1. Start with **one Catgirls conversion** (`shredders`) and **one Bloodfairies conversion** (`choker`), not all four simultaneously. Preserve IDs, costs where feasible, evolution stage availability, collection unlocks, and replay serialization.
2. Implement their abilities as explicit deterministic triggers using the existing CLASH evolution/effect machinery, not new chance rolls. An empty allied board must have a documented legal outcome; no invisible fizzles.
3. Keep each crew's 20-card starter at 13–15 fighters, ensure the six-crew 300-card invariant and three-stage COG coverage remain valid, and compare deck-builder selection rates rather than merely average win rates.
4. Run the existing CLASH starter guard (42–58% per crew) and constructed guard, plus held-out seeds and adversarial edge fixtures (full lanes, no target, duplicate copies, tier III, replay). Reject a conversion that makes early turns automatic or creates a dominant must-pick.
5. Compare the pre/post card selection rate, not just aggregate power. The success condition is that playing the card puts a memorable **fighter on the board** while preserving a tactical choice.

## Decision requested before wholesale conversion

Recommend a **two-card reversible experiment** before changing the remaining non-fighter roster. If the two conversions improve fighter play and preserve balance, continue in small crew-paired batches. Do not delete the original IDs, change all 300 cards, or claim the full t-051 roadmap complete on the strength of this proposal.

This is a design handoff only: no card stats, rules, or art were changed by this document.
