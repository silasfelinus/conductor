# superkate-hairstyle-ai — task history archive

Full `note:` prose for completed superkate-hairstyle-ai tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Write the design brief and start building

<!-- note:begin t-001 -->
DONE (2026-07-09, Silas-directed Claude session): wrote DESIGN-BRIEF.md — what Hair Studio is, who it serves, the surprise constraint, the web-first-in-Kind-Robots surface recommendation, the existing Kontext backend contract, the color/style/enhance prompt builder, the async/navigable-loading requirement, the per-client gallery decision (reuse the ArtCollection pattern anchored to the calculator customer profile), and the ChatGPT/Claude/Silas responsibility split. Registered the project in priority.yaml and project-overrides.yaml and queued icon/card/hero art in ART-PROMPTS.md + art-prompts.yaml.
<!-- note:end t-001 -->

## t-003 — Design the color/style/enhance prompt builder + Kontext param mapping

<!-- note:begin t-003 -->
DONE (2026-07-09): implemented directly in stylist-manager.vue rather than a standalone doc. buildPrompt() merges the three toggle clauses (change hair color to X / restyle as Y / improve overall photo quality+lighting+sharpness) with a free-text slot and a fixed identity-preservation suffix ("keep the same person, same face and identity, natural photorealistic result"), routed through artStore.generateArt engine:'kontext' → /api/comfy/kontext/generate. The templates + contract are documented in DESIGN-BRIEF.md.
<!-- note:end t-003 -->

## t-004 — Build the Hair Studio tab shell + navigation entry (staged/flagged)

