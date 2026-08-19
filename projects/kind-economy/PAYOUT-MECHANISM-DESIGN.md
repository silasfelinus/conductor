# Creator Payout Mechanism — Design (kind-economy/t-014)

**Status:** design complete for what an agent can settle; four items below need Silas's
decision (and one needs a CPA) before any code is written. Not legal or tax advice.

**Model, as Silas specified it (2026-08-19, verbatim):** *"we credit the creator with
more tokens, which are the paid resource used to generate interactions. Then when they
reach a threshold, they can request a withdrawal and we pay. Since we only create
tokens when users pay money, and we only credit a portion of tokens paid back to
creators, a reasonable withdrawal timer should prevent most situations of fraud."*

The economic reasoning holds: credit in tokens, pay on request past a threshold, and
the fact that a fraud round-trip returns only a third of the money makes self-dealing
unprofitable on its own. This document works out the three things the task note asked
for and flags what's left.

---

## 1. Earned mana is a liability the moment it's credited

`User.earnedTokens` (added by t-006, currently populated by nothing — t-007/t-008 do
the crediting) is not a score. From the instant a `RevenueSplit.creatorShareCents` row
credits it, that balance is **money owed to the creator**, whether or not they ever
request a withdrawal. Three consequences:

- **Never mint into it.** Achievements, referral bonuses, admin adjustments, and any
  future "give users free stuff" mechanism must credit `User.mana` (or a new
  non-withdrawable bucket), never `earnedTokens`. The invariant that makes the whole
  payout design safe is that `earnedTokens` has exactly one source: a real paid spend on
  someone else's object, recorded in `RevenueSplit`. If that invariant ever has a second
  writer, the fraud-resistance argument above stops holding — a free giveaway would
  become withdrawable cash.
- **Sum of outstanding `earnedTokens` across all users is a real balance-sheet
  liability**, not a vanity metric. It belongs in whatever bookkeeping view eventually
  answers "what does Kind Robots currently owe," the same way `kind-economy/t-010`'s
  mission-accrual dashboard answers the equivalent question for the mission share.
  Worth a follow-up task once payouts exist: an admin view of total outstanding
  creator liability, not just per-creator earnings (t-009 already covers the
  per-creator view).
- **A withdrawal is a liability discharge, not an expense.** When paid, decrement
  `earnedTokens` by exactly the withdrawn amount and write an immutable record (see
  §3) — never delete or edit history, matching `RevenueSplit`'s and
  `ManaTransaction`'s existing correction-only-via-new-row convention.

## 2. The withdrawal timer, sized against the real threat

Silas's instinct — a timer prevents most fraud — is right, and the number that makes it
right is the card-network dispute window, not an arbitrary "feels safe" duration.

**The attack the timer defends against:** buy tokens with a stolen card → spend on a
confederate's object → confederate withdraws → the real cardholder disputes the charge
weeks later → the cash is already gone and Kind Robots eats the chargeback with nothing
to claw back.

**The window that closes it, per card-network rules (verified against current sources,
2026-08-19):**

- Standard dispute window: **120 days** from the transaction date (or expected-delivery
  date for physical goods, whichever is later) — this is the baseline across Visa,
  Mastercard, and Amex.
- **Reason-code extension: up to 540 days** for certain reason codes, most notably
  "services not rendered" / "credit not processed"-type claims. Kind Robots sells a
  *service* (generation access), not a physical good, so this is the realistic upper
  bound to design against, not the 120-day headline figure.
- Amex-specific: cardholders get 120 days; merchants/acquirers get 20 days to respond
  once a dispute opens (irrelevant to the payout timer itself, relevant to whoever
  handles dispute responses operationally).

**Recommendation:** set the withdrawal-eligibility timer per-credit (i.e., a given
`earnedTokens` credit becomes withdrawable N days after the `RevenueSplit` row that
created it, not N days after the withdrawal request) at **120 days as the default**,
with the understanding that this leaves exposure to the long-tail 540-day reason codes.
Two honest options, not a recommendation to pick between — this is Silas's call:

- **(a) 120 days, accept residual long-tail risk.** Matches the standard window,
  keeps creators from waiting over a year for money they're owed, and treats the
  540-day tail as a cost of doing business (same as any marketplace with a payout
  timer shorter than the absolute maximum dispute window — this is the industry-normal
  tradeoff, not a naive one).
- **(b) 120 days plus a capped clawback right**, not a longer hold: pay on the normal
  timer, but reserve the contractual right (in creator terms of service) to net a
  future chargeback against the creator's *future* earnings if one lands after payout.
  This keeps the timer short (good for creator trust) while giving Kind Robots a
  recovery path for the rare long-tail case, at the cost of needing actual ToS language
  and a "negative balance" carry mechanism.

Either is defensible. A flat 540-day hold is very unlikely to be worth it — it would
make the payout program nearly a year and a half of latency for a fraud pattern that
120 days already mostly closes.

## 3. What the code needs (not built by this task — this is the design)

