# Hair by Superkate Backend API and Schema Contract

Date: 2026-07-08  
Task: `superkate-services-calculator/t-027`  
Status: implementation contract  
Scope: fake/local sync contract only; no production deploy, secrets, DNS, billing, analytics, direct-send email, or real customer-data service.

## Purpose

This contract defines the dedicated Hair by Superkate backend shape before any backend scaffold is created. It translates the approved local-first Superkate app model into a small, authenticated sync API that can later run on Silas's self-hosted Postgres/MariaDB-capable Unraid infrastructure.

The immediate Android beta remains local-only. The backend described here is for fake-data/test sync first, then human-gated production planning later.

## Safety boundaries

The backend must not:

- send receipt emails directly;
- store email-provider credentials;
- add analytics or customer-behavior tracking;
- expose public admin pages;
- create production database connections, DNS, deploy settings, or secrets;
- accept unauthenticated customer or appointment reads/writes;
- log raw request payloads, customer names, customer emails, receipt text, or appointment totals tied to identifiable customers.

The backend may:

- run locally with fake/test configuration;
- validate customer and appointment payloads;
- store customer and appointment sync records in a test database;
- return fake-data examples and deterministic sync responses;
- provide a health check that does not reveal customer data.

## Ownership model

Every row belongs to an authenticated owner and one business scope.

Required ownership fields:

| Field | Type | Rule |
| --- | --- | --- |
| `ownerUserId` | string | Authenticated account/user that owns the data. Never accepted from client payload as authority. |
| `businessSlug` | string | Default `hair-by-superkate`; validated server-side. |
| `serverId` | string | Server-generated stable ID. |
| `localId` | string | Client-generated stable UUID from the app. Unique per owner/business/entity. |

Server routes derive `ownerUserId` from auth context. Client-provided owner fields are ignored or rejected.

For beta scaffolding, auth may be a fake local test identity such as `test-owner-superkate`, but the API boundary should already behave as if auth is real.

## Entity model

### Customer

Canonical customer fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `serverId` | string | server | Server-generated ID. |
| `localId` | string | yes | Client UUID; used for local-to-server mapping. |
| `ownerUserId` | string | server | From auth context. |
| `businessSlug` | string | server | Default `hair-by-superkate`. |
| `name` | string | yes | Trimmed, 1-120 chars. |
| `email` | string/null | no | Trimmed lowercase if present; nullable. |
| `createdAt` | ISO datetime | yes | Client-created timestamp accepted after validation. |
| `updatedAt` | ISO datetime | yes | Last client edit time. |
| `deletedAt` | ISO datetime/null | no | Tombstone marker; deletion propagation only. |
| `serverVersion` | integer | server | Monotonic server revision. |
| `syncedAt` | ISO datetime | server | Server acceptance timestamp returned to client. |

Constraints:

- Unique `(ownerUserId, businessSlug, localId)`.
- If `deletedAt` is set, the row remains as a tombstone until the retention window is decided.
- Customer deletion never cascades appointment deletion.
- Customer names should not be written to logs.

### Appointment

Canonical appointment fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `serverId` | string | server | Server-generated ID. |
| `localId` | string | yes | Client UUID; used for local-to-server mapping. |
| `ownerUserId` | string | server | From auth context. |
| `businessSlug` | string | server | Default `hair-by-superkate`. |
| `customerLocalId` | string/null | no | Links to customer by local ID within owner/business scope. |
| `customerServerId` | string/null | server | Optional resolved server link. |
| `clientNameSnapshot` | string | yes | Historical receipt-safe name snapshot. |
| `appointmentDate` | ISO date | yes | Date of service, not necessarily sync date. |
| `hourlyRateCents` | integer | yes | Non-negative integer cents. |
| `timeSpentMinutes` | integer | yes | Non-negative integer minutes. |
| `productCostCents` | integer | yes | Non-negative integer cents; default 0. |
| `appointmentTotalCents` | integer | server/client | Must equal calculated total. |
| `createdAt` | ISO datetime | yes | Client-created timestamp accepted after validation. |
| `updatedAt` | ISO datetime | yes | Last client edit time. |
| `deletedAt` | ISO datetime/null | no | Tombstone marker; no bulk delete in v1. |
| `serverVersion` | integer | server | Monotonic server revision. |
| `syncedAt` | ISO datetime | server | Server acceptance timestamp returned to client. |

