# Emperor of Dust: balance report

*Generated for `emperor-of-dust/t-009` on 2026-10-20 from kind_robots
`utils/scripts/emperorFortressBalanceReport.ts` (the same simulation
`verifyEmperorFortressBalance.test.ts` holds in CI). Re-run it after content or
engine changes and paste the table between the markers.*

## How it plays

Each policy plays whole 50-day campaigns through the real engine. It takes on
every follower who offers, buying beds when it can afford them, and answers
every audience by its own rule. It staffs quests with the best-odds party when
the odds are 45% or better, except the reckless and idle policies.

- **Greedy** takes the first answer; **random** varies it; **spurn-all** helps
  nobody it can avoid helping.
- **Reckless** sends the smallest party anywhere, whatever the odds.
- **Idle** answers petitions against everyone and never sends a party.
- **Patron of X** always picks the choice that raises X most. Between equal
  choices it helps no other host, and it staffs X's quests first.

Patrons do not shop in the market, so their brass is a ceiling, not a floor.

## Findings and fixes (t-009)

| Finding | Fix |
|---|---|
| The Freehold barn won the hideout in nearly every run, whoever the crown courted. Chores and Act I dawn quests pushed the Freeholds to 100 affinity. | Chores pay 3 affinity, not 5–8. Five new chores cover the Storm Crows, Mire Mothers, Pack, Moles and Rustline, and a faction's chores wait for its banner. The hideout weighs **pledges** (story flags where the crown took a side) at 20 each on top of affinity. |
| The Rustline had almost nothing to win. | Two Act IV choices: the Day 31 Ford barricade and the Day 37 salvage market. Blue Lantern pays the Rustline on a plain success, and buying Jinx's crate counts as a pledge. |
| About 20 Ledger loans per run with a full barracks: taxes top out at 41 brass a day, and 12 followers at 6 cost 72. | Wage is 4 per follower. |
| A Hundred Candles (3 deaths) was unreachable with five lethal quests. | It now takes two deaths. The Well That Spoke and the Bell's Lost Clapper are lethal. |

## Notes for later
- **Iron Peace** is common among patrons of the Pack, the Rustline and the Bell.
  That is the bots' Day 49 rule (Open Roads helps other hosts), not a game rule.
  Six peaces serve seven hosts and the Mire Mothers, so the Pack, Rustline,
  Saltroad and Freeholds share the general peaces.
- **Faction wipe-outs** happen only to neglect (the idle policy, about one per
  run). The act-end war rules in SYSTEMS-V03.md, where a war's loser cedes a
  region, are not built yet.
- **t-028** still owes hideout income (the host's share) and followers leaving
  with Komodo. Act V brass will tighten when that lands, so re-run this report.

<!-- balance-report:start -->
40 seeded campaigns per policy (seeds 1–40), all 50 days, played through the real Kind Robots engine.

| Policy | Hideouts | Endings | Deaths / run | Runs losing 2+ | Loans / run | Factions wiped / run | Lowest final brass |
|---|---|---|---:|---:|---:|---:|---:|
| Takes the first answer (`greedy`) | freehold-barn 40 | Open Roads 40 | 0.05 | 0 | 2.00 | 0.00 | 0 |
| Answers at random (`random`) | freehold-barn 35, bell-cellars 2, mole-tunnels 2, moving-caravan 1 | Open Roads 20, The Bell Restored 10, The Crow’s Bargain 5, Iron Peace 3, The Witchwater Throne 2 | 0.10 | 0 | 2.67 | 0.00 | 2 |
| Favours nobody (`spurn-all`) | freehold-barn 28, moving-caravan 12 | Iron Peace 37, The Long Night 2, A Hundred Candles 1 | 0.13 | 1 | 1.80 | 0.00 | 0 |
| Sends anyone, anywhere (`reckless`) | freehold-barn 40 | Open Roads 30, The Long Night 9, A Hundred Candles 1 | 0.30 | 1 | 4.08 | 0.00 | 1 |
| Never sends a party (`idle`) | nameless-cave 40 | The Long Night 40 | 0.00 | 0 | 12.30 | 1.00 | 1 |
| Patron of moles (`patron:moles`) | mole-tunnels 40 | Tunnels and Councils 40 | 0.17 | 0 | 0.57 | 0.00 | 4 |
| Patron of storm-crows (`patron:storm-crows`) | crow-cave 36, freehold-barn 4 | The Crow’s Bargain 40 | 0.07 | 0 | 1.07 | 0.00 | 5 |
| Patron of hollow-bell (`patron:hollow-bell`) | bell-cellars 40 | Iron Peace 28, The Bell Restored 11, A Hundred Candles 1 | 0.17 | 1 | 2.00 | 0.00 | 2 |
| Patron of jackalwire (`patron:jackalwire`) | wagon-circle 38, moving-caravan 1, freehold-barn 1 | Iron Peace 39, A Hundred Candles 1 | 0.15 | 1 | 2.63 | 0.00 | 1 |
| Patron of saltroad (`patron:saltroad`) | moving-caravan 40 | Open Roads 40 | 0.05 | 0 | 3.52 | 0.00 | 1 |
| Patron of freeholds (`patron:freeholds`) | freehold-barn 40 | Open Roads 40 | 0.07 | 0 | 2.88 | 0.00 | 3 |
| Patron of rustline (`patron:rustline`) | rail-station 35, freehold-barn 4, moving-caravan 1 | Iron Peace 39, A Hundred Candles 1 | 0.13 | 1 | 1.68 | 0.00 | 0 |
| Patron of mire-mothers (`patron:mire-mothers`) | freehold-barn 21, moving-caravan 18, bell-cellars 1 | The Witchwater Throne 34, Iron Peace 5, A Hundred Candles 1 | 0.13 | 1 | 2.60 | 0.00 | 3 |
<!-- balance-report:end -->
