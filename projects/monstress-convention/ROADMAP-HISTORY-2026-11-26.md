# Roadmap history — 2026-11-26 PT

Exact replaced YAML blocks, not live direction. Source commit `06538af28ab1f75f8ad7cc206f80d357d382251d`, blob `57b77b077e11f6635e1d53293630a1571dc6aa39`.

## goal

<!-- raw:begin goal -->
goal: >-
  Develop MONSTRIQUE as an adult point-and-click murder mystery: Iris is the field protagonist; her astute germophobic boss Norb supports her; at the seedy motel smarmy franchise agent Odette and adult companion Violet are both murdered, both become ghost witnesses, and the separate Monstrique Convention Center plus joke shop, mansion and sewers unlock through city leads. Deliver a fully playable, fair-clue investigation with hotspot-and-verb puzzles, shared evidence/topic notebooks, differential dialogue, an interactive ghost witness, optional consensual flirtation, lavish hand-painted single-screen art, seeded playtests, and a guest/CHILD/mature-off-safe general edition alongside server-authorized mature extras for signed-in non-CHILD opt-in adults. The initial public Play route and dual editions were approved in kind_robots#4903; full-story visual acceptance, new public promotion and any further publication remain separately gated.
<!-- raw:end goal -->

## t-015

<!-- raw:begin t-015 -->
    note: |-
      Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

      AUDIT DONE 2026-11-12: projects/monstress-convention/STANDARD-AUDIT-2026-11-12.md holds the Met/Partial/Missing table, a proposed achievement list with award points, character-fit notes and the three smallest next PRs. Start there.

      Start with the audit table from docs/agents/main-game-standard.md (title screen; settings menu; save/load and persistent progress; 12+ achievements; scrapbook; multiple endings with painted plates; customizable characters; 3+ replay hooks), marking each Met / Partial / Missing with evidence (file, route, live record). Put the table in this note and the first PR. Then close each gap in small CI-tested PRs; queue any needed ending, scrapbook or portrait art in an auto_submit ledger.

      Item 7 (customizable characters) applies "in most cases": if this genre makes it a poor fit, say so in the audit with the reason and leave it for Silas rather than skipping silently.

      Achievements are tracked by their own task; this one covers everything else.

      2026-11-11 PT: First main-game standard implementation slice prepared for kind_robots: title Achievements entry, persistent Endings gallery, truthful per-browser settings copy, and a two-step current-edition case/keepsake reset. The other edition and account achievements are left untouched. Remaining standard gaps include account-backed saves, volume controls, run history, painted ending plates, and deeper replay/customization.

      2026-11-11 PT: First main-game-standard slice shipped in kind_robots#5061 (squash 22da02d). Title Achievements sheet with pending-catalog empty state, endings scrapbook, accurate browser-local settings description, and double-confirmed edition-scoped save and keepsake reset. All six latest-head GitHub workflows passed including the full contract suites. Remaining t-015: account-backed saves, sound/music volume, finished-run history, ending artwork delivery, additional earned endings and replay/customization decisions. Return to ready rather than falsely marking the broad standard complete.
<!-- raw:end t-015 -->

## t-011

<!-- raw:begin t-011 -->
    note: |-
      Require authenticated opt-in and no CHILD role (including CHILD+ADMIN); verify nav, highlight, project list, search/discovery, SSR hydration, direct game route, game JSON/API, ArtImage access. ?showMature=true must never grant access. Do not publish externally as part of this task.

      Scoped admin-navigation check in kind_robots: moved Monstrique to the first Admin destinations and added role/maturity/CHILD launch-visibility regression tests. Remaining t-011 security matrix remains outstanding, so return this task to ready after the nav fix merges.

      2026-11-07 PT: Verified and merged kind_robots #4893 (df79f9035b0ed808c2eb2bb47c981a1331a99e7d). MONSTRIQUE now has explicit navigation:true at Admin sort 11 and an actual nav/route/mature/child access contract test. All seven CI workflows completed green including contract and TypeScript. Remaining t-011 security work: project/search/highlight, SSR and image/API access, production proof; keep ready rather than marking the whole audit done.

      2026-11-07 PT: Added Admin launcher opt-in affordance for mature-off non-CHILD administrators on desktop and mobile without revealing Monstrique itself; persisted consent uses existing MaturityToggle/AccountStore. New contract asserts both surfaces, no spoiler leaks and existing nav authorization. This is a scoped t-011 slice; remaining security matrix returns to ready after merging.

      2026-11-07 PT: Verified all eight GitHub workflows, including the full contract shard and tablet audit; merged kind_robots #4902 (06267009b68a908c11e88a399d95d95fb8c3e266). Mature-off, non-CHILD Admin users now see a generic persisted opt-in control in both launcher layouts, then the gated Monstrique nav entry on consent. No name leak before opt-in, and no Play release. Full t-011 security audit still remains (SSR, discovery, ArtImages, production runtime), so return to ready. Live deployment unverified.

      2026-11-07 PT: Implemented opt-in general versus mature Monstrique editions in kind_robots worker branch. General-audience game preserves the Chapter One detective path, removes flirting/romance scrapbook content, rewrites suggestive dialogue and uses a separate save. The mature audience decision comes from a no-store JWT-only server endpoint and existing role/consent predicate. Public Play route and nav are outward-facing: implementation PR requires security and visual human gate before merge/deployment. Existing private Admin studio remains separate.

      2026-11-07 PT: Added a general-safe, guest-playable Chapter One alongside a server-JWT-authorized mature edition in kind_robots DRAFT PR #4903 (head 42e1b0037729bd19b22e71cdc5671e99d2dd801e; CI pending). Includes explicit public-scene/topics/scrapbook allowlists, separate saves, covered murder scene, no general-edition flirting, and regression replay. This is an outward-facing route: keep draft UNMERGED until human visual/publication review and complete server asset/SSR security audit. Canonical dual-edition design notes merged in conductor PR #7159. Additional t-011 security work is still required, so return this task to ready rather than marking the audit finished.

      PARTIAL MERGED 2026-11-09 PT: Silas explicitly replied "Human approved" in the current ChatGPT session to the pending human gate on Kind Robots PR #4903. The formerly draft public-safe general plus server-authorized mature edition PR was reconciled with current main, 10/10 latest-head GitHub workflows completed successfully, and PR #4903 squash-merged at dee2774007c79bda5b162940b68745269683f77a. This approval is for this specific Play route and two-edition release; it is not blanket approval of future mature assets, home Highlights, community promotion, or the full-game t-013 visual acceptance. Remaining t-011 work: independently verify direct ArtImage URL protections, SSR/hydration, search/project discovery, cross-account save isolation, authenticated live behavior, and production deployment before marking the security matrix complete. No manual deployment performed.

      2026-11-11 PT coordination audit: the general Play route is approved and merged, not awaiting a first release gate. Keep this task ready for the unfinished two-edition security matrix: direct ArtImage and splash URLs, SSR/hydration, public discovery, cross-account and cross-edition saves, CHILD+ADMIN and invalid JWT, and verified production behavior. The `/admin/monstrique` Studio (Preview + Series bible, kind_robots#5010) is a separate ADMIN + mature-only surface.
<!-- raw:end t-011 -->
