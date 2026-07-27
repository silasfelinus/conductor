# Humboldt Scoop CMS — Real-Address Privacy, Map Costs, and Launch Gates Review

Task: `humboldt-scoop-cms/t-010`. This document reviews the current (dummy-data)
implementation shipped by t-007/t-008/t-009 against what changes the moment real
customer addresses, real crew rollout, or real map-provider billing enter the
system. It does not authorize any of those — per `gate_human: true`, this task
ends at `needs-human` regardless of findings. Nothing here flips a switch; Silas
reviews and decides.

## 1. What exists today (verified against current code)

- **Backend** (`src/`): a Hono HTTP service (`src/server.ts`) serving customers,
  route planning, and a dispatcher map UI, all reading from
  `seedData` (`src/schema.ts`) — static, in-repo dummy fixtures. No database.
  No customer, property, pet, or visit record in this codebase has ever come
  from a real person.
- **Route planning** (`src/routing/`): deterministic only, per the roadmap's own
  "no LLM involvement" rule (`server.ts:167-169`). Two matrix providers:
  `HaversineMatrixProvider` (default — pure great-circle math, zero network
  calls, zero third parties) and `OSRMMatrixProvider` (calls a **self-hosted**
  OSRM instance via `OSRM_BASE_URL`, no API key, no metering — see
  `ops/routing/README.md`). There is no code path to any paid third-party
  routing/geocoding API (Google Maps, Mapbox, OpenRouteService, etc.).
- **Dispatcher map UI** (`GET /dispatch`, `src/dispatchPage.ts`): Leaflet is
  vendored from `node_modules` and served locally (`server.ts:159-165`) —
  no CDN script/style fetch. Map **tiles**, however, come from the public
  OpenStreetMap tile server (`tile.openstreetmap.org`) directly from the
  crew/dispatcher's browser — see "Geocoding/map-provider data handling" below.
- **Route drafts** (`src/routing/drafts.ts`): in-memory `Map`, explicitly
  documented as not surviving a server restart (`drafts.ts:3-8`). Nothing is
  persisted to disk or a database.
- **Field client** (`field_client/`, Flutter/Dart): `RouteStorage` is an
  abstract interface (`route_services.dart:66`) with only a
  `MemoryRouteStorage` implementation wired up today — same "no real
  persistence yet" posture as the backend, by design, to keep Linux/iOS
  ports viable later without committing to a platform-specific store now.
- **OSM extract pipeline** (`ops/routing/fetch-extract.sh`): fetches a
  Humboldt County road-network extract via the public Overpass API
  (`overpass-api.de`) for OSRM's routing graph. This is map/road data, not
  customer data — no customer address ever goes into this fetch.

## 2. Data retention

**Today:** nothing to retain — all customer/property/pet/visit data is
hardcoded dummy fixtures checked into the repo (`src/schema.ts`), and the only
runtime state (route drafts) is in-memory and lost on restart. There is no
retention policy because there is no persisted real data.

**Before real addresses:** this project has no database yet (see `SCHEMA.md`'s
"definition-first model... does not create database migrations"). Before
real customer records exist, Silas needs to decide and document: how long a
cancelled customer's record, past visit history, and crew notes are kept;
whether visit photos (not yet implemented) would ever be retained versus
processed and discarded; and whether route *drafts* (which currently contain
full customer names/addresses/coordinates in-memory) get persisted at all, or
stay intentionally ephemeral post-launch the way they are today.

## 3. Encryption

**Today:** not applicable — no real data exists to encrypt, and there is no
database or disk persistence layer to configure at-rest encryption for.

**Before real addresses:** once a real persistence layer is chosen (`SCHEMA.md`
flags this as open — "map these to database IDs or keep them as external-safe
slugs/UUIDs"), it needs at-rest encryption for the datastore (or full-disk
encryption on the self-hosted box, consistent with this project's
self-hosting posture) and TLS in transit for every hop: dispatcher browser →
CMS API, CMS → self-hosted OSRM/VROOM (currently plain HTTP per
`ops/routing/README.md`'s `http://localhost:5000` — fine on a `--network host`
loopback, not fine if OSRM/VROOM ever move off-box), and field client → CMS
API. None of this is wired up today because none of it is needed for dummy
data on localhost.

