# Superkate Services Calculator — Cloud Sync Ownership Decision Note

Date: 2026-07-08  
Task: `superkate-services-calculator/t-023`  
Status: human decision recorded; no production sync implementation

## Purpose

This note records the cloud sync ownership decision for the Superkate Services Calculator before any production sync code is built. The app remains local-first: customer and appointment history should work safely on-device first, with cloud sync added later as account-backed backup/recovery and cross-device continuity.

Silas has chosen the long-term sync direction: **a dedicated Hair by Superkate backend should own sync/auth**, not the Kind Robots backend.

## Current constraints

- First app target is Android.
- Customer names, optional email addresses, appointment prices, and receipt context are sensitive customer data.
- Receipts remain user-reviewed local email drafts; no backend direct-send receipts in beta.
- Silas can self-host on Unraid and already runs Postgres/MariaDB for Hair by Superkate and Kind Robots infrastructure.
- The app is for a real local business, but beta should avoid public deploys, app-store submission, analytics, billing, and production customer-data sync until explicitly approved.

## Decision

Use a **dedicated Hair by Superkate backend** for eventual cloud sync and authentication.

That means:

```txt
Owner/auth: dedicated Hair by Superkate backend
Business scope: first-class single business tenant
Database: self-hosted Postgres or MariaDB on Unraid
Client model: local-first SQLite with authenticated incremental sync
Immediate beta: local-only Android until durable persistence/export/app-lock are safe
```

This keeps salon customer data in salon-specific infrastructure instead of mixing it into Kind Robots project/Dream/gallery/admin surfaces.

## Why this direction

A separate backend costs more setup, but it gives the cleanest business boundary:

- Salon customer data lives in salon-owned infrastructure.
- Future staff access can be designed around the business instead of broad Kind Robots accounts.
- Business backups, retention, restore, and incident response can be documented specifically for Hair by Superkate.
- The app can grow into a private salon operations tool without inheriting unrelated product assumptions.

## Implementation sequence

Do not jump straight to production sync. Build in this order:

1. Finish durable local SQLite persistence.
2. Add customer edit/delete, appointment delete, CSV export, and optional app/device lock.
3. Keep local records sync-ready with stable IDs, timestamps, tombstones, and version fields.
4. Scaffold the dedicated backend locally or in-repo without secrets, DNS, deploys, or production data.
5. Define the sync contract and database schema.
6. Add authenticated sync only after the local app and backend contract are testable with fake data.
7. Handle deployment, DNS, secrets, backups, and real customer data as explicit later human-gated tasks.

## Backend shape

The dedicated backend should start small:

- Health check endpoint.
- Auth/session placeholder or documented auth boundary.
- Customer model/table.
- Appointment model/table.
- Incremental sync contract.
- Tombstone-aware deletes.
- Basic automated tests.
- No direct-send receipt email.
- No analytics over customer data.
- No public admin dashboard yet.

Every synced row should include at least:

```txt
ownerId
businessSlug
id
createdAt
updatedAt
deletedAt?
syncVersion
```

Use `businessSlug = hair-by-superkate` even if the backend starts as a single-business service. That keeps the schema explicit and avoids accidental global reads/writes.

## Tenant and authorization requirements

- Every customer and appointment row belongs to one authenticated owner.
- Every row includes a business scope, initially `hair-by-superkate`.
- Reads, writes, deletes, exports, and sync pulls must filter by owner and business scope.
- Delete flows should use tombstones for sync propagation.
- Appointment history should preserve `clientNameSnapshot` even if a customer profile changes or is deleted.
- Server routes must validate money as integer cents and time as integer minutes.
- Logs must not include customer names, email addresses, receipt bodies, or identifiable appointment totals.

## Backup and restore expectations

Minimum before real customer sync:

- Database backups exist and are restorable.
- Restore process is documented in plain language.
- CSV export remains available from the app as a user-initiated escape hatch.
- Export files are not automatically emailed or uploaded.
- Cloud sync is described to users as private account recovery/sync, not a public shared customer database.

## What not to build yet

Do not build these until explicitly approved:

- Production sync against real customer data.
- Backend direct-send receipt email.
- Staff/shared-account access.
- Public admin dashboard.
- Analytics over customer data.
- App-store/TestFlight/Play Store distribution.
- Billing/subscription gates.
- DNS, secrets, or deploy changes.

## Next roadmap tasks

The next safe tasks are:

1. Document the dedicated backend contract and schema.
2. Scaffold a local/test-only backend surface with fake-data tests.
3. Add app-side sync client interfaces without enabling production sync.
4. Add human-gated deploy/secrets/backups tasks only after fake-data sync passes locally.
