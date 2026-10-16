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
| The Complier | 75.5% | 24.4% | 5.13 | 3 of 10 |
| The Rebel | 50.6% | 49.4% | 5.77 | 3 of 10 |
| The Coward | 100.0% | 0.0% | 2.01 | 2 of 10 |
| The Saint | 62.5% | 37.5% | 5.69 | 9 of 10 |
| The Schemer | 50.8% | 49.3% | 5.89 | 8 of 10 |
| Random baseline | 78.4% | 21.6% | 5.04 | 10 of 10 |

### Successors lost per run, by department

| Policy | Orientation | Records & Forms | Toy Division | Wellness & Testing | Sub-Level Zero |
|---|---:|---:|---:|---:|---:|
| The Complier | 0.72 | 1.86 | 0.97 | 0.62 | 0.97 |
| The Rebel | 1.10 | 0.70 | 1.87 | 1.20 | 0.90 |
| The Coward | 0.51 | 0.21 | 0.48 | 0.30 | 0.51 |
| The Saint | 0.45 | 1.16 | 1.64 | 1.21 | 1.24 |
| The Schemer | 1.18 | 0.54 | 1.87 | 0.96 | 1.34 |
| Random baseline | 0.77 | 0.67 | 1.35 | 1.04 | 1.21 |

### Endings (share of runs)

| Ending | The Complier | The Rebel | The Coward | The Saint | The Schemer | Random baseline |
|---|---:|---:|---:|---:|---:|---:|
| Employee of the Month | 39.0% | · | 96.6% | 0.8% | 1.9% | 22.9% |
| Promoted to Management | · | 47.2% | · | · | 11.8% | 19.6% |
| Escape Through the Ducts | · | · | · | 1.4% | 12.8% | 1.4% |
| Roach Union General Strike | · | · | · | 18.9% | · | 2.0% |
| Society Coup | · | · | · | 2.8% | · | 0.9% |
| Whistleblower | · | · | · | 4.2% | 2.1% | 1.9% |
| Early Retirement | 36.6% | · | 3.4% | 29.6% | 18.3% | 28.8% |
| The Kind Rewrite | · | · | · | 1.9% | 1.3% | 0.1% |
| Position Eliminated | 24.4% | 36.5% | · | 33.3% | 35.6% | 19.9% |
| The Department of Posthumous Affairs | · | 12.8% | · | 4.3% | 13.6% | 1.8% |

### Meter limits hit per run

| Policy | clearance:max | clearance:min | composure:max | composure:min | forms:min | successors:min | suspicion:max | suspicion:min |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| The Complier | 6.55 | 0.00 | 0.05 | 3.12 | 7.44 | 0.17 | 0.17 | 4.29 |
| The Rebel | 4.51 | 0.00 | 0.15 | 0.46 | 0.28 | 0.02 | 4.52 | 0.94 |
| The Coward | 4.87 | 0.00 | 0.73 | 0.73 | 6.09 | 0.00 | 0.69 | 2.97 |
| The Saint | 1.11 | 0.05 | 1.16 | 0.20 | 3.24 | 0.14 | 4.36 | 0.40 |
| The Schemer | 2.00 | 0.02 | 0.31 | 1.06 | 1.38 | 0.15 | 3.57 | 1.10 |
| Random baseline | 4.80 | 0.01 | 0.19 | 1.04 | 2.65 | 0.10 | 2.59 | 1.50 |

### Top causes of termination

| Policy | Causes (per run) |
|---|---:|
| The Complier | Nervous breakdown 3.04; The Form That Requires Itself 0.84; The Board 0.40; The Guard Who Is Also You 0.24 |
| The Rebel | A short, friendly conversation 4.05; Your 90-Day Review, Today at 3 0.89; Nervous breakdown 0.44; The Successor Waiting Room 0.17 |
| The Coward | Nervous breakdown 0.73; A short, friendly conversation 0.69; Your 90-Day Review, Today at 3 0.27; The Guard Who Is Also You 0.23 |
| The Saint | A short, friendly conversation 4.12; The Board 0.41; The Drop Test 0.33; Nervous breakdown 0.19 |
| The Schemer | A short, friendly conversation 3.29; Nervous breakdown 0.95; Your 90-Day Review, Today at 3 0.76; The Board 0.30 |
| Random baseline | A short, friendly conversation 2.48; Nervous breakdown 1.01; Your 90-Day Review, Today at 3 0.47; The Board 0.38 |

### Choice health

- Dominant choices (every temperament makes the same call): none.
- Choices no bot ever picked: `the-admin-terminal/type-kevins-password`, `the-listening-room/switch-off-the-bears`.
- Rarest choices (picks across every policy): `the-spare-mustaches/return-the-mustaches` 2, `tank-nine/call-in-kevins-favor` 3, `next-years-menu/order-off-the-boards-menu` 23, `the-union-archive/ask-for-your-file` 26, `a-capsule-from-yourself/hand-it-to-pip` 28.
<!-- /generated:balance -->
