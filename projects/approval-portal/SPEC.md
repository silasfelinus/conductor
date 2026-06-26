# Approval Portal Spec

## Purpose

Approval Portal is a small web console over the Conductor repository. The repo remains the source of truth. The portal reads project state from roadmap files, pitch files, Git history, and open pull requests, then helps Silas make explicit decisions that are written back as auditable Git changes.

The portal should not maintain a second project database. Any cached or indexed data must be disposable and rebuilt from the repository and GitHub API.

## V1 recommendation

Build a local-first Nuxt 4 / Vue 3 / TypeScript app under `projects/approval-portal/` with server API routes that read the checked-out repository files and call GitHub only for live PR and commit metadata. This matches Silas's house stack, keeps the UI familiar, and leaves room for later authenticated deployment without changing the data model.

Recommended stack:

- Nuxt 4 + Vue 3 + TypeScript for the app shell.
- Pinia for client-side state stores.
- Tailwind + DaisyUI for fast, readable screens.
- Nitro server routes for filesystem reads and GitHub API calls.
- `yaml` or `js-yaml` for roadmap parsing.
- No persistent database in m1. Derived JSON can be cached in memory only.

Alternative stack:

- A tiny static Astro or Vite app with a Node CLI that exports repo state to JSON.
- This is simpler for read-only viewing, but it becomes awkward once approvals, PR actions, and rollback flows need authenticated GitHub writes.

## Source-of-truth data

### Local repository files

The portal reads these files directly from the Conductor checkout:

- `CONTROL.md` for current steering direction and project order guidance.
- `project-overrides.yaml` for active, paused, retired, or finished project status.
- `projects/priority.yaml` for project selection order.
- `projects/*/roadmap.yaml` for project kind, milestones, tasks, dependency state, gates, and notes.
- `pitches/*.md` for proposal metadata and pitch body.
- `STATUS.md` as read-only display context only; never write it.
- `ART-PROMPTS.md` and `projects/images/` later for workspace visual asset status.

### GitHub API data

The portal reads live GitHub state for:

- Open PRs against `main`.
- PR author, branch, status, mergeability, checks, labels, and timestamps.
- Recent merged PRs and commits for update confirmation and rollback planning.
- Branch names matching `worker/*` for active work visibility.

The portal should not infer deployment status, DNS state, billing state, or secrets. Those are outside scope and remain human-gated.

## Screens by milestone

### m1: Read-only dashboard

The first usable milestone should be read-only.

Screens:

1. Project overview
   - Shows active projects from `project-overrides.yaml` and `projects/priority.yaml`.
   - Displays project kind, priority, milestone progress, task counts by status, and latest updated task.
   - Flags paused projects as inactive and hides them from the default work queue.

2. Project detail
   - Shows the selected project's CONTROL.md direction block.
   - Lists milestones and tasks grouped by status.
   - Highlights `ready`, `claimed`, `review`, `needs-human`, `blocked`, and `waiting` states.
   - Shows dependency chains and human gates.

3. Pitch queue
   - Lists `pitches/*.md` with `status: awaiting-silas`, `approved`, or `rejected`.
   - Shows project target, rough effort, suggested first task, and pitch body preview.
   - No approve/reject buttons yet.

4. PR queue
   - Lists open PRs against `main`.
   - Groups worker PRs by project/task when the branch or PR body includes those identifiers.
   - Shows check status and mergeability as informational only.

### m2: Pitch voting

Adds write actions for pitch decisions after Silas approves this spec.

Screens/actions:

- Approve pitch.
- Reject pitch.
- Add a short decision note.
- Show the exact file diff before writing.

The write mechanism should create a branch and PR by default, not commit directly to `main`, unless Silas explicitly enables direct writes for low-risk metadata.

### m3: Update confirmation

Adds a review console for worker PRs.

Screens/actions:

- View PR summary, changed files, checks, and handoff body.
- Mark a PR as accepted for Reviewer/merge flow.
- Mark a PR as rejected or needs changes by commenting and/or updating roadmap task status.
- Never merge outward-facing, irreversible, billing, DNS, deploy, send, or publish changes automatically.

### m4: Rollback

Adds safe rollback planning.

Screens/actions:

- List recent merged PRs and commits.
- Explain what would be reverted.
- Open a revert PR using `git revert` semantics.
- Never force-push or rewrite history.

### m5: Auth + deploy plan

Adds deploy planning only after the earlier flows are trusted.