Total calculation:

```txt
appointmentTotalCents = round((hourlyRateCents * timeSpentMinutes) / 60) + productCostCents
```

The server must recompute this value. If the client sends a mismatched total, the server should either reject with a validation error or return the corrected computed value. Prefer rejection for sync contract tests so bugs are loud.

Constraints:

- Unique `(ownerUserId, businessSlug, localId)`.
- Appointment history remains readable if a customer is edited or deleted.
- `clientNameSnapshot` is required even when `customerLocalId` is present.
- Appointment deletion is a tombstone update, not a physical delete, during sync.

## Local-to-server ID mapping

The app already owns local UUIDs. The backend adds server IDs without replacing local IDs.

Sync responses should include both IDs:

```json
{
  "entity": "customer",
  "localId": "local-customer-uuid",
  "serverId": "srv_customer_123",
  "serverVersion": 7,
  "syncedAt": "2026-07-08T18:58:17Z"
}
```

Rules:

- Client sends `localId` for every upsert.
- Server creates `serverId` on first accepted upsert.
- Later upserts may include both `localId` and `serverId`; server still scopes by owner/business.
- A `serverId` owned by another user/business must behave as not found/forbidden without leaking existence.
- The app should keep local IDs as the primary UI keys.

## Sync metadata

Each syncable entity uses:

| Field | Purpose |
| --- | --- |
| `updatedAt` | Client-side edit ordering and conflict comparison. |
| `deletedAt` | Tombstone propagation. |
| `serverVersion` | Server monotonic ordering. |
| `syncedAt` | Client-visible accepted timestamp. |
| `syncCursor` | Pull endpoint cursor for changes after a server version/time. |

Server version is the preferred cursor for deterministic tests. Timestamp cursors are acceptable only if precision and ordering are explicitly tested.

## Conflict policy

Use beta-safe last-write-wins with server validation:

1. Server receives upsert with `updatedAt`.
2. Server compares it to the stored row for the same owner/business/local ID.
3. If incoming `updatedAt` is newer, accept and increment `serverVersion`.
4. If incoming `updatedAt` is older, reject with conflict or return the current server row.
5. If timestamps are equal but content differs, prefer server row and return conflict.

Minimum conflict response:

```json
{
  "success": false,
  "code": "CONFLICT",
  "message": "A newer saved version already exists.",
  "serverRecord": {}
}
```

Do not include private customer details in logs when conflicts occur.

## API envelope

All JSON endpoints should use a predictable envelope.

Success:

```json
{
  "success": true,
  "data": {}
}
```