## 4. Access roles

**Today:** there is no authentication or authorization anywhere in this
codebase — confirmed by grep across `src/`: no `auth`, `apiKey`, `token`, or
`role`/`permission` handling exists. Every route (`/customers`, `/routes/*`,
`/dispatch`) is open to anyone who can reach the port. This is fine right now
because the service holds only dummy data and (per `STACK.md`'s guardrails)
isn't deployed anywhere public.

**Before real addresses or crew rollout — this is the biggest open gap:**
launch needs at minimum (a) an authenticated dispatcher/admin role for the
`/dispatch` UI and customer-editing routes, and (b) a scoped crew/field-client
credential that can only read *that crew's own* assigned today-route, not the
full customer list — the field client currently has no concept of "which crew
member am I" at all, since it only ever sees the same dummy fixtures. Building
real auth is real implementation work, not just a policy decision, so this
should become its own `ready` task once Silas approves moving toward real
data — it is not something to bolt on silently alongside the first real
customer import.

## 5. Logs

**Today:** the only `console.log` in the backend is the startup banner
(`server.ts:241`, "listening on http://localhost:PORT") — no request logging,
no customer data ever written to stdout/stderr, confirmed by grep. The field
client and dispatcher page have no logging of their own beyond default
framework/browser console noise during development.

**Before real addresses:** if request/access logging is added later (useful
for debugging route-planning issues), it must not log full customer
name/address/coordinate payloads in plaintext to a shared log store — redact
or hash identifying fields, consistent with the existing
`gateDetailsPlaceholder: '[GATE DETAILS REDACTED / ENTERED BY APPROVED HUMAN
WORKFLOW]'` pattern already used for gate codes in `server.ts:78`.

## 6. Geocoding / map-provider data handling

- **Routing/matrix (distance, duration, turn-by-turn):** self-hosted OSRM,
  no data leaves the box (`matrixProvider.ts`). No third party ever sees a
  customer address for this purpose.
- **Map tiles:** the dispatcher UI's Leaflet map pulls visual tile images
  from the public `tile.openstreetmap.org` server directly from the
  dispatcher's browser (`dispatchPage.ts:171`). This means OpenStreetMap's
  tile infrastructure sees the **approximate viewport bounding box** (which
  neighborhood/area the dispatcher is currently looking at) via ordinary
  tile-request HTTP, the same way any site using free OSM tiles works — it
  does **not** receive customer names, addresses, or any CMS data, only tile
  x/y/z coordinates for whatever map area is on-screen. This is the standard,
  free, no-API-key OSM tile usage and matches `STACK.md`'s "no payment
  processor... without explicit approval" guardrail, but Silas should know
  it's an external network call at all, however low-risk.
- **OSM road-network extract:** `fetch-extract.sh` calls the public Overpass
  API (`overpass-api.de`) to download Humboldt County's road network for
  OSRM's own graph-building. This is map/road topology only — it sends a
  bounding box, not any customer data, and only runs on the actual host
  (not reachable from this sandbox, and not part of any request-time path).
- **No other geocoding provider is wired up anywhere in this codebase** —
  there is no forward-geocoding (address → lat/lng) implementation yet at
  all. `RoutePlanRequest` already expects numeric `lat`/`lng` on every stop
  (`server.ts:196-207`), meaning address-to-coordinate conversion is an
  **unbuilt, unapproved step** that would need its own provider decision
  (self-hosted Nominatim vs. a paid geocoder) and its own human gate before
  a single real address is ever typed into this system.

## 7. API billing limits

**Today:** zero paid API surface. OSRM and VROOM are self-hosted with no
metering (`matrixProvider.ts:91-93`: "No API key: this is a self-hosted,
unmetered service, never a paid third-party routing API"). OSM tiles and the
Overpass API are both free, keyless public services. There is nothing to set
a billing limit on because nothing here bills.

**Before real addresses:** if a geocoding step is later approved and it uses
a paid provider (rather than self-hosted Nominatim), that task needs its own
spend cap and needs-human gate per the standing rule in `CLAUDE.md`/
`AGENTS.md` — never wire live billing without explicit approval. If
self-hosted Nominatim is chosen instead, it inherits the same "runs on
Silas's box, unmetered" posture as OSRM/VROOM and this section would not
change.

## 8. Offline behavior

- **Field client:** designed dummy-data-first with an abstracted
  `RouteStorage` interface (`route_services.dart:66`) specifically so a real
  offline-capable store (SQLite, Hive, etc.) can be swapped in later without
  touching the UI or API-calling code — see `t-009`'s note: "Keep provider,
  storage, permissions, and deep-link services abstracted." Today, losing
  connectivity mid-route means losing the in-memory route data on next
  app restart, since nothing persists to disk yet.
- **Dispatcher web UI:** no offline support — it's a live page calling the
  backend on every action (select customers, recalculate, save draft). Not a
  gap for launch review purposes since dispatching happens from a fixed
  location with normal connectivity, per the "Android is the first field-client
  target" framing (the office/dispatcher role isn't the one that needs
  offline resilience — the crew in the field is, and that's `field_client`).

**Before real addresses / crew rollout:** decide whether the field client
needs true offline route caching (crew loses signal mid-neighborhood) before
first real rollout, or whether that's an acceptable v1 gap given Humboldt
County's actual cell coverage. This is a product decision, not a code change
this review can make.

## 9. Deletion / export

**Today:** not applicable in either direction — there is no real customer
data to delete or export, and no persistence layer to build either feature
against yet. Dummy fixtures live in version control (`src/schema.ts`) and
get deleted/replaced the normal way, by editing the file.

**Before real addresses:** once a real persistence layer exists, launch needs
at least: a way to fully delete a customer and all associated
properties/pets/visits/drafts/route-history on request, and a way to export a
customer's own data on request (name, properties, visit history, invoices).
Neither exists today because neither is needed for dummy data — this becomes
its own scoped task once the persistence layer is chosen, since the concrete
shape depends on which datastore Silas picks (`SCHEMA.md` leaves this open).

## Summary — what's actually gating launch

Everything above that reads "before real addresses" in this document is a
**gap, not a red flag** — none of it needed to exist for the dummy-data-only
work this roadmap has authorized so far (`STACK.md`/`SCHEMA.md` guardrails:
"dummy/seed data only until Silas approves real data entry"). The two gaps
that are genuinely bigger than "add a feature later" and should shape *how*
real-data rollout is sequenced, not just what's built:

1. **No authentication/access-role system exists at all.** This is real,
   scoped engineering work (dispatcher/admin auth + scoped crew credentials)
   that should be its own approved task *before* any real customer record is
   entered — not something added quietly alongside the first real import.
2. **No geocoding step exists.** Real addresses can't become the `lat`/`lng`
   this system already expects without picking and approving a
   geocoding provider (self-hosted Nominatim recommended, to stay consistent
   with this project's self-hosted-only posture and avoid a new billing
   surface) — this is also its own task, not a detail to settle mid-import.

FOR SILAS: This document is the requested privacy/cost/launch-gate review
(`humboldt-scoop-cms/t-010`). It found no real customer data, no live
billing, and no undisclosed third-party data flows anywhere in the current
dummy-data implementation — the only external network calls a deployed
instance would make are free/keyless (OSM tiles, Overpass API) and
self-hosted (OSRM/VROOM). To approve moving toward real data, review section
9's two flagged gaps (auth, geocoding) and either approve them as prerequisite
tasks or tell me how you want them sequenced; then this task can be set
`approved_by_human: true` / `status: done`. Real addresses, customer data
import, map-provider billing changes, and crew rollout itself all remain
separate hard needs-human gates regardless — this review does not authorize
any of them.
