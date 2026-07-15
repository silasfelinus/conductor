# Print-on-demand provider recommendation — KR-logo item

Date: 2026-07-15
Task: digital-storefront/t-015
Status: draft for Silas review — no accounts created, no services connected

## Scope

This narrows `research/stores.md`'s general Printful-vs-Printify note into a concrete pick
for the specific next step: get the Kind Robots logo (`kindlogo_new.png`) onto one
`pod-text-art` item, orderable through the storefront with API-driven fulfillment from
this app's Nuxt/Vercel backend, as fast and cheaply as possible. This does not replace
`stores.md`'s broader multi-channel plan — it answers "which POD backend do we wire up
first, and for which product."

## Recommendation: **Printful**, first item = **sticker**

Wire up Printful's API first, and make a die-cut or kiss-cut sticker the first orderable
KR-logo product. Revisit Printify once volume or margin pressure justifies a second
integration (its 100+ print-provider network is a real advantage at scale, just not on
day one).

### Why Printful over Printify for this app specifically

| Factor | Printful | Printify | Verdict |
| --- | --- | --- | --- |
| API auth | OAuth2 Bearer token (Private Token for a single-store app is exactly our case); v2 API adds request-signed, expiring webhooks | Personal Access Token (Bearer) or OAuth2 for multi-merchant platforms | Both fine for a serverless backend; Printful's Private Token path is the simpler single-tenant fit — no need for the multi-merchant OAuth flow Printify's design assumes. |
| Webhooks | v2: HTTPS-enforced, signed, expiring webhooks; dedicated `package_shipped`, order-status, catalog-price-change, and near-real-time stock events | Webhooks for `order:created`, `order:sent-to-production`, `order:shipment:created`, etc. | Comparable coverage; Printful's v2 signing story is documented more explicitly, which matters for verifying webhook authenticity in a Vercel serverless function (mirrors the same signature-verification pattern this app already uses for Stripe webhooks). |
| Fulfillment model | Printful owns/operates most of its own facilities | Printify is a marketplace of 100+ third-party print providers | Single-supplier consistency (Printful) means one quality bar and one set of shipping SLAs to document, instead of picking and monitoring a provider per product on day one. Printify's provider flexibility is a real strength once we're running enough volume to shop providers for margin — not needed for the first item. |
| Docs / integration maturity | Interactive docs, sandbox/test mode, broad platform-integration list (20+ platforms) | Solid REST docs, less standardized sandbox story in public docs | Printful's public documentation is the more mature reference to build a first-time Nuxt integration against. |
| Free tier | $0/month, 455+ products, automatic fulfillment, unlimited stores, mockup generator, Design Maker | $0/month (Free), up to 5 stores | Both free at our volume; no cost difference at the "one item, low volume" stage. |
| Nuxt/Vercel fit | Plain REST + webhooks — no official Nuxt SDK from either vendor, so this is custom integration work either way | Same | No difference; this app's existing Stripe-webhook route (`server/routes` pattern) is the template for whichever provider we pick. |

Both platforms expose free, well-documented REST APIs with webhook support, so API cost
and Nuxt/Vercel compatibility are a wash. Printful wins on **single-supplier fulfillment
consistency** and **webhook-signing documentation maturity**, both of which matter more
for a first integration than Printify's larger provider network — that network's benefit
(shop providers against each other for margin, avoid backorders) only pays off once
there's enough order volume to make provider-switching worth the added integration
surface.

### Per-order economics (base cost, before Printful's own markup or our retail price)

