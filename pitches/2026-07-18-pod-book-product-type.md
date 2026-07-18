# Pitch: New product-types.yaml entry — `pod-book` (print-on-demand physical books)
date: 2026-07-18
project-target: digital-storefront
status: awaiting-silas

## The idea
Add a new approved product type, `pod-book`, to `projects/digital-storefront/product-types.yaml`:
`Print-on-demand physical books (page-count-based, e.g. coloring books, via Lulu Print API)`.
This distinguishes printed *books* (perfect-bound, priced/fulfilled by page count and paper
stock, produced through a book printer's API) from the existing `pod-text-art` type, which
covers flat-design merch (stickers, mugs, apparel) fulfilled through Printful/Printify. The two
have different vendors, different fulfillment APIs, and a different cost model — conflating
them under one catalog type would misrepresent what "POD" means for each SKU.

## Why it's worth doing
digital-storefront/t-018 (catalog plan for the coloring-book project's Monster Recast and Kind
Robots sets — see SPEC.md §11) needs this type for the physical-book variant of each coloring
book. coloring-book/t-009 already researched and recommended a specific vendor and format
(Lulu, 8.5×11 perfect-bound, 60# uncoated paper — `projects/coloring-book/docs/pod-coloring-books.md`),
so this isn't speculative: the moment either coloring-book production set (t-022, t-024) reaches
36/36 pairs, the digital variant can go live immediately under the existing `pdf-coloring` type,
but the physical variant has no catalog type to attach to without this addition. Approving now
unblocks that go-live path without re-opening this same question later.

## Rough effort
small — this is a one-line addition to an approved-list YAML file plus wiring the `Product.type:
POD` / `metadata.vendor: "lulu"` shape already specified in SPEC.md §3 and §11. No schema
migration, no new Prisma enum value (the existing generic `POD` `ProductType` enum value covers
it — only the catalog-level `product-types.yaml` list needs the new line).

## Suggested first task
Once approved: add the `pod-book` entry to `product-types.yaml`, then digital-storefront/t-018's
physical-variant work (creating the actual `Product` row and Lulu sandbox integration step) can
proceed under the normal reversible/no-spend rules already documented in SPEC.md §11's
"not gated" list — Lulu account creation, credentials, and any real listing/spend remain
separately hard-gated regardless of this pitch's outcome.