<!-- note:begin t-004 -->
DONE (PR #133 merged by Silas 2026-07-09): added content/stylist.md (/stylist page embedding :stylist-manager), a "stylist"/"Hair Studio" tab under the art dashboard (dashboardHelper, route /stylist), an art tutorial-channel "stylist" section, and placeholder tab/tutorial webp images (real art queued in art-prompts.yaml requests). The tab is registered in the art dashboard normally — Silas clarified (2026-07-09) the "surprise" is just flavor (Superkate doesn't know it's coming); it needs NO preview/role gating. Not verified in a running app (no local build env / live Comfy server).
<!-- note:end t-004 -->

## t-005 — Image intake — upload + camera capture tied to a client

<!-- note:begin t-005 -->
DONE (PR #133 merged by Silas 2026-07-09): stylist-manager.vue has upload (click + drag/drop) and camera capture (getUserMedia → canvas → data URL) with a preview and a free-text Client field, plus a camera-unavailable fallback to upload. Produces the data URL the Kontext endpoint expects. Follow-up: bind the Client field to real calculator customer profiles instead of free text (coordination with superkate-services-calculator) — tracked under t-008.
<!-- note:end t-005 -->

## t-006 — Transformation controls → prompt builder (color / style / enhance, any combo)

<!-- note:begin t-006 -->
DONE (PR #133 merged by Silas 2026-07-09): three independent checkboxes (change color + color field, change style + style field, improve overall image) plus a free-text notes field, merged by buildPrompt() into one Kontext prompt with the identity-preservation suffix. A plain-language changeSummary previews what will change; Style-it is disabled until a photo is present AND at least one option is selected.
<!-- note:end t-006 -->

## t-007 — Async generation with navigable loading state

<!-- note:begin t-007 -->
DONE (PR #134 merged by Silas 2026-07-09): job state moved to a dedicated stylistStore, so a styling job keeps running and its result still lands even when Superkate leaves and returns to the /stylist tab (the component is now a view over the store; store actions outlive component unmount). jobs[] carry pending/done/failed with retry + dismiss, filtered per client. This is the true "leave and come back" behavior the task asked for. Pending runtime verification (no local build env / live Comfy server in the authoring environment).
<!-- note:end t-007 -->

## t-008 — Per-client transformation gallery (before/after + metadata)

<!-- note:begin t-008 -->
DONE first cut (PR #134 merged by Silas 2026-07-09): a durable "Past looks for <client>" gallery loads the user's saved private stylist results across sessions (GET /api/art/user/:id, filtered by the "stylist:" designer tag, grouped by client) alongside the live before/after session grid. REMAINING (a follow-up, see t-013): the *before* image isn't persisted across sessions — save-generated only stores the generated result — so the durable view shows past RESULTS, not durable before/after pairs; and the client key is still a free-text tag rather than a real calculator customer-profile link. Full durable before/after needs the source image saved too (coordinate with the calculator project).
<!-- note:end t-008 -->

## t-009 — Kontext API client — mana/gate handling, error + timeout states

<!-- note:begin t-009 -->
DONE (PR #134 merged by Silas 2026-07-09): the store already routes through artStore.generateArt → /api/comfy/kontext/generate (performFetch retries + 180s timeout), and every failure lands on the job tile with a Retry action. Added friendlyError() mapping the real first-run failure modes — insufficient mana, no active Comfy/Kontext server, timeout, and not-signed-in — to actionable messages. Still runs under the studio KR account; no per-client billing (that's t-011, human-gated). Pending runtime verification.
<!-- note:end t-009 -->

## t-011 — PLAN paid gating + free trial (do NOT implement billing)

<!-- note:begin t-011 -->
FOR SILAS: human-gated PLANNING only. Before Hair Studio charges anyone, Silas decides: free-trial shape (how many free generations), price/service charge, whether this stays inside Hair by Superkate or spins into a separate app, which account/billing rails (Kind Robots mana vs external), and access control for non-Superkate users. Agents may write the plan doc but must NOT wire real billing, payment, signup, or production access. TO APPROVE a build step: Silas leaves a concrete decision in this note and creates a scoped reversible follow-up task; nothing bills money without that.
DONE 2026-07-25: Silas — "this project is low priority, literally just make choices and run with it." Wrote BILLING-PLAN.md with concrete defaults: 3 free transformations per user, then billed via the EXISTING Kind Robots mana rail (no new payment infra — Hair Studio already charges mana per Kontext call for the internal phase, public launch just keeps that), stays inside Hair by Superkate (no separate-app spin-off), no special access gate beyond normal Kind Robots auth. No billing code, signup flow, or production access touched — plan doc only, per this task's own explicit boundary. Unblocks t-012 (public launch readiness) once someone's ready to flip the switch — that task still needs its own explicit go-ahead.
<!-- note:end t-011 -->

## t-013 — Persist the source photo for durable before/after + real client link

<!-- note:begin t-013 -->
DONE — kind_robots PR #141 merged (2026-07-10 08:47): durable before/after achieved with no schema change (source photo already travels in each ArtJob payload; stylistStore recovers befores from DONE queue jobs; Past looks gained tap-to-flip Before/After compare), AND the real client-identity link landed in the same PR — styled photos now carry the synced StylistClient id in their designer tag ("stylist:Alex#42"); history matches by id first, name second, so renames don't orphan a client's looks and legacy tags keep working. Reviewer audit (2026-07-10): closing out — roadmap had been left at status: review after the PR merged.
<!-- note:end t-013 -->

## t-014 — Route generation through the ArtJob queue (prod tailnet fix)

<!-- note:begin t-014 -->
DONE (kind_robots PR #138 + conductor PR #320, both merged by Silas 2026-07-09/10): production styling failed with ENOTFOUND on the ts.net Comfy hostname — the deployed backend is not on the home tailnet. Fix uses the existing durable ArtJob queue: new /api/comfy/kontext/enqueue (mana-gated, workflow + input image + save block in the job payload), stylistStore enqueues and polls /api/art/queue/:id, the queue complete endpoint applies isPublic:false + designer + ownership to the uploaded ArtImage, and relay_agent.py gains input-image upload to ComfyUI. TO VERIFY: deploy updated relay_agent.py on the home server, merge both PRs, then run /stylist on the deployed site end-to-end.
<!-- note:end t-014 -->

## t-015 — Replicate the full Superkate app on the Hair Studio page

<!-- note:begin t-015 -->
DONE (kind_robots PR #138, merged by Silas 2026-07-10): built the sub-tabbed suite on /stylist — Hair Studio | Calculator | Clients | History — backed by a new localStorage-persisted superkateStore (the approved easy mock; KR-model sync is the follow-up). Implements the calculator SPEC core formula (rate x time + products, cents), hours/minutes preset chips, optional product cost defaulting to $0.00, client book with optional email, appointment search by client/date, warm receipts with the configurable contact block + "Superkate loves you!" and a mailto composer with email prefill, and the delete-detach invariant. The restyler's client field suggests known clients from the book. Not runtime-verified in this environment.
<!-- note:end t-015 -->

## t-016 — KR-backed persistence for the suite (synced client book)

<!-- note:begin t-016 -->
DONE — kind_robots PR #141 merged (2026-07-10 08:47): replaces the suite's localStorage mock for signed-in users with real Kind Robots persistence — new additive-only StylistClient + StylistAppointment tables (migration 20260710020000, CREATE TABLE + FKs only), owner-checked /api/stylist/* CRUD (server owns the money math), and a write-through store that migrates pre-existing local data up on first sync and falls back to local-only for guests/offline. Reviewer audit (2026-07-10): read migration.sql line-by-line — two CREATE TABLE statements + three ADD CONSTRAINT (FK) statements only, no DROP/rewrite of existing data; satisfies the additive-only bar for Reviewer-mergeable migrations. Migration deployed via prisma migrate deploy on merge. Closing out — roadmap had been left at status: review after the PR merged.
<!-- note:end t-016 -->

## t-017 — Surface the home relay's declared capabilities and last-claim time on an admin status readout

<!-- note:begin t-017 -->
Kaizen from the 2026-07-10 first-live-test stall (conductor #341 / kind_robots #145): the queue guard skips agents that don't declare supportsInputImages, which is invisible without pm2 access. Add a small admin-only readout (e.g. on /stylist or an /admin surface) showing each known relay agent's last claim attempt, declared capabilities, and agent version, so a version-gap stall is diagnosable from the browser. Delivered in kind_robots PR #317 (merged): server/utils/relayAgentRegistry.ts + GET /api/art/queue/relay-status + admin-gated Diagnostics tab on /stylist (stylist-relay-status.vue).
<!-- note:end t-017 -->

## t-018 — Hair-mask SOURCE for true hair-only restyling (auto-seg or brush)

<!-- note:begin t-018 -->
RESOLVED 2026-07-19 (Silas-directed agent run): picked option (b) from this task's own note — a manual freehand brush instead of MediaPipe auto-segmentation, since the brush needs no new npm dependency/model download and ships in one pass. New components/art/stylist-mask-brush.vue paints a mask on an offscreen canvas at the source photo's NATURAL resolution (independent of the preview's letterboxed CSS display size), so the exported mask lines up pixel-for-pixel with what the relay uploads regardless of aspect-fit letterboxing. stylist-restyle.vue gained an opt-in 'Only restyle the hair' toggle wired to the already-existing (previously unused) maskData plumbing (stylistStore.ts, enqueue.post.ts, workflow.ts's LoadImageMask/SetLatentNoiseMask). Verified via vue-tsc + eslint (clean); could not verify live in a browser since this sandbox has no real DATABASE_URL and /stylist is ADMIN-gated (confirmed sandbox-wide, not change-specific: the home page 500s identically). Merged kind_robots PR #504 (self-merged, Contract Tests + TypeScript Type Check both green). No Cypress coverage exists for stylist-restyle.vue (pre-existing gap, not introduced here) -- flagged as this task's kaizen suggestion.
<!-- note:end t-018 -->

## t-020 — Flip roadmap-tracked tasks to status review (not left at claimed) before opening a PR from a non-worker/* session

<!-- note:begin t-020 -->
DONE 2026-07-17 (claude-burst-hourly-20260717T1110Z, conductor PR): fixed at the process level rather than per-project, since the gap applies to any session picking up a roadmap-tracked task, not just this one. Added AGENTS.md 'Picking what to work on' step 7 (after claim_task.py, before the Rotation collisions section): every session -- worker/* hourly AND Silas-directed claude/*/burst-mode sessions -- must run scripts/set_task_field.py <project> <task-id> status review (with claimed_by/owner reflecting the real session and branch, no worker/* prefix required) before opening the PR, so a Reviewer sweep can find in-progress work via roadmap state instead of hand-checking GitHub. Also documents that a session merging its own PR may flip review straight to done right after merge -- the point is no silent claimed-to-done jump with zero externally-visible checkpoint. No kind_robots code change needed; this project's roadmap.yaml itself is the only file this specific task touches beyond AGENTS.md.
<!-- note:end t-020 -->

## t-021 — Add minimal Cypress coverage for /stylist (currently zero automated coverage)

<!-- note:begin t-021 -->
Kaizen from t-018 (kind_robots PR #504). No Cypress test references "stylist" anywhere in the repo (grep -rli stylist cypress/ returns nothing), and the maskData API path (enqueue.post.ts, workflow.ts's LoadImageMask/SetLatentNoiseMask) has no contract-test coverage either -- both pre-existing gaps, not introduced by t-018, but now compounded by the new stylist-mask-brush.vue UI on top of them. Start minimal: at least one Cypress e2e assertion that an admin session can reach /stylist and see Hair Studio render, plus a contract test asserting enqueue.post.ts forwards a provided maskData through to the ComfyUI payload unchanged. IMPLEMENTED 2026-07-19 (~07:40 UTC): kind_robots PR #513 (branch claude/vigilant-edison-lwefr4). Contract test (utils/scripts/verifyKontextMaskForwarding.ts, wired into package.json + contract-tests.yml) covers maskData forwarding into the ArtJob payload unchanged and the LoadImageMask/SetLatentNoiseMask graph wiring -- extracted a small buildKontextInputImages() helper from enqueue.post.ts's inline logic so it's unit-testable (behavior unchanged). The Cypress e2e piece is narrower than originally scoped: investigated Cypress's admin-auth options first and found no way to establish a real authenticated ADMIN browser session today -- the existing beta-admin-token bypass (cypress/support/api-auth.ts) is API-header-only and rejected by /api/auth/validate/token.ts (requires an actual 3-part JWT), and no seeded admin login (username/password) is exposed to Cypress. Shipped what's honestly verifiable instead: cypress/e2e/stylist-access.cy.ts asserts an anonymous visitor to /stylist is redirected to /login rather than seeing Hair Studio -- real coverage of the requiredRole: ADMIN gate itself, not a fabricated "renders correctly" assertion. Filed the authenticated-session gap as this PR's kaizen suggestion (a seeded Cypress admin identity or test-only JWT-minting path) rather than blocking or faking it. Verified locally: npm run test (vue-tsc) clean, eslint clean, prettier clean, npm run test:kontext-mask-forwarding passes. Could not run the new Cypress spec live in-sandbox (cypress postinstall's binary download is blocked by the egress allowlist, same as npm ci's CYPRESS_INSTALL_BINARY=0 workaround) -- CI is the real verification gate for that spec. DONE 2026-07-19 (~07:45 UTC): kind_robots PR #513 merged squash `8a1b9fb` after all 4 CI checks green (TypeScript, Contract verifiers, facet-alias-smoke, GitGuardian).
<!-- note:end t-021 -->
