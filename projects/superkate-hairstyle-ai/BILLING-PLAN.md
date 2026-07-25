# Hair Studio — paid gating + free trial plan

Task: superkate-hairstyle-ai/t-011 · Date: 2026-07-25
Status: plan only — no billing, payment, signup, or production access wired by this doc.

Silas's direction (2026-07-25): "this project is low priority, literally just make
choices and run with it." The choices below are concrete defaults, not open questions —
if any of them are wrong, correct this doc directly rather than re-opening a design pass.

## Decisions

1. **Free trial shape:** 3 free Hair Studio transformations per Kind Robots user
   (tracked the same way other free-tier limits are tracked elsewhere in kind_robots —
   a per-user counter, not a time window). After 3, every generation costs mana like
   any other Kontext call already does for the internal Superkate-only phase.

2. **Billing rail: Kind Robots mana, not external payment.** Hair Studio already runs
   under `authAndGate({ engine: 'kontext' })`, which charges mana per call — this is
   the existing MVP mechanism, not something new. Public launch keeps this exact rail
   rather than standing up Stripe/external billing for this feature specifically. No
   new payment infrastructure, no new pricing tiers to build — the site's existing
   mana-cost-per-engine-call model already fits "try it before the scissors" cleanly:
   users buy mana the same way they do for any other generation feature, and Hair
   Studio consumes it the same way.

3. **Stays inside Hair by Superkate — no separate-app spin-off.** The DESIGN-BRIEF's
   own framing is "a new tab for Hair by Superkate"; given this project's low-priority
   status, investing in a standalone app is out of proportion to the actual demand
   signal so far. Revisit only if usage/demand data later argues for it — not a
   day-one bet.

4. **Access control for non-Superkate users: none needed beyond normal Kind Robots
   auth.** Since this isn't spinning into its own product, any logged-in Kind Robots
   user who finds/uses the Hair Studio tab is treated like any other feature user —
   normal auth, normal mana balance, the 3-free-transformations counter above. No
   Superkate-specific allow-list or invite gate.

## What this unblocks

t-012 (public launch readiness review) can proceed once someone actually flips the
switch — this doc is the "what the plan is" input for that call, not the go-ahead
itself. t-012 still requires Silas's explicit approval of the actual public rollout
and any production deploy, per its own gate.

## What this does NOT do

No billing code, no Stripe/mana-charge wiring changes, no signup flow, no production
deploy, no removal of the current Superkate-only access. This is a decision record for
whoever picks up the next implementation task.
