# Pitches

Where proposal-kind agents (and any agent with an idea) drop pitches for Silas to vet.
One file per pitch: `pitches/<date>-<slug>.md`, using the pitch template in AGENTS.md.

Pitches surface in the Conductor review queue. The canonical statuses are:

- `awaiting-silas` — needs a human decision
- `approved` — accepted; move the useful work into the target project roadmap
- `rejected` — declined after review (`passed` is a legacy alias)
- `duplicate` — already represented by an existing project, task, or shipped feature
- `superseded` — the underlying need belongs in a newer or broader system
- `archived` — retained for history or inspiration, but not actionable

Approved and rejected pitches remain in history instead of lingering in the active queue. Duplicate, superseded, and archived pitches belong in the archive tab. Before creating any pitch, compare it against every pitch regardless of status, active project goals and tasks, STATUS.md, and relevant shipped Kind Robots features. A renamed existing feature is not a new pitch.


## Daily docket

`pitches/daily/<date>.yaml` holds the five new project pitches the digest shows each day, validated by `scripts/daily_pitches.py` (five per day, at least three needing no LLM at runtime, deduped against projects, pitches and earlier days). Silas's decisions live in `pitches/daily/decisions.yaml`. An approved pitch becomes a project via `scripts/intake.py`; the longer `pitches/<date>-<slug>.md` template above still applies to proposal-kind tasks.
