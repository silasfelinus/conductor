# Slime City CLASH: useful-but-fragile evolution contract

**Direction approved by Silas, 2026-11-09 PT.** This is the default interaction/card-design
contract for all **300 existing collectible IDs** in CLASH Solo (20-card decks) and Alliance
(30-card decks). The 2026-11-08 [evolution plan](CLASH-EVOLUTION-PLAN.md) supplies trajectories,
art requirements and crew ownership; [CARD-REDESIGN-300.md](CARD-REDESIGN-300.md) is the
card-by-card QA ledger. This document overrides any suggestion that a late bloomer may be
a *dead, blank, or deliberately unplayable* Level 1.

## The one-sentence promise

> **Useful but fragile at Level 1; stronger interactions at Level 2;
> a spectacular, earned expression of the same identity at Level 3.**

"Fragile" does **not** universally mean one hit point or bad base stats. A Tim-style 1/8
defender can have a sturdy body but be a *fragile plan*: little offensive pressure,
slow setup, vulnerable to displacement, silence, removal of its follow-on creation,
or an opponent simply racing past it. For a weak-body engine, fragility may literally
mean low life. **The opponent needs a credible answer, while the player needs a
reason to put the first version on the board.** A fragile card must not be worthless.

### Default interaction rhythm

| Stage | Obligation | Player feeling | Failure we reject |
| --- | --- | --- | --- |
| **L1: Do a job** | One legible, specific action with real immediate value **even if the card dies soon**: defend, make a token, heal a wound, put pressure in a lane, mark a foe, disrupt a strike, or set up an explicit follow-up. | "This helps me *now*; can I protect it or exploit the opening?" | An inert tax paid only to earn future levels; a card too poor to play against normal pressure. |
| **L2: Build the connection** | Preserve the recognizable job; widen or sharpen its interaction with at least one real card/archetype, positioning state, timing window or prior investment. | "That first play mattered; this works with the rest of my deck." | Only +X/+Y; three disconnected abilities; a setup whose payoffs need an impossible board. |
| **L3: Deliver the promise** | A distinctive named transformation, substantial compounding effect or **choose-one** evolution. Its visual and tactical arrival should be memorable, but it retains a readable answer. | "I built toward this, and now I can do the *thing*." | Bigger vanilla stats, a guaranteed unanswerable win, a payoff rarely reachable even in deliberately built decks. |

**Investment must feel continuous.** A playable Level 1 makes a sensible decision; Level 2
rewards repetition and creates an engine; Level 3 realizes it. Some cards are early
specialists, role shifters or sacrifice engines; those exceptions are **authored and
justified**, not a universal weaker-L1/stronger-L3 stat formula. A higher level may
trade attack for an aura; **higher usefulness and greater interactions** matter more
than monotonic numeric power.

## Seven enforceable design questions per card

1. **One core verb.** Name the card's principal job in **one sentence**: "protect,"
   "create," "drain," "redirect," "rescue," "mark," "delay," "explode," "equip," etc.
   A card can have modifiers and timing conditions, but no ability salad.
2. **Immediate, finite L1 value.** Specify the *state that changes this turn* or at
   the very next predictable trigger. Note its normal case, empty-board case, and
   whether the printed action has a legal target. If nothing happens in common
   situations, explain why the body or tempo is still a credible play.
3. **Honest fragility.** Name how the opponent can answer the L1 *plan* before it
   compounds, and what the player loses by investing. Being fragile is **not**
   synonymous with dying immediately. Do not require every card to be a glass cannon.
4. **At least one concrete combo.** Name a **real existing card ID** or precisely
   defined archetype, the actual board/trigger sequence, and what value emerges.
   At least one synergy should reinforce the crew's identity, and at least one
   defensive interaction/counter should be visible to a rival.
5. **Faction specificity.** Explain why this card would be *less natural* in each
   other crew without resorting to an "enemy faction" hate effect. The faction
   should own a distinctive decision, not just a differently colored icon.
6. **A complete three-beat arc.** In plain language: **seed -> compound -> payoff**.
   The payoff must be recognizably related to the opening. An L3 fork must offer
   genuinely different uses, not the same answer with different numbers.
7. **Player/CPU/replay truth.** The written rule, UI preview, battle effect and CPU
   valuation must agree. Stage 3 should be attainable with realistic draw/replay
   patterns; a stage that exists in data but never lands in CLASH has not passed.

### Crew-specific combo vocabulary

| Crew | Typical build-around payoff | Fragility/counterplay |
| --- | --- | --- |
| Gene Riot Catgirls | Ambush timing, endangered-unit rescue, escaped copies, survival tricks | Target the rescued body, lock the escape lane, force rescue too early |
| Punk Bloodfairies | SWARM density, LEECH chains, choirs, encores and casualties turned into advantage | Sweep small tokens, isolate the singer, deny a second strike |
| Ironjaw | Stacked protection, adjacency, construction, heavy breakthrough | Split their line, deny neighboring slots, bypass the one armored body |
| Riot Saints | Timed explosions, seeded risk, martyrdom, dangerous collateral | Spread out, induce premature detonation, punish self-harm |
| Undertow | Information, traps, delayed precision, denial chains | Scan/disarm the setup, overwhelm its time window, block the marked lane |
| Meat Exchange | Debt, collection, buyouts, recurring claims | Rush the collector, decline the bait, break the compounding contract |
| Mercenaries | One unusual, portable tactical trick | Always a tradeoff; never a generic superior copy of a crew signature |

