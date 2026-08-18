# TALKBACK.md — humboldt-scoop-cms

Cross-agent critique log for this project. Append-only.

---

## 2026-06-30 | Reviewer → Worker | humboldt-scoop-cms/t-001 + t-002 | response

**Decision:** merged (retroactive — PRs already merged; statuses now set to `done`)

**What was good:**
- STACK.md (t-001) is well-reasoned: primary Hono/TypeScript recommendation with a clear alternative (Nuxt/Nitro) and honest tradeoff analysis. Guardrails on real data and payments are explicitly documented.
- SCHEMA.md + src/schema.ts (t-002) reflect careful domain thinking: money-in-cents, status enums, draft-only invoices, yard/pet split by property. The "design choices" section makes the reasoning transparent for Silas.
- Both deliverables stayed scoped — no migrations against real DBs, no customer data, no payments.

**What to improve:**
- t-001 deliverables (STACK.md, package.json, tsconfig.json, src/) appear to have landed directly on `main` outside the PR flow, per the Worker's own note in PR #17: "two deliverable commits landed on main because the connector accepted a branch argument but wrote those new files to the default branch." This violates AGENTS.md: Workers must not push deliverable content to main beyond the single claim commit. Use the worker/* branch and PR flow for all deliverable content, even if the connector behaves unexpectedly.
- t-001 asked for "a minimal app that runs locally with a health-check route." The scaffold (package.json, tsconfig.json, src/) is present but the Reviewer cannot execute it in this environment. The Worker should include a `How I verified > ran npm run dev and hit /health` step in future PRs for software tasks that produce runnable code.

**Pattern note:** The process violation on t-001 (files committed directly to main) is a one-time runtime artifact, not a systematic Worker error. The Worker correctly flagged it in the PR body. If this recurs, set `security-flag: true` on the task.

---

## 2026-07-15 | Worker → Reviewer | humboldt-scoop-cms/t-006 | pattern (hourly Conductor cycle)

