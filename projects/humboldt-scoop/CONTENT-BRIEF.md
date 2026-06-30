# Humboldt Scoop Solutions — Content Brief

Generated: 2026-06-30
Source: `projects/humboldt-scoop/scoops/wp-content/themes/humboldt-scoop-solutions/`

---

## Current Site Structure

The site is a single-page layout with anchor-linked sections. One domain, no dedicated blog or secondary pages visible in the theme files.

| Section | Anchor | Status |
|---|---|---|
| Hero | (top) | ✓ copy exists |
| Why Us | `#hss-why` | ✓ copy exists |
| What We Offer | `#hss-services` | ✓ copy exists |
| Pricing | `#hss-pricing` | ✓ structure exists — data from `hss_pricing()` function |
| Who We Serve | `#hss-who` | ✓ copy exists |
| About / Team | `#hss-about` | ✓ bios present — **photos missing** |
| FAQ | `#hss-faq` | ✓ 6 questions answered |
| Poopstakes | `#hss-poopstakes` | ✓ copy exists |
| Contact / Quote Form | `#hss-contact` | ✓ form fields defined |

Navigation order: Why Us → What We Offer → Pricing → Who We Serve → FAQ → Poopstakes → **Get a Quote** (CTA button)

---

## What Copy Exists

### Hero
> "A cleaner yard, without the dirty work."
> "Humboldt Scoop Solutions handles your dog's business so you don't have to. Reliable, local, and friendly pooper-scooper service for homes, rentals, and shared spaces."

Trust badges: ✓ Locally owned · ✓ Flat honest pricing · ✓ Cancel anytime

**Assessment:** Tagline is strong. Body copy is slightly generic — could lean harder on the Humboldt/Northern CA identity.

---

### Why Us
Three value cards:
1. 🌲 **Local & dependable** — real Humboldt folks you can count on, week after week
2. 🧼 **Thorough & tidy** — double-checked yard, no missed spots, tools sanitized between stops
3. 💙 **Friendly & flexible** — easy scheduling changes, no long-term contract required

**Assessment:** Solid. The emoji icons feel warm and on-brand. Card copy is brief but complete.

---

### What We Offer
Service tiers:
- **One-Time Cleanup** — single visit, for first cleans or pre-event prep
- **Weekly** (badge: Most Popular) — steady, hassle-free ongoing service
- **Bi-Weekly** — good middle ground for lower-traffic yards
- **Monthly** — light maintenance for smaller or occasional-use spaces
- **Commercial / HOA / shared spaces** — multi-dog parks, rental complexes, communal yards

