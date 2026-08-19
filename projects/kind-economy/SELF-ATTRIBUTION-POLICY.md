# Self-Attribution Policy — Admin and Creator Earnings on One's Own Assets

**Created:** 2026-08-19 · **Task:** kind-economy/t-021 · **Status:** design only — no
RevenueSplit ledger exists yet (t-008 builds it); this policy is prescriptive for that
build, not a live change. Reversible.

**One line:** admin-owned and self-owned assets earn creator share on exactly the same
terms as everyone else's, every such row is visibly tagged rather than folded into
"platform," and the anti-arbitrage math is verified rather than assumed.

---

## The tension, restated

Silas, 2026-08-19: *"I'm kinda feeling like for assets I made, I would be able to earn
creator share percent, but want that to feel honest, transparent, and fair."*

Both halves are correct and they pull against each other:

- **The case for:** he made the assets. The creator share exists to reward exactly
  that authorship. Carving the admin out means the platform's single most prolific
  creator is the only one who works for free, which quietly understates what creator
  earnings look like at scale and treats "made by Silas" as somehow not real creation.
- **The problem:** he is also the site admin. On his own assets he receives the
  platform third *and* the creator third — two of three shares of net — and he is the
  one who sets the rules that produce that outcome. Nothing about that is dishonest,
  but it is invisible by default, and invisible is what turns a fair arrangement into
  one that reads as rigged the first time someone graphs it.

The fix is not to solve the tension by picking a side (excluding admin earnings would
be dishonest about authorship; ignoring the optics would be naive). The fix is to make
the arrangement **boring in public** — ordinary, visible, and explainable in one
sentence a skeptic would accept.

---

## The policy

### 1. No special case in the split math

Admin-owned and self-owned assets earn the creator third on **exactly the same terms**
as anyone else's — same percentage, same triggers, same `ManaAttributionSource`
resolution path already built in `server/utils/manaAttribution.ts` (kind-economy/t-007,
merged today). No multiplier, no bonus, no separate code path, no config flag that
distinguishes "admin's own asset" from "any other creator's asset" at the point money
splits. If t-008's RevenueSplit logic ever needs an `if (isAdmin)` branch to implement
this policy, that is the bug, not a detail — the policy is that no such branch should
exist.

### 2. Every row is tagged, none are silent

`kind-economy/t-007` already added `isSelfAttribution` (creator == spender) to
`ManaTransaction`. This policy extends the same discipline to t-008's RevenueSplit
ledger: **every** RevenueSplit row records the creator's identity, full stop — there is
no "admin earnings" path that skips attribution or gets folded into the platform
share's bucket. An admin-attributed row looks, in the data model, exactly like a
random-creator-attributed row with `creatorUserId` happening to equal the admin's id.
That sameness *is* the transparency mechanism: there is nothing to selectively hide
because nothing is structurally different to hide.

### 3. Public transparency surfaces break it out, not fold it in

Whatever the mission-share dashboard (t-010) or any other public transparency surface
ends up looking like, admin-attributed creator earnings get their **own visible line**
— e.g. "creator earnings (site admin's own assets): $X" — never merged into a generic
"platform" total and never omitted. Folding it in would be the one move that actually
converts an honest arrangement into a hidden one: the two-thirds-to-admin outcome is
fine when it's a labeled, addable number; it is a problem the moment it disappears into
an aggregate. This is a requirement on whatever dashboard t-010 builds, not a
suggestion — record it as a `depends_on`/note link from t-010 to this policy when that
task is scoped.

### 4. The sentence a stranger would accept

The plain-language version, meant to sit next to the dashboard line itself, not buried
in a FAQ:

> *"When Silas's own characters, art, or scenarios are what a paid generation was
> built from, he earns the same one-third creator share any other creator would —
> tracked and shown here the same way, because he made the thing the same way."*

If a version of that sentence needs a qualifier, a footnote, or a "well, actually" to
stay true, the policy is wrong, not the sentence. The draft above passes that test: it
names the amount (one-third, not more), names the mechanism (same terms as anyone),
and names why (he made the thing) without asking the reader to trust anything that
isn't also visible on the dashboard next to it.

---

## The adjacent case: a non-admin creator spending on their own object

Same principle, same answer: **you earn on your own work**, whether you're the site
admin or any other creator generating from a Character, Bot, Facet, etc. you made
yourself. The policy in sections 1–4 applies without an admin/non-admin distinction —
"self-attribution" is one policy, not two.

The abuse question this immediately raises — can a creator round-trip money through
their own asset to mint free creator earnings? — has an answer that already holds
structurally, verified against the current code rather than assumed:

**The invariant, verified 2026-08-19:**
`server/utils/manaSpendResolution.ts` (kind-economy/t-006, merged today) resolves every
generation spend from the `TOKENS` pool first and only falls back to `MANA` when
`TOKENS` alone can't cover the cost — no partial split across both pools for one spend.
`prisma/schema.prisma`'s `ManaResource` enum comment states the design intent
explicitly: *"EARNED is the pool future creator-attribution may ever credit from"* —
i.e. only a `TOKENS`-funded spend is eligible to generate a creator-share credit at
all; a `MANA`-funded (free) spend is not, because free mana carries no revenue to
split in the first place. `User.tokens` only increases via a real Stripe purchase
(kind-economy/t-006's split), never from `MANA`/`CYCLE_REFILL` grants.

So a self-attribution round trip — spend on your own object to earn a creator share on
your own spend — necessarily starts from **paid** money and returns at most one third
of it as `EARNED` tokens. Two-thirds of the original spend leaves the loop entirely
(mission + platform shares), so every round trip is a real, unrecoverable loss to the
person doing it. There is no zero-cost input to arbitrage: free mana literally cannot
fund an attributable spend under the current split, and even a fully-paid round trip
loses money on every cycle. This holds today, not just once t-008 ships the ledger —
t-008 only has to preserve the invariant it inherits, not create it.

**Decision on the adjacent abuse question (per the task's own final instruction):**
given the loss is real, structural, and already enforced by the tokens-first spend
resolution rather than by policy alone, self-attributed spends should be **logged and
visible** (section 2 above already requires this) but not additionally excluded or
capped. Adding a cap or exclusion on top of a mechanism that already makes the
behavior unprofitable would be solving a problem that doesn't exist at the cost of
extra special-casing — exactly what section 1 says this policy should avoid. If usage
data after launch ever shows the invariant doesn't hold in practice (e.g. a future
change lets `MANA` fund an attributable spend), that is a bug in the invariant to fix,
not a reason to add a cap here.

---

## What this unblocks

- **t-008** (RevenueSplit ledger): build against sections 1–2 directly — no
  admin/self branch in the split logic, every row (including admin's own) carries
  `creatorUserId` and an equivalent `isSelfAttribution`-style flag.
- **t-010** (mission-share dashboard, not yet scoped in detail): must break out
  admin-attributed creator earnings as their own labeled line per section 3.
- **Public copy** (wherever the three-way split is explained to users): the section 4
  sentence, or a close variant of it, is the canonical public explanation for this
  case — reuse it rather than drafting a new one under pressure later.

## What this does not decide

This is a design doc, not a live change — there is no RevenueSplit ledger to apply it
to yet. Nothing here moves money, changes a percentage, or touches Stripe. t-008 is
where this policy becomes code, and per this project's standing safety posture, any
row that starts actually crediting real dollars remains subject to the project's own
`gate_human`/outward-facing rules independent of this document.
