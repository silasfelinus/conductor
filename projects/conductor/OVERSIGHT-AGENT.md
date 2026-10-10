# Conductor portfolio oversight roles

This is the repo-side operating contract for oversight work that ordinary Worker/Reviewer rotation does not reliably cover. It exists because a healthy task queue can still be pointed at the wrong portfolio: Kind Robots project rows can drift from Conductor, CONTROL/priority can drift from the latest human direction, and task bookkeeping can say "done" while the intended outcome is not actually true.

`PORTFOLIO-OVERSIGHT.md` is the deterministic sensor. Scheduled/rotating agents are the judgment layer.

## Startup overlay

After reading `AGENTS.md`, `CONTROL.md`, `project-overrides.yaml`, and `projects/priority.yaml`, read `PORTFOLIO-OVERSIGHT.md` before accepting an ordinary `select_role.py` Worker/Reviewer fallback.

Use these oversight roles when the report says they are needed, in this order:

1. **project-sync-auditor** — Kind Robots ↔ Conductor project parity has forward drift, reverse orphan(s), or could not be verified. Run `scripts/check_project_scaffold_drift.py` with the production-safe token path. Verify every Kind Robots `conductorSlug` resolves to one Conductor roadmap and every active Conductor project has the intended Kind Robots row. Where live Project settings are available, also verify the Conductor-owned coordination fields projected into Kind Robots still agree with `project-overrides.yaml` and `projects/priority.yaml`; presentation-only fields remain Kind Robots-owned per `SOURCE_OF_TRUTH.md`.
2. **roadmap-auditor** — `audit_roadmaps.py` reports deterministic errors. Repair unambiguous bookkeeping/state defects immediately. Never paper over a source-of-truth conflict by changing whichever side is easiest.
3. **roadmap-intent-auditor** — the semantic intent review is within its one-day advance notice window, or already due. This is deliberately model/human-judgment work rather than another regex. Prioritize the actual review before its deadline and write a dated report only after completing it.

Broken/reviewable code already in flight can still outrank a soft semantic review when delaying it is clearly higher leverage, but deterministic project/roadmap drift should not sit indefinitely behind ordinary ready-task churn.

## Project-sync audit

The existing `scripts/check_project_scaffold_drift.py` is the minimum mechanical contract, not the whole review. For each active/continuous project:

- Confirm the Conductor slug, Kind Robots `conductorSlug`, and roadmap directory identify the same project. Look for typo twins, duplicate rows, retired rows still claiming an active slug, and new Kind Robots projects whose scaffold Todo was closed without a roadmap landing.
- Confirm Conductor-owned lifecycle and priority intent are represented consistently. `project-overrides.yaml` and `projects/priority.yaml` are authoritative for coordination; Kind Robots is a projection/read surface for those fields.
- Do not overwrite Kind Robots-owned presentation metadata (title, description, art, visibility/presentation choices) just to make a mechanical comparison pass.
- If the answer is unambiguous, fix the stale coordination record. If two live sources both plausibly encode different recent human decisions, preserve both and raise one concise `FOR SILAS:` choice rather than guessing.

## Roadmap-intent audit

Run this at least every **3 days**, and sooner after a substantial priority or direction change.

**Scheduling and dispatch are owned by Conductor, not a personal ChatGPT routine.**
The built-in `.github/workflows/conductor-oversight.yml` runs every six hours and
persists `PORTFOLIO-OVERSIGHT.md/json`. On day two of a three-day cycle the
sensor raises `semantic-review-upcoming`; when due it raises
`semantic-review-due`. `scripts/select_role.py` independently reads the
latest completed audit date and assigns `roadmap-intent-auditor` at either
point, ahead of ordinary work (but behind urgent PR/workflow repair).
Agents reading `AGENTS.md` must act on that role; a paused personal ChatGPT
agent cycle must not hide the assignment. The separate ChatGPT Semantic Review
task may also execute the work, but Conductor's notice/routing does not depend
on its enabled state.

