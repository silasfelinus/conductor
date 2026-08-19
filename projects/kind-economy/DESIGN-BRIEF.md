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

1. **Paid and free tokens are indistinguishable.** `User.mana` is one `Int`.
   `maybeRefill()` tops every user up to `manaCap` daily (`CYCLE_REFILL`) and grants a
   250-mana `SIGNUP_BONUS`. Purchased mana lands in the same balance. At spend time
   (`manaGate` → `chargeForGeneration`) nothing knows whether the mana being burned was
   bought or given away. **"Paid usage is split three ways" is not currently computable
   from the data we store.** This is the single biggest blocker and everything else
   depends on fixing it.

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

### Legal / entity side

From the `SaveOneHuman` repo's own checklist and history:

- California nonprofit corporation — **name reserved, articles filed, EIN obtained** ✅
- Board of directors — **never appointed** ❌
- Bylaws + conflict-of-interest policy — **never drafted** ❌
- Initial board actions — **never taken** ❌
- CT-1 initial registration with the CA AG's Registry of Charitable Trusts — **never
  filed** ❌
- Revenue, ever: **$0**
- Current posture: mid-unwind, overdue zero-dollar filings being submitted
- Website: static GitHub Pages at `saveonehuman.org`; `index.html` only —
  `about`, `donate`, `values`, `links`, `thanks`, `stretch` are 1-byte placeholders

Silas's stated target is to restart the entity **around January 1**, to line the entity
up with a clean fiscal/tax year and avoid extra part-year filings while infrastructure
is still being built.

---

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
is already a registered charity, or (c2) **through a revived Save One Human** acting as
the charitable arm.

> **Key finding: restarting the nonprofit is not required to make the revenue share
> work.** Path **C1** — for-profit platform, mission share donated straight to AMF — is
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

Silas's explicit ask: send malaria money "directly to the fundraiser and minimize
reporting and tax complications." Ranked by how little accounting each creates:

1. **Keep sending donors out to `againstmalaria.com/amibot`.** Those dollars never touch
   our books, never become revenue, and never need to be reported by us. This already
   works — it raised the $840 — and it should stay, regardless of what else gets built.
2. **Periodic corporate donation of the accrued mission share.** Kind Robots recognizes
   100% of paid-token revenue, then donates the mission share to AMF on a schedule
   (monthly or quarterly). One expense line, one receipt, fully deductible. Requires an
   accurate accrual ledger, which is exactly what m2 builds.
3. **Stripe Connect transfers to AMF.** Technically imaginable, practically unavailable —
   AMF would have to be an onboarded Connect account. Worth ruling out explicitly and
   early so nobody designs toward it.

The mission share is a **corporate donation of platform revenue**, not a pass-through of
user donations. Keeping those two flows separate — donation traffic goes out to AMF's own
page, platform revenue is ours and then partly donated — is what keeps the reporting
simple and the donor-intent story clean.

---

## MVP shape

The smallest honest slice that makes the three-way split real, ordered so that every
reversible step lands before any irreversible one:

1. **Make paid mana distinguishable from granted mana.** Without this, nothing else is
   computable.
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

## Non-goals for v1

- Redesigning the mana economy or repricing generation
- Print-on-demand fulfillment (owned by `digital-storefront` m4 / t-040)
- The storefront catalog itself (owned by `digital-storefront`)
- Marketing, launch, or any public announcement of creator earnings
- Crypto, DAF, or any donation vehicle beyond a plain corporate donation

## Relationship to `digital-storefront`

`digital-storefront` owns **what is sold** — catalog, PDFs, POD items, DLC packs, the
giving page. **Kind Economy owns what happens to the money afterward** — the split, the
ledger, payouts, and remittance. The one genuine overlap is
`digital-storefront/t-039` (Stripe E2E, parked at `needs-human` since 2026-08-08); this
project adopts that unblock as m3/t-011 rather than duplicating it, and t-039 should
close by reference once m3 lands.
