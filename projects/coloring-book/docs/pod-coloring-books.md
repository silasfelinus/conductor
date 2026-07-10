# Print-on-Demand Physical Coloring Books

date: 2026-07-10
task: coloring-book/t-009 (research portion)
status: research complete — NO accounts created, NO listings, NO spend
related: digital-storefront m4 (owns the provider relationship),
projects/digital-storefront/research/stores.md (t-001 platform research),
docs/generation-pipeline.md (print-ready page spec)

## Relationship to prior storefront research

`digital-storefront/research/stores.md` (2026-06-26) covered *merch* POD
(Printful, Printify, Redbubble) and digital storefronts (Gumroad, itch.io,
Etsy). **None of those print perfect-bound books** — Printful/Printify do
apparel/posters/notebooks, not trade paperbacks. This doc extends that
research with the book-printer lane it deliberately deferred ("POD research
next"). The digital coloring-PDF lane from stores.md (Gumroad + itch.io)
remains valid and complementary: same interior PDF, two products.

Verification note: pricing pages that require calculators or logins could not
all be fetched directly (session proxy blocked several domains); figures below
are marked verified vs estimate. All costs are US-market, July 2026.

## Provider comparison

### Amazon KDP

- **Interior spec:** 8.5×11 supported ("large trim"); min 24 pages; B/W ink on
  white or cream paper — **no paper-weight choice at all**. Thin stock is the
  #1 complaint for KDP coloring books (marker/gel bleed-through, tearing);
  community mitigations are single-sided layouts and telling users to slip a
  sheet behind the page. No-bleed file 8.5×11 or bleed file 8.625×11.25;
  margins ≥0.375" (see generation-pipeline.md spec table); 300 DPI.
- **Cover:** single print-ready PDF wrap (spine width = page count × paper
  factor), or their online Cover Creator. Glossy or matte.
- **Per-unit cost (verified):** B/W, 24–108 pages, large trim, US:
  **$2.84 flat** (standard trim would be $2.30; 8.5×11 is large). Over 108
  pages: $1.00 + $0.012/page + large-trim surcharge (~$0.006/page).
  A 40–60 page book = $2.84 regardless of exact page count.
- **Royalty/pricing:** 60% × list price − printing cost, on Amazon
  marketplaces. Minimum viable list ≈ $4.74 ($2.84 ÷ 0.60); a $9.99 list
  yields ≈ $3.15/copy. Expanded distribution exists at 40%.
- **API/integration:** **none.** Manual dashboard uploads only; no order-
  injection, no programmatic publishing. Amazon retail is the discovery
  channel, not a storefront backend.
- **Setup:** free; KDP account (tax interview, bank details) — hard-gated.

### Lulu

- **Interior spec:** 8.5×11 (US Letter) supported. Bindings with page ranges:
  perfect bound 32–800, coil 2–470 (lies flat — genuinely nice for coloring),
  saddle stitch 4–48 (Lulu's own docs suggest it for coloring books). Paper:
  **60# white/cream uncoated** (standard, absorbs crayon/pencil well) and
  **80# white coated** (higher opacity, less show-through, but coated stock
  takes marker poorly — smears). Single-sided layout is our call, not theirs.
- **Cover:** print-ready wrap PDF; templates + spine calculator provided.
- **Per-unit cost (estimate — confirm in calculator):** B/W standard 60#,
  8.5×11 perfect bound, 40–64 pages ≈ **$2.50–$4.50/copy**; coil binding adds
  a couple of dollars. Lulu publishes no flat rate card; use
  lulu.com/pricing or the API's cost-calculation endpoint for exact quotes.
- **Royalty/pricing:** no fees, no setup cost; on Lulu's own marketplace you
  keep 80% of margin over print cost. The interesting mode for us is
  **white-label fulfillment: our storefront charges the customer, Lulu bills
  us print + shipping** — pricing fully ours.
- **API/integration (verified):** **Lulu Print API is real and current** —
  developers.lulu.com, docs at api.lulu.com/docs. RESTful, OpenID Connect
  auth, **free sandbox environment** (sandbox jobs never print or charge), no
  service fee — pay only print + shipping per order. Endpoints cover print-job
  creation, cost calculation, shipping options, status webhooks. This is the
  only major book printer with a self-serve public API.
- **Setup:** free account; API keys from the developer portal — hard-gated.

### IngramSpark

- **Interior spec:** 8.5×11 supported; paper choices: 50# white/cream, **70#
  white** (thicker, better for image-heavy/coloring content). Standard 0.125"
  bleed / margin conventions.
- **Cover:** print-ready wrap; stricter file QA than KDP/Lulu.
- **Per-unit cost (estimate):** rate-card model: per-page cost × pages + per-
  unit binding charge. B/W 8.5×11 perfect bound 48–64 pages typically lands
  ≈ **$3–5**; note announced **2026 price increases**. Their Print & Ship
  calculator gives exact quotes without an account.
- **Royalty/pricing:** list price − wholesale discount (you set 30–55%; retail
  distribution effectively demands ~53–55%) − print cost. Title setup fees are
  now $0 (waived/eliminated); revisions can carry fees. Its superpower is
  **distribution** (Ingram feeds bookstores/libraries/Amazon), not margins or
  automation.
- **API/integration:** **no public self-serve API** for indie accounts;
  Ingram Content Group APIs exist for large partners/third-party middleware
  only.
- **Setup:** free account; more formal onboarding (ISBN required — they sell
  them, or Bowker) — hard-gated.

### Bookvault (strong alternative found)

- **What:** UK-origin POD book printer with US printing (bookvault.app),
  popular with direct-sales indie authors; offset-quality digital print.
- **Interior spec:** dozens of bindings, custom trim sizes, multiple paper
  stocks including heavier uncoated options — more coloring-friendly paper
  latitude than KDP.
- **Per-unit cost (estimate):** competitive with Lulu (marketing cites ~$1
  base for a 200-page standard-trim paperback before paper/size upgrades);
  8.5×11 coloring interior needs a real quote.
- **API/integration (verified to exist):** **direct public API** plus turnkey
  Shopify/Woo/Payhip/Wix apps — order-injection like Lulu.
- **Royalty/pricing:** pure fulfillment — we charge the customer, Bookvault
  bills print + ship. Small per-title upload fees (packages ~$33–120 for bulk
  uploaders).
- **Setup:** free-ish account + upload fee per title — hard-gated.

### Comparison summary

| | KDP | Lulu | IngramSpark | Bookvault |
|---|---|---|---|---|
| 8.5×11 B/W 40–60pp unit cost | **$2.84 flat (verified)** | ~$2.50–4.50 (est) | ~$3–5 (est) | competitive (quote needed) |
| Coloring-friendly paper | worst (no choice, thin) | 60# uncoated / 80# coated | 50# / 70# white | multiple stocks |
| Bindings | perfect bound only | perfect, **coil**, saddle | perfect (+hardcover) | many |
| API | **none** | **yes — public, sandbox, free** | no (partner-only) | yes + shop plugins |
| Sales channel | Amazon retail (huge) | Lulu shop + **our storefront** | bookstore/library distribution | our storefront |
| Fees | $0 | $0 | setup $0, revision fees; 2026 price rises | per-title upload fee |
| ISBN needed | no (free ASIN/ISBN) | no (optional) | yes | optional |

## Recommendation

**v1 provider: Lulu.** Reasons, in design-brief order (cheapest thing that
ships, storefront owns the relationship):

1. The **verified public Print API with a free sandbox** means the entire
   set→book pipeline (interior PDF assembly → cost quote → print job) can be
   built and tested end-to-end **now, with zero spend and no gate broken** —
   sandbox jobs don't print or charge. No other provider allows that.
2. White-label fulfillment fits the KR storefront model: books sell where our
   users already are, prices are ours, Lulu is invisible.
3. Real paper choices and coil/saddle options — materially better coloring
   books than KDP's fixed thin stock.
4. KDP remains the obvious **channel #2** (Amazon discovery, $2.84 verified
   unit cost) once a book exists — the same interior PDF uploads manually in
   an afternoon. IngramSpark only matters if bookstore distribution ever
   matters. Bookvault is the fallback/competitive quote against Lulu.