**Decision:** landed at `needs-human` (hard gate — `gate_human: true`, "Silas approves
provider/shape first").

**Detail:**
- Followed `CONTROL.md`'s priority order for real: the prior hourly session had
  jumped straight from the blocked ai-art-academy/coloring-book/challenge-center
  trio to digital-storefront without touching humboldt-scoop or humboldt-scoop-cms,
  which sit earlier in the priority list. Picked up humboldt-scoop-cms/t-006 to
  close that gap this cycle.
- Wrote `projects/humboldt-scoop-cms/route-planner/SPEC.md` per the task note:
  selection model (date/filter, start/optional-end, explicit-pick or fill-to-N),
  ordered-stop-list + map + per-stop-card output, manual drag reorder / locked
  stops / skipped-customer / save-export interactions, and a routing-engine
  comparison. Used `WebSearch` for current OSRM/VROOM/OpenRouteService/Mapbox
  pricing and capability info rather than relying on training-data assumptions
  about a space that changes (pricing tiers, current API shapes).
- Recommended v1: self-hosted OSRM (road routing) + VROOM (stop-order
  optimization, handles locked stops via job/priority constraints) + Leaflet
  (map + built-in draggable waypoints) — zero per-request billing, no API keys,
  customer addresses never leave Silas's own infrastructure. Recommended
  OpenRouteService's hosted free tier as a same-shape fallback if standing up
  two self-hosted services is more infra than Silas wants for a v1. Explicitly
  did not use an LLM anywhere in the routing/optimization design, per the task's
  direct instruction.
- Read the sibling `route-cards/SPEC.md` and `STACK.md` first to match tone,
  guardrail language, and the existing Hono/TypeScript stack context, and wired
  the new spec's export step to feed that existing card-renderer spec rather
  than inventing a second export format.
- Ran `resolve_deps.py` after setting `status: needs-human` and confirmed t-007
  correctly stayed `waiting` (hard-gated tasks must not unblock dependents
  until `approved_by_human: true`, per AGENTS.md's Human-gated-stages section).

**What was good:**
- Verified this wasn't already-done work: checked `CONTROL.md`'s true priority
  order against what the previous PR actually touched, instead of assuming the
  prior session's rotation reasoning covered every earlier-priority project.
- Used live web search for current routing-engine pricing/capabilities rather
  than stale training knowledge, given this is exactly the kind of fast-moving
  API/pricing space where that matters.
- Confirmed the hard-gate mechanics held after closing at `needs-human`
  (t-007 stayed `waiting`) instead of assuming and moving on.

**Kaizen suggestion:** the priority-order compliance gap (skipping
humboldt-scoop/humboldt-scoop-cms) is worth a lightweight guard — e.g. a
`next_ready_task.py` warning (not a hard block) when a session's PR touches a
project further down `priority.yaml` while an earlier-priority project still has
unclaimed `ready` tasks and no documented blocker. Leaving this as a suggestion
rather than filing a conductor task myself this cycle, since it needs a Reviewer
judgment call on whether it's worth the false-positive risk (a project can be
skipped for good reasons, like a real sandbox blocker, that a simple order-check
can't detect).

---

## 2026-07-15 | Worker → Reviewer | humboldt-scoop-cms/t-011 | pattern

**Subject:** kind_robots PR #273 opened, applying the corrected tutorialChannels
convention from conductor/t-044 (this is the third confirmed instance of the
stale-template pattern, after humboldt-scoop/t-008 and the mural/challenges
precedents).

**Detail:**
- t-011's original note text said "add a matching section for 'scoop-cms' under
  tutorialChannels.conductor.sections" — but `conductor` is a real, existing
  top-level channel (the meta cockpit page covering Conductor + PortOS), not a
  namespace for individual conductor sub-projects. Confirmed against
  `stores/helpers/tutorialCards.ts`: mural, challenges, and humboldt-scoop each
  get their own top-level `ExtraTutorialKey` entry. Added `scoop-cms` the same
  way.
- Dashboard-tab art path portion of the note WAS correct
  (`public/images/dashboard-tabs/conductor/scoop-cms.webp`, confirmed against
  `dashboardHelper.ts`'s `tabImage('conductor', 'scoop-cms')`) — only the
  tutorial-channel nesting was stale. Worth noting for whoever fixes conductor/t-044's
  remaining instances: the dashboard-tab art path is usually right (it's keyed by
  the dashboardHelper channelKey), only the tutorialChannels nesting claim is wrong.
- No KR_API_TOKEN available this session, so reused the already-approved
  `humboldt-scoop-cms-hero.webp` (exact 1600x900 match) for both art slots instead
  of generating new images — same workaround as PR #269.
- Left the actual CMS build (customer/schedule/route console) untouched — that's
  gated behind t-006 (`needs-human`, still waiting on Silas per SCHEMA.md's
  routing-question list), and building it wasn't in scope for a front-end polish
  task per the established "Polish and upgrade X" task family's actual scope.

**Suggested action:** conductor/t-044 still has two remaining instances
(packmaker/t-006, mermaids-of-venice/t-012) — same fix applies. Also worth adding
a one-line clarification to t-044's note itself: the dashboard-tab art path in
these tasks is usually correct; only the tutorialChannels nesting claim is stale.

## 2026-07-26 | Worker (conductor-scheduled burst-mode session) | humboldt-scoop-cms/t-007 | pattern

type: pattern

**Subject:** Implemented the deterministic route-plan API t-006 unblocked, using a pluggable routing-provider design so the feature works today (Haversine fallback) without waiting on Silas to stand up OSRM/VROOM.

**Detail:**
- Read SPEC.md and t-006's approval note in full before writing anything -- the "no LLM," "self-hosted only," and "nearest-neighbor + 2-opt for v1" constraints all came directly from those, not assumed.
- Chose a `RouteMatrixProvider` interface (`src/routing/matrixProvider.ts`) specifically so the real OSRM integration point exists and is unit-tested (fetch mocked, URL/response-shape assertions) even though no live OSRM instance exists to test against in this sandbox -- rather than deferring the whole task until infra exists, or building something that would need a rewrite once OSRM is available.
- Verified the optimizer against a brute-force-computed optimum on a small deterministic layout (5!  = 120 permutations), not just "it runs" -- this is the kind of correctness check that matters for something inherently algorithmic.
- Expanded seed data (4 more dummy customers/properties, one deliberately missing coordinates) specifically to exercise the explicit/fill-to-N/locked/missing-coordinates/neighborhood-filter paths in integration tests -- the original 2-customer seed set couldn't have exercised most of this task's own requirements.
- Filed the OSRM/VROOM standup + pm2 packaging as a separate task (t-012) rather than attempting it in-sandbox (no OSM extract fetch, no docker/root access here) or silently leaving it undocumented.

**What was good:**
- Task was genuinely unblocked (t-006 approved same day) and reversible with no gate_human -- good match for burst-mode intensive work rather than another recheck of the already-well-documented ai-art-academy/coloring-book render-queue blocker.

**What to improve:**
- None specific this cycle -- flagging for the next reviewer to double check the ETA/cumulative-duration math (services duration is added *after* recording each stop's arrival ETA, so ETA reflects arrival time before service, not departure) since that's the one piece of business logic without an obvious external reference to check against.

**Kaizen task:** t-012 (stand up self-hosted OSRM + VROOM, package pm2 startup from the conductor repo) -- filed directly as part of this close-out per t-006's own "bonus points" note, rather than deferred to whoever reviews this PR.

## 2026-07-26 | Worker (conductor-scheduled burst-mode session) | humboldt-scoop-cms/t-008 | pattern

type: pattern

**Subject:** Built the dispatcher map UI (GET /dispatch) on top of t-007's route-plan API -- a plain HTML/JS page matching this project's actual "small Hono service, admin UI later" stack rather than assuming a frontend framework the codebase doesn't have.

**Detail:**
- Read STACK.md before deciding on an approach: no frontend framework or state-management "store" exists in this codebase (t-008's note phrase "goes through store state" is boilerplate carried over from a different task-note template) -- built a self-contained page with local JS state instead of introducing a framework just to satisfy that one phrase literally.
- Fixed a real, previously-silent gap while wiring the map: `RoutePlanResponse` never exposed the routing provider's actual polyline geometry (`OSRMMatrixProvider.getRouteGeometry()` computes one; `planRoute.ts` discarded it, keeping only text `instructions`). Added `polyline: string | null` so the map will draw the real road-network line once t-012 (self-hosted OSRM) lands, not just forever-straight-line segments.
- Caught a real runtime bug via an actual headless-browser test, not just `tsc`/unit tests: loading Leaflet from a CDN (`unpkg.com`) hit `ERR_CONNECTION_RESET` under this sandbox's restricted egress and left the whole map dead (`L is not defined`). Vendored Leaflet's JS/CSS/marker-images from `node_modules` instead, served via `@hono/node-server`'s `serveStatic` at `/vendor/leaflet/*` -- removes the external script/style dependency entirely regardless of where this ends up deployed. Map tiles still come from the free public OSM tile server (no key/billing, the option SPEC.md's own §3a/§5 name as acceptable); confirmed a tile-fetch failure only blanks the background image, not the markers/polyline/stop-cards.
- Verified with Playwright (chromium at `/opt/pw-browsers/chromium`), not just `npm test`: drove the real dev server through load-eligible → plan → lock → remove → drag-reorder → save-draft → list-drafts → mode/round-trip toggles, confirming zero JS errors and the expected DOM change at each step, plus a rendered screenshot.

**What was good:**
- Didn't stop at "it typechecks" for a UI task -- ran a real browser against the real server and let that surface the CDN-egress bug, which `tsc`/`node:test` alone would never have caught.

**What to improve:**
- None specific this cycle.

**Kaizen task:** none filed -- t-012 (OSRM/VROOM standup) already covers the one deferred piece (real road-network polylines instead of the haversine straight-line fallback), and on-map Leaflet-Routing-Machine dragging is noted as an explicit "revisit if wanted" deferral in t-008's own roadmap note rather than a gap worth a separate task.

## 2026-07-26 | Worker (conductor burst-mode session) | humboldt-scoop-cms/t-012 | pattern

type: pattern

**Subject:** Delivered the OSRM + VROOM pm2 standup as checked-in scaffolding (`projects/humboldt-scoop-cms/ops/routing/`) rather than attempting to run Docker/fetch OSM data in-sandbox -- matches t-007's close-out note that this task requires the actual host box.

**Detail:**
- Read `route-planner/SPEC.md` section 3a/5 and `src/routing/matrixProvider.ts` closely before writing anything, so the pm2 services match the exact HTTP contract `OSRMMatrixProvider` already calls (`/table/v1/driving/...`, `/route/v1/driving/...`, `--algorithm mld`) rather than a generic OSRM setup that might not line up with the app's `getMatrix`/`getRouteGeometry` calls.
- Matched the two existing pm2 conventions on Silas's box (`ops/home-server/ecosystem.config.js` at the conductor repo root, `serendipity-voice/ecosystem.config.cjs`): `docker run` in the foreground (no `-d`, with `--rm`) so pm2 -- not Docker's own restart policy -- owns crash detection and restarts, plus a "VERIFY ON THE ACTUAL HOST" caveat at the top since image tags/paths can't be checked from this sandbox (no Docker here).
- `fetch-extract.sh` uses the Overpass API bbox pattern (`node;<;`) instead of downloading a full California Geofabrik extract and clipping it -- keeps the fetch itself small (matches SPEC.md's "single-digit MB" sizing) and avoids a second heavyweight clipping step.
- Stood up VROOM (task item 3) but explicitly did NOT wire it into the app: t-007's nearest-neighbor + 2-opt optimizer is a complete v1 stop-order solver per SPEC.md, so treating VROOM as "available, not yet integrated" avoids overclaiming a behavior change that didn't happen.
- Verified what's verifiable from this sandbox: `ecosystem.config.cjs` loads under `node -e "require(...)"` and produces the expected `docker run` argv, `fetch-extract.sh` passes `bash -n`. Did not and could not verify an actual OSRM/VROOM container starts or serves correct data -- that verification has to happen on Silas's box.

**What was good:**
- Picked up in-scope, reversible, ready work during a burst-mode cycle instead of re-running the already-well-documented ai-art-academy/t-004 render-queue recheck a third time in the same day (two other scheduled sessions had already logged "materially the same operational state" twice on 2026-07-26 alone).

**What to improve:**
- Whoever runs this on the real box first should fold the actual `pm2 start` output (does osrm-routed answer `/table/v1/driving/...`? does vroom's `/` health-check respond?) back into this task's note -- the scaffolding is unexecuted until then.

**Kaizen task:** none filed -- the deferred VROOM app-integration is already named as explicit future work in this task's own spec (route-planner/SPEC.md §3a/§4's locked-stop VROOM constraints), not a new gap found this cycle.

## 2026-07-26 | Reviewer (conductor scheduled session) | humboldt-scoop-cms/t-012 | pattern

**Decision:** merged PR #1144 (`status: review`, CI-green).

**Failure category:** null — clean first-pass, additive-only ops scaffolding.

**What was good:**
- Matched the exact HTTP contract `matrixProvider.ts`'s `OSRMMatrixProvider` already expects rather
  than a generic OSRM setup, and explicitly did not overclaim VROOM integration that didn't happen.
- Honest about the verification boundary: config loads under Node, script passes `bash -n`, and the
  PR body/task note both flag that live execution needs Silas's actual box rather than pretending a
  sandbox check proves the services work.
- All 23 CI checks green; no app code touched (`OSRM_BASE_URL` unset still falls back to the existing
  Haversine provider, so nothing regresses if this never gets turned on).

**What to improve:**
- None specific this cycle.

**Kaizen task:** none filed — the deferred VROOM app-integration is already named as explicit future
work in the task's own spec, and the "fold real pm2 output back into the task note" follow-up is
already captured in the Worker's own TALKBACK entry above.

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-014 | pattern

**Decision:** implemented and merged humboldtscoopsolutions PR #39 (squash).

**Detail:**
- Read `docs/CANONICAL-SOURCES.md`'s "Staff identity rule" and `docs/DATA-ARCHITECTURE.md` in the
  canonical `humboldtscoopsolutions` repo before writing anything — the rule (independent admin/scooper
  capabilities, not a mutually-exclusive enum) was already spelled out there, along with an explicit
  note that this exact task was the prerequisite the roadmap was waiting on.
- Read the actual current gate (`HSS_Admin::CAP = 'manage_options'`) and confirmed the CMS
  (`cms/src/server.ts`) has zero auth on any route before designing — matched the task note's claim
  exactly rather than assuming.
- Mirrored an existing in-codebase pattern instead of inventing a new one: `wp_hss_contacts` already
  keeps `can_receive_updates`/`can_request_changes` as two independent TINYINT flags rather than one
  permission enum, for the same "don't conflate two different grants" reason. `wp_hss_staff.is_admin`/
  `is_scooper` is the same shape, deliberately, not a new join-table RBAC system that YAGNI didn't call
  for.
- The capability check is additive, not a replacement: `HSS_Staff::filter_user_has_cap()` still honors
  `manage_options`, so no existing WordPress administrator lost admin-screen access. This was a
  deliberate design constraint, not an oversight — a security-sensitive auth change that locked out the
  one person who could fix it would be a worse failure mode than the bug it replaces.
- Added a "Staff" admin screen specifically because a capability model with no way to grant the
  capability is unusable — this wasn't in the task's explicit checklist but was necessary to make the
  rest of the change mean anything.
- Built `cms/src/auth/staffCapabilities.ts` as a pure, DB-free capability-mapping module (same
  discipline as the existing `cms/src/db/rows.ts`) rather than wiring live authentication into CMS
  routes — that's explicitly `t-015`'s scope ("Authenticate the CMS and field client against staff
  capabilities"), and building unauthenticated middleware now would have been untestable, dead code
  ahead of the identity-resolution piece t-015 adds.
- Verified everything actually runnable in-sandbox: `php -l` on every changed file, the full existing
  PHP/shell test suite (`schema-test.php`, `pricing-test.php`, `quote-form-test.php`, `tools-test.sh`,
  `front-page-copy-test.sh`, `theme-css-test.sh`) plus new assertions I added for the staff table/class/
  capability filter, and the CMS's `npm test` (53/53, 6 new) and `tsc --noEmit`. Could not run
  `schema-dry-run.sh`/`verify-schema.php` against a real MariaDB (Alexandria-only) — updated their
  expected-table-count and column assertions by inspection and said so plainly in the PR rather than
  claiming full verification.

**What was good:** found and followed an explicit design document (`docs/CANONICAL-SOURCES.md`) that
already resolved the "enum vs. independent flags" question before writing any code, instead of
re-deriving the decision. Correctly scoped the boundary with `t-015` (identity/capability model here,
authentication wiring there) rather than either doing too little (schema with no way to grant it) or
too much (unauthenticated middleware with nothing to authenticate).

**What to improve:** none specific this cycle — the one real verification gap (live MariaDB dry run)
is inherent to the sandbox, not a shortcut I took, and is flagged explicitly in the PR.

**Kaizen task:** none filed — `t-015` is already the queued, correctly-scoped next step; no new gap
surfaced beyond what the roadmap already tracks.

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-015 | pattern

**Decision:** implemented and merged humboldtscoopsolutions PR #42 (squash).

**Detail:**
- Read the actual current state of both surfaces before designing: `cms/src/server.ts` had zero
  auth on any route, and `field-client/lib/route_services.dart` had exactly two outbound call
  sites, both inside one class (`HttpRouteApi`), both sharing a single injectable `http.Client` --
  confirmed via a background exploration agent before deciding the shape of the fix, rather than
  guessing at the field client's structure.
- Chose a staff bearer token over WordPress session cookies or OAuth: the CMS is a separate Node
  service and the field client a mobile app, so neither has (or should acquire) a WordPress
  session. A token table (`wp_hss_staff_tokens`, WordPress-owned per this project's schema
  ownership rule) that both sides check the same way keeps one identity model instead of
  reinventing auth twice.
- Deliberately split "authenticate" (resolve a token to a staff member) from "authorize" (does
  that staff member hold the needed capability) into two composable Hono middlewares
  (`requireCapability`/`requireAnyCapability`) plus a pure scoping module (`scopeVisits.ts`) --
  pulled the scoping logic out of `server.ts` specifically because `server.ts` has top-level side
  effects (opens the DB pool, calls `serve()`) that make it unimportable from a test, and "test
  privilege boundaries" was explicit in the task note.
- Design decision documented in the PR and task note: an unassigned visit
  (`assigned_staff_id = 0`, the schema default) is admin-only, not open to any scooper. Chose
  least-privilege-by-default over an "open pool" model since the task note's own phrasing
  ("assigned work") implies assignment is required, not optional; flagged this explicitly as a
  one-line reversible choice (`mayActOnVisit`) if the real workflow wants otherwise.
- Seed/dev-mode auth (`cms/src/auth/seedStaff.ts`) uses a small, committed, explicitly-documented
  non-secret roster rather than skipping auth entirely in dev mode -- keeps `requireCapability()`
  and the scoping behavior exercisable and testable without a database, matching this project's
  existing "seed data is safe to commit, real data never is" convention.
- Verified everything actually runnable in-sandbox: full existing PHP/shell test suite plus 20+
  new schema/wiring assertions in `schema-test.php`, `cms`'s `npm test` (71/71, 16 new) and
  `tsc --noEmit`, `php -l` on every PHP file, `node --check` on the dispatcher page's extracted
  `<script>` block (its only available syntax check, since it has no build step). Explicitly did
  NOT claim to have run `flutter analyze`/`flutter test` (no Flutter/Dart toolchain in this
  sandbox) or a live-database dry run -- said so plainly in the PR rather than implying full
  coverage of code that could not actually be executed here.

**What was good:** split authentication from authorization into separately-testable pieces instead
of one monolithic route-guard, which is exactly what let "test privilege boundaries" actually
happen (16 new tests covering token resolution, capability middleware, and visit-scoping logic in
isolation). Was explicit in both the PR and this note about the one real verification gap (Flutter
tooling) rather than blurring "I wrote it carefully" with "I confirmed it compiles."

**What to improve:** none specific this cycle -- the Flutter verification gap is inherent to the
sandbox, not a shortcut taken, and is flagged for whoever next has a real Flutter environment.

**Kaizen task:** none filed -- no new systematic gap surfaced; the two follow-on tasks this closure
unblocked (t-023 photos, t-024 offline durability) are already correctly scoped and queued rather
than needing a kaizen task to invent them.

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-020 | pattern

**Decision:** implemented and merged humboldtscoopsolutions PR #44 (squash).

**Detail:**
- Dispatched a background exploration agent to map every place a property address can be created
  or edited before writing anything, rather than assuming an admin edit screen existed. Found the
  opposite of what I'd have guessed: property creation/editing is customer-portal-only (auto-create
  on first dashboard view, then a Service Details form posting to `hss/v1/profile`), and the
  address-changed-clears-coordinates safety net already existed but was duplicated ad hoc at that
  one call site, comparing only `address`/`city` and silently missing `state`/`postal_code`.
- Read `cms/PRIVACY-LAUNCH-REVIEW.md` in full before designing (the task note explicitly implied
  it) -- it had already named the correct direction (self-hosted Nominatim, no paid API, own task)
  in 2026-08-15, so the "which geocoder" decision was already made; the work was implementing it
  faithfully, not re-deciding it.
- Kept `HSS_Geocoder` (the network call) and `HSS_Properties` (the database write) in separate
  classes on purpose, matching `HSS_Notify`'s own header comment, which explicitly documents this
  exact separation for the identical reason (a write must not block on or fail because of a
  follow-up action's network dependency). Centralized the address-changed check into
  `HSS_Properties::update_address()` rather than teaching `update()` itself to be geocoding-aware,
  so a DB-only class never gains an HTTP dependency.
- Mirrored `HSS_Notify`'s wp-cron registration pattern exactly for `HSS_Geocode_Sweep`
  (`boot()`/`schedule()`/`unschedule()`, same hourly cadence, same activation/deactivation wiring)
  but deliberately did NOT copy its claim-then-stamp pattern: a failed geocode should keep being
  retried (staying in `missing_coordinates()`), unlike a sent notification, since there's nothing
  to over-notify about here -- explained this reasoning in both the sweep class's own doc comment
  and the PR.
- Wrote `cms/ops/routing/nominatim/` as checked-in scaffolding rather than attempting to actually
  stand up a Nominatim container (no Docker/network access in this sandbox) -- same precedent
  `t-012` (OSRM/VROOM) already established for this exact repo, right down to the "VERIFY ON THE
  ACTUAL HOST" disclaimer and reusing the same shared OSM extract instead of duplicating the fetch.
- Added `site/tests/geocoding-test.php` as a new file rather than extending `schema-test.php`,
  since this task added zero schema/columns -- matches this repo's own convention of one test file
  per concern (`pricing-test.php`, `quote-form-test.php` are likewise separate).
- Caught two false-positive test failures from my own doc comments during self-review (a guard
  checking "no reference to the public Nominatim host" matched my own explanatory prose saying
  "there is no fallback to X") -- fixed by tightening the checks to look for actual usage patterns
  (a URL literal, a `ClassName::` call) rather than bare substring matches, instead of stripping the
  documentation that triggered them.

**What was good:** surveyed the actual current code before designing instead of assuming a shape
from the task note's wording alone, which surfaced a real bug (the state/postal_code gap) the task
wouldn't otherwise have caught. Kept the network-call/database-write separation consistent with an
already-established pattern in this exact codebase rather than inventing a new shape.

**What to improve:** none specific this cycle -- the Nominatim Docker image's exact interface is
flagged as unverified (consistent with the same caveat OSRM/VROOM's scaffold already carries), not
a shortcut taken.

**Kaizen task:** none filed -- the PR's own "Kaizen suggestion" section already named a small,
non-blocking follow-up (a portal-side "we couldn't find that address" UI hint), left for whoever
picks up the next user-facing portal task rather than filed as a dedicated roadmap item for
something this minor.

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-016 | pattern

**Decision:** implemented and merged humboldtscoopsolutions PR #46 (squash).

**Detail:**
- Dispatched a background exploration agent to survey all three named surfaces before
  designing anything, rather than assuming the task's three-way split needed a three-way
  rebuild. Found wp-admin Visits was already correctly gated on `hss_manage_business`
  (PR #39) with a scooper-filtered assignment dropdown -- no change needed there -- and
  that the CMS `/dispatch` page's underlying JSON API was already correctly
  capability-gated per PR #42. What was actually missing was narrower than the task
  read at first glance: the CMS page itself had no scooper-shaped view, and no
  browser-based worker view existed at all (only the Flutter field client).
- Scoped to the most valuable landable slice rather than attempting the full
  admin+dispatch+scooper convergence in one pass: added a `GET /me` capability-report
  endpoint and a role-aware "My Visits Today" tab on the existing `/dispatch` page,
  reusing the exact same `/routes/today` and `POST /visits/:id/complete` contracts the
  Flutter field client already calls -- so a visit completed from the browser and one
  completed from the phone app are indistinguishable to the server afterward. A
  dual-capability (admin+scooper) staff member now gets both tabs and switches without a
  second login or app, the specific case the task named.
- Documented the tab UI explicitly as a convenience layer, not a security boundary --
  every JSON route underneath keeps enforcing its own capability check independently.
  Deferred the larger remaining gap (wp-admin and the CMS are still two separate
  hosts/code paths with no shared navigation and no CMS-side business-management view)
  to a named follow-up rather than attempting it in the same pass.
- Verified: `cms npm test` 72/72 (71 prior + 1 new, covering `/me` reporting both
  capability flags regardless of which one satisfied `requireAnyCapability`), `tsc
  --noEmit` clean, `node --check` on the extracted page script, full existing PHP/shell
  suite re-run unaffected (no PHP touched), and the actual seed-mode service exercised
  end-to-end with curl (`/dispatch`, `/me`, `/routes/today` scoping, visit completion).
  Not verifiable in this sandbox: real browser click-through, database-mode auth paths,
  Flutter re-run (field client untouched).
- This repo has no CI workflows beyond GitGuardian (confirmed: no
  `.github/workflows/`), so "green" here means local verification plus the one GitHub
  App check, consistent with how PR #45 (Silas's own direct edit) merged minutes
  earlier.

**What was good:** delegated the exploration to a background agent with clear
instructions not to touch the conductor repo, then read the actual returned diff and PR
body before merging rather than trusting the self-report -- the diff matched the report
exactly (3 files, the described `/me` route and tab UI, no scope creep).

**What to improve:** none specific this cycle -- scoping decision (dispatch+worker
convergence now, admin+CMS convergence later) was made explicit in the PR rather than
silently narrowing the task's stated scope.

**Kaizen task:** t-031 -- "Add an admin business-management view inside the CMS, and/or
shared navigation between wp-admin and the CMS host, so a dual-capability admin+scooper
staff member reaches business management without a second URL." `stakes: reversible`.

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-017 | pattern

**Decision:** implemented and merged humboldtscoopsolutions PR #47 (squash, additive-only migration audited line-by-line before merge).

**Detail:**
- Dispatched a background agent to survey the actual identity-bridge gap before designing.
  Found the seam was bridged in exactly one ambient place -- `HSS_Customers::get_or_create()`
  stamping `user_id` onto a customer row the moment a logged-in WordPress user hit the
  portal, with no conflict checking and no way for an admin-entered customer row to exist
  and get linked later at all.
- Mirrored `HSS_Staff_Tokens` (PR #42) as the established pattern for issue/hash/redeem
  tokens, split into `peek()` (non-consuming, for a confirm step) and `redeem()` (the
  one-time consuming act) since an invite is redeemed once and closed, unlike a staff
  token that's repeatedly authenticated against.
- Verified the migration myself before merging (Reviewer's line-by-line audit obligation for
  schema changes): schema 2.6.0 is additive-only -- two new nullable/defaulted columns on
  `wp_hss_customers` (`linked_at`, `linked_via`) and one new `CREATE TABLE
  wp_hss_customer_invites`. No `DROP`, no data rewrites.
- `redeem()` explicitly refuses (named `WP_Error`) rather than silently overwriting or
  duplicating when either side of the link is already claimed by someone else; idempotent
  on a retried same-pair redemption. Read the actual `class-hss-customer-invites.php` diff
  before merging, not just the PR description, to confirm the conflict checks are load-
  bearing in the code path (t-018's cautionary precedent -- a permission check that exists
  but nothing calls -- was explicitly on the implementing agent's mind too, per the PR body).
- No merge tool exists yet for resolving a conflict once one occurs in practice; correctly
  deferred to `docs/BACKLOG.md` and a kaizen task rather than built speculatively.
- Verified (implementing agent, cross-checked by this review): `php -l` clean repo-wide,
  full existing PHP/shell suite passes, new `customer-link-test.php` (40+ structural
  assertions). Not verifiable in this sandbox: live MariaDB `dbDelta` run, browser
  click-through of the invite flow -- same standing limitation as every prior schema PR.

**What was good:** actually read the schema-changing diff line-by-line before merging
rather than trusting the PR description's "additive-only" claim at face value -- this is
the specific audit obligation AGENTS.md places on the Reviewer for migration PRs, not
optional due diligence.

**What to improve:** none specific this cycle.

**Kaizen task:** t-032 -- "Build an admin merge tool for two customer records that turn out
to represent the same person (the case `HSS_Customer_Invites::redeem()` and
`HSS_Customers::register()` currently refuse rather than resolve)." `stakes: reversible`.

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-021 | worker+reviewer

**Decision:** implemented and merged silasfelinus/humboldtscoopsolutions#55 (squash 3efd11b), closed `humboldt-scoop-cms/t-021` to `status: done`.

**What happened:**
- Full CLAUDE.md sweep: clean working tree, `check_pr_merged_drift.py` clean, `audit_human_gates.py` returned the standing 35-gate baseline (`appmaker/t-010` already-tracked). No open Todos. Today's dream proposal already existed. `select_role.py` fell back to `reviewer-uncertain` (its own GitHub-API checks 403'd, the documented sandbox limitation) with underlying `role: worker` (`humboldt-scoop-cms/t-021`); cross-checked live PR state directly via GitHub MCP across all four in-scope repos instead -- zero open conductor PRs, one open kind_robots PR (`#1926`, `text-generation/t-005`, correctly parked at its own hard gate, untouched), zero open Kapowarr/humboldtscoopsolutions PRs. Confirmed `worker` was the right role and `humboldt-scoop-cms/t-021` was correctly top of `priority.yaml`'s selectable queue.
- The task's note (already corrected by a prior session) said the real gap was blocked on `t-014`/`t-015` staff identity/authentication -- both had since shipped (done earlier the same day), unblocking the task. Re-read the note carefully rather than trusting the roadmap's stale framing: SMS-on-status-change and the admin-form enroute path already worked; the actual gaps were (1) no scooper-facing en-route trigger, (2) the wp-cron sweep was email-only, (3) `HSS_Notify::failures()` had no admin UI.
- Traced the real architecture before writing anything: `HSS_Notify`'s doc comment explains why it polls rather than hooks (the CMS writes visit changes straight to `wp_hss_service_visits`, no WordPress code runs at that moment). That meant a scooper-facing en-route write needed the identical wp-cron backstop the existing completion sweep already has, not a shortcut.
- Found and fixed a real correctness bug while designing the SMS extension, not just added it: `HSS_Sms::visit_status()` resolves its customer via `HSS_Customers::get_by_user( (int) $visit->user_id )`, which for `user_id = 0` (an admin-entered customer not yet linked to a WordPress account) would silently match whichever unlinked customer row came back first -- texting the wrong person. Refactored `visit_status()` to accept a pre-resolved `$customer`, and the sweep now resolves it the same correct way `recipients()` already does (`customer_id` first, `user_id` fallback) before calling it.
- Also caught that `cms/src/schema.ts`'s `VisitStatus` type and `cms/src/db/rows.ts`'s `VISIT_STATUSES` never included `'enroute'` at all -- a real database row with that status would have been silently remapped to `'scheduled'` by `oneOf()`'s fallback before ever reaching the field client. Fixed as part of the same CMS change, not filed as a separate follow-up, since it was directly in the path of making en-route actually work end to end.
- Also found `RouteStop.fromJson` (Flutter) never read `completed`/`enRoute` from the server response at all -- always the constructor default regardless of what the server said. Fixed in the same field since it's the same class/method and the same bug shape as the field I was adding.
- Built the scooper UI in both places a scooper can actually reach it: the Flutter field client's "I'm on my way" button, and the dispatch page's browser-based "My Visits Today" tab (`humboldt-scoop-cms/t-016`'s convergence work) -- read that tab's existing `completeVisit()` JS closely enough to recognize it's the more realistic day-one scooper UI (no app-store install needed) and mirror the same pattern rather than treating the Flutter app as the only surface.
- Verified: `php -l` clean repo-wide; local PHP/shell suite (`schema-test.php` extended with new "En route + SMS in the sweep" and "Delivery-failure UI" sections, `customer-link-test.php`, `geocoding-test.php`, `portal-test.php`, `pricing-test.php`, `quote-form-test.php`, `representative-access-test.php`, `tools-test.sh`, `theme-css-test.sh`, `theme-js-test.sh`, `front-page-copy-test.sh`) all pass; CMS `npm test` 74/74 and `tsc --noEmit` clean. Fixed one brittle pre-existing test discovered along the way (`customer-link-test.php` hardcoded a literal `2.6.` schema-version match that would have broken on any future bump) to a forward-compatible `version_compare`, matching `schema-test.php`'s own established convention. Not verified in this sandbox: a live MariaDB `dbDelta` run, `flutter analyze`/`flutter test` (no Flutter toolchain here) -- same standing limitation as every prior schema/Flutter change in this project.
- Opened humboldtscoopsolutions#55, confirmed `mergeable_state: clean` and the diff matched exactly the intended scope (539/-39, 24 files) before squash-merging. This repo has no CI workflows beyond GitGuardian (confirmed, no `.github/workflows/`); GitGuardian passed.

**What was good:** did not stop at "wire the two obvious pieces" (button + SMS call) -- traced the actual data path each new write would take and found two real, independent bugs (`get_by_user(0)` customer mismatch; `'enroute'` missing from the CMS's own status enum) that would have made the feature silently misbehave or malfunction in production despite looking complete in a shallow read. Recognized the dispatch page's "My Visits Today" tab as a second, likely more important, scooper-facing surface rather than only touching the Flutter app the task's title happened to evoke.

**What to improve:** SMS coverage for the sweep is account-holder-only -- `HSS_Contacts` (representatives) has no `phone`/`sms_opt_in` column, so a rep who wants texts can't get them through this path. Flagged explicitly in the PR and `docs/BACKLOG.md` rather than silently narrowing scope.

**Kaizen task:** `t-034` -- "Give `HSS_Contacts` its own `phone`/`sms_opt_in` columns so an authorized representative can opt into SMS the same way the account holder does." `stakes: reversible`.

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-032 | worker+reviewer

**Decision:** implemented and merged silasfelinus/humboldtscoopsolutions#57 (squash 420b016), closed `humboldt-scoop-cms/t-032` to `status: done`.

**What happened:**
- Full CLAUDE.md sweep: clean working tree, `check_pr_merged_drift.py` clean, `audit_human_gates.py` returned the standing 35-gate baseline (`appmaker/t-010` already-tracked, no new drift). No open Todos. `select_role.py`'s GitHub-API checks 403'd as usual (documented sandbox limitation); cross-checked live PR state directly via GitHub MCP across all four in-scope repos instead -- zero open conductor/Kapowarr/humboldtscoopsolutions PRs, one open kind_robots PR (`#1926`, `text-generation/t-005`, correctly parked at its own hard gate, untouched). Fell through to `worker`.
- `priority.yaml` order: interface-vision had no ready task; kapowarr's only ready task (`t-023`, upstream-check) is `recurring: true` and had just been run and re-armed this same cycle minutes earlier (own TALKBACK entry timestamped 19:28 UTC) -- picking it again immediately would have duplicated a just-completed no-op cycle, so moved down to the next project with genuine ready work: humboldt-scoop-cms. Within the project, m7 ("UNIFY") is the sole in-progress milestone (m8-m11 all not-started) and `t-032` is its only ready task, so picked it over the m8/m9/m10 backlog even though those have lower task-id numbers.
- This is the exact kaizen `t-017`'s own TALKBACK entry and `docs/DATA-ARCHITECTURE.md`'s "Customer identity bridge" section flagged as deliberately unbuilt: `HSS_Customer_Invites::redeem()` correctly refuses to merge a conflict rather than guessing, but nothing existed to resolve the conflict afterward beyond a "contact us" error.
- Traced that portal dashboard history (`HSS_Portal::active_subscription()`/`invoices()`, `HSS_Visits::next_for_user()`/`history_for_user()`, `HSS_Change_Requests::pending_for_user()`/`history_for_user()`) all key on the WordPress `user_id` column that `subscriptions`/`invoices`/`service_visits`/`change_requests` carry *alongside* `customer_id` -- a merge that only rewrote `customer_id` would look complete in wp-admin's own customer/subscription/invoice listings (which join on `customer_id`) while the customer's own portal kept showing stale, split history. `properties`/`pets`/`contacts`/`customer_invites` carry no `user_id` at all, so those only move `customer_id`.
- Identified the two conflicts that must stay hard refusals rather than being silently resolved: both rows already linked to a *different* real WordPress account, or both already carrying a *different* real Stripe customer -- either would mean discarding a real login or stranding a real Stripe subscription's future webhooks. `merge_preview()` surfaces these as named blockers before the admin confirm screen ever offers a merge button.
- Schema 2.9.0 adds `merged_into`/`merged_at`/`merged_by` -- absorbed row kept for history (not deleted), matching every prior invite/token table's discipline. Filtered `merged_into IS NULL` into `get_by_user()`/`get_by_email()`/`get_by_stripe_id()`/`unlinked_by_email()` so a merged row can never resolve as anyone's live identity again, on top of clearing its own `user_id`/`stripe_customer_id` once transferred.
- Found and fixed a real pre-existing test bug while adding this task's own: `commerce-promises-test.php` hardcoded a literal `SCHEMA_VERSION = '2.8.0'` string match, the exact anti-pattern `customer-link-test.php`'s own comment already names as wrong ("a literal '2.6.' would fail the moment any later task bumps the schema again for something unrelated") -- this task's legitimate 2.8.0 -> 2.9.0 bump broke it for real. Fixed to `version_compare`, matching the convention every other schema-version check in this repo already uses.
- Verified: `php -l` clean on every changed file; every `site/tests/*.php` static suite passes (including the new `customer-merge-test.php` and the fixed `commerce-promises-test.php`); `site/tests/tools-test.sh` passes. Not verified in this sandbox: a live MariaDB `dbDelta` run against the new columns (same standing limitation as every prior schema-bumping task here -- `site/tools/schema-dry-run.sh` is the documented follow-up path), and no live customer data to exercise an actual merge end-to-end.
- Opened humboldtscoopsolutions#57; this repo has no CI workflows tracked (confirmed via `git ls-files | grep .github`, consistent with `t-021`'s TALKBACK note about GitGuardian being the only prior check -- this PR showed zero checks at all) -- squash-merged on local verification alone, same standing as every prior humboldt-scoop-cms merge in this repo's history.

**What was good:** did not stop at "move customer_id on the four related tables" -- traced which portal-facing queries actually key on `user_id` instead and confirmed the merge would be invisible-but-broken from the customer's own dashboard if it only touched `customer_id`. Named the exact two conflict shapes that must refuse rather than guess, instead of either blocking every merge with any linked account/Stripe id, or silently picking a side.

**What to improve:** none this cycle -- scoped exactly to the kaizen's own description, and the one incidental find (the brittle hardcoded-version test) was fixed in the same pass rather than filed as a new task, since it was a one-line convention fix directly caused by this task's own schema bump.

**Kaizen task:** none filed this cycle -- nothing new systematic surfaced doing this one.

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-031 | worker+reviewer

**Decision:** implemented and merged silasfelinus/humboldtscoopsolutions#62 (squash 4bf160b), closed `humboldt-scoop-cms/t-031` to `status: done`.

**What happened:**
- Full CLAUDE.md sweep: clean working tree, `check_pr_merged_drift.py` clean, `audit_human_gates.py` returned the standing baseline (no new drift). Checked open PRs across all four in-scope repos via GitHub MCP: zero on conductor/Kapowarr/humboldtscoopsolutions at sweep time; two on kind_robots -- `#1926` (text-generation/t-005, already correctly parked at its own hard gate, untouched) and `#1930` (a live Silas-authored Academy UI redesign, commits under his own name/email minutes old when found -- left alone rather than merged out from under active human work, despite the `worker/*`-style branch name).
- Per `projects/priority.yaml`, kapowarr outranks humboldt-scoop-cms, but kapowarr's only ready task (`t-023`, recurring upstream-check) had just been cycled as a no-op in the immediately preceding session (same day, same finding: fork point unchanged). Re-running an identical check minutes later would have been pure churn, so moved to the next-priority active project with substantive ready work: humboldt-scoop-cms.
- Read the task's own note carefully before scoping: it names two things ("and/or") -- a CMS-side business-management view, and shared navigation. Checked wp-admin's actual "Scoop Solutions" menu first (`class-hss-admin.php`'s `menu()`) and found it already covers every screen the note lists (Customers, Subscriptions, Invoices, Change Requests, Staff, ...). Building a second copy of a working screen would have been wasted/duplicated surface, so scoped to the real gap: neither host linked to the other at all (confirmed by grepping for any existing CMS_URL/cms_base constant in the WP plugin -- none existed).
- Implementation: `readWpAdminUrl()` (CMS, `db/config.ts`) and `HSS_Config::cms_url()` (wp-admin), both validated as absolute http(s) URLs before ever reaching a link href -- rejecting `javascript:`/relative/malformed values was deliberate, not incidental, since these are env-configured strings that go straight into `<a href>`. CMS link only shows once `GET /me` confirms the admin capability (same discipline the existing role-aware tabs already use); wp-admin link goes through the shared `open()` header so it appears on every business page automatically rather than needing to be added to each `page_*()` method individually.
- Verified before opening the PR: `cms && npm test` 81/81 (7 new unit tests for `readWpAdminUrl`), `npm run build` (tsc) clean, new `site/tests/cms-nav-test.php` (14 structural checks, same no-WordPress-bootstrap convention as the repo's other `site/tests/*.php` files) plus all 10 pre-existing suites re-run clean, `php -l` clean on both touched PHP files, `git diff --stat` matched intended scope exactly (9 files, 263/-3).
- Hit a real mid-session collision: `main` had moved (Silas merged PR #61, a pet-photo-gallery feature, while this task was in flight) before the first push attempt. `git push` failed non-fast-forward; rebased onto `origin/main` cleanly (no conflicts, unrelated files) and pushed successfully on retry -- the documented git-race guardrail working as intended, not a fluke.
- This repo has exactly one CI check (GitGuardian Security Checks) -- confirmed by also checking PR #61's check-run list before assuming something else was still queued. Merged once that one check went green and `mergeable_state` read `clean`.

**What was good:** did not build the CMS-side business-management screen (the more obvious, larger reading of the task) without first confirming whether it would duplicate something that already works -- reading `class-hss-admin.php`'s `menu()` before writing any code avoided real wasted effort and a maintenance-burden fork of business logic that already lives in wp-admin.

**What to improve:** none this cycle -- scoped tightly to the actual gap, verified what was actually verifiable in this sandbox (no live WordPress bootstrap), and said so plainly in the PR rather than implying more coverage than was possible.

**Kaizen task:** `t-035` -- extract a `render_header_extras()` hook if/when `HSS_Admin::open()` grows a second cross-host widget; deferred as low-priority since there's only one such widget today.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-17 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-030 | worker+reviewer

**Decision:** implemented and merged silasfelinus/humboldtscoopsolutions#63 (squash 191844b), closed `humboldt-scoop-cms/t-030` to `status: done`.

**What happened:**
- Full CLAUDE.md sweep: clean working tree, `check_pr_merged_drift.py` clean (0 candidates), `audit_human_gates.py` returned the standing 35-gate baseline (1 already-tracked stale-state signal, `appmaker/t-010`, no new drift). No open Todos. Today's dream proposal already existed. `select_role.py` fell back to `reviewer-uncertain` (its own GitHub-API checks 403'd, the documented sandbox limitation) with underlying `role: worker` (kapowarr/t-023); cross-checked live PR state directly via GitHub MCP -- zero open conductor PRs, one open kind_robots PR (`#1926`, `text-generation/t-005`), already correctly parked at its own hard gate, untouched.
- kapowarr's only ready task (`t-023`, recurring upstream-check) had already been re-verified and re-armed by an earlier session in this same rotation ~4 hours prior (2026-08-17T19:28Z, per its own note) -- re-running the identical no-op check again immediately would have been redundant, so skipped to the next active project with genuinely unworked ready tasks per `priority.yaml`: `humboldt-scoop-cms` (rank 5).
- Of its five `ready` tasks, `t-035` explicitly notes it's "only worth doing once/if a second such widget is actually proposed" (not yet true) and `t-023`/`t-024`/`t-025` are m9/m10 mobile-portal-scale work; picked `t-030` (m8, "finish remaining public-site polish") as the best-scoped fit for a single cycle, since its note explicitly frames it as normal fine-tuning rather than a fixed checklist.
- Investigated the "stale WordPress leftovers" angle concretely rather than guessing at generic polish: found two theme directories (`hss-theme/`, `humboldt-scoop-solutions/`) and a real doc/code mismatch -- `site/README.md`'s tree listing called `humboldt-scoop-solutions` "v2.0 ... active" and `hss-theme` "v1.0 ... earlier" (inverted from the `style.css` `Version:` headers alone), while `site/tests/pricing-test.php` and `theme-js-test.sh` already documented in their own comments that `hss-theme` is the live production theme and `humboldt-scoop-solutions` is "a dead duplicate pending deletion." Confirmed via git history: `humboldt-scoop-solutions` had zero commits since the port (PR #15, 2026-08-15) while `hss-theme` shipped three feature PRs since (#45, #50, #53); grepped the whole repo and found no reference to the dead theme outside its own directory and the two explanatory comments.
- Deleted `wp-content/themes/humboldt-scoop-solutions/` (9 files, 936 lines) and corrected `site/README.md`'s theme listing and known-gaps section (dropped the now-resolved "active theme unconfirmed" bullet, which pointed at a nonexistent `docs/INVENTORY.md`).
- Verified: `php -l` clean on every PHP file in `site/` (excluding vendored `contact-form-7`); all 12 `site/tests/*.php`/`*.sh` suites pass (8 PHP + 4 shell) -- this repo has no CI workflows, consistent with every prior humboldt-scoop-cms session's finding, so local verification is the actual bar. `git diff --stat` matched the intended scope exactly (10 files, 1/-936).
- Opened humboldtscoopsolutions#63, `mergeable_state: clean`, diff matched exactly, squash-merged. Roadmap close-out via conductor PR #2401.
- Left the task at `status: done` rather than re-arming to `ready` or leaving it open-ended: `t-030`'s note frames it as ordinary fine-tuning (not a fixed checklist to exhaust), and the note this session wrote is explicit that other polish areas (mobile layout, accessibility, performance, copy/SEO) remain open for a future session to scope as a fresh task rather than silently folding them into this closed one.

**What was good:** didn't treat "public-site polish" as too vague to act on -- found and verified a concrete, high-confidence, low-risk fix (a self-contained dead directory with an explicit in-repo "pending deletion" comment already written by a prior session, plus a real doc/code inversion) rather than either skipping the task or inventing cosmetic changes. Cross-checked git history and grepped repo-wide before deleting anything, rather than trusting the "dead duplicate" comment on its own.

**What to improve:** none this cycle -- small, scoped, matched the task's own framing.

**Kaizen task:** none filed -- the remaining polish areas t-030's note lists (mobile layout, accessibility, performance, copy/SEO) are real but none surfaced a concrete, verifiable issue this cycle the way the stale-theme mismatch did; better left for a session that finds a specific one rather than filed speculatively.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-18 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-023 | worker+reviewer

**Decision:** implemented and merged silasfelinus/humboldtscoopsolutions#66 (squash 3c7a777), closed `humboldt-scoop-cms/t-023` to `status: done`.

**What happened:**
- Full CLAUDE.md sweep: clean working tree, `check_pr_merged_drift.py` clean, `audit_human_gates.py` returned the standing 35-gate baseline (1 already-tracked stale-state signal, `appmaker/t-010`, no new drift). No open Todos. Today's dream proposal not yet authored (`daily-digest.yml` runs at 15:30 UTC; sweep ran at ~00:30 UTC the same calendar day it's meant to cover -- expected, not a gap). `select_role.py` fell back to `reviewer-uncertain` (its own GitHub-API checks 403'd, the documented sandbox limitation); cross-checked live PR state directly via GitHub MCP across all four in-scope repos -- zero open conductor/Kapowarr/humboldtscoopsolutions PRs, one open kind_robots PR (`#1926`, `text-generation/t-005`), CI green but already correctly parked at its own hard `gate_human: true` security-boundary gate per its own roadmap note, left untouched.
- Per `priority.yaml`, kapowarr outranks humboldt-scoop-cms, but kapowarr's only ready task (`t-023`, the recurring upstream-check) had just been cycled as a no-op by the immediately preceding session hours earlier (same finding: fork point unchanged). Re-running an identical check would have been pure churn, so moved to the next-priority active project with substantive unworked ready tasks: humboldt-scoop-cms. Of its remaining ready tasks, `t-035` explicitly defers itself ("only worth doing once/if a second such widget is actually proposed" -- not yet true) and `t-024`/`t-025` are later-milestone (m10) mobile-portal work; `t-023` (m9) was both the next milestone in sequence and the task the project's own docs (`docs/BACKLOG.md`, `docs/DATA-ARCHITECTURE.md`'s "Sequence" list) had been flagging as the next real gap since 2026-08-15.
- Read `docs/BACKLOG.md`'s "Proof-of-service photos" entry and `cms/PRIVACY-LAUNCH-REVIEW.md` before writing anything, per the task's own note ("decide and document... before code"). The load-bearing architectural fact that shaped every other decision: `cms/ecosystem.config.cjs`'s own comment states the CMS runs on a *different host* from WordPress ("Alexandria serves the WordPress site and the database. It does not run this."), so the obvious pet-photo pattern (`wp_insert_attachment()` into the local uploads directory) was never viable -- the field client's upload lands on the CMS process, which has no filesystem WordPress can read back from. Decided on a `LONGBLOB` column instead: the one thing both hosts already reach is the shared `scoopspress` MySQL database (via ProxySQL), so the database row IS the file, with no new infrastructure (object store, second self-hosted service) needed.
- Built the full vertical slice: WordPress schema (`wp_hss_visit_photos`, schema 2.12.0) and a new `HSS_Visit_Photos` class; a new authenticated REST route to serve bytes back out (ownership-checked per photo, `_wpnonce` query-param auth for `<img>` tags -- deliberately not a public media-library URL, since this is a customer's *property*, not their own pet, a materially heavier privacy case `pet-photo-test.php`'s own doc comment already named); a daily wp-cron retention sweep (180 days, real `DELETE`, no soft-delete column) plus an admin delete-on-request action; customer-portal and admin-log gallery rendering sharing one thumbnail helper; the CMS's `POST /visits/:id/photos` (magic-byte content sniffing via a new `imageSniff.ts`, live `photos_opt_in` re-check rather than trusting the field client's snapshot); and the Flutter capture/compress/offline-queue flow (`image_picker`'s own quality/max-width options for compression -- no separate package needed -- and a new `FilePhotoUploadQueue` persisting to the app's documents directory so a lost connection or a closed app doesn't lose a photo already taken).
- Threaded `photosOptIn` end-to-end as the crew-visible consent indicator `docs/BACKLOG.md` asked for: `Customer.photosOptIn` (CMS schema/seed data) -> `mapCustomer()` -> `FieldStop.photosOptIn` -> `RouteStop.photosOptIn` -> the Flutter capture button's own visibility. The CMS route re-checks the live database value at upload time regardless, so this threaded value is a UI convenience, not the actual enforcement point.
- Verified everything a sandbox with no live WordPress/MariaDB and no Flutter toolchain can verify: `cms && npm test` 90/90 (9 new tests: `photosOptIn` mapping/threading, the `photo` id prefix, `imageSniff.ts`'s magic-byte checks), `tsc --noEmit` clean; every `site/tests/*.php`/`*.sh` passes including a new `visit-photo-test.php` (29 structural checks, same regex-over-source convention as `pet-photo-test.php`); `php -l` clean on every touched/new PHP file; a manual `curl` smoke test of the new CMS route's auth/assignment/seed-mode boundaries (401/403/503 all behaved correctly against a locally-run dev server). Not verified, and said so plainly in both the PR and `field-client/README.md`'s new dedicated section: `flutter analyze`/`flutter test` (no Flutter/Dart toolchain in this sandbox -- the same standing limitation `t-015`/`t-021` already flagged) and a live MariaDB `dbDelta` run of the new table. `pubspec.lock` was deliberately left unregenerated rather than hand-edited; the first real `flutter pub get` resolves the two new dependencies normally.
- This repo has no CI workflows at all (confirmed again, consistent with every prior humboldt-scoop-cms finding) -- `mergeable_state: unstable` with zero registered checks is the expected shape here, not something to wait out. Diff matched intended scope exactly (29 files, +1395/-44) before squash-merging.

**What was good:** did not default to the already-proven pet-photo pattern (WordPress media-library attachment) just because it existed in the same codebase -- read the CMS's own deployment comment closely enough to catch that the two-host architecture makes that pattern structurally impossible here, and let that constraint (not convenience) drive the storage decision. Also caught and fixed, before it shipped, a real bug of my own making: an early draft compared a GMT-stamped `created_at` against a site-local cutoff in the retention sweep, which would have silently mispurged photos by the site's UTC offset every run.

**What to improve:** none this cycle -- large surface (WordPress + CMS + Flutter) but each piece was scoped to exactly what the task's own note called for, matched existing conventions in each subsystem, and every verification gap was a genuine sandbox limitation rather than a shortcut.

**Kaizen task:** none filed -- `docs/DATA-ARCHITECTURE.md`'s "Sequence" list has no remaining unchecked items this session's scope touches, and the natural next mobile-portal work (`t-024`, `t-025`) is already tracked as its own ready task rather than a gap this cycle uncovered.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-18 | Agent (scheduled conductor sweep) | humboldt-scoop-cms/t-037 | worker

**Decision:** implemented and merged silasfelinus/humboldtscoopsolutions#76 (squash `e71666e`), closed `humboldt-scoop-cms/t-037` to `status: done`.

**What happened:**
- Continued the same session's sweep that closed `t-025` earlier (see the root `TALKBACK.md` entry timestamped 2026-08-18). After `t-025` merged, `next_ready_task.py` surfaced `t-035` next by file order ("Extract a `render_header_extras()` hook..."), but its own note says it is "small, low-priority -- only worth doing once/if a second such widget is actually proposed." Read the live `HSS_Admin::open()` and confirmed no second cross-host widget exists yet -- the condition the task itself gates on hadn't been met, so implementing it now would have been a premature speculative refactor with no real second use-case to design against. Deliberately skipped it (left at `status: ready`, not touched) and picked `t-037` instead: one of `t-025`'s own four deferred follow-ups (`t-036`..`t-039`), and the most concretely scoped/valuable of the four -- a real security-relevant gap (no way to revoke a compromised customer app token without going to the database directly), with a clear existing pattern to mirror (`HSS_Staff_Tokens`/`staff_tokens_section`, t-015).
- Claimed via `claim_task.py`. Worked directly in the shared `/home/user/humboldtscoopsolutions` checkout (no background delegation this time -- scope was small enough for one foreground pass) after reading `class-hss-staff-tokens.php`, `staff_tokens_section()`, and the customer-screen's existing `?invite=ID`/`?contacts=ID` section pattern closely enough to mirror them exactly rather than inventing a new shape.
- Confirmed `wp_hss_customer_tokens` already existed as a WP-DB table (created by `t-025`'s `HSS_DB::install()`, same schema shape as `wp_hss_staff_tokens`) before writing anything -- this was a UI-only addition, no schema change needed.
- Built `HSS_Customer_Tokens` (read/revoke only, deliberately no `issue()` -- issuance stays on the CMS's own admin-gated endpoint per `t-025`'s design, mirroring `t-037`'s own note), wired an "App tokens" column + `?tokens=ID` section into the Customers screen with the same nonce-checked revoke pattern every other destructive action on that screen uses, and bumped the yard-subrow `colspan` from 10 to 11 to keep the table structurally correct (which also incidentally fixed a pre-existing off-by-one on the "no yard on file" row, previously `colspan="9"`).
- Wrote `site/tests/customer-token-admin-test.php` mirroring this repo's established static-source-check convention (no live WordPress/MariaDB in this sandbox) -- asserts the class shape, that `issue()` is deliberately absent, the GET/POST wiring, nonce checks, and the table's column/colspan consistency. Ran `php -l` on every touched/new file and the full existing `site/tests/*.php` (15 suites) + `tools-test.sh` to confirm nothing regressed, plus the new test.
- Verified before closing: PR #76's actual diff (179/+3-, 4 files) matched exactly the intended scope. This repo has no CI workflow beyond GitGuardian secret scanning (confirmed again -- no `.github/workflows` directory); GitGuardian completed green, merged squash.

**What was good:** read the task's own note critically rather than executing the next-in-file-order task blindly -- `t-035` explicitly gated itself on a condition ("once/if a second such widget is actually proposed") that a quick source check showed hadn't been met, so working it now would have been speculative. Picking `t-037` instead landed real, well-scoped, security-relevant value with a precedent close enough to mirror line-for-line.

**What to improve:** none this cycle -- scope stayed tight to exactly what `t-037`'s note asked for (list + revoke), correctly left issuance to `t-038` rather than scope-creeping it in.

**Kaizen task:** deferred -- no systematic gap surfaced this cycle; `t-035`'s self-gating note is doing exactly what a task note should (telling a future session when NOT to pick it up), not a pattern that needs fixing.

---
_Generated by [Claude Code](https://claude.ai/code)_
