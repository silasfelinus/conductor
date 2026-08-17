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
