# Sketchy — Token/Request Tier Spec

Generated: 2026-07-21
Task: sketchy/t-004
Depends on: sketchy/t-001 (PRODUCT-SPEC.md §"Free vs. Paid Tiers", the placeholder this doc replaces)
Grounded against: kind_robots `prisma/schema.prisma`, `server/utils/mana.ts`, `manaGate.ts`, `manaCost.ts`,
`comfyGate.ts`, `generationMana.ts`, `karma.ts`, `server/api/stripe/*`.

---

## Why this doc exists

PRODUCT-SPEC.md's tier table was written before anyone had actually read the mana implementation. Two of
its claims don't match the real system:

1. **"Deducted via `withArtMana` or equivalent mana hook"** — `withArtMana` (`server/utils/generationMana.ts:21`)
   is typed for `kind: 'art'` and costed via `estimateArtCostUsd()`, i.e. image-generation jobs. A drawing
   critique is a **vision-input + text-output** Claude call, not an image generation — it belongs with
   `withTextMana` / `kind: 'text'` (same file, line 34), not `withArtMana`.
2. **"Paid tier has higher mana ceiling via the existing Kind Robots subscription model"** — there is no
   tier-based `manaCap` override anywhere in `manaGate.ts`/`mana.ts`. `User.manaCap` is a flat
   `Int @default(500)` per user regardless of `isMember`. This line describes aspirational behavior that
   does not exist yet.

This doc replaces the placeholder table with numbers and a gating mechanism that are actually buildable
against the shipped mana system, and narrows the backend-pitch surface down to what's genuinely missing.

---

## The core problem this spec has to solve

Sketchy needs a **per-tier daily request ceiling** (2/5/20, etc.) that a first-time reader would assume
comes "from mana." It can't, for three separate reasons, all confirmed against the real schema:

- **Guests have no mana balance.** `karma`/`mana` live on `User` (`schema.prisma:1241-1242`). A guest (no
  login) has no `User` row at all, so there is nothing to debit or check. Guest limiting must be enforced
  entirely on Sketchy's own side (see "Guest tier" below) — it was never going to be a mana question.
- **Mana has no daily-reset mechanism today.** `User.lastManaRefill` / `manaCap` / `ManaReason.CYCLE_REFILL`
  exist as schema plumbing (`schema.prisma:1270-1271`, `1841`) but no cron or middleware anywhere in
  `server/` actually calls a refill. A free user's mana balance, once spent, stays spent — there is no
  "resets to N every day" behavior to hook into.
- **Mana has no per-tier ceiling.** Even if refill existed, `manaCap` is flat per-user, not
  `isMember`-aware. "Paid users get a bigger daily allowance" cannot be expressed as "a bigger `manaCap`"
  without a kind_robots change that doesn't exist yet.

**Resolution:** split the two jobs mana is being asked to do, and assign each to the layer that can
actually do it today:

| Job | Mechanism | Why |
|---|---|---|
| "Does this user have enough currency to afford this call at all?" | Real mana debit via `manaGate`/`withTextMana`, same as every other AI action in Kind Robots | This is what mana already does; no change needed |
| "Has this user hit their **tier's daily critique/assignment limit**?" | A count Sketchy computes itself from its own `SketchyCritique.createdAt` / `SketchyAssignment.assignedAt` rows, filtered to the last 24h and compared against a table keyed on tier | Mana has no per-tier daily ceiling and no reset cron; inventing one there is out of scope for an MVP. Counting Sketchy's own rows needs zero kind_robots changes. |

A user can hit either wall first: mana runs out (real currency exhausted — same failure everyone else in
Kind Robots gets), or the daily tier count runs out (Sketchy's own soft cap, resets naturally at the 24h
rolling window). Both show the same friendly copy (see "Remaining usage display"); Sketchy does not need
to tell the user which wall they hit.

---

## Tiers and limits

Unchanged from PRODUCT-SPEC.md's numbers — this doc adds the mechanism, not new numbers, since Silas has
not asked for different limits:

| Tier | Identity | Daily critique requests | Daily assignment generation | Practice Journal | Enforcement |
|---|---|---|---|---|---|
| Guest | no Kind Robots login | 2/day | 3/day | No | Sketchy-side counter keyed to a signed anonymous session cookie (see below) |
| Free | logged-in `User`, `isMember: false` | 5/day | 10/day | Limited (last 10 sessions) | Sketchy-side counter keyed to `krUserId`, real mana debit per call |
| Paid | logged-in `User`, `isMember: true` | 20/day | Unlimited | Full history | Sketchy-side counter keyed to `krUserId` (skipped entirely when unlimited), real mana debit per call |

"Unlimited" assignment generation for paid still spends mana per call — it only skips the daily
count-based ceiling, not the currency check. A paid user with 0 mana still gets a 402, same as anywhere
else in Kind Robots.

### Guest tier mechanism

Guests have no `User.id` to key a counter on. Use a signed, httpOnly anonymous session cookie
(`sketchy_guest_id`, opaque UUID minted on first visit) as the counter key in Sketchy's own app-owned DB.
This is a Sketchy-only concern — it never touches Kind Robots' `User` table, and it's the reason guests
were never going to be a mana question in the first place. Cookie-clearing resets a guest's counter; that
is an accepted MVP limitation (same tradeoff every anonymous-tier product makes), not a security gap to
close now.

