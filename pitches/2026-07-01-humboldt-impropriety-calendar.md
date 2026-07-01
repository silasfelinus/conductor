# Pitch: Humboldt Impropriety Calendar

status: proposed
project: digital-storefront
date: 2026-07-01
product_type_requested: physical-calendar
stakes: outward-facing
human_gate: required

## One-line pitch

Transform the earlier coloring-book direction into a new custom-calendar product line, led by **Humboldt Impropriety Calendar**: a tasteful, consent-first, mature historical art calendar celebrating the people who helped build Humboldt County's adult play-party scene from Club Risqué through Reasons to Say Yes and Humboldt Impropriety Society.

## Why this is a new project, not a coloring-book variant

This is not a coloring book rename. It changes the product type, rights model, contributor workflow, safety requirements, fulfillment stack, and marketing posture.

The proposed product is a physical or printable calendar with twelve contributor/model features, short historical captions, and a public-safe storefront. The private video archive may inform internal research, but it must not be published, uploaded to storefronts, used in listing previews, or shared outside explicit private consent review.

## Product shape

- **Format:** 12-month mature art calendar, likely 2027-ready unless production can move fast enough for a late-2026 drop.
- **Theme:** Humboldt adult-community history, nightlife, performance, play-party culture, and the people behind it.
- **First title:** Humboldt Impropriety Calendar.
- **Tone:** cheeky, reverent, local, queer-positive, sex-positive, safe-ish-for-work in public previews.
- **Content level:** no explicit sex acts in storefront previews; no public use of private event videos; no identifying anyone without signed consent.
- **Calendar pages:** one featured contributor or ensemble per month, plus tasteful caption/history notes.
- **Front-end assets:** cropped, covered, stylized, or illustration-forward previews suitable for a public landing page.

## Contributor model

Each month should have a primary credited model/artist/contributor, even if some pages represent groups or behind-the-scenes contributors. Every contributor must choose one compensation model before publication.

### Option A — royalty share

- Featured month contributor receives **5% of net sales** for calendars sold.
- Twelve months at 5% each = 60% of net sales allocated to featured contributors.
- Remaining 40% covers project/admin share, design/layout, copywriting, storefront, samples, customer support, historical editing, contingency, and reinvestment.
- “Net sales” should be defined as money actually retained after refunds, discounts, sales tax/VAT, payment processing fees, platform fees, print cost, packaging, shipping subsidy, and chargebacks.

### Option B — flat fee

- Contributor may instead choose a flat buyout/feature fee.
- Suggested test range: **$150–$300 per accepted month image**, with the exact number depending on final retail price, expected run size, and whether the contributor supplies production-ready art.
- Flat-fee contributors do not receive ongoing royalties unless negotiated separately.

### Option C — hybrid

- Small upfront fee plus smaller royalty, useful for contributors who need cash now but still want upside.
- Suggested pilot: **$75 upfront + 2.5% net sales** for the featured month.

## Rights and consent requirements

Before anything is shown publicly or sent to a printer, collect a release for every identifiable adult in the calendar image and every credited artist/model/contributor.

Minimum release terms:

- All depicted people are 18+ at the time of image creation and calendar publication.
- Contributor owns or controls the submitted image or has written permission from the photographer/artist.
- Contributor grants calendar-specific print, digital preview, marketing, and archival rights.
- Contributor selects compensation option: 5% royalty, flat fee, or hybrid.
- Contributor approves final crop, caption, credit name, and public bio level.
- Contributor may use legal name, stage name, initials, or anonymous credit.
- Private archival footage remains private unless separately released in writing.
- No revenge, coercive, hidden-camera, intoxication-compromised, or ambiguous-consent material.

## Storefront and payment posture

This should launch as a public-safe landing page plus gated product listing, not as an explicit adult-content site.

Recommended posture:

1. Build a safe landing page with censored/stylized previews, contributor credits, historical framing, FAQ, consent language, and an 18+ notice.
2. Treat checkout/provider selection as a compliance task, not a vibes task. Mainstream processors and POD vendors can reject mature/adult products with little warning.
3. Avoid selling the private archive, videos, or explicit digital content. That moves the project into a much riskier payment/platform category.
4. Prefer physical print sales and preorders with explicit refund, fulfillment, and contributor payout rules.

## Fulfillment research questions

The first implementation task should compare:

- Adult-tolerant short-run printers for wall calendars.
- Print-on-demand vendors that allow mature artistic calendars.
- Manual preorder batch printing versus automated POD.
- Whether a local/regional printer is safer than POD for this particular content.
- Minimum viable run size, sample costs, and per-unit margin at 25 / 50 / 100 / 250 units.

Known concern: some large POD vendors restrict or prohibit adult content, especially on wall calendars. This needs explicit verification before accounts, uploads, or sales.

## Website architecture

For Kind Robots / digital storefront integration:

- Add the project as a new storefront concept after human approval.
- Use a public-safe hero, card, and icon set.
- Keep all API/storefront interactions behind the existing store pattern; front-end components should use Pinia stores, not direct API calls.
- Store release metadata privately; do not expose legal names, emails, private media links, or payout details on the public site.
- Model pages should be optional and only show contributor-approved bios/images.

Suggested data concepts:

- `CalendarProject`
- `CalendarIssue`
- `CalendarMonthFeature`
- `ContributorRelease`
- `ContributorPayoutChoice`
- `SafePreviewAsset`
- `PrivateArchiveReference`

## Initial roadmap proposal

If Silas approves this pitch, add `physical-calendar` or `custom-calendar` to approved product types, then create a new content project or digital-storefront subproject.

Suggested tasks:

1. **Compliance and fulfillment brief** — compare printers, POD rules, payment processors, mature-content constraints, and recommend a launch stack. Ends needs-human.
2. **Contributor release packet** — write model/artist release, payout election form, caption approval sheet, and private-archive boundary policy. Ends needs-human.
3. **Calendar creative bible** — define tone, visual safety rules, month structure, public-safe preview rules, typography/layout direction, and historical caption style. Ends needs-human.
4. **Contributor outreach draft** — write invitation message for past artists/models/contributors explaining the calendar, safety rules, compensation options, and submission specs. Ends needs-human.
5. **Storefront landing-page spec** — design public page sections, safe assets, 18+ notice, preorder CTA, FAQ, and admin needs. Ends needs-human.
6. **Prototype one month** — create a sample month layout using placeholder/safe dummy art only. Ends needs-human.

## Approval needed

This pitch needs Silas to decide:

- Should the approved product type become `physical-calendar`, `print-calendar`, or broader `custom-calendar`?
- Should this live under `digital-storefront` or become a new top-level project, likely `humboldt-impropriety-calendar`?
- Which compensation default should be offered first: 5% net sales, flat fee, or hybrid?
- What content ceiling should be enforced for the public storefront: lingerie/pinup, burlesque/theatrical, implied nudity, artistic nudity, or stricter?

No publishing, vendor upload, contributor contact, payment setup, or public page should happen before explicit approval.
