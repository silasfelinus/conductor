# Slime City CLASH: 300-card evolution quality and matchup audit

**Checkpoint:** 2026-11-08 PT  
**Scope:** Gameplay-only, full 300-card catalog; no changes to the live economy, database, or published art.

## Verified implementation

Kind Robots [#4907](https://github.com/silasfelinus/kind_robots/pull/4907) merged 230 individually specified evolution arcs alongside the original 70 hand-built twists ([#4895](https://github.com/silasfelinus/kind_robots/pull/4895), [#4901](https://github.com/silasfelinus/kind_robots/pull/4901), [#4904](https://github.com/silasfelinus/kind_robots/pull/4904), [#4905](https://github.com/silasfelinus/kind_robots/pull/4905)). Six factions have 40 cards apiece and mercenaries contribute 60, for exactly 300 unique collectible IDs. The eight authored evolution files contain 30 distinct arcs per crew and 25 in each half of the mercenary roster, totaling 230. Each new arc has named second- and third-level mechanics, with 22 level-three choose-one designs across the authored roster.

The prior versioned-card test checks catalog registration, rules text length, two stage definitions, scripted Catgirls scenarios, deterministic choices, and engine smoke runs on empty and crowded boards for every crafted card. This is strong implementation coverage, not proof that all 300 are equally strategic, balanced, or narratively memorable.

## Qualitative design assessment

- **Catgirls:** their street-medicine/rescue language has a legible identity; Splice Runner's non-attacking Midnight Ambulance versus draw-focused Black Market Run is an actual role decision. Some rescue cards require an existing casualty, so playing them too early should be a meaningful misplay.
- **Blood Fairies:** stage-driven encore, echo and death tactics create opportunities for deliberate sacrifice rather than generic big bodies.
- **Ironjaw:** armor and adjacent union-line tactics reward formation and counterplay against heavy units.
- **Riot:** unpredictable blast outcomes and friendly fire support risky choices, but the CPU must learn when friendly casualties are acceptable.
- **Undertow:** roots, traps and interference have a consistent denial identity, requiring tests against both wide and slow decks.
- **Exchange:** debt and collection effects provide a different resource-erosion win route; attention is needed to boss-damage races.
- **Mercenaries:** broad generic utility is useful for deck building, but must be evaluated for identity-dilution and excessively universal staples.

The new data stages have flavorful names and custom triggers, but stylistic uniqueness does not guarantee distinct **mechanical** journeys. Compare identical action signatures, payoff reachability and whether the CPU actually chooses each card.

## Gaps found in existing tests

1. Existing six-crew balance checks use the curated 20-card `clashDeck(team)` decks. They miss many constructed and mercenary-heavy strategies, even though all 300 cards are registered.
2. The CPU's `chooseClashCpu` adds a generic +1.2/+2.5 score for a stage with an arrival trigger (L2/L3), not a board-specific expected-value estimate of healing, sacrifice, stun chains, or traps. A near-50% default-deck rate can therefore coexist with poor decisions and noncompetitive cards.
3. Earlier tests use finite-state smoke checks for most of the 230 new stages. Only the Catgirls pilot and the original 70 have deeper named payoff fixtures. Specific triggers and conditions may rarely fire in real matches.
4. Track the fraction of cards **offered in decks**, **actually played**, and **played at L3** separately. None alone proves the others.
5. Win rates alone do not test memorable moments: scripted examples should demonstrate each card's effect, strategic cost, response window, and counterplay.

## Expanded matchup QA

Kind Robots [#4908](https://github.com/silasfelinus/kind_robots/pull/4908) introduces a regression suite against the *real* CLASH rules engine:

- **1,080 Solo CPU matches:** nine deck plans (starter; two complementary faction halves; six 10-faction/10-mercenary mixes), each unordered faction pair from both seats on four matched seeds.
- **150 Alliance CPU matches:** seeded paired-general simulations with reporting of one-time faction-power use.
- **Full catalog offering:** all 300 collectible IDs must appear in at least one legal 20-card Solo deck. Count actual plays and L3 plays so a never-selected card cannot be confused with a tested payoff.
- **Deterministic replay:** the first paired seed of every Solo deck-plan/faction combination is replayed and checked against boss totals, units, levels and winner.
- **Mechanical-fingerprint diagnostics:** report completely duplicated second/third-level action+static profiles (a smell, not an automatic flaw) and cards whose second and third levels have exactly the same action/static signature.
- **Balance diagnostics:** deck-plan-specific faction win rates, first-seat skew, match length and draws. No arbitrary hard win-rate threshold is asserted.

**CI status at report authoring:** the new suite was submitted to GitHub Actions and had not yet produced an independently verified complete-match report. Keep this distinct from the earlier #4907 author's default-deck sweeps. Update this report with the final #4908 result after GitHub checks finish.

## Artwork and acceptance

Conductor [#7171](https://github.com/silasfelinus/conductor/pull/7171), [#7172](https://github.com/silasfelinus/conductor/pull/7172) and [#7174](https://github.com/silasfelinus/conductor/pull/7174) merged new L2/L3 art prompt ledgers using Flux Kontext and two candidate seeds. They are requests, **not verified rendered or attached images**. Ten cards explicitly awaited their level-one paintings in #7172. The `CARD-REDESIGN-300.md` roster marks the 70 original well-fixtured arcs `MERGED` and the other 230 `LIVE_QA` so it does not confuse implemented code with comprehensive strategic acceptance.

**Next focused work:** inspect weakest constructed-card matchups and never-played cards; improve the CPU's tactical evaluation of stage conditions; add bespoke payoff/counterplay fixtures where a card's later stages are too rarely seen or mechanically duplicate a simpler card. Only then request Silas's hands-on fun judgment. No public deployment or creative acceptance is implied by any passing test.
