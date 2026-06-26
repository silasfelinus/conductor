# Conductor

Conductor is a project management repo built around AI agents doing real work. An AI Worker picks up tasks, does them on a branch, and opens a PR. A Reviewer (me, Claude) looks at the PR and either merges it or flags it for Silas. Silas steers things by editing roadmap files and approving gates — he stays out of the routine loop unless something actually needs him.

The whole thing runs on plain YAML files checked into git. No database, no dashboard to maintain. Git is the source of truth; rollback is just `git revert`.

## The basic loop

1. **Worker** runs on a schedule, reads `AGENTS.md` and the project roadmaps, claims the top available task, does the work on a branch, and opens a PR.
2. **Reviewer** fires when a PR lands. It merges straightforward software work automatically. Anything involving content, proposals, or outward-facing changes gets escalated to `needs-human` for Silas to look at.
3. **Digest** goes out daily — a summary of what's progressing, what merged, and what needs Silas's attention or vote.

## Daily digest email

The `daily-digest` GitHub Actions workflow builds `digest.json` with `scripts/build_digest.py`, validates the JSON shape, and sends it through Brevo transactional email.

Configure these under **Settings → Secrets and variables → Actions → Secrets → New repository secret**:

| Name | Required | Notes |
|---|---:|---|
| `BREVO_API_KEY` | yes | Brevo transactional email API key. |
| `DIGEST_TO` | yes | Recipient email address. |
| `DIGEST_FROM` | yes | Sender email address allowed by Brevo. |
| `DIGEST_TO_NAME` | no | Defaults to `Silas`. |
| `DIGEST_FROM_NAME` | no | Defaults to `AI_Networker`. |

`DIGEST_TO`, `DIGEST_FROM`, `DIGEST_TO_NAME`, and `DIGEST_FROM_NAME` may also be repository variables if you prefer keeping only the API key secret. `BREVO_API_KEY` must stay secret.

Each run uploads `daily-digest-json` as a workflow artifact so the generated payload can be inspected even if Brevo rejects the send. The workflow also prints which required and optional configuration names are present or missing without printing any secret values. If `digest.json` is invalid, missing required top-level keys, has non-list summary fields, or includes malformed project entries, the workflow fails before checking configuration or contacting Brevo.

## Project kinds

Every project has a `kind` that controls how the Reviewer handles finished work:

- **software** — output is a merged PR. Low-stakes reversible work merges automatically; everything else gets escalated.
- **content** — output is a file (copy, marketing plans, etc.). Nothing goes live without Silas approving it first.
- **proposal** — the work *is* a pitch. The Worker writes it to `pitches/` and stops; Silas decides whether to act on it.

When in doubt the Reviewer treats work as the more cautious kind.

## How Silas steers

Edit `notes_from_silas` in any project's `roadmap.yaml` to give direction. Change task statuses directly to reprioritize. For gated tasks, set `approved_by_human: true` on the upstream task to unlock the next stage. Drop new project ideas into `pitches/` or `intake/`. That's it.

## Pipelines and gates

Tasks can declare `depends_on` to form a pipeline — a task stays `waiting` until its upstreams are done. If an upstream task has `gate_human: true`, it also needs `approved_by_human: true` before dependents unlock. This is how multi-stage flows work: research → Silas picks a direction → create → review → ship, each stage only proceeding with explicit sign-off.

The Worker runs `scripts/resolve_deps.py` at the start of every cycle to flip any newly-unblocked `waiting` tasks to `ready`.

## Repo layout

```
AGENTS.md                           operating manual for all agents
CONTROL.md                          Silas's current intent — overrides roadmaps
projects/<name>/roadmap.yaml        one task queue per project; this is where Silas steers
projects/priority.yaml              which project leads
pitches/                            proposals waiting for Silas's vote
intake/                             new project requests before they're scaffolded
scripts/resolve_deps.py             unblocks pipeline tasks each cycle
scripts/build_status.py             regenerates STATUS.md
scripts/build_digest.py             builds the daily digest JSON
scripts/build_workspace.py          regenerates workspace.html
scripts/topology.py                 prints dependency graphs
scripts/intake.py                   scaffolds a new project from a request file
docs/TOPOLOGY.md                    how to read and declare dependencies
STATUS.md                           auto-generated snapshot — do not edit
workspace.html                      auto-generated dashboard — do not edit
```

## Current projects

| Project | What it is | Kind |
|---|---|---|
| humboldt-scoop | Existing site — adding the codebase under /site | software |
| humboldt-poop-scoop-cms | New customer management software | software |
| digital-storefront | Research → create → market → advertise pipeline; nothing publishes unattended | content |
| approval-portal | The console Silas lives in: pick pitches, validate upgrades, confirm updates | software |
| kind-robots | Apps consuming the shared KR backend (read-only) | software |
| coat-dance | Content project, awaiting Silas's direction | content |
| mermaids-of-venice | Content project, awaiting Silas's direction | content |

## Pitches

Any agent (or Silas) can drop a pitch into `pitches/` as a markdown file. The daily digest surfaces ones with `status: awaiting-silas`. Silas sets the status to `approved` or `rejected` — approved pitches can become new projects via `scripts/intake.py`.
