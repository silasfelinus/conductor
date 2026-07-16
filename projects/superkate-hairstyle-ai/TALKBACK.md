# TALKBACK — superkate-hairstyle-ai

Append-only cross-vetting log for the Hair Studio project. Never edit or delete prior entries.
Format is defined in the root `AGENTS.md` ("How to write a talkback entry").

## 2026-07-09 | Claude (Silas-directed) → Worker | superkate-hairstyle-ai/t-001 | pattern

**Subject:** Project created as an independent sibling of superkate-services-calculator.

**Detail:**
- Silas asked for a surprise Hair Studio feature for Hair by Superkate: upload/snap a client
  photo, pick color/style/enhance (any combo), send to the Kind Robots Kontext Comfy backend,
  get the same photo back with new hair; navigable loading; per-client before/after gallery.
- Made it a **new project** rather than folding into the calculator: different tech surface
  (generative image editing vs. Flutter appointment math), a different eventual monetization
  path (paid + free trial, possibly a separate app), and it keeps the deep calculator roadmap
  clean. Associated via DESIGN-BRIEF + shared customer-profile identity anchor.
- Verified the backend already exists: `POST /api/comfy/kontext/generate` takes `imageData` +
  `prompt` and returns the transformed `data.imageData`, gated by mana/`authAndGate`. MVP is
  frontend + prompt building + gallery only — no backend build needed.
- Recommended a **web-first surface in Kind Robots** (t-002, soft gate) because the Kontext
  backend and gallery infra live there and Flutter build/verify is human-gated (calculator
  t-014), which keeps stalling that roadmap.

**Suggested action:** Worker — start on t-003 (prompt-builder design) and t-004 (staged tab
shell). Keep everything behind a preview flag; the feature is a surprise for Superkate. Do NOT
build billing or reveal the feature — t-011/t-012 are hard human gates. Silas — answer t-002
(web-first vs Flutter-first) when convenient; the team proceeds web-first meanwhile.

## 2026-07-09 | Claude (Silas-directed) → Worker | superkate-hairstyle-ai/t-004..t-008 | pattern

**Subject:** First working cut of the Hair Studio tab landed in kind_robots (branch
claude/superkate-hairstyle-ai-nse06o). Silas confirmed web-first.

**Detail:**
- Reused existing infra instead of building a model backend: artStore.generateArt with
  engine:'kontext' already generates via /api/comfy/kontext/generate AND persists the result
  via /api/art/save-generated. art-styler.vue was the working reference for kontext + server
  resolution. New surface is a thin component + config, no backend work.
- Privacy requirement satisfied structurally: every generated ArtImage is saved with
  isPublic:false, so client photos never surface in public galleries or the memory-match game
  (the game/getters filter on image.isPublic). Tagged designer "stylist:<client>" for later
  per-client grouping.
- Files: components/art/stylist-manager.vue, content/stylist.md (/stylist → :stylist-manager),
  dashboardHelper "stylist" tab (route /stylist), tutorialCards "stylist" art section, and two
  placeholder webp tab/tutorial images (real art queued in art-prompts.yaml requests).
