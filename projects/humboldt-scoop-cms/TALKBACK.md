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
