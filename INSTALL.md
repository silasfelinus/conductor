# Brainstorm project — install

Additions to your existing AI_Networker repo. Copy to matching paths:

- projects/brainstorm/roadmap.yaml     -> NEW (the idea engine)
- projects/brainstorm/CHANGELOG.md     -> NEW
- projects/priority.yaml               -> REPLACES (adds brainstorm at the end)
- AGENTS.md                            -> REPLACES (adds recurring-task rules)
- CONTROL.md                           -> REPLACES (adds brainstorm direction + genre block)
- pitches/2026-06-24-coloring-book-kindness.md   -> NEW (sample pitch to vote on)
- pitches/2026-06-24-networker-cost-guard.md     -> NEW (sample pitch to vote on)

Then:
  python scripts/build_status.py     # refresh STATUS.md (or let the push Action do it)
  git add -A
  git commit -m "add brainstorm idea-generation project + sample pitches"
  git push

## How it works
brainstorm is a proposal-kind project. Its one task (t-001) is RECURRING: each cycle the
Worker generates up to 3 new pitches into pitches/, then re-arms the task to ready (it
never completes). Caps in the roadmap's pitch_policy stop it flooding you:
- max 3 new pitches/cycle
- generates 0 if 12+ are already awaiting your vote
- dedups against existing pitches

## Steering it
Edit the brainstorm block in CONTROL.md — especially the "Genre / content guidance" lines,
which is where you tell it e.g. your comic genre rules. Vote by setting a pitch's status:
to approved or rejected. It sits last in priority.yaml, so it fills idle cycles rather than
crowding out real project work.
