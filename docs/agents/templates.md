# Reviewer feedback and pitch templates

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> The PR handoff template stays in AGENTS.md because check_pr_handoff_template.py enforces it.

## Reviewer feedback template (unresolved critique, challenge or material pattern only)
```
## YYYY-MM-DD | Reviewer → Worker | <project>/<task-id> | <critique|pattern|response>

**Decision:** merged | rejected (pass N) | escalated to needs-human | challenge resolved | audited already-merged work

**Failure category:** (rejections/blocks only) transient | actionable | quality | scope —
per the "Failure triage" section. Quality/scope: also write `retry_context:` on the task.

**What was good:**
- specific things the Worker did well

**What to improve:**
- specific, actionable critique with reference to the diff or output

**Kaizen task:** <task-id created> — <one sentence> (or "deferred — <reason>")
Do not create a task merely because a PR merged. Only a demonstrated defect, unmet original
requirement or explicit owner direction warrants a new task; optional ideas are nonblocking.
Use "None" for an ordinary successful closure. Completed work is history, not a TALKBACK source.

**Pattern note:** (optional — only if this is a recurring issue across tasks)
- describe the pattern and link to prior instances in this file
```

## Pitch template (proposal-kind tasks → pitches/<date>-<slug>.md)
```
# Pitch: <title>
date: <iso>
project-target: <existing project name, or "new", or "ai-networker-itself">
status: awaiting-silas        # awaiting-silas | approved | rejected

## The idea
2-4 sentences.

## Why it's worth doing
## Rough effort
small | medium | large
## Suggested first task
What the Worker would do first if you approve.
```
