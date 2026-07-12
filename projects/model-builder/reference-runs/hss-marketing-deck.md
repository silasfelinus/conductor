# Reference Run — Humboldt Scoop Solutions Marketing Deck

**Model Builder run (t-016) · INTERNAL REVIEW DRAFT — not for publication**

- **Source model:** `humboldt-scoop` (Project)
- **Related source:** `humboldt-scoop-cms` (route-maker / reliability proof)
- **Recipe:** `marketing-deck`
- **Stakes:** outward-facing · **gate_human: true** — nothing here ships until Silas approves.
- **Grounding (authoritative, no rebrand):** `projects/humboldt-scoop/CONTENT-BRIEF.md`
  and the live theme. Existing logo, approved copy, and real product screens win.

> **What this is:** the Marketing Deck recipe run for HSS, produced as an internal
> review set — pitches, copy, and asset **specs / generation prompts**, plus a launch
> plan. **No images were generated, nothing was published, printed, posted, or spent.**
> Each image item lists the prompt/size to run through the Model Builder's
> GENERATE_ASSETS stage once Silas approves the concepts. The existing brand is the
> constraint, not a suggestion.

## Brand kit (extracted, authoritative)

- **Tagline:** "A cleaner yard, without the dirty work."
- **Voice:** warm, local, lightly playful; practical and honest. Humboldt-proud.
- **Palette:** navy `#1b3a5c` (primary) · cream `#fbf9f5` / `#f5f0e8` (paper) ·
  gold `#e8a030` (CTA/accent) · teal `#7bbfb5` / `#a7dccb` (fresh/clean) ·
  earthy rust `#b9684f` / `#8b2a1a` (grounding accent).
- **Trust badges:** Locally owned · Flat honest pricing · Cancel anytime.
- **Service area:** Arcata, Eureka, and surrounding Humboldt County.
- **Differentiator to lean on (via CMS):** software-scheduled routes = "we never
  miss a visit." Reliability is the product.
- **Contact:** info@humboldtscoopsolutions.com · Arcata, CA.
- **Do-not-invent:** prices (dynamic via `hss_pricing()`), team photos (missing —
  see photo-shoot plan), any claim of coverage outside Humboldt County.

---

## Build Items

Each item shows its **Pitch**, its **Fields & Prompts** (copy + an art-generation
spec), and review notes — the four-gate structure the Model Builder walks.

### 1. Business card `business-card` · ASSET_ONLY · image

**Pitch:** A pocketable trust signal for door-to-door, community boards, and
leave-behinds. Front = brand + tagline; back = services + QR to the quote form.

**Copy**
- Front: logo · "A cleaner yard, without the dirty work." · Arcata • Eureka • Humboldt County
- Back: "Weekly · Bi-weekly · One-time · Commercial / HOA" · "Flat honest pricing · Cancel anytime" · info@humboldtscoopsolutions.com · [QR → quote form] · "Locally owned"

**Art-prompt (front), 3.5×2in @ 300dpi (1050×600px):**
> Clean flat business-card front for a friendly local pooper-scooper service,
> deep navy `#1b3a5c` background, cream `#fbf9f5` type, warm gold `#e8a030` accent
> rule, small teal paw/pine motif, generous whitespace, no clutter, print-ready,
> logo placeholder top-left. Warm, trustworthy, small-business, NOT corporate.

**Notes:** Use the real logo (do not regenerate it). QR must point at the live
quote form only. Two-color-friendly for cheap printing.

### 2. Logo application sheet `logo-application` · ASSET_ONLY · image

**Pitch:** Show the *existing* logo used consistently across surfaces (card, sign,
truck magnet, shirt, invoice header) so vendors and the team apply it correctly.

**Fields:** clear-space rule, min size, navy-on-cream + cream-on-navy lockups,
one-color fallback. **No redesign of the logo** — application only.

**Art-prompt:** a tidy brand-application board (grid of mockups) — omit until the
real logo file is dropped in; generating a fake logo here would violate "no rebrand."

**Notes:** BLOCKED on the real logo asset. Flag for Silas: point me at the logo file.

### 3. Lawn sign `lawn-sign` · ASSET_ONLY · image

