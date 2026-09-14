# ecosystem-map — task history archive

Full `note:` prose for completed ecosystem-map tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Write the ecosystem design brief

<!-- note:begin t-001 -->
Roadmap/reality drift found and corrected: DESIGN-BRIEF.md already existed in full (canonical ownership table, project bot parity, visual asset parity, image approval gate, duplication risks, first deliverables, non-goals) but this task was still marked ready. Verified the document covers the full scope asked for — the shared resource graph across Conductor projects, Dreams, Bots, ArtCollections, narrator topics/threads, menus, generated images, and project UI — and flipped to done.
<!-- note:end t-001 -->

## t-002 — Confirm scope with Silas

<!-- note:begin t-002 -->
CLEARED 2026-07-06 (Silas in-session, daily standup): scope confirmed — ecosystem-map owns the cross-project asset/bot/resource audit. approved_by_human set per the CONTROL.md in-session clearance rule. FOR SILAS: soft checkpoint, nothing is blocked on it. Confirm whether ecosystem-map should own the cross-project asset/bot/resource audit, or redirect it into an existing project such as kind-robots or global-ui. Development can continue while you decide.
<!-- note:end t-002 -->

## t-003 — Inventory project visual asset coverage

<!-- note:begin t-003 -->
Added projects/ecosystem-map/ASSET-COVERAGE-MATRIX.md: a static-repo-verifiable audit of all 40 projects' icon/card/hero coverage (present vs queued in art-prompts.yaml vs missing-and-unqueued), ArtCollection inspiration image counts, and mock-screenshot need (sourced from FRONTEND-SURFACE-MAP.md's Class column where audited). Found 6 active projects with no identity images and nothing queued (animation-manager, kindrobots-unraid, model-builder, mural-design, newsfeed, davinci-hero), 7 projects already queued in art-prompts.yaml pending only a generation pass, and 23 of 34 non-retired projects with zero inspiration images. Project Dreams/liveUrl and bot avatar/portrait images are explicitly out of scope (DB-only data; bot images belong to t-004) rather than guessed. Does not generate or touch any image binaries, per DESIGN-BRIEF.md's non-goals.
<!-- note:end t-003 -->

## t-004 — Specify Manager and Assistant bot parity

<!-- note:begin t-004 -->
Added projects/ecosystem-map/BOT-PARITY-SPEC.md, grounded in the live kind_robots schema (Bot.BotType is a free string not an enum; portraits live in ExpressionMedia, not on Bot; there is no dreamType: PROJECT -- Project is its own model joined via Project.managerBotId -> Bot.id). Covers botType selection (MANAGER for project-steering bots, linked through Project.managerBotId not a Dream), avatar image prompt rules, the 20-slot ExpressionMedia emotion/action portrait set (10 EMOTION + 10 ACTION values from the real Expression enum, plus CUSTOM), narrator NarratorTopic/NarratorThread wiring where starterPrompts *is* the project navigation menu contract, and a minimum-viable-parity implementation sequence for t-006 to route per project. Verified schema details via GitHub read-only research against silasfelinus/kind_robots (Bot, ExpressionMedia, NarratorTopic, NarratorThread, Project models) rather than assuming the DESIGN-BRIEF.md description was implementation-accurate.
<!-- note:end t-004 -->

## t-005 — Audit shared layers for duplicate development

<!-- note:begin t-005 -->
Analyze active projects for overlapping systems: galleries, project menus, narrator threads, pack/content permissions, task surfaces, roadmap milestones, ArtCollections, bot images, and project metadata. Produce a reuse map with specific recommendations for which layer owns each primitive.
DONE 2026-07-19 (burst-mode): wrote projects/ecosystem-map/REUSE-MAP.md, a static audit of silasfelinus/kind_robots's schema/components against DESIGN-BRIEF.md's ownership table. Two confirmed real findings: (1) 22 independently-implemented `*-gallery.vue` components with no shared base — same grid/filter/variant pattern hand-rolled per model (`ui-gallery.vue` is a same-named-but-unrelated style-guide page, not a base component); (2) content sharing/visibility is still ~19 scattered `isPublic` booleans with no Grant/ACL model, matching and independently re-verifying projects/kind-robots/SHARING-SPEC.md's existing findings rather than duplicating that design work. One confirmed gap (not duplication): roadmap milestones never reach the kind_robots DB — scripts/sync_projects.py only syncs the free-text `goal`, so no front-end surface can currently show per-milestone progress. Everything else audited (bot images/ExpressionMedia, project↔bot linkage, Todo vs roadmap task separation, ArtCollections) was confirmed correctly single-owned, no action needed. This unblocks t-006 (all of its t-003/t-004/t-005/t-007/t-008 dependencies are now done).
<!-- note:end t-005 -->