Failure:

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "Time spent must be zero or greater.",
  "fieldErrors": {
    "timeSpentMinutes": "Must be a non-negative integer."
  }
}
```

## Endpoints

Base path for local scaffold examples:

```txt
/api/superkate
```

### GET `/api/superkate/health`

Purpose: local/test health check.

Response:

```json
{
  "success": true,
  "data": {
    "service": "hair-by-superkate-sync",
    "mode": "local-test",
    "database": "available"
  }
}
```

No auth required for local health if it returns no sensitive configuration. Production health must not reveal secrets, database URLs, or counts.

### GET `/api/superkate/sync/bootstrap`

Purpose: return initial fake/test sync settings for authenticated local development.

Auth: required, even if fake local auth.

Response:

```json
{
  "success": true,
  "data": {
    "businessSlug": "hair-by-superkate",
    "ownerUserId": "test-owner-superkate",
    "serverVersion": 0,
    "features": {
      "pushCustomers": true,
      "pushAppointments": true,
      "pullChanges": true,
      "directEmailSend": false,
      "analytics": false
    }
  }
}
```

### POST `/api/superkate/sync/push`

Purpose: accept local dirty customers and appointments.

Auth: required.

Request:

```json
{
  "businessSlug": "hair-by-superkate",
  "customers": [],
  "appointments": []
}
```

Response:

```json
{
  "success": true,
  "data": {
    "accepted": {
      "customers": [],
      "appointments": []
    },
    "rejected": [],
    "serverVersion": 12,
    "syncedAt": "2026-07-08T18:58:17Z"
  }
}
```

Rules:

- Validate every record before writing.
- Accept partial success only if rejected rows are clearly reported.
- Never accept cross-owner or cross-business IDs.
- Recompute appointment totals server-side.
- Treat `deletedAt` as a tombstone upsert.
- No bulk physical delete.

### GET `/api/superkate/sync/pull?businessSlug=hair-by-superkate&afterVersion=0`

Purpose: pull server changes after a cursor.

Auth: required.

Response:

```json
{
  "success": true,
  "data": {
    "customers": [],
    "appointments": [],
    "serverVersion": 12,
    "hasMore": false
  }
}
```

Rules:

- Return only rows owned by authenticated owner and requested business.
- Include tombstones so local clients can mark deleted records.
- Page if needed; do not return unlimited history without a limit.

### POST `/api/superkate/sync/reset-test-data`

Purpose: test-only helper for local scaffold tests.

Auth: required fake test auth.

Rules:

- Available only in local/test mode.
- Must be impossible in production mode.
- Does not exist in production routing unless explicitly gated.

## Validation rules

### Strings

- `name`: trim; 1-120 chars.
- `email`: nullable; trim; lowercase; basic email shape if present; max 254 chars.
- `clientNameSnapshot`: trim; 1-120 chars.
- `businessSlug`: exact `hair-by-superkate` for v1.

### Money

- Store as integer cents.
- Must be finite integer.
- Must be `>= 0`.
- Recommended upper bound for v1 test validation: `<= 1_000_000` cents per field unless Silas changes it.
- No floats in persistence.

### Time

- Store as integer minutes.
- Must be finite integer.
- Must be `>= 0`.
- Recommended upper bound for v1 test validation: `<= 24 * 60`.
- UI may collect hours/minutes, but API stores minutes.

### Dates

- `appointmentDate`: ISO calendar date.
- `createdAt`, `updatedAt`, `deletedAt`, `syncedAt`: ISO datetimes.
- Reject invalid dates.
- Do not require appointment date to be today or future; salon history can be backfilled.

## Fake-data examples

### Customer upsert

```json
{
  "localId": "local-customer-kate-test-1",
  "name": "Test Client",
  "email": "test.client@example.test",
  "createdAt": "2026-07-08T18:00:00Z",
  "updatedAt": "2026-07-08T18:00:00Z",
  "deletedAt": null
}
```

### Appointment upsert

```json
{
  "localId": "local-appt-kate-test-1",
  "customerLocalId": "local-customer-kate-test-1",
  "clientNameSnapshot": "Test Client",
  "appointmentDate": "2026-07-08",
  "hourlyRateCents": 8000,
  "timeSpentMinutes": 90,
  "productCostCents": 1500,
  "appointmentTotalCents": 13500,
  "createdAt": "2026-07-08T18:05:00Z",
  "updatedAt": "2026-07-08T18:05:00Z",
  "deletedAt": null
}
```

Calculation:

```txt
($80.00 * 90 / 60) + $15.00 = $135.00
```

## Implementation guidance for `t-028`

The backend scaffold should start with:

- local/test-only configuration;
- health route;
- fake auth context;
- in-memory or file-backed test database configuration;
- customer and appointment schema/model placeholders matching this contract;
- validation helpers for money, minutes, dates, and business slug;
- sync push/pull route tests;
- no production secrets or deploy hooks.

Recommended first tests:

1. health route returns local-test status without secrets;
2. unauthenticated push/pull is rejected;
3. customer upsert trims name/email and returns server ID/version;
4. appointment upsert recomputes total and rejects mismatches;
5. customer tombstone does not delete appointments;
6. appointment tombstone appears in pull response;
7. cross-business or cross-owner access is rejected;
8. production-only dangerous reset route is unavailable outside local/test mode.

## Open human-gated decisions for later

These do not block fake/local scaffolding:

- final production hostname/subdomain;
- production database engine and backup schedule;
- restore-test process;
- secret storage mechanism;
- account system for real auth;
- whether any future staff/family shared access exists;
- production monitoring boundaries;
- direct-send email, if ever approved as a separate future feature.

Production sync remains blocked by the existing human-gated deployment/secrets/backup planning task.
