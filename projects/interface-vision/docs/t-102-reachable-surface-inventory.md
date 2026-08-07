# t-102: Canonical reachable-surface and responsive acceptance inventory

Built 2026-08-07 as the deliverable for interface-vision/t-102. This is the
baseline inventory t-103 works from — per t-102's own note, "the inventory
must be numeric and shrink-to-zero."

Static analysis only — no dev server was started, no browser was driven.
Repo snapshot: `kind_robots`, branch `claude/relaxed-lovelace-i4x1f5` ==
`origin/main` as of commit `ee989ab` (2026-08-07 ~10:12 UTC). Routes are
enumerated as of that snapshot; new pages/content added after this date are
not reflected here and should be added to the inventory as t-103 progresses.

## How a URL resolves here (read first)

- `pages/[...slug].vue` is the catch-all. For any path not matched by a more
  specific file under `pages/`, it runs
  `queryCollection('content').path(path).first()` against the **`content`**
  Nuxt Content collection only.
- `content.config.ts` defines two collections: `content` (`source.include:
  '**/*.md'`, `exclude: ['channels/**']`) and `channels` (`source:
  'channels/**/*.md'`). **`content/channels/**` is therefore never resolved
  by the catch-all route** — those 61 files are channel/tab *configuration*
  (nav label, icon, cards, and a `route:` field), not pages themselves. They
  drive `channelContentStore` / the channel-select dropdown and the
  `dashboardShell`, and each one's `route:` field points at the actual
  content page (or static page) that renders when a user follows it.
- No file in `content/**` sets an explicit `path:` frontmatter override, so
  every routable content file's path is the plain Nuxt Content default: file
  path under `content/`, extension stripped, `index.md` → parent directory
  (`content/index.md` → `/`).
- Nuxt's file-based `pages/**/*.vue` routing takes precedence over the
  `[...slug].vue` catch-all for an exact literal path match. Two content
  files collide with a static page at the same path and are therefore dead
  content (see **Shadowed content**, below).

## Summary counts

