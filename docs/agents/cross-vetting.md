# Cross-vetting, TALKBACK entries, challenges and security flags

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> Read before writing a TALKBACK entry or challenging a decision.

## Cross-vetting protocol

Agents are expected to critique each other's methods, not just the output of a single task.
This section defines how.

### What Worker critiques in Reviewer
- Decisions that seem inconsistent with AGENTS.md or CONTROL.md
- Rejections where the stated reason doesn't match the diff
- Patterns of over-escalation (sending reversible work to `needs-human` unnecessarily)
- Patterns of under-escalation (merging work that should have been gated)

### What Reviewer critiques in Worker
- Scope violations (doing more or less than the task specified)
- Verification gaps (claimed "verified" but didn't check the relevant thing)
- Template discipline (missing or thin sections in the handoff)
- Recurring mistakes across tasks (same error in multiple cycles)
- Dependency shortcuts (doing work before a gate is properly cleared)
- Merge discipline problems (dropping valid changes, skipping conflicts, or failing to re-check after conflict fixes)

### How to write a talkback entry

Both agents use this format. Append to `projects/<name>/TALKBACK.md` for project-specific
observations, or to the root `TALKBACK.md` for system-level patterns. Never edit or
delete existing entries.

```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

### Challenge flow (Worker disputes a Reviewer decision)

1. Worker sets `status: challenged` on the task in `roadmap.yaml`.
2. Worker appends a `challenge` entry to the project's `TALKBACK.md` with its full case.
3. Reviewer reads the challenge entry and appends a `response` — either adjusting the
   decision (→ set `status: ready`, back to normal flow) or holding it (→ set
   `status: needs-human`, Silas arbitrates).
4. Silas resolves by editing the roadmap directly and leaving a note in the roadmap's
   task `note:` field. Challenged tasks never auto-resolve.
5. After resolution, both agents append a brief `response` entry noting what was learned.

A `challenged` task counts toward the iteration budget: if a task reaches `passes == 3`
via the normal retry loop, it goes to `blocked` as usual. Challenges and retries share the
same counter.

### Security flags

Either agent may append a `security-flag` entry to TALKBACK.md at any time. A security
flag is for observations about the system itself — scope creep, unexpected permissions,
suspicious patterns in PRs, or anything that makes the system less safe. Security flags
do NOT block the task cycle automatically, but they MUST be reviewed by Silas before
the next cycle that touches the flagged project. Include `security-flag: true` on the
relevant roadmap task if one exists.
