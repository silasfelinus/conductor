# Emperor of Dust — Systems Design v0.3: the Fortress
*Silas's direction, 2026-10-18 PT. **This document supersedes SYSTEMS-V02.md and every conflicting
rule in GAME-BIBLE.md and DAY-PLAN.md.** Where v0.2 and v0.3 disagree, v0.3 wins. Numbers are
starting values for simulation and playtest, not locked balance.*

Reference for flow (not style): *Sovereign Tower*. Silas's screenshots show the loop he wants: a
cycle counter, a small strip of faction meters plus one coin total, a quest scroll with a stat
requirement wheel, damage risk, promised rewards and assignment slots, a follower card with a stat
wheel and equipment, a world map with crested faction banners and fog over unexplored land, and
art-led dialogue scenes with two illustrated speakers, a nameplate, a short choice list and a log
button. **Do not copy their art, layout or text.** Emperor of Dust keeps its own Zuzu-world look
(DAILY-DREAM-VIBE.md: ash, brass, kiln ochre, salvage).

## What changed from v0.2

| v0.2 | v0.3 |
|---|---|
| Numerical **Horde** headcount, troop contingents per mission | **Removed entirely.** No troops, no headcount. The garrison is a local faction (the Gate Watch) with a support meter, nothing more. |
| In-world hour clock, 1–5 h outward travel, return ETAs, pausable timeline | **Game days only.** A quest takes 1–3 days. No hours, no travel math, no pause clock. |
| 100 days, ten acts | **50 days, five acts of 10 days.** |
| 100-follower pool, 5 starters | **20 followers**, 4 at the start. |
| Might / Diplomacy / Ingenuity, 0–5 | **Five stats, 0–10** (below), plus secret skills, secret weaknesses and one unique ability. |
| 0–3 leaders per incident | **1–4 followers per quest.** |
| Prosperity and Popularity meters | **Brass** (coin) and **local faction support** replace them. |
| Eight kingdom factions | **5 local fortress factions + 10 kingdom factions** (room for 6 / 12). |
| Map is the whole game screen | **Fortress view** with five rooms; the map is one room. |
| Three images per follower (healthy, injured, splash) | **Eight per follower**: five illustrated moods and three portrait states. |