| Metric | Count |
|---|---|
| Total distinct reachable URL surfaces | **85** (68 content-rendered + 15 static-page concrete + 2 dynamic, each represented by one example) |
| ...covered by the responsive-audit **default** route list | **7** real routes (`/`, `/conductor`, `/dreams`, `/art`, `/bots`, `/characters`, `/rewards`) — the list had an 8th entry, `/scenarios`, that matched no real route at all (fixed in kind_robots #1559, see Notes) |
| Admin-only surfaces | **10** (5 content-driven, 5 static `pages/admin/*.vue`) |
| Orphaned / unlinked from any nav source found | **16** (9 content, 7 static) |
| Dynamic / parameterized routes | **2** patterns (`/users/[id]`, `/play/challenges/[slug]`) |
| Content files total under `content/**/*.md` | 132 |
| ...excluded as dev-only (`content/dev/**`) | 1 |
| ...channel/tab config, not directly routable (`content/channels/**`) | 61 |
| ...actually routable content pages | 70 (68 render; 2 are shadowed/dead — see below) |
| Static `pages/**/*.vue` files | 18 (1 catch-all mechanism + 2 dynamic + 15 concrete routes) |

**The headline number for t-103: 51 non-admin, nav-linked routes have zero
responsive-audit coverage today, against 7 that are covered.**

**Nav-reachability method**: a route counts as nav-reachable if its path
appears in at least one of three live navigation sources: (a) the `route:`
field of a `content/channels/**/*.md` file (rendered by the channel-select
dropdown, `components/navigation/channel-select.vue`, and gated by
`filterChannelsByRole` / `filterChannelsByPermission`), (b) the `route:`
field of a tab inside `stores/helpers/dashboardHelper.ts`'s `dashboardConfigs`
(the per-dashboard tab bar), or (c) a `link` field in
`stores/seeds/smartIcons.json` (the default smartbar/directory icons). For
the handful of static pages not covered by any of those three registries, an
in-app `NuxtLink`/`to=` reference was searched for instead (documented
inline per route below).

## Content-driven routes, grouped by content directory

`nav?` = found in a live nav source (see method above). `audited?` = in the
responsive-audit script's current default `--routes` list.

### content/channels/admin (6 files — config only, not directly routable)
All six are `contentType: tab`/`channel` metadata for `channelKey: admin`.
Each carries a `route:` that points at one of the 5 admin content pages
below (`/artjob`, `/navigation-health`, `/project-placement`, `/scoop-cms`,
`/user-admin`) or, for `index.md`, also `/artjob` (channel default tab).

### content/channels/sanctuary (7 files — config only)
`channelKey: sanctuary`. Routes point at `/about`, `/cart`, `/sanctuary`
(giftshop's route, and the channel default), `/giving`, `/mermaids`,
`/privacy`.

### content/channels/plan (17 files — config only)
`channelKey: plan`. Routes point at `/build/animation-manager`, `/appmaker`,
`/brainstorm`, `/coloring`, `/conductor-app`, `/build/hair-studio`,
`/conductor` (channel default + `projects` tab), `/model-builder`,
`/build/mural`, `/plan/wonderlab` (museum tab), `/plan/newsfeed`, `/packs`,
`/stylist`, `/plan/voice-lab`, `/plan/watchlist`, `/wishmaster`.

### content/channels/play (19 files — config only)
`channelKey: play`. Routes point at `/academy`, `/art`, `/bots`,
`/play/challenges`, `/characters`, `/play/davinci`, `/play/memory`
(`experiments` tab), `/facets`, `/dreams` (`gallery.md`, and the channel
default), `/music-mentor`, `/resources`, `/rewards`, `/stories`
(`scenarios.md`), `/play/screenfx`, `/serendipity`, `/storybook`,
`/taskmaster`, `/play/video-generator`.

### content/channels/home (12 files — config only)
`channelKey: home`. Routes point at `/account`, `/achievements`, `/chats`,
`/` (`dashboard.md`, and the channel default), `/for-you`, `/friends`,
`/messages`, `/navigation`, `/register`, `/themes`, `/wallet`.

### content/plan (4 files — all render)
| path | source | title | nav? | admin? | audited? |
|---|---|---|---|---|---|
| /plan/newsfeed | content/plan/newsfeed.md | Newsfeed | yes | no | no |
| /plan/voice-lab | content/plan/voice-lab.md | Voice Lab | yes | no | no |
| /plan/watchlist | content/plan/watchlist.md | Watchlist | yes | no | no |
| /plan/wonderlab | content/plan/wonderlab.md | Backend Museum | yes | no | no |

### content/plan/projects (4 files — all render)
| path | source | title | nav? | admin? | audited? |
|---|---|---|---|---|---|
| /plan/projects/coat-dance | content/plan/projects/coat-dance.md | Coat Dance | yes | no | no |
| /plan/projects/humboldt-scoop | content/plan/projects/humboldt-scoop.md | The Humboldt Scoop | yes | no | no |
| /plan/projects/ruler-hooked | content/plan/projects/ruler-hooked.md | Ruler Hooked | yes | no | no |
| /plan/projects/sketchy | content/plan/projects/sketchy.md | Sketchy | yes | no | no |

(nav yes because `dashboardHelper.ts` carries a `route:` for each of these
four project cards.)

### content/play (4 files — all render)
| path | source | title | nav? | admin? | audited? |
|---|---|---|---|---|---|
| /play/challenges | content/play/challenges.md | Challenge Center | yes | no | no |
| /play/davinci | content/play/davinci.md | Da Vinci | yes | no | no |
| /play/memory | content/play/memory.md | Memory Dungeon | yes | no | no |
| /play/screenfx | content/play/screenfx.md | Screen FX | yes | no | no |

### content/build (3 files — all render)
| path | source | title | nav? | admin? | audited? |
|---|---|---|---|---|---|
| /build/animation-manager | content/build/animation-manager.md | Animation Manager | yes | no | no |
| /build/hair-studio | content/build/hair-studio.md | Hair Studio | yes | no | no |
| /build/mural | content/build/mural.md | Mural | yes | no | no |

### content/shop (2 files — all render)
| path | source | title | nav? | admin? | audited? |
|---|---|---|---|---|---|
| /shop/cancel | content/shop/cancel.md | Checkout Cancelled | no (Stripe redirect target) | no | no |
| /shop/success | content/shop/success.md | Payment Confirmation | no (Stripe redirect target) | no | no |

### content root (53 files) — grouped here by the `channelKey` each declares

**home** (11 render): /, /account, /achievements, /chats, /dashboard,
/for-you, /friends, /messages, /navigation, /register, /themes, /wallet
— all nav-reachable (channels/home). None audited except `/`.

**play** (14 render): /academy, /art*, /bots*, /characters*, /dreams*,
/facets, /resources (**shadowed**, see below), /rewards*, /sanctuary
(actually `channelKey: sanctuary`, see below), /serendipity, /stories,
/storybook, /taskmaster — all nav-reachable. `*` = in the audit default list.

**plan** (8 render): /appmaker, /brainstorm, /coloring, /conductor*,
/conductor-app, /model-builder, /packs, /stylist, /wishmaster — all
nav-reachable. `*` = in the audit default list.

**sanctuary** (5 render): /about, /cart, /giving, /mermaids, /privacy,
/sanctuary — all nav-reachable.

**admin** (5 render, all admin-only): /artjob, /navigation-health,
/project-placement, /scoop-cms, /user-admin — all `requiredRole: ADMIN` in
frontmatter, all nav-reachable (channels/admin), none audited.

**no channelKey declared** (10 files):

| path | source | title | nav? | admin? | audited? |
|---|---|---|---|---|---|
| /button | content/button.md | Button | **no — orphaned** | no | no |
| /error | content/error.md | Direction | **no — orphaned, and shadowed by pages/error.vue** | no | no |
| /forum | content/forum.md | Forum | yes (smartIcons) | no | no |
| /icons | content/icons.md | Icons | **no — orphaned** | no | no |
| /login | content/login.md | Login | **no — orphaned from the 3 registries**, but functionally always reachable (`pages/[...slug].vue` special-cases `isLoginPath`, and auth flows link here directly) | no | no |
| /reset-password | content/reset-password.md | Reset Password | **no — orphaned** (likely reached only via emailed reset link) | no | no |
| /servers | content/servers.md | Servers | yes (dashboardHelper `server` tab) | no | no |
| /stages | content/stages.md | Stages | **no — orphaned** | no | no |
| /ui | content/ui.md | UI Gallery | **no — orphaned** | no | no |

## Shadowed content (URL is reachable, but the content file never renders)

Two `content/**/*.md` files sit at the exact same literal path as a static
`pages/**/*.vue` file. Nuxt's file-based routing always wins, so these two
content files are dead — the URL works, but always renders the static page,
never the content:

| path | shadowed content file | winning static page |
|---|---|---|
| /resources | content/resources.md | pages/resources.vue |
| /error | content/error.md | pages/error.vue |

## Static pages (`pages/**/*.vue`, 18 files)

`[...slug].vue` is the catch-all mechanism itself, not a route, and is
excluded below.

| path | source | nav? | admin? | audited? | notes |
|---|---|---|---|---|---|
| /admin/achievement-art | pages/admin/achievement-art.vue | **no — orphaned**, zero inbound `NuxtLink` found anywhere in the repo | **yes** (`userStore.isAdmin` gate in-component) | no | |
| /admin/wonderlab-review-generator | pages/admin/wonderlab-review-generator.vue | **no — orphaned from primary nav**, only linked from its own admin-review sibling pages | **yes** | no | part of a 4-page cluster with no entry point from the main channel/dashboard nav |
| /admin/wonderlab-review-plan | pages/admin/wonderlab-review-plan.vue | same as above | **yes** | no | |
| /admin/wonderlab-review-rollout | pages/admin/wonderlab-review-rollout.vue | same as above | **yes** | no | |
| /admin/wonderlab-reviews | pages/admin/wonderlab-reviews.vue | same as above — cluster hub page, but nothing outside the cluster links to it either | **yes** | no | |
| /auth/google | pages/auth/google.vue | yes — linked from `components/user/google-login.vue` (login flow) | no | no | OAuth callback/entry, not a content surface |
| /build-bench | pages/build-bench.vue | yes (dashboardHelper `builder` dashboard, `build-bench` tab) | no | no | |
| /coloring-page | pages/coloring-page.vue | yes (dashboardHelper `art` dashboard, `coloring-page` tab) | no | no | |
| /email-confirmation | pages/email-confirmation.vue | **no — orphaned from in-app nav**; reached via emailed confirmation link only | no | no | |
| /error | pages/error.vue | **no — orphaned** | no | no | shadows content/error.md (see above) |
| /music-mentor | pages/music-mentor.vue | yes (channels/play/music-mentor.md `route:`) | no | no | |
| /plan/wonderlab/commentary-guide | pages/plan/wonderlab/commentary-guide.vue | **no — orphaned**, zero inbound `NuxtLink` found; `utils/scripts/verifyWonderLabCoreFixtures.ts` checks for a `content/channels/plan/commentary-guide.md` companion file that does not exist | no | no | |
| /play/challenges/leaderboard | pages/play/challenges/leaderboard.vue | yes — linked from `components/conductor/challenge-center-page.vue` | no | no | |
| /play/video-generator | pages/play/video-generator.vue | yes (channels/play/video-generator.md `route:`) | no | no | |
| /resources | pages/resources.vue | yes (channels/play/resources.md `route:`) | no | no | shadows content/resources.md (see above) |

## Dynamic / parameterized routes (2 patterns)

| pattern | source | representative example | nav? | admin? |
|---|---|---|---|---|
| /users/[id] | pages/users/[id].vue | `/users/1` — id is the numeric `User.id`; example usage: `components/wonderlab/component-review-feed.vue:279` | yes | no |
| /play/challenges/[slug] | pages/play/challenges/[slug].vue | `/play/challenges/neon-ramen-bar-icon` — slug from `scripts/seed_challenges.ts`; linked via `components/conductor/challenge-center-page.vue:143` | yes | no |

## Excluded: dev-only

| path (would-be) | source |
|---|---|
| /dev/missing-image-test | content/dev/missing-image-test.md |

## Gaps — reachable, nav-linked, non-admin, NOT in the audit's default list

This is the actionable backlog for t-103. All routes below pass every
filter (real route, nav-reachable, not admin-gated) but are absent from
`utils/scripts/auditResponsiveLayout.mjs`'s default `--routes` list.

**Content-driven, channel `home`:** /account, /achievements, /chats,
/dashboard, /for-you, /friends, /messages, /navigation, /register, /themes,
/wallet

**Content-driven, channel `play`:** /academy, /facets, /resources
(shadowed — an audit would actually measure `pages/resources.vue`),
/serendipity, /stories, /storybook, /taskmaster

**Content-driven, channel `plan`:** /appmaker, /brainstorm, /coloring,
/conductor-app, /model-builder, /packs, /stylist, /wishmaster,
/plan/newsfeed, /plan/voice-lab, /plan/watchlist, /plan/wonderlab,
/plan/projects/coat-dance, /plan/projects/humboldt-scoop,
/plan/projects/ruler-hooked, /plan/projects/sketchy

**Content-driven, channel `sanctuary`:** /about, /cart, /giving, /mermaids,
/privacy, /sanctuary

**Content-driven, no channelKey but nav-reachable:** /forum, /servers

**content/build (plan channel, via `route:` under content/build/*):**
/build/animation-manager, /build/hair-studio, /build/mural

**content/play subdir (play channel, via `route:` under content/play/*):**
/play/challenges, /play/davinci, /play/memory, /play/screenfx

**Static pages:** /auth/google, /build-bench, /coloring-page, /music-mentor,
/play/challenges/leaderboard, /play/video-generator

**Dynamic (one representative path each):** /users/1,
/play/challenges/neon-ramen-bar-icon

## Notes / things worth flagging beyond the inventory itself

- **`/scenarios` in the audit's default route list did not correspond to any
  real route.** The scenarios channel tab's actual `route:` is `/stories`
  (`content/channels/play/scenarios.md`), and `coreObjectRoutes.ts` already
  documents `// NOT /scenarios.` for exactly this reason. Every audit run
  against the default list was silently measuring a 404/not-found page for
  that eighth entry instead of the real Scenario surface. **Fixed in
  kind_robots #1559**, along with three live Dream-narrator navigation
  payloads in `narratorHelper.ts` that had the identical stale `/scenarios`
  path (the 'Scenarios' nav action, the 'New Scenario' builder create-spec,
  and the 'Tell me a story' starter prompt) — those were a real, live nav
  bug, not just an audit-tooling one.
- **`stores/helpers/dashboardHelper.ts`'s `footer` dashboard has a `builder`
  tab whose `route:` is `/builder`**, which matches no content file and no
  `pages/**/*.vue` file anywhere in the repo. `narratorHelper.ts`'s own
  `'builder'` nav action has the identical dead `/builder` path. Not fixed
  in #1559 — the correct destination isn't obvious (there's no single
  top-level page for the multi-tab Builder dashboard, whose tabs each route
  to their own entity page: `/dreams`, `/characters`, `/bots`, `/rewards`,
  `/stories`, `/art`). Filed as interface-vision/t-107.
- **Two content files are permanently shadowed and dead**: `content/error.md`
  and `content/resources.md` both lose to a same-path static page
  (`pages/error.vue`, `pages/resources.vue`) under Nuxt's routing
  precedence. `/resources` is nav-linked and heavily used, so whatever is in
  `content/resources.md` (title "Resources") has never actually rendered.
  Left as inventory data for t-103 rather than fixed here — deciding whether
  to delete the dead content file or repoint the static page needs product
  judgment this task didn't ask for.
- **The four `pages/admin/wonderlab-review-*.vue` pages,
  `pages/admin/achievement-art.vue`, and
  `pages/plan/wonderlab/commentary-guide.vue`** are reachable only by typing
  the URL directly (or via docs — `docs/wonderlab-personality-review-rollout.md`
  references `/admin/wonderlab-reviews` in prose) — none have a discoverable
  in-app entry point from the channel dropdown, a dashboard tab, or the
  smartbar. Flagged as orphaned rather than dropped, per the task brief
  ("admin-only surfaces come last").
