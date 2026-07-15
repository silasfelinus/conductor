# Gallery-to-swag pipeline — design doc

date: 2026-07-15
task: digital-storefront/t-016
status: draft for Silas review — no accounts created, no code shipped

## What this is

A design for turning ArtImage records already in the kind_robots gallery (site-generated
or user-uploaded) into orderable print-on-demand (POD) products — the automated version
of what `components/giftshop/print-swag.vue` currently fakes with a `console.log` +
`alert()` stub. Builds directly on `digital-storefront/t-015`'s provider pick: **Printful**,
first item **sticker**, single-supplier account.

This is a design doc only. Implementation tasks get filed from it once Silas has reviewed
the plan; nothing here creates a Printful account, lists a product, or charges anyone.

## 1. Art selection UX

Three entry points into the same flow, all landing on one product-configurator component
(replacing `print-swag.vue`'s stub):

1. **From the user's own gallery** — an existing ArtImage the user owns. Entry point:
   a "Print this" action on the art-viewer/gallery card, alongside existing actions
   (download, share, react). Reuses `art-styler.vue`'s established pattern of passing an
   `artImageId` into a child component (`print-swag.vue` already accepts `artImageId` as
   a prop — the plumbing exists, only the backend is a stub).
2. **Curated "specifically chosen pieces"** — a Silas-picked subset of ArtImage rows
   flagged for storefront promotion (see §6, needs one schema field). Surfaced on the
   storefront's swag landing page as a "featured prints" rail, independent of any one
   user's gallery.
3. **Upload flow** — `print-swag.vue`'s existing `customImageUrl` field, generalized to a
   real upload (reuse `stores/uploadStore.ts`'s target-model pattern already used by
   `art-maker.vue`, targeting a new `ArtImage` row with `userId` set and `isPublic: false`
   by default so a private upload doesn't leak into the public gallery just to get
   printed).

Configurator steps once an image is selected: product type (sticker first, per t-015;
mug/tee follow once the Printful integration is proven), live mockup preview (Printful's
Mockup Generator API, called at add-to-cart time, not on every keystroke), quantity, then
"Add to Cart" — which creates a `Product` row on the fly (see §3) rather than requiring
every possible art+product combination to be pre-seeded.

## 2. Print-file requirements

Printful's sticker specs (per their public product docs) are the floor every source image
must clear before the "Add to Cart" button enables:

- **Minimum resolution**: 150 DPI at the target print size (Printful's baseline; 300 DPI
  recommended for crisp small text/line art). A 4"×4" sticker needs ~600×600px at 150 DPI,
  ~1200×1200px at 300 DPI.
- **File format**: PNG with transparency for die-cut/kiss-cut edges; JPEG acceptable for
  rectangular products (mug wrap, print) where there's no cutline to respect.
- **Color mode**: RGB (Printful converts to CMYK on their end; no client-side conversion
  needed).

ArtImage rows store `imagePath`/`path` but no explicit width/height/DPI columns today —
check §6 for the schema gap this creates. Until that lands, the configurator should probe
the actual image dimensions client-side (an `Image` load + `naturalWidth`/`naturalHeight`
check) before allowing add-to-cart, and show a plain "this image is too small to print
well at this size" warning rather than silently accepting a blurry order.

## 3. POD API order flow

Extends the `Product`/`Order`/`OrderItem` model SPEC.md (§3) already defined for the wider
storefront, adding one `POD`-specific piece: a `PrintJob` join between an `OrderItem` and
Printful's order, so fulfillment status can be tracked without overloading `OrderItem`.

```
model PrintJob {
  id                String      @id @default(cuid())
  orderItemId       String      @unique
  orderItem         OrderItem   @relation(fields: [orderItemId], references: [id])
  artImageId        Int
  artImage          ArtImage    @relation(fields: [artImageId], references: [id])
  printfulOrderId   String?     // set once Printful confirms order creation
  printfulVariantId String      // Printful catalog variant (e.g. "die-cut sticker, 4in")
  status            PrintJobStatus @default(PENDING) // PENDING | SUBMITTED | IN_PRODUCTION | SHIPPED | FAILED
  trackingUrl       String?
  createdAt         DateTime    @default(now())
  updatedAt         DateTime    @updatedAt
}
```

Flow, reusing the Stripe webhook pattern SPEC.md §2 already specifies:

1. User configures a print (art + product type + quantity), "Add to Cart" creates/reuses
   a `Product` row (`type: POD`, `metadata: { printfulVariantId, artImageId }`) and adds
   it to the cart the same way any other cart item works today.
2. Stripe Checkout Session runs as normal (existing `checkout.post.ts` pattern).
3. On `checkout.session.completed`, the webhook's per-item fan-out (SPEC.md §4) gets a new
   branch for `type: POD`: create the `Order`/`OrderItem` rows as usual, then create a
   `PrintJob` row and call Printful's Order API (Sync-Order create) with the shipping
   address from the Checkout Session and the `printfulVariantId` from the product's
   metadata. Store the returned `printfulOrderId`.
4. Subscribe to Printful's order-status webhooks (`package_shipped`, production-status
   changes). Verify the request signature (mirrors the raw-body + signature-verification
   pattern SPEC.md already specifies for Stripe) and update `PrintJob.status`/
   `trackingUrl`.
