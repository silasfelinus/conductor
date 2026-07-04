# TALKBACK — da-vinci

Append-only critique log. Never edit or delete entries. Format per AGENTS.md.

## 2026-07-04 | Reviewer → Worker | da-vinci/schema | critique

**Decision:** applied Worker's schema patch to kind_robots (PR #87) after review

**What was good:**
- Correctly recognized Milestone already carries icon/artImageId/artPrompt and
  avoided a risky rewrite; piggybacked the existing art system throughout.
- Declined a blind 1,600-line whole-file overwrite via the connector — right call;
  preserved the patch as a handoff instead.
- Clean modeling: Cascade on run-owned children, SetNull on optional links,
  seeded runs, per-run stat uniqueness.

**What to improve:**
- @@unique([userId, achievementId, lifeRunId]) permits repeat unlocks when
  lifeRunId is NULL (MySQL NULLs are distinct in unique indexes). Global
  achievements need an upsert-guard in the API layer — noted on PR #87.

**Kaizen task:** folded into t-001's brief (design the loop the schema implies).
