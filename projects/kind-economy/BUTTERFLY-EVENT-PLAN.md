# Butterfly Fundraising Event — Plan

**Created:** 2026-08-19 · **Task:** kind-economy/t-022 · **Status:** planning/design only —
no venue booked, no deposit paid, no date announced, no vendor contacted.

**One line:** a public, butterfly-themed fundraising event that carries AMI's own
argument — a mosquito net costs a few dollars, a life costs about $5,000, here is what
your twenty bucks does — without Kind Robots ever taking custody of a donor's money.

---

## Why butterflies, specifically

This isn't decoration layered onto a generic fundraiser. AMI — the site's AI presence
supporting the Against Malaria Foundation fundraiser at
[againstmalaria.com/amibot](https://againstmalaria.com/amibot) — is visually a horde of
rainbow butterflies, and malaria nets are the literal thing being funded. The theme
*is* the pitch:

- A butterfly is fragile, short-lived, and disproportionately beautiful for its size —
  the same asymmetry as a $5 net standing between a child and a mosquito-borne disease
  that kills roughly one person per $5,000 of net funding (AMF's own stated cost-per-
  life-saved figure).
- "A horde of rainbow butterflies" scales visually from one attendee's phone screen to
  a gallery wall, which is exactly the range of formats considered below.
- It gives the room something to look at, hold, and make, rather than asking people to
  stare at a slide of statistics. The ask ("here's what $20 buys") rides on the image,
  it doesn't compete with it.

---

## The non-negotiable design constraint: never take custody of donations

This shapes every option below, so it's stated once, up front, rather than re-derived
per format.

**Kind Robots must never collect money at this event and forward it to AMF.** The
moment an entity solicits or collects charitable contributions on another
organization's behalf, most states — including California — classify that as a
**commercial co-venture / charitable solicitation** activity with registration
requirements wildly out of proportion to a small community event (see
`research/remittance-options.md` and `kind-economy/t-005`'s findings on the same
structural trap, one layer up, for online payments).

**The fix is the same one the online flow uses: route every dollar directly to AMF,
never through Kind Robots.**

- **QR codes, everywhere.** On the wall, on table tents, on a printed handout, in the
  event description — all pointing at `againstmalaria.com/amibot`.
- **A laptop or tablet at the door** (and one more near any art display), logged into
  the AMF donation page, so anyone without a phone or who wants a guided hand can give
  on the spot.
- **No cash jar. No Venmo. No "give it to a volunteer and we'll forward it."** If a
  well-meaning attendee tries to hand a volunteer cash, the volunteer's job is to walk
  them to the QR code or the laptop, not to accept it.
- **If Silas wants to sell anything** (prints of AMI-generated art, butterfly merch,
  a zine) — that is ordinary commerce through Kind Robots' normal storefront
  (`digital-storefront`), charged and fulfilled the regular way, kept **visibly
  separate** from the donation flow (different table, different signage, explicitly
  labeled "this purchase supports Kind Robots / this QR code donates directly to AMF").
  Never blend "buy this print, proceeds go to malaria nets" language unless the print
  sale itself is structured as a genuine AMF pass-through donation, which reopens the
  exact custody problem this section exists to avoid — simplest is to sell merch as
  merch, and let the donation ask stand on its own next to it.

This constraint doesn't just avoid a compliance headache — it's the one piece of
architecture that keeps this event as cheap and simple as the website itself.

---

## Format and scale options

Three shapes, ordered from lightest to heaviest. Each can be run standalone or as a
progression (small first, scale up if it works).

### Option A — Gallery night (AMI-generated art on display)

A one-evening pop-up gallery of AMI/AMI-adjacent generated butterfly and nature art —
prints, a projected slideshow, maybe a large-format wall piece — in a borrowed or
cheap-rental space (library community room, coffee shop after hours, coworking space
common area, a gallery willing to do a low/no-fee community night).

- **What the site's generated art contributes:** this is the most direct use of Kind
  Robots' actual product. The Daily Dream pipeline already produces genuine generated
  art and writing every day (per the design brief's own note that this is "far better
  source material than anything written to be promotional") — curate a set of
  existing, already-generated butterfly/nature pieces rather than commissioning new
  work, which keeps the cost near zero and sidesteps any "was this made *for* the
  event" framing question.
- **Attendee experience:** browse art, read a short framed card at the entrance (or
  QR-linked page) explaining the $5,000-saves-a-life math, scan a code to give,
  optionally buy a print (separate flow, see above).
- **Rough scale:** 20–60 attendees, 2–3 hour evening window.

### Option B — Community make-a-butterfly workshop

A hands-on session where attendees make physical butterflies (paper cutting, painting
pre-cut wooden/cardstock blanks, simple origami) — possibly displayed afterward as a
"horde" installation echoing AMI's own visual identity, photographed, and used as
future social content (subject to `kind-economy/t-024`'s labelled-AI-content
guardrails if AMI appears alongside it — the workshop itself involves no AI content
generation and needs none of that policy work to run).

- **What the site's generated art contributes:** reference images / templates
  generated by the site's art tools, used as printable stencils or inspiration boards
  — a genuine, low-stakes use of the generation pipeline that gives attendees
  something concrete to take home.
- **Attendee experience:** make something, take it home or add it to the display wall,
  same donation ask (QR + laptop) framed as "you just made a butterfly — here's what a
  real one, or rather a real net, costs."
- **Rough scale:** 15–40 attendees (workshop format caps headcount by table/material
  availability more than by venue size), 1.5–2 hour session.
- **Best paired with Option A** as a wall of finished butterflies feeding into the same
  room's gallery display — genuinely the same event, two entry points.

### Option C — Talk plus donation drive

The lightest-weight option: a short talk (Silas, or Silas plus a guest who can speak to
either malaria prevention or the AI-for-good angle) framing the $5-net/$5,000-life math
and Kind Robots' mission, followed by open donation time with the same QR/laptop setup.
No art production, no workshop materials.

- **What the site's generated art contributes:** slides only — a few generated
  butterfly images as visual backing for the talk, zero incremental production cost.
- **Attendee experience:** listen, ask questions, give if moved to.
- **Rough scale:** scales widest (a talk format tolerates a bigger or smaller room
  without changing the plan), but also has the least "reason to come" for anyone not
  already interested — this option's honest risk is under-attendance more than
  overspend.

**Recommendation for a first run: A + B combined**, as the fee-light, cheapest-to-
break-even option (see budget below) with the strongest "reason to attend and bring a
friend" — a talk (Option C's content) can simply open the combined event as a five-
minute framing before the room turns into gallery-plus-workshop.

---

## Venue candidates (rough, unconfirmed — no vendor contacted)

All candidates below are categories to canvass, not specific bookings. Selecting and
contacting a real venue is outside this task's scope (planning/design only) and should
happen only after Silas reviews this plan.

| Venue type | Typical cost for a 2–3hr community event | Notes |
|---|---|---|
| Public library community room | Often free or nominal ($0–50) for nonprofit/community use | Usually requires advance booking, may cap capacity, may restrict food/drink |
| Coworking space common area (off-hours) | Free–$100, especially if Silas or a contact is a member | Good projector/AV access typically already there |
| Coffee shop / cafe (after hours or a slow evening) | Free–$150, sometimes in exchange for the shop's own promotion or a minimum spend | Built-in foot traffic if run during open hours instead |
| Community/rec center room | $50–200 depending on city and room size | Often the most "event-shaped" space (tables, chairs, AV included) |
| Local gallery or art collective's community night slot | $0–100, sometimes just a % of any print sales | Best fit for Option A specifically; some galleries run free "community night" slots looking for exactly this kind of programming |
| Someone's backyard / a park picnic shelter (weather permitting) | $0–75 (park shelter permit fee) | Cheapest option; workshop-format-friendly; weather-dependent |

**Recommendation:** canvass library community rooms and gallery community-night slots
first — both categories exist specifically to host free/low-cost community programming
and both fit this event's shape (Option A/B) well.

---

## Rough budget

Everything below is a planning estimate for a first, small run (Option A+B combined,
~30–50 attendees). Real numbers depend on the venue chosen and must be confirmed before
any deposit is paid — this table exists so Silas can sanity-check the shape of the
spend, not as a quote.

| Line item | Low estimate | High estimate | Notes |
|---|---|---|---|
| Venue | $0 | $150 | See candidates above; several free options exist |
| Printing (art prints for display, event signage, QR code cards) | $30 | $120 | Home/office printer for signage; a print shop for gallery-quality art prints if displaying larger pieces |
| Workshop materials (paper, cardstock blanks, paint, scissors, glue) | $20 | $80 | Scales with attendee count; dollar-store-tier materials keep this low |
| Refreshments (optional — light snacks/water) | $0 | $60 | Skippable entirely without hurting the event's core purpose |
| A4/table-tent QR code stands or holders | $0 | $30 | Can be improvised (taped cards, printed paper folded into a tent) |
| Misc / buffer (10–15%) | $5 | $65 | Standard contingency |
| **Total** | **~$55** | **~$505** | |

**Break-even framing, per the task's own instruction:** this event raises money for AMF
via a **direct-to-AMF** flow — Kind Robots never receives or holds the donated funds,
so there is no "the event needs to raise $X to cover costs" in the sense of the
donations themselves funding the event. The honest break-even question is narrower:
*"was hosting this worth the real dollars Silas or Kind Robots spent out of pocket on
venue/materials, versus just donating that same $55–$505 directly?"*

That is answerable in exactly two ways, and the plan should commit to one before
booking anything:

1. **Attach a real fundraising multiplier claim and hold it accountable.** If the goal
   is "this event should generate more AMF donations than the cash spent running it,"
   set a concrete target before the event (e.g., "raise at least 3× the event's
   out-of-pocket cost in tracked AMF donations") and check it against
   `againstmalaria.com/amibot`'s own totals before/after the event date. This requires
   accepting that attribution will be approximate — donations made because of the
   event aren't cryptographically distinguishable from donations that would have
   happened anyway, though a dedicated event-specific note or short-lived unique link
   (if AMI's fundraiser platform supports one) would sharpen this.
2. **Treat it as a $55–$505 marketing/outreach spend, not a fundraising ROI bet.** The
   event's real return may be community visibility, new supporters signing up for
   Kind Robots itself, or simply a genuine, low-cost act of community building that
   doesn't need to "pay for itself" in donation dollars to be worth doing — the same
   way a "Save One Human" nonprofit's founding motivation was never itself an ROI
   calculation. This framing removes the "did we net-lose money" anxiety entirely by
   not asking the event's donations to cover its own cost, since Kind Robots was never
   going to receive that money to net against in the first place.

Recommendation: pick framing (2) as the honest default (it matches the "don't take
custody of donations" constraint's own spirit — nothing here is Kind Robots' revenue
to net against costs) and treat framing (1)'s multiplier tracking as an optional bonus
metric to record after the fact, not a precondition for running the event.

---

## What would have to be true for this to be worth running

- The out-of-pocket spend stays at or near the low end of the budget above (free/cheap
  venue, minimal-cost materials) — this is easily controllable by venue choice.
- At least one of: (a) it visibly increases traffic to `againstmalaria.com/amibot`
  around the event date, (b) it brings new people into Kind Robots' own community
  (signups, return visitors, word of mouth), or (c) it produces reusable content
  (photos of the finished butterfly wall, a short recap) that extends the event's
  reach past the room it happened in.
- It stays genuinely small and low-stakes for a first run — this plan deliberately
  avoids anything that requires a permit beyond a possible park-shelter fee, a signed
  vendor contract, or a paid headline act. Scaling up is a decision for *after* a first
  run demonstrates the format works, not a bet made up front.

---

## What this task does NOT cover (explicitly out of scope here)

- Booking any venue, paying any deposit, signing any vendor agreement.
- Announcing a date publicly.
- Contacting a specific library, gallery, or coworking space by name.
- Designing the storefront-merch flow in detail (that's ordinary `digital-storefront`
  work if Silas wants to sell prints/merch at the event).
- Any AI-generated social content promoting the event (`kind-economy/t-024`/`t-025`/
  `t-026` cover labelled-AI content generally; this plan doesn't assume that pipeline
  exists yet).

Per the task note: **escalate to needs-human before anything is booked, paid for, or
publicly announced.** This document is that escalation's substance — the roadmap task
is being set to `needs-human` alongside this plan so Silas can pick a format (A, B, C,
or the recommended A+B combination), approve a venue category to start canvassing, and
green-light an actual date before any of the "not covered" items above happen.
