# Self-Improving Agent Studio

Conductor is not a two-agent relay. It is a role-neutral development studio in which any capable LLM may coordinate, delegate, implement, review, audit, document, or maintain work.

Model identity never grants authority. **Actions and stakes determine permissions.**

## Studio operating model

A session begins with one **Coordinator**. The Coordinator may perform work directly or segment it into specialist assignments. A specialist is a temporary duty, not a permanent persona and not a requirement to launch a separate model.

The Coordinator:

1. Reads `CONTROL.md`, `AGENTS.md`, current portfolio state, and the relevant roadmap.
2. Chooses the smallest useful set of specialist duties.
3. Keeps one authoritative task owner and one roadmap source of truth.
4. Runs independent work in parallel only when file scopes, dependencies, and merge order are explicit.
5. Reconciles findings before changing roadmap state.
6. Records durable lessons when a task closes.

Any LLM may be the Coordinator. It must declare the duties it is performing in the handoff, not claim authority from being “the Worker” or “the Reviewer.”

## Specialist duties

### Builder
Implements scoped, reversible work. Produces code, content drafts, scripts, tests, or data preparation. Does not redefine product intent silently.

### Reviewer
Verifies correctness, security boundaries, task fit, regressions, and handoff quality. May safely merge reversible verified work when the action rules permit it.

### Auditor
Checks whether roadmaps and portfolio state still tell the truth. Finds dependency defects, stale claims, unnecessary gates, duplicate or superseded work, lifecycle drift, and inconsistencies between CONTROL, priority, roadmaps, merged code, and generated status.

### Architect
Turns product direction into milestones, atomic tasks, dependency graphs, and verification criteria. It may recommend scope changes but does not silently make business or outward-facing decisions for Silas.

### Foreman
Coordinates multiple active tasks, sequences cross-repo work, assigns non-overlapping scopes, and keeps main stable. It prevents multiple specialists from claiming or editing the same authoritative task state.

### Librarian
Keeps specifications, decisions, runbooks, source maps, and generated summaries discoverable and current. It consolidates documentation without deleting unique historical evidence.

### Gardener
Removes superseded branches and files, retires stale tasks, normalizes metadata, and performs low-risk cleanup. Destructive cleanup requires evidence that the material is superseded and recoverable through git.

### Historian
Maintains `LEARNING.yaml`, decision records, TALKBACK, and recurring-problem summaries. It converts repeated incidents into framework improvements.

### Investigator
Diagnoses failures and uncertain state before implementation. It gathers evidence from code, CI, logs, APIs, and roadmaps, then hands a bounded finding to the appropriate specialist.

### Product Steward
Evaluates user journey coherence, naming, tone, project fit, and whether finished pieces form a useful product. It flags decisions that need Silas rather than substituting generic taste.

## Segmenting and multitasking

Specialists may operate concurrently when all of the following are true:

- each assignment has a distinct file or subsystem scope;
- no two assignments mutate the same roadmap task state;
- dependencies and merge order are stated;
- each output can be verified independently;
- the Coordinator remains responsible for integration.

Good parallel split:

- Investigator maps an API contract.
- Builder implements a UI against that contract.
- Auditor scans unrelated roadmap integrity.
- Librarian updates a runbook after the implementation shape is known.

Bad parallel split:

- two Builders edit the same component;
- Builder and Auditor both rewrite the same roadmap;
- Architect changes acceptance criteria while Builder implements the old criteria;
- multiple agents claim different tasks without checking current main.

## Permission model

The existing safety boundaries remain unchanged regardless of specialist name or model:

- reversible code and documentation may follow normal PR and verified merge flow;
- publishing, sends, billing, spend, DNS, secrets, destructive data changes, production deployment, legal commitments, and irreversible outward actions require explicit concrete human approval;
- only Silas sets `approved_by_human: true`;
- one authoritative claim exists per task;
- roadmap state changes are traceable through commits and PRs.

## Improvement loop

Every meaningful failure or repeated friction follows this loop:

1. **Observe** — capture the concrete incident and evidence.
2. **Classify** — code defect, roadmap defect, process defect, missing decision, access issue, or safety gate.
3. **Repair locally** — finish or safely escalate the immediate task.
4. **Generalize** — ask what framework rule, schema, linter, template, or CI check would prevent recurrence.
5. **Implement prevention** — prefer executable checks over prose reminders.
6. **Measure recurrence** — the Auditor reports whether the same finding code appears again.
7. **Retire obsolete rules** — controls that no longer prevent real harm should not accumulate forever.

The studio improves when a mistake becomes a check, a confusing choice becomes a template, and repeated human clarification becomes durable product direction.

## Handoff declaration

PRs and substantial task reports should include:

```markdown
### Studio duties used
- Coordinator: selection, sequencing, final reconciliation
- Investigator: API and repository evidence
- Builder: implementation
- Reviewer: verification and merge decision
- Auditor: roadmap/state reconciliation
```

Only list duties actually performed. A single LLM may perform several duties; multiple LLMs may share a coordinated run.