# Superkate Services Calculator — Customer Database and Cloud Sync Architecture

Date: 2026-07-06  
Task: `superkate-services-calculator/t-010`  
Status: pre-implementation decision record

## Purpose

This note selects the customer database, appointment storage, cloud sync approach, auth/tenant model, conflict handling, backup/export path, and optional app/device lock approach for the Superkate Services Calculator before appointment persistence work begins.

The goal is a private, local-first appointment calculator that is safe enough for customer names, optional customer email addresses, appointment pricing, and receipt preparation without turning the MVP into enterprise beige spreadsheet purgatory.

## Selected architecture

Use a **local-first app database plus authenticated cloud sync**.

The MVP should persist customer and appointment history locally first so Superkate can work during or after appointments even when connectivity is flaky. Cloud sync should be designed as a beta requirement from the start, not bolted on later. Local data remains the source of the active UI experience; the server is the sync authority for cross-device recovery and backup.

Recommended shape:

- Local app database: SQLite-backed storage for mobile/desktop app targets, or IndexedDB only for a web-only prototype.
- Server sync API: Kind Robots-owned API routes or the eventual app-owned service layer, with authenticated access and per-user/per-business authorization.
- Records: `Customer` and `Appointment`, using the fields already approved in `SPEC.md`.
- Money/time: store money as cents and time as minutes; calculate totals from stored values.
- Receipts: user-reviewed email composer only; no backend direct-send in beta.

## Local database decision

For a paid or customer-data beta, do **not** use `localStorage` for appointment history. It is too fragile for structured customer data and too easy to misuse.

Use a real local persistence layer:

- For a Flutter/conductor-app path: SQLite through the platform-supported SQLite package.
- For a Nuxt/web prototype: IndexedDB through a typed wrapper, with a clear migration path to SQLite if packaged later.
- For any server-backed beta: Prisma models on the server side can mirror the same canonical fields, but the client should still keep local pending changes until synced.

Local tables/collections:

```txt
Customer
- id
- name
- email
- createdAt
- updatedAt
- deletedAt?          # tombstone for sync deletion propagation
- syncVersion
- syncedAt?

Appointment
- id
- customerId?
- clientNameSnapshot
- appointmentDate
- hourlyRateCents
- timeSpentMinutes
- productCostCents
- appointmentTotalCents
- createdAt
- updatedAt
- deletedAt?          # tombstone for sync deletion propagation
- syncVersion
- syncedAt?
```

Keep `clientNameSnapshot` on appointments so older receipts stay readable if a customer profile changes later.

## Auth and tenant model

The cloud sync model should assume a single business owner at first, but avoid hardcoding that assumption into unsafe route behavior.

Recommended tenant shape:

- `userId`: the authenticated Kind Robots user who owns the data.
- `businessSlug`: default `hair-by-superkate` or equivalent business identifier.
- Every cloud-synced customer and appointment belongs to both `userId` and `businessSlug`.
- Every API route checks authenticated user identity before returning, creating, updating, deleting, or exporting records.

For beta, one user and one business is enough. The important part is that every synced row has an ownership boundary so future multi-device or family/staff access does not require a risky rewrite.

## Sync approach

Use timestamp/version based incremental sync with tombstones.

Each local record should track:

- `id`: stable UUID generated client-side.
- `updatedAt`: last local edit time.
- `syncVersion`: monotonic server version or revision number returned by the server.
- `syncedAt`: when the local client last confirmed server acceptance.
- `deletedAt`: nullable deletion marker for deletion propagation.

Basic flow:

1. User edits locally.
2. App marks the record dirty by updating `updatedAt` and clearing or aging `syncedAt`.
3. Sync pushes dirty records to authenticated API routes.
4. Server validates fields, checks ownership, stores the row, increments `syncVersion`, and returns accepted records.
5. Client pulls remote records changed since the last sync cursor.
6. Client applies remote changes unless there is a local conflict.
7. UI shows synced, offline, pending changes, or sync error states without exposing customer data in logs.

## Conflict strategy

Use **last-write-wins with visible conflict safety** for beta.

For this app, appointment records are usually entered by one person on one device at a time. A complex merge UI would be overkill. Still, avoid silent data loss where possible:

- If the same record changed locally and remotely since last sync, keep the newest `updatedAt` version as active.
- Preserve the overwritten version in a local conflict log or lightweight recovery table for debugging/recovery.
- Surface a calm sync message like “Some older edits were replaced by newer saved changes” without showing private customer details.
- Prefer appointment-specific edits over customer-profile edits for receipt history because appointment snapshots are historical facts.

Deletions use tombstones so a deleted customer or appointment is removed on other devices instead of resurrected by stale clients.

## Backup and export path

Paid v1 should include CSV export for customers and appointments.

Minimum export expectations:

- Customer CSV: `id`, `name`, `email`, `createdAt`, `updatedAt`.
- Appointment CSV: `id`, `customerId`, `clientNameSnapshot`, `appointmentDate`, `hourlyRateCents`, `timeSpentMinutes`, `productCostCents`, `appointmentTotalCents`, `createdAt`, `updatedAt`.
- Export should be initiated by the authenticated user only.
- Export files should not be automatically emailed or uploaded elsewhere.
- Cloud sync backup should be explained as account-backed recovery, not a public/shared database.

Avoid destructive bulk delete in paid v1. Single appointment delete, customer edit/delete, and deletion propagation are enough.

## App/device lock approach

App lock should be optional and presented during onboarding, then adjustable in settings.

Recommended behavior:

- Ask during onboarding whether to protect saved customer history with device authentication.
- Use platform secure authentication where available: Face ID, Touch ID, passcode, Android biometrics, or OS equivalent.
- Do not store custom lock PINs unless a later security review specifically approves that path.
- Lock access to saved customer/appointment history, export, and settings that reveal customer email.
- The calculator can remain usable for unsaved one-off totals if that does not expose stored history.

## API safety requirements

All sync API routes must:

- Require authenticated access.
- Scope every read/write to the authenticated owner and business slug.
- Validate money as integer cents and time as integer minutes.
- Reject negative time and invalid currency values.
- Avoid logging customer names, emails, receipt text, appointment totals tied to identifiable customers, or raw payloads.
- Use HTTPS-only communication in production.
- Keep email-sending credentials out of the beta because receipts open a user-reviewed composer.

## What t-003 should build next

`t-003` can now implement the customer and appointment data model with persistence using this contract:

- Stable `Customer` and `Appointment` entities.
- Local persistence with dirty/sync metadata.
- Money stored as cents; time stored as minutes.
- Appointment totals calculated from input fields.
- Customer email optional.
- Appointment `clientNameSnapshot` required.
- No backend direct-send receipt behavior.
- No bulk delete.
- No customer-data logging.

## Open decisions to collect before paid release

These do not block t-003, but they should be collected before a paid handoff:

- Exact booking/contact link for receipts.
- Exact preferred reply contact.
- Final app-lock onboarding wording.
- Whether beta ships as web-only first, packaged app first, or both.
- Which account system owns authentication for cloud sync.