## t-006 — Create implementation tasks for confirmed gaps

<!-- note:begin t-006 -->
Turn the confirmed ecosystem gaps into small project-owned implementation tasks. Route shared UI work to global-ui or kind-robots and project-specific surfaces to their home roadmaps. Do not implement the gaps inside ecosystem-map itself. Missing user-facing surfaces should add a tab to an existing channel according to TAB-INTEGRATION.md; WonderLab is the fallback, and a new channel requires explicit human approval. FRONTEND-SURFACE-MAP.md currently identifies 15 missing or incomplete surfaces and prioritizes already-built partial integrations first. RAN 2026-07-20 (claude-conductor-burst-20260720T0700Z): verified live against kind_robots main (not just re-reading the 2026-07-10 audit) before writing any new tasks, since the audit note flagged partial integrations as the priority. Checked stores/helpers/dashboardHelper.ts and content/*.md for all 15 rows marked "missing" or "incomplete": every one (Humboldt Scoop, Humboldt Scoop CMS, Sketchy, Storybook, Da Vinci, Media Watchlist, Conductor App, Alexa Integration/Voice Lab, Mermaids of Venice, Packmaker, Coat Dance, Wishmaster, Challenge Center, Serendipity, AppMaker) now has a registered dashboard tab, a channelKey/tabKey pair, and a content/<slug>.md route rendering the shared project-front-page scaffold (the project-frontend-pages pass referenced in this doc's own 2026-07-12 update). Then checked each of those 15 projects' own roadmap.yaml for the corresponding follow-up implementation task: all 15 already have a "Polish and upgrade <Project> front-end surface" task (the standard task shape used across every project for exactly this "evolve the scaffold into the full interactive experience" step) — 5 already `done` (Humboldt Scoop/t-008, Humboldt Scoop CMS/t-011, Mermaids of Venice/t-012, Packmaker/t-006, Challenge Center/t-019) and the remaining 10 already `ready` and queued in priority.yaml order (AppMaker/t-012, Coat Dance/t-010, Conductor App/t-013, Da Vinci/t-014, Media Watchlist/t-006, Alexa Integration/t-015, Serendipity/t-012, Sketchy/t-007, Storybook/t-010, Wishmaster/t-003). No new implementation tasks were needed — creating duplicates of the existing "polish and upgrade" tasks would only fork the same work into two roadmap entries. Updated FRONTEND-SURFACE-MAP.md to record this re-audit so the next cycle reads current reality instead of the stale 2026-07-10 snapshot. Marking t-006 done: its job (confirm gaps -> route implementation tasks to the right project roadmaps) is complete — the gaps were closed by intervening project-frontend-pages + per-project polish work between 2026-07-12 and now, this cycle only confirmed and documented it.
<!-- note:end t-006 -->

## t-007 — Map project front-end surfaces and canonical launch links

<!-- note:begin t-007 -->
Completed projects/ecosystem-map/FRONTEND-SURFACE-MAP.md as a static GitHub audit of all 29 active projects. Results: 8 complete user-facing surfaces, 6 internal or platform projects that should not receive fake standalone tabs, and 15 missing or incomplete surfaces. The map records existing/proposed channel, tab, route, component evidence, tutorial/image state, intended Dream.liveUrl, confidence, and follow-up order. It distinguishes working UI from APIs/assets/project cards alone. Challenge Center is partial rather than verified complete: APIs, schema, card, and collection art exist, but no dedicated component/render branch was found in the current Conductor manager. AppMaker and Wishmaster have reusable nested Conductor components but still need canonical tab integration. Production Dream.liveUrl values remain a database verification step for t-006 implementation work.
<!-- note:end t-007 -->

## t-008 — Write the project tab integration runbook

<!-- note:begin t-008 -->
Added projects/ecosystem-map/TAB-INTEGRATION.md. It defers exact code templates to kind_robots/sample/new-section.md and conductor projects/kind-robots/SECTIONS.md, while defining Ecosystem's placement policy: reuse existing surfaces, choose the best existing channel, use WonderLab as fallback, and gate new channels. The guide includes working references, the dashboard/tutorial/image/manager/page/liveUrl sequence, completion checks, and the required FRONTEND-SURFACE-MAP.md columns.
<!-- note:end t-008 -->
