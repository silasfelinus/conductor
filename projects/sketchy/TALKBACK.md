# TALKBACK.md — sketchy

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-07-20 | Reviewer (agent run) | sketchy/t-003 | implemented, self-closed done

**Decision:** wrote `projects/sketchy/CRITIQUE-RUBRIC.md`, closed t-003 `done`.

**Failure category:** none — clean first pass.

**What was good:**
- Read `PRODUCT-SPEC.md`, `SKILL-LADDER.md`, and `docs/ai-critique-apis.md` in full before
  writing anything — found all three already contain real content relevant to this task
  (the 5-dimension critique table + JSON shape, illustrative routing examples + friendly
  progression rules, and the API integration notes respectively) and built the new doc on
  top of them instead of re-deriving or duplicating.
- Turned the existing docs' illustrative/example-based coverage into implementable
  specifics: numeric 1-10 rubric anchors per dimension, a full 9-category ×
  5-dimension applicability matrix (SKILL-LADDER only gestured at "some dimensions get
  skipped"), a deterministic routing algorithm with an explicit tie-break order and a
  concrete friendly-progression override (so "never two corrections in a row" is an
  actual rule an implementation can check, not just a stated intent), and the literal
  system-prompt text to send to the critique API rather than a description of what it
  should contain.
- Called out explicit edge cases (blank submission, off-topic image, API content-policy
  refusal) with handling that doesn't need special-case code — e.g. a blank submission
  naturally floors every score and routes to a gentle re-upload prompt via the normal
  scoring path, no separate "is this blank" check needed.
- No `gate_human` — this elaborates an already-Silas-approved product spec (t-001) rather
  than setting new product direction, same precedent as t-002's `SKILL-LADDER.md` closing
  without a human gate.

**What to improve:** none this cycle.

**Kaizen task:** none filed — t-004 (token tiers) is next in the milestone and already
exists as a `ready` task; no new gap surfaced.

## 2026-07-21 | Worker (burst) | t-008 | done

**Decision:** filed and implemented in the same session (reversible, scoped —
session claude-conductor-burst-20260721T2017Z-sketchy-t008, conductor PR #994,
squash b4f5378).

**Context:** milestones m2/m3 had every spec task marked done but nothing had
ever built against those specs -- `apps/sketchy/lib/main.dart` was still the
untouched AppMaker boilerplate. Built the full core loop (calibration ->
assignment -> submission -> critique -> next assignment) on mock/local data:
30 assignments sourced from SKILL-LADDER.md's actual sample prompts, and a
critique/routing engine implementing CRITIQUE-RUBRIC.md §2's dimension table
and §3's weakest-skill routing (tie-break order, friendly-progression
override, all-8+ terminal case) rather than a stub. flutter_riverpod +
go_router, matching apps/conductor's conventions.

**What was good:**
- Grounded every piece of mock content in the project's own docs instead of
  inventing placeholder text -- assignment prompts/success-criteria are
  SKILL-LADDER.md's real samples, and the critique dimensions/anchors/routing
  table come straight from CRITIQUE-RUBRIC.md, not paraphrased loosely.
- Verified with the real toolchain, not just review: `flutter analyze
  --fatal-infos` (0 issues) and `flutter test` (15/15, 12 new unit tests
  covering every routing branch) both passed locally before pushing.
- Fixed a real correctness bug analyze caught: the router was being rebuilt
  from scratch on every `SketchyApp.build()` call (would have reset
  navigation state on any rebuild) -- moved it into a cached `Provider<GoRouter>`.
- Diagnosed a scary-looking CI failure correctly instead of assuming a
  regression: app-ci.yml ran every app in one job (not just sketchy), and the
  failure was a pre-existing hang in superkate-services-calculator's
  csv_export_widget_test.dart, unrelated to this diff. Read the full job log
  before merging rather than guessing; filed
  superkate-services-calculator/t-037 for the actual hang instead of touching
  an unrelated project's test inside this task.
- Fixed milestone-status drift found along the way (m1 done-but-marked-not-started,
  m2/m3 not-started despite this task moving them forward).

**What to improve:** none this cycle.

**Kaizen task:** none filed here — the one real gap found (the shared
apps/-in-one-job CI hang) is filed on superkate-services-calculator/t-037,
where the actionable fix actually lives.
