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

`pitches/daily/<date>.yaml` is the source for the five new project pitches the digest shows each day; `scripts/daily_pitches.py` validates it (five per day, at least three needing no LLM at runtime, deduped against projects, pitches and earlier days) and `--materialize` writes one `pitches/<date>-<slug>.md` per pitch. Those files are the decision record: the Kind Robots project page lists and votes on them, and the digest's Approve / Pass buttons (signed links, `scripts/pitch_links.py`) write the same `status:` line. Sessions author pitches and never decide them. An approved pitch becomes a project via `scripts/intake.py` (`daily_pitches.py --approved` lists the ones waiting). The longer pitch template above still applies to proposal-kind tasks.
