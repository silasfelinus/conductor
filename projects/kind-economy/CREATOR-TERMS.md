# Creator Revenue Share — Terms (Draft)

**Created:** 2026-09-11 · **Task:** kind-economy/t-017 · **Status:** draft only — not
published, not legally reviewed, not yet agreed to by any creator. Publication is the
gate; this document is safe, reversible work on its own. **Not legal or tax advice.**

**One line:** when someone spends paid tokens on something you made, Kind Robots splits
that spend three ways — you get a third, in tokens, and you can cash out once your
balance clears a short waiting window.

---

## Why this document exists

The site already tells creators this, on six tutorial channels:

> "When people spend paid tokens on something you made, you earn a share. Paid usage is
> split three ways - Kind Robots, the anti-malaria fundraiser, and you. Build something
> people love, and the swarm pays you back."

That promise needs terms a real person can read and agree to before it becomes real
money. This draft is written for a creator who makes art, not a lawyer — plain language
first, with the underlying mechanism spelled out so nothing is hidden. It follows the
model Silas approved (`DESIGN-BRIEF.md`, `PAYOUT-MECHANISM-DESIGN.md`) and the entity
decision he made 2026-09-11 (Path C1 — for-profit platform, mission share donated
directly to the Against Malaria Foundation).

A handful of specific numbers below are still open — Silas's pricing/product call, one
needs a CPA — and are marked **[OPEN]** rather than guessed at. The rest reflects
decisions already made.

---

## 1. What earns a share

You earn a share when someone spends **paid tokens** — not free mana — generating an
interaction from something you made: a Character, Bot, Scenario, Facet, or artwork.
Free usage (mana grants, signup bonuses, cycle refills) never earns a creator share,
because it never involved real money changing hands. Only a real, paid token spend does.

If the thing that got spent on is your own — including if you're Silas, on his own
assets — you earn the same third everyone else does, on the same terms, no special
case. (See `SELF-ATTRIBUTION-POLICY.md` for the full reasoning; the short version: it
would be dishonest to say authorship earns a share and then quietly exempt the person
who authors the most.)

## 2. How your share is calculated

Every paid spend splits **three equal ways**, on the **net** amount after real costs —
not the sticker price:

1. Stripe's processing fee comes off the top.
2. The actual cost of running the generation (model/GPU cost) comes off next.
3. What's left splits evenly: **one third to Kind Robots, one third donated directly to
   the Against Malaria Foundation, one third to you.**

The split is on net rather than gross so that the numbers are always real — nobody's
share depends on an estimate, and a spend whose costs happen to exceed what was charged
never produces a negative share for you; it produces a zero.

Every split is recorded permanently, one line per paid spend, in cents, so your
earnings can always be reconstructed and never silently adjusted after the fact.

## 3. When and how you're paid

**Credited immediately, withdrawable after a short wait.** The moment someone's paid
spend is attributed to something you made, your share is credited to your account in
tokens — that money is yours from that instant, tracked as something Kind Robots owes
you, not a score that can be revoked.

**Withdrawal timer: [OPEN — recommended 120 days].** Each credit becomes eligible to
withdraw a fixed number of days after it was earned (not after you ask). The
recommended default is **120 days**, matching how long a card-issuing bank gives a
cardholder to dispute a charge — the wait exists so that a stolen-card purchase can be
caught and reversed before the cash has already left the building, not to make you wait
on money that's genuinely yours. Two shapes of this policy are both defensible (a flat
120-day wait that accepts a small residual risk from rarer, longer dispute windows; or
the same 120-day wait paired with a contractual right for Kind Robots to net a future
chargeback against your future earnings if one lands after you've already been paid).
Whichever Silas picks, it will be stated here exactly, in days, with no vague language.

**How you're paid: [OPEN — recommended manual transfer for v1].** At today's volume,
the plan is a person paying you directly (bank transfer, PayPal, or similar) rather than
an automated payment-processor payout — simpler to start, with no separate account
you're required to open elsewhere. This may move to an automated payout system later as
volume grows; if it does, this document will say so before it changes for you.

