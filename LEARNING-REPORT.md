# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-14T09:53:26Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **952**
- Outcomes: blocked: 16, cancelled: 1, done: 935
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 29 | 100% |
| conductor | 101 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 135 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 57 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 83 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 20 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 21 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 935 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 21 |
| transient | 15 |
| actionable | 14 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 21 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 14 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-14 `conductor/t-156` — recheck_render_queue.py's classify() checked only queueDepth.PENDING before check_render_box.py's own render_throughput_verdict() was ever consulted, so it wrote 'healthy' to RENDER-BACKLOG.md for a box that was actually down (every job failing fast, never leaving anything stuck PENDING) in the exact same live session where check_render_box.py correctly reported DOWN. Two scripts reading the same stats endpoint with different classifiers will disagree eventually -- when one is already the documented single source of truth for a judgment (here, 'is the render box actually rendering'), the other should delegate to it rather than reimplement a weaker version. Caught this live because the two scripts were run back-to-back in the same session on coloring-book/t-022; would otherwise have silently written a wrong ledger entry.
- 2026-09-14 `kind-robots/t-062` — This sandbox's local verification habit of running vue-tsc/eslint/prettier/test:layout-contract missed a fourth check bundled into the same CI job: test:kr-class-coverage, which failed on the first push over kr-text-sm -- a plausible-looking primitive name (the sm-size family is all modified: kr-text-black-sm, kr-text-dim-sm, kr-text-bold-sm, kr-text-faded-sm, but no bare kr-text-sm) that doesn't actually exist in assets/css/tailwind.css. Read a CI workflow file's full step list (.github/workflows/<job>.yml) before claiming local verification covers a job, rather than assuming the one script named in the job title is the whole job -- layout-contract.yml alone runs four separate npm scripts plus two fixture/selftest scripts. Also: a Grant-sharing pitch (kind-robots/t-044/t-050/t-062) that adds canView()/existsActiveGrant() to two view routes plus a minimal Share/Shared-with-me UI has no existing owner-facing edit surface to embed the share widget into for either Project or Resource -- shipped as two standalone /projects/[id]/share and /resources/[id]/share pages instead of wiring into the admin-only conductor project-detail panel, which is gated on isAdmin and would never reach the non-admin owners Grant sharing exists for.
- 2026-09-14 `interface-vision/t-133` — Real PR traffic touching *.sh files was too sparse to answer the task's own question from CI history alone (only one recent PR had an actual .sh diff, and it produced zero shellcheck findings) -- ran shellcheck directly against the full current *.sh corpus (12 scripts) as a stand-in evidence base instead of waiting indefinitely for more PR traffic. Only SC2086 had multiple true-positive hits with zero false positives; the other codes seen (SC2207/SC2010/SC2209/SC1003) each had a single occurrence and one (SC2209) was a confirmed false positive on this repo's TOOL=name assignment style, confirming the task's own caution against flipping the whole pass to blocking at once.
- 2026-09-13 `kind-robots/t-096` — The task's original filing (grep of 'return errorHandler(error)') undercounted the real call-site pattern -- most of the codebase actually writes 'const handled = errorHandler(error)' then a separate status line, so the literal grep matched only 19 of 470 real call sites and the filing concluded almost nothing was fixed (8/432) when in fact 429/470 already were. Re-derive the live count with a broader pattern (any errorHandler( call, cross-referenced against status-setting patterns) before trusting a stale filing's scope estimate, especially for a task that's sat open a couple of days -- the codebase moves. Also found and fixed a second, coupled bug while auditing: several routes called errorHandler() with a wrapper object ({error, context, statusCode}) instead of the actual Error, which errorHandler() doesn't recognize, silently discarding the intended status and message even in the JSON body -- worth checking call-site *shape*, not just call-site *presence*, when fixing a suspected systemic misuse.
- 2026-09-13 `coloring-book/t-043` — t-039's second finding (quality guard blind to noise on the color variant) sat unaddressed in a task note for two days because it was independent of the hard relay-access gate blocking the rest of that task -- worth scanning needs-human/soft_gate notes for an already-specified, self-contained fix like this rather than treating the whole task as blocked. The fix itself needed no new dependency: a spatial-autocorrelation ratio computed from pixels PIL already samples, verified against real random noise (hf_ratio 0.98) and real structured images (gradient 0.0001, blurred texture 0.047) before picking the threshold, not just the selftest's synthetic blocks.
- 2026-09-13 `conductor/t-151` — Built the advisory periodic-sweep guard (option (b)) the filing task itself proposed, mirroring check_milestone_status_drift.py's structure exactly (same overrides-filtering, --json/--include-inactive flags, exit-1-on-findings-only contract) rather than inventing a new shape. Running it against the live repo immediately validated the fix: both findings (model-builder/t-029, storybook/t-010) were already known from the filing session's ad hoc sweep, and interface-vision/t-104 -- the task whose 395KB note prompted this -- no longer appears, confirming its T104-HISTORY.md archive trim is still holding months later.
- 2026-09-13 `coloring-book/t-042` — Kaizen from t-041: load_stats() now warns once (module-level flag, printed to stderr) the first time it hits Pillow's ImportError in a process, instead of only ever returning None. Verified against a real missing-Pillow sandbox rather than a mock. A tiny, fully-specified kaizen note from the prior session's close-out needed no design judgement -- just implement, verify against the real failure condition it names, and close.
- 2026-09-13 `coloring-book/t-041` — Kaizen from t-040: grepping the rest of the coloring-book pipeline for the same bare 'from PIL import Image' pattern found two more genuine hits (consume_coloring_book_color_art.py, manage_coloring_book_cover.py) and two false leads that already degrade gracefully (art_quality.py's load_stats returns None; consume_art_queue_core.py's save_result falls back to PNG with its own actionable message). A kaizen framed as 'grep for the same pattern elsewhere' is worth doing literally and completely in one pass rather than fixing only the first hit found -- distinguishing already-graceful call sites from genuinely bare ones is the actual work, not the grep itself.
- 2026-09-13 `coloring-book/t-040` — A recurring TALKBACK-flagged papercut (bare 'PIL unavailable' error on a non-persistent sandbox Pillow install, rediscovered fix-and-forgotten across three separate sessions on 2026-08-11 and 2026-09-13) had its actual fix fully specified in the task note before this session ever claimed it -- the work was pure implementation, no design decision needed. When a TALKBACK entry proposes the exact same concrete fix three times running, the next session to touch that area should file the roadmap task itself rather than re-suggesting it a fourth time; this task existed only because a prior session finally did that.
- 2026-09-13 `kindrobots-unraid/t-019` — An alarming-looking MCE decoded to a benign one. Status bea0000000000108 sets PCC (processor context corrupt), which reads as the urgent case, but TSC 0 is the decisive field: a real machine-check exception captures a timestamp, so zero means machine_check_poll() read stale bank status -- and the boot-time poll of all banks runs without MCP_TIMESTAMP, so it always logs TSC 0. EDAC initialising 45s later confirmed the line landed ~1 min into a boot. Decode the status bits before escalating on the headline; also decode IPID (HWID 0xB0 / McaType 0x5 = SMCA_EX) rather than assuming a bank number means memory. The correlation check the task was filed to run came back NEGATIVE and was still worth the round trip: dmesg covered the whole current boot including t-018's window with no MCE, which is a clean negative on hardware for that incident, and the same output exposed three real blind spots (RAM-only syslog, non-ECC memory so no EDAC detector at all, 4x16GB DDR4-3600 above JEDEC on a Matisse IMC) now tracked at t-020. A diagnostic that disproves your hypothesis but hands you the actual lead is a success, not a wasted pass.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-14T09:53:26Z_
