# Conductor portfolio oversight roles

This is the repo-side operating contract for oversight work that ordinary Worker/Reviewer rotation does not reliably cover. It exists because a healthy task queue can still be pointed at the wrong portfolio: Kind Robots project rows can drift from Conductor, CONTROL/priority can drift from the latest human direction, and task bookkeeping can say "done" while the intended outcome is not actually true.

`PORTFOLIO-OVERSIGHT.md` is the deterministic sensor. Scheduled/rotating agents are the judgment layer.

## Startup overlay

After reading `AGENTS.md`, `CONTROL.md`, `project-overrides.yaml`, and `projects/priority.yaml`, read `PORTFOLIO-OVERSIGHT.md` before accepting an ordinary `select_role.py` Worker/Reviewer fallback.

Use these oversight roles when the report says they are needed, in this order:

1. **project-sync-auditor** — Kind Robots ↔ Conductor project parity has forward drift, reverse orphan(s), or could not be verified. Run `scripts/check_project_scaffold_drift.py` with the production-safe token path. Verify every Kind Robots `conductorSlug` resolves to one Conductor roadmap and every active Conductor project has the intended Kind Robots row. Where live Project settings are available, also verify the Conductor-owned coordination fields projected into Kind Robots still agree with `project-overrides.yaml` and `projects/priority.yaml`; presentation-only fields remain Kind Robots-owned per `SOURCE_OF_TRUTH.md`.
2. **roadmap-auditor** — `audit_roadmaps.py` reports deterministic errors. Repair unambiguous bookkeeping/state defects immediately. Never paper over a source-of-truth conflict by changing whichever side is easiest.
3. **roadmap-intent-auditor** — the semantic intent review is within one day of its deadline, or already due. An agent should complete the substantive review before the due date if available; never write an empty dated report merely to clear the sensor.

Broken/reviewable code already in flight can still outrank a soft semantic review when delaying it is clearly higher leverage, but deterministic project/roadmap drift should not sit indefinitely behind ordinary ready-task churn.

## Project-sync audit

The existing `scripts/check_project_scaffold_drift.py` is the minimum mechanical contract, not the whole review. For each active/continuous project:

- Confirm the Conductor slug, Kind Robots `conductorSlug`, and roadmap directory identify the same project. Look for typo twins, duplicate rows, retired rows still claiming an active slug, and new Kind Robots projects whose scaffold Todo was closed without a roadmap landing.
- Confirm Conductor-owned lifecycle and priority intent are represented consistently. `project-overrides.yaml` and `projects/priority.yaml` are authoritative for coordination; Kind Robots is a projection/read surface for those fields.
- Do not overwrite Kind Robots-owned presentation metadata (title, description, art, visibility/presentation choices) just to make a mechanical comparison pass.
- If the answer is unambiguous, fix the stale coordination record. If two live sources both plausibly encode different recent human decisions, preserve both and raise one concise `FOR SILAS:` choice rather than guessing.

## Roadmap-intent audit

Run this at least every **3 days**, and sooner after a substantial priority or direction change.

**Advance agent notice:** Every six hours, Conductor Oversight marks an
upcoming review one day before its three-day deadline. `scripts/select_role.py`
assigns `roadmap-intent-auditor` ahead of the ordinary ready-task backlog.
The agent is the only semantic judgment layer, using existing Conductor agent
sessions rather than billing a new model API. An upcoming/due notice alone
must not generate an email or claim the audit is done.

**Scheduled evidence preparation (no API spend):** GitHub Actions
`.github/workflows/semantic-intent-review.yml` runs daily. When the last
merged `INTENT-AUDIT-YYYY-MM-DD.md` is at least three Pacific days old,
`scripts/run_semantic_intent_review.py` creates the artifact
`semantic-intent-brief.md` plus a machine-readable attempt record with
`status: awaiting-agent`. The bounded context contains human direction,
lifecycle, priorities, lead roadmaps, structural warnings and recent commits.
This is **a brief, not a semantic review**: the workflow never makes an
LLM inference, writes a dated INTENT-AUDIT report, opens a report PR,
advances freshness, or spends credits. The six-hour oversight workflow
dispatches another packet only when due and no recent attempt exists.

**Actual reviewer:** On a `roadmap-intent-auditor` assignment, an existing
Conductor agent reads the original files listed below, evaluates intent with
evidence and, when warranted, authors a real
`projects/conductor/INTENT-AUDIT-YYYY-MM-DD.md`. Open a PR, run CI and
merge if safe. An agent unable to finish keeps the review due. The report
date only advances after that real report merges. Never copy the packet
verbatim as a completed report. Inspect actual PRs and shipped behavior
before treating a `done` task as a delivered result.

**Failure and notification boundary:** The email watchdog never emails for
review age alone or `awaiting-agent`. A genuine failed evidence-preparation
Actions job newer than the last successful report (or an explicitly verified
`INTENT-REVIEW-FAILURE.json`) may trigger an incident email. Model unavailability
and the retired GitHub Models failures are not active service incidents.
A successful packet-preparation job **does not** prove semantic review happened.
Project parity and deterministic roadmap errors keep separate escalation rules.

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
