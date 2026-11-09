# Slime City: Story adventure and Alliance Tower

**Human direction:** Silas, 2026-11-08 PT. This supersedes treating Story as a roguelike or merely duplicating Arena modes. CLASH is the only modern battle ruleset; old formats are not a development target.

## Two distinct experiences under one Slime City console

### STORY = six individually authored SOLO CLASH adventures

- The player chooses **one** of six factions, never a randomly paired Alliance. One persistent narrative arc for that crew, with named characters, escalating stakes, cross-chapter memories, costly decisions and an ending earned by those choices. Not a run that resets after defeat.
- Retain existing `utils/slimeCity/campaign.ts`, its five major rival battles, six independent saved ledgers, dialogues, support echoes and ending branches. Do not replace that work with a generic procedurally generated campaign.
- The existing five fights are **chapter anchors, not a sufficient long-form story by themselves**. Expand each into roughly three authored beats (arrival/exploration, confrontation, aftermath) plus meaningful interludes and callbacks, targeting at least 15 distinct narrative scenes per crew before claiming a lengthy adventure. Present one clear card-based choice at a time over painted art, never a long web-form screen.
- Winning a major chapter requires the player to **choose one of two card rewards**, always exactly two distinct options; consider existing rarity classifications when constructing the pair. Prefer at least one faction-specific, underused card, and increase the odds/guarantee of rarer alternatives in later chapters. A choice is earned and permanent for **that Story save**. No deck-size inflation: Story battles use Solo Clash and trade a new card into the 20-card battle loadout.
- Loss retries the authored chapter with consequences, **not** a reset of the story campaign. Make outcomes reflect the user's chosen conviction/cunning route and previously unlocked cards.
- Current first slice in Kind Robots #4914 implements two-option story unlocks and story-only battle decks, not additional long-form writing. Continue authoring six full journeys independently.

Faction-specific dramatic throughlines:
1. **Gene Riot Catgirls / The Ninth Life Protocol:** personal identity and patent ownership, a stolen body mold, lab survivors, and the ethical cost of holding the research after liberation. Feature neglected rescue/gear cards as concrete plot objects.
2. **Punk Bloodfairies:** music, organizing, expendable crowds versus community care, and whether the uprising becomes a new hierarchy. Make sacrifice/encore evolutions emotional decisions.
3. **Ironjaw Ogres:** foundry safety and unions, stolen machine parts, solidarity versus boss privileges, and a future outside the assembly line. Gear should have a recognizable job in the narrative.
4. **Riot Saints:** disaster-comedy, spectacular sabotage, the people living downstream of every explosion, and earning responsibility without losing their reckless identity.
5. **Undertow Intelligence:** competing surveillance networks, truth traded for leverage, civilian exposure, and a decision about whether to dismantle the network. Debt/trap cards should open alternate approaches.
6. **Meat Exchange:** debt, bailouts, counterfeit food, exploitation and a credible route away from oligarchy. Consequences should follow individual contracts and debtors across chapters.

### ALLIANCE TOWER = 30-card two-faction roguelike

- Player chooses two different factions, one **general**, and builds 30 unique cards from either or the 60 mercenaries. Keep the unrestricted card-type composition explicitly requested by Silas; do not silently reinstate the rejected twelve-creature minimum.
- The general determines the one-time faction power. Choosing the other general from the same two factions must have a real tactical identity and must be tested with unchanged decks/seeds.
- Rise through **12 floors in three four-floor acts**: Undercity, Foundry and Spire. At each floor pick a fork between two meaningful arenas; traps, repairs, rivals, relics, odd allies, merchants, one-time bargains and bosses change the current run. An attractive option must sometimes be dangerous.
- Boss health and pressure rise predictably; a floor defeat ends the run. Offer eventual secure suspend-and-resume instead of retriable free refreshes. Never give a zero-victory run a collectible reward.
- Mid-run relics/gear are temporary, but finishing a run can provide **two distinct card spoils, choose one**, and bounded persistent variables. Start with separate Tower-only Cinders and card unlocks; add thematic relic pools and class-adjacent synergy later. These are not server pack cards, account XP, or Meat.
- The current Kind Robots #4914 vertical slice implements a seeded two-fork, twelve-floor battle path, varied boss life, Wards/Scars/Guard, cinder-based next-run protection, and a Tower card joining later 30-card run decks. Do not mistake this for a full encounter/relic economy.
- Next upgrade: multiple event types *without* mandatory fights, at least 6 meaningful run-changing relics with tradeoffs, upgrade/repair events, boss-specific gimmicks, alternate encounter text/art per general+ally relationship, an authored Tower guide and controlled deck-selection of earned Tower cards.
- Tower's persistent effects must remain bounded. Avoid a pay-to-win or grinding-only best strategy.

## Card-quality acceptance work

Prior full-catalog Alliance test: Kind Robots #4913 ran 1,140 seeded games; 285/300 catalog cards were selected, only 104 reached L3; specials-only decks drew 59.2% and all 120 reached the 24-round cap. The fifteen unplayed cards included Backwater IOU, Stolen Bone Saw, Spare Nine Lives, Second Pounce Rig, Encore or Die, Union Reallocation, Furnace Overdrive, Posthumous Saint Medal, Tunnel Harpoon, Acquisition Clause, Secondhand Halo, Emergency Wings, Theftproof Toolkit, Broken Halo, and Union Suit.

Do not "fix" these with unthematic raw stats. Separate:
- **CPU never chooses** useful cards because it undervalues existing fighter protection, expensive gear or situational evolution payoffs: fix valuations, assert an actual action and replay.
- **Card is playable but underpowered:** give its authored L2/L3 ability a distinctive decision/payoff with response window and counterplay.
- **Card needs a deck archetype:** use Story card offers and Tower events to teach or reward the synergy, then benchmark appropriate constructed decks.
- **No-creature all-special stalls:** test strategic counterplay and alternate win pressure, preserve intentionally legal weird decks; avoid simply imposing a new deck restriction.

Required tests: full 300-card registration; constructed two-seat Solo/Alliance matrices; general swap controls; evolution L3 reach; deterministic same-seed replays; exploit tests for repeat rewards, rerolled battles, forged collection credit and cross-account contamination; six story playthroughs and multiple full Tower runs. Source tests are **not** subjective fun acceptance, phone/desktop art checks or verified deployment.

## Scope and release gates

The code lives in the existing Slime City Play/Collection/Story/Clash surfaces. Do not fork another independent game unless an identified incompatibility forces it. No migrations or account progression writes without explicit scoped review. A GitHub source merge does not prove deployment on self-hosted Unraid. Human acceptance is needed for overall fun, visual quality and public launch/marketing. Art queue status remains separate from complete writing, rules and playtest work.
