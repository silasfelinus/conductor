# Zuzu: Shifting Lands: decisions after the build roadmap

This is the human playtest and release checklist that comes after the build roadmap. It is **not** an active Conductor roadmap task and **not** a blocker to the `playtest` lifecycle. It preserves former roadmap task `t-018`, moved here on 2026-11-17 PT at Silas's explicit direction ("Do it on Zuzu"), following the Shifting Desks precedent and the 2026-11-15 PT playtest rule. No creative verdict is assumed, and `approved_by_human` was never set.

The agent-owned roadmap is finished. Master issue [kind_robots#3917](https://github.com/silasfelinus/kind_robots/issues/3917) was closed with the `[FLAGGED FOR HUMAN TESTING]` prefix. Play at https://kindrobots.org/play/zuzu-shifting-lands. The evaluation questions (whether each traveler's road feels distinct, the tone of the dark personal endings, the provisional names) are in the preserved note below.

What remains is Silas's own call, outside the roadmap:
- **Verdict:** approve, or request revisions. Revision requests become scoped `playtest_iteration: true` tasks in the roadmap.
- **Release:** wider home or Arcade promotion, external sharing, advertising, paid spend, or publication. Each stays explicitly human-controlled, separately from this verdict.

## Preserved former roadmap task (historical, not claimable)

```yaml
  - id: t-018
    milestone: m5
    title: "FINAL ONLY — human approval of fully built, illustrated and adversarially tested Shifting Lands"
    status: needs-human
    owner: null
    passes: 0
    stakes: outward-facing
    gate_human: true
    gate_reason: creative-approval
    depends_on: [t-048]
    source_issue: "silasfelinus/kind_robots#3917"
    note: >-
      The ONLY Shifting Lands creative-approval gate. Do not advance to
      needs-human or ask Silas for final visual/game acceptance until
      t-048 proves all authored cards/trials/journals, all follower quests,
      all requisite encounter, quest, consequence and ending images,
      every ending graph path and reached trace, and complete adversarial
      simulations and visual QA have passed. Once all prerequisites are
      verified and merged, offer Silas an Approve/Request revisions verdict
      backed by full evidence. His approval stays explicit; public release,
      spending or production deployment remains separately authorized.

      FOR SILAS (2026-11-14 PT): Shifting Lands is open for playtest. Agent production is
      complete and this gate is your Approve / Request revisions call. It is not approved.
      PLAY: /play/zuzu-shifting-lands on kind_robots main (a self-hosted deploy needs your
      Force Update). READY: 13 premade travelers plus custom travelers, each premade with its
      own road (4 own cards, 3 own choices, 3 own endings), 120 shared cards, 5 trials, 19
      shared and 39 personal endings (all 58 witnessed by seeded replay), title screen,
      scrapbook, achievements, second-person text throughout. ART: 120/120 card faces, 50/52
      own cards, 36/39 personal endings, 13/13 portraits; the last 5 are re-rendering
      (ROUND-16) and ship as a playtest update. PLEASE EVALUATE: whether the roads feel
      distinct per traveler; the tone of the dark personal endings that turn on betraying a
      child (Hester's writ, Wren's kit, the Coyote's runaways, Gideon's three names; harm
      stays off-screen); the provisional names (Hester Kell, Augustin, invented family names);
      balance (kind play wins about 74%). KNOWN LIMITS: settings cover motion and dice sound
      only; saves are per browser. Evidence: projects/zuzu-shifting-lands/READINESS-
      DOSSIER-2026-11-14.md.

      Gate re-check 2026-11-14 PT (gate-triage): deploy step done -- kindrobots.org
      /api/version serves kind_robots 3ba0c28 (main HEAD, 2026-11-14 03:01 PT), which includes
      #5146 (last five plates: every own card and personal ending painted). No Force Update
      needed; /play/zuzu-shifting-lands returns 200. Only Silas's Approve / Request revisions
      verdict remains (creative-approval).

      Gate re-check 2026-11-17 PT (gate-triage, DEPLOY_PREREQ_MET): production now serves
      kind_robots d5898c8 and /play/zuzu-shifting-lands returns 200. Nothing that waits on a
      deploy is left to re-run. Only Silas's Approve / Request revisions verdict remains
      (creative-approval).
    updated: '2026-11-17T19:49:17Z'
    gate_rechecked: '2026-11-17'
```
