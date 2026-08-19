# Kind Economy — Design Brief

**Created:** 2026-08-19 · **Project kind:** software (with a human-gated legal track)
**One line:** The money layer for Kind Robots — take money in, split it three ways,
pay creators, send the mission share to the malaria fundraiser, and decide what
legal home that mission needs.

---

## Why this project exists

Silas started **Save One Human** during the pandemic, on the premise that ~$5,000 of
malaria-net funding saves one human life. He incorporated in California, obtained an
EIN, raised $0, and later began unwinding the entity and filing the overdue zero-dollar
returns.

**Kind Robots** is that mission's spiritual successor: use AI to generate revenue for
social good, starting with the Against Malaria fundraiser at
<https://againstmalaria.com/amibot> (~$840 raised to date, almost entirely Silas's own
donations plus birthday-gift redirects from family).

The plan is a **three-way revenue share**: when someone spends paid tokens, the money
splits equally between site admin, the creator of the web object that inspired the
interaction, and the malaria fundraiser.

The site says this out loud already. It is not true yet. This project makes it true.

---

## Verified current state (audited 2026-08-19)

### Take-in side — built, never run with real money

`kind_robots` has real Stripe infrastructure:

| Piece | Where | State |
|---|---|---|
| Checkout / cart | `server/api/stripe/checkout.post.ts` (297 ln) | Written, untested live |
| Mana top-ups | `server/api/stripe/topup.post.ts` — server-trusted $5/$10/$25 tiers | Written, untested live |
| Supporter subscription | `server/api/stripe/subscribe.post.ts` | Written, untested live |
| Cancel subscription | `server/api/stripe/cancel-subscription.post.ts` | Written, untested live |
| Checkout status | `server/api/stripe/checkout-status.get.ts` | Written, untested live |
| Webhook fulfillment | `server/api/stripe/webhook.post.ts` (663 ln) | Signature-verified; idempotent on `stripeSessionId` |
| Data model | `Order`, `OrderItem`, `Entitlement`, `PrintJob`, `Grant`, `ManaTransaction` | Migrated |
| Mana peg | `server/utils/mana.ts` — `PEG_USD_PER_MANA = 0.001` | 1,000 mana = $1 |

**No `STRIPE_SECRET_KEY` or `STRIPE_WEBHOOK_SECRET` is configured anywhere** — not in
the repo, not in CI, no `.env.example`. Test coverage is auth-rejection Cypress specs
only. `digital-storefront/t-039` has been parked at `needs-human` since 2026-08-08 for
precisely this reason: the sandbox cannot reach a database or a Stripe account.

**Not a single real dollar has moved through this code.**

### Split / payout side — does not exist

Five concrete gaps, each verified by reading the code:

1. **The paid resource doesn't exist as a separate thing.** The intended model has two
   currencies — free **mana** (limited access, lower queue priority, never purchased) and
   paid **tokens** (the resource actually spent on generation, created only when real
   money is paid). The code has neither: `User.mana` is one `Int` fed by *both* Stripe
   purchases (`applyMana({ reason: 'PURCHASE' })`) and free grants (`CYCLE_REFILL`,
   `SIGNUP_BONUS`), and there is **no token model in `schema.prisma` at all**. At spend
   time (`manaGate` → `chargeForGeneration`) nothing knows whether the balance being
   burned was bought or given away. **"Paid usage is split three ways" is not currently
   computable from the data we store.** This is the single biggest blocker and everything
   else depends on fixing it.

2. **Spends carry no creator attribution.** `applyMana()` takes a free-text
   `refId: String?`. Nothing records *whose* Scenario, Bot, Character, Facet, or artwork
   seeded the interaction, so a creator's share cannot be computed even in principle.

3. **No payout mechanism at all.** Zero references to Stripe Connect,
   `transfer_data`, `application_fee`, or destination charges anywhere in the repo.
   There is no way to pay a creator a cent today.

4. **No route for the mission share.** `components/pages/giving-page.vue` sends users
   *out* to `againstmalaria.com/amibot`. That is excellent for donor-intent purity — and
   it is how the $840 was actually raised — but it means the site's *own* share of paid
   revenue has no path to the fundraiser.

