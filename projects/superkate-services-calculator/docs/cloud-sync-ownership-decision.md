# Superkate Services Calculator — Cloud Sync Ownership Decision Note

Date: 2026-07-08  
Task: `superkate-services-calculator/t-023`  
Status: decision support; no production sync implementation

## Purpose

This note compares who should own cloud sync for the Superkate Services Calculator before any production sync code is built. The app already has a local-first direction: customer and appointment history should work locally first, with cloud sync added as account-backed backup/recovery and cross-device continuity.

No option below authorizes production sync yet. The next implementation step should stay local-only until Silas chooses the owner/auth path.

## Current constraints

- First app target is Android.
- Customer names, optional email addresses, appointment prices, and receipt context are sensitive customer data.
- Receipts remain user-reviewed local email drafts; no backend direct-send receipts in beta.
- Silas can self-host on Unraid and already runs Postgres/MariaDB for Hair by Superkate and Kind Robots infrastructure.
- The app is for a real local business, but beta should avoid public deploys, app-store submission, analytics, billing, and production customer-data sync until explicitly approved.

## Options

### Option A — Reuse Kind Robots backend/auth

Use Kind Robots as the authenticated sync host. Add Superkate-specific customer and appointment sync routes/models under the existing Kind Robots backend and scope every row to the authenticated owner plus a business slug such as `hair-by-superkate`.

**Best when:** speed and operational simplicity matter most.

**Pros**

- Reuses existing auth/session patterns instead of creating a second account system.
- Reuses existing hosting, API conventions, database access, backups, and monitoring habits.
- Faster to build a private beta because the app can sync against familiar infrastructure.
- Easier for Silas to maintain because there is one central backend brain instead of another tiny service goblin hiding under the stairs.

**Cons**

- Mixes a family/business tool into the broader Kind Robots app boundary.
- Requires extra care so Superkate customer data never leaks into generic project/Dream/gallery/admin surfaces.
- Future staff or business-only access could get awkward if Kind Robots accounts are too broad.
- Any Kind Robots auth or deploy incident can affect the salon sync surface.

**Security shape**

Every synced row should include at least:

```txt
userId
businessSlug
id
createdAt
updatedAt
deletedAt?
syncVersion
```

Every route must require authentication and filter by both `userId` and `businessSlug`. No customer payloads in logs. No analytics events with customer details.

### Option B — Separate Hair by Superkate backend

Create a small dedicated backend/API for Hair by Superkate sync, backed by Silas's self-hosted Postgres or MariaDB. The Superkate app authenticates against that backend instead of Kind Robots.

**Best when:** clean business-data isolation matters more than fastest delivery.

**Pros**

- Stronger product boundary: salon data lives in salon infrastructure.
- Easier to reason about future staff access, business backups, and business-specific retention policy.
- Can choose a minimal auth model just for Superkate instead of inheriting Kind Robots account assumptions.
- Cleaner if this app grows into a real paid/private salon tool.

**Cons**

- More setup: auth, API routes, database migrations, backups, SSL/proxy, monitoring, and incident recovery.
- More things to patch and remember exist.
- Slower beta unless the service is kept extremely small.
- Risk of underbuilding auth/backup discipline if treated as a quick side service.

**Security shape**

Use the same data ownership model as Option A, but with a service-level owner/business table from day one. Even if Superkate is the only tenant, do not hardcode global reads/writes.

### Option C — Local-only beta with manual backup/export first

Delay cloud sync and ship a local-first beta with durable SQLite, optional app/device lock, and CSV export before adding any server sync.

**Best when:** the immediate goal is a safe Android beta without introducing server risk.

**Pros**

- Lowest privacy risk because customer data stays on-device.
- Lets the appointment calculator become useful without solving account ownership now.
- Avoids accidental production data exposure while the app is still taking shape.
- Reduces scope while durable persistence, edit/delete flows, export, and app-lock UX land.

**Cons**

- No cross-device recovery if the device is lost or damaged.
- Manual backups are easy to forget.
- Does not satisfy the long-term cloud sync expectation.
- Later sync needs migration metadata planned now so local records can sync cleanly later.

**Security shape**

Still include sync-ready fields locally: stable UUIDs, `createdAt`, `updatedAt`, `deletedAt`, and optional `syncedAt`/`syncVersion` placeholders. That keeps the eventual sync migration boring, which is the correct vibe for customer data.

## Recommendation

Use **Option C for the immediate Android beta**, while preparing for **Option A unless Silas explicitly wants stronger business isolation**.

That means:

1. Finish durable local SQLite first.
2. Add customer edit/delete, appointment delete, CSV export, and optional app/device lock.
3. Keep records sync-ready with stable IDs, timestamps, tombstones, and version fields.
4. Do not implement production cloud sync until Silas chooses either Kind Robots-owned auth or a separate Hair by Superkate backend.

This gives Superkate a useful private tool sooner while avoiding the classic trap where “just add sync” becomes “congrats, you invented a privacy-sensitive distributed systems problem in a wig.”

## Preferred ownership decision before production sync

If Silas wants the fastest safe path, choose:

```txt
Owner/auth: Kind Robots backend/auth
Business scope: hair-by-superkate
Database: existing Kind Robots database or a clearly separated schema/table namespace
Client model: local-first SQLite with authenticated incremental sync
```

If Silas wants the cleanest long-term business boundary, choose:

```txt
Owner/auth: dedicated Hair by Superkate backend
Business scope: first-class single business tenant
Database: self-hosted Postgres or MariaDB on Unraid
Client model: local-first SQLite with authenticated incremental sync
```

Either path must be picked before production sync implementation begins.

## Tenant and authorization requirements

Regardless of backend owner:

- Every customer and appointment row belongs to one authenticated owner.
- Every row includes a business scope, initially `hair-by-superkate`.
- Reads, writes, deletes, exports, and sync pulls must filter by owner and business scope.
- Delete flows should use tombstones for sync propagation.
- Appointment history should preserve `clientNameSnapshot` even if a customer profile changes or is deleted.
- Server routes must validate money as integer cents and time as integer minutes.
- Logs must not include customer names, email addresses, receipt bodies, or identifiable appointment totals.

## Backup and restore expectations

Minimum before real customer sync:

- Database backups exist and are restorable, not merely “probably somewhere on the server,” the haunted classic.
- Restore process is documented in plain language.
- CSV export remains available from the app as a user-initiated escape hatch.
- Export files are not automatically emailed or uploaded.
- Cloud sync is described to users as private account recovery/sync, not a public shared customer database.

## What not to build yet

Do not build these until explicitly approved:

- Production sync API routes.
- Backend direct-send receipt email.
- Staff/shared-account access.
- Public admin dashboard.
- Analytics over customer data.
- App-store/TestFlight/Play Store distribution.
- Billing/subscription gates.
- DNS, secrets, or deploy changes.

## Decision needed from Silas

Before production sync begins, choose one:

1. **Kind Robots owns sync/auth** — fastest beta path, shared infrastructure, tighter route isolation required.
2. **Hair by Superkate owns sync/auth** — cleaner business boundary, more setup and maintenance.
3. **Local-only beta first** — safest immediate Android beta; revisit sync after persistence/export/app-lock are proven.

Recommended default: **local-only beta first, then Kind Robots-owned sync/auth for the first private cloud beta** unless Silas wants a dedicated Hair by Superkate backend from the start.