**Pitch:** The highest-ROI local ad — a yard sign at serviced homes ("This yard
kept clean by Humboldt Scoop") turns every customer into a referral billboard.

**Copy:** "This yard: scooped & tidy 🐾" · "Humboldt Scoop Solutions" ·
"humboldtscoopsolutions.com" · small "Locally owned • Arcata".

**Art-prompt, 18×24in yard sign (900×1200px):**
> Double-sided yard-sign design, navy `#1b3a5c` field, big cream headline, gold
> `#e8a030` accent bar, simple teal pine + paw icon, high-contrast readable from
> the sidewalk, weatherproof screen-print friendly, cheerful and neighborly.

**Notes:** Customer opt-in required before placing a sign at their home (consent
is a human step, not automated).

### 4. Banner `banner` · ASSET_ONLY · image · 1280×720

**Pitch:** A reusable wide banner for the farmers-market booth, community events,
and the top of any digital ad set.

**Copy:** "A cleaner yard, without the dirty work." · "Weekly pooper-scooper
service in Arcata & Eureka" · "Get a free quote → humboldtscoopsolutions.com".

**Art-prompt, 1280×720:**
> Wide horizontal event banner, navy-to-teal soft gradient, cream headline left,
> friendly dog + tidy backyard illustration right (fog-kissed NorCal vibe), gold
> CTA pill, lots of breathing room, welcoming and clean.

### 5. Flyer `flyer` · ASSET_ONLY · image

**Pitch:** A single-page leave-behind for apartment complexes, HOA boards, and vet
offices — the B2B/property-manager door-opener.

**Copy blocks:** headline "Tired of the backyard minefield?" · 3 value cards
(🌲 Local & dependable · 🧼 Thorough & tidy · 💙 Friendly & flexible) · "Serving
renters, HOAs, landlords, breeders & shared spaces" · tear-off/QR CTA.

**Art-prompt, 8.5×11in (1275×1650px):** print flyer, cream paper, navy headline,
teal cards, gold CTA, one warm photo-real dog-in-yard hero area (leave space),
approachable, uncluttered.

**Notes:** Property-manager version should swap the hero line to "Keep every unit's
yard clean — one invoice, one reliable route" (ties to the CMS route-maker).

### 6. Website mockup board `website-mockup` · ASSET_ONLY · image

**Pitch:** The site already exists and is authoritative — this is a *refinement*
board, not a redesign: it visualizes the two P1 content gaps landing (team photos +
narrative bios) and a testimonial pull-quote in the social-proof slot.

**Fields:** annotate the existing single-page anchor layout (Hero → Why Us →
Offer → Pricing → Who → About → FAQ → Poopstakes → Quote). Show the About section
*with* photos and 2-sentence bios; add one customer pull-quote near the hero.

**Notes:** No layout/nav changes proposed. Real screens win. This board exists to
make the CONTENT-BRIEF's priority order visible, not to rebuild the site.

### 7. App mockup board `app-mockup` · ASSET_ONLY · image

**Pitch:** Preview the field/customer app powered by `humboldt-scoop-cms` — the
Android-first route client — as a marketing proof point: "software-scheduled, never
miss a visit."

**Fields:** three phone frames — (a) today's optimized route/map, (b) a customer's
property + pets + schedule, (c) visit-logged confirmation. Dummy data only.

**Notes:** Uses seed/dummy data only (per CMS `notes_from_silas` — no real customer
data, addresses, or map-provider billing). Marketing may reference "route-optimized
reliability"; it may NOT imply features that aren't built yet.

### 8. Photo-shoot plan `photo-shoot-plan` · ASSET_ONLY · plan

**Pitch:** The single highest-impact gap in the whole brand (per CONTENT-BRIEF): real
team photos + a few real yard/action shots. This is a *plan*, not a generated image.

**Shot list:**
1. Viktors (Founder) — friendly half-body, navy shirt, outdoor Arcata light.
2. Silas (Ops & Web) — same treatment, consistent framing.
3. Kathryn "superkate!" (Marketing) — warmer, on-brand playful.
4. Hero: a scooper (branded shirt) in a tidy backyard, dog nearby, morning fog.
5. Detail: sanitized tools / double-bag step (the "thorough & tidy" proof).
6. Sign-in-yard candid (for the lawn-sign social proof).

**Direction:** consistent 3:4 portraits, cream/navy wardrobe, natural NorCal light,
genuine-not-stock. Consent required for any person or customer property shown.

### 9. Print & video shot lists `video-shot-list` · ASSET_ONLY · plan

**Print:** card, sign, flyer hero, booth banner (covered above).
**Video (15–30s):**
1. Problem: cluttered backyard, owner sighs (2s).
2. Solution: branded van/scooter arrives, friendly wave (3s).
3. Process montage: scoop → double-bag → sanitize (6s).
4. Payoff: kid + dog play on a clean lawn (4s).
5. CTA card: tagline + quote URL + "Locally owned, Arcata & Eureka" (3s).

### 10. Static ad concepts `static-ads` · ASSET_ONLY · image

**Pitch:** A small set of square social/static posters for local awareness — three
angles, one per audience.

**Concepts:**
- A) Homeowner — "Reclaim your backyard." tidy-lawn hero, gold CTA.
- B) Property manager — "One route. Every unit. One invoice." (CMS angle.)
- C) Poopstakes — "New customers win local goodies + good-dog bragging rights."