**Minimum withdrawal amount: [OPEN].** There will be a minimum balance before a
withdrawal is worth requesting, sized so the transfer itself doesn't eat a large chunk
of what you're owed. The exact number depends on live pricing and isn't set yet.

## 4. Tax paperwork

If you're a **US creator** paid **$600 or more in a calendar year**, Kind Robots is
required to collect a **W-9** from you and send you a **1099-NEC** reporting what you
were paid, the same as any business paying a contractor. Below $600 in a year, there's
no federal filing requirement, though Kind Robots may still ask for the same
information up front rather than only after you cross the line.

If you're **outside the US**, a **W-8BEN** takes the place of the W-9, and the tax
treatment differs by country — Kind Robots will tell you what's needed based on where
you are.

**[OPEN — CPA question, not yet settled]:** whether a balance that's been credited to
you but not yet withdrawn counts as taxable income to you the moment it's credited, or
only once you actually cash out. This affects when Kind Robots is required to report
your earnings and may affect how you should think about your own taxes. This document
will be updated with a definite answer before real payouts begin, and you should not
treat silence here as "it doesn't count until withdrawn" — check with your own tax
preparer if this matters to you before that's settled.

*Nothing in this section is tax advice for your personal situation — it describes what
Kind Robots is required to do, not what you should do.*

## 5. If Kind Robots changes the percentages

Any change to the split, the withdrawal timer, or the payout method applies **only
going forward** — to spends that happen after the change, never retroactively to a
share you've already earned. A credit already sitting in your balance keeps the terms
it was earned under.

If a change would make the arrangement meaningfully worse for creators generally (a
smaller share, a longer wait, a stricter threshold), Kind Robots will say so plainly,
in this document, before it takes effect — not bury it in a changelog.

## 6. If Kind Robots shuts down, or your account is closed

A balance you've earned is money you're owed, not a privilege that lapses if the
platform stops running or your account is closed or banned. **[OPEN — Silas's call, not
yet finalized]:** the working assumption is that an unclaimed or unpaid balance stays on
the books as a liability rather than being zeroed out or swept into general revenue —
Kind Robots doesn't get to keep money it owes you just because you haven't asked for it
yet. Whether there's ever a formal process for reaching you, or what happens to a
balance that's genuinely unclaimable after a long period, is still being worked out and
will be stated here in specific terms rather than left implicit.

## 7. The mission share, so you can see the whole picture

The third that doesn't go to you doesn't go to "the company" either — it's the third
that funds the reason this project exists. One third of every paid spend is donated
directly to the **Against Malaria Foundation** (a real, registered 501(c)(3), EIN
20-3069841) — the same fundraiser at <https://againstmalaria.com/amibot> that Kind
Robots has been pointing donors to from the start. You can verify that this is really
happening the same way anyone else can: by checking the fundraiser's own public totals.

## 8. What this document is not

This is not a contract yet. Nothing here has been reviewed by a lawyer or a CPA, no
creator has agreed to it, and no real payout has ever been made under it (real Stripe
processing hasn't been turned on yet — see `digital-storefront/t-039` /
`kind-economy/t-011`). Publishing this as a real, binding agreement — the point where a
creator can actually click "I agree" and mean something by it — is a separate,
outward-facing step that needs Silas's sign-off and, for the **[OPEN]** items above, a
professional's review first.

---

## For Silas — what's left to close the open items

1. **Withdrawal timer shape** — flat 120 days, or 120 days plus a contractual clawback
   right for late chargebacks. Either closes §3.
2. **Payout method** — confirm manual transfer for v1 (recommended) or something else.
   Closes §3.
3. **Minimum withdrawal threshold** — a dollar/token number, once live pricing is
   settled. Closes §3.
4. **Constructive-receipt timing** — needs a CPA: is a credited-but-unwithdrawn balance
   taxable to the creator at credit or at withdrawal? Closes §4.
5. **Unclaimed-balance policy** — confirm "stays a liability indefinitely" as the
   permanent answer, or set a different one (possible escheatment obligations are a CPA
   question too). Closes §6.

Once those five are answered, this document is ready for the "professional reviews"
step the task note calls for — before anything is published or a creator is asked to
agree to it.
