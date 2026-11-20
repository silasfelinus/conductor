# Space Couch review feedback

## 2026-11-19 PT · t-041 shared settings (#5368)

- **Decision:** merged reversible app PR [kind_robots#5368](https://github.com/silasfelinus/kind_robots/pull/5368), squash commit `98bec1780a071b1b3fdbc971c2f79e16a57136d1`.
- **Verification:** nine exact-head GitHub Actions workflow groups completed success, including the full seeded Space Couch voyage matrix, Playbook Kit, TypeScript, layout, and all contract shards. No authentic browser viewport/art URL acceptance was claimed.
- **Positive:** replaced the separate title-only preference toggles with the existing Playbook Kit settings sheet; preserved `game-of-captains-voyage-v1` and old preference records; covered legacy migration and reactive text/motion presentation with regression tests.
- **Remaining:** account-backed voyage and live achievement verification, delivered painted ending/species URLs, 390/768/1440 browser QA, and independent editorial/art review. Return t-041 to READY (partial), not DONE.
- **Lesson:** migrate historical preference records once and prefer the current versioned settings system, without introducing a second write path or resetting unrelated saves.

## 2026-11-19 PT · t-041 portable voyage backup (#5378)

- **Decision:** merged reversible Kind Robots PR [#5378](https://github.com/silasfelinus/kind_robots/pull/5378) at `a4de97d2e954c64926781b5c52653eb572b42734`.
- **Verification:** all nine original latest exact-head checks COMPLETED/SUCCESS: TypeScript, Playbook Kit, layout, formatting, schema parity, architecture, seeded gameplay, full Space Couch adversarial voyages and all four contract shards. No browser preview/production deployment was asserted.
- **Review finding:** initial backup import introduced a second intentional `restoring = true` path. The achievement contract rightly caught the changed number of guarded restores, and we explicitly asserted imported progress cannot award achievements. A second test used the wrong expected union size for two devices; it now pins preservation of all distinct finished voyages.
- **Positive:** current-save format, completed-run IDs and account-bound records preserved. Explicit import confirmation, JSON shape validation, duplicate-safe history merge and rollback on failed storage writes reduce the risk of losing a run.
- **Remaining:** finish the agent-owned art and responsive verification tasks; do not conflate a local backup with authenticated cloud save or claim subjective art approval. t-041 remains READY (partial).
- **Lesson:** test both historical progress import paths and the union of unique records rather than assuming imported history supersedes local progress.
