# Shifting Desks balance report

Task: shifting-desks t-019. Five policy bots and a random baseline each play 2,000 seeded runs through all
five departments, using the real game engine (Kind Robots `utils/shiftingDesks/balance.ts`). Same seeds,
same numbers, every time.

- **Regenerate:** in kind_robots, `npx tsx utils/scripts/shiftingDesksBalanceReport.ts`. Paste its output
  between the generated markers below.
- **Thresholds:** `utils/scripts/verifyShiftingDesksBalance.test.ts` fails the Shifting Desks gameplay CI job
  when a pack change breaks them.

## The bots

Each bot picks the open choice that best fits its temperament. Ties are broken by the run's seeded dice.
Every bot spends Forms on rolls while it has more than two, and uses its society favor and mutation whenever
they apply.

| Bot | Plays for |
|---|---|
| The Complier | the highest Obedience grade on the card |
| The Rebel | the highest Spite grade |
| The Coward | no dice, then the lowest cost, then the least attention |
| The Saint | the highest Empathy grade |
| The Schemer | the highest Ingenuity grade (added so all four grades have a bot) |
| Random baseline | any open choice, uniformly |

## Thresholds the test holds

- **No clean wins.** Every temperament loses at least 2 Successors per run on average.
- **Elimination stays a risk, not the norm.** No temperament is eliminated in more than half its runs, and
  every temperament finishes at least 40% of them.
- **No floor is a massacre.** No temperament loses more than 2 Successors per run in any one department.
- **Every ending is earned.** Each of the 10 endings is reached by some temperament, and random play alone
  reaches all 10.
- **Safety never buys a payoff.** The Coward only ever ends as Employee of the Month, in Early Retirement or
  eliminated.
- **No dominant choices.** No card has a choice that all five temperaments agree on.
- **No dead choices.** Any choice no bot ever picks must be gated behind a flag. Deep callbacks may stay
  rare.

## What the first run found, and what changed

| | Complier | Rebel | Coward | Saint | Schemer | Random |
|---|---:|---:|---:|---:|---:|---:|
| Eliminated, before | 18.8% | 39.5% | 0.1% | 21.3% | **54.0%** | 16.5% |
| Eliminated, after | 18.7% | 35.8% | 0.1% | 19.9% | 45.0% | 14.4% |
| Orientation Successors lost per run, before | 0.72 | 1.53 | 0.51 | 0.51 | **1.93** | 0.98 |
| Orientation Successors lost per run, after | 0.72 | 1.10 | 0.51 | 0.45 | 1.18 | 0.77 |

1. **The 90-Day Review, `swap-the-file`.**
   - The problem: it charged a Successor up front, then rolled a Dire 11. A failed review is re-dealt up to
     three times, so a Schemer could lose three Successors before reaching Records. The choice's own hint
     says *"Success spends a Successor's clean record."*
   - The fix: the Successor is now spent on success, the up-front cost is 1 composure, and the roll is Risky
     (9).
   - This was the Schemer's biggest killer, and it put the Schemer over the 50% ceiling.
2. **The squeak-code secret: `return-the-mustaches` was never picked in 12,000 runs.**
   - The chain spans three floors: Toy Division's Dire `squeeze-the-duck` (or Dale's apology) opens Wellness's
     Humming Door, which opens Sub-Level Zero's mustaches. Only about 1 run in 700 got through it.
   - The fix: `squeeze-the-duck` is now Risky (9), and the Humming Door and the Spare Mustaches went from
     weight 2 to weight 3.
   - Random play now completes the chain about 2.3 times as often. It stays a secret, but a findable one.
3. **Hints must tell the truth.** A new conductor test checks two things:
   - a hint's difficulty word (Routine, Risky or Dire) matches its roll;
   - a hint that says success spends a Successor doesn't also charge one up front.
4. **Left alone, because the data says so:**
   - **The thaw.** Lowering it from 2 to 1 roughly doubles elimination for every temperament except the
     Coward (Saint 20% → 42%, Schemer 46% → 72%), so it stays at 2.
   - **Card costs elsewhere.** Every other floor is within the thresholds.

## Open design calls (for t-020, Silas's fun verdict)

- **The Coward almost never dies, but it pays for that.**
  - It survives 99.9% of runs. It still loses 2.65 Successors per run, and it never sees any of the 7 payoff
    endings.
  - That reads as *Papers, Please*: obedience keeps you alive and keeps you small.
  - If it should also be deadly, the lever is the no-roll "safe" choices that trade composure for clearance.
- **Clearance hits its cap all the time.** The Complier and Rebel bump into clearance 5 five to six times a
  run, so late "+1 clearance" rewards are worth nothing. A clearance sink or spend, such as a clearance-gated
  route on every floor, would make those trades real. That's a design change, not a tuning pass.
- **Pure styles see few endings.** The Complier and Rebel each see 3 of 10. Mixed play (random baseline, 10 of
  10) is rewarded, which is the intent.

## Generated report

