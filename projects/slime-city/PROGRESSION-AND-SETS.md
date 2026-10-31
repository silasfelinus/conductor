# Slime City progression, faction strengths and expansion sets
Decision brief, 2026-10-30 PT. User direction: daily and weekly challenges; CPU battles award XP; unlock cards through virtual-Meat packs only, randomly chosen from uncollected cards with one guaranteed rare. Implementation issue: [Slime City #4535](https://github.com/silasfelinus/kind_robots/issues/4535).

## Product loop
Blackout CPU battle → XP + Meat → daily/weekly claim → buy a 3-card Street Pack for 100 Meat → collect distinct cards → eventually build a legal constructed deck. All six existing 10-card starter decks are **loaner decks**, always playable from level 1. Unlocking a collectible does not remove the loaner; collection ownership matters for future constructed decks, not immediate pay-to-win power. No paywalls, cash, conversion to money, external trading, or real-money transactions.

**Level curve:** level = 1 + floor(sqrt(XP / 100)); level 2 at 100 XP, level 3 at 400 XP, level 4 at 900 XP. No card power is tied to level. Suggested future ability unlocks: level 2 faction dossiers; level 3 experimental deck editing and two constructed slots; level 5 district challenge contracts; level 8 alternate AI personas; level 12 additional deck slots / cosmetic profiles. Keep all faction loaners playable even if the player never opens a pack. These are roadmap decisions, not all implemented.

### Starter rewards (internal proof of concept)
- WIN: 80 XP + 45 Meat; DRAW: 35 XP + 15 Meat; LOSS: 25 XP + 10 Meat.
- First ten completed CPU bouts per Pacific calendar day earn base payout, then free practice stays available with no base payout. Distinct command/seed match receipts do not pay twice. **The database is authoritative.** Every user has an account-owned wallet, XP, collection and claims. CPU battles use server-issued match IDs/seeds and are replay-verified for a once-only payout.
- Dailies: Clock In (one bout, +20 Meat/+20 XP); Own the Pit (one Blackout win, +35/+35); Union of Monsters (three creature cards deployed, +25/+25).
- Weeklies: Street Champion (five CPU wins, +125 Meat/+150 XP); Six-Crew Sampler (battle with three distinct crews, +85/+100); Cardboard Riot (24 cards played, +110/+120).
- Windows reset daily at Pacific midnight, weekly on Monday at Pacific midnight. Challenges claim once per period and **do not** use daily streaks or FOMO timers.
- The internal `/admin/slime-city` view uses authenticated API routes for all reads, purchases, claims and match settlement. New additive `SlimeCityAccount` and `SlimeCityMatch` tables store all wallet, inventory, XP and audit data. Client-side data is display state only, never currency authority. The broader t-008/t-010 roadmaps remain incomplete.

### Street Pack v0
- Cost: **100 virtual Meat**; contents: exactly **3 previously uncollected cards**, **one guaranteed RARE** and two **COMMON or UNCOMMON**. Zero duplicates across packs and no repeat of the same card already collected. Rarity and collection probability are transparent.
- Current pool: 60 authored cards, 20 RARE / 40 other, exactly 20 possible packs. Rare selection is deterministic given a random entropy seed (to allow tests) but drawn from the remaining uncollected rare pool; the other two come from the remaining other-card pool. If one of the pools is empty, **sold out / cannot purchase**, not a degraded guarantee or replacement duplicate.
- V0 rare pool uses three marked cards per crew (signature creature + two special slots), plus one extra marked special each for Catgirls and Undertow (weaker from old POC). Printed rarity does **not** increase a card's combat statistics; rarity describes collection scarcity, not a right to win.
- Future larger sets must package a balanced ratio of rare-or-better to two normal cards; avoid impossible guarantees near exhaustion. The player sees pack price and contents before paying. **No paid randomness** and no lootbox purchases with real money.

## Distinct faction strengths and counterplay

| Crew | Primary strength | Deliberate weaknesses and counterplay | Set design constraint |
| --- | --- | --- | --- |
| Gene Riot Catgirls, Blue biotech | Agile 1–2-range positioning, regen/heal and one-time Ambush; clever surgical attacks | Vulnerable to direct piercing damage, anti-heal and forced movement. Sustain should be a strategic decision, not infinite AP | No repeatable free healing loops or turn-one instant kill |
| Punk Bloodfairies, Purple swarm | Cheap wide deployment, flying/frenzy pressure, SWARM buffs and LEECH | Weak one-on-one bodies, fragile under area attacks and armored chokepoints | Swarm buffs cap at +1 per source; swarm should not trivially flood field cap |
| Ironjaw Chrome Ogres, Green forge | Highest armor, BULLDOZE, durable battlefield anchors | Slow starts, low range, vulnerable to blue traps, rooting and Meat Exchange mana debt | No unbreakable armor stacks; explicit armor piercing counters |
| Riot Saints, Red chaos | VOLATILE death bursts, explosive area effects, tempo disruption | Risk of friendly fire, inconsistent survivability, lower sustained endurance | Random effects bounded and replayable from seed, visible blast radius |
| Undertow Intelligence, Blue espionage | Stealth, vision denial, SNARE, two traps, reconnaissance and PIERCE | Low open-combat HP; falls to proactive board sweep and early rush | **Stealth is an explicit card keyword**, never global hidden-deployment privilege; opponent gets discoverable counters |
| Meat Exchange, Gold extortion | CONTROL, COLLECT, debt/discount, economic denial and costly finishers | Slow early mana and vulnerable to fast aggressive decks | Debt capped and always telegraphed; avoid taxation locks that deny any playable turn |

**Balance target:** seeded CPU-v-CPU cross-faction matrix with both seating orders, 100+ seeds per pair, same starting XP and starter legality. Aim 40–60% head-to-head win share absent explicit intended counters, >30% even for worst pairing, no unwinnable locks, first meaningful choice before round 2. Watch Catgirls (formerly Blackout 76% in legacy game), Undertow (32% legacy), and Meat Exchange/Steel armor interactions, but **re-measure on the new 10×6 open Blackout** before nerfs. Legacy 8×8 benchmark is no longer a reliable balance baseline.

## Card-set roadmap
- **Founders of the Pit (S0)**: the 60 existing distinct authored starter cards (ten per crew). Current pack/rarity prototype uses 20 rares + 40 common/uncommon. Existing art ledger only covers 36 old card briefs; 24 additional art deliveries need verification and attachments.
- **The Gutter Crown (S1)**: **50 new collectible cards per crew = 300 total**. Preserve the mathematical guarantee with exactly **100 RARE-or-LEGENDARY + 200 COMMON/UNCOMMON** cards, sufficient for 100 strictly duplicate-free three-card packs. Per crew, assign 20 COMMON and two LEGENDARY; give four crews (Catgirls, Undertow, Bloodfairies, Ironjaw) 13 UNCOMMON and 15 RARE each, and two crews (Riot Saints, Meat Exchange) 14 UNCOMMON and 14 RARE each. Totals: **120 common + 80 uncommon + 88 rare + 12 legendary = 300**. Every pack has **exactly one** of the 100 rare-or-better and two of the 200 common/uncommon, until all 100 packs are bought. The rare card is guaranteed, but its subclass (rare vs legendary) is randomly selected from the uncollected eligible rare-or-better pool, with odds that adapt as the uncollected inventory shrinks; reveal the exact remaining eligible counts before spending. Do not recycle duplicates or quietly substitute common cards when rare inventory is empty. Rarity does not directly increase printed combat numbers.

- **Faction campaigns (S2)**: unique six story arcs, rival captains, distinct deck archetypes and authored rare rewards. Story unlocks should add cards to the *nonrare* pool or fixed choice rewards, never invalidate a purchased rare guarantee.
- Cosmetics and the city overworld can have independent unlocks. No card or unit gets larger printed attack solely because of rarer rarity or account level.

## Secure delivery dependency
The first account-owned API, issued CPU match IDs and transactional ledger are implemented; t-008 still requires a stronger anti-bot review, transaction history, campaign integration, and actual deployed schema verification before a general launch.

## Challenge fairness
Daily and weekly progression should reward broad gameplay, not force a single purchased faction or scarce card. Every launch-day challenge must be achievable using free loaner decks and should remain completable without opening packs. No consecutive-day streak penalties or compulsory purchases.

## Next design decision
Run at least 100 seeded test games with each crew on both sides in open-information Blackout and collect failure causes. Only then finalize stats and decide whether the next authored 50-card-per-crew expansion should be staged as ten-card batches with real ArtJobs. Prioritize quality and unique crew identities over sheer item count.
