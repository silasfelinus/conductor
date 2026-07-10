# SyncEngine Design Note

Date: 2026-07-10
Task: `superkate-services-calculator/t-032`
Status: design note — no live endpoint, no production sync (t-030 gates unchanged)
Builds on: `docs/backend-api-schema-contract.md` (t-027), `lib/sync/` client interfaces (t-029)

## What exists today

- **Local storage** (`sqlite_persistence_service.dart`, schema v1): `customers`
  (id, name, email, created_at, updated_at) and `appointments` (…, synced_at).
  Customers have no `synced_at`; neither table has `server_id`.
- **Deletes are physical.** `deleteCustomer` removes the row and detaches its
  appointments in one transaction; `deleteAppointment` removes the row. Nothing
  records that a deletion happened — but the sync contract propagates deletions
  as `deletedAt` tombstone upserts.
- **Sync boundary** (`lib/sync/`): `SuperkateSyncClient` (bootstrap → push →
  pull with a `serverVersion` cursor), wire records with `localId`/`serverId`
  and tombstones, `FakeSyncClient` for tests, `DisabledSyncClient` as the
  production default.

The SyncEngine is the missing piece between the two: it decides *what* is
dirty, *when* to talk to the client interface, and *how* results flow back
into local storage and the UI's `SyncStatus`.

## Design decisions

### 1. Dirty tracking: per-row watermark, not a dirty flag

A row is dirty when `synced_at IS NULL OR updated_at > synced_at`.

- No new write paths: every existing edit already bumps `updated_at`, so
  nothing can forget to set a flag.
- Schema delta (v2 migration): add `synced_at TEXT` and `server_id TEXT` to
  `customers`; add `server_id TEXT` to `appointments` (it already has
  `synced_at`).
- On push ack, the engine writes `synced_at = ack.syncedAt` and
  `server_id = ack.serverId`. Local IDs remain the UI keys (contract rule).

### 2. Deletions: outbox table, not soft-delete columns

Add a `sync_outbox` table instead of `deleted_at` columns on live tables:

```sql
CREATE TABLE sync_outbox (
  entity     TEXT NOT NULL,   -- 'customer' | 'appointment'
  local_id   TEXT NOT NULL,
  server_id  TEXT,
  deleted_at TEXT NOT NULL,
  PRIMARY KEY (entity, local_id)
)
```

- `deleteCustomer` / `deleteAppointment` insert an outbox row inside their
  existing transactions; every list/search query stays untouched (no
  `WHERE deleted_at IS NULL` sprinkled everywhere — the row is really gone
  locally, exactly as the app behaves today).
- Push sends outbox rows as tombstone records (`deletedAt` set). On ack the
  outbox row is cleared. Rows never synced (no `server_id`, never pushed)
  can be dropped from the outbox without a network round-trip.
- The customer-delete detach rule stays local-only mechanics; the server
  contract already guarantees appointments survive customer deletion.

### 3. Pull application: LWW with a local-edit guard

Engine stores `last_server_version` in a one-row `sync_state` table. Pull
`afterVersion=last_server_version`, then per record:

1. **Tombstone** → delete the local row (and detach, for customers) unless the
   local row is dirty and newer than the tombstone's `updatedAt` — then keep
   the local row; the next push re-creates it server-side (contract accepts a
   newer upsert after a tombstone as a new revision).
2. **Upsert, no local row** → insert with `server_id`, `synced_at`.
3. **Upsert, local row clean** → overwrite.
4. **Upsert, local row dirty** → keep local if its `updatedAt` is newer
   (server will accept it on next push); otherwise take the server row and
   drop the local edit (it lost LWW — same rule the server applies).

Apply pulls in one transaction per batch; update `last_server_version` only
after the batch commits.

### 4. Loop order and triggers

One sync pass = `push` then `pull` (push first so LWW conflicts surface as
push rejections, which carry the server row for immediate reconciliation).

Beta triggers, in order of preference:
- manual "Sync now" action;
- app-open/app-resume when sync is enabled and the device is online.

No background timers, no silent retries: on failure set
`SyncStatus.offline` (transport error) or `SyncStatus.error` (server
rejection), keep everything local, and let the next trigger try again.
A single retry with ~2s backoff on transport errors is acceptable; anything
more belongs after the beta.

### 5. SyncStatus mapping (SPEC "Sync / Account Status")

```
disabled        client.isSyncAvailable == false (today: always)
idle            last pass clean, nothing dirty, outbox empty
pendingChanges  any dirty row or outbox row exists
syncing         a pass is in flight
offline         last pass failed on transport
error           last pass had rejections needing attention
```

Status copy must never include customer names/emails (contract logging rule).

## What the engine is NOT allowed to do (unchanged gates)

- No live endpoint, secrets, or real customer-data upload — the engine is
  built and tested against `FakeSyncClient` only, and `DisabledSyncClient`
  stays the wired-in default until Silas clears t-030's production gates.
- No analytics, no direct email send, no background network activity.

## Implementation order (future tasks, each small and reversible)

1. Schema v2 migration + outbox writes in the two delete paths (pure local,
   testable with the existing sqlite test setup).
2. `SyncEngine` with push pass against `FakeSyncClient` (dirty scan, acks,
   outbox clearing).
3. Pull pass + `sync_state` cursor + LWW application rules.
4. `SyncStatus` wiring + a status chip and manual "Sync now" in settings —
   visible but inert while the client is `DisabledSyncClient`.