- Fixed a reactivity bug pre-commit: was mutating a raw object after pushing it into a ref
  array (Vue 3 proxy won't track that) — switched to patchResult(id, patch) by id.

**Flags for Reviewer / Silas:**
- NOT verified in a running app — no local build env (no node_modules) and no live Comfy
  server here. Typecheck/lint could not run. Needs a real run before merge to main.
- The tab is registered in the art dashboard config but is NOT yet behind a preview/role flag,
  so it is technically reachable. The surprise constraint wants it hidden from Superkate until
  Silas approves the reveal — added as a follow-up under t-012 and noted on t-004.
- Client field is free text for now; binding to real calculator customer profiles is the
  cross-project coordination in t-008.

**Suggested action:** Silas — run kind_robots locally (or a preview deploy) with an active
Comfy/Kontext server and try /stylist end-to-end; confirm results save private. Worker — pick
up t-007 (store-level background job so it survives leaving the tab) and t-008 (durable
per-client gallery) next.

## 2026-07-09 | Claude (Silas-directed) → Worker | superkate-hairstyle-ai/t-007+t-008 | pattern

**Subject:** t-007 (navigable async) done and t-008 (durable per-client gallery) first cut, via a
dedicated stylistStore. kind_robots PR #134.

**Detail:**
- Root fix for "navigable while waiting": job state was component-local and died on tab switch.
  Moved it into stores/stylistStore.ts, so the generateArt promise resolves against the store
  even after the component unmounts — the result lands when Superkate returns to /stylist. This
  is the correct Pinia pattern (store outlives component lifecycle).
- t-008 first cut: durable "Past looks for <client>" loads the user's saved private stylist
  images (GET /api/art/user/:id, filtered by the "stylist:" designer tag) and groups by client.
- Honest gap called out and turned into t-013: save-generated only persists the RESULT, so the
  before image isn't durable and the client key is still a free-text tag. Full durable
  before/after + real customer-profile link needs the source saved and cross-project
  coordination with the calculator.

**Flags for Reviewer / Silas:**
- Still not runtime-verified (no node_modules / live Comfy server in this environment). Followed
  existing artStore + performFetch conventions and self-reviewed reactivity (store refs read
  inside component computeds track correctly). Needs a real /stylist run.

**Suggested action:** Silas — merge #134 after a local /stylist smoke test. Next up unless you
redirect: t-009 (harden Kontext API client error/timeout/mana states) and t-010 (polish
empty/loading/error + before/after compare), then t-013.

## 2026-07-09 | Claude (Silas-directed) → system | superkate-hairstyle-ai dashboard bugfix | pattern

**Subject:** Live-run feedback from Silas surfaced two dashboard bugs; diagnosed and fixed in
kind_robots PR #136. PRs #133/#134 merged by Silas — t-004..t-009 are done.

**Detail:**
- Bug 1: selecting the Hair Studio tab still showed the image generator. The dashboard header's
  tab buttons only set store state (no navigation); art-manager renders the active tab
  internally and its validTabs didn't include "stylist", so it fell back to "generate". Fix:
  stylist renders inline in art-manager like every other art tab.
- Bug 2: returning to the Art channel forgot the remembered tab. content/art.md pinned
  dashboardTab: generate — a VALID art tab — so every /art visit force-reset tab memory via
  setDashboardShellFromContent + the header's route-enforced watch. Other channels' landing
  pages carry non-tab hints (bots.md → "overview"), which is why only Art misbehaved. Fix:
  setDashboardShellFromContent only enforces a frontmatter tab that names a real tab of that
  dashboard (page-as-tab identity, e.g. /stylist, /memory); otherwise it preserves the
  remembered tab. art.md no longer pins a tab.
- Ops note: the git relay's push path failed persistently this session (hangups/413); the fix
  went up via the GitHub API (push_files), which also normalized navStore.ts and
  art-manager.vue from legacy CRLF to the .gitattributes-declared LF — PR #136 flags to review
  with whitespace hidden.

**Suggested action:** Silas — merge #136, hard-refresh, and retest: pick Hair Studio (should
render in place), hop to Rewards and back to Art (should return to Hair Studio). Worker — next
up: t-013 (durable before/after source persistence + real client link) and t-010 (state polish).

## 2026-07-09 | Claude (Silas-directed) → system | superkate-hairstyle-ai/t-014 | pattern

**Subject:** Production styling failed (ENOTFOUND on the ts.net Comfy host from Vercel).
Root-caused and re-routed through the durable ArtJob queue. kind_robots PR #138 + relay
change on conductor PR #320. Silas also expanded scope: full Superkate app replica on the
Hair Studio page (t-015, claimed).

**Detail:**
- The direct /api/comfy/kontext/generate route dials the Comfy box from the deployed backend,
  which is not on the home tailnet — ts.net names don't resolve there. The repo already had
  the working pattern: the ArtJob queue that ops/home-server/relay_agent.py claims OUTWARD
  (pull model, no inbound path, "all policy lives in kind_robots").
- New /api/comfy/kontext/enqueue: mana-gated at enqueue, job payload carries the kontext
  workflow + input image + a save block. relay_agent.py gained stdlib multipart upload of
  payload images to ComfyUI's input folder (LoadImage support — image-to-image jobs).
- Ownership subtlety: save-generated rejects foreign userIds, so relay uploads land owned by
  the relay machine user. The queue COMPLETE endpoint (already admin-gated) now applies the
  job's save block + ownership by the enqueuing user — keeping stylist photos private and in
  Superkate's Past-looks history. Legacy jobs without a save block are untouched.
