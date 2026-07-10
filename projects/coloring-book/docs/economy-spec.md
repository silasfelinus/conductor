# Coloring Book — Free Tier, Tokens, and Purchasable-Set Economy

date: 2026-07-10
task: coloring-book/t-008
status: spec complete (no code changes; Stripe/product creation hard-gated as always)
related: sketchy/t-004 (same "align with KR economy, no second economy" requirement —
this spec and Sketchy's should stay interchangeable in their KR-facing assumptions),
digital-storefront/t-017 (DLC unlock mechanics), kind-robots/t-008 (private-but-shared
ACL), ai-art-academy/t-011 (FLUX licensing gate), docs/generation-pipeline.md (costs)

## 1. What the KR economy actually is today (honest code inventory)

Investigated read-only in `/home/user/kind_robots` on 2026-07-10.

### Real and wired

- **Schema** (`prisma/schema.prisma`): `User.mana Int @default(0)`,
  `User.manaCap Int @default(500)`, `User.lastManaRefill`, `User.signupBonusGiven`,
  `User.isGuest`, `User.stripeCustomerId`. A `ManaTransaction` ledger model
  (signed `amount`, `reason`, `balanceAfter`, `refId`, `provider`, `costUsd`) with a
  `ManaReason` enum covering `SIGNUP_BONUS`, `CYCLE_REFILL`, `GENERATION_ART`,
  `GENERATION_TEXT`, social rewards, bounties, `PURCHASE`, `SUBSCRIPTION_GRANT`,
  refunds/adjustments. `KarmaTransaction` is a separate community-score ledger, not a
  spend currency (explicitly commented as such) — leave it alone.
- **USD peg**: two independent constants agree — `server/utils/mana.ts`
  `PEG_USD_PER_MANA = 0.001` and `server/utils/manaGate.ts` `MANA_PER_USD = 1000`.
  **1 mana ≈ $0.001; $1 ≈ 1000 mana.** This peg is the spine of everything below.
- **Refill / signup** (`server/utils/refill.ts`, called lazily from
  `server/api/mana/[id].get.ts`): one-time **250 mana signup bonus** for non-guest
  users; **daily top-up to `manaCap` (500)** — top-to-cap, no rollover, never reduces.
- **Generation gate** (`server/utils/manaGate.ts` via
  `server/utils/generationMana.ts` `withArtMana`/`withTextMana`): genuinely wired
  into 13 endpoints, including `server/api/art/generate.post.ts`,
  `server/api/comfy/sdxl/generate.post.ts`, the chat/botcafe endpoints, and
  `suggest.post.ts`. It pre-checks balance (402 `INSUFFICIENT_MANA` style error),
  computes cost as `max(1, ceil(estCostUsd * 1000))`, and exposes a `commit()` that
  decrements `User.mana` after successful generation. **Free paths already built in**:
  admin, server API key, `FAMILY` role, `useOwnResource` (BYOK), and generations
  routed to the user's own server or a public non-official server
  (`isFreeServerForUser`) are all zero-cost.
- **Cost estimators** (`server/utils/manaCost.ts`): `estimateArtCostUsd` — hosted
  OpenAI image flat $0.04; self-hosted GPU `0.002 + steps*0.00008 + megapixels*0.0005`
  (≈ **$0.005 for a 25-step 1088×1408 image**, i.e. ~5 mana).
- **Wallet UI** (`stores/manaStore.ts`, `components/giftshop/mana-wallet.vue`,
  `server/api/mana/[id].get.ts`): real, working balance/cap/refill-countdown/
  transaction display backed by the API. Guests see a sign-up nudge; FAMILY shows ∞.

### Stubbed or aspirational

- **`server/utils/charge.ts` (`chargeForGeneration`) is dead code** — a
  ledger-writing alternative to `manaGate` (plans: community/byok/local/family,
  admin auto-refund) that **no endpoint calls**. The live path is `manaGate`.
- **Ledger gap in the live path**: `manaGate.commit()` decrements `User.mana`
  directly and **never writes a `ManaTransaction` row** — so real generation spends
  bypass the ledger, and the wallet's "Recent activity" only ever shows bonuses,
  refills, and bounty events. `GENERATION_ART`/`GENERATION_TEXT` reasons exist but
  are only written by the unused `charge.ts`.
- **Purchases don't credit anything.** `server/api/stripe/checkout.post.ts` and
  `subscribe.post.ts` create real Stripe Checkout sessions (checkout builds line
  items from the `stores/seeds/cartItems.ts` seed, which includes a
  "100 Boost Tokens / $5.00" item; subscribe uses a single `STRIPE_PRICE_ID` env),
  but **there is no Stripe webhook** — nothing ever writes `PURCHASE` or
  `SUBSCRIPTION_GRANT` mana. Payment → mana fulfillment does not exist.
- **`components/giftshop/credit-purchase.vue` is a pure stub**: hardcoded
  50/$5, 200/$18, 500/$40 "credits", a fake 2-second delay, and an `alert()` —
  no API call at all.
- **Naming drift**: the same currency is called *mana* (schema, wallet), *credits*
  (credit-purchase stub), *boost tokens* (cartItems seed), and *mana tokens*
  (subscription-manager copy). The currency IS mana; everything else is copy debt.
- `Composition.manaCharged` exists in the schema ("economy reconciliation anchor")
  but no server code writes it yet.

**Bottom line**: the mana *spend* side (gate + free paths + daily refill + wallet UI)
is real and shipped. The mana *purchase* side (Stripe → mana credit) and the spend
*ledger* are the missing halves. This spec builds only on the shipped half and lists
the missing pieces as small tasks (section 7).

## 2. Free tier

**Principle: the free tier IS the existing daily mana refill.** No new counter, no
per-app quota table — that would be a second economy by another name (same rule as
sketchy/t-004). The coloring app converts mana into a friendlier unit at display
time only (section 5).

### Per-page price grounding (own hardware vs API)

| Path | Real cost per page | At the peg |
|---|---|---|
| Own hardware (homelab Comfy/Kontext, per `estimateArtCostUsd`) | ≈ $0.005 (electricity + amortized GPU) | ~5 mana |
| Licensed API (fal/Replicate Kontext dev, per generation-pipeline.md) | ≈ $0.025–0.04 per model call; a pipeline page may take 1–2 calls (conversion + gray-fix pass) | ~25–80 mana |

A "page generation" is more than one raw image call: the pipeline (generation-
pipeline.md §5) may run a second Kontext pass and always runs deterministic
post-processing (threshold, despeckle, upscale, leak-QA — negligible cost).

### Recommendation

- **Flat price: 25 mana per generated page** (see section 3 for reasoning).
- **Effective free allowance: up to 20 page generations per day** — this is not a
  new number, it falls out of the existing 500-mana daily cap ÷ 25. At own-hardware
  cost that is ≤ ~$0.10/user/day worst case, fine. New signups additionally get 10
  pages' worth from the existing 250 signup bonus. The mana pool is shared across
  all KR apps, so a heavy chat user has fewer page generations that day — that is
  the intended single-economy behavior, exactly as Sketchy's critiques share it.
- **One knob if economics bite**: if paid-API routing or abuse makes 20/day too
  generous, raise the page price (40 mana → 12/day) or lower `manaCap`. Never add a
  coloring-book-specific quota.
- **Unlimited coloring, always free.** Coloring an already-available page is pure
  client-side flood fill — zero marginal cost. It never consumes mana, never checks
  a balance, works for guests, works offline-ish. This is non-negotiable UX
  (section 5).
- **Free sampler pages**: each launch set ships a free sampler — recommend **4 free
  pages from Kind Robots and 4 from Monster Recast** (marked `free: true` in the set
  manifest), chosen to show range (a solo character, a busy ensemble page, a simple/
  kids-toggle page, a detailed adult-style page). Free pages are colorable and
  exportable by anyone including guests. Samplers are the funnel to set purchases.
- **BYO stays free**: users generating on their own server/BYOK pay nothing — this
  already works in `manaGate` and should be surfaced in the app ("using your own
  server? generations are free"), matching the existing mana-wallet copy.

## 3. Token model (it's mana; there is exactly one currency)

- **Currency**: KR **mana**. The coloring book introduces no new balance, table, or
  enum value beyond a `refId` convention. Kill the "credits"/"boost tokens" copy
  drift wherever the coloring app is concerned (and pitch the rename upstream —
  section 7).
- **Cost per generated page: flat 25 mana** (≈ $0.025), regardless of prompt→page or
  image→page conversion. Reasoning: (a) covers the licensed-API worst case of one
  Kontext call with margin, and roughly covers two calls at own-hardware blend;
  (b) flat pricing is legible — "a page costs 25 mana" beats a steps×megapixels
  formula in every user-facing sentence; (c) it stays honest to the peg so the
  wallet ledger's `costUsd` reconciliation still means something. Implementation:
  a flat estimator entry feeding the existing `withArtMana` gate — not a bypass.
- **Failed generations are not charged**: `manaGate` already checks before and
  commits after; keep that ordering. Best-of-N candidate picking (pipeline QA) is a
  pipeline cost decision, not a user charge — the user buys one accepted page.
- **How mana is bought**: through the existing (to-be-finished) KR flows only —
  one-time top-ups via Stripe Checkout (`/api/stripe/checkout` + the currently
  missing webhook crediting `PURCHASE` mana) and the subscription flow crediting
  `SUBSCRIPTION_GRANT` monthly mana. The coloring app links to the existing wallet/
  subscription pages; it does **not** ship its own purchase UI. **All live Stripe
  product/price/webhook creation remains hard-gated at go-live** (digital-storefront
  rules; Silas approval required). Until that gate opens, the free tier is the whole
  economy — which is fine (section 6).
- **Suggested top-up SKUs** (catalog candidates only, consistent with the peg and
  the existing seed's $5/100... which underprices the peg 10×): **1000 mana / $1.99**,
  **5000 mana / $7.99**, **12000 mana / $14.99**. Small premium over the peg funds
  margin + Stripe fees. Final pricing is a storefront decision; the coloring app
  only ever says "get more mana."

## 4. Set unlocks (Kind Robots, Monster Recast)

- **Model**: a coloring book **set is a one-time digital unlock** (not a
  subscription, not consumable). Owning a set = all its pages are colorable,
  progress-savable, and exportable forever; free sampler pages behave identically
  without purchase.
- **Purchase paths**: (a) USD storefront item — the primary path, a digital-
  storefront catalog candidate per set (hard-gated at go-live as always); (b)
  *optionally later*, mana-priced unlock for smaller sets — allowed by the
  single-economy rule since mana is the one currency, but defer the decision; don't
  build two purchase paths at launch.
- **Entitlement mechanics — reference, don't duplicate**: per-user unlock of
  content owned/curated by someone else is exactly the "private-but-shared" middle
  state being designed in **kind-robots/t-008** (private-but-shared ACL / per-user
  grants) and the DLC purchase mechanics in **digital-storefront/t-017** (packmaker
  packs as store items, entitlement tying a purchase to per-user unlocks). Coloring
  book sets are one more grantee-content type on that same mechanism: *a set
  purchase creates the same kind of per-user access grant as a DLC pack purchase.*
  This spec deliberately defines only the requirements a set places on that design:
  - grant is per-user, permanent, revocable only by admin/refund;
  - a set manifest must be readable in "preview" mode (titles, cover, page
    thumbnails, which pages are free) without the grant;
  - full-resolution page rasters of paid sets must be served through an
    authenticated endpoint, never from `public/` (same rule t-011's SPEC.md states
    for the novel PDF);
  - generated-by-user pages are owned by their creator and need no grant.
- **PDF/POD**: the same unlock should later entitle the digital PDF download of the
  set (storefront delivery mechanics), and POD paper books are separate physical
  SKUs — both out of scope here, owned by digital-storefront m4/m5.

## 5. Display / UX rules

Borrow Sketchy's framing (sketchy PRODUCT-SPEC.md): **abstract the unit, hide raw
mana inside the app, never block the core free activity.**

- **Allowance display**: the generator UI shows *"You can generate N more pages
  today"* where `N = floor(manaBalance / 25)` — computed from the live mana
  balance, exactly like Sketchy shows "3 critiques remaining today" instead of raw
  mana. One shared derivation (a small composable over `manaStore`) so Sketchy and
  the coloring book can't drift.
- **One tap to the truth**: the allowance chip links to the existing mana wallet
  (`mana-wallet.vue` surface) for users who want the real number, the refill
  countdown (`manaStore.refillCountdown` already exists), and the ledger.
- **Never block coloring**: zero-balance users can still open every free/owned
  page, color, undo, save locally, and export. No modal, no nag on the coloring
  surface. Monetization pressure lives only in the library (locked sets show
  previews + price) and the generator.
- **Generation gated gracefully**: at N = 0 the generate button stays visible but
  switches to a friendly state — "Out of generations for today — refills in
  {countdown}", with secondary actions "Get more mana" and "Browse pages to color
  instead" (redirect to free activity, never a dead end). The 402 from `manaGate`
  is the backend truth; the UI should pre-empt it with the local check but handle
  the 402 with the same friendly state, not an error toast.
- **Guests**: can color and export free pages without an account; generation
  requires signup (matches guest handling in the wallet: guests get daily top-up
  but the pitch is "sign up to keep your balance"). Frame signup around the 250
  bonus: "Sign up and generate your first 10 pages free."
- **FAMILY role** shows ∞ as the wallet already does.
- **Set purchases are not mana** in the UI: sets show a price tag (USD), tokens
  show mana — don't let the two blur into a "coins buy everything" arcade.

## 6. Licensing dependency (sequencing)

- **Paid generation is gated on ai-art-academy/t-011** (needs-human: FLUX.1-dev /
  Kontext-dev weights are under the FLUX Non-Commercial License; running them
  inside a *paid* generation service requires the licensed-API route or a BFL
  commercial license — generation-pipeline.md §0 has the full analysis).
- **The free tier can ship first**: free-tier generation on Silas's own hardware is
  the arguably-fine case flagged in t-011, and free sampler pages + set coloring
  involve no model inference at all at use time. Sets themselves are produced
  in-pipeline before sale; their *sale* is a content sale, not a generation
  service.
- **Charging mana for generation = commercial service**: the moment
  purchased mana can pay for a FLUX-dev/Kontext generation, we are commercial. So
  the go-live order is: (1) free tier + free samplers; (2) set unlocks (content
  sales — still check t-011's read on selling pipeline outputs, but the pipeline
  already routes production generation through licensed endpoints per
  generation-pipeline.md §5); (3) paid token generation only after t-011 resolves —
  either confirmed licensed-API routing (fal/Replicate) for all paid generations or
  a switch to Apache-2.0/MIT bases (FLUX.2 klein, Z-Image Turbo, HiDream) with
  their coloring LoRAs, which the pipeline doc already shortlists as the
  commercially-clean default.
- Practical consequence for the code: the generation endpoint needs a
  **paid-generation feature flag** (default off) so free-tier routing (own
  hardware / free paths in `manaGate`) can ship while community-pool charging
  stays dark until t-011 clears.

## 7. Implementation tasks (small, reversible, kind_robots)

Each is independently shippable and reversible; none creates Stripe objects.

1. **Ledger the live gate** — make `manaGate.commit()` write a `ManaTransaction`
   (reason `GENERATION_ART`/`GENERATION_TEXT`, `refId`, `costUsd`) via `applyMana`
   instead of a bare decrement; then delete or fold in the unused
   `server/utils/charge.ts`. Fixes the wallet's empty spend history for real.
2. **Flat coloring-page estimator** — add a `coloring-page` case to
   `manaCost.ts`/`withArtMana` returning a flat $0.025 (25 mana), used by the
   coloring-book generation endpoint; write `Composition.manaCharged` (or the page
   metadata JSON) with the charged amount for reconciliation.
3. **Paid-generation flag** — env/config flag gating community-pool (charged)
   generation for the coloring endpoint, default off until ai-art-academy/t-011.
4. **Allowance composable** — `useGenerationAllowance(priceMana)` wrapping
   `manaStore`: returns `remaining`, `refillCountdown`, `canGenerate`; shared by
   coloring book and Sketchy so the display rule stays single-sourced.
5. **Copy unification (no schema change)** — rename "credits"/"boost tokens" to
   mana in `credit-purchase.vue`, `cartItems.ts`, `subscription-manager.vue`;
   align the stub's price points with the peg-consistent SKUs (section 3) as
   display-only until purchase fulfillment exists.
6. **Stripe webhook (test mode only)** — `/api/stripe/webhook` verifying
   signatures and crediting `PURCHASE` / `SUBSCRIPTION_GRANT` mana via `applyMana`
   on completed sessions. Test-mode only; **live products/prices/webhooks remain
   hard-gated on Silas** (digital-storefront rules).
7. **Free-sampler manifest support** — `free: true` per page in set manifests +
   library UI honoring it (preview mode for locked sets).
8. **Set entitlement check (stub)** — a `hasSetAccess(userId, setId)` server util
   with a temporary implementation (free sets + owner), swapped later for the
   kind-robots/t-008 ACL / storefront t-017 entitlement — the seam, not the
   mechanism.
