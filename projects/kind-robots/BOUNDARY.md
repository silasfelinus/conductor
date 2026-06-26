# Kind Robots app/backend boundary

## Purpose

This project is for app-owned Kind Robots work that can be developed safely inside the Conductor loop without changing the existing shared Kind Robots backend or production deployment. The shared backend stays the source of current production behavior; this project defines what a new app layer may own, what it may consume, and where future work must become a pitch or human-gated task.

## Boundary principle

The app may build local UI, orchestration, workspace flows, and project-specific adapters. It must not modify the existing Kind Robots production backend, database schema, billing logic, generation endpoints, auth system, or deployment infrastructure from this repository. When a feature appears to require a shared backend change, the Worker should write a pitch under `pitches/` instead of editing the external system.

## App-owned concerns

The Kind Robots app can own these concerns inside `projects/kind-robots/`:

- Local app shell, screens, routes, and workspace UI experiments.
- Project-specific documentation, specs, tasks, and roadmap planning.
- Read-only adapters that consume published/shared APIs.
- Local mock data and fixtures for development.
- UI state, view models, Pinia stores, and client-side interaction flows.
- App-specific validation and display logic that does not alter shared backend contracts.
- Draft-only workflows for review, approval, or human handoff.
- Integration notes that document what the shared backend already provides.

## Shared backend concerns consumed as external services

The app should treat these as read-only external capabilities unless Silas explicitly approves a separate task in the owning repo:

- Authentication and account identity.
- Core user records and production data models.
- Art, image, and text generation endpoints.
- Mana, credits, subscriptions, billing, and payment status.
- Existing bot, character, gallery, art, pitch sheet, and chat APIs.
- Production database migrations and Prisma schema changes.
- Email, publishing, deployment, DNS, secrets, and billing infrastructure.

## Auth boundary

For early local prototypes, auth may be represented with a single-user mock or a documented placeholder. The app should not create a competing auth model. A production auth plan must explain how it delegates to the existing Kind Robots identity system or why a separate flow is needed, and that plan should be human-gated before implementation.

## Data model boundary

The app may define local TypeScript types for display and validation, but those types should mirror external contracts rather than redefine production truth. It may store mock fixtures for local development. It must not add production Prisma models, alter shared migrations, or assume direct write access to Kind Robots data.

When a missing model or field is discovered, create a proposal describing the desired backend change, the owning repo, migration risk, and the smallest safe rollout path.

## Generation endpoint boundary

The app may call or mock existing generation endpoints through documented adapters. It should not introduce new production generation routes, model routing, queue behavior, cost accounting, or provider configuration from this project. Changes that affect generation cost, model selection, safety, or public output should become human-gated pitches.

## Mana and billing boundary

Mana, credits, subscriptions, payment status, and spending limits are external source-of-truth concerns. This project may show balances returned by existing APIs and may design UI for draft purchase or upgrade flows, but it must not trigger payments, change balances, update subscription state, or spend money. Any billing-related mutation is irreversible enough to require explicit human approval and likely belongs in the shared backend repo.

## Allowed first roadmap after approval

A safe first build sequence after Silas approves this boundary would be:

1. Read-only workspace dashboard using local fixtures that match existing API shapes.
2. Adapter layer that fetches existing public/authenticated API data without writes.
3. UI flows for approvals and generation requests that stop at draft/handoff state.
4. Human-gated write strategy for any action that changes production data.
5. Separate pitches for any required shared backend changes.

## Escalation triggers

Set the task or pitch to `needs-human` before proceeding when work involves:

- Production data writes.
- Prisma migrations or shared schema edits.
- Auth/session/token changes.
- Billing, credits, subscriptions, payments, or ad spend.
- DNS, deploys, secrets, environment variables, or infrastructure provisioning.
- Publishing, sending, posting, or exposing content publicly.
- Any change that must happen in `silasfelinus/kind_robots` or another external repo.

## Reviewer checklist

Before approving future Kind Robots app tasks, confirm that the PR:

- Stays inside `projects/kind-robots/` unless the task explicitly allows otherwise.
- Uses mock or read-only data unless a human-gated write task was approved.
- Does not modify shared backend contracts or production infrastructure.
- Documents any required external backend change as a pitch instead of silently implementing it.
- Leaves deploys, DNS, secrets, sends, publishing, and billing untouched.
