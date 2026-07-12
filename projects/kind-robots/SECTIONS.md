# Adding a page, tab, or channel to Kind Robots

Process doc for the conductor loop. Whenever a task — Silas's or a project's
— requires a new section in the kind_robots app, follow this so it happens
the same way every time. (For generating *content objects* — bots, dreams,
characters, rewards, scenarios, threads, expressions, pitch sheets — see
`GENERATION.md` in this folder.) The canonical implementation framework (full
recipes, code templates, image checklist) lives in the kind_robots repo at
**`sample/new-section.md`**; this doc is the policy layer plus the condensed
checklist for planning without the other repo open.

## Vocabulary

- **Page** — `content/{title}.md` in kind_robots. Single-word lowercase
  filename; the filename IS the route. The body is exactly one line, the
  page's primary component directive: `:{title}-manager`.
- **Tab** — an entry inside an existing channel's config in
  `stores/helpers/dashboardHelper.ts`. The channel's manager component
  renders the right tab dynamically.
- **Channel** — a new top-level key in `dashboardConfigs`, with its own
  tabs, footer entry, nav card, tutorial channel, route, and image set.

## Permission gates

| Adding a… | Gate |
| --- | --- |
| Page | reversible software work — Worker/Reviewer may proceed and merge normally |
| Tab in an existing channel | reversible software work — proceed normally |
| **Channel** | **hard `needs-human` — Silas only.** Do not create a new channel unless Silas explicitly approved it in the task (`approved_by_human: true` or a direct session instruction). A task that turns out to need a new channel stops at `needs-human` with a note proposing the channel key, tabs, and route. |

Cross-repo rules apply as usual (AGENTS.md): the roadmap task lives in
conductor, the code lands in kind_robots on a `worker/*` branch PR'd to its
`main`; if repo access is blocked, preserve the patch as a
`projects/kind-robots/docs/<task-id>-*.md` handoff instead.

## Condensed checklists

All keys are single-word lowercase. All images go under
kind_robots `public/images/`, filenames matching keys exactly. Icons are
Iconify `kind-icon:*` names, not files.

### Every page (channel page or standalone tab page)

1. `content/{title}.md` — frontmatter per `content.config.ts`, including a
   valid `dashboardKey`/`dashboardTab` pair (checked by
   `validateDashboardPair`).
2. Body: `:{title}-manager` — nothing else. The component lives at
   `components/{domain}/{title}-manager.vue`; filenames are globally unique.

### Every tab

1. Entry under the channel's key in `dashboardConfigs.{channel}.tabs[]`
   (`stores/helpers/dashboardHelper.ts`) — key, label, icon, title,
   summary, `image: tabImage(...)`, narrative, route. Add
   `requiredRole: 'ADMIN'` for admin-only tabs.
2. Matching section under the channel's key in
   `tutorialChannels.{channel}.sections[]`
   (`stores/helpers/tutorialCards.ts`).
3. Images: `dashboard-tabs/{channel}/{tab}.webp` and
   `tutorials/{channel}/{tab}.webp` (same art in both paths is fine).
4. **Register the Project DB placement** (easy to miss — the front-end wiring
   does not set it): add `liveUrl`/`channelKey`/`tabKey` to the project's entry
   in `project-overrides.yaml` (or its `roadmap.yaml`); `scripts/sync_projects.py`
   upserts them to the `Project` row via `PATCH /api/projects/{slug}`. Without
   this the project has a page but no DB registration.

### Every channel (after Silas approves)

1. Footer entry in `dashboardConfigs.footer.tabs[]` — this registry IS the
   channel list; nav cards derive from it (never hand-edit `navCards.ts`;
   its only hand-written card is conductor).
2. The channel's own `dashboardConfigs.{channel}` block with `defaultTab`
   and one tab entry per tab.
3. `footerDashboardMap` entry (compile-enforced).
4. `tutorialChannels.{channel}` with hero/overview and one section per tab
   (compile-enforced).
5. `content/{channel}.md` page calling `:{channel}-manager`, a tab switcher
   driven by `getDashboardTabs('{channel}')` that dynamically shows the
   right tab.
6. `components/navigation/channel-select.vue` → `allChannels[]` — hand
   maintained, fails silently; easiest step to miss.
7. Images: hero `nav/heroes/{channel}.webp`, card/thumb
   `nav/thumbs/{channel}.webp`, tutorial hero
   `tutorials/{channel}/hero.webp`, plus the per-tab pair above.

### Verification before PR

- Typecheck passes (missing `footerDashboardMap`/`tutorialChannels` entries
  fail the build).
- The page loads and its `dashboardKey`/`dashboardTab` validate.
- The channel appears in the header dropdown and footer nav (the dropdown
  is the unenforced step — check it last).

## Art requests

Per AGENTS.md, generated project art is pre-approved: agents may generate
and commit the hero/card/tab/tutorial images through the auto art pipeline
when the task calls for it, keeping prompt/model/source metadata. Missing
art may also be queued via `ART-PROMPTS.md`. Never let missing images block
the code PR — the app falls back to placeholders.