<!-- generated:balance -->
2000 seeded runs per policy (seeds `balance-<policy>-<n>`, job titles in rotation), played through the real Kind Robots engine.

### Survival

| Policy | Finished | Eliminated | Successors lost / run | Endings seen |
|---|---:|---:|---:|---:|
| The Complier | 81.3% | 18.7% | 4.91 | 3 of 10 |
| The Rebel | 64.2% | 35.8% | 5.42 | 3 of 10 |
| The Coward | 100.0% | 0.1% | 2.65 | 3 of 10 |
| The Saint | 80.1% | 19.9% | 4.99 | 9 of 10 |
| The Schemer | 55.0% | 45.0% | 5.72 | 8 of 10 |
| Random baseline | 85.5% | 14.4% | 4.74 | 10 of 10 |

### Successors lost per run, by department

| Policy | Orientation | Records & Forms | Toy Division | Wellness & Testing | Sub-Level Zero |
|---|---:|---:|---:|---:|---:|
| The Complier | 0.72 | 1.50 | 0.88 | 0.88 | 0.93 |
| The Rebel | 1.10 | 0.41 | 1.71 | 1.15 | 1.06 |
| The Coward | 0.51 | 0.16 | 0.47 | 0.56 | 0.96 |
| The Saint | 0.45 | 0.86 | 1.36 | 1.13 | 1.19 |
| The Schemer | 1.18 | 0.37 | 1.67 | 1.06 | 1.44 |
| Random baseline | 0.77 | 0.66 | 1.13 | 0.98 | 1.20 |

### Endings (share of runs)

| Ending | The Complier | The Rebel | The Coward | The Saint | The Schemer | Random baseline |
|---|---:|---:|---:|---:|---:|---:|
| Employee of the Month | 42.2% | · | 45.0% | 1.2% | 0.1% | 19.3% |
| Promoted to Management | · | 59.2% | · | · | 14.3% | 21.6% |
| Escape Through the Ducts | · | · | · | 1.1% | 13.4% | 1.3% |
| Roach Union General Strike | · | · | · | 22.8% | · | 1.8% |
| Society Coup | · | · | · | 3.3% | · | 1.4% |
| Whistleblower | · | · | · | 5.3% | 1.9% | 2.8% |
| Early Retirement | 39.1% | · | 55.0% | 39.5% | 22.0% | 36.0% |
| The Kind Rewrite | · | · | · | 2.4% | 1.4% | 0.3% |
| Position Eliminated | 18.7% | 26.0% | 0.1% | 17.8% | 32.8% | 13.6% |
| The Department of Posthumous Affairs | · | 9.8% | · | 2.1% | 12.3% | 0.8% |

### Meter limits hit per run

| Policy | clearance:max | composure:max | composure:min | forms:min | successors:min | suspicion:max | suspicion:min |
|---|---:|---:|---:|---:|---:|---:|---:|
| The Complier | 6.02 | 0.01 | 3.02 | 0.57 | 0.12 | 0.10 | 3.33 |
| The Rebel | 5.09 | 0.02 | 0.96 | 0.44 | 0.05 | 3.39 | 0.90 |
| The Coward | 4.71 | 0.16 | 0.94 | 0.35 | 0.00 | 0.60 | 2.89 |
| The Saint | 1.18 | 0.15 | 0.70 | 0.73 | 0.07 | 2.99 | 0.41 |
| The Schemer | 2.27 | 0.01 | 1.45 | 0.64 | 0.15 | 2.90 | 1.03 |
| Random baseline | 4.45 | 0.03 | 1.61 | 0.56 | 0.07 | 1.56 | 1.49 |

### Top causes of termination

| Policy | Causes (per run) |
|---|---:|
| The Complier | Nervous breakdown 2.95; The Form That Requires Itself 0.76; The Board 0.42; The Guard Who Is Also You 0.24 |
| The Rebel | A short, friendly conversation 3.09; Nervous breakdown 0.94; Your 90-Day Review, Today at 3 0.89; The Successor Waiting Room 0.20 |
| The Coward | Nervous breakdown 0.94; A short, friendly conversation 0.60; The Board 0.55; Your 90-Day Review, Today at 3 0.27 |
| The Saint | A short, friendly conversation 2.86; Nervous breakdown 0.66; The Board 0.45; The Drop Test 0.33 |
| The Schemer | A short, friendly conversation 2.62; Nervous breakdown 1.33; Your 90-Day Review, Today at 3 0.76; The Board 0.34 |
| Random baseline | Nervous breakdown 1.58; A short, friendly conversation 1.49; Your 90-Day Review, Today at 3 0.47; The Board 0.42 |

### Choice health

- Dominant choices (every temperament makes the same call): none.
- Choices no bot ever picked: none.
- Rarest choices (picks across every policy): `the-admin-terminal/type-kevins-password` 1, `the-spare-mustaches/return-the-mustaches` 3, `the-listening-room/switch-off-the-bears` 3, `tank-nine/call-in-kevins-favor` 14, `next-years-menu/order-off-the-boards-menu` 21.
<!-- /generated:balance -->
