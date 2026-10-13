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

## Window 9 shift (t-016)

The Records window shift adds four certain stamps before the review, so the first run with it on the board
moved Records for everyone:

| Records Successors lost per run | Complier | Rebel | Coward | Saint | Schemer |
|---|---:|---:|---:|---:|---:|
| Before the window | 1.50 | 0.41 | 0.16 | 0.86 | 0.37 |
| First draft of the window | 2.08 | 0.97 | 0.26 | 1.39 | 1.27 |
| Shipped | 1.86 | 0.70 | 0.21 | 1.16 | 0.54 |

Two changes got it there:

- **The first draft broke two thresholds.** Every by-the-book stamp cost composure, so the Complier lost
  more than 2 Successors per run at Records. Approving your own Successor spent one outright, which put the
  Schemer at 53.5% eliminated.
- **Denying the courier and the Successor now costs a Form for the paperwork.** Approving the Successor no
  longer spends him: it buys 2 composure and costs 2 Suspicion, because he is very productive in your name
  and PAL has questions for both of you.

## Open design calls (for t-020, Silas's fun verdict)

- **The Coward almost never dies, but it pays for that.**
  - It survives 99.9% of runs. It still loses about 2.7 Successors per run, and it never sees any of the 7 payoff
    endings.
  - That reads as *Papers, Please*: obedience keeps you alive and keeps you small.
  - If it should also be deadly, the lever is the no-roll "safe" choices that trade composure for clearance.
- **Clearance hits its cap all the time.** The Complier and Rebel bump into clearance 5 about five times a
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
| The Complier | 75.4% | 24.6% | 5.20 | 3 of 10 |
| The Rebel | 62.0% | 38.0% | 5.53 | 3 of 10 |
| The Coward | 100.0% | 0.1% | 2.68 | 3 of 10 |
| The Saint | 75.8% | 24.3% | 5.36 | 9 of 10 |
| The Schemer | 55.5% | 44.5% | 5.80 | 8 of 10 |
| Random baseline | 86.8% | 13.3% | 4.72 | 10 of 10 |

### Successors lost per run, by department

| Policy | Orientation | Records & Forms | Toy Division | Wellness & Testing | Sub-Level Zero |
|---|---:|---:|---:|---:|---:|
| The Complier | 0.72 | 1.86 | 0.95 | 0.80 | 0.89 |
| The Rebel | 1.10 | 0.70 | 1.64 | 1.10 | 0.99 |
| The Coward | 0.51 | 0.21 | 0.48 | 0.55 | 0.93 |
| The Saint | 0.45 | 1.16 | 1.47 | 1.08 | 1.19 |
| The Schemer | 1.18 | 0.54 | 1.69 | 1.03 | 1.36 |
| Random baseline | 0.77 | 0.67 | 1.16 | 0.98 | 1.14 |

### Endings (share of runs)

| Ending | The Complier | The Rebel | The Coward | The Saint | The Schemer | Random baseline |
|---|---:|---:|---:|---:|---:|---:|
| Employee of the Month | 36.1% | · | 49.5% | 0.8% | 0.3% | 21.8% |
| Promoted to Management | · | 58.1% | · | · | 13.7% | 22.1% |
| Escape Through the Ducts | · | · | · | 0.8% | 14.2% | 1.6% |
| Roach Union General Strike | · | · | · | 22.4% | · | 2.0% |
| Society Coup | · | · | · | 3.1% | · | 1.1% |
| Whistleblower | · | · | · | 5.5% | 2.1% | 2.5% |
| Early Retirement | 39.3% | · | 50.4% | 37.9% | 21.9% | 34.3% |
| The Kind Rewrite | · | · | · | 1.9% | 1.6% | 0.3% |
| Position Eliminated | 24.6% | 28.3% | 0.1% | 21.8% | 32.6% | 12.3% |
| The Department of Posthumous Affairs | · | 9.8% | · | 2.5% | 11.9% | 0.9% |

### Meter limits hit per run

| Policy | clearance:max | composure:max | composure:min | forms:min | successors:min | suspicion:max | suspicion:min |
|---|---:|---:|---:|---:|---:|---:|---:|
| The Complier | 5.67 | 0.01 | 3.24 | 1.96 | 0.17 | 0.09 | 4.20 |
| The Rebel | 4.95 | 0.14 | 0.61 | 0.35 | 0.04 | 3.94 | 0.89 |
| The Coward | 4.83 | 0.16 | 0.97 | 0.63 | 0.00 | 0.64 | 2.99 |
| The Saint | 1.24 | 0.38 | 0.43 | 1.02 | 0.08 | 3.72 | 0.42 |
| The Schemer | 2.26 | 0.29 | 1.11 | 0.53 | 0.13 | 3.42 | 1.00 |
| Random baseline | 4.54 | 0.08 | 1.44 | 0.78 | 0.07 | 1.79 | 1.50 |

### Top causes of termination

| Policy | Causes (per run) |
|---|---:|
| The Complier | Nervous breakdown 3.16; The Form That Requires Itself 0.84; The Board 0.43; The Guard Who Is Also You 0.24 |
| The Rebel | A short, friendly conversation 3.59; Your 90-Day Review, Today at 3 0.89; Nervous breakdown 0.59; The Successor Waiting Room 0.19 |
| The Coward | Nervous breakdown 0.97; A short, friendly conversation 0.64; The Board 0.50; Your 90-Day Review, Today at 3 0.27 |
| The Saint | A short, friendly conversation 3.56; The Board 0.44; Nervous breakdown 0.39; The Drop Test 0.32 |
| The Schemer | A short, friendly conversation 3.13; Nervous breakdown 0.98; Your 90-Day Review, Today at 3 0.76; The Board 0.32 |
| Random baseline | A short, friendly conversation 1.73; Nervous breakdown 1.41; Your 90-Day Review, Today at 3 0.47; The Board 0.39 |

### Choice health

- Dominant choices (every temperament makes the same call): none.
- Choices no bot ever picked: none.
- Rarest choices (picks across every policy): `the-admin-terminal/type-kevins-password` 1, `the-listening-room/switch-off-the-bears` 1, `tank-nine/call-in-kevins-favor` 5, `the-spare-mustaches/return-the-mustaches` 6, `next-years-menu/order-off-the-boards-menu` 14.
<!-- /generated:balance -->