**v1 book format:**

- 8.5×11 portrait, **perfect bound** (retail-normal spine; coil as a possible
  premium "lies-flat edition" later)
- **Single-sided coloring pages** — art on rights, versos blank or carrying a
  faint page title/attribution line; kills bleed-through on any paper and
  is the standard for marker-friendly books
- **48–64 interior pages** = 24–32 coloring images (clears perfect-bound's
  32-page minimum with front matter: title page, about/credits, test-your-
  colors page) — i.e. roughly two 10–16 page digital sets, or one set plus
  bonus pages, per physical book
- **60# uncoated white** paper (crayon/pencil-first; note in listing copy
  that heavy markers should have a backing sheet), matte cover
- Interior pages straight from the generation-pipeline masters (2550×3300 px,
  300 DPI, no-bleed, ≥0.5" margins, ≥0.5–0.75" gutter side)
- Indicative economics (confirm with calculator): ~$3.50 print + ~$9.99 list
  direct → ~$4–6 gross margin per copy before shipping handling

## Hard-gated for Silas — nothing below happens without explicit approval

- [ ] **Account creation** — Lulu account (and later KDP/Bookvault/IngramSpark),
      including the Lulu developer-portal API credentials (even sandbox keys
      require an account)
- [ ] **Tax/banking details** on any provider (KDP tax interview, Lulu payee info)
- [ ] **Listing publication** — making any book purchasable anywhere (Lulu
      shop, our storefront, Amazon), and any metadata that goes public
