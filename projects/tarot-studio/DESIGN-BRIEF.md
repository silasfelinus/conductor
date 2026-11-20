# Tarot Studio — production design brief

Date: 2026-11-20 PT  
Status: internal authoring approved by Silas; printing, commerce and publication gated  
Master issue: https://github.com/silasfelinus/kind_robots/issues/5431

## Why this exists

Silas's original 2026-10-02 Kind Oracle was not removed. Its Conductor project
`kind-oracle` and 78-card specification survive, and the seedable reading engine
remains in `kind_robots/utils/oracle/reading.ts` (PR #3207). The original was
moved into the Daily Dream Workshop's `continuous` member-project tier on
2026-11-01. Tarot Studio is a **new first-tier, active production project**,
not a reclassification of Kind Oracle. The two projects share canonical card
identity but have different responsibilities.

The immediate goal is a handcrafted **SuperKate Tarot** as a one-of-a-kind
personal gift, with the same tools reusable for **Kind Robots Tarot** and
**Zuzu Tarot**. New decks need no new code or schema.

## Public/private boundaries

- `/admin/tarot` is an admin-only tool and an ADMIN navigation tab. It is
  not an accessible storefront or a public `/play` surface.
- Kind Oracle is a separate free-to-play, authored-content reading engine:
  seeded draws, upright/reversed orientation, pair passages, position frames,
  no runtime LLM. Its IDs from `projects/kind-oracle/docs/spec.md` remain
  canonical mapping keys in the Kind Robots tarot deck.
- Tarot Studio owns deck/card art direction, composition, prompt recipe,
  checkpoint override, LoRAs, render attempts, and print/approval status.
  Its card records never replace or overwrite the canonical reading engine.
- A private *draft* may be saved by an admin at any time. Only actual
  ArtImages can be considered rendered; only review decisions on those
  outputs can mark art approved. Queue state must not masquerade as delivery.
- No person is rendered as SuperKate's photographic likeness without a
  suitable user-supplied/reference-approved source. Rainbow hair artistry
  and her imaginative stylist identity are the initial visual direction.

## Deck and card data contract

A `TarotDeck` row owns title, slug, overall style bible, default engine,
checkpoint and LoRA recipe, shared back design, print status, and timestamps.

A `TarotCard` row belongs to exactly one deck. It records a **fixed tarot
identity** (`key`, Major/Minor, suit, rank, ordinal) and a **canonical
`oracleId`**. Deck-specific overrides include card title, image prompt,
checkpoint, LoRAs, upright/reversed meanings, notes, ArtJob ID, accepted
ArtImage ID, image URL and review state. The editable fields are persisted on
the server with ADMIN authorization. Prompt changes do not automatically
resubmit, approve, or replace prior artwork.

Each seed deck has 78 cards: 22 majors (The Fool through The World) plus
four 14-card suits (Wands/Cups/Swords/Pentacles: Ace–Ten, Page, Knight,
Queen, King). For Kind Robots, majors display the recovered Kind Oracle titles.
Minor IDs map Wands→Sparks, Cups→Currents, Swords→Breezes,
Pentacles→Cogs, Page→Apprentice, Knight→Wanderer, Queen→Keeper,
King→Elder. The reading engine's seed and pair/position text remain
independent of Tarot Studio's rendered pictures.

## Admin experience

- Art-first gallery with full 78 card reachability by its own bounded scroll.
- Deck switcher (SuperKate, Kind Robots, Zuzu, user-created decks).
- Filters: project/deck, Major/Minor Arcana, suit, rank, checkpoint,
  production status, and search.
- Single-card inspector with editable prompt, engine/checkpoint inheritance,
  LoRAs, meanings, notes, review state, provenance.
- Deck-wide inspector with visual bible, default model recipe, card back.
- Responsive 390/768/1440 px presentation, keyboard and screen-reader
  controls; one console header and page-help tutorial.
- Render attempts through existing `/api/art/enqueue` and durable ArtJobs,
  with stable idempotency request keys; never build a second queue.
- **Artwork remains image-shaped even when missing**; don't pretend the
  decorative draft placeholder is produced art.

## Art standards

Default to Krea 2 for literal subject fidelity; render physical characters,
poses, scenes and lighting. Avoid typographic/layout terms in raw image prompts
that models may draw as lettering. Names, Roman numerals, suit markers, borders,
safe zones and print registration marks are deterministic layout overlays,
**not AI-generated text**. Record every generation's engine, checkpoint,
LoRAs, seed, ArtJob ID, ArtImage ID, delivery path and approval.
Persist unsuccessful and alternate renders for comparison; do not silently
overwrite an accepted face.

## Print production

One physical prototype, **SuperKate first**, before opening retail orders.
Use provider-neutral export profiles so the dimensions can be calibrated
from the printer's chosen stock, card size, corner radius, bleed and margin.

### Print-ready package contract

- Exactly 78 correctly ordered fronts plus a shared back, optional booklet,
  tuck/rigid box files and manifest/checksums.
- Render/composite at the vendor's actual final physical size plus bleed, at
  300 DPI or vendor-specific requirement; add an explicit safe area for any
  text, numerals and critical faces.
- Assert required image completeness, dimension/DPI, consistent card ordering,
  legibility of metadata overlays, minimum resolution and color format.
- Never upscale low-res images silently as if this makes them print-ready;
  flag low-res source art for review.
- Export a contact sheet and manifest for human review. Check a **physical
  proof** for crop, color, coating, corners, opacity and deck shuffle feel.

### Vendor candidates

1. **QPMN / MakePlayingCards**: strongest candidate for low-run custom tarot
   and later automated API print + direct shipping. Confirm their current
   tarot SKU, template, API payload, shipping, webhooks and commercial terms
   before spending; do not assume the advertised API covers all tarot variants.
2. **The Game Crafter**: useful for prototype-on-demand and short-run proofing.
   Verify tarot box/card/stock options, API order automation, minimum quantities
   and country-by-country freight in a trial.
3. **PrintNinja**: investigate for larger print runs when there is repeat
   demand and actual inventory economics; not the default first proof.

Do not hard-code a provider's bleed specification until the selected product
template has been downloaded and checked. Keep per-provider adapter modules
and print profiles so changing the supplier does not rebuild the art pipeline.

## Commerce and fulfillment

Kind Robots already has Stripe checkout, Product/Order/OrderItem/PrintJob
models and existing store POD infrastructure. **Extend those**; do not
invent a second payments ledger. The original digital-storefront Conductor
project is paused, so new scoped tarot deliverables stay within tarot-studio
until a direct owner directive reopens storefront-wide work.

Phase A, after proof and approval: accessible Kind Robots giftshop listing.
A paid Stripe webhook creates or reuses an idempotent order and print job,
sends a secure **admin order notification** with fulfillment checklist,
and exposes order status without leaking the buyer's shipping details.
Manual fulfillment and actual shipment are human work. Test without charges
or outward emails.

Phase B, only after separate approval: provider adapter creates the
print order with an idempotency token, bounded price/cost checks, customer
shipping consent and tracking reconciliation. Retrying must never buy the
same deck twice; errors park in a visible fulfillment queue.

## Explicit human gates

- **Publish**: product listing, pricing, public checkout and shop promotion.
- **Money**: printer account/order, paid print proof, billing, API charges.
- **Physical access**: reviewing a real delivered printed proof.
- **Secrets**: vendor credentials or new email service configuration.
- **Subjective approval**: portrait/style likeness, artwork, card backs,
  packaging and acceptance of a physical proof.

Building private, reversible editor/queue/export code is already authorized
and should continue without asking for approval between each task.

## Completion sequence

1. Register this project, preserve recovery links, write this brief.
2. Persistent admin deck and card editor, seeded 78 × 3, filters, tests.
3. Durable ArtJobs queue and image review/acceptance.
4. Finish all cards and meanings; produce proof files.
5. Verify physical print proof; separately approve public shop.
6. Add paid-order notification workflow; optionally automate vendor fulfillment.