**Assessment:** Tier names are clear. No pricing shown in this section (deferred to #pricing). Commercial call-out is important for B2B leads — could use a bit more specificity.

---

### Pricing
Pricing data is dynamic via `hss_pricing()` WordPress function — actual prices are not hardcoded in the template. Featured plan is `weekly`.

**Assessment:** Pricing mechanism is correct (admin-editable). Unknown whether all tiers are currently populated with real numbers — needs a check in WP admin. The pricing section should show base price + "per additional dog" rate for each tier.

---

### Who We Serve
Customer segments listed:
- Apartment renters / HOAs
- Landlords and property managers
- Elderly residents
- People with disabilities
- Busy professionals
- Dog breeders
- Landscapers and contractors
- Parks and shared spaces

**Assessment:** Comprehensive. The order (residential first, B2B at end) is right. Could add a "multiple dogs?" hook since breeders and multi-dog households are a high-value segment.

---

### About / Team
Three team members:
- **Viktors Graube** — Founder
- **Silas Knight** — Operations & Web
- **Kathryn "superkate!" Knight** — Marketing & Community

Avatars are initials-only placeholders.

**Assessment:** Bios exist in template but are placeholder-length (title only, no narrative). This section is the biggest content gap after photos. Each person needs: 1–2 sentences, what they bring to HSS, optional personal hook (e.g. own a dog, local since X year).

---

### FAQ
Six questions currently answered:

1. **Do you need to be home?** No — just need access to the backyard.
2. **What happens to the waste?** Double-bagged and left in your bin (or taken away — per plan).
3. **What if my dog is outside?** Contact us; most dogs are fine, but we'll work with you.
4. **Can I cancel anytime?** Yes — no long-term contracts.
5. **How does billing work?** Monthly billing after service.
6. **What areas do you cover?** Arcata, Eureka, and surrounding Humboldt County.

**Assessment:** Good coverage of objections. Missing: (a) what happens if it rains or we skip a visit, (b) do you work with large breeds / multiple dogs, (c) how do I get started / how fast can service begin? Consider adding 2–3 more questions.

---

### Poopstakes
> "Every new customer is automatically entered into our giveaway — win free service, local goodies, and good-dog bragging rights."

**Assessment:** Charming and on-brand. Needs: (a) how often do drawings happen (monthly? quarterly?), (b) what "local goodies" specifically (even a vague "Humboldt-made treats" is better than nothing), (c) a lightweight rules/transparency link.

---

### Contact / Quote Form
Fields: Name, Phone, Email, City, Number of dogs, Interested in (dropdown), Message  
Contact: `info@humboldtscoopsolutions.com` · Arcata, CA

**Assessment:** Form is clean. "City" is a good qualifier. "Number of dogs" is useful for pricing context. Consider adding "How did you hear about us?" — especially to track Poopstakes referral source.

---

## What's Missing

| Gap | Priority | Notes |
|---|---|---|
| Team photos | P1 | Initials avatars are explicitly placeholders in source code |
| Team bios (narrative) | P1 | Only job titles present; no personal copy |
| Pricing numbers confirmed live | P1 | `hss_pricing()` powers the section — need WP admin check |
| FAQ: missed-visit policy | P2 | What happens if service is skipped (weather, holiday)? |
| FAQ: large dogs / multiple dogs | P2 | High-value segment needs its own answer |
| FAQ: how fast to start | P2 | Onboarding question that converts fence-sitters |
| Poopstakes: cadence + prize specifics | P2 | "Local goodies" needs a concrete example |
| Commercial CTA specificity | P3 | "Contact us" is fine but a dedicated commercial inquiry path would help |
| Multi-page content (blog, gallery) | P3 | Single-page is intentional; blog is a later investment if at all |

---

## Tone & Voice Assessment

**Current tone:** Warm, local, a little playful ("good-dog bragging rights"), practical ("flat honest pricing," "cancel anytime").  
**What's working:** The emoji accents (🌲🧼💙), the nickname "superkate!", the Poopstakes idea — these read as genuine small-business personality, not corporate copy.  
**Suggested adjustments:**

1. **Lean harder into Humboldt identity.** "Locally owned" is stated but not felt. One or two region-specific details (Arcata fog, NorCal dogs, "your neighbors") make the brand stickier.
2. **Add one voice of a customer.** Even a single pull-quote placeholder ("HSS is the best thing to happen to our backyard — Arcata, CA") would warm the social proof section significantly.
3. **Hero body copy:** "homes, rentals, and shared spaces" is accurate but flat. Try: "whether you've got one senior dog or a yard full of puppies, we show up on schedule so you don't have to think about it."
4. **Team section:** The most underleveraged section on the page. A founder's 2-sentence story ("Viktors started HSS because...") converts more than any feature list.

---

## Priority Order for Content Refresh

1. **Team photos** — single highest-impact gap; section reads unfinished without them
2. **Team bios (2–3 sentences each)** — founder story, roles, and one personal hook per person
3. **Pricing confirmation** — verify WP admin has all four tiers priced + dog-count pricing set
4. **FAQ expansion** — add 2–3 questions (missed visit, fast start, large/multi-dog)
5. **Poopstakes specifics** — cadence and at least one concrete prize example
6. **Hero body copy refresh** — optional but worth a pass once team section is solid
7. **Social proof / testimonials** — future milestone once first customers provide feedback

---

*Next: once Silas adds team photos and bios, the About section becomes the site's strongest trust signal. All other gaps are polish.*