- DEPLOY STEP FOR SILAS: restart the home relay agent with the updated relay_agent.py after
  merging, or queued stylist jobs will fail at the LoadImage node.

**Suggested action:** Silas — merge kind_robots #138 + conductor #320, update the home relay
agent, then run /stylist on the deployed site end-to-end. Claude — t-015 (full app replica
suite on /stylist: Calculator | Clients | History | Hair Studio) is in progress.

## 2026-07-09 | Claude (Silas-directed) → system | superkate-hairstyle-ai/t-015 | pattern

**Subject:** Full Superkate app replica built on /stylist (kind_robots PR #138, part 2).

**Detail:**
- New suite shell on /stylist: Hair Studio | Calculator | Clients | History, view choice held
  at store level so it survives navigation (consistent with the dashboard-tab fix).
- superkateStore is the approved "easy mock": localStorage-persisted customers, appointments,
  and receipt settings. Calculator SPEC honored — rate x time + products in cents, hours/
  minutes preset chips, product cost optional defaulting to $0.00, warm receipt with the
  configurable contact block (glossgenius link + reply email) and "Superkate loves you!",
  mailto composer with client email prefill, and the delete-detach invariant from calculator
  t-031's test list.
- Cross-feature tie-in: the restyler's Client field now suggests names from the client book —
  first step toward the t-013 real client-identity link.
- Follow-up (not this PR): replace localStorage with KR-model-backed persistence so Superkate's
  book syncs across devices; that is where the "1-1 it somehow" upgrade lands.

**Suggested action:** Silas — one review pass on kind_robots #138 covers both the prod
generation fix and the suite; remember to restart the home relay agent with the updated
relay_agent.py (conductor #320) or queued styling jobs will fail at the LoadImage node.

## 2026-07-10 | Claude (Silas-directed) → system | superkate-hairstyle-ai meantime upgrades | pattern

**Subject:** Silas merged kind_robots #138 and conductor #320 (t-014/t-015 done — the queue
generation path and the full suite are on main for his live test). Meantime upgrades shipped:
kind_robots PR #141 + conductor PR #326.

**Detail:**
- t-013 first half solved with no schema change: the source photo already travels in each
  ArtJob payload, so stylistStore recovers befores from the user's DONE queue jobs and Past
  looks gained a tap-to-flip Before/After compare (also satisfies t-010's compare requirement).
- New Settings view in the suite: editable salon name / booking link / reply contact per the
  calculator SPEC, with live receipt preview.
- Relay hardening: upload_comfy_input_images refactored into pure helpers with 14 new pytest
  cases (multipart shape, data-URL handling, error paths). Conductor suite: 86 passed.
- Remaining before public/paid: t-013 second half (real client-identity link), t-010 leftovers,
  KR-model-backed persistence for the suite (replace localStorage), t-011/t-012 human gates.

**Suggested action:** Silas — live-test /stylist on main (remember the relay agent restart),
then merge #141 and #326 at leisure; both are additive. Claude — next: KR-backed persistence
for the suite so Superkate's client book syncs across devices.

## 2026-07-10 | Claude (Silas-directed) → system | superkate-hairstyle-ai/t-016 | pattern

**Subject:** KR-backed persistence shipped (kind_robots PR #141 extended) — and the work
environment finally has a full toolchain, so this batch is typechecked and linted.

**Detail:**
- t-016: StylistClient + StylistAppointment tables (additive-only migration), owner-checked
  /api/stylist/* CRUD, and a write-through superkateStore: local cache hydrates instantly,
  server copy loads for signed-in users, pre-existing local data migrates up on first sync,
  guests/offline stay local-only. Suite header shows syncing/synced with graceful fallback.
- Verification milestone: npm install restored node_modules, so `npm run test` (full vue-tsc)
  and eslint now run — both pass clean across every file this project has touched. prisma
  generate ran against the new schema (generated client is committed per repo convention).
  The typecheck caught one latent bug from the queue PR (ArtJob Json payload cast) — fixed.
- Migration note for the Reviewer/Silas: 20260710020000_add_stylist_suite is CREATE TABLE +
  ADD CONSTRAINT only (~45 lines) — the class of migration AGENTS.md permits merging after a
  line-by-line audit. Merge deploys it via prisma migrate deploy.

**Suggested action:** Silas — kind_robots #141 now carries persistence + before/after compare +
settings; conductor #326 is the relay test hardening. After merging, a hard refresh on /stylist
should show "synced" in the suite header when signed in. Remaining roadmap: t-013 second half
(client-identity link now natural via StylistClient ids), t-010 leftovers, t-011/t-012 gates.

## 2026-07-10 | Claude (Silas-directed) → system | superkate-hairstyle-ai t-010/t-013 + relay guard | pattern

**Subject:** While Silas is away from the relay (~6h): t-013 completed (rename-proof client
links), t-010 completed (first-run hint was the last gap), and a stale-relay guard added so
nothing breaks in the meantime.

**Detail:**
- t-013: styled photos now carry the synced StylistClient id in their designer tag
  ("stylist:Alex#42"); history matches by id first, name second, so renames don't orphan a
  client's looks and legacy tags keep working.
- Stale-relay guard: the claim endpoint only hands image-carrying jobs (Hair Studio) to agents
  declaring supportsInputImages — the OLD relay would otherwise claim them, fail LoadImage
  three times, and land them FAILED. Now they wait patiently until the updated agent starts.
  Relay declares the capability; test added (suite: 87 passed).
- Ops runbook added to ops/home-server/README.md: exact pm2 restart steps and the log lines
  that prove a styling ran end-to-end — the relay restart is a 2-minute job when Silas is home.
- All kind_robots changes typechecked (full vue-tsc) and linted before push.

**Suggested action:** Silas — merge kind_robots #141 and conductor #326 whenever; the deployed
site is safe either way thanks to the claim guard. When home: git pull conductor on the home
server, pm2 restart kr-relay, then style something in /stylist and watch the logs per the
runbook. Remaining roadmap after that: t-011/t-012 human gates only.

## 2026-07-10 | Claude (Silas-directed) → system | superkate-hairstyle-ai first live test | pattern

**Subject:** First live styling stalled — job enqueued, never completed. Diagnosed overnight;
most probable cause is a handshake version gap, not a code defect. Fixes + observability
shipped (kind_robots PR #145, conductor runbook triage table).

**Detail:**
- Evidence: "it is adding as an art job" = enqueue path (mana gate, workflow build, ArtJob
  create) works in production, including the new tables/migration. The job then never left
  PENDING (or was never observed completing).
- Probable cause: kind_robots #141 (claim guard requiring supportsInputImages) merged 08:47;
  conductor #326 (the agent DECLARING that capability) merged 08:53. A relay pulled/restarted
  between those knows how to upload input images but never receives image jobs — the guard
  skips it by design. One more conductor pull + pm2 restart resolves it, and the stalled job
  completes on its own (durable queue doing its job).
- Shipped while Silas sleeps (kind_robots PR #145): job tiles now show live queue state
  (queued vs rendering) + a stalled-queue warning after 60s, so this exact triage is readable
  from the UI; client-side photo downscaling (1280px JPEG) to preempt request-size limits on
  phone photos; and a CI fix — main's `satisfies Prisma.InputJsonValue` refactor of
  enqueue.post.ts didn't compile (runtime unaffected; builds don't typecheck).
- Runbook gained a symptom→cause→fix triage table for this incident class.

**Suggested action:** Silas (morning): (1) home server: git pull conductor + pm2 restart
kr-relay — watch the stalled job complete; (2) merge kind_robots #145 and this conductor PR;
(3) rerun a styling and confirm the tile goes queued → rendering → done. If it instead goes
rendering → failed, the ComfyUI error will be in pm2 logs — paste it to the session.

## 2026-07-10 | Reviewer → Worker | superkate-hairstyle-ai stall-triage PRs | critique

**Decision:** merged conductor #341 (squash 23d2472) and kind_robots #145 (squash 45ecf07)

**What was good:**
- Root-cause diagnosis (6-minute merge gap between the claim guard #141 and the capability declaration #326) is specific, time-stamped, and falsifiable — with the honest caveat that the stalled job completes on its own
- Observability follows the incident: queue-state badges + a 60s stall warning make this exact failure readable from the UI without pm2 access
- The CI typecheck fix casts at the boundary matching the existing /api/art/queue pattern instead of inventing a new one; interval timer is cleaned up in onBeforeUnmount

**What to improve:**
- Photo downscaling silently falls back to the raw image on decode error — fine, but a debug log would help if the request-size limit ever bites anyway

**Kaizen task:** superkate-hairstyle-ai/t-017 — surface the relay's declared capabilities on an admin status readout so version-gap stalls are visible without shell access

## 2026-07-10 | Reviewer → system | superkate-hairstyle-ai t-010/t-013/t-016 | pattern
type: pattern

**Decision:** audited already-merged work (kind_robots PR #141, merged by Silas 08:47) — no
new merge to perform, roadmap reconciled to match reality.

**Detail:**
- This Reviewer session was triggered expecting an open worker/* PR; none existed in either
  repo (list_pull_requests returned zero for conductor and kind_robots), matching the pattern
  already flagged in conductor/t-026.
- Instead found real stale state: t-010, t-013, and t-016 were still `status: review` even
  though PR #141 — and the TALKBACK entries describing t-010/t-013 as "completed" — landed on
  main over 5 hours earlier. The roadmap was never flipped after the PR merged.
- Audited the migration this session hadn't yet reviewed: `20260710020000_add_stylist_suite`
  is exactly two `CREATE TABLE` statements + three `ADD CONSTRAINT` (FK) statements, no
  `DROP`/rewrite of existing data — satisfies the additive-only bar for a Reviewer-mergeable
  migration (it already shipped to prod via `prisma migrate deploy` on merge; audit here is
  after the fact but the migration reads exactly as documented in the PR body and TALKBACK).
- Set t-010, t-013, t-016 to `status: done` with notes citing PR #141 directly.

**What to improve:**
- When a Silas-directed session merges its own PR and marks work "completed" in TALKBACK, it
  should flip the roadmap task status in the same commit — don't leave that for a future
  Reviewer sweep to discover by cross-referencing TALKBACK against roadmap.yaml.

**Kaizen task:** deferred — conductor/t-026 already covers the broader "Reviewer triggered
with nothing to review" pattern; no new task needed for this specific staleness, since it's
a one-time reconciliation rather than a recurring gap (the sessions that did this work were
Silas-directed, not a repeating Worker mistake).

## 2026-07-16 | Reviewer → Worker | superkate-hairstyle-ai/t-017 | pattern (conductor burst cycle)

type: pattern

**Decision:** merged (Silas merged kind_robots PR #317 directly). Closing out the roadmap
task to `done` from this session since it claimed and delegated the implementation.

**Detail:**
- Claimed via `claim_task.py` (worker/claude-conductor-burst-20260716-sh017) as the burst-mode
  pick this cycle, chosen deliberately over the top-priority `next_ready_task.py` result
  (ai-art-academy/t-008) — that task is a known, repeatedly-documented sandbox egress block
  (metmuseum.org/upload.wikimedia.org 403 via the agent proxy), and this cycle's routine asked
  for rotation across projects rather than re-hitting the same blocked task a fifth time.
  `global-ui/t-018` was also skipped — a concurrent session had it claimed at the time
  (confirmed via its `claimed_at` timestamp being well inside the 90-minute TTL, and it
  resolved independently as conductor PR #633 / kind_robots #316).
- Implementation used an in-memory (module-level `Map`) registry rather than a new Prisma
  model/migration — the task's data (relay last-seen + declared capabilities) is ephemeral
  operational telemetry, not something needing DB durability or cross-install sync, and this
  sandbox has no reliable live-DB path to author/verify a migration against. Scoped
  deliberately smaller than "add a RelayAgent table" to keep the PR landable in one sandbox
  session with real (typecheck/lint/focused-test) verification instead of claimed-but-unrun
  DB-backed verification.
- Verification gap, disclosed honestly in the PR body: no live DB/dev server or real relay
  available in this sandbox, so the claim endpoint's DB-backed path and the new panel's live
  fetch were not exercised end-to-end; Cypress e2e didn't run (binary download blocked by
  sandbox egress). `npm run test:relay-agent-registry`, full `vue-tsc` typecheck, and
  lint/prettier on touched files were all run and are clean.

**What was good:**
- Correctly scoped around a known constraint (no DB migration risk in an unverifiable
  sandbox) instead of attempting a DB-backed design that couldn't be tested here.
- PR body's "Not verified" section states the live-fetch/relay gap plainly instead of
  implying full verification.

**What to improve:**
- None new this cycle — first pass, clean typecheck/lint, no rejection.

**Kaizen task:** `superkate-hairstyle-ai/t-020` — flag relays that stopped polling entirely
(not just ones missing a declared capability) on the new admin panel, mirroring
`queue/stats.get.ts`'s `STALE_CLAIM_MINUTES` pattern.
