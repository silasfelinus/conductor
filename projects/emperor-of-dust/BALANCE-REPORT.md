# Emperor of Dust: balance report

*Originally generated for `emperor-of-dust/t-009` on 2026-10-20, updated 2026-10-22 from kind_robots
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
40 fresh-onboarding campaigns per policy (seeds 1–40), each lasting 50 game days. Run against the real Kind Robots engine on 2026-10-22 (`verifyEmperorFortressAdversarial.test.ts`).

| Policy | Hideouts | Endings | Deaths / run | Runs losing 2+ | Loans / run | Factions wiped / run | Lowest final brass |
|---|---|---|---:|---:|---:|---:|---:|
| Takes the first answer (`greedy`) | freehold-barn 40 | Open Roads 38, The Long Night 1, A Hundred Candles 1 | 0.30 | 1 | 0.60 | 0.00 | 5 |
| Answers at random (`random`) | freehold-barn 23, bell-cellars 13, moving-caravan 3, mole-tunnels 1 | Open Roads 19, Iron Peace 12, The Bell Restored 4, The Long Night 2, The Crow’s Bargain 2, Tunnels and Councils 1 | 0.33 | 0 | 0.90 | 0.00 | 0 |
| Favours nobody (`spurn-all`) | freehold-barn 38, moving-caravan 2 | Iron Peace 38, The Long Night 2 | 0.20 | 0 | 0.50 | 0.00 | 12 |
| Sends anyone, anywhere (`reckless`) | freehold-barn 39, bell-cellars 1 | Open Roads 29, The Long Night 9, A Hundred Candles 2 | 0.50 | 3 | 3.00 | 0.00 | 5 |
| Never sends a party (`idle`) | nameless-cave 40 | The Long Night 40 | 0.00 | 0 | 8.45 | 1.00 | 1 |
| Patron of moles (`patron:moles`) | mole-tunnels 40 | Tunnels and Councils 39, A Hundred Candles 1 | 0.28 | 1 | 0.38 | 0.00 | 27 |
| Patron of storm-crows (`patron:storm-crows`) | crow-cave 36, freehold-barn 4 | The Crow’s Bargain 37, A Hundred Candles 2, The Long Night 1 | 0.40 | 2 | 0.17 | 0.00 | 15 |
| Patron of hollow-bell (`patron:hollow-bell`) | bell-cellars 40 | The Bell Restored 23, Open Roads 11, Iron Peace 4, The Long Night 2 | 0.35 | 1 | 0.30 | 0.00 | 3 |
| Patron of jackalwire (`patron:jackalwire`) | wagon-circle 39, freehold-barn 1 | Iron Peace 39, A Hundred Candles 1 | 0.25 | 1 | 0.38 | 0.00 | 0 |
| Patron of saltroad (`patron:saltroad`) | moving-caravan 40 | Open Roads 40 | 0.25 | 0 | 0.70 | 0.00 | 12 |
| Patron of freeholds (`patron:freeholds`) | freehold-barn 40 | Open Roads 39, The Long Night 1 | 0.40 | 0 | 0.45 | 0.00 | 38 |
| Patron of rustline (`patron:rustline`) | rail-station 36, freehold-barn 4 | Iron Peace 39, The Long Night 1 | 0.33 | 0 | 0.75 | 0.00 | 1 |
| Patron of mire-mothers (`patron:mire-mothers`) | freehold-barn 40 | The Witchwater Throne 35, Iron Peace 4, The Long Night 1 | 0.38 | 0 | 0.33 | 0.00 | 10 |


### Post-merge recruitment stress test (2026-10-22)

- **552 complete campaigns / 27,600 simulated days**, including 1,632 validated dawn states. All eight ending families occurred.
- **240 new opening seeds / 480 rival-choice branches.** All four visitor-and-dispute combinations occurred. Rewinding changed the selected visitors or rival dispute in 342 of the 480 branches without leaving a broken court; one confirmed Day 1 rewind defect was fixed.
- The first day displayed **at most 2 quests**, rather than six or more. No duplicate or mutually excluded recruits entered tested runs.
- Across the 520 base strategy runs: 158 deaths (9 campaigns losing two or more), 676 loans and 40 faction wipe-outs (all 40 in the deliberately idle runs).
- **Writing/balance follow-up:** `spurn-all` still reaches Iron Peace in 38/40 seeds. This appears thematically cheap and warrants inspecting the peace eligibility conditions, rather than weakening the simulation thresholds.

Verification: GitHub Actions `Emperor of Dust Dispatch Contract` for Kind Robots commit `fb001af317db2b1cd79f0f7b92e4544de97303ad`.
<!-- balance-report:end -->