The model requires two resources that didn't exist until t-006 (`tokens` for spend,
`earnedTokens` for creator credit) and a ledger that didn't exist until t-008
(`RevenueSplit`, immutable, `creatorUserId`/`creatorShareCents` per paid spend). Both
now exist. What's still missing, for a future implementation task to build once §4's
open questions are answered:

- A `PayoutRequest` (or similarly-named) append-only model: `id`, `createdAt`,
  `creatorUserId`, `amountCents`, `status` (`requested` → `approved`/`denied` →
  `paid`/`failed`), `eligibleCreditIds` or a cutoff timestamp (so a request only draws
  on `RevenueSplit` rows already past the withdrawal timer), and a `reversedById`-style
  correction pointer for consistency with the rest of this project's ledger tables.
  Never edit a row in place once `paid`.
- A read path that computes "withdrawable now" = sum of a creator's
  `RevenueSplit.creatorShareCents` rows (reversal-excluded, same helper as t-009/t-010)
  whose `createdAt` is older than the timer, minus anything already requested/paid.
  This is a pure function, unit-testable the same way `creatorEarnings.ts` and
  `missionAccrual.ts` are.
- A request endpoint (creator-facing, their own balance only, same shape as
  `creator-earnings.get.ts`) and an admin approval/fulfillment surface. No code should
  auto-fulfill a payout without a human step until Silas explicitly gates that open
  (matches this project's standing rule: "no payout of any kind without Silas's
  explicit per-action approval").
- The actual money-movement integration is the one piece this document does not
  design, because it depends on §4 below.

## 4. Open questions — Silas's call, one needs a CPA

None of these break the model above; they're inputs the model needs before it can be
built:

1. **How the withdrawal is actually paid.** No payout mechanism exists in the repo
   today — zero references to Stripe Connect, `transfer_data`, or `application_fee`.
   Two realistic paths: **Stripe Connect Express** (creators onboard a lightweight
   Stripe account, Kind Robots pushes transfers — standard for marketplace payouts,
   but requires each creator to complete Stripe's own KYC) vs. **manual transfer**
   (Silas or an admin pays out by hand — PayPal, Venmo, a check — at low volume, with
   no Stripe Connect integration to build at all). At current volume (~$0 real revenue
   to date per the design brief), manual is almost certainly the right v1: it needs no
   new Stripe integration, no creator KYC flow, and can be replaced by Connect later
   once volume justifies the engineering cost. Recommend starting manual; Silas
   confirms.
2. **Minimum withdrawal threshold.** High enough that a payout is worth its own
   transfer/processing cost (manual payouts have real per-transaction friction; Stripe
   Connect has per-transfer fees). No specific number recommended here — depends on
   the token peg's real USD value at whatever mana/token pricing is live when this
   ships, which is Silas's pricing call, not an agent's.
3. **Identity/tax collection.** In the US, a creator paid **$600 or more in a calendar
   year** requires a W-9 and a 1099-NEC from Kind Robots (or whatever entity pays them —
   see the kind-economy DESIGN-BRIEF.md's still-open entity question). Below $600, no
   federal filing requirement, but Kind Robots should still decide whether to collect
   identity information at signup-for-payout regardless, versus only after crossing the
   threshold. Non-US creators need a W-8BEN instead, and foreign-payment tax withholding
   rules differ by country — this is real compliance surface, not a formality, and
   belongs with the same CPA who resolves the entity question in
   `projects/kind-economy/DESIGN-BRIEF.md`.
4. **What happens to earned balances from creators who never onboard** (never provide
   payout identity/tax info, or the account is later deleted/banned). Recommend: the
   liability stays on the books indefinitely rather than being silently zeroed or
   swept into platform revenue — an unclaimed creator balance is not Kind Robots'
   money merely because nobody's claimed it yet. Whether there's ever an escheatment-
   style policy (many US states require unclaimed property to eventually revert to the
   state, not the holder) is itself a question for the CPA/entity conversation, not
   something to decide informally here.
5. **CPA question, not an agent's to answer:** does credited-but-unwithdrawn
   `earnedTokens` become taxable income to the creator at the moment of credit, or only
   at redemption? "Constructive receipt" doctrine could make it the former even though
   the creator hasn't touched a bank account — if so, Kind Robots may owe 1099
   reporting the moment a balance crosses $600 in a year *regardless of withdrawal
   status*, which changes both the reporting cadence and probably the UI copy around
   "earned but not yet withdrawn." Flagging explicitly per this project's standing
   rule that professional-review items get named plainly rather than guessed at.

## Bottom line

The model is sound and (as of t-006/t-007/t-008) the data shape now supports it:
tokens are the only source of `earnedTokens` credit, `RevenueSplit` is the immutable
ledger to draw a payout from, and a time-gated withdrawal closes most of the
chargeback-fraud surface. What remains before implementation is (a) Silas picking a
payment path (recommend: manual v1) and a withdrawal-timer policy
(recommend: 120 days, accept the long-tail risk per §2), and (b) the CPA settling the
tax-timing and entity questions in §4.3–4.5. Parking this task at `needs-human` for
those decisions rather than guessing at them.
