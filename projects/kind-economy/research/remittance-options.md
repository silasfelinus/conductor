# How the mission third reaches AMF — structure first, mechanism second

**Task:** `kind-economy/t-005`. Research and recommendation only. No account created, no
contact made with AMF or any platform, no money moved. **This is not legal or tax advice.**
It is general information from public sources, organized to give Silas (and a CPA/attorney
he retains) a concrete starting point. **Nothing here should be built on until a CPA
confirms the structure**, per the task's own requirement.

## The question Silas asked

> "Can I take money and then give it directly to againstmalaria to be considered tax
> neutral? Is there a way we can automate that 1/3 so it is directly paid to our
> fundraiser to avoid any IRS double dipping?"

## The problem, confirmed real

Taking $100 and later donating $33 does **not** net to zero by default. The $100 is gross
receipts the moment it's charged to Kind Robots. The $33 is a *separate* charitable
contribution, and whether it offsets anything depends entirely on entity type and whether
itemizing is worth it:

- **Sole prop / single-member LLC** (Kind Robots' likely current shape): a charitable
  contribution is not a Schedule C business expense — it only reaches Schedule A itemized
  deductions on the personal return. Silas is very likely taking the standard deduction
  like most filers, in which case the deduction is worth **$0** and the full $100 stays
  taxable. This is the double-dip he's worried about, and it is the default today.
- **Partnership / S-corp**: same shape — passes through to the personal return, same
  itemization problem.
- **C-corp**: the corporation can deduct directly, but capped at 10% of taxable income
  (with a new 1% floor added for tax years beginning after 2025-12-31), excess carried
  forward five years. Committing a third of revenue to donations blows past that cap
  immediately — the corporation would owe tax on the excess it can't yet deduct.

None of these make a flat "donate a third" mechanism tax-neutral by itself. **The fix has to
be structural — keeping the mission third out of Kind Robots' gross receipts in the first
place — not a bigger or smarter deduction.**

## Option A — the customer donates directly; it never becomes Kind Robots' revenue

This is the direct, strong answer to "automate that 1/3." Structure checkout so the
customer's mission third is *their own* donation to AMF, not Kind Robots' money passing
through. If it genuinely never touches Kind Robots' books as revenue, there's no deduction
question to solve — Kind Robots' gross receipts are two-thirds (split further into the
creator third and the platform third), and "a third of what you pay buys nets" becomes a
literally true, independently verifiable claim instead of a promise resting on a deduction
that doesn't work.

### Mechanism: Every.org, not Stripe Connect

**Stripe Connect is a dead end for this and should be dropped from the design entirely.**
Connect exists to split *one* payment across parties who are all onboarded Connect accounts
(e.g., a marketplace and its sellers). AMF is not going to onboard as a Stripe Connected
Account for Kind Robots specifically, and there's no indication any major charity does this
routinely for individual commerce integrations. Stop designing toward it.

**Every.org** is the workable alternative:

