# Reference Run — Humboldt Scoop Solutions Marketing Deck

**Model Builder run (t-016) · autonomous full-example set**

- **Source model:** `humboldt-scoop` (Project)
- **Related source:** `humboldt-scoop-cms` (route-maker / reliability proof)
- **Recipe:** `marketing-deck`
- **Grounding (authoritative, no rebrand):** `projects/humboldt-scoop/CONTENT-BRIEF.md`,
  the live theme, and Silas's data below. Existing logo, copy, and product screens win.

> **How gates work here (corrected):** the four gates are **optional front-end
> pauses** a user can place on a request — e.g. "don't generate this item" or "stop
> after prompt creation so I can edit before art." They are **not** a backend block
> that waits on a repo file. This run assumes the default: **create full objects**
> (examples for everything) with minimal human interaction. Generated project art is
> pre-approved internal work (AGENTS.md, 2026-07-06).
>
> **What still isn't automatic:** the generator's hard rule is *no text / no logo / no
> watermark*, so it produces the **text-free imagery**; the real logo (`logo_clean.jpg`)
> and copy are composited in a layout step. And live spend / posting / printing / real
> customer contact stay off by default — those aren't "gates to wait on," they're just
> out of scope for an internal example set.

## Brand kit (authoritative)

- **Name (always paired):** **Humboldt Scoop Solutions — Professional Pet Waste Removal.**
  The descriptor "Professional Pet Waste Removal" always follows the name.
- **Tagline:** "A cleaner yard, without the dirty work."
- **Logo:** `projects/humboldt-scoop/scoops/wp-content/uploads/2026/01/logo_clean.jpg`
  (real file — composite it into laid-out pieces; never AI-generate or restyle it).
- **Voice:** warm, local, lightly playful; practical and honest. Humboldt-proud.
- **Palette:** navy `#1b3a5c` (primary) · cream `#fbf9f5` / `#f5f0e8` (paper) ·
  gold `#e8a030` (CTA/accent) · teal `#7bbfb5` / `#a7dccb` (fresh/clean) ·
  earthy rust `#b9684f` / `#8b2a1a` (grounding accent).
- **Trust badges:** Locally owned · Flat honest pricing · Cancel anytime.
- **Differentiator (via CMS):** software-scheduled routes = "we never miss a visit."
- **Contact:** info@humboldtscoopsolutions.com · Arcata, CA.

### Pricing (authoritative — Silas)

Rates by number of dogs; **billed on the 1st of the month.**

| Plan | 1 dog | 2 dogs | 3 dogs | 4+ dogs |
|---|---|---|---|---|
| **Weekly** | $19 | $22 | $25 | by quote |
| **Bi-weekly** (every 2 weeks) | $30 | $35 | $40 | by quote |
| **Monthly** | $50 | $60 | $70 | by quote |

(Plus **One-Time Cleanup** for first cleans / pre-event, per existing site tier.)

### Service area

- **Core:** Eureka · Arcata · McKinleyville.
- **Also serving / by request:** Trinidad · Cutten · Freshwater · Blue Lake.
  (Reasonable estimate — confirm/trim later.)

---

## Build Items

Each item shows its **Pitch**, its **Copy/Fields**, and its **Art** (a text-free
generation prompt for the pipeline, or "layout" when it's an assembly of imagery +
logo + copy). Sizes are print- or platform-correct.

### 1. Business card `business-card` · ASSET_ONLY

**Pitch:** Pocketable trust signal for door-to-door, community boards, leave-behinds.

**Copy** — Front: logo · "Humboldt Scoop Solutions — Professional Pet Waste Removal" ·
"A cleaner yard, without the dirty work." · Eureka • Arcata • McKinleyville.
Back: "Weekly from $19 · Bi-weekly from $30 · Monthly from $50 · One-time & 4+ dogs by
quote" · "Flat honest pricing · Cancel anytime · Billed the 1st" ·
info@humboldtscoopsolutions.com · [QR → quote form].

**Art:** *layout* — navy card, cream type, gold rule, teal pine/paw motif; real logo
top-left; generatable component = the small paw/pine flourish (text-free).

### 2. Logo application sheet `logo-application` · ASSET_ONLY

**Pitch:** Show the real logo used consistently across surfaces (card, sign, magnet,
shirt, invoice header) so vendors/team apply it correctly. **No redesign.**

**Fields:** clear-space, min size, navy-on-cream + cream-on-navy lockups, one-color
fallback — all using `logo_clean.jpg`. **Art:** *layout only* (no generation).

### 3. Lawn sign `lawn-sign` · ASSET_ONLY · 18×24in

**Pitch:** Highest-ROI local ad — a sign at serviced homes turns customers into
referral billboards. (Customer opt-in before placing.)

**Copy:** "This yard: scooped & tidy 🐾" · "Humboldt Scoop Solutions — Professional
Pet Waste Removal" · "humboldtscoopsolutions.com" · "Locally owned • Eureka–Arcata".

**Art:** *layout* over a text-free generated background — see queue `marketing-sign-bg`.

### 4. Banner `banner` · ASSET_ONLY · 1280×720

**Pitch:** Reusable wide banner for the farmers-market booth, events, and the top of
digital ad sets.

**Copy:** name + descriptor · "A cleaner yard, without the dirty work." · "Weekly pet
waste removal in Eureka, Arcata & McKinleyville" · "Free quote → humboldtscoopsolutions.com".

**Art:** text-free wide illustration — queue `marketing-banner-bg` (1280×720).

### 5. Flyer `flyer` · ASSET_ONLY · 8.5×11in