Kept from v0.2: injury is common and death rare and telegraphed; deterministic seeded resolution;
Young Komodo's morning briefing with two truths and a lie; persistent Items of Power (one or two
equipped per run); the Mole Revolutionaries as enemies of the swamp witches; pre-Zuzu continuity
(Hollow Bell is still standing, Zuzu is not a recruit, the Abbess's order operates quietly).

## Money: Brass

The currency is **brass**: stamped salvage discs (washers, buttons and bolt-heads from the lost
humans' ruins) countersunk with the imperial mark. Counted as plain numbers ("40 brass"); slang
"bits". UI icon: a holed brass disc. It fits the project's ash-and-brass palette and the
relics-of-the-lost-humans canon without saying "gold" or "dollars".

*Silas's call if he wants another name; alternatives considered: scrip, tallies, rings. Changing it
is a string swap, so the build proceeds on "brass".*

- **Income:** taxes from each kingdom region, collected every morning (map room shows the rate).
  Quest rewards. Some throne-room choices (fines, bribes accepted, sold favors).
- **Spending:** follower wages (daily upkeep per recruited follower), recruitment fees, market
  items, barracks upgrades, healing, and throne-room solutions that cost brass.
- **Debt:** brass can go negative once (a loan from the Ledger, local faction) with a support
  cost; a second default triggers a Ledger crisis event, never a game over.
- Starting value: 120 brass, ~25/day taxes, ~4/day wage per follower. Tune by simulation.

## The day cycle

A day is one **Cycle** (the HUD shows "Day 17 · Act II"). Every day runs the same shape:

1. **Dawn report.** An animated night → dawn transition, then the results of anything that
   finished overnight: returning followers, quest outcomes (triumph / success / partial /
   failure), rewards, injuries, revealed secret traits, deaths, taxes collected, wages paid,
   faction shifts. Short cards, art-led, skippable.
2. **Komodo's briefing.** Three intelligence reports, two true and one false (kept from v0.2),
   plus one line of Young Komodo advice. 50 authored briefings, one per day.
3. **The Fortress.** The player moves freely between rooms (below), in any order: hold audiences
   in the throne room, talk in the barracks, buy at the market, check the map, assign quests.
   Nothing is timed inside the day.
4. **Finish.** A big Finish button (it warns about unheard audiences and expiring quests, but
   never blocks). Followers ride out, the day/night animation plays, quest days tick down, and
   the next dawn report begins.

Quest-specific aftermath appears **in the throne room** the next day (a grateful mayor, an angry
crow envoy) and, more lightly, as **barracks chatter** from the followers who were there.

## The Fortress: five rooms

### Throne room — daily audiences
2–4 audiences per day, each an art-led conversation with an NPC (illustrated reactions) or a
minor petitioner (text only). An audience can:
- **Recruit** a follower (often for a fee, sometimes for a promise).
- **Present a wasteland problem** whose solutions open **new quest paths**, map locations or
  story branches.
- Offer solutions that are **gated**: they cost brass, require a local faction support
  threshold ("needs Gate Watch 12"), a kingdom affinity tier ("Storm Crows: Friendly"), a
  follower present in the barracks, or a flag from an earlier choice. Locked options stay
  **visible with their requirement shown**, so the player learns what they could have afforded.
- Carry moral and flavor choices that shift faction support/affinity, follower opinion and flags.

Audiences come from three sources: the authored day script, consequences of past quests/choices,
and a seeded pool of minor petitions by region and faction.

### Quest room — the board
Quests are posted scrolls. Each has:
- **Title, region, issuing faction**, short art-free description with highlighted keywords.
- **Duration** 1–3 days (followers are away that long; results arrive the dawn after).
- **Expiry**: days left on the board (usually 1–3). An unassigned quest vanishes when it
  expires, with authored consequences: at minimum lost rewards; sometimes a faction penalty, a
  worse follow-up, or a throne-room complaint. Not every expiry punishes; some just pass.
- **Party size** 1–4 slots (a minimum and maximum).
- **Stat requirements** on the five stats, shown as bands (Low / Mid / High / Extreme). Some are
  **"?" until revealed** by a follower with the right secret skill, a Lamplight Archive
  threshold, a market map, or Komodo's hint.
- **Danger**: an injury range (for example "1–3 wounds") and an explicit **lethal** marker when
  death is possible. No lethal marker, no death.
- **Promised rewards**: brass, faction support/affinity, items, recruits, flags.

Assignment: drag or tap followers into slots. A preview shows the party's combined stats against
each band and an honest success estimate (exact when every requirement is known, a range when any
"?" remains). Faction modifiers, equipment and known traits apply in the preview; unknown secret
traits do not, so they can surprise.

### Barracks — the followers
- Grid of follower portraits (neutral / injured / dead state), sorted by availability:
  ready, on quest (days left), injured (days left), dead (memorial row).
- Selecting a follower opens the **full illustrated view**: stat wheel, equipment slots, known
  traits, unique ability, faction modifiers, biography, and **Talk**.
- **Talk** opens conversations: daily chatter (often about yesterday's quest), personal arc
  scenes, hidden-allegiance reveals and romance scenes. Each follower has a limited number of new
  conversations per day so the barracks is not a grind.
- **Capacity** starts at **6 beds**. Upgrades: 9 beds (cost brass), 12 beds (brass plus Gate
  Watch support). A full barracks blocks recruiting, not anything else.

### Market — equipment
- 2 equipment slots per follower (**tool/weapon** and **charm**). Items give stat bonuses, a
  power (for example "this quest takes one day less, minimum 1", "+affinity effect on Saltroad
  quests", "reveals one '?' requirement", "one fewer injury day"), or both.
- Stock rotates every few days, weighted by which kingdom factions are friendly (Saltroad
  caravans bring medicine, the Rustline sells relic tools, Storm Crow charms need Crow trust).
- Items are per-run. **Items of Power** (persistent, meta) are separate: they belong to the
  emperor, not to a follower, and still use the one-or-two equipped slots from v0.2.
- Healing services live here too: pay brass to shorten an injury by a day.

### Map room — the kingdom
- The kingdom map with **crested banners** for each kingdom faction's territory, settlements,
  fog over unrevealed land, and markers for active quests.
- Per region: controlling faction, **tax rate** paid to the throne, the faction's **affinity
  tier**, and current tensions with neighbors.
- Act-end changes are shown here first (see "Acts and the changing map").
- The map is information and choice context; quests are still assigned in the quest room.
- Geography, fortress floor plan and act overlays for the map art: [MAP-LAYOUT.md](MAP-LAYOUT.md).

*Phone layout: one room per screen with a bottom room bar. Desktop: the room fills the stage, with
the HUD strip (day, act, five local meters, brass) on top.*

## Factions

### Local fortress factions (5, room for a 6th)
Small-scale court politics, shown as **support counts** on the HUD (start ~10 each, roughly
0–30). Thresholds unlock throne-room solutions, market stock, barracks upgrades and special
quests. A meter at 0 triggers a crisis audience (a strike, a walkout, a plot), never a game over.

| Faction | Who | Wants |
|---|---|---|
| **The Ledger** | Merchants, money-changers, brass-stampers | Low taxes on trade, open roads, repaid debts |
| **The Old Houses** | Landed families who backed the throne | Precedence, land, their sons and daughters in office |
| **The Yard** | Laborers, cooks, stablehands, the fortress commons | Bread, fair wages, not being spent on the emperor's wars |
| **The Lamplight Archive** | Scribes, scholars, cartographers | Records kept, truth told, relics studied rather than sold |
| **The Gate Watch** | The fortress garrison | Pay, respect, defensible walls, a commander who does not waste them |

Optional sixth: **The Bell Chapel** (fortress clergy), if a playtest wants a faith voice separate
from the Abbey.

### Kingdom factions (10 by Act III, room for 12)
Location- and people-based, with **affinity −100..+100** shown as five tiers (Hostile, Wary,
Neutral, Friendly, Allied), each controlling **territory** that pays taxes when affinity is
Neutral or better. Each also has a hidden **strength** used for act-end map resolution.

| Faction | Home | Visible from |
|---|---|---|
| **Hollow Bell** (the Bell) | Border town, bell tower, Mayor Mara Reedbell | Day 1 |
| **The Abbey** (the convent of the Silent Bell, the Abbess's otter nuns) | Mission road, adobe walls | Day 1 |
| **Storm Crow Conclave** | Cave heights, west | Day 1 |
| **Mire Mothers** (swamp witches) | Mirefen wetlands, north | Day 1 |
| **Jackalwire Pack** (hyena raiders) | Rail canyon, south | Day 1 |
| **Saltroad Caravans** | Trade road villages | Day 1 |
| **Border Freeholds** | Scattered homesteads | Day 1 |
| **Mole Revolutionaries** | Underground; enemies of the Mire Mothers, opposed to the throne | Day 1 (hostile) |
| **The Rustline** (magpie and rat salvagers of the lost humans' ruins) | Sunken rail yards, east | Revealed end of Act I |
| **The Black Verge Court** (the gorilla powers; some bear vampiric or dark-magic conditions) | Far border | Revealed end of Act II |

Canon guardrails: factions are not species and do not decide an individual's morality
(WORLD-GUIDE.md). The Abbey's charity is a disguise for the cosmic-horror rites; harm to children
is stakes, never spectacle. The cosmic horrors released at Day 40 are tied to the Abbey's crypt;
their nature stays as unexplained as canon requires.

## Followers (20)

Four start in the barracks; the other sixteen are recruited through audiences, quests and
choices, and some can be missed entirely. F001–F010 from FOLLOWERS-PILOT-01.md are kept as the
first ten (their stats and traits get re-expressed in the v0.3 schema); ten more are authored.

**Each follower has:**
- **Five stats, 0–10**: **Might** (fighting, endurance), **Guile** (stealth, speed, tricks),
  **Wits** (invention, investigation, medicine), **Heart** (persuasion, comfort, courtly
  manners), **Lore** (magic, weather, the occult, old relics). Totals ~20–26 so no one is good
  at everything.
- **Secret skills (1–2) and secret weaknesses (1–2)**, hidden at first. Each is revealed the first
  time it **matters** on a quest or in a conversation ("Ash Quill can read Rustline glyphs";
  "Bram Coil panics underground"). Once revealed it shows on the card and in the preview.
- **Cross-run memory:** revealed traits are stored in a **persistent Codex** (meta-save, like
  Items of Power), so a player starting a new game already knows what they discovered before.
  Codex holds traits, unique abilities and biography pages unlocked; it never carries over items,
  brass or relationships.
- **One unique ability**, entirely their own (for example Wisp Fen: "Field Surgery: any injured
  party member on her quest returns with 2 fewer injury days"; Saffron Kett: "Jury-rig: once per
  quest, treat one failed requirement as met at Mid").
- **Faction modifiers**: per kingdom faction, +/− to that follower's effective stats on quests
  involving it, and sometimes extra dialogue options. The modifier reflects the follower's
  **true** allegiance, which may differ from their listed origin.
- **Origin vs. true allegiance**: the card shows home region and origin faction. Their biography
  and conversations can reveal a different loyalty. A follower raised as a slave by the Storm
  Crows lists Crow origin, but carries a hidden −3 on Crow quests and a hostile option in Crow
  audiences, until a barracks conversation reveals why (and may let the player change it).
  Hidden modifiers apply silently until revealed, then join the Codex.
- **Equipment**: 2 slots (market items).
- **Romance**: about 6 of the 20 are romanceable, a mix of genders and presentations, available
  regardless of how the emperor presents. Built through barracks Talk scenes, gifts and keeping
  promises; a romance has its own arc, can sour, and changes how that follower behaves on quests
  and at the final act. **Young Komodo is never romanceable.**
- **State**: ready, on quest (N days), injured (N days), dead.

**Injury and death.** Injury is the common setback: minor 1–2 days, serious 3–5, grave 6–8
(starting values). Death happens **only** on quests marked lethal (or authored sacrifices), only
on a bad result, and is announced in the dawn report with a memorial in the barracks. Target: zero
or one death in a competent full run.

## Art contract

**Followers — 8 images each, 160 total for 20:**
- **Illustrated (full character)** ×5 moods: **neutral, happy, excited, sad, angry**. Used in
  barracks Talk, throne-room scenes, recruiting and dawn reports.
- **Portrait (small bust)** ×3 states: **neutral, injured, dead**. Used on the barracks grid,
  quest slots, HUD and reports. *Dead* is a memorial treatment (desaturated, candle or ribbon
  frame), never gore.
- One locked character design sheet per follower, used as the reference for all eight so the
  character stays recognizable. Batch in fives with an editorial check before scaling.

**Major NPCs** (Young Komodo, Mara Reedbell, the Abbess, faction envoys, ~12–16 total): the same
**five illustrated moods**, **no portraits**. Young Komodo also gets one extra: **betrayal**.

**Minor petitioners**: no portrait; a faction crest and text are enough.

Asset ids: `followers/FNNN/illustrated/{neutral,happy,excited,sad,angry}`,
`followers/FNNN/portrait/{neutral,injured,dead}`, `npcs/<slug>/illustrated/<mood>`. Render
through Kind Robots ArtJobs; a queued job, prompt or placeholder is not a delivered image. Runtime
fallback: missing mood → neutral illustrated; missing injured/dead portrait → neutral portrait
with a temporary state badge; never a broken image.

## Dialogue presentation

- Art-driven scenes: one or two illustrated speakers over a room or location background.
- Simple, stylish text box: nameplate, body text, a short choice list (2–4), a **log** button
  for history.
- **Text streams** in typewriter style. Tap/click once to finish the line instantly, again to
  advance. A speed setting (normal / fast / instant) persists per player.
- Choices that need brass, support, affinity or a follower show the requirement and stay
  disabled when unmet.

## Acts and the changing map

Five acts of ten days. **Days 10, 20, 30 and 40 each end with a map event** shown in the map room
and announced at dawn:

| Act | Days | Arc | Act-end map event |
|---|---|---|---|
| I · The Crown of Salvage | 1–10 | Founding the court, first taxes, first followers, first quests | Fog lifts over the **Rustline**; the strongest pressure of Act I resolves (for example a Jackalwire raid takes or loses a Freehold village) |
| II · Rain Debt | 11–20 | Drought, rain bargains, food, the Storm Crows' price | Territory shifts by weather: the Mirefen spreads or dries, Crow covenants claim land; **Black Verge Court** revealed; funded projects appear (a repaired aqueduct, a new market road) |
| III · Kind Roads | 21–30 | Smuggling, raids, the Abbey's hospitality, missing children evidence | Faction wars resolve on the map: the weaker side loses territory; **a faction can be wiped out** if its strength reached zero |
| IV · The Long Table | 31–40 | Open faction war, alliances, Komodo's clues tighten | **Day 40: Young Komodo betrays the emperor**, the kingdom erupts in war and the **cosmic horrors are unleashed** from beneath the Abbey; the fortress falls |
| V · The Hideout | 41–50 | On the run with revolutionaries; rebuild alliances; final confrontation | Day 50 ending |

**Faction strength and wipe-outs.** Each kingdom faction has hidden strength (0–10) moved by
quests, wars and player support. At each act end, faction pairs at war compare strength; the loser
cedes a region. A faction at 0 strength is **wiped out**: its banner leaves the map, its taxes
stop, its quests close, and its surviving people scatter (some followers' allegiance changes,
new refugee audiences appear). A wipe-out is always **telegraphed one act ahead** in reports and
audiences, and only at act ends. Player choices can save or doom any faction, the Bell included;
game branches stay alternate history and never decide who destroys Hollow Bell in Book One.

## Young Komodo and the betrayal

Young Komodo is the emperor's advisor: the morning briefing, hints on "?" requirements, dry jokes
about the price of promises. **Not romanceable.**

- The betrayal at the end of Act IV (Day 40) **always happens**. What changes with play is who
  Komodo hands the fortress to, how many followers he takes with him, and what the player saw
  coming.
- Clues are seeded from Act I: several of the false reports in his briefings turn out, in
  hindsight, to be **his own lies**; with the Eye of the Elder Crow equipped a replaying player
  can catch them early. Barracks followers notice his errands. The Lamplight Archive can find a
  ledger page that does not add up.
- Proposed motive (Silas to confirm or replace): Komodo has made a bargain with the Abbess's
  order, believing that only a surrendered throne lets the wasteland survive what is waking under
  the Abbey. He thinks he is the pragmatic one.
- Followers with low loyalty or a hidden allegiance aligned with Komodo's buyer may leave with
  him; a revealed romance or a completed personal arc protects against that.

## The final act: the hideout

From Day 41 the fortress view is replaced by a **hideout** with the same room functions in
rougher form (audience corner, bunks, a peddler, a scratched map, a quest wall). **Where** it is
depends on which kingdom faction the player built up most, with the highest affinity and strength:

- Mole tunnels under the badlands (Mole Revolutionaries)
- A Storm Crow cave (Storm Crow Conclave)
- Hollow Bell's cellars beneath the bell tower (Hollow Bell)
- A painted wagon circle in the rail canyon (Jackalwire Pack)
- A moving caravan (Saltroad Caravans)
- A hidden barn and root cellar (Border Freeholds)
- A collapsed rail station (The Rustline)
- Fallback when no faction is Friendly or better: a nameless cave with a handful of
  revolutionaries (always reachable, so a weak run never softlocks)

Each hideout changes Act V's quest pool, market and ending options. Brass income drops to what the
host faction shares. Days 41–50 build alliances against Komodo's patron and the horror, ending on
Day 50.

**Ending families** (revised from v0.2's eight; final list set during Act V scripting): the Bell
Restored, Open Roads, Iron Peace, the Crow's Bargain, the Witchwater Throne, Tunnels and
Councils (Mole settlement), the Long Night (the horror wins, the survivors scatter), and A
Hundred Candles (heavy losses, every dead follower named).

## Saves, load and rewind

Silas, 2026-10-18: *"given the nature of passing and failing quests, we should have a robust
load/save system, and allow the player the option to rewind to previous days (though random
events will stay random, another pass will not create the same events necessarily)."*

- **Autosave** after every action (an audience answered, a quest assigned, Finish).
- **Dawn snapshots:** the save keeps the run as it stood at the start of every day so far.
- **Rewind** to the dawn of any earlier day (or restart today). Later days are discarded.
- **Rewinding starts a new branch.** Seeded events after that point roll fresh: the dawn's random
  chores, quest results, injuries and deaths can all come out differently. Authored content
  (the day's script, the audiences, the quests your answers post) stays the same, and your
  choices still decide what is offered.
- **Manual slots** (three to start) with a label and timestamp, each holding the full run and its
  dawn snapshots, so a slot can be rewound too.
- **Meta progress survives rewinds and reloads:** the Codex (revealed traits and allegiances) and
  Items of Power are never rolled back. A player who learned a secret on a failed branch keeps it.
- **Robustness:** every save is validated before it is written and when it is read (known ids,
  bounded values, no double-booked follower). An unreadable save is never overwritten; the game
  says so and offers a new run or a slot. Storage that is blocked or full is reported, not
  ignored.

## Items of Power (persistent, kept from v0.2, travel items reworked)

One slot per run at first, a second unlocked by progress. The Eye of the Elder Crow highlights the
false report. Hours no longer exist, so **Komodo's Brass Hourglass** becomes "once per act, one
quest finishes a day early (minimum 1)" and **Crowstep Spurs** becomes "once per act, one quest
expiry is extended by one day". The Bellkeeper's Seal, the Mole King's Lantern and the Ember Ward
keep their effects, re-timed to the 50-day calendar (Acts II–IV). The Codex (revealed traits) is
also persistent but is not an Item of Power and uses no slot.

## Content targets for 50 days

- 50 authored days, each with: one Komodo briefing (3 reports), 2–4 throne-room audiences (at
  least one authored), 2–5 quests on the board (1–2 authored, the rest from seeded templates by
  region/faction), night aftermath and barracks chatter hooks.
- 20 followers fully authored; ~12–16 major NPCs with five moods each; Komodo's betrayal track.
- 5 local + 10 kingdom factions with strength, territory, taxes and act-end rules.
- 4 act-end map events, ≥7 hideout variants, 8 ending families.

## Acceptance for implementation

- No Horde, troop or hour/travel state anywhere in the engine, saves or UI; saves from v0.2
  pilot runs are discarded with a clear "new version" notice rather than migrated by guesswork.
- Exactly 50 days; quests take 1–3 days, use 1–4 followers, expire with authored consequences.
- No follower double-booked; injured and dead followers cannot be assigned.
- Deaths only on lethal-marked quests or authored sacrifices.
- Secret traits reveal when relevant, persist in the Codex across runs, and appear in previews
  once known.
- Brass, five local supports and ten kingdom affinities are bounded and explained in the dawn
  report.
- Act-end map events fire on Days 10/20/30/40; wipe-outs telegraphed one act ahead.
- Komodo's betrayal fires on Day 40 in every run; the hideout always resolves to a location.
- Text streaming with instant-complete and a persisted speed setting.
- Deterministic within a branch (seed + branch + choices → same run, for tests); a rewind
  advances the branch so replayed days roll fresh. Autosave, dawn snapshots for every day, three
  manual slots, validated saves that never overwrite unreadable data.
- Responsive at 390 / 768 / 1440.
- Still private Admin only; public `/play` remains Silas's explicit release gate (t-010).