5. **The promise is already shipped.** `CREATOR_EARNINGS_MESSAGE` in
   `stores/helpers/tutorialCards.ts` appears on six tutorial channels:

   > "When people spend paid tokens on something you made, you earn a share. Paid usage
   > is split three ways - Kind Robots, the anti-malaria fundraiser, and you. Build
   > something people love, and the swarm pays you back."

   Narrator seeds repeat the mission claim across dozens of rooms. At current volume
   (essentially zero paid usage) nobody has been shortchanged, so this is a credibility
   item rather than an incident — but the copy should be **deliberately** either moved to
   future tense or backed by a real mechanism, not left to drift.

### Legal / entity side — researched 2026-08-19

**Save One Human was never a 501(c)(3).** Federal exemption was never applied for.

The repo's own registration checklist records exactly three of ten steps complete:

| Step | State |
|---|---|
| Determine the corporation's name | ✅ |
| File articles of incorporation (`arts-pb.pdf`, Nonprofit **Public Benefit** Corporation, $30) | ✅ |
| Obtain an EIN | ✅ |
| Appoint the board of directors | ❌ |
| Draft bylaws + conflict-of-interest policy | ❌ |
| Take initial board actions | ❌ |
| File CT-1 with the CA AG's Registry of Charitable Trusts | ❌ |
| File the Statement of Information with the CA Secretary of State | ❌ |
| **Apply for federal tax exemption (IRS Form 1023/1023-EZ)** | ❌ **never applied** |
| **Apply for California tax exemption (FTB Form 3500)** | ❌ **never applied** |

Independently corroborated: **ProPublica Nonprofit Explorer returns zero results** for
"save one human" (`total_results: 0`). Nonprofit Explorer mirrors the IRS Exempt
Organizations Business Master File, which only lists organizations the IRS has actually
recognized as exempt — so zero results is exactly what a never-applied entity produces.
There is no public IRS record of this entity and there never was one. The EIN exists but
is not published anywhere, because the IRS does not publish EINs for non-exempt entities.
**The public record that does exist is the California Secretary of State corporate
filing.**

**The expensive finding.** A California nonprofit corporation that never obtained FTB
exemption is taxed exactly like a for-profit corporation and owes the **$800 minimum
franchise tax for every year it existed**, regardless of revenue. Zero income does not
mean zero tax, and filing returns showing $0 taken in does not by itself discharge it.
Incorporated in 2020, that is potentially five-plus years of $800 plus penalties and
interest. This may already have been resolved during the unwind — or it may be an open
liability. Either way it is the single biggest factor in whether reinstating or starting
fresh is cheaper, and it belongs to a CPA.

*Not legal or tax advice — general rules from public sources; the actual situation needs
a professional.*

**The entity is dissolved.** Silas, 2026-08-19: *"Save one human is definitely
disbanded, as far as I know. I finalized that around 2023-2024."* Recorded as his account
rather than a verified filing — the confirming record is the CA SOS entity status, which
this session could not reach (bizfileonline.sos.ca.gov sits behind Incapsula bot
protection; the AG registry at rct.doj.ca.gov returned 503).

So **there is nothing to reinstate.** Any future entity is a new incorporation with a new
EIN — an old EIN cannot be reused for a new corporation. That also means the franchise-tax
question above, whatever its answer, **does not follow him into a future entity**: a new
corporation inherits none of the old one's tax history.

**One question left, and it's a ten-minute closure check rather than a blocker:** which
dissolution route was used, and was **FTB Form 3502** filed? California provides that form
— *Nonprofit Corporation Request for Pre-Dissolution Tax Abatement*, R&TC §23156 —
specifically to abate unpaid qualified taxes, interest, and penalties for a nonprofit that
certifies it never conducted business or has ceased and holds no assets. Save One Human,
with zero revenue ever, is the textbook case for it. Short-form dissolution was *not*
available — that route closes 24 months after incorporation, and 2023–2024 is well past.