**Pitch:** Single-page leave-behind for apartments, HOA boards, and vet offices — the
B2B/property-manager door-opener.

**Copy:** headline "Tired of the backyard minefield?" · 3 value cards (🌲 Local &
dependable · 🧼 Thorough & tidy · 💙 Friendly & flexible) · pricing snapshot · "Serving
renters, HOAs, landlords, breeders & shared spaces" · QR CTA. Property-manager variant
headline: "Keep every unit's yard clean — one invoice, one reliable route."

**Art:** *layout* over a text-free hero image — queue `marketing-flyer-hero`.

### 6. Website mockup board `website-mockup` · ASSET_ONLY

**Pitch:** Site exists and is authoritative — this is a *refinement* board: the two P1
gaps landing (team photos + narrative bios) and a testimonial pull-quote near the hero.
Also surface the confirmed pricing table and service-area line. **No layout/nav change.**

**Art:** *annotation of real screens* (no generation).

### 7. App mockup board `app-mockup` · ASSET_ONLY

**Pitch:** Preview the `humboldt-scoop-cms` Android-first route client as a proof
point: "software-scheduled, never miss a visit." Three phone frames — today's optimized
route, a customer's property + pets + schedule, a visit-logged confirmation. **Dummy
data only.** **Art:** *UI mockup* (no generation).

### 8. Photo-shoot plan `photo-shoot-plan` · ASSET_ONLY

**Pitch:** The single highest-impact brand gap (per CONTENT-BRIEF). Reasonable-estimate
plan; edit later.

**Shot list (estimated):** (1) Viktors — friendly half-body, navy shirt, outdoor
Arcata light; (2) Silas — matching framing; (3) Kathryn "superkate!" — warmer, playful;
(4) hero: branded-shirt scooper in a tidy backyard, dog nearby, morning fog; (5) detail:
sanitized tools / double-bag; (6) sign-in-yard candid. Consistent 3:4 portraits,
cream/navy wardrobe, natural NorCal light, genuine-not-stock. Consent for people/property.

**Art:** text-free mood-board reference — queue `marketing-photo-moodboard`.

### 9. Print & video shot lists `video-shot-list` · ASSET_ONLY

**Print:** card, sign, flyer hero, booth banner (above). **Video (15–30s):**
(1) problem: cluttered yard, owner sighs; (2) solution: branded arrival, friendly wave;
(3) montage: scoop → double-bag → sanitize; (4) payoff: kid + dog on a clean lawn;
(5) CTA card: name + descriptor + quote URL + "Eureka–Arcata–McKinleyville".

### 10. Static ad concepts `static-ads` · ASSET_ONLY · 1080×1080

Three angles, one per audience. **Copy** — A) Homeowner: "Reclaim your backyard.";
B) Property manager: "One route. Every unit. One invoice."; C) Poopstakes: "New
customers win local goodies + good-dog bragging rights." Each: name+descriptor + gold CTA.

**Art:** three text-free square backgrounds — queue `marketing-ad-a/b/c` (1080×1080).

### 11. Video commercial treatment `commercial-treatment` · ASSET_ONLY

30-second local spot, warm and neighborly, landing on reliability. Open on the "backyard
minefield" dread → the friendly HSS arrival (the reliability beat: "same day, every week,
because a route says so") → tidy-process montage → clean yard + happy dog + tagline. VO
warm and local; no jingle — let the Humboldt calm carry it. Full name+descriptor on the
end card.

### 12. Storyboard `storyboard` · ASSET_ONLY

5 panels visualizing the treatment: dread → arrival → process → payoff → CTA card.
**Art:** text-free 5-panel line-art board — queue `marketing-storyboard` (1280×720).

### 13. Week-by-week launch plan `launch-plan` · ASSET_ONLY

Staged, low-cost, local-first. Outward spend/print/posting is out of scope for this
internal example set (do it when Silas is ready), but nothing here waits on a repo file.

| Week | Focus | Ready |
|---|---|---|
| 0 | Foundations | Concepts approved (this deck); pricing confirmed (done); photo shoot booked |
| 1 | Site content | Team photos + bios; testimonial slot; pricing table + area line; FAQ +3 |
| 2 | Yard presence | Lawn signs printed; placement consent flow |
| 3 | Leave-behinds | Cards + flyers printed; vet/HOA drop list |
| 4 | Local awareness | 3 static ad concepts finalized |
| 5 | Booth/events | Banner printed; farmers-market kit |
| 6 | Video | Shoot per shot list; edit 30s spot |
| 7 | Poopstakes | Cadence + concrete prize + rules link |
| 8 | Measure | "How did you hear about us?" tracking review |

---

## Objects created / queued

To make this a real full-object example set with minimal human interaction, the
text-free visual components are queued into the live art pipeline
(`projects/art-generate.yaml`, target `humboldt-scoop`), which the distribute-images
workflow turns into committed HSS ArtCollection images:

`marketing-banner-bg`, `marketing-sign-bg`, `marketing-flyer-hero`,
`marketing-ad-a/b/c`, `marketing-storyboard`, `marketing-photo-moodboard`.

The text/logo layout pieces (card, logo sheet, laid-out sign/flyer/ads) are assembly
steps over those images + `logo_clean.jpg` — kept out of the generator because it
forbids text/logos, and to honor "no rebrand."

## Notes

- No live spend, posting, printing, or real customer contact — internal example set.
- Existing logo/site/pricing mechanism authoritative; the pricing/area/descriptor above
  are Silas-provided truth, folded into the deck and the CONTENT-BRIEF.