**Art-prompt (each), 1080×1080:** clean square poster, brand palette, single big
idea, cream headline on navy or teal, gold CTA pill, one friendly focal image,
lots of negative space, thumb-stopping but not loud.

**Notes:** Concepts only. No ad account, no spend, no posting — that's a Silas gate.

### 11. Video commercial treatment `commercial-treatment` · ASSET_ONLY · plan

**Pitch:** A 30-second local spot treatment built from the shot list — warm,
neighborly, a little funny, ending on reliability.

**Treatment:** Open on the universal dread of the "backyard minefield." Cut to the
friendly HSS arrival (the reliability beat — "same day, every week, because a route
says so"). Montage of the tidy process. Land on a clean yard, a happy dog, and the
tagline. VO warm and local; no jingle needead — let the Humboldt calm carry it.

### 12. Storyboard `storyboard` · ASSET_ONLY · image

**Pitch:** 5-panel board visualizing the treatment for review before any shoot.

**Art-prompt:** a 5-panel storyboard sheet, simple warm line-art, navy/cream/gold,
panels = dread → arrival → process → payoff → CTA card. Rough, for alignment only.

### 13. Week-by-week launch plan `launch-plan` · ASSET_ONLY · plan

A staged, low-cost, local-first rollout. Everything outward-facing is a Silas gate.

| Week | Focus | Deliverables ready | Human gate before it goes out |
|---|---|---|---|
| 0 | Foundations | Approve concepts (this deck); confirm live pricing; shoot team photos | Silas approves deck; books shoot |
| 1 | Site content | Team photos + bios live; one testimonial slot; FAQ +3 Qs | Silas publishes site edits |
| 2 | Yard presence | Lawn signs printed; consent flow for placement | Silas approves print spend + customer opt-in |
| 3 | Leave-behinds | Business cards + flyers printed; vet/HOA drop list | Silas approves print run + outreach list |
| 4 | Local awareness | 3 static ad concepts finalized | Silas approves ad account + budget (spend gate) |
| 5 | Booth/events | Banner printed; farmers-market booth kit | Silas books event |
| 6 | Video | Shoot per shot list; edit 30s spot | Silas approves shoot + posting |
| 7 | Poopstakes push | Cadence + concrete prize defined; rules link | Silas approves promotion + rules |
| 8 | Measure | "How did you hear about us?" tracking review | — |

---

## Safety & provenance

- **No outward action taken.** No image generated, nothing published, printed,
  posted, emailed, or purchased. Every outward step in the launch plan is an
  explicit Silas gate.
- **No rebrand.** Existing logo, copy, palette, pricing mechanism, and site
  structure are treated as authoritative; items 2 and 6 explicitly defer to them.
- **Real data protected.** App item uses dummy data only; no customer addresses,
  no map-provider billing, no live pricing invented.
- **To generate the visuals:** run each image item's prompt/size through the Model
  Builder GENERATE_ASSETS stage (a1111/comfy) under Silas's team tokens, review
  candidates, then promote only approved assets. That step is intentionally NOT
  done here.

## Open questions for Silas

1. Where is the real **logo** file? (Unblocks items 1, 2, 3, 4, 5.)
2. Are all four **pricing** tiers populated in WP admin (base + per-additional-dog)?
3. Approve the **photo-shoot** as Week 0 priority?
4. Any budget ceiling for print (signs/cards/flyers) so I can right-size quantities?
