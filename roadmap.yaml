# Setup — AI_Networker Agent Loop

Your repo already exists (github.com/silasfelinus/AI_Networker) with .gitignore, LICENSE,
and a README. These files drop in alongside those. Do the steps in order.

## 1. Add the scaffold to the repo
From inside your existing clone (keeps the LICENSE/.gitignore already there):
```bash
git checkout -b scaffold-agent-loop
# copy the unzipped files into the repo root:
#   AGENTS.md CLAUDE.md projects/ pitches/ scripts/ .github/ docs/ README.md
git add -A
git commit -m "scaffold agent coordination loop + 3 projects + pitches"
git push -u origin scaffold-agent-loop
```
Open a PR and merge it yourself — the one human merge before the loop takes over.

## 2. Branch protection on `main`
Settings → Branches → rule for `main`: require a pull request before merging. Makes
"PRs only, no rogue commits" structural. (The sample pitch suggests adding a CI gate so
you can also require status checks — your call whether to approve it.)

## 3. Secrets (Settings → Secrets and variables → Actions)
- `RESEND_API_KEY` — from resend.com (free tier fine).
- `DIGEST_TO` — your email.
- `DIGEST_FROM` — a sender on a domain verified in Resend. You run Cloudflare email for
  humboldtscoopsolutions.com, so verifying a sender there is straightforward.

Test it: Actions tab → daily-digest → Run workflow. You should get an email showing the
three projects and the sample pitch under "Awaiting your vote."

## 4. Worker — ChatGPT Task (hourly, GitHub connector enabled)
> You are the Worker agent for the silasfelinus/AI_Networker repo.
> 1. Read AGENTS.md in full. Run `python scripts/resolve_deps.py` and commit any unblock
>    changes to main with message "resolve: unblock dependents".
> 2. Read projects/priority.yaml and every projects/*/roadmap.yaml (skip _template).
> 3. Honor each project's notes_from_silas and priority.yaml ordering.
> 4. Find the highest-priority task with status: ready. Never touch status: waiting tasks.
>    If none ready anywhere, stop — don't invent work.
> 5. Note the project's `kind` (software/content/proposal) — it sets how you finish.
> 6. Atomically claim it: set status: claimed, owner: worker, bump updated, commit that
>    one change to main with message "claim: <project>/<task-id>".
> 7. Branch worker/<project>-<task-id>, do ONLY that task. software: PR + handoff template,
>    status: review. content: write draft, PR, status: needs-human. proposal: write
>    pitches/<date>-<slug>.md, PR, status: needs-human. If the task has gate_human: true,
>    always finish at status: needs-human regardless of kind.
> 8. Never merge. Never push to main except the claim/resolve commits. One task at a time.
> 9. Never deploy, send, publish, list a product, or spend money — status: needs-human.

## 5. Reviewer — Claude Code Routine (event-triggered)
At claude.ai/code/routines (or /schedule in CLI):
- Repository: silasfelinus/AI_Networker. Install the Claude GitHub App on the repo when
  prompted (web-setup alone grants clone access but does NOT install the App — webhooks
  need the App).
- Trigger: GitHub event → pull_request opened, filter head branch = worker/*
- Prompt:
  > You are the Reviewer. Read AGENTS.md. Check the target project's `kind` in its
  > roadmap. For software PRs that do the task, are scoped, and reversible: approve,
  > merge, set status: done on main, bump updated. Needs changes: comment specifically,
  > set status: ready, increment passes (at passes==3 set blocked). For content or
  > proposal or anything outward-facing/irreversible: do not trigger publish/deploy/send;
  > leave at status: needs-human for Silas. Never re-implement the Worker's task yourself.
- Plan note: Pro = 5 routine runs/day. Event-triggered keeps you in budget as long as the
  Worker opens ≤5 PRs/day. Max raises it to 15.

## 6. First-run discipline
humboldt-scoop t-001 (the no-op smoke test) is the top ready task. Let one full
Worker → PR → Reviewer → merge → digest cycle complete before trusting it unattended.

## Driving the pipelines (storefront, portal)
These projects have staged tasks: one is `ready`, the rest are `waiting` behind it. When a
gated task finishes, it lands at `status: needs-human`. To advance the pipeline, edit that
task in the roadmap: set `approved_by_human: true` and `status: done`. The next Worker run
auto-unblocks the next stage. That single edit is your "I picked / I approve" action — for
which stores to pursue, which concepts to build, whether the portal spec is good, etc.

## Adding projects later (brainstorm agent, more pipelines, etc.)
Copy projects/_template to projects/<name>, set its `kind`, fill the roadmap, add it to
priority.yaml. For the brainstorm agent: make a `proposal`-kind project whose roadmap
tells it to generate N pitches per cycle into pitches/. Agents and digest pick it up
automatically.

## Gotchas
- Routines + Managed Agents are research preview / beta as of mid-2026; limits and APIs
  may shift. Watch run records the first week.
- The claim-commit on main is the race tiebreaker: first claim wins. Fine for one Worker
  + one Reviewer; harden if you add Workers.
- The digest is your trust gauge. While its escalations and pitch list match your own
  judgment, the loop is calibrated right.
