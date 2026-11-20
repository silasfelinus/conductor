# Emperor of Dust: second-pass trace coverage audit (2026-11-20 PT)

**Status:** Evidence inventory, not an independent five-act editorial verdict or a human playtest. This is a partial result for Conductor `emperor-of-dust/t-044`; keep master Kind Robots issue [#4142](https://github.com/silasfelinus/kind_robots/issues/4142) open.

## Reproducible source

- Kind Robots exact tested commit: `1b54e7e6020b858c922e3ca1e9f17a0504015837`.
- CI run: [44728766903](https://github.com/silasfelinus/kind_robots/actions/runs/44728766903), artifact `emperor-editorial-screening` ID `14625771393` (30-day retention).
- Read `second-pass-manifest.json` plus all sixteen `second-pass-*.trace.json` files within that artifact. Recomputed counts directly from the trace event arrays, not from intended design behavior.
- Method: eight deterministic policies (greedy, random, spurn-all, marshal, reckless, idle, Freeholds patron, Mire Mothers patron), two seeds (17 and 41), fifty played days each and 51 recorded dawns. No injected ending flags. All results are **model simulations**, not human-player observations.

## What the first matrix actually exercised

| Measure | Observed in these sixteen traces |
| --- | ---: |
| Complete simulated campaigns | 16 |
| Dawn snapshots, including Day 51 | 816 |
| Court choices with eligibility/effects | 2,202 |
| Barracks replies | 760 |
| Quest results (all tiers) | 1,283 |
| Maximum recorded loan balance | 0 |
| Maximum memorial/death count | 0 |
| Distinct earned ending families | 4 of 8 |

The four observed endings were `open-roads` (10 runs), `iron-peace` (2), `long-night` (2) and `witchwater-throne` (2). **Not observed here:** `bell-restored`, `crows-bargain`, `hundred-candles`, `tunnels-and-councils`. Their absence in this sample does not mean they are unreachable. The separate seeded balance suite tests reachability over a broader policy/seed matrix.

### Coverage by act

| Days | Court choices | Barracks replies | Quest results |
| --- | ---: | ---: | ---: |
| Act I, Days 1–10 | 770 | 125 | 280 |
| Act II, Days 11–20 | 340 | 173 | 260 |
| Act III, Days 21–30 | 259 | 166 | 249 |
| Act IV, Days 31–40 | 448 | 160 | 252 |
| Act V, Days 41–50 | 385 | 136 | 242 |

These are event **counts**, not qualitative scores. Repeated visits to the same scene count separately. All sixteen scripts record save-roundtrip evidence at Days 1, 11, 21, 31, 41 and 51, plus the Day 31 rewind at the end; those are technical recovery tests, not browser QA.

## Why this is not yet acceptance

1. The sixteen-persona selection misses half the endings, and zero run deaths/loans leave casualty, memorial override, borrowing and scarcity dialogue unevaluated by this specific sample.
2. High action counts do not establish that the writing is distinctive, readable, balanced or causally remembered. The [scored second-pass protocol](../2026-11-19/SECOND-PASS-SCORING-PROTOCOL.md) requires per-act reviewer records citing both strengths and weaknesses from complete text and later callbacks. One provisional marshal/17 score record is not full coverage.
3. A synthetic engine trace cannot validate actual painted ArtImage bytes, scene attachment, graphical density, mobile tap targets, or 390/768/820/1440 browser screenshots.

## Next acceptance instruments

- Kind Robots PR **#5432** adds a supplemental, legally played eight-ending witness suite. Its Emperor Dispatch workflow on exact head `7f43eac2243726afdd7ab8eca6ae3fc5db17c0fb` passed (run [44737362182](https://github.com/silasfelinus/kind_robots/actions/runs/44737362182)); I downloaded artifact ID `14630375105`, inspected `second-pass-ending-witnesses-manifest.json`, and parsed **all eight** matching 51-dawn trace JSON files. The eight transcript files and all six save checkpoints per run are present. This verification is narrower than full PR merge approval: the separate repository-wide Contract Tests workflow still needs to finish before merging.
- The supplemental witness campaigns cover all **8/8 endings** without injected flags and add 408 dawns, five follower deaths across four campaigns, and one campaign with a loan. This demonstrates the memorial and loan mechanics can occur, not that their difficulty or prose is accepted. The sampled witness policies/seeds are: `bell-restored` random/6, `crows-bargain` random/7, `hundred-candles` spurn-all/7, `iron-peace` random/8, `long-night` greedy/4, `open-roads` greedy/1, `tunnels-and-councils` patron:moles/1, and `witchwater-throne` patron:mire-mothers/1.
- Score the missing reviewer personas under the existing protocol using their actual day-by-day traces. Include more than one seed, and explain N/A rather than inventing scores.
- Add observed resource-stress/death, loan and memorial scenarios with explicit chance/dispatch routes, save continuity and failure evidence.
- Keep real image review/export and real-browser visual acceptance separate gates. `ArtJob DONE`, a YAML ledger or generated test traces are not delivered art.

**Verdict:** The first matrix is substantial **mechanical traversal evidence**, but it is not the finite t-044 closeout, independent qualitative acceptance, or the project playtest handoff.
