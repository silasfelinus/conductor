# TALKBACK.md — digital-storefront

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-07-05 | Reviewer → Worker | digital-storefront/(roadmap rewrite) | pattern

**Decision:** merged (conductor PR #204 — reactivation, kind flipped content → software)

**What was good:**
- The v1 catalog and every task in the rewritten roadmap trace directly to Silas's
  explicit in-session direction, not agent invention; CONTROL.md, roadmap.yaml, and
  product-types.yaml all tell the same story.
- Every outward step (live Stripe, POD account creation, publishing, spend) stayed
  correctly hard-gated at needs-human even though the kind flipped to software.
- The product-types.yaml addition — normally "ONLY Silas adds" — was flagged
  explicitly for Reviewer attention with a clear escape hatch (revert the hunk) if
  it read as too forward. Good instinct: default to flagging boundary-adjacent
  edits rather than assuming they're fine.

**What to improve:**
- Nothing structural. Minor: the STORE-AUDIT task (t-008) already prose-mentions
  the Stripe lazy-init issue but doesn't make it an actionable task on its own —
  I split that into a standalone kaizen task (kind-robots t-009) rather than
  leaving it buried in an audit note for a future agent to rediscover.

**Kaizen task:** kind-robots/t-009 — lazy-init the Stripe client in checkout/subscribe
routes so a missing STRIPE_SECRET_KEY degrades to a 500 instead of crashing server
boot. (Sourced from the kaizen suggestion in the companion kind_robots PR #91.)

**Pattern note:**
- Recording Silas's verbatim direction into normally-restricted files
  (product-types.yaml) with an explicit inline comment crediting the source and a
  named reviewer escape hatch is a good pattern — keep doing this instead of
  silently expanding restricted files.

## 2026-07-15 | Reviewer → Reviewer | digital-storefront/t-015 | pattern

**Decision:** done (self-claimed and closed in one session — no cross-repo code, pure research output).

**What was good:**
- ai-art-academy (this hour's nominal top-priority project) and digital-storefront's
  own t-012/t-013 (Stripe wiring) were both re-confirmed blocked this session (museum
  egress 403, api.stripe.com 403 — same sandbox proxy denials documented in prior
  TALKBACK entries). Rather than idling or re-flagging an already-documented blocker,
  rotated down the priority list to t-015, a task with no external API dependency.
- Backed the Printful-vs-Printify recommendation with live 2026 web research (pricing,
  API/webhook docs) rather than relying on the general shortlist in research/stores.md,
  and cited sources inline in the new doc.
- Picked a concrete first SKU (sticker) with an explicit reason (lowest cost/risk,
  no size/color variant matrix, fastest turnaround) instead of leaving "whatever item
  is easiest" unresolved for the next agent to re-litigate.
- Folded the concrete provider/item pick directly into the now-unblocked t-016's note
  so its future implementer doesn't have to re-read pod-provider.md to know which
  vendor/product family to design against.

**Kaizen task:** digital-storefront/t-019 — periodically re-verify the api.stripe.com
and museum-site sandbox-egress blockers (t-012/t-013/ai-art-academy) since sandbox
network policy could change between sessions; a stale "confirmed blocked" note can
otherwise strand real ready work indefinitely without anyone rechecking.

**Pattern note:**
- Second cycle in a row (see PR #544's TALKBACK entry) where the "rotate to the next
  project when the top-priority one is blocked" instruction correctly avoided an idle
  cycle. Worth keeping as standing practice rather than special-casing it each time.

## 2026-07-15 | Reviewer → Reviewer | digital-storefront/t-019, t-016 | pattern

**Decision:** both done (self-claimed and closed in one session; t-016 followed by two
new kaizen `ready` tasks, t-020/t-021).

**What was good:**
- t-019 was a genuine recheck, not a rubber-stamp: re-curled api.stripe.com,
  www.metmuseum.org, and upload.wikimedia.org directly and checked
  `/__agentproxy/status` fresh rather than trusting the prior session's TALKBACK note.
  Stamped the recheck timestamp onto every task that cites the same blocker
  (digital-storefront t-011/t-012/t-013, ai-art-academy t-004/t-008/t-013) so the next
  few burst cycles can skip re-curling and just check whether the timestamp is recent —
  directly closes the loop t-019 itself was filed to start.
- ai-art-academy (top of priority.yaml) was checked FIRST this cycle and confirmed
  still blocked on two separate fronts (KR_API_TOKEN absent for t-004/t-009, museum
  egress 403 for t-008/t-013) before rotating down to digital-storefront/t-016 — same
  discipline as the prior two cycles' TALKBACK pattern notes.
- t-016's design doc (docs/gallery-to-swag-pipeline.md) surfaced a real gap instead of
  hand-waving past it: the schema has no way to enforce CONTROL.md's
  commercial-generation licensing rule on gallery art before it's printed and sold.
  Rather than silently assuming "print whatever's in the gallery," the doc proposes a
  concrete field (`Resource.commercialSafe`) and a default-deny policy, and separates
  out the one launch item (KR-logo sticker) that doesn't need the schema change at all
  so it isn't blocked waiting on a pitch.

**Kaizen tasks:** digital-storefront/t-020 (pitch: `Resource.commercialSafe` licensing
field) and t-021 (pitch: `ArtImage.storefrontFeatured` curation field) — both concrete,
small, reversible follow-ups the design doc surfaced. Filed two instead of the usual
one since both are genuine, independently-landable schema-pitch gaps rather than one
being a weaker substitute for the other; flagging this deviation from the "exactly one"
convention explicitly rather than silently doing it.

**Pattern note:**
- Third cycle in a row where checking the top-priority project's blockers first (and
  recording *why*, with a timestamp) before rotating down the list kept the cycle from
  idling or re-doing verification work a prior session already did. t-019 was written
  specifically to stop this from being re-litigated every single cycle — worth checking
  in a future cycle whether the RECHECKED-note pattern actually cut down on repeated
  egress checks, or whether it needs a more structured "last verified" field instead of
  free-text notes.

## 2026-07-15 | Reviewer → Silas | digital-storefront/t-020 | closed (hourly cycle, pitch)

**Decision:** parked at `needs-human` (proposal-kind resolution — pitch written, awaiting Silas)

**Detail:** Priority-order projects ahead of digital-storefront (challenge-center,
ai-art-academy, humboldt-scoop, humboldt-scoop-cms) had no unblocked ready work this
cycle: challenge-center is fully `done`, ai-art-academy's four ready tasks are all
still blocked on the same reconfirmed KR_API_TOKEN/museum-egress limits, and the
Humboldt projects have nothing `ready` (humboldt-scoop-cms/t-006 is `needs-human`).
digital-storefront's own t-011/t-012/t-013 need Stripe test-mode (same egress block)
and t-018 is note-level blocked on coloring-book t-006/t-007 not having landed yet —
but t-020 and t-021 are both `kind_robots pitch` tasks per BOUNDARY.md (schema
changes are never a direct edit from this project) with no external dependency, so
picked t-020.

- Claimed via `claim_task.py` (digital-storefront/t-020).
- Read `docs/gallery-to-swag-pipeline.md` §4/§6 (the kaizen source) and the live
  kind_robots `Resource`/`ArtImage` Prisma models directly rather than assuming the
  note's field-name suggestion was final — confirmed `ArtImage.checkpointResourceId`
  is the actual join point and that `Resource` currently has no license-related
  column at all.
- Wrote `pitches/2026-07-15-resource-commercial-safe-field.md` per the pitch
  template: additive `Resource.commercialSafe` (or `licenseClass` enum) column,
  defaulted unsafe/unknown, seeded true for FLUX.1-schnell/OpenAI/approved-API rows.
- Verified: `python3 -c "import yaml; yaml.safe_load(...)"` on the edited
  roadmap.yaml, and `scripts/audit_roadmaps.py` (0 errors, same warning/info counts
  as baseline).
- Set t-020 to `needs-human` with a FOR SILAS note (soft gate, proposal-kind
  resolution per AGENTS.md — not a stuck-agent escalation).

**What was good:**
- Didn't just restate the task note's suggested field name/type as the final
  answer — cross-checked the real `Resource` model shape (`resourceType`,
  `supportedServer`, `civitaiUrl`/`huggingUrl`/`localPath`) before recommending
  the enum-vs-boolean tradeoff in the pitch.

**Kaizen task:** none filed this cycle — t-021 (the companion
`StorefrontFeaturedArt`/`storefrontFeatured` pitch from the same kaizen source)
remains `ready` and is the natural next pick for a future cycle; no new systemic
gap surfaced by this one.

## 2026-07-15 | Reviewer → Silas | digital-storefront/t-021 | closed (hourly cycle, pitch)

**Decision:** parked at `needs-human` (proposal-kind resolution — pitch written, awaiting Silas)

**Detail:** Same cycle as t-020 (see entry above) — picked up the sibling pitch task
right after t-020's PR merged, per the "may complete several tasks in one run" rule
(one claim in flight at a time, each finished before claiming the next).

- Claimed via `claim_task.py` (digital-storefront/t-021).
- Confirmed directly against the live kind_robots `ArtImage` Prisma model that it has
  no featured/curation flag today, matching the doc's claim.
- Wrote `pitches/2026-07-15-storefront-featured-art.md` per the pitch template:
  additive `ArtImage.storefrontFeatured` boolean, or a `StorefrontFeaturedArt` join
  table if sort-order curation is wanted from day one.
- Verified: `python3 -c "import yaml; yaml.safe_load(...)"` on the edited
  roadmap.yaml, and `scripts/audit_roadmaps.py` (0 errors, same warning/info counts
  as baseline).
- Set t-021 to `needs-human` with a FOR SILAS note (soft gate, proposal-kind
  resolution — not a stuck-agent escalation).

**What was good:**
- Both digital-storefront pitches from t-016's kaizen source (t-020, t-021) are now
  written and parked in the same cycle, giving Silas one batch to review instead of
  two separate future interruptions.

**Kaizen task:** none filed this cycle — this pass was itself closing out the last
two open items from a prior kaizen; no new systemic gap surfaced.

## 2026-07-17 | Reviewer → Silas | digital-storefront/t-013 | pattern (autonomous hourly cycle)

**Decision:** merged kind_robots PR #361 (squash 98190504) and conductor PR #700
(bookkeeping, squash ae3e266). t-013 closed done; kaizen t-024 filed.

**Detail:**
- Prior burst-mode session had already implemented the code (kind_robots#361) and opened
  the conductor bookkeeping PR (#700) setting `status: review`, but left both PRs open —
  this cycle's job was verification + merge + close, not implementation.
- Delegated the payment-code diff review to a subagent (kind_robots#361 touches
  `server/api/stripe/webhook.post.ts`, a new `cancel-subscription.post.ts`, and a
  `User.stripeSubscriptionId` migration) to keep ~115K chars of diff out of the main
  session context. Verified: migration is a single nullable `ADD COLUMN` (no drops), no
  hardcoded/live Stripe keys (both new/changed routes read `process.env.STRIPE_SECRET_KEY`,
  same as the pre-existing webhook), the new cancel-subscription endpoint derives the user
  from `requireApiUser` and takes no client-supplied id (so user A cannot cancel user B's
  subscription), and the webhook's `stripe.webhooks.constructEvent` signature check is
  untouched — the new subscription branches sit after it, not around it. All 3 kind_robots
  CI checks (TypeScript, Contract verifiers, GitGuardian) and all conductor CI checks green.
- Also found (not from this task, closed separately): conductor PR #698 was a duplicate
  `coloring-book/t-022` re-arm — PR #699 had already merged the identical change moments
  earlier (rotation collision). Closed #698 rather than force a conflicting merge; no work
  was lost since #699's version is on `main`.

**Failure category:** n/a (clean merge; subagent review caught one pre-existing,
not-introduced-by-this-PR gap, filed as kaizen rather than blocking the merge).

**Kaizen task:** t-024 — `subscribe.post.ts` still accepts a client-supplied `userId`
with no auth check (pre-existing, not worsened by #361; the new cancel-subscription
endpoint was built correctly via `requireApiUser` and should be the model for the fix).
