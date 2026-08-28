# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-28T20:36:17Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **814**
- Outcomes: blocked: 16, cancelled: 1, done: 797
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 70 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 25 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 86 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 40 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 86 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 53 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 9 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 10 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 798 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 12 |
| transient | 11 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `transient` — 11 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-28 `conductor/t-135` — Every roadmap TASK status has cross-referencing tooling; MILESTONE status had none, and it drifted badly once checked -- 30 real mismatches across 20 active projects on the first run, not just the one case that prompted the task. A field that is only ever read (never audited against the data it summarizes) will drift silently no matter how cheap it would be to keep correct; the fix is a lightweight standalone advisory check wired into the session-startup sweep, not a one-time manual correction.
- 2026-08-28 `conductor/t-133` — A guard added to fix one lane's resubmission bug (Daily Dream's should_consume_after_submission, scoped via is_daily_dream_request) does not automatically protect a second lane that reaches the same underlying data through a different, unpatched import path (submit_mandarin_tutor_artjobs.py imports consume_art_requests directly, bypassing the consume_art_requests_to_media.py monkeypatch entirely). When a task says "widen guard X", check every caller reaches guard X's actual code path before assuming a change to X's own module is sufficient -- here the real fix had to live one layer lower, in a function both lanes genuinely share.
- 2026-08-28 `conductor/t-134` — A directory-listing-only share probe ("can I read one entry") is not a test for a partially-populated share -- it needs to check the specific files a render actually depends on, opened and read, not just scandir'd or stat'd (a stale SMB handle can satisfy a stat too). Generalized as KR_SHARE_REQUIRED_FILES, opt-in and unset by default so the existing directory-only behavior is unchanged unless configured.
- 2026-08-28 `cthulhuquarium/t-063` — A kaizen note's framing of "what's still open" (t-062's note named only t-058) was itself stale by the time this audit ran -- it undercounted by four tasks (t-019, t-021, t-022, t-041 were also open needs-human items). A planning/audit task should always re-derive the open set directly from live roadmap state (grep every task's own status) rather than trusting the prior task's kaizen prose about what remains, even when that prose sounds authoritative. Also caught a genuinely stale milestone `status` field (m3 sat at `not-started` despite 25/31 tasks done) -- milestone status isn't auto-derived from task counts anywhere in this repo's tooling, so it silently drifts unless an audit like this one checks it by hand.
- 2026-08-28 `cthulhuquarium/t-062` — Show-the-price-before-clicking (kind_robots#2182) had a nearby precedent in the same function (breedCost, added by t-055) that looked like a template but wasn't quite one: breedCost is a fixed per-species number nested under Monster, while sellPrice depends on the individual's own rolled stats and belongs as a top-level ClientStock field instead. Copying the precedent's TYPE SHAPE without checking whether its reasoning (per-species vs. per-individual) still applies would have produced a field that was technically present but structurally misleading. Checking why a precedent is shaped the way it is, not just that one exists, is what caught this before it shipped.
- 2026-08-28 `cthulhuquarium/t-061` — A "read-and-report audit" task (kind_robots#2181) turned out to have exactly one applicable shape once grepped precisely: of 17 files matching `meta:` under server/, only three (browse/catalog/leaderboard) return an actual API-response meta object -- everything else was ComfyUI workflow node `_meta`, a same-named but unrelated shape. Narrowing from a broad text match to the specific contract (an API route's response envelope, not any object literal keyed `meta`) before concluding "N call sites found" avoided both over-counting false positives and under-counting by assuming the grep result was already the answer. The two real hand-cast call sites (browse/leaderboard pages) already read the server's meta.total correctly -- the audit's fix was purely routing through performFetch's typed second generic instead of a manual ApiResponse<T> & {meta?: {...}} cast, so "no behavior change" was verifiable, not just claimed.
- 2026-08-28 `cthulhuquarium/t-060` — Extracting a shared useOneShotReveal() composable for revealedUnlock/Hatch/Breed (kind_robots#2180) kept every external ref/function name on the store unchanged, so no component needed touching -- confirming a presentation-only refactor is genuinely presentation-only by checking call-site signatures, not just behavior, avoids a should-have-been-a-no-op PR accidentally growing scope.
- 2026-08-28 `cthulhuquarium/t-059` — Reusing an existing formatting idiom (formatBestStats()/BEST_STAT_LABELS, t-031) instead of inventing a parallel one kept the diff to a single small helper (tankStockStatsLine()) that reshapes TankStock's stat<Name> fields into the same BestiaryStatBlock shape the Ichthyonomicon already consumes. Worth flagging as its own kaizen (t-062) rather than scope-creeping into this task: making an individual's rolled stats visible for the first time immediately raises the follow-on question a player will actually ask -- "what would this sell for?" -- which the Sell button still doesn't answer despite the price already varying per individual (sellPrice() in aquariumEconomy.ts). Noticing a UI change makes a previously-invisible economic question visible is a useful generic signal for kaizen filing, distinct from noticing a code-shape duplication.
- 2026-08-28 `cthulhuquarium/t-057` — A task that reads as UI-only ("show a countdown") can be blocked on a small, shared infrastructure gap: performFetch() (stores/utils.ts) silently dropped every response's `meta` object, and at least 17 server routes already return one. Worth checking whether a "just read this field" task's data is actually reachable before assuming the store layer already exposes it -- the fix here (an optional second generic on ApiResponse<T, M>, purely additive/backward-compatible) was small, but skipping that check would have meant reaching for a server-side workaround (a second field on `data`, or a new endpoint) that the task's own note explicitly said wasn't needed.
- 2026-08-28 `cthulhuquarium/t-056` — A repeated-shape kaizen (three near-identical one-shot-signal refs) is worth pausing on before extracting: the task named three call sites (bestiaryJustCompleted, milestoneToastQueue, finaleJustTriggered), but a fourth near-identical trio (revealedUnlock/revealedHatch/revealedBreed, a typed-payload variant of the same shape) was sitting right next to it in the same file. Scoping the extraction to exactly what the task named (rather than also folding in the sibling pattern) kept the diff small and reviewable, but the sibling was worth filing as its own immediate kaizen (t-060) rather than a speculative "if a fourth shows up" -- it already had three instances, the same threshold that triggered this task in the first place.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-28T20:36:17Z_
