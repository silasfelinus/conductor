# animation-manager — TALKBACK

Append-only. See root AGENTS.md for format and rules.

## 2026-07-20 | Reviewer → Worker | animation-manager/t-005 | pattern

type: pattern

**Subject:** New WonderLab-style content routes need two registrations, not one — CI (Contract verifiers) caught the miss on first push.

**Detail:**
- t-005 added `content/animation-manager.md` (the route mount, with `channelKey: lab` / `tabKey: animation-manager` in frontmatter) plus the front-end nav wiring (`dashboardHelper.ts`'s `wonder` tab list, `lab-manager.vue`'s tab switch, `tutorialCards.ts`). That combination is enough to make the page navigable in the UI, but `utils/scripts/verifyChannelContent.ts` (run in CI as `test:channel-content`, part of the Contract Tests job) separately requires a matching `content/channels/<channelKey>/<tabKey>.md` document with `contentType: tab` — the *content-system* tab registration, distinct from the *dashboard-nav* tab registration.
- First push failed CI with `content/animation-manager.md: references unknown tab lab/animation-manager`. Fixed in a follow-up commit by adding `content/channels/lab/animation-manager.md` mirroring `screen-fx.md`'s shape (same `channelKey`/`tabKey`/`route`, next `sort` value). Second push was clean.
- No rework needed beyond the one follow-up commit — the fix was well-scoped and caught before merge, exactly as CI is supposed to work. Logged as a `LEARNING.yaml` lesson (quality/passes-0, since it was caught and fixed within the same PR cycle without a Reviewer rejection) so the next agent adding a WonderLab tab checks for the `content/channels/<channel>/` directory up front instead of discovering the gap via a CI failure.

**Suggested action:** When wiring a new dashboard tab that also needs a route-mounted content page, check `content/channels/<channelKey>/` for the tab-registration convention before writing the route mount — `screen-fx.md` + `content/channels/lab/screen-fx.md` is the reference pair to copy from.

## 2026-07-20 | Reviewer → Worker | animation-manager/t-005 | critique

type: critique

**Decision:** merged (kind_robots PR #590, squash ad145742, after one CI-driven follow-up commit)

**Failure category:** n/a (self-reviewed/self-merged single-session Worker+Reviewer run; no Reviewer rejection occurred)

**What was good:**
- Explored the existing Component/Reaction/animationCatalog infrastructure (already built by t-004) thoroughly before writing any UI code, and reused `components/wonderlab/component-card.vue` wholesale instead of building a duplicate card component — kept the diff smaller and the Reaction-rating display consistent with the rest of WonderLab.
- Followed the task's literal "use an animationManagerStore" instruction while still avoiding a second CRUD/API layer — the store is a thin composition over `componentStore`/`animationStore`/`animationCatalog`, not a duplicate registry.
- Ran the full relevant contract-test surface locally (`vue-tsc`, `eslint`, and 26 individual `test:*` scripts covering channel-content, channel-resolver, tutorial-channel-resolver, every `wonderlab-*` fixture suite, animation-catalog, and animation-component-attempts) both before the first push and again after the CI-driven fix, rather than assuming a clean typecheck was sufficient.
- Flagged two deliberate scope cuts in the PR body instead of silently under-delivering: no fabricated "conductor pitch status" data (linked to `/conductor` instead, since no kind_robots API exposes `PITCHES.yaml`), and no auto-supersession on promote (left as a named kaizen task rather than guessed at).

**What to improve:**
- Before the first push, only `vue-tsc` (`npm run test`) and `eslint` were run locally — not `npm run test:channel-content` or any of the other repo-specific `test:*` contract scripts wired into `contract-tests.yml`. That gap is exactly why the missing tab registration reached CI instead of being caught locally: vue-tsc has no opinion on content-frontmatter conventions. Once the failure surfaced, the full relevant `test:*` surface was identified from `.github/workflows/contract-tests.yml` and run locally for the fix — that should be step zero for any PR touching `content/` or `stores/helpers/*.ts` in this repo, not a reaction to a CI failure.

**Kaizen task:** t-012 — Auto-supersede the prior WORKING build when Animation Manager promotes a new one (from the Worker's own kaizen suggestion in the PR body).

## 2026-07-20 | Worker (conductor burst session) | animation-manager/t-007 | pattern

**Decision:** merged (kind_robots PR #627, squash 398a327a, single clean push, all 3 CI checks passed first try).

**Failure category:** none — no CI failure, no rework.

**What was good:**
- Read the shipped `bioluminescent-tide.vue` build first and matched its structure (ResizeObserver sizing, capped DPR, `prefers-reduced-motion` listener, full RAF/observer/listener cleanup on unmount) instead of inventing a new shape, so the new effect fits the existing review bar.
- Followed the "cache repeated lantern shapes" performance-risk note from the pitch literally: lantern silhouettes are `Path2D` objects cached by rounded-radius bucket in a `Map`, built once and reused every frame rather than reconstructed per lantern per frame.
- Ran the full locally-runnable verification surface before pushing (learned from t-005's TALKBACK entry above): `npm test` (vue-tsc), eslint, `test:animation-catalog`, and `test:animation-component-attempts` — not just typecheck.
- Discovered the branch's local checkout had diverged from `origin/main` with no common ancestor (a force-pushed remote history) before pushing, not after a rejected push — reset the branch onto current `origin/main` and reapplied the two changed files rather than fighting an unrelated-histories merge.
- Attempted a real live-browser smoke test (a temporary throwaway page mounting just the new component, deleted before commit) rather than assuming the DB blocker applied without checking; confirmed it's a global SSR/DB-missing 500 on every route, not something specific to this change, and documented that precisely instead of hand-waving "couldn't verify."

**What to improve:**
- The live browser smoke test and the `Component` attempt record (SPEC.md's "Attempt records" step) are both still deferred — this sandbox has no reachable `DATABASE_URL`. Whoever next has DB access should run the smoke matrix (`docs/architecture/animation-catalog-smoke-matrix.md`) against Screen FX and startup-wallpaper surfaces and create the `paper-lantern-weather@v1` attempt record, then flip `PITCHES.yaml`'s build entry from `candidate` to `shipped`.

**Kaizen task:** none new this cycle.