5. Order-status page (reuses whatever "my orders" surface SPEC.md's Order model produces
   for digital goods) shows `PrintJob.status` and tracking link for POD items alongside
   download links for digital items.

Test-mode/sandbox order first, per t-015's integration outline; a live order is a
separate, explicitly-gated step regardless of how complete this code is.

## 4. Moderation / rights considerations

This is the section most likely to need a Silas decision before implementation, because
POD turns a gallery image into a **commercial physical product**, which is a stricter bar
than "visible on the site":

- **Commercial-generation licensing rule (CONTROL.md, 2026-07-10)** already states the
  house rule for anything sold: license-unencumbered backends (FLUX.1 schnell) or
  OpenAI/ChatGPT image generation, or an approved licensed API (BFL Kontext pro/max,
  fal/Replicate). **FLUX.1 dev, Kontext dev, and dev-trained LoRAs never touch commercial
  output.** Style Lab entries built on living-artist/brand LoRAs (ai-art-academy's
  DESIGN-BRIEF.md calls out Disney, Gorillaz, DB4RZ by name as Style-Lab-only) are exactly
  the case this rule exists to catch — printing "art in the style of Gorillaz" for money
  is a real trademark/style-appropriation exposure the free-play gallery doesn't carry.
- **The schema has no field to enforce this today.** `Resource` (the LoRA/checkpoint
  registry) has `resourceType`, `civitaiUrl`/`huggingUrl`/`localPath`, `isMature`,
  `isPublic` — but nothing that says "commercial-safe" or records which generation
  backend/model produced a given `ArtImage`. `ArtImage.checkpointResourceId` links to the
  `Resource` used, which is the right join point, but there's no boolean to gate on. This
  needs a `kind-robots` pitch (per BOUNDARY.md — backend schema changes are never direct
  edits): add a `commercialSafe` (or `licenseClass: 'open' | 'restricted' | 'unknown'`)
  field to `Resource`, defaulted conservatively to unsafe/unknown, with the FLUX-schnell /
  OpenAI / approved-licensed-API backends marked safe at seed time. Until that field
  exists, the print flow should **default-deny**: only allow printing images whose
  `checkpointResourceId` is null (meaning no LoRA/checkpoint override — base-model-only
  generation, or a plain upload) or explicitly allow-listed by slug, and require the
  uploader to attest they own rights to any uploaded (non-generated) image.
- **isMature gate.** `ArtImage.isMature` and `Resource.isMature` already exist — reuse
  them as a hard "not eligible for POD" filter regardless of the licensing question above.
  A print-on-demand vendor relationship is not the place to relitigate content-rating
  policy; simplest rule wins.
- **Ownership.** A user should only be able to print their own `ArtImage` rows (`userId`
  match) or explicitly curated/public pieces (§6) — not any public gallery image belonging
  to someone else. This avoids a second, harder rights question (can User B print User A's
  generated art?) that the v1 pipeline doesn't need to answer yet.
