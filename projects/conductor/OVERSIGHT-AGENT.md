# Conductor portfolio oversight roles

This is the repo-side operating contract for the oversight work that ordinary Worker/Reviewer rotation does not reliably cover. It exists because a healthy task queue can still be pointed at the wrong portfolio: Kind Robots project rows can drift from Conductor, CONTROL/priority can drift from the latest human direction, and task bookkeeping can say "done" while the intended outcome is not actually true.

`PORTFOLIO-OVERSIGHT.md` is the deterministic sensor. Scheduled/rotating agents are the judgment layer.

## Startup overlay

After reading `AGENTS.md`, `CONTROL.md`, `project-overrides.yaml`, and `projects/priority.yaml`, read `PORTFOLIO-OVERSIGHT.md` before accepting an ordinary `select_role.py` Worker/Reviewer fallback.

Use these oversight roles when the report says they are needed, in this order:

1. **schedule-medic** — scheduled-agent heartbeat is overdue. Confirm whether the external scheduled sessions are still firing. The heartbeat is evidence of repo activity, not proof by itself: a genuinely clean/no-op scheduled session may leave no commit. If the external scheduler is healthy, record that evidence and do not manufacture work. If it is absent, surface the platform-level gate immediately; repo code cannot recreate an external trigger.
2. **project-sync-auditor** — Kind Robots ↔ Conductor project parity has forward drift, reverse orphan(s), or could not be verified. Run `scripts/check_project_scaffold_drift.py` with the production-safe token path. Verify every Kind Robots `conductorSlug` resolves to one Conductor roadmap and every active Conductor project has the intended Kind Robots row. Where live Project settings are available, also verify the Conductor-owned coordination fields projected into Kind Robots still agree with `project-overrides.yaml` and `projects/priority.yaml`; presentation-only fields remain Kind Robots-owned per `SOURCE_OF_TRUTH.md`.
3. **roadmap-auditor** — `audit_roadmaps.py` reports deterministic errors. Repair unambiguous bookkeeping/state defects immediately. Never paper over a source-of-truth conflict by changing whichever side is easiest.
4. **roadmap-intent-auditor** — the semantic intent review is due. This is deliberately model/human-judgment work rather than another regex. Perform the review described below and write a dated report only after actually completing it.

Broken/reviewable code already in flight can still outrank a soft semantic review when delaying it is clearly higher leverage, but deterministic project/roadmap drift should not sit indefinitely behind ordinary ready-task churn.

## Project-sync audit

The existing `scripts/check_project_scaffold_drift.py` is the minimum mechanical contract, not the whole review. For each active/continuous project:

- Confirm the Conductor slug, Kind Robots `conductorSlug`, and roadmap directory identify the same project. Look for typo twins, duplicate rows, retired rows still claiming an active slug, and new Kind Robots projects whose scaffold Todo was closed without a roadmap landing.
- Confirm Conductor-owned lifecycle and priority intent are represented consistently. `project-overrides.yaml` and `projects/priority.yaml` are authoritative for coordination; Kind Robots is a projection/read surface for those fields.
- Do not overwrite Kind Robots-owned presentation metadata (title, description, art, visibility/presentation choices) just to make a mechanical comparison pass.
- If the answer is unambiguous, fix the stale coordination record. If two live sources both plausibly encode different recent human decisions, preserve both and raise one concise `FOR SILAS:` choice rather than guessing.

## Roadmap-intent audit

Run this at least every **3 days**, and sooner after a substantial priority or direction change.

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

## Scheduled-agent heartbeat

`scripts/build_portfolio_oversight.py` looks for recent git activity whose commit message identifies a scheduled Agent session. Default threshold: **6 hours**. This is a watchdog for the class of outage where external platform triggers disappear while GitHub Actions continue producing reports.

The threshold is intentionally looser than the usual cadence because not every valid scheduled cycle must mutate the repo. Treat an overdue heartbeat as a reason to inspect the scheduler, not as proof that it is broken.

## Deterministic sensor

Run locally/CI:

```bash
python scripts/build_portfolio_oversight.py
```

With `KR_API_TOKEN`, it includes Kind Robots project parity. `--fail-on-action` exits non-zero when deterministic drift, an overdue scheduled-agent heartbeat, an overdue semantic intent review, or an unresolved Kind Robots parity check requires attention. The scheduled `Conductor Oversight` workflow persists `PORTFOLIO-OVERSIGHT.{md,json}` so connector-only agents can consume the result without needing direct production API access.
