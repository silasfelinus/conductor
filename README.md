# Conductor

Conductor is a private, single-owner, Git-native project manager for Silas's projects. Agents deliver work; deterministic scripts and GitHub Actions coordinate it. Git is the authoritative task ledger. Kind Robots owns runtime/presentation and reads the existing commit-stamped projection; no new Conductor API, service or database is required.

**Architecture and critique entrypoint:** [Lightweight Conductor](docs/agents/LIGHTWEIGHT-CONDUCTOR.md). Read it for the design, current rollout, invariants and review questions, not as a second mandatory agent prompt.

## The basic loop

1. **Assignment:** read [AGENTS.md](AGENTS.md) once. Accept a direct assignment or use the live selector / generated [STATUS.md](STATUS.md) pickup hints. Load only the assigned role, project direction and task.
2. **Execution:** claim canonical work using the session-aware protocol, implement and test a narrow scope, transition to review and open a PR.
3. **Verification:** check latest-head CI, fix failures, merge reversible ungated work and reconcile completion. Human approvals remain separate.
4. **Maintenance:** Actions handle deterministic checks, task events, dependencies, generated views and digest plumbing. Agents diagnose exceptions, not duplicate every scan.

Six specialist assignments are developer, reviewer, content, art, QA and daily creative. Existing medic roles handle exceptions. No routine model-provider API calls from Actions.

See [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md) for ownership, [CONTROL.md](CONTROL.md) for current direction, and the [connector protocol](docs/github-connector-worker.md) for live claims and transitions.

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
| `DIGEST_SMTP_USER` | recommended | Gmail address the digest is sent from over SMTP. With `DIGEST_SMTP_PASSWORD` set, the digest goes out through Gmail with its links untouched; Brevo becomes the fallback. |
| `DIGEST_SMTP_PASSWORD` | recommended | A Gmail [app password](https://myaccount.google.com/apppasswords) for `DIGEST_SMTP_USER` (needs 2-Step Verification). Not the account password. |
| `DIGEST_SMTP_FROM` | no | From address if it differs from `DIGEST_SMTP_USER` (must be a verified Gmail "Send mail as" alias). May also be a repository variable. |

Do not add a model-provider API key to this repo for routine worker or digest operation. If a future task genuinely needs one, make that a separate human-approved design change instead of quietly adding it to Actions.

## Daily digest email

The `daily-digest` GitHub Actions workflow builds `digest.json` with `scripts/build_digest.py`, validates the JSON shape, renders a Brevo payload preview, and sends scheduled runs through Brevo transactional email.

When `DIGEST_SMTP_USER` and `DIGEST_SMTP_PASSWORD` are set, the send step uses Gmail SMTP first and only falls back to Brevo if that fails. Brevo rewrites every link in transactional mail through its `sendibt*.com` click tracker and offers no self-serve way to turn that off, so SMTP is the only path that delivers direct Kind Robots links (animation-manager t-026).

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