- **Takedown path.** Because Printful fulfillment can't be un-shipped once triggered, any
  moderation flag on an `ArtImage` (existing `isActive`/`isPublic` toggles, or a future
  report/flag mechanism) should be checked at Checkout-Session-creation time, not just at
  gallery-display time — an image flagged between "added to cart" and "payment completed"
  should fail the webhook's `PrintJob` creation step with a clear order-support path
  rather than silently shipping it.

None of the above is a hard blocker for building the technical pipeline (§1–3); it's a
policy default (deny unless explicitly known-safe) that keeps the first live order from
being the thing that discovers the gap the hard way.

## 5. Curated "specifically chosen pieces" support

The storefront's swag rail (§1.2) needs a way to say "these ArtImage rows are the ones we
sell, regardless of the automatic self-service flow" — the KR-logo item (t-015's actual
launch product) is exactly this: `kindlogo_new.png` isn't even an `ArtImage` row today,
it's a static asset in this project's `projects/digital-storefront/` folder. Two cases to
support, not one:

1. **Curated ArtImage rows** — an existing gallery image Silas wants featured for sale.
   Needs one boolean-or-better field: `ArtImage.storefrontFeatured` (or a lighter-weight
   join table `StorefrontFeaturedArt { artImageId, sortOrder, addedAt }` if ordering/
   curation metadata is wanted later) — another `kind-robots` pitch, same BOUNDARY.md
   rule as §4's licensing field. Until it exists, a simple allow-list of `artImageId`s
   in this project's `docs/` (or `product-types.yaml`) is a fine v1 stand-in, same
   pattern this project already uses for the fixed v1 catalog.
2. **Non-ArtImage source art** (the actual KR logo, and likely future one-off brand
   assets) — these become a `Product` row (`type: POD`) with `metadata.staticAssetPath`
   pointing at the file instead of an `artImageId`, bypassing the ArtImage-ownership/
   moderation checks in §4 entirely since they're Silas-supplied brand assets, not
   user/AI-generated gallery content. The webhook fan-out (§3 step 3) branches on whether
   `metadata.artImageId` or `metadata.staticAssetPath` is set to know which print-file to
   hand Printful.

This means the KR-logo sticker (t-015's actual next build step) doesn't need to wait on
either of §4's schema pitches — it ships through the static-asset path, which has no
rights ambiguity. The self-service "print any of my gallery art" flow (§1.1/§1.3) is the
piece that needs §4's licensing field before it should go live for real users.

## 6. Schema gaps this doc surfaces (for kind-robots pitches, per BOUNDARY.md)

None of these block the KR-logo-sticker build (§5 case 2); they block the general
self-service gallery-to-swag flow (§1 cases 1 and 3):

- `Resource.commercialSafe` (or `licenseClass` enum) — §4, gates which generation
  backend/LoRA an ArtImage can trace back to before it's print-eligible.
- `ArtImage` width/height (or a computed check at upload/generation time) — §2, avoids
  accepting print orders for images too small to print well.
- `ArtImage.storefrontFeatured` or a `StorefrontFeaturedArt` join — §5 case 1, curation
  without a full admin CRUD surface.
- New `PrintJob` model — §3, POD-specific fulfillment tracking, additive-only migration.

## 7. Suggested build order (each independently landable)

1. KR-logo sticker via the static-asset path (§5 case 2) — no schema pitches needed,
   ships as soon as the Printful account exists (needs-human) and `Product`/`Order`/
   `OrderItem`/webhook infrastructure from SPEC.md lands.
2. `PrintJob` model + Printful order-creation branch in the webhook fan-out (§3).
3. Printful order-status webhook subscription + `PrintJob.status` surfacing on the
   order-status page.
4. File the two `kind-robots` pitches from §6 (`commercialSafe`, `storefrontFeatured`).
5. Self-service "print my art" entry point on the gallery/art-viewer (§1.1), gated on
   pitch 4 landing.
6. Upload-to-print entry point (§1.3), same gate.

## What this does NOT do

- No Printful account created (needs-human, per t-015).
- No schema migrations applied — §6's fields are proposals for kind-robots pitches.
- No code shipped against `print-swag.vue` or the webhook handler.
- No decision made on the licensing-field default beyond "deny unless known-safe," which
  is a policy stance, not a schema choice Silas needs to bless line-by-line.
