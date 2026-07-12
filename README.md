# Conductor

Conductor is a project management repo built around AI agents doing real work. A session-driven Worker picks up tasks, does them on a branch, and opens a PR. A Reviewer looks at the PR and either merges it or flags it for Silas. Silas steers things by editing roadmap files and approving gates — he stays out of the routine loop unless something actually needs him.

The repo itself does not call model-provider APIs from GitHub Actions. Agent judgment and implementation happen from interactive assistant sessions using GitHub tools/connectors. Actions are for deterministic checks, digest generation, and safe plumbing.

The whole thing runs on plain YAML files checked into git. No database, no dashboard to maintain. Git is the source of truth; rollback is just `git revert`.

## The basic loop

1. **Worker session** reads `AGENTS.md`, `CONTROL.md`, and the project roadmaps, claims the top available task, does the work on a branch, and opens a PR.
2. **Reviewer session** fires when a PR lands. It merges straightforward software work automatically. Anything involving content, proposals, or outward-facing changes gets escalated to `needs-human` for Silas to look at.
3. **Actions healthcheck** validates the queue, dependency resolver, and digest plumbing without calling a model-provider API.
4. **Digest** goes out daily — a summary of what's progressing, what merged, and what needs Silas's attention or vote.

## Action secrets

Configure these under **Settings → Secrets and variables → Actions → Repository secrets → New repository secret**:

| Name | Required | Notes |
|---|---:|---|
| `KR_API_TOKEN` | recommended | Kind Robots app/JWT token used by repo plumbing for Todo checks and optional Dream sync. Not a GitHub token. |
| `BREVO_API_KEY` | yes for scheduled digest email | Brevo transactional email API key. |
| `DIGEST_TO` | yes for scheduled digest email | Recipient email address. May also be a repository variable. |
| `DIGEST_FROM` | yes for scheduled digest email | Sender email address allowed by Brevo. May also be a repository variable. |
| `DIGEST_TO_NAME` | no | Defaults to `Silas`. May also be a repository variable. |
| `DIGEST_FROM_NAME` | no | Defaults to `AI_Networker`. May also be a repository variable. |

Do not add a model-provider API key to this repo for routine worker or digest operation. If a future task genuinely needs one, make that a separate human-approved design change instead of quietly adding it to Actions.

## Daily digest email

The `daily-digest` GitHub Actions workflow builds `digest.json` with `scripts/build_digest.py`, validates the JSON shape, renders a Brevo payload preview, and sends scheduled runs through Brevo transactional email.

Each run uploads `daily-digest-artifacts` containing `digest.json` and `digest-email.json`. The generated `digest-email.json` preview omits recipient, sender, and API key values. The workflow also prints which required and optional configuration names are present or missing without printing any secret values. Scheduled runs still require `BREVO_API_KEY`, `DIGEST_TO`, and `DIGEST_FROM` before sending.

Manual `workflow_dispatch` runs default to a safe dry run and do not send email. They still build and upload the digest artifacts so the JSON payload and rendered email body can be inspected. To intentionally send a manual test email, run the workflow with `send_email` enabled.

## Worker healthcheck

The `Worker Healthcheck` workflow runs `scripts/run_worker.py --dry-run`. It checks Todo visibility when `KR_API_TOKEN` is available, runs dependency resolution in dry-run mode, builds and validates the daily digest JSON, and prints the highest-priority ready task. It does not claim tasks, open PRs, merge branches, or call model-provider APIs.

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

The Worker healthcheck runs `scripts/resolve_deps.py --dry-run` so dependency changes are visible without mutating roadmaps from Actions.

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
| humboldt-scoop-cms | Customer management, scheduling, visit records, billing drafts, and Android-first mapped route planning | software |
| model-builder | Resumable gated recipe runner for upgrading or creating Kind Robots records; Marketing Deck is one preset | software |
| digital-storefront | Research → create → market → advertise pipeline; nothing publishes unattended | content |
| approval-portal | The console Silas lives in: pick pitches, validate upgrades, confirm updates | software |
| kind-robots | Apps consuming the shared KR backend (read-only) | software |
| coat-dance | Content project, awaiting Silas's direction | content |
| mermaids-of-venice | Content project, awaiting Silas's direction | content |

## Pitches

Any agent or Silas can drop a pitch into `pitches/` as a markdown file. The daily digest surfaces ones with `status: awaiting-silas`. Silas sets the status to `approved` or `rejected` — approved pitches can become new projects via `scripts/intake.py`.
