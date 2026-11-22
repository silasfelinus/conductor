# CI art-ledger loader parity: measured split (2026-11-22 UTC)

Conductor `comet-city-academy/t-043`, follow-up to the loader-parity
scheduling change merged in [PR #7695](https://github.com/silasfelinus/conductor/pull/7695)
on 2026-11-20 22:46:42 UTC. Measurements below are **pytest wall-clock
durations from the actual completed GitHub Actions job logs**, not estimates
from runner startup or an assumed improvement.

| Run | UTC start of workflow | Pytest summary | Pytest duration |
| --- | --- | --- | ---: |
| [Pre-split Worker PR CI 44810467441](https://github.com/silasfelinus/conductor/actions/runs/44810467441), Python test suite job 136545402582 | 2026-11-20 20:20:31 | 4,859 passed; 8 skipped | **219.02 s** |
| [First post-merge Worker PR CI 44831965912](https://github.com/silasfelinus/conductor/actions/runs/44831965912), Python test suite job 136618858402 | 2026-11-20 22:48:40 | 4,859 passed; 8 skipped; 1 deselected (`art_parity`) | **279.10 s** |
| [First completed daily loader parity 44948778718](https://github.com/silasfelinus/conductor/actions/runs/44948778718), job 136981871592 | 2026-11-21 20:55:05 | 1 passed; 7 deselected | **19.03 s** |

**Observed difference:** the first post-merge main-suite run was **60.08
seconds slower (+27.4%)**, not faster. The change removed the exhaustive
`art_parity` item from every PR (1 deselected), but it did **not** make the
first sampled end-to-end Python suite faster. This single before/after
comparison is not a controlled benchmark. Do not attribute the 60-second
regression to loader choice alone.

Post-merge `--durations=10` pointed to unrelated expensive calls:
`test_media_wrapper_resolves_names_before_submitting` at **62.00 s**,
`test_repo_ledgers_have_no_new_templated_cells` at **38.67 s**, and
`test_repo_ledgers_unsubmitted_cells_pass_negation_rules` at **37.07 s**.
Their combined **137.74 s** dominates this measurement. A later performance
task should investigate their I/O and repeated YAML parsing rather than
declare the parity split a measured speedup.

## Did the daily parity check actually execute?

**Yes.** The scheduled workflow installed PyYAML 6.0.4's CPython 3.12
manylinux wheel and ran:

```sh
pytest -q -m art_parity tests/test_sweep_art_ledgers.py --durations=3
```

GitHub Actions output names the real test
`tests/test_sweep_art_ledgers.py::test_all_opted_in_art_ledgers_have_identical_safe_loader_data`,
reports **18.95 s call duration**, and finishes **1 passed, 7 deselected
in 19.03 s**. It did not skip the parity test. In that test, both
`yaml.SafeLoader` and `yaml.CSafeLoader` parse every opted-in art ledger
and their resulting data must compare equal.

## Guard against silent future skips

Before this follow-up the marked test used `pytest.skip` when
`CSafeLoader` was missing. A scheduled workflow could therefore turn
green despite checking **zero** comparisons. This increment makes the
marked test **fail** instead, with an explicit missing-C-loader error.
A separate fast, unmarked pytest test deliberately removes `CSafeLoader`
and asserts the scheduled test fails. The daily workflow remains a
scheduled/on-demand lane; the exhaustive comparison is still excluded
from ordinary PR CI.

Next interpretation: the split is correct in coverage and scheduling, but
the speed goal is **not demonstrated** by the first after-run. Investigate
the 62/39/37-second calls separately if reducing PR latency is the aim.