If the dissolution went through the 3502 abatement path, the accrued franchise tax is very
likely already cleared. If it was an ordinary SOS Certificate of Dissolution without one,
there may be a residual balance. Check the paperwork for a 3502, or call the FTB nonprofit
line at (916) 845-4171. The EIN itself is on the IRS CP 575 letter.

**A new name, not a revival (Silas, 2026-08-19):** *"When we restart, it will be a new
name and new nonprofit. Kind robots is the future, save one human was the seed."* Save
One Human's name is retired along with its corporation. Any future entity carries the
Kind Robots identity and is a fresh incorporation — never framed as reviving the seed.

**Triggered by revenue, not by a date (Silas, 2026-08-19):** *"We don't need to think
about 501.3 or whatever status until we have so much more under our belt and are
legitimately taking in money as an entity from users."* The January 1 target is
withdrawn. `m6` is weighted 5, and its tasks now depend on `t-013` — the first real
dollar — so the entity track cannot become actionable before the platform is actually
earning. `t-018` is **closed**, with its findings recorded, rather than parked at
`needs-human`, because `audit_human_gates.py` filters purely on `status == "needs-human"`
and would otherwise resurface it in every session sweep forever.

**What this settles by default:** the near-term shape is Path C1 — the platform operates
for-profit, and the mission share is donated directly to the Against Malaria Foundation.
`t-003` stays open only to confirm that formally with a CPA.

## The decision that gates everything else

**Which entity receives the money?** Three shapes, with real consequences:

**A. For-profit Kind Robots, donating a share.**
Payments land in Silas's business (sole proprietorship or an LLC). The mission share is
a documented charitable contribution to the Against Malaria Foundation. Creator payouts
are ordinary 1099-NEC contractor payments.
*Simplest. Fastest. No nonprofit required.* User payments are not tax-deductible, and
the three-way split is a promise the company keeps rather than a legal restriction.

**B. Nonprofit receives everything.**
User donations become tax-deductible and grant eligibility opens up. But paying a
revenue share to creators out of a 501(c)(3) raises private-benefit questions, and
running a commercial AI platform inside a charity invites UBIT (unrelated business
income tax) analysis. It also puts the whole platform under nonprofit governance —
board, bylaws, public disclosure.
*Highest compliance burden by a wide margin.*

**C. Hybrid — the likely answer.**
For-profit Kind Robots runs the platform, takes payments, and pays creators. The mission
share goes to charity either (c1) **directly to the Against Malaria Foundation**, which
is already a registered charity, or (c2) **through a newly incorporated charity** acting as
the charitable arm (Save One Human itself is dissolved and cannot be revived).

> **Key finding: restarting the nonprofit is not required to make the revenue share
> work** — and the research above makes the case stronger, since there is no dormant
> 501(c)(3) to reactivate cheaply. Path **C1** is now clearly the near-term answer.
> Path **C1** — for-profit platform, mission share donated straight to AMF — is
> the cheapest honest route and needs no entity work at all. Reviving Save One Human
> earns its keep only if Silas specifically wants tax-deductible donations flowing to a
> Kind Robots-controlled charity, wants grant eligibility, or wants the mission to
> outlive him institutionally. Those are good reasons. They are just not *prerequisites*,
> and treating them as prerequisites would stall the revenue work for months.

**Open fact-finding only Silas can do:** whether the dissolution was actually *completed*
or merely begun. If Save One Human has been formally dissolved, "restarting" means a new
incorporation; if the filings were brought current but dissolution never finished,
reinstatement may be the cheaper path. This needs a CA Secretary of State business
search, an FTB entity-status check, and an AG Registry of Charitable Trusts lookup.

---

## Minimizing tax and reporting complexity

Silas's question, 2026-08-19: *"Can I take money and then give it directly to
againstmalaria to be considered tax neutral? Is there a way we can automate that 1/3 so
it is directly paid to our fundraiser to avoid any irs double dipping?"*

**Short answer: not by default, and the default is the bad case.** Taking $100 and
donating $33 does not net to zero. The $100 is gross receipts; the $33 is a separate
charitable contribution whose value depends entirely on entity type:

| Entity | Treatment |
|---|---|
| Sole prop / single-member LLC | **Not** a Schedule C expense. Flows to Schedule A itemized. **Worth nothing if he takes the standard deduction** — taxed on the full amount. |
| Partnership / S-corp | Same shape; passes through to the personal return. |
| C-corp | Deducts directly, but capped at **10% of taxable income**, 5-year carryforward — plus a new **1% floor** for tax years beginning after 2025-12-31. A third of revenue blows past 10% immediately. |

So the fear is well-founded, and the current default (sole prop, standard deduction) is
the worst version of it.

### The fix is structural: keep it out of gross receipts

**A. Make the mission third the *customer's* donation, not ours.** Structure checkout so
the customer's third goes to AMF directly rather than through Kind Robots. It never
becomes revenue, so there's no deduction question at all — gross receipts are two thirds,
out of which the creator third is paid. The customer gets the deduction, which is a
selling point rather than fine print, and "a third of what you pay buys nets" becomes
literally true and independently verifiable.

*Mechanism:* a donation-platform API, **not** Stripe Connect — AMF would have to be an
onboarded Connect account, which is effectively a dead end and should stop being designed
toward. Every.org publishes a free, no-platform-fee donation API with embeddable donate
links, programmatic fundraiser creation, and **partner webhooks** that would reconcile
each donation back to the interaction that produced it. AMF is reachable: **The Against
Malaria Foundation (US) is a real 501(c)(3), EIN 20-3069841**, Kansas City MO, deductible
for US donors.

*The catch:* collecting or soliciting donations on a charity's behalf is a **commercial
co-venture** in many states, with registration requirements. Routing through a platform
that is itself the receiving charity may absorb most of that — but that has to be checked,
not assumed. It's the most likely reason option A turns out more expensive than it looks.

**B. §162 business expense instead of §170 charitable contribution.** A payment to a
charity carrying genuine return benefit commensurate with its value (sponsorship,
advertising, logo placement) is an ordinary business expense with **no percentage
ceiling**. Real distinction, not a loophole — and the code explicitly forbids
reclassifying a pure gift as a business expense to dodge the limits, so it only works
where the business return is actual. Fact-specific; CPA territory.

**C. Baseline, already working:** keep pointing donors out to againstmalaria.com/amibot.
Zero complication, zero reporting, and it's how the existing ~$840 was raised. Whatever
else gets built, this stays.

*Not legal or tax advice — general rules from public sources. A CPA confirms the
structure before anything is built on it.*

## Decisions made (Silas, 2026-08-19)

- **The split is on NET, not gross.** "Profit share should be net. Not gross." Stripe
  fees and the real model/GPU cost of the generation come off the top; the three shares
  are equal slices of what remains. Two consequences fall out: the ledger must capture
  *actual* provider cost rather than an estimate, and a spend whose costs exceed its
  gross needs an explicit zero/negative-margin path rather than a negative creator share.
- **Silas earns creator share on his own assets**, on the same terms as everyone else —
  "but want that to feel honest, transparent, and fair." Because he is also the admin,
  that means two of three shares on his own work, which is defensible but must be
  *visible*. Handled as `t-021`.
- **The entity track is deferred** to 2027 or later. See above.
- **Creator payout model settled:** credit creators in **tokens**, and past a threshold
  they request a cash withdrawal. Silas: *"Since we only create tokens when users pay
  money, and we only credit a portion of tokens paid back to creators, a reasonable
  withdrawal timer should prevent most situations of fraud."* The economics are sound —
  a round trip through your own asset returns only a third, so self-dealing loses money.
  Two refinements in `t-014`: earned tokens are a **liability from the moment they're
  credited**, not when paid; and the withdrawal timer should be **at least as long as the
  card-dispute window** (commonly ~120 days), so a chargeback can't land after the cash is
  already withdrawn.