The six-hour GitHub workflow is a deterministic dispatcher, **not** an LLM:
it cannot replace the actual judgment and source review. An available agent
must read the current sources, repair unambiguous drift and land a real dated
review. A due sensor alone never emails Silas; only an actual, recorded failed
review attempt warrants semantic escalation.

If a scheduled attempt fails before a valid audit is completed, write
`projects/conductor/INTENT-REVIEW-FAILURE.json` on a branch and open a PR with
this small record (do not silently suppress the original error):

```json
{
  "status": "failed",
  "attempted_at": "2026-10-13T15:00:00Z",
  "reason": "Specific failed operation and what was attempted"
}
```

Use the actual timestamp and error, never the example values. Merge a safe failure
record once verified so oversight can see it. The watchdog ignores absent,
malformed, future-dated, or superseded failure markers. A later successful dated
`INTENT-AUDIT-YYYY-MM-DD.md` supersedes the failed record without rewriting
history. If GitHub itself is unavailable, the reviewer may not be able to persist
the record; do not claim that absence proves the scheduled attempt succeeded.

Read, in order:

1. `CONTROL.md`.
2. `project-overrides.yaml` and `projects/priority.yaml`.
3. The roadmaps for the lead/high-priority active projects plus any project whose lifecycle or priority recently changed.
4. Relevant recent TALKBACK/commit history that records direct human steering or a correction to earlier assumptions.
5. `ROADMAP-AUDIT.md` for structural findings.

Then answer these questions with evidence rather than task-count numerology:

- Does the priority order still match the latest explicit direction? A dated newer human decision beats stale prose.
- Does each lead project's stated goal/milestones describe what we are actually trying to build now, including later corrections?
- Do `done` tasks correspond to outcomes that really landed, rather than PR/bookkeeping completion while the intended behavior remains missing?
- Are open tasks still relevant, or were they superseded by a later design choice, implementation, or project pivot?
- Does project lifecycle make sense? An `active` project with only human-gated leftovers, or a `finished` project whose stated goal is still unmet, deserves explicit review.
- Is progress being measured against the user's intention, not just against the roadmap's own possibly-stale text?

Repair clear stale bookkeeping in the same cycle. Split uncertain subjective/product-direction questions into narrow human gates; do not gate unrelated work.

### Intent audit report

A completed semantic review is recorded as:

`projects/conductor/INTENT-AUDIT-YYYY-MM-DD.md`

Keep it short and evidence-oriented:

- **Verified** — projects/settings/direction checked and what was confirmed.
- **Corrected** — unambiguous drift repaired in this cycle, with PR/task references.
- **Still questionable** — only genuine ambiguities or human decisions, with the exact choice needed.
- **Next review** — normally three days later.

Do **not** write a dated report merely to silence the due signal. If required sources were unavailable, leave the review overdue and record the availability problem instead.

## OpenAI scheduled-agent liveness

ChatGPT scheduler liveness is monitored natively in ChatGPT from the actual task state
(enabled/disabled plus last run time). Repository git history cannot authoritatively prove
that the ChatGPT scheduler fired because unattended scheduled runs may be prevented from
mutating GitHub by platform safety controls.

`scripts/build_portfolio_oversight.py` still records the historical
`openai-scheduled-` / `OPENAI-SCHEDULED-HEARTBEAT.json` signal as a **legacy diagnostic**
for debugging old runs. Claude scheduled commits do **not** satisfy that diagnostic. It
must not change the deterministic oversight status, route an `openai-schedule-medic`
role, or trigger email by itself.

## Deterministic sensor

Run locally/CI:

```bash
python scripts/build_portfolio_oversight.py
```

With `KR_API_TOKEN`, it includes Kind Robots project parity. `--fail-on-action` exits non-zero when deterministic drift, an overdue semantic intent review, or an unresolved Kind Robots parity check requires attention. The scheduled `Conductor Oversight` workflow persists `PORTFOLIO-OVERSIGHT.{md,json}` so connector-only agents can consume the result without needing direct production API access.
