# Recovering approved historical daily pitches

The **approved-pitch recovery** job closes the gap between an older daily
pitch vote and Conductor's actual build queue. It is not the current daily
deliveries policy.

## Scope and source of truth

- The vote in `pitches/YYYY-MM-DD-<slug>.md` is authoritative. Only a
  materialized record with `status: approved` is eligible.
- Only dockets **before 2026-10-13 Pacific** are candidates. The current
  five-evidenced-upgrades daily process lives in
  `scripts/daily_project_deliveries.py` and remains separate.
- A new idea gets an existing `intake.py` scaffold and actionable tasks for
  **a real admin preview, implementation/art, and later polish**. This does
  not create a placeholder URL or falsely claim the app can already run.
- An approved enhancement to another project becomes a single ready task
  in that existing roadmap, source-linked for deduplication.
- An Arcade-targeted pitch goes into the existing `kr-arcade/games.yaml`
  queue. It does **not** create another top-level Conductor project.
- Source linkage and slug checks make repeat runs safe. A missing target
  fails rather than fabricating an unrelated project.

## Operator commands

Preview the scope without any edits:

```bash
python scripts/approved_pitch_recovery.py
```

Apply once (writes repository coordination files only):

```bash
python scripts/approved_pitch_recovery.py --apply
python scripts/validate_roadmaps.py
```

The GitHub Actions workflow
`.github/workflows/recover-approved-pitches.yml` runs hourly and on
relevant main-branch pitch changes. It tests the recovery logic before
applying it, commits only real changes, and avoids force pushes. If
another main writer wins the race, the job fails and the next run
rechecks from the current main. After a real change, it dispatches
the Kind Robots projection sync; that projection is **read-only**
coordination data, not a live Project presentation or route mutation.

## What this does not do

It does not send API requests to Kind Robots, generate or pay for art,
open public Play routes, auto-approve publishing, or claim a scaffold is
playable. Approved projects still need actual scoped implementation PRs,
completed passing CI, tested admin preview routes with contextual help,
verified images, and explicit authorization for public release.

Track these later acceptance steps in
[Conductor issue #6013](https://github.com/silasfelinus/conductor/issues/6013)
and its `conductor/t-207` task. Do not close either from the intake-only
slice.
