# Zuzu Gamebook: decisions after the build roadmap

This is the human playtest and release checklist that comes after the build roadmap. It is **not** an active Conductor roadmap task and **not** a blocker to the `playtest` lifecycle. It preserves former roadmap task `t-017`, moved here on 2026-11-17 PT at Silas's explicit direction ("Do it on Zuzu"), following the Shifting Desks precedent and the 2026-11-15 PT playtest rule. No creative verdict is assumed, and `approved_by_human` was never set.

The agent-owned roadmap is finished. Master issue [kind_robots#4139](https://github.com/silasfelinus/kind_robots/issues/4139) was closed with the `[FLAGGED FOR HUMAN TESTING]` prefix. Play at https://kindrobots.org/play/zuzu-gamebook. Review asks: [PLAYTEST-READINESS-2026-11-15.md](PLAYTEST-READINESS-2026-11-15.md).

What remains is Silas's own call, outside the roadmap:
- **Verdict:** approve, or request revisions. Revision requests become scoped `playtest_iteration: true` tasks in the roadmap.
- **Release:** wider home or Arcade promotion, external sharing, advertising, paid spend, or publication. Each stays explicitly human-controlled, separately from this verdict.

## Preserved former roadmap task (historical, not claimable)

```yaml
  - id: t-017
    milestone: m5
    title: Final complete-game playtest and creative acceptance (not public release)
    status: needs-human
    owner: null
    passes: 0
    stakes: reversible
    gate_human: true
    gate_reason: subjective-acceptance
    depends_on: [t-006, t-007, t-008, t-009, t-012, t-013, t-015]
    note: >-
      This is the ONLY current complete-game human acceptance gate. Historical
      t-010 was marked done before the book was complete and does not constitute
      acceptance of the current nine-act game. Keep this task waiting until
      every nonrecurring agent-owned content, artwork, writing, accessibility,
      15-ending replay, art provenance, seeded balance, and responsive QA task
      is actually DONE, with actual delivered (not queued) images. Then set
      this task to needs-human, switch the project to playtest, and flag the
      OPEN master issue #4139 for Silas's subjective game verdict. His feedback
      drives iterative playtest tasks. This is NOT approval for publication,
      billing, or production-side effects. The existing recurring t-011
      continues as bounded playtest_iteration work after handoff.

      2026-11-15 PT handoff: every nonrecurring agent-owned task is done (t-006, t-007, t-008,
      t-009, t-012, t-013, t-015), with delivered rather than queued art at 385/385 sections.
      Waiting on Silas's subjective game verdict; approved_by_human is NOT set. This is not
      publication approval. Play at https://kindrobots.org/play/zuzu-gamebook. Review asks are
      in projects/zuzu-gamebook/PLAYTEST-READINESS-2026-11-15.md. His feedback becomes
      playtest_iteration tasks.
    updated: '2026-11-15T02:24:21Z'
```