---

## Mana cost per action

Concrete costs, using the real gate formula (`manaGate.ts:76-78`):
`cost = Math.max(1, Math.ceil(estCostUsd * MANA_PER_USD))`, where `MANA_PER_USD = 1000`
(`mana.ts:7-9`, peg $0.001/mana).

| Action | Basis | estCostUsd | Mana charged |
|---|---|---|---|
| Critique (Claude Vision call) | docs/ai-critique-apis.md's own estimate: "~$0.005–0.01/critique" | 0.008 (mid-estimate, flat) | 8 mana |
| Assignment generation | Text-only, no image input, materially cheaper than a critique call | 0.001 (floor) | 1 mana |

Use a **flat per-call estimate**, not real-time token counting, for both. `estimateTextCostUsd()`
(`manaCost.ts`) estimates pure text calls; it has no vision-input term, and building one is unnecessary
complexity for a single-image, bounded-size critique call whose cost band is already known from the API
survey. If actual Claude billing drifts meaningfully from the $0.005–0.01 band docs/ai-critique-apis.md
found, revisit the flat estimate then — don't pre-optimize token-exact costing at MVP.

These are the numbers Sketchy's backend passes as `estCostUsd` when it calls the (not-yet-existing, see
below) mana-charge endpoint — they are not a kind_robots schema change, just Sketchy-side constants.

---

## What Sketchy calls, concretely

Sketchy is a separate app with its own DB (per PRODUCT-SPEC.md's "App-Owned Schema") that consumes Kind
Robots over HTTP — it is not a page inside the kind_robots Nuxt app, so it cannot call `withTextMana`
in-process the way `server/api/art/enqueue.post.ts:163-170` calls `authAndGate` in-process. Every existing
mana-gated route in kind_robots gates its **own** action; there is no existing endpoint that lets a
trusted external caller charge an arbitrary user's mana for an action performed *outside* kind_robots.
That gap — not the mana math above — is the actual missing piece, and it's narrower than PRODUCT-SPEC.md's
original 3-item backend-pitch table:

1. ~~"Mana allowance reset (daily free tier)"~~ — **removed**. Per the "core problem" section above, the
   daily ceiling is a Sketchy-side count, not a mana refill. No kind_robots cron is needed for tiering to
   work.
2. ~~"Higher mana ceiling for paid Sketchy tier"~~ — **removed**. Same reason: the paid tier's extra
   headroom is Sketchy's own daily-count ceiling (20 vs. 5, unlimited assignments), not a bigger
   `manaCap`.
3. **Kept, narrowed to one concrete ask:** a small authenticated endpoint, callable by a trusted Sketchy
   machine credential (same `requireMachineUser` pattern `comfyGate.ts:47`'s `authAndGate` already uses for
   Comfy image routes), that takes `{ krUserId, kind: 'text', estCostUsd, refId }`, runs the existing
   `manaGate` → perform-nothing (Sketchy already did the actual critique/generation itself) →
   `gate.commit(refId, estCostUsd)` sequence server-side, and returns the new balance or a 402. This reuses
   `manaGate`/`applyMana` byte-for-byte — no new mana logic, no new `ManaReason` needed beyond one addition
   (`GENERATION_TEXT` already exists and fits both actions; no new enum value required after all, since
   critique/assignment generation are both text-classed AI generations from mana's point of view).

This is filed as a pitch against kind-robots (see below) rather than implemented directly here, per
PRODUCT-SPEC.md's own rule: "Any shared-backend changes are flagged as pitches, not direct edits."

---

## Remaining usage display

Unchanged from PRODUCT-SPEC.md: `"3 critiques remaining today."` — computed as
`tierDailyLimit - countSince(now - 24h)`, floored at 0, never showing raw mana. If the wall hit is actually
insufficient mana rather than the daily count, the copy is the same sentence at 0 remaining — Sketchy does
not need a separate "you're out of mana" message; both walls are already indistinguishable to the user by
design (PRODUCT-SPEC.md: "abstract it to 'critique requests'").

---

## Acceptance criteria

- [ ] Guest/Free/Paid daily ceilings enforced via Sketchy's own per-tier counters (guest: signed cookie;
      Free/Paid: `krUserId`), not a kind_robots mana-cap change.
- [ ] Every critique and assignment-generation call still attempts a real mana charge via the pitched
      charge endpoint once it exists; a 402 from that endpoint blocks the action regardless of the
      Sketchy-side daily count.
- [ ] Flat mana costs: 8 mana/critique, 1 mana/assignment generation, both driven by Sketchy-side constants
      matching docs/ai-critique-apis.md's cost survey — not real-time token metering.
- [ ] "Unlimited" (paid-tier assignment generation) skips the daily-count check but never skips the mana
      charge.
- [ ] UI never shows raw mana numbers — only the "N remaining today" framing already specified in
      PRODUCT-SPEC.md.

---

## Feeds into

- kind-robots pitch (new, filed alongside this task): the trusted machine-credential mana-charge endpoint
  described above. Blocks real implementation of Sketchy's critique/assignment mana debit until approved.
- sketchy/t-007 (front-end polish): the "N remaining today" indicator design lives there once this spec is
  approved.
