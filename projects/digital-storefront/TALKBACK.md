# TALKBACK.md — digital-storefront

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-07-05 | Reviewer → Worker | digital-storefront/(roadmap rewrite) | pattern

**Decision:** merged (conductor PR #204 — reactivation, kind flipped content → software)

**What was good:**
- The v1 catalog and every task in the rewritten roadmap trace directly to Silas's
  explicit in-session direction, not agent invention; CONTROL.md, roadmap.yaml, and
  product-types.yaml all tell the same story.
- Every outward step (live Stripe, POD account creation, publishing, spend) stayed
  correctly hard-gated at needs-human even though the kind flipped to software.
- The product-types.yaml addition — normally "ONLY Silas adds" — was flagged
  explicitly for Reviewer attention with a clear escape hatch (revert the hunk) if
  it read as too forward. Good instinct: default to flagging boundary-adjacent
  edits rather than assuming they're fine.

**What to improve:**
- Nothing structural. Minor: the STORE-AUDIT task (t-008) already prose-mentions
  the Stripe lazy-init issue but doesn't make it an actionable task on its own —
  I split that into a standalone kaizen task (kind-robots t-009) rather than
  leaving it buried in an audit note for a future agent to rediscover.

**Kaizen task:** kind-robots/t-009 — lazy-init the Stripe client in checkout/subscribe
routes so a missing STRIPE_SECRET_KEY degrades to a 500 instead of crashing server
boot. (Sourced from the kaizen suggestion in the companion kind_robots PR #91.)

**Pattern note:**
- Recording Silas's verbatim direction into normally-restricted files
  (product-types.yaml) with an explicit inline comment crediting the source and a
  named reviewer escape hatch is a good pattern — keep doing this instead of
  silently expanding restricted files.

## 2026-07-15 | Reviewer → Reviewer | digital-storefront/t-015 | pattern

**Decision:** done (self-claimed and closed in one session — no cross-repo code, pure research output).

**What was good:**
- ai-art-academy (this hour's nominal top-priority project) and digital-storefront's
  own t-012/t-013 (Stripe wiring) were both re-confirmed blocked this session (museum
  egress 403, api.stripe.com 403 — same sandbox proxy denials documented in prior
  TALKBACK entries). Rather than idling or re-flagging an already-documented blocker,
  rotated down the priority list to t-015, a task with no external API dependency.
- Backed the Printful-vs-Printify recommendation with live 2026 web research (pricing,
  API/webhook docs) rather than relying on the general shortlist in research/stores.md,
  and cited sources inline in the new doc.
- Picked a concrete first SKU (sticker) with an explicit reason (lowest cost/risk,
  no size/color variant matrix, fastest turnaround) instead of leaving "whatever item
  is easiest" unresolved for the next agent to re-litigate.
- Folded the concrete provider/item pick directly into the now-unblocked t-016's note
  so its future implementer doesn't have to re-read pod-provider.md to know which
  vendor/product family to design against.

**Kaizen task:** digital-storefront/t-019 — periodically re-verify the api.stripe.com
and museum-site sandbox-egress blockers (t-012/t-013/ai-art-academy) since sandbox
network policy could change between sessions; a stale "confirmed blocked" note can
otherwise strand real ready work indefinitely without anyone rechecking.

**Pattern note:**
- Second cycle in a row (see PR #544's TALKBACK entry) where the "rotate to the next
  project when the top-priority one is blocked" instruction correctly avoided an idle
  cycle. Worth keeping as standing practice rather than special-casing it each time.

## 2026-07-15 | Reviewer → Reviewer | digital-storefront/t-019, t-016 | pattern

**Decision:** both done (self-claimed and closed in one session; t-016 followed by two
new kaizen `ready` tasks, t-020/t-021).

**What was good:**
- t-019 was a genuine recheck, not a rubber-stamp: re-curled api.stripe.com,
  www.metmuseum.org, and upload.wikimedia.org directly and checked
  `/__agentproxy/status` fresh rather than trusting the prior session's TALKBACK note.
  Stamped the recheck timestamp onto every task that cites the same blocker
  (digital-storefront t-011/t-012/t-013, ai-art-academy t-004/t-008/t-013) so the next
  few burst cycles can skip re-curling and just check whether the timestamp is recent —
  directly closes the loop t-019 itself was filed to start.
- ai-art-academy (top of priority.yaml) was checked FIRST this cycle and confirmed
  still blocked on two separate fronts (KR_API_TOKEN absent for t-004/t-009, museum
  egress 403 for t-008/t-013) before rotating down to digital-storefront/t-016 — same
  discipline as the prior two cycles' TALKBACK pattern notes.
- t-016's design doc (docs/gallery-to-swag-pipeline.md) surfaced a real gap instead of
  hand-waving past it: the schema has no way to enforce CONTROL.md's
  commercial-generation licensing rule on gallery art before it's printed and sold.
  Rather than silently assuming "print whatever's in the gallery," the doc proposes a
  concrete field (`Resource.commercialSafe`) and a default-deny policy, and separates
  out the one launch item (KR-logo sticker) that doesn't need the schema change at all
  so it isn't blocked waiting on a pitch.

**Kaizen tasks:** digital-storefront/t-020 (pitch: `Resource.commercialSafe` licensing
field) and t-021 (pitch: `ArtImage.storefrontFeatured` curation field) — both concrete,
small, reversible follow-ups the design doc surfaced. Filed two instead of the usual
one since both are genuine, independently-landable schema-pitch gaps rather than one
being a weaker substitute for the other; flagging this deviation from the "exactly one"
convention explicitly rather than silently doing it.

**Pattern note:**
- Third cycle in a row where checking the top-priority project's blockers first (and
  recording *why*, with a timestamp) before rotating down the list kept the cycle from
  idling or re-doing verification work a prior session already did. t-019 was written
  specifically to stop this from being re-litigated every single cycle — worth checking
  in a future cycle whether the RECHECKED-note pattern actually cut down on repeated
  egress checks, or whether it needs a more structured "last verified" field instead of
  free-text notes.

## 2026-07-15 | Reviewer → Silas | digital-storefront/t-020 | closed (hourly cycle, pitch)

**Decision:** parked at `needs-human` (proposal-kind resolution — pitch written, awaiting Silas)

**Detail:** Priority-order projects ahead of digital-storefront (challenge-center,
ai-art-academy, humboldt-scoop, humboldt-scoop-cms) had no unblocked ready work this
cycle: challenge-center is fully `done`, ai-art-academy's four ready tasks are all
still blocked on the same reconfirmed KR_API_TOKEN/museum-egress limits, and the
Humboldt projects have nothing `ready` (humboldt-scoop-cms/t-006 is `needs-human`).
digital-storefront's own t-011/t-012/t-013 need Stripe test-mode (same egress block)
and t-018 is note-level blocked on coloring-book t-006/t-007 not having landed yet —
but t-020 and t-021 are both `kind_robots pitch` tasks per BOUNDARY.md (schema
changes are never a direct edit from this project) with no external dependency, so
picked t-020.

- Claimed via `claim_task.py` (digital-storefront/t-020).
- Read `docs/gallery-to-swag-pipeline.md` §4/§6 (the kaizen source) and the live
  kind_robots `Resource`/`ArtImage` Prisma models directly rather than assuming the
  note's field-name suggestion was final — confirmed `ArtImage.checkpointResourceId`
  is the actual join point and that `Resource` currently has no license-related
  column at all.
- Wrote `pitches/2026-07-15-resource-commercial-safe-field.md` per the pitch
  template: additive `Resource.commercialSafe` (or `licenseClass` enum) column,
  defaulted unsafe/unknown, seeded true for FLUX.1-schnell/OpenAI/approved-API rows.
- Verified: `python3 -c "import yaml; yaml.safe_load(...)"` on the edited
  roadmap.yaml, and `scripts/audit_roadmaps.py` (0 errors, same warning/info counts
  as baseline).
- Set t-020 to `needs-human` with a FOR SILAS note (soft gate, proposal-kind
  resolution per AGENTS.md — not a stuck-agent escalation).

**What was good:**
- Didn't just restate the task note's suggested field name/type as the final
  answer — cross-checked the real `Resource` model shape (`resourceType`,
  `supportedServer`, `civitaiUrl`/`huggingUrl`/`localPath`) before recommending
  the enum-vs-boolean tradeoff in the pitch.

**Kaizen task:** none filed this cycle — t-021 (the companion
`StorefrontFeaturedArt`/`storefrontFeatured` pitch from the same kaizen source)
remains `ready` and is the natural next pick for a future cycle; no new systemic
gap surfaced by this one.

## 2026-07-15 | Reviewer → Silas | digital-storefront/t-021 | closed (hourly cycle, pitch)

**Decision:** parked at `needs-human` (proposal-kind resolution — pitch written, awaiting Silas)

**Detail:** Same cycle as t-020 (see entry above) — picked up the sibling pitch task
right after t-020's PR merged, per the "may complete several tasks in one run" rule
(one claim in flight at a time, each finished before claiming the next).

- Claimed via `claim_task.py` (digital-storefront/t-021).
- Confirmed directly against the live kind_robots `ArtImage` Prisma model that it has
  no featured/curation flag today, matching the doc's claim.
- Wrote `pitches/2026-07-15-storefront-featured-art.md` per the pitch template:
  additive `ArtImage.storefrontFeatured` boolean, or a `StorefrontFeaturedArt` join
  table if sort-order curation is wanted from day one.
- Verified: `python3 -c "import yaml; yaml.safe_load(...)"` on the edited
  roadmap.yaml, and `scripts/audit_roadmaps.py` (0 errors, same warning/info counts
  as baseline).
- Set t-021 to `needs-human` with a FOR SILAS note (soft gate, proposal-kind
  resolution — not a stuck-agent escalation).

**What was good:**
- Both digital-storefront pitches from t-016's kaizen source (t-020, t-021) are now
  written and parked in the same cycle, giving Silas one batch to review instead of
  two separate future interruptions.

**Kaizen task:** none filed this cycle — this pass was itself closing out the last
two open items from a prior kaizen; no new systemic gap surfaced.

## 2026-07-17 | Reviewer → Silas | digital-storefront/t-013 | pattern (autonomous hourly cycle)

**Decision:** merged kind_robots PR #361 (squash 98190504) and conductor PR #700
(bookkeeping, squash ae3e266). t-013 closed done; kaizen t-024 filed.

**Detail:**
- Prior burst-mode session had already implemented the code (kind_robots#361) and opened
  the conductor bookkeeping PR (#700) setting `status: review`, but left both PRs open —
  this cycle's job was verification + merge + close, not implementation.
- Delegated the payment-code diff review to a subagent (kind_robots#361 touches
  `server/api/stripe/webhook.post.ts`, a new `cancel-subscription.post.ts`, and a
  `User.stripeSubscriptionId` migration) to keep ~115K chars of diff out of the main
  session context. Verified: migration is a single nullable `ADD COLUMN` (no drops), no
  hardcoded/live Stripe keys (both new/changed routes read `process.env.STRIPE_SECRET_KEY`,
  same as the pre-existing webhook), the new cancel-subscription endpoint derives the user
  from `requireApiUser` and takes no client-supplied id (so user A cannot cancel user B's
  subscription), and the webhook's `stripe.webhooks.constructEvent` signature check is
  untouched — the new subscription branches sit after it, not around it. All 3 kind_robots
  CI checks (TypeScript, Contract verifiers, GitGuardian) and all conductor CI checks green.
- Also found (not from this task, closed separately): conductor PR #698 was a duplicate
  `coloring-book/t-022` re-arm — PR #699 had already merged the identical change moments
  earlier (rotation collision). Closed #698 rather than force a conflicting merge; no work
  was lost since #699's version is on `main`.

**Failure category:** n/a (clean merge; subagent review caught one pre-existing,
not-introduced-by-this-PR gap, filed as kaizen rather than blocking the merge).

**Kaizen task:** t-024 — `subscribe.post.ts` still accepts a client-supplied `userId`
with no auth check (pre-existing, not worsened by #361; the new cancel-subscription
endpoint was built correctly via `requireApiUser` and should be the model for the fix).

## 2026-07-17 | Reviewer → Worker | digital-storefront/t-024 | critique

**Decision:** merged (kind_robots PR #373, squash; conductor PR #728 merged first for
the roadmap claim→review flip, then this task set to `done` directly on `main`).

**Failure category:** n/a (clean first-pass; all 3 kind_robots checks green — GitGuardian,
TypeScript, Contract verifiers).

**What was good:**
- Fix mirrors the already-correct sibling endpoint (`cancel-subscription.post.ts`) exactly
  — same `requireApiUser` pattern, same removal of the client-supplied id. Minimal, scoped
  diff (one file, net negative lines).
- PR body confirmed the vulnerability explicitly before describing the fix (unauthenticated
  `prisma.user.findUnique({ where: { id: userId } })` from request body) rather than just
  asserting the change was needed.
- Verified the client (`cartStore.ts`'s `performFetch`) already attaches a bearer token on
  every call, so no client-side change was required to keep the flow working.

**What to improve:**
- None for this task — clean, well-scoped security fix.

**Kaizen task:** t-025 — drop `cartStore.ts`'s now-unused `subscribe(userId)` parameter and
its one caller's pass-through, now that the server no longer reads it (from the Worker's own
kaizen suggestion on PR #728).

## 2026-07-18 | Reviewer → Worker | digital-storefront/t-018 | critique

**Decision:** merged (self-merged; burst-mode session acting as both Worker and Reviewer
since no `worker/*` PR was open at cycle start)

**Failure category:** n/a (clean first-pass; no rejection or retry)

**What was good:**
- The task's own note carried an explicit "do not trust the resolver promotion, verify
  cross-project blockers by hand" warning from 2026-07-17. Verified each cited blocker
  live before claiming rather than either blindly claiming or blindly reverting to
  `waiting`: coloring-book t-009 (Lulu POD research) done, t-006/t-007 superseded-done by
  the current production tasks (t-022/t-024), kind-robots t-008 (sharing/grant design)
  done, packmaker t-003 (pack drafts) done. All genuinely clear.
- Deliverable (SPEC.md §11) reuses existing schema/plumbing verbatim for the digital
  variant (pdf-coloring type, §3-5 Entitlement/download path) rather than inventing new
  shape, and correctly identified that the physical variant needs a new catalog-level
  product type (`pod-book`) distinct from the existing `pod-text-art` (merch, not
  page-priced books) — filed as a pitch per CONTROL.md's standing rule instead of editing
  `product-types.yaml` directly.
- Did not block on either coloring-book production set (t-022, t-024) reaching 36/36 —
  correctly scoped this task as catalog/plan design, independent of content completion.
- `scripts/validate_roadmaps.py` clean; YAML changes verified parseable.

**What to improve:**
- Nothing notable this cycle.

**Kaizen task:** none filed separately — the natural follow-up (adding `pod-book` to
`product-types.yaml`) is exactly the pitch this task filed; a fresh kaizen task would just
duplicate it.

## 2026-07-26 | Reviewer → Worker | digital-storefront/t-029 | pattern

**Decision:** merged kind_robots PR #996.

**Failure category:** null — clean first-pass implementation.

**What was good:**
- `checkPrintEligibility()` is a pure function implementing the pipeline doc's §4 rule
  exactly (not-mature, owned-or-public, base-model-or-commercialSafe-checkpoint,
  default-deny), tested in isolation from the HTTP layer.
- The new `GET /api/art/image/:id/print-eligibility` endpoint reused the existing
  `facets.get.ts` auth/visibility pattern (`getOptionalApiUser` + explicit `canView`
  check) rather than inventing a new one — no schema changes, no live checkout/payment
  logic touched, fully additive and reversible.
- Correctly scoped: left the custom-pasted-image-URL case explicitly ungated (documented
  in a code comment) rather than over-building eligibility logic for a case with no
  underlying `ArtImage` record to check.
- All CI green (verify, TypeScript, Contract verifiers, facet-catalog) at review time.

**What to improve:**
- Nothing notable this cycle.

**Kaizen task:** t-030 created — design a `PrintJob` model + real POD checkout flow to
replace `print-swag.vue`'s remaining UI mock (the Worker's own kaizen suggestion, taken
as-is). Flagged in the roadmap note that payment/checkout integration will likely reach a
hard `needs-human` gate once it touches a live payment provider, even though the
schema/plumbing work leading up to that point is reversible software.

## 2026-07-26 | Worker → Reviewer | digital-storefront/t-030 | pattern

**Decision:** merged (Silas), kind_robots PR #1004.

**Failure category:** null — clean first-pass implementation.

**Subject:** PrintJob model + real POD checkout flow, replacing print-swag.vue's mock.

**Detail:**
- Dispatched a research subagent first to map the exact current code
  (print-swag.vue, t-029's eligibility endpoint, the real landed Prisma schema,
  the webhook fan-out) rather than implementing straight from the design
  doc's draft — this caught a real type mismatch (the doc's `PrintJob` draft
  used `cuid()`/`String` ids; the actually-landed `Product`/`Order`/`OrderItem`
  models all use `Int @id @default(autoincrement())`) before it became a
  migration that wouldn't type-check against `OrderItem.id`.
- Scoped down from the design doc's full ambition deliberately: built a
  dedicated single-item `pod-checkout.post.ts` route matching print-swag.vue's
  actual single-image-modal UI, rather than trying to also fix the general
  multi-item cart checkout's fulfillment gap in the same PR (that gap is real —
  `checkout.post.ts`'s cart flow sets `metadata.kind: 'giftshop_checkout'`,
  which the webhook's dispatch doesn't handle at all, so cart-originated
  purchases of any type currently never create an `Order`). Flagged this in
  the PR as a follow-up rather than scope-creeping this PR.
- Made one legitimate scope cut: dropped print-swag.vue's freeform "paste a
  different image URL" input. It had no backing `ArtImage` row, so there was
  no way to gate eligibility or attach a `PrintJob` to it — the design doc's
  actual entry points (gallery / curated / upload) all produce a real
  `ArtImage` row. Flagged this explicitly in the PR rather than silently
  deleting a visible feature.
- Fixed a real pre-existing bug as part of making the new POD path work
  correctly: `handleProductPurchase` in the webhook hardcoded `quantity: 1`
  for every product purchase regardless of what the Stripe session actually
  sold; now reads the real quantity via `listLineItems`. This affects every
  product type, not just POD, and is a correctness improvement the PR
  description calls out explicitly rather than burying in an unrelated diff.
- Regenerating the Prisma client picked up `models/RewardFacet.ts`, which an
  earlier merged PR ("Build nested Facet-driven Daily Dreams") had added to
  the schema but apparently never regenerated/committed for (likely one of
  the `push_files`-workaround merges documented in CLAUDE.md, which can't run
  `prisma generate`). Included it since leaving it out would have left the
  committed generated client inconsistent with schema.prisma.
- Verified locally via `provision_kind_robots_deps.sh`: `prisma validate` +
  `generate`, full-project `vue-tsc --noEmit` (0 errors after two rounds of
  fixes — a `$fetch` generic-instantiation-depth error and an
  `catalogEntry possibly undefined` narrowing issue), `eslint`/`prettier`
  clean, and the two relevant contract verifiers
  (`verifyNoPrismaJsonCast.ts`, `verifyFetchGenericPinning.ts`) both passed.
  Could not exercise a live Stripe test-mode click-through or webhook
  delivery from this sandbox (no `STRIPE_SECRET_KEY`/`STRIPE_WEBHOOK_SECRET`)
  — flagged this gap explicitly in the PR rather than claiming full
  end-to-end verification.

**What was good:**
- Research-before-code caught a real type mismatch against the design doc.
- Correctly declined to scope-creep into the general cart-checkout gap,
  flagging it instead of expanding this PR.

**What to improve:**
- Nothing notable this cycle.

**Kaizen task:** t-031 (filed by the Reviewer on merge, below) — wire
`checkout.post.ts`'s general cart flow to actually fulfil what it sells
(currently only single-item `productSlug`-metadata routes get real
Order/fulfillment records).

## 2026-07-26 | Reviewer (scheduled agent run) | digital-storefront/t-030 | pattern

**Decision:** merged kind_robots PR #1004 (`status: review`, CI-green, found as one of several open PRs a broader session-level clean-main sweep surfaced beyond `select_role.py`'s local heuristic, which had missed it because its GitHub API check 403s in this sandbox).

**Failure category:** null — clean first-pass, matches the task exactly.

**Subject:** t-030 asked for a `PrintJob` model + real POD checkout flow, replacing `print-swag.vue`'s mock. The task's own note flagged this as likely to reach a hard `needs-human` gate "once it touches a live payment provider" — worth checking carefully before merging rather than assuming the PR's own "reversible" self-classification was correct.

**Detail:**
- Dispatched a subagent to independently audit (1) the migration SQL line-by-line against this repo's additive-only rule and (2) the Stripe webhook's billing-correctness logic, rather than taking the PR description's verification section at face value.
- Migration: `CREATE TABLE PrintJob` + 2 `ADD CONSTRAINT` FKs only — no drops, no rewrites. Passes.
- Webhook: `PrintJob` creation happens inside the same `$transaction` as the `Order`/`OrderItem` it's keyed to (atomic), is mutually exclusive with the existing `Entitlement` branch (no double-crediting), and reads Stripe line-item quantity from the trusted server-side `session.id` rather than client input.
- Confirmed the actual gate the task's note anticipated doesn't apply here: `getStripeClient()` reads `STRIPE_SECRET_KEY` from env with no hardcoded key or live-mode override — identical to every other already-merged Stripe route in this codebase (test-mode by configuration, same posture as the rest of the storefront work) — so this stays reversible software, not an outward-facing live-payment action. Printful vendor submission (the part that really would be outward-facing) is explicitly not implemented and stays its own needs-human step.
- All 6 kind_robots CI checks green; squash-merged (`e3d921b`).

**What was good:**
- The PR author made a clear, well-justified scope call (dropping the freeform "paste an image URL" field since it had no `ArtImage` row to gate eligibility against) and flagged it explicitly in "Flags for Reviewer" instead of silently narrowing scope.
- Server-side re-validation of print eligibility (fresh DB fetch, not trusting client state) — closes a real gap the removed mock field had left open.

**What to improve:**
- None specific this cycle.

**Kaizen task:** t-031 — wire the general multi-item cart checkout (`checkout.post.ts`) to actually fulfil what it sells, per the PR's own kaizen suggestion (currently only single-item dedicated routes like this one get real Order/Entitlement/PrintJob creation; the shared cart flow is decorative past the Stripe redirect).

## 2026-07-26 | Reviewer (conductor-scheduled burst session, follow-up) | digital-storefront/t-030 | pattern

type: pattern

**Subject:** Independent re-review of already-merged kind_robots PR #1004 (dispatched before I saw it had already merged) turned up one additional gap the prior review entry didn't call out: the webhook's POD branch doesn't re-check `ArtImage` eligibility at payment-completion time, only at checkout-creation time.

**Detail:**
- `server/api/stripe/webhook.post.ts`'s POD branch in `handleProductPurchase` creates the `PrintJob` straight from `Product.metadata` (`artImageId`/`printfulVariantId`) with no fresh `checkPrintEligibility` re-check — matches design doc `gallery-to-swag-pipeline.md` §4's explicit "Takedown path" ask: an image flagged between cart-add and payment-completion should fail PrintJob creation, not ship silently.
- Confirmed this is currently inert (no Printful vendor account/API key exists, so `PrintJob` rows stay `PENDING` regardless) rather than live-exploitable — so not a blocker on an already-merged, reversible, test-mode PR.
- Filed as `digital-storefront/t-032` (`depends_on: t-030`) rather than reopening/reverting anything, so it's addressed before or alongside whatever task wires real Printful order submission.

**Suggested action:** none beyond the filed task — flagging here so the next reviewer of a Printful-integration PR knows to check this specific re-validation exists before merging that one.

## 2026-07-26 | Worker (conductor-scheduled burst session) | digital-storefront/t-031 | pattern

type: pattern

**Subject:** Research-before-code caught a shape mismatch (single-Product-per-session webhook vs. multi-item cart) and a real data-loss bug (client drops artImageId before checkout) that the task's own kaizen note hadn't anticipated -- decomposed rather than guessed.

**Detail:**
- kind_robots PR #1007: the general cart checkout succeeded at Stripe but created no `Order`/`OrderItem` at all, because `handleProductPurchase` (the existing webhook handler) is keyed on a single session-level `metadata.productSlug` -- a shape that doesn't fit a multi-item cart. Confirmed via the Stripe SDK's own `.d.ts` files (not guessed, not tested live -- no `STRIPE_SECRET_KEY` in this sandbox) that Stripe `LineItem` objects carry their own per-line `metadata`, distinct from `price_data.product_data`, and round-trip through `listLineItems()` with no `expand` needed. Used that to add a new, separate `handleGiftshopCartPurchase` handler rather than overloading `handleProductPurchase`'s single-product assumptions.
- Found mid-implementation that `stores/cartStore.ts`'s `checkout()` drops the client's own tracked `artImageId` before sending to the server (`{ id: item.type, quantity }` only), so there is no real art to attach a `PrintJob` to for print/shirt/sticker/mug/book today. Rather than fabricate an `artImageId` to satisfy the task's literal ask ("create the same ... PrintJob rows"), split that off as `digital-storefront/t-033` with the concrete plumbing steps already researched, and shipped the honest landable core: real `Order`/`OrderItem` for every type, plus real mana-crediting for `tokens` (an audit-only record would mean charging real money and granting nothing).
- Extended `applyMana` with an optional `tx` parameter (backward compatible, every existing caller unaffected) so the mana credit commits atomically with the `Order`/`OrderItem` write instead of opening a second, non-atomic transaction -- a subtle correctness gap I caught by tracing what `applyMana`'s own `prisma.$transaction` call would do if invoked from inside a caller's already-open transaction (it wouldn't join it).

**What was good:**
- Treated the kaizen note's scope as a starting hypothesis to verify, not a spec to implement blind -- both real complications (metadata shape, dropped artImageId) were found during research, before any code was written, not discovered as a mid-review surprise.

**What to improve:**
- None specific this cycle.

**Kaizen task:** `t-033` (real artImageId/PrintJob wiring for print/shirt/sticker/mug/book) -- already carries the concrete plumbing steps from this cycle's research, not a generic "do the rest" placeholder.

## 2026-07-26 | Worker (conductor-scheduled agent run) | digital-storefront/t-032 | pattern

type: pattern

**Subject:** Closed a self-filed kaizen task (from reviewing PR #1004) by mirroring an existing, already-reviewed pattern (`pod-checkout.post.ts`'s `checkPrintEligibility` call) into the webhook path rather than inventing a new approach.

**Detail:**
- `server/api/stripe/webhook.post.ts`'s `handleProductPurchase` POD branch previously created a `PrintJob` straight from `Product.metadata` with no re-check of the underlying `ArtImage`'s current state. Fixed by re-fetching the same fields `pod-checkout.post.ts` selects (`userId`, `isMature`, `isPublic`, `isActive`, `checkpointResourceId`, `CheckpointResource.commercialSafe`) and calling the same shared `checkPrintEligibility()` helper, rather than duplicating or reinventing the eligibility logic.
- On failure, chose to still create the `PrintJob` row (with `status: FAILED`) rather than silently skip creation — this keeps an audit trail of "payment succeeded, fulfillment was blocked" instead of a payment with no corresponding fulfillment record at all, which would be harder to reconcile later.
- kind_robots PR #1008: all 4 CI checks green, no review comments, merged squash `bc592f5`.

**What was good:**
- Reused the exact existing eligibility-check shape instead of writing new logic, keeping the two enforcement points (checkout-creation, webhook-fulfillment) mechanically identical and easy to keep in sync going forward.

**What to improve:**
- None specific this cycle.

**Kaizen task:** none filed — this closes a previously-filed kaizen with no new gap surfaced. `t-033` (real artImageId/PrintJob wiring for the general cart's physical-goods types) remains the next open follow-up in this area.

## 2026-07-26 | Worker (conductor-scheduled burst session) | digital-storefront/t-032 | pattern

type: pattern

**Subject:** Rotation collision — a second, concurrent session independently implemented an equivalent fix for this exact task and merged first (kind_robots PR #1008); this session's own PR #1009 hit a real merge conflict, was compared against #1008, confirmed equivalent, and closed unmerged rather than land a duplicate.

**Detail:**
- This session claimed t-032 via `claim_task.py` under session id `claude-conductor-scheduled-20260726T090000Z-ds-t032`, implemented kind_robots PR #1009, and only discovered the collision when `merge_pull_request` returned a genuine 405 conflict (not routine `STATUS.md` staleness) — `origin/main` had already absorbed an equivalent fix via kind_robots PR #1008 (branch `worker/digital-storefront-t-032`) moments earlier.
- Compared both diffs directly rather than assuming equivalence: same core approach (re-fetch `ArtImage` inside the fulfillment transaction, re-run the unmodified `checkPrintEligibility`, record a `FAILED`-status `PrintJob` instead of shipping on ineligibility). Only difference: this session's version also re-derived the buyer's `isAdmin` status for the re-check via `userIsAdmin()`; PR #1008's omits it (passes `{ userId }` only) — a minor, arguably more-conservative behavior for a payment-fulfillment gate, not a defect either way.
- Closed the redundant PR #1009 without merging, reset this session's kind_robots branch to drop the superseded commit, and found the roadmap task had *already* been fully closed out by the other session (a different "Worker (conductor-scheduled agent run)" TALKBACK entry, same date) by the time this session got back to writing its own close-out — so no roadmap/TALKBACK duplicate note was written, just this collision write-up.
- Notable possible root cause, not fully confirmed: this session generated its claim `--session` id by hand-typing a plausible-looking but *coarse* on-the-hour timestamp (`...20260726T090000Z...`) rather than invoking `date -u` for real seconds-precision — exactly the anti-pattern AGENTS.md's "Rotation collisions" section warns against ("a full ISO timestamp with seconds... not a coarse hour/rotation label"). If the other concurrent session picked a similarly-rounded label, that would explain why both sessions' `claimed_by` trails look confusingly similar despite being genuinely different sessions — `claim_task.py` itself correctly keyed the actual claim/collision-prevention on project/task, not session id, so this didn't cause a *false* claim (both sessions still raced to real implementation, which is the underlying gap `claim_task.py` closes only partially — see the Suggested action on this same date's earlier `kind-robots/t-049`-adjacent... actually see the general "Rotation collisions" section of `AGENTS.md` itself, not a task-specific note).

**What was good:**
- Verified the two PRs were actually equivalent before discarding either — didn't just assume "someone else got there" and walk away blind.

**Suggested action:** always invoke `date -u +%Y%m%dT%H%M%SZ` (or equivalent) for a claim's `--session` value rather than typing a plausible round-hour timestamp by hand — the latter is exactly the collision-prone pattern AGENTS.md already calls out, and this cycle is a concrete instance of it very likely contributing to (though not solely causing, since `claim_task.py`'s own project/task-keyed race window is the deeper structural gap) two sessions doing the same implementation work in parallel.

## 2026-07-26 | Reviewer (conductor-burst session) | digital-storefront/t-034 | pattern

type: pattern

**Decision:** merged (kind_robots PR #1014, self-merged same session).

**What was good:**
- Read the actual FK schema constraint (`PrintJob.artImageId` non-null, no `onDelete: SetNull`)
  and the sibling `fulfillGiftshopPrintJob` function before writing the fix, rather than
  guessing at the failure mode from the task note's description alone.
- Verified with eslint + a full `vue-tsc --noEmit` typecheck locally (via
  `provision_kind_robots_deps.sh`) instead of just asserting correctness from the diff shape.

**What to improve:**
- None — task was scoped tightly and the fix is a direct mirror of already-proven code in
  the same file, low risk.

**Kaizen task:** t-035 — extract a shared `createPrintJobIfEligible` helper so the two
POD-fulfillment paths stop independently reimplementing the same missing-ArtImage guard
(this is the second time one copy fixed a gap the other already had right — see t-032's
TALKBACK entry above for the closely related duplication this task was filed from).

## 2026-07-26 | Worker (conductor scheduled run) | digital-storefront/t-035 | pattern

type: pattern

**Decision:** merged (kind_robots PR #1016, self-merged same session).

**What was good:**
- Read both call sites' full logic line-by-line before extracting the helper, rather than
  eyeballing the "obviously duplicated" shape -- confirmed the return-value semantics
  (both branches returned/created a row for the eligible AND FAILED cases, only skipping
  entirely when the ArtImage was gone) actually matched before consolidating them.
- Verified with eslint + a full `vue-tsc --noEmit` typecheck locally, and hit a real
  rotation collision on the claim step (a concurrent session's claim commit landed on
  `origin/main` between local claim and push) -- resolved by merging main's `owner`/
  `claimed_by`/`claimed_at` fields into the local `status: review` edit rather than
  guessing which side was newer.

**What to improve:**
- None specific this cycle.

**Kaizen task:** none filed — this closes a previously-filed kaizen (from t-034) with no
new gap surfaced.

## 2026-07-26 | Worker → Reviewer | digital-storefront/t-026 | pattern

**Decision:** implemented and opened kind_robots PR #1018, left at `status: needs-human`
(hard gate: `gate_human: true`, `stakes: outward-facing`, real purchase-fulfillment logic).

**What was good:**
- Caught a real spec/schema drift before writing code instead of after: the task's
  original note (filed 2026-07-18) specified `Grant.level: UNLOCK`, but the actual
  `GrantLevel` enum (finalized by kind-robots/t-037, approved 2026-07-25/26) only has
  `VIEW`/`ADMIN`. Grepped `server/utils/contentAccess.ts` first and found it already
  gates Pack-owned content on `GrantLevel.VIEW` for an active `PACK` Grant — used `VIEW`
  to match the code that will actually consume this Grant, rather than inventing a value
  that doesn't exist in the schema or silently guessing.
- Verified the task's stated precondition ("packmaker/t-004 admin generator has produced
  an approved, purchasable pack") doesn't actually hold yet — grepped for any DLC Product
  creation and found none; the packmaker admin panel builds `Pack` content bundles but no
  priced `Product` row. Documented this gap explicitly in the PR and the FOR SILAS note
  instead of quietly building code no one can currently exercise.
- Full local verification available this cycle (`provision_kind_robots_deps.sh` +
  `npm run test`/eslint/prettier, all clean) since a real kind_robots checkout exists in
  this sandbox — no need for the CI-only fallback some prior cross-repo cycles used.

**What to improve:**
- None specific this cycle.

**Kaizen suggestion:** a follow-up task to build the DLC Product-creation path
(packmaker admin panel -> `Product` row with `type: DLC`, `metadata: {packId}`) so this
fulfillment logic can be exercised end-to-end in test mode — noted in the PR itself,
Reviewer/Silas can decide whether to file it now or after PR #1018 is approved.

## 2026-07-27 | Worker (conductor scheduled burst-mode rotation) | digital-storefront/t-023 | pattern

**Decision:** implemented and opened kind_robots PR #1056, left at `status: needs-human`
(hard gate: `gate_human: true`, `stakes: outward-facing`, real Stripe checkout + paid
file delivery).

**What was good:**
- Picked this task specifically because six other ready "polish and upgrade front-end
  surface" tasks this cycle (alexa-integration/t-015, ruler-hooked/t-010, serendipity/
  t-012, wishmaster/t-003, appmaker/t-012, conductor-app/t-013) had all independently
  converged to the same dead end — steps (2)/(4) already done, step (1) blocked on the
  external art-render relay, step (3) an admin-only action — leaving no real code work
  in any of them this cycle. Verified this directly (checked art-prompts.yaml for their
  request ids, confirmed the target .webp files don't exist in kind_robots) rather than
  claiming one anyway for the sake of rotating.
- Read SPEC.md §5 and the existing webhook (`handleProductPurchase`) before writing any
  code — confirmed the Product/Order/Entitlement schema, the webhook's
  `metadata.productSlug` fulfillment path, and the `mermaids-of-venice-pdf` seed row
  (scripts/seed_products.ts) already existed from t-011/t-022, so this task really was
  just the remaining checkout-creation + delivery half, not a rebuild.
- Closed the 2026-07-26 security flag (public, unauthenticated `public/mermaids.pdf`) in
  the same PR rather than treating it as separate/later work, per the task note's own
  instruction — moved it to a new `storage/products/` root via a small
  `productStorageRoot.ts` util mirroring the existing `imageStorageRoot.ts` env-override
  pattern, confirmed via full-repo grep that nothing else referenced the old path first.
- Matched existing conventions rather than inventing new ones: `product-checkout.post.ts`
  mirrors `pod-checkout.post.ts`'s structure; the download component authenticates via a
  Bearer-token blob fetch (not a plain `<a href>`) because that's how auth actually works
  in this app (`stores/userStore.ts`'s token, not a cookie) — checked `performFetch`
  before assuming a simple link would work.
- Full local verification available this cycle: `provision_kind_robots_deps.sh` +
  eslint + prettier + full-project `npm run test` (vue-tsc --noEmit), all clean.

**What to improve:**
- Could not exercise a live Stripe checkout/webhook round-trip or a real authenticated
  download in this sandbox (no `STRIPE_SECRET_KEY`, no reachable `DATABASE_URL`) —
  documented explicitly as "verification still needed" in both the PR and the roadmap
  note rather than implying it was tested end-to-end.

**Kaizen task:** none filed this cycle — the PR's own "Kaizen suggestion" section notes
a small future refactor (extracting `product-checkout.post.ts`'s hardcoded `/mermaids`
redirect into per-product metadata once a second Entitlement product exists) that isn't
worth a standing roadmap task yet since no second product exists.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-27 | Worker (conductor scheduled burst-mode rotation) | digital-storefront/t-023 | response

**Decision:** closed out — kind_robots PR #1056 was merged directly by Silas
(`merged_by: silasfelinus`, confirmed via the GitHub API) about 30 minutes after
opening. Set `approved_by_human: true` and `status: done` on that basis per
AGENTS.md's human-gate-clearance rule, rather than leaving the task sitting at
`needs-human` until a separate roadmap-editing round.

**Detail:**
- Verified `merged_by` on the PR object before treating the merge as clearance —
  a merge alone isn't proof of human intent if some other process could merge
  hard-gated PRs, so checked who actually did it rather than assuming.
- Left the one still-open item (confirming `STRIPE_SECRET_KEY`/
  `STRIPE_WEBHOOK_SECRET` are live-ready and that `seed_products.ts --write` has
  run against production) as a flag in the task note rather than a blocking
  status — it's a deploy/ops step outside what this roadmap task can verify or
  complete itself, and blocking `done` on it would leave a shipped, reviewed,
  merged PR looking unfinished indefinitely.

**Suggested action:** none — this cycle worked as designed.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-05 | Worker (conductor scheduled agent run) | digital-storefront/t-036 | response

**Decision:** closed out — corrected the one wrong `server/api/store/checkout.post.ts`
reference inside t-031's note to the actual path,
`server/api/stripe/checkout.post.ts`, with a parenthetical marking the
correction so the original text stays legible in history rather than being
silently rewritten.

**Detail:**
- Verified independently before editing: `Grep` for `server/api/store/checkout.post.ts`
  across the roadmap found only t-031's note (the bug) and t-036's own
  title/note (documenting the bug, left as-is since that's the accurate
  historical record of what was filed). No other roadmap or doc referenced the
  wrong path.
- Scope was exactly what t-036 asked for — a doc-accuracy fix, no code touched
  (t-031's underlying implementation was already correct; only its note's file
  path reference was wrong).

**Suggested action:** none — straightforward, low-risk correction, worked as scoped.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-08 | Reviewer (scheduled agent run) | digital-storefront/t-038 | critique

**Decision:** merged kind_robots PR #1603 (t-038 slice 1) despite a red `responsive-layout-audit` check, after confirming the failure was unrelated to this PR's diff.

**Detail:**
- Structural CI (TypeScript, contracts, lint) was fully green. The deployment-triggered `audit` job failed on exactly one finding: `desktop /taskmaster ❌` — CRUSHED/STARVED-TEXT on the narrative ingredient grid.
- That is the same regression `interface-vision/t-113` (kind_robots PR #1600, open at review time) already exists to fix — it predates this PR, and #1603's diff only touches `components/giftshop/giftshop-interact.vue` and `giftshop-manager.vue`, neither of which is anywhere near `/taskmaster` or the shared narrative ingredient picker. Confirmed via the PR's own file list before merging past the red check.
- This is the "base branch itself is broken, the PR's own diff isn't the cause" case from AGENTS.md's pr-medic playbook, just surfaced via the audit rather than a structural check.

**What was good:** reading the actual audit failure detail (which route/viewport, what defect) rather than treating any audit failure as an automatic block — the standing "wait for audit before merging a layout change" rule is about layout changes actually being unverified, not about tolerating zero red anywhere regardless of attribution.

**Suggested action:** none new — t-113 (PR #1600) already tracks the real fix.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-08 | Worker+Reviewer (scheduled conductor sweep) | digital-storefront/t-004 | response

type: response

**Subject:** t-004 (DLC pack-to-product admin route + packId Grant wiring) implemented and merged; split two follow-ons instead of expanding scope -- t-005 (hard needs-human/security, pre-existing Character/Reward access gap) and t-043 (ready/software, Dream/Facet list-route Grant-awareness).

**Decision:** merged kind_robots PR #1630 (squash `0a69a96`) | closed t-004 done | filed t-005, t-043

**Detail:** Reclaimed a stale claim (`2026-08-08T151329Z-pr1612-rv-a83f`, claimed 8+ hours earlier with no TALKBACK entry, no PR, well past `CLAIM_TTL_MINUTES`) before doing any work. Dispatched a read-only Explore subagent into the kind_robots checkout first, specifically to answer: which of the four flagged ad-hoc access-check implementations are genuinely extendable vs. need first-time behavior changes. It found the original task note's framing was incomplete -- `characters/[id].get.ts` wasn't a fourth *pattern*, it (and three Reward routes) had **no check at all**, and `characters/index.get.ts`'s list branch runs an unfiltered `findMany()`. That reframed the scope split: Dream and Facet single-item routes had an existing check to extend (safe, additive, behavior-preserving); Character and Reward did not (fixing them is this app's first-ever check there, a real behavior change, not an extension) -- so wiring those in as part of the same "mechanical" pass would have silently changed live behavior under cover of a DLC-wiring task.

Shipped only what was genuinely additive: new admin route `server/api/admin/packs/[id]/product.post.ts` (matches the `server/api/admin/wonderlab/**` `requireAdminApiUser`+`readBody` convention, idempotent upsert by `Product.slug`, `metadata: JSON.stringify({packId})`/`type: 'DLC'` matching exactly what the webhook's existing `handleProductPurchase` already parses), plus a PACK-Grant fallback added to `dreams/[id].get.ts`, `dreams/[id]/facets.get.ts`, and `facets/[id].get.ts` -- each wrapped so the existing isOwner/isAdmin/isPublic(/isMature) outcome is byte-for-byte unchanged and the Grant check only fires in the case that would otherwise throw/404.

Filed the two deferred pieces as separate tasks rather than either bundling them in or dropping them silently: t-005 is a genuine pre-existing security gap (any caller can read any user's private Character/Reward rows today) that needs Silas's product call before an agent touches it, since the open list-route read already feeds a live UI store (`characterStore.ts`'s app-wide character-picker) and no in-repo caller is verified to *not* depend on it; t-043 is ordinary follow-on software work (list routes need a Grant-subjectId prefetch, not a `canView()` swap) with no security dimension, so it's `ready` for normal Worker pickup.

**Failure category:** none -- first pass, verified before merge (`eslint` 0 problems, `prettier --check` clean, `vue-tsc --noEmit` clean exit 0, lint ratchet 392/27 unchanged; no live DB in this sandbox so not integration-tested).

**What was good:** dispatching the investigation before writing any code, rather than assuming the original task note's four-pattern framing was still accurate -- it wasn't, and building on the wrong framing would have meant either quietly fixing a real security gap without a decision-maker's sign-off, or quietly leaving it out of a note that no longer mentioned it existed.

**Suggested action:** none new -- t-005's note already lays out the decision Silas needs to make, and t-043 is a clean, scoped, non-gated pickup.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-08 | Reviewer/Worker (scheduled conductor sweep) | digital-storefront/t-005 | pattern

type: pattern

**Subject:** found a stranded kind_robots branch (`worker/digital-storefront-t-004-20260808-a83f`) containing an already-written, apparently correct fix for exactly the security gap this session just filed as `t-005` -- from the same abandoned session whose stale roadmap claim on `t-004` was reclaimed earlier this run.

**Decision:** did not rescue/merge it. Recorded it in `t-005`'s note as reference material for whoever implements the fix after Silas answers the policy question, and left the branch in place rather than deleting it.

**Detail:** Branch discovery came from a routine `list_branches` check after merging this session's own `t-004`/`t-005`/`t-043` PRs -- not something `check_pr_merged_drift.py` or `audit_human_gates.py` would surface, since neither inspects branches with no open PR. The branch's 10 commits wire `contentAccess.ts`'s `canView()` into `characters/[id].get.ts`, `characters/index.get.ts`, `rewards/[id].get.ts`, and `rewards/index.get.ts` (the exact routes `t-005` flags), plus a new `viewablePackIds(userId)` helper that prefetches a user's active PACK Grant subjectIds -- exactly the "Grant-subjectId prefetch" this session's own `t-043` described as the missing piece for list-route Pack-awareness, already applied to `dreams/index.get.ts` and `facets/index.get.ts` too. Spot-read several diffs: consistent style, correct `auth?403:404` semantics matching this repo's existing routes, no obvious bugs.

Two reasons this wasn't simply merged despite looking solid: it's now ~9 hours stale (predates this session's own Dream/Facet changes to some of the same files, so a clean merge isn't possible without real conflict resolution), and more importantly, merging behavior-changing access-control code that was written and abandoned without any recorded reasoning or sign-off would make the exact policy call `t-005` exists to escalate to Silas, just with extra steps. Good code doesn't retroactively authorize a security decision no one signed off on.

**What was good:** checking `list_branches` for stray refs even after all open PRs were already merged and drift/gate audits were clean -- a fully "reconciled" roadmap state doesn't mean nothing else is lying around, and this branch would have been invisible to any script that only reasons about `status:` fields or open PRs.

**Suggested action:** none new beyond what `t-005`'s note already says -- whoever resolves the policy question should rebase this branch's approach rather than reinvent it, and should fold `t-043` into the same pass since this branch already solved both.

---
_Generated by [Claude Code](https://claude.ai/code)_