Screens/actions:

- Single-user auth for Silas.
- GitHub token storage plan.
- Deployment checklist.
- No deployment or provisioning in the task itself.

## Repo-write strategy

### Default rule

All write actions should produce auditable Git changes. The safe default is:

1. Read current file SHA/ref.
2. Create a branch named `portal/<action>-<slug>-<timestamp>`.
3. Write the minimal file change.
4. Open a PR into `main` with a clear title and handoff body.
5. Let the existing Reviewer/human process merge or reject it.

### Direct-to-main exception

Direct commits to `main` should be disabled by default in the portal. They can be considered later only for explicitly approved metadata-only actions such as marking a pitch rejected, but even then the UI should show the exact diff first.

### Pitch approval writes

Approving a pitch should update the pitch front matter:

- `status: approved`
- `approved_by: silas`
- `approved_at: <iso timestamp>`

If the pitch requires a new roadmap task, the portal should propose a second diff that adds a `ready` task to the target project's `roadmap.yaml`. That task creation should be a PR, not a direct commit.

Rejecting a pitch should update:

- `status: rejected`
- `rejected_by: silas`
- `rejected_at: <iso timestamp>`
- optional `decision_note`

### Roadmap task writes

Roadmap writes should be minimal and preserve task identity.

Supported writes:

- Set `approved_by_human: true` and `status: done` for a gated task Silas approves.
- Set `status: ready` and increment `passes` when work needs another Worker attempt.
- Set `status: blocked` when the pass budget is exhausted.
- Add a new scoped task when a PR discovers out-of-scope follow-up work.

The portal should not silently reorder tasks or rewrite whole roadmap files unless the parser can preserve formatting safely. If formatting preservation is not reliable, the UI should warn that YAML will be normalized.

### PR actions

PR actions should use GitHub APIs where possible:

- Comment on a PR.
- Request changes or approve via review.
- Enable auto-merge only when the PR is safe, mergeable, and checks are acceptable.
- Never manually merge from the portal until Silas has explicitly approved that capability.

### Rollback writes

Rollback should open a branch and PR containing a normal revert commit. The portal must show:

- Original PR or commit.
- Files touched.
- Expected revert branch name.
- Any conflict or missing context.

No force-push, no hard reset, no direct mutation of protected branches.

## API shape for m1

Suggested local routes:

- `GET /api/projects` returns active project summaries.
- `GET /api/projects/:slug` returns roadmap, CONTROL direction, milestones, and tasks.
- `GET /api/pitches` returns parsed pitch metadata and body excerpts.
- `GET /api/pull-requests` returns open PR summaries from GitHub.
- `GET /api/status` returns read-only STATUS.md summary if useful.

All routes should return `{ success, data }` or `{ success, message }` shapes. No write routes in m1.

## Data model for the UI

Project summary:

- slug
- kind
- override status
- priority rank
- progress percent
- milestone counts
- task counts by status
- ready task count
- needs-human count
- review count

Task summary:

- id
- title
- milestone
- status
- owner
- updated
- passes
- stakes
- depends_on
- gate_human
- approved_by_human
- note

Pitch summary:

- slug
- title
- date
- project-target
- status
- rough effort
- suggested first task
- body excerpt

PR summary:

- number
- title
- branch
- base
- author
- state
- draft
- mergeability
- check status
- project/task guess
- URL

## Safety boundaries

The portal must not:

- Touch DNS.
- Touch billing or payment systems.
- Deploy anything.
- Send emails, publish posts, create listings, or trigger ads.
- Store secrets in the repo.
- Modify the Kind Robots shared backend from this project.
- Invent tasks that bypass roadmap dependency gates.

When in doubt, the portal should generate a proposed PR and mark the relevant roadmap task `needs-human`.

## Acceptance criteria for m1

Silas should be able to run the app locally and see:

- Active projects in priority order.
- Project progress and task status breakdowns.
- A detail page for each project with milestones and task gates.
- Awaiting pitch queue.
- Open worker PR queue.
- No write buttons and no deploy path.

## Open decisions for Silas

1. Should m2 pitch approve/reject write directly to `main`, or always via PR?
2. Should the portal live only inside Conductor, or eventually become a Kind Robots workspace app that reads Conductor remotely?
3. Should single-user auth use GitHub OAuth, a local password, or an Authelia-protected route?
4. Should PR merge actions remain outside the portal until after rollback is proven?
