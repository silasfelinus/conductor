# NAVIGATION-MAP.md — global-ui

Final navigation/presentation map for the task-surface system: where each surface
actually lives in the Kind Robots workspace UI today, checked directly against the
kind_robots `main` branch (not just the original spec's intent). Companion to
TASK-SURFACE-SPEC.md (the design) and GLOSSARY.md (the vocabulary) — this document is
the as-built map plus a gap list.

Version: 1.0
Date: 2026-07-15
Depends on: t-002, t-003, t-004, t-007, t-008, t-009 (all `done`)
Verified against: kind_robots `origin/main` @ b4c1e6d4 (`components/pages/conductor-page.vue`,
`components/pages/conductor-manager.vue`, `stores/todoStore.ts`, `stores/serendipityStore.ts`)

---

## 1. Navigation map (where each surface lives today)

| Surface | Entry point | Component | Scope | Data source |
|---|---|---|---|---|
| Project task (roadmap) | Plan → Conductor (`content/conductor.md`, `dashboardKey: conductor`) → select a project | `conductor-manager.vue` → `conductor-page.vue` (roadmap section) | Per-project | conductor `roadmap.yaml`, read-only mirror |
| Task creation form | Same project detail view, "Add task" form | `conductor-page.vue` | Per-project | `todoStore.createTodo()` → kind_robots DB `Todo` |
| Honeydo queue | Same project detail view → `taskTab === 'HONEYDO'` | `conductor-page.vue` | **Global** data (`todoStore.honeyDoTodos`, unfiltered by project) but **not** a top-level nav destination — reached only by opening a project and switching tabs | kind_robots DB `Todo` (`category: HONEYDO`) |
| Honeydo (conversational) | Serendipity voice chat, ambient real-world hooks | `serendipityStore.ts` (`kind: 'honeydo'` question hooks) | Global | Same `Todo` rows, surfaced as spoken prompts |
| Kaizen section | Project detail view, below roadmap | `conductor-page.vue` (`dreamKaizens(dreamId)`) | Per-project | kind_robots DB `Todo` (`category: KAIZEN`, `dreamId`-scoped) until promoted, then `roadmap.yaml` |
| "How can I make this look better?" prompt | Kaizen section, project detail view | `conductor-page.vue` | Per-project | `todoStore.createTodo()` (KAIZEN, `dreamId` set) |
| Desired-feature wishlist | Project detail view, below kaizen section | `conductor-page.vue` (`dreamFeatures(dreamId)`) | Per-project | kind_robots DB `Todo` (`category: DESIRED_FEATURE`, `dreamId` + `order`) |
| Approval gate badge | Task card in roadmap section | `conductor-page.vue:1638-1671` (`task.gateHuman`/`task.approvedByHuman`) | Per-task | conductor `roadmap.yaml` |
| Completed task | Task card in roadmap section, inline (badge + icon only) | `conductor-page.vue:2736-2747` | Per-project | conductor `roadmap.yaml` (`status: done`) |
| UI style gallery / token reference | `/ui` route | `ui-gallery.vue` | Global | `content/ui.md` + `assets/css/tailwind.css` (`.kr-*` classes) |
| Site-audit agent | Not yet a live surface (see §3) | — | — | `projects/global-ui/SITE-AUDIT-AGENT.md` (design only) |

---

## 2. What matches the spec

- **Project tasks** — read-only mirror of `roadmap.yaml`, exactly as TASK-SURFACE-SPEC.md
  §1/§6 requires. No UI write path into conductor files. ✅
- **Task creation** — routes through `todoStore.createTodo()`, not a direct API call,
  supports all four categories. ✅ (t-002)
- **Kaizen** — correctly `dreamId`-scoped via `dreamKaizens(dreamId)`, plus the "make
  this look better" free-text prompt. ✅ (t-004, t-006)
- **Desired-feature wishlist** — correctly `dreamId`-scoped via `dreamFeatures(dreamId)`,
  orderable, promote/retire supported. ✅ (t-007)
- **Approval gates** — `awaiting approval` / `approved` badges driven by
  `gateHuman`/`approvedByHuman`, matches spec §2/§6 exactly. ✅
- **Honeydo data model** — correctly global/unscoped (`todoStore.honeyDoTodos` filters
  only on `category`, not `dreamId`), matching spec §3's "not project-specific." ✅

## 3. Where the as-built UI diverges from the original spec (follow-up candidates)

1. **Honeydo has no dedicated top-level nav surface.** TASK-SURFACE-SPEC.md §3 called
   for a "For You" inbox "top-level nav." What shipped (t-003) is a `HONEYDO` tab
   *inside* the per-project Conductor page — global data, but the only way to reach it
   is: open Plan → Conductor → pick any project → switch to the Honeydo tab. A user
   with zero interest in a specific project's roadmap has no direct path to "what does
   the AI need from me right now." The Serendipity voice agent partially compensates
   (ambient honeydo hooks in conversation), but there is no visual equivalent.
2. **No "Completed (N)" collapsed disclosure.** TASK-SURFACE-SPEC.md §7 specified
   completed tasks default-collapsed under a per-milestone "Completed (N)" header. What
   shipped is inline status badges/icons on `done` tasks with no grouping or collapse —
   long-lived projects with many closed tasks show every one, all the time, in the
   roadmap list.
3. **Site-audit agent is designed but not confirmed live.** SITE-AUDIT-AGENT.md (t-009)
   defines the prompt, weekly cadence, and scope, but its own note says it "needs Silas
   approval before the trigger is created" — no roadmap or TALKBACK entry since
   2026-06-30 confirms the Claude Code Remote trigger was actually created. The
   recurring site-audit agent loop this task is supposed to map is currently a spec, not
   a running loop.

None of these are regressions — t-002 through t-009 shipped real, working, spec-compliant
data plumbing (`dreamId` scoping is correct everywhere it matters). The gaps are entirely
in top-level *discoverability*: two of three items above ship correct data with an
incomplete or missing front-door.

## 4. Recurring site-audit agent loop (as specified, pending activation)

Per SITE-AUDIT-AGENT.md: weekly (Mondays 09:00 UTC), reads roadmaps/API routes/stores/
schema, diffs conductor vocabulary against actual kind_robots frontend/backend support,
writes `AUDIT-REPORT-YYYY-MM-DD.md` plus up to 3 new `ready` tasks. Hard boundaries: no
live URLs, no main-branch pushes, no `gate_human` tasks. This document's §3 findings are
exactly the kind of gap that loop is designed to catch automatically once it's running —
until the trigger exists, that catching happens manually (as in this task).

---

## 5. Follow-up tasks (scoped separately, not folded into t-005)

See roadmap.yaml t-014, t-015, t-016.