## Existing real-card exemplars, not promises of new card IDs

**Glitter Riot Choir** (`s1-riot-choir`, Bloodfairies): its small initial
fighter participates in the board fight. L2's adjacent ally aura makes
positioning worthwhile. At L3, *Wall of Sound* gives up its own strike to
amplify other allies; *Backup Singers* fills nearby space with small bodies.
This is one recognizable idea, **the crowd makes the music**, with two
different crescendo outcomes. The opponent can clear the crowd or remove the
support. Test whether L1 is competitively worth deploying **without** the
L3 payoff, especially when other board slots are contested.

**Union Bridgebearer** (`s2-ironjaw-union-bridgebearer`, Ironjaw): useful as
an early line-holder; L2 makes adjacent fighters more effective; L3 becomes
a non-striking support bridge, providing protective value to neighbors.
The bridge's *body* need not be fragile: the plan is fragile because it relies
on positioning and the survival of the surrounding line. Test that protecting
the bridge isn't automatically the best choice against every enemy.

**Tim / Thundersaur inspiration** (SolForge, user's examples, **not copied
cards or verified numeric specifications**): a defender that helps create a
better version, and a threat whose later repetitions become increasingly
valuable. The generalizable delight is that **each play is both an action
and an investment**. Don't simply reproduce these named cards or their
proprietary rules; design original Slime City identities using the same
decision structure.

## Required card-design worksheet

For each of 300 cards, keep one short worksheet. Omitted cells are a **QA gap**,
not silent acceptance.

```yaml
card_id: existing-id             # Never invent a duplicate for an evolution.
crew: existing-faction-or-mercenary
signature_verb: protect
one_sentence_promise: "I hold the line now; later the whole crew can cross."
trajectory: useful-fragile-to-engine # Or a named exception + reason.
level_1:
  immediate_board_change: "..."
  normal_case: "..."
  empty_board_case: "..."
  fragility_or_opportunity_cost: "..."
level_2:
  same_identity_new_decision: "..."
  concrete_combo_id: existing-other-card-id
  combo_sequence: "first ... then ..."
level_3:
  named_payoff: "..."
  transformation_or_branch: "..."
  why_earlier_plays_mattered: "..."
  opposing_answer: "..."
faction_ownership: "..."
ui_preview_and_art: "what changes and how player recognizes it"
fixtures:
  - level_1_pays_before_removal
  - combo_resolves_with_real_target
  - level_3_payoff_and_counterplay
  - deterministic_replay
  - cpu_can_choose_card_in_relevant_state
  - both_20_card_solo_and_30_card_alliance_reachability
```

### Acceptance checks, not false automatic scores

**Mechanical fixtures (automatable):** All levels have legal effects;
L1 produces the declared value on a representative board; a normal opponent
answer prevents or reduces snowballing; the named combo and L3 transformation
actually resolve; both L3 forks work when offered; 20-card Solo and 30-card
Alliance decks remain valid; deterministic command replay reproduces the
result; the CPU can find the payoff instead of ignoring the card.

**Quantitative diagnostics (reported, not arbitrary hard win-rate gates):**
by card and by format, track offered-in-deck, first play, replay to L2,
play at L3, effect-trigger frequency, impact when triggered, dead-hand rate,
and how often the opponent successfully answers it. Stratify by curated
deck/archetype and both seats. Compare meaningful conditions; an L3 being
unseen in random mixed decks is an investigation prompt, not proof of failure.

**Human design acceptance (cannot be automated):** Two reviewers can state
the card's verb, immediately useful L1 play, L1 vulnerability, faction combo,
L3 dream, and how to stop it. If they need a paragraph to decode the card,
or if the first two plays feel like a tax, redesign it. Preserve art direction:
new, visually continuous L2/L3 paintings and clear on-card text.

### Review disposition

- **PASS:** useful but answerable L1, real synergistic L2, satisfying L3,
  reachable and counterable in Clash, original to crew.
- **NEEDS DESIGN:** empty early play, generic stat ramp, disconnected
  mechanics, duplicate journey, no real combo, no answer or unclear UI.
- **NEEDS GAMEPLAY/CPU:** mechanically sound on paper, but not chosen,
  inaccessible at L3, or AI misplays its combo.
- **NEEDS ART:** rules accepted, evolved images absent or unverified.
- **HUMAN FUN GATE:** mechanics/replay and art QA verified, player enjoyment
  not yet accepted.

**Scope boundaries:** This doc is a design contract and QA rubric, not a
claim that all 300 cards already satisfy it. It does not change existing IDs,
game rules, deployed art, card ownership, currency or public release.
