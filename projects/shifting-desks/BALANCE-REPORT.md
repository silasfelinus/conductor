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
| The Complier | 78.4% | 21.6% | 5.09 | 3 of 10 |
| The Rebel | 52.9% | 47.1% | 5.68 | 3 of 10 |
| The Coward | 100.0% | 0.0% | 2.00 | 2 of 10 |
| The Saint | 64.8% | 35.1% | 5.69 | 9 of 10 |
| The Schemer | 56.0% | 44.0% | 5.88 | 8 of 10 |
| Random baseline | 83.5% | 16.5% | 4.85 | 10 of 10 |

### Successors lost per run, by department

| Policy | Orientation | Records & Forms | Toy Division | Wellness & Testing | Sub-Level Zero |
|---|---:|---:|---:|---:|---:|
| The Complier | 0.63 | 1.83 | 1.01 | 0.61 | 1.01 |
| The Rebel | 1.09 | 0.68 | 1.98 | 1.13 | 0.79 |
| The Coward | 0.41 | 0.29 | 0.46 | 0.28 | 0.56 |
| The Saint | 0.32 | 1.33 | 1.52 | 1.22 | 1.30 |
| The Schemer | 1.32 | 0.63 | 1.80 | 0.95 | 1.18 |
| Random baseline | 0.77 | 0.68 | 1.30 | 1.00 | 1.10 |

### Endings (share of runs)

| Ending | The Complier | The Rebel | The Coward | The Saint | The Schemer | Random baseline |
|---|---:|---:|---:|---:|---:|---:|
| Employee of the Month | 42.3% | · | 99.7% | 1.4% | 4.2% | 28.8% |
| Promoted to Management | · | 46.9% | · | · | 15.7% | 18.9% |
| Escape Through the Ducts | · | · | · | 0.5% | 5.8% | 0.6% |
| Roach Union General Strike | · | · | · | 8.2% | · | 0.9% |
| Society Coup | · | · | · | 2.3% | · | 0.3% |
| Whistleblower | · | · | · | 2.6% | 1.6% | 1.0% |
| Early Retirement | 36.1% | · | 0.3% | 47.2% | 26.7% | 31.8% |
| The Kind Rewrite | · | · | · | 0.7% | 0.7% | 0.1% |
| Position Eliminated | 21.6% | 41.8% | · | 33.6% | 39.6% | 15.8% |
| The Department of Posthumous Affairs | · | 5.3% | · | 1.5% | 4.5% | 0.7% |

### Meter limits hit per run

| Policy | clearance:max | clearance:min | composure:max | composure:min | forms:min | successors:min | suspicion:max | suspicion:min |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| The Complier | 7.01 | 0.00 | 0.03 | 3.17 | 7.06 | 0.16 | 0.11 | 5.04 |
| The Rebel | 2.77 | 0.00 | 0.26 | 0.44 | 1.18 | 0.04 | 4.33 | 0.88 |
| The Coward | 5.41 | 0.00 | 0.36 | 1.07 | 6.25 | 0.00 | 0.49 | 3.00 |
| The Saint | 0.61 | 0.07 | 0.80 | 0.32 | 3.31 | 0.17 | 4.01 | 0.42 |
| The Schemer | 1.86 | 0.01 | 0.28 | 0.83 | 2.43 | 0.16 | 3.61 | 1.03 |
| Random baseline | 4.61 | 0.00 | 0.12 | 1.08 | 2.97 | 0.08 | 2.26 | 1.68 |

### Top causes of termination

| Policy | Causes (per run) |
|---|---:|
| The Complier | Nervous breakdown 3.10; The Form That Requires Itself 0.80; The Board 0.41; The Guard Who Is Also You 0.20 |
| The Rebel | A short, friendly conversation 3.91; Your 90-Day Review, Today at 3 0.86; Nervous breakdown 0.40; The Successor Waiting Room 0.20 |
| The Coward | Nervous breakdown 1.07; A short, friendly conversation 0.49; Your 90-Day Review, Today at 3 0.20; The Guard Who Is Also You 0.18 |
| The Saint | A short, friendly conversation 3.81; The Board 0.61; Nervous breakdown 0.30; The Jam in Tube 14 0.20 |
| The Schemer | A short, friendly conversation 3.35; Your 90-Day Review, Today at 3 0.81; Nervous breakdown 0.76; The Board 0.39 |
| Random baseline | A short, friendly conversation 2.17; Nervous breakdown 1.07; Your 90-Day Review, Today at 3 0.46; The Board 0.38 |

### Choice health

- Dominant choices (every temperament makes the same call): none.
- Choices no bot ever picked: `which-office-supply-are-you/return-her-envelope`, `the-suggestion-tube/post-the-help`, `the-two-quiet-rooms/tap-the-squeak-rhythm`, `the-spare-mustaches/return-the-mustaches`, `the-admin-terminal/type-kevins-password`, `the-listening-room/switch-off-the-bears`, `ticket-number-two/find-your-help`.
- Rarest choices (picks across every policy): `the-pre-exit-interview/return-halvorsens-envelope` 1, `gus-measures-the-glass/cosign-it` 1, `random-loyalty-screening/hand-over-the-dead-badge` 1, `pip-at-window-10/take-over-window-10` 1, `dales-testimony/remind-dale-of-the-forgery` 3.
<!-- /generated:balance -->