- **The model has two resources; the code has one.** Free **mana** grants limited access
  at lower queue priority and is never purchased. **Tokens** are the paid resource, and
  creator credit derives from token spends only — so a giveaway structurally cannot become
  withdrawable cash. That guarantee lives in the shape of the data rather than in a rule,
  which is why `t-006` (introducing the split) is a security boundary and not tidiness:
  until it exists, any creator-credit rule written against `User.mana` would credit
  giveaway balance as readily as purchased balance.

## MVP shape

The smallest honest slice that makes the three-way split real, ordered so that every
reversible step lands before any irreversible one:

1. **Split the paid token resource from free mana.** The design assumes two currencies;
   the code has one. Without this, nothing else is computable.
2. **Attribute each chargeable generation to a creator** — record source type, source id,
   and creator user id on the spend.
3. **Write an immutable `RevenueSplit` ledger** — one row per paid spend, in integer
   cents, platform / mission / creator, summing exactly to the amount charged.
4. **Show creators their accrued earnings, read-only.** No payouts yet. This is where the
   public promise stops being vapor.
5. **Then, and only then:** live Stripe, real creator payouts (Connect Express, minimum
   thresholds, tax forms), and the first real mission remittance.

Steps 1–4 are reversible software with no outward-facing risk and no money moving. Step 5
is where the human gates live.

---

## Fundraising & outreach (m5, added 2026-08-19)

Everything above is plumbing — it makes money *split* correctly. None of it makes money
*arrive*. Three initiatives from Silas, each with its own task:

**The butterfly event** (`t-022`). A public, butterfly-themed fundraiser. AMI is a horde
of rainbow butterflies and the money buys nets, so the theme carries the argument rather
than decorating it. The design constraint is the same one that keeps the website simple:
**don't take custody of donations.** Point people at againstmalaria.com/amibot and let
them give directly. Collecting money on another charity's behalf pulls California's
charitable-solicitation registration rules into a small community event; direct-to-AMF
sidesteps the category entirely.

**The Sift** (`t-023`). Silas's strongest idea: the panhandler-with-multiple-bowls bit,
run as AI supporters vs. AI skeptics, with the non-AI side's content made entirely
without AI. What makes the original work is that it's funny, it costs the giver nothing,
and both bowls buy the same sandwich — all three properties have to survive. Both sides
fund malaria nets identically; the vote is expressive, the money is never conditional.
The non-AI side has to be *genuinely good*, argued in hand-made work by someone who means
it — if it's visibly the weaker exhibit the whole thing reads as rigged and deserves to.
The hard mechanical problem is attribution: if donations go directly to AMF we may not be
able to see who gave to which side, so the tally may need two distinct fundraiser links
or self-reporting. That gets resolved in the design, not hand-waved.

**Labelled-AI social content** (`t-024`, `t-025`, `t-026`). Silas shelved this over
anti-AI backlash; the responsible version is buildable, and the guardrails belong in the
architecture rather than in a policy document. AMI posts *as AMI* — a labelled AI
character with a stated purpose, never a synthetic persona presenting as human, and never
a system that could become one by flipping a config value. V1 is **draft-only**: the
pipeline generates and queues, a human approves before anything posts. The daily
dream/digest cycle already produces real generated art and writing every day, which is
far better source material than anything written to be promotional. Platform policy
research (`t-024`) comes first because it determines what the pipeline is allowed to be.

## Non-goals for v1

- Redesigning the mana economy or repricing generation
- Print-on-demand fulfillment (owned by `digital-storefront` m4 / t-040)
- The storefront catalog itself (owned by `digital-storefront`)
- Any public announcement of creator earnings before the mechanism exists
- Crypto, DAF, or any donation vehicle beyond a plain corporate donation

## Relationship to `digital-storefront`

`digital-storefront` owns **what is sold** — catalog, PDFs, POD items, DLC packs, the
giving page. **Kind Economy owns what happens to the money afterward** — the split, the
ledger, payouts, and remittance. The one genuine overlap is
`digital-storefront/t-039` (Stripe E2E, parked at `needs-human` since 2026-08-08); this
project adopts that unblock as m3/t-011 rather than duplicating it, and t-039 should
close by reference once m3 lands.