- [Every.org](https://www.every.org/) is itself a 501(c)(3) (EIN 61-1913297) running a
  no-platform-fee donation infrastructure: no cut of the donation, no monthly/setup fee.
- Its [free Charity API](https://www.every.org/charity-api) covers 1M+ registered US
  501(c)(3)s, with an [embeddable donate link/button](https://docs.every.org/docs/intro)
  that accepts URL parameters to pre-fill amount, frequency, and flow behavior (including
  whether the donor is redirected back to Kind Robots after completing the gift).
- **The Against Malaria Foundation (US)** — EIN 20-3069841, Kansas City MO, the exact EIN
  Silas already has on file — **is confirmed listed and routable** at
  [every.org/againstmalaria](https://www.every.org/againstmalaria). Verified directly,
  live, during this research (not assumed from the API docs).
- Reconciliation: Every.org offers both a
  [Nonprofit Donation Webhook](https://docs.every.org/docs/webhooks/nonprofit-webhook)
  (fires to AMF's own admins) and a
  [Partner Webhook](https://docs.every.org/docs/webhooks/partner-webhook) (fires to Kind
  Robots as the referring partner, keyed by a partner donation ID Kind Robots sets on the
  Donate Link). The partner webhook payload includes amount, currency, net-of-fees amount,
  and the recipient nonprofit's slug/EIN/name — enough to reconcile a specific donation back
  to the interaction that generated it.
- Money flow: donations settle to Every.org first; Every.org grants the funds to AMF's bank
  account on a weekly cycle once AMF has deposit info on file with Every.org (a detail for
  AMF's own Every.org account, not something Kind Robots manages).

### The catch, researched honestly — and it's a real one, more concrete than "check the seven co-venture states"

The original task note flagged commercial-co-venture registration (7 states: AL, CA, HI,
IL, MA, MS, SC) as the thing to check. That's necessary but **understates** the actual
exposure. A newer, broader category is more directly on point:

**California's "charitable fundraising platform" law** (final regulations effective
2024-06-12) defines a covered platform as *"a person, corporation, or other legal entity
that provides a website, mobile device application, or other internet-based platform to
Californians, and performs, permits, or enables solicitations through its platform,"*
**explicitly including** cases where *"platform users make purchases or perform other
activity that cause donations to be sent to one or more charities based on their purchases
or activity."*

That is Option A's mechanism, described almost word for word. Read straightforwardly, a
checkout flow where a customer's purchase causes a donation to AMF makes Kind Robots itself
a "charitable fundraising platform" under California law — not just a commercial
co-venturer — with its own registration (Form PL-1, $625 fee, annual PL-2 renewal at $625)
independent of whatever Every.org itself has already registered. **Hawaii enacts an
equivalent law effective 2026-01-01.** More states are actively moving this direction (see
Illinois, New York cause-marketing guides turned up in this research); treat this as a
growing category, not a fixed list of seven.

One narrower reading may reduce exposure, and it's the load-bearing fact question a
CPA/attorney needs to resolve before anything is built: California's own guidance
distinguishes a platform that *enables solicitations through its platform* from one that
merely **links out** to another party's already-registered donation page. *"A charitable
organization that has its own platform, and solicits donations only for itself through its
own platform, is not a charitable fundraising platform"* — by extension, if the mission
third is completed as a genuine **redirect to Every.org's own hosted donate page** (Every.org
processes the transaction, issues the tax receipt, is the party actually "enabling" the
solicitation) rather than an **embedded flow inside Kind Robots' own checkout UI** (where
Kind Robots' own pages/APIs are the thing performing the solicitation), Kind Robots' own
registration exposure is plausibly lower. This research could not find a source that
resolves this cleanly either way for Every.org specifically — Every.org's own compliance
messaging says *it* handles registration/receipting for the donation, but doesn't address
whether a commercial partner embedding its widget also needs its own registration. **This
is exactly the fact pattern to put in front of a CPA/attorney before building anything**,
and it changes the engineering approach materially:
- **Lower-registration-risk design:** at the mission-third step, redirect the customer to
  Every.org's hosted donate page for AMF (pre-filled amount via URL params), let them
  complete the donation there, and use the Partner Webhook to reconcile back. Kind Robots
  never renders its own donation-collection UI for that leg.
- **Higher-registration-risk design:** embed Every.org's flow inside Kind Robots' own
  checkout page so it feels seamless. More likely to read as Kind Robots itself "enabling
  solicitations through its platform" under the CA definition above.

Either way, if Kind Robots reaches meaningful volume from California donors specifically,
budget for the possibility of registering as a commercial co-venturer and/or charitable
fundraising platform in at least California, and monitor Hawaii from 2026-01-01. This is a
real, recurring compliance cost (~$625/state/year plus filing), not a one-time setup fee —
size it against actual expected donation volume before committing to the embedded design.

## Option B — Section 162 business expense instead of Section 170 charitable contribution

If a payment to AMF carried a genuine return benefit commensurate with its value —
sponsorship recognition, logo placement, advertising — it could be deducted as an ordinary
Section 162 business expense with **no percentage-of-income ceiling**, instead of a capped
Section 170 charitable contribution. This is a real, IRS-recognized distinction (the
sponsorship/advertising line), not a workaround: *"a payment or transfer to or for the use
of a tax-exempt charitable organization that bears a direct relationship to the taxpayer's
trade or business and that is made with a reasonable expectation of financial return
commensurate with the amount of the payment ... may constitute an allowable deduction as a
trade or business expense rather than a charitable contribution."*

The code is explicit that this only works where the business return is **actual**, not
manufactured to dodge Section 170's limits — the IRS looks at substance. AMF is not going to
provide Kind Robots with $ex-thousands of dollars in bona fide advertising value each month
in a way that would survive scrutiny at Kind Robots' likely volume. **This is fact-specific
and belongs in front of the CPA as a secondary question, not the primary structure** — flag
it, don't design around it as Plan A.

## Option C — baseline, already working, keep it regardless of what else ships

Kind Robots already links donors out to `againstmalaria.com/amibot` for direct giving from
`giving-page.vue` (confirmed in the kind-economy design-brief audit). Zero complication,
zero reporting burden, no registration question at all — it's how the existing ~$840 was
raised. **Whatever else gets built, this stays live**, both as a fallback if Option A's
compliance cost doesn't pencil out yet, and as an option for donors who'd rather give
outside a specific purchase flow.

## Recommendation

**Primary: Option A, implemented as a redirect-to-Every.org's-hosted-page design, not an
embedded-in-checkout design**, specifically because it plausibly minimizes the "charitable
fundraising platform" registration question while still (a) keeping the mission third out
of Kind Robots' gross receipts, (b) making "a third of what you pay buys nets" literally,
verifiably true via the Partner Webhook, and (c) giving the customer their own real,
receipted, deductible donation. Do not build the embedded-in-checkout variant until a
CPA/attorney has specifically opined on the CA/HI platform-registration exposure described
above — that opinion is the actual gate, not a formality.

**Fallback: Option C stays live unconditionally**, and is the right default if the CPA
review of Option A takes a while or comes back requiring registration overhead Silas
doesn't want to carry yet.

**Secondary, not primary: Option B** — worth a CPA's opinion on whether any portion of a
platform-level relationship with AMF (co-branding, impact reporting, etc.) could
legitimately support a Section 162 characterization for the *platform's* own contribution,
but this does not solve the customer-facing "automate the 1/3" ask on its own and should not
block Option A's design.

**What Option A is explicitly not settled on:** whether the redirect-vs-embedded
distinction actually changes Kind Robots' registration obligation under California's
charitable-fundraising-platform regulations, and what (if anything) Every.org's own terms
say about partner liability when its widget is embedded versus linked to. Both are concrete
questions for the CPA/attorney conversation this task set out to prepare for — not resolved
here, and this document should not be read as though they were.

## Sources

- [Every.org — Nonprofit Fundraising Platform Overview](https://www.every.org/)
- [Every.org — Free Charity API](https://www.every.org/charity-api)
- [Every.org Charity API Docs — Introduction](https://docs.every.org/docs/intro)
- [Every.org Charity API Docs — Nonprofit Donation Webhook](https://docs.every.org/docs/webhooks/nonprofit-webhook)
- [Every.org Charity API Docs — Partner Webhook](https://docs.every.org/docs/webhooks/partner-webhook)
- [Every.org — The Against Malaria Foundation profile](https://www.every.org/againstmalaria)
- [IRS EOS — The Against Malaria Foundation, EIN 20-3069841](https://apps.irs.gov/app/eos/detailsPage?ein=203069841&name=The+Against+Malaria+Foundation&city=Kansas+City&state=MO&countryAbbr=US&type=returnsSearch)
- [Charity Navigator — The Against Malaria Foundation](https://www.charitynavigator.org/ein/203069841)
- [Labyrinth Inc. — Cause Marketing and Commercial Co-Venture Registration](https://labyrinthinc.com/cause-marketing-commercial-co-venture-registration/)
- [Greenberg Traurig — California Charitable Fundraising Platforms Final Regulations](https://www.gtlaw.com/en/insights/2024/4/effective-june-12-california-issues-final-regulations-for-charitable-fundraising-platforms)
- [CA Attorney General — Charitable Fundraising Platforms](https://www.oag.ca.gov/charities/pl)
- [Affinity Fundraising Registration — Does a Donate Button Trigger Registration Requirements?](https://www.fundraisingregistration.com/resources/topic/donate-button-trigger-registration-requirements/)
- [Perlman & Perlman — Charitable Fundraising Registration FAQ](https://perlmanandperlman.com/charitable-fundraising-registration-faq/)
- [Cornell LII — 26 U.S. Code § 162, Trade or Business Expenses](https://www.law.cornell.edu/uscode/text/26/162)
- [LegalClarity — Is a Sponsorship Tax Deductible?](https://legalclarity.org/when-is-a-sponsorship-tax-deductible/)

## Next steps this unblocks

- `kind-economy/t-002`/`t-003` (entity-shape decisions) can proceed knowing Option A does
  not require reviving Save One Human — it works identically for a for-profit structure.
- Before any implementation task designs a checkout flow around this: get the CPA/attorney
  read on the redirect-vs-embedded registration question above. That answer should become
  its own roadmap task once Silas has it, rather than being assumed either way here.