| Item | Printful base cost | Printify base cost | US shipping (first item) | Notes |
| --- | --- | --- | --- | --- |
| Die-cut / kiss-cut sticker | ~$3–4 typical range for custom stickers (no single official figure found; sticker SKUs aren't part of Printful's most-cited base-cost tables) | $1.20–$2.80 | Printful sticker shipping rose to $4.29 (Feb 2026); Printify stickers ship cheap flat-rate | Printify is meaningfully cheaper per unit on stickers, but the gap is small in absolute dollars at one-item order volume, and stickers are cheap enough on either platform that supplier consistency outweighs a $1–2 base-cost delta for the FIRST item. |
| 11oz mug | $5.95–$7.56 depending on source/tier | $6.45–$8.25 | ~$4.55 (Printify), similar range Printful | Roughly comparable; Printful slightly cheaper at the low end. |
| T-shirt (Bella+Canvas 3001 / Gildan 5000) | ~$11.50–$11.69 (Free plan) | $8.80–$10.98 (Free plan), $5.92–$8.77 with Printify Premium ($39/mo or $24.99/mo annual) | $3.99–$5.99 | Printify undercuts Printful on tees, more so with its paid Premium tier — but Premium's $39/mo (or $24.99/mo annual) only pays for itself around 16-17 orders/month (10-11 on annual billing). Irrelevant at launch volume. |

**Bottom line on economics:** margins are close enough on all three items that supplier
count/integration complexity should decide the *first* item, not a few dollars of base
cost. Stickers have the lowest absolute price point and lowest shipping cost on either
platform, which also makes them the least risky first SKU to price and ship — a customer
eating a sticker's shipping cost or a mispriced margin is a much smaller mistake than the
same error on a t-shirt.

### Why sticker as the first item (not mug or tee)

- Lowest base cost and lowest per-order shipping on both platforms — smallest financial
  exposure while validating the whole order → payment → fulfillment pipeline.
- Single, flat print area (the KR logo as-is) — no sizing/color-variant matrix to design
  or price like apparel needs (S–XXL, multiple garment colors).
- Fastest print turnaround of the three product types on both platforms, so the first
  end-to-end test order comes back quickest.
- Once the Printful integration (webhook handling, order creation, status sync) is proven
  on a sticker, adding a mug or tee SKU through the same connected account is additive
  work, not a new integration.

### Integration outline (for the eventual build task — not part of this research task)

1. Create a Printful account + Private Token (needs-human — no account creation here).
2. Add a single sticker product (KR logo art) via Printful's Product/Sync-Product API,
   generate a mockup via the Mockup Generator API for the storefront listing.
3. On checkout (after Stripe payment succeeds — reuse the pattern from
   `digital-storefront/t-012`/`t-013`'s Stripe webhook work), create a Printful order via
   their Order API using the confirmed shipping address.
4. Subscribe to Printful's `package_shipped`/order-status webhooks, verify the request
   signature, and update the order record so the storefront can show shipping status.
5. Test-mode/sandbox order first; live order only after Silas approves (this is an
   outward-facing, real-money step and stays gated regardless of which provider is
   chosen).

## What this does NOT do

- No Printful or Printify account was created.
- No API keys were requested or stored.
- No product was listed publicly.
- No payment or fulfillment was triggered.

## Sources

- [Printful API](https://www.printful.com/api)
- [Printful API Documentation](https://developers.printful.com/docs/)
- [Printful API Documentation v2 (beta)](https://developers.printful.com/docs/v2-beta/)
- [Printful pricing](https://www.printful.com/pricing)
- [Printful product price updates](https://www.printful.com/product-price-updates)
- [Overview – Printify API Reference](https://developers.printify.com/)
- [Printify API – Help Center](https://help.printify.com/hc/en-us/sections/4471760080657-Printify-API)
- [Printify pricing](https://printify.com/pricing/)
- [Print on Demand 2026: Printify vs Printful — inkandpxl.com](https://inkandpxl.com/blogs/feature/print-on-demand-2026-printify-vs-printful-the-definitive-profit-guide)
- [Printful vs Printify (2026) — printondemandbusiness.com](https://www.printondemandbusiness.com/printful-vs-printify/)
- [The Complete Guide to Printify's Most Profitable Products — PodVector AI](https://podvector.ai/articles/printify/products/the-complete-guide-to-printifys-most-profitable-products)
- [How Much Does Printify Charge Per Shirt? — PodVector AI](https://podvector.ai/articles/printify/costs-and-charges/how-much-does-printify-charge-per-shirt)
- [Printful Pricing 2026 — checkthat.ai](https://checkthat.ai/brands/printful/pricing)