- [ ] **Price setting** — list prices, discounts, wholesale percentages
- [ ] **Any spend** — proof copies (first real dollars; recommended before any
      listing goes live), ISBN purchases, IngramSpark revision fees, Bookvault
      upload fees, paid API calls outside sandbox
- [ ] **ISBN/imprint decisions** — publishing under a KR imprint name

Not gated (reversible, no accounts): assembling interior/cover PDFs,
preflighting against provider specs, cost modeling from public calculators,
and writing the storefront integration against Lulu's documented API shapes
(everything short of requesting credentials).

## Sources

- Lulu Print API: https://developers.lulu.com/ · https://api.lulu.com/docs/ · https://www.lulu.com/sell/sell-on-your-site/print-api · https://help.api.lulu.com/en/support/solutions
- Lulu paper/bindings: https://help.lulu.com/en/support/solutions/articles/64000255473-cover-and-interior-paper-stocks · https://help.api.lulu.com/en/support/solutions/articles/64000254625-what-is-the-difference-between-binding-types- · https://www.lulu.com/pricing
- KDP printing cost: https://kdp.amazon.com/en_US/help/topic/G201834340 (values corroborated via theauthorcentral.com and bookbloom.io calculators: $2.30/$2.84 fixed 24–108pp; $1.00 + $0.012/pp above)
- KDP trim/bleed/margins: https://kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6
- KDP paper complaints (coloring): https://www.kdpcommunity.com/s/question/0D58V00008827tLSAQ/we-need-better-choices-for-printing-papers-on-kdp · https://coloringbutterfly.com/coloring-books-poor-quality-paper/
- IngramSpark: https://www.ingramspark.com/pricing · https://myaccount.ingramspark.com/documents/IngramSparkPriceSheet.pdf · https://janefriedman.com/ingramspark-will-increase-pricing-in-2026/ · https://www.ingramspark.com/hubfs/downloads/Paper_Specs_Spark.pdf
- Bookvault: https://bookvault.app/ · https://apps.shopify.com/bookvault · https://scribecount.com/author-resource/publishing-wide/bookvault
- Prior POD/storefront research: projects/digital-storefront/research/stores.md
