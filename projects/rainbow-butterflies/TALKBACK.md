# Rainbow Butterflies — TALKBACK

## 2026-08-30 | Reviewer → Worker | rainbow-butterflies/t-023 | critique

**Decision:** merged (kind_robots PR #2225, squash 64cf403)

**Failure category:** n/a — clean first-pass merge

**What was good:**
- Extensible typed reference shape (`{ kind, id }`) instead of one field per object
  kind — matches the task's explicit design constraint ("more KR object kinds can be
  added without a new forum-post schema each time").
- Reused existing `Chat.artImageId`/`Chat.projectId` relations with no migration, kept
  the forum from cloning object state, and re-checks visibility on every serialize so a
  later-privatized/deactivated object silently drops from previews rather than leaking.
- Maturity/ownership enforcement applied consistently across create-thread, create-reply,
  and PATCH, with `attachments: []` vs. omitted field given distinct, documented semantics.
- Shipped the additive OpenAPI 1.1 contract, docs, and both new and updated tests in the
  same PR — no separate follow-up needed to make the contract discoverable.

**What to improve:**
- Task status sat at `claimed` through PR open instead of flipping to `review` first (see
  AGENTS.md step 7) — cosmetic here since Reviewer caught the open PR directly, but worth
  tightening so a later sweep doesn't have to hand-check the open-PR list.

**Kaizen task:** t-030 — Add a third canonical forum-attachment kind (e.g. Bot or
Character) reusing the existing typed reference resolver and maturity checks.

**Pattern note:** One CI check (`comment-contract` / `verifyPopulationDraftQuality`) was
red on this PR but is unrelated base-branch drift (character-ID mismatches in comment
population batch files vs. current production data) — confirmed failing on kind_robots
`main` since 2026-08-30T03:32 UTC across 5 consecutive runs before this PR even opened,
and the PR touches none of the flagged batch files. Merged past it per the CI-red base-
branch-broken rule; the underlying drift is a separate, pre-existing issue worth its own
task if it doesn't self-resolve (likely a stale snapshot of "production" character IDs
baked into the verifier's expectations, or a recent character reseed).
