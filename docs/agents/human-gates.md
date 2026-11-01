# Human gates — hard vs soft, notes for Silas, gate legitimacy

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> Read before parking any task at `needs-human` or running `gate-triage`.

### Hard vs soft needs-human

`needs-human` has two flavors — agents must distinguish them:

**Hard** (Silas must act before anything proceeds):
- `gate_human: true` on the task
- `stakes: outward-facing` or `stakes: irreversible`
- Content or proposal kind reaching publication/delivery
- Security flags requiring acknowledgement

**Soft** (agent got stuck, no workaround found — but other work can continue):
- Connector/tooling failure mid-task where content is complete
- Unclear architectural direction without a blocking dependency
- Access limitation that prevents verification but doesn't invalidate the work

On a **soft** `needs-human`: set the task status, add `soft_gate: true`, document the reason clearly in the task
`note:`, then **immediately re-run task selection** and pick the next available `ready` task.
Do not end the cycle — there is almost always other work. Only stop if every ready task is
also blocked. `soft_gate: true` is metadata for auditors and coordinators; it never satisfies a dependency
or grants permission for outward-facing work.

On a **hard** `needs-human`: stop. Do not pick another task. Flag clearly for Silas.

**Scope gates on NEW projects are soft** (Silas, 2026-07-04): when a fresh project or
pitched idea lands, do not park it behind scope approval. Build the design brief and
start working immediately; raise the scope-confirmation task as a soft needs-human that
runs in parallel with development. Course correction after Silas responds is cheap and
expected — the bias is toward making things happen. (Outward-facing/irreversible steps
remain hard gates as always.)

**Lifecycle clarification (Silas, 2026-08-07):** `continuous` now owns never-idle
behavior. The historical autonomous rules below apply only when the project's override
status is `continuous`. `autonomous: true` on a finite `active` roadmap may grant broad
initiative while real ready tasks exist, but it may not invent endless polish/content work
after the finite queue empties. AI Art Academy's test-run never-idle loop is explicitly
ended; Animation Manager and Dream Cycle are the initial continuous programs.

**Autonomous projects — never idle** (Silas, 2026-07-10): a roadmap may declare
`autonomous: true` (first test run: ai-art-academy). These projects must keep moving
without Silas's input:
- Escalate only ACTUAL human gates — spend, publishing, outward-facing/irreversible
  steps, licensing doubts, backend schema needs. Everything else: decide, record the
  decision in the task note or docs, and keep building. Scope confirmations are soft
  gates that run in parallel; course-correct when Silas replies.
- When an autonomous project has no `ready` task, the Worker does NOT stop or invent
  arbitrary work — it may create and immediately claim exactly ONE improvement task
  from the standing menu: (a) a style/polish pass on the project's front end, (b) a
  roadmap upgrade (refine tasks, detail the next milestone, prune stale notes), (c)
  generate more art inspirations or content assets, (d) expand the project's
  docs/curriculum/content. `stakes: reversible`, normal PR flow, one per cycle.
  Prefer a recurring roadmap task that encodes this menu (e.g. ai-art-academy/t-010)
  over ad-hoc task creation when one exists.
- All other safety rules still apply unchanged — autonomy widens WHAT gets worked on,
  never WHO can approve gates.

**Generated art is pre-approved** (Silas, 2026-07-06): internal auto-generated project art
is not a human gate. Agents may request, create, commit, and promote generated images for
project icons/cards/heroes, inspirations, ArtCollections, Dream images, Bot avatars, and Bot
emotion/action portraits when the action is task-scoped, traceable, and reversible. Keep the
prompt/model/source metadata needed to recreate or delete the image. This does not authorize
publishing, external posting, paid tool spend, production deploys, billing, secrets, or DNS.

### Writing needs-human task notes for Silas (not for agents)

When a task ends at `needs-human`, rewrite the `note:` field so Silas can act on it
without reading the surrounding code or roadmap. Use this structure:

```
FOR SILAS: What was produced and where to find it (file path, one sentence).
What it contains (2-3 specific things, not agent jargon).
TO APPROVE: What Silas needs to read, decide, or change — and the exact edit
to make (set approved_by_human: true and status: done, or add a note with X).
What unblocks when he does (next task id + what it will do).
```

Do NOT write the note for the next agent to read. The agent reads the roadmap;
Silas reads the note. Agent-facing context belongs in the PR description.

### A gate must say why it needs a human, or agents take it back

Silas, 2026-09-30: *"can we get some sort of oversight so that we aren't allowing things to hang
when its not really a human gate issue?"* The triage that prompted this found 15 of 51 open gates
were agent work. Examples: a dependency wait filed as a gate. A decision already answered by one of
Silas's standing directives. A "needs a Force Update" block on a fix that had been live for nine
days. A "needs DATABASE_URL" block that an admin endpoint plus a workflow would have removed.

- **`gate_reason:`** names why a human is needed. It is one of `money`, `publish`, `legal`,
  `irreversible`, `secrets`, `security`, `physical-access`, `subjective-acceptance`, or
  `creative-approval`. Set it whenever you park a task at `needs-human`. If none fits, it is
  probably not a human gate.
- **`python scripts/check_gate_legitimacy.py [--live]`** flags gates agents should take back:
  - NO_GATE_BASIS: a hard gate with no hard-gate marker.
  - APPROVED_PARKED: an approved decision nobody executed.
  - SHOULD_BE_WAITING: an unmet `depends_on`. Use `status: waiting` instead.
  - DEPLOY_PREREQ_MET: waiting on a deploy that has already shipped.
  - UNREVIEWED: not re-triaged in 7 days (soft), 14 days (hard), or 30 days (with a human-only
    `gate_reason`).
- **`select_role.py` returns `gate-triage`** while any finding exists. It ranks above `worker`.
  Clear each finding in one of three ways: execute it, reclassify it (`ready`/`waiting`, or a
  new ready task for the engineering it hides), or re-check it for real and stamp
  `gate_rechecked: YYYY-MM-DD` with a one-line reason in the note. A stamp without a real
  re-check is the failure this exists to stop.
- Before parking on access ("needs DB/shell/Alexandria"), ask whether an admin HTTPS endpoint
  plus a conductor workflow using `KR_API_TOKEN` would remove the need. That is how
  art-archive/t-040 turned a shell-only import into a button. Building that path is agent work.
- Before parking on a decision, check CONTROL.md, `notes_from_silas`, and standing directives.
  If Silas has already answered, apply the answer.
- **Default-recommendation rule (Silas, 2026-09-30, standing).** A reversible product decision
  gate can be parked only with a written recommendation. If Silas has not answered within 7 days,
  the next `gate-triage` session adopts the recommendation. It records "ADOPTED under the
  2026-09-30 default-recommendation rule" in the note, sets the task back to `ready`, and builds
  it. Silas can still reverse the decision later. This never applies to a gate whose
  `gate_reason` is money, publish, legal, security, irreversible, secrets, or physical-access.
  Leave `approved_by_human` unset when adopting. Only Silas's own answer sets it.
