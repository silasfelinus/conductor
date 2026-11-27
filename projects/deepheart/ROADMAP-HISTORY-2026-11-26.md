# Roadmap history — 2026-11-26 PT

Exact replaced source YAML; historical only. Source commit `06538af28ab1f75f8ad7cc206f80d357d382251d`, blob `14118d1897976bf2e233aa37f96006f565db18e1`.

## t-012

<!-- raw:begin t-012 -->
    note: |-
      Queued is not rendered is not delivered. Portraits land under /images/deepheart/.

      Anthro direction work in review: fifty unique portrait specifications, hero-first selector, species-free player labels, and a new 94-subject private repaint ledger. Rendering and canonical delivery remain outstanding and must return t-012 to ready after the PRs merge.

      The Deepheart anthropomorphic-cartoony visual canon, hero-first builder, and private mature-admin comparison bible /admin/deepheart/bible were merged in kind_robots PR #5268 with ten completed green CI workflows. The 40-cell 5-scenes-by-8-models high-priority (900) private style trial manifest was merged in conductor PR #7511; the 94-cell bulk repaint remains drafted with auto_submit: false until art direction is reviewed. The Conductor bible URL fix merged in PR #7515 with successful Worker PR CI. Resume this task to confirm Auto Art Generate accepted all 40 ArtJob IDs, inspect actually rendered mature/private images, decide the cartoon-anthro style before unlocking the 94-cell repaint, and wire URL-verified art to the runtime. At this handoff no ArtJob IDs or delivered image URLs for the new trial were verified. Do not close t-012 yet.

      Deepheart Art bible link was a nested Nuxt route whose parent lacked a NuxtPage outlet. Child component could not render. Opened a scoped route-outlet fix with a regression contract, pending GitHub checks. The forty style samples and ninety-four held repaints still require visual review and delivery; retain the art task for follow-up.

      Silas approved Deepheart's visual bake-off in session 2026-11-17 PT: Krea 2 is the default for all ordinary art; Furrytoon Mix XL v3 is preferred for adult-only intimate romance unlocks. The Art bible route repair Kind Robots #5299 is merged and confirmed working. Resume t-012 to release the held Krea 2 anthro repaint manifest and establish separate private Furrytoon romance art direction. Do not publish generated adult imagery or treat old completed Krea 2 humanoid backlog jobs as accepted anthro replacements.

      Silas approved Krea 2 for 94 normal anthro repaint cells and Furrytoon Mix XL v3 for 41 separate private, mature romance unlock candidates. The proposed Conductor manifest and Design Brief edits opt both ledgers into the scheduled ArtJob sweep while preserving old delivered jobs and isolating mature image keys. Awaiting green CI and merge. No new ArtJob IDs or delivered URLs have yet been verified, and in-game mature-only unlock UI is still outstanding.

      Silas selected Krea 2 for every standard Deepheart picture and Furrytoon Mix XL v3 for separate mature romantic unlocks. Conductor PR #7564 merged at 35249a4 after green CI and Kind Robots PR #5303 merged at 8edab70 after seven green checks. The auto-art workflow #44256987440 accepted 94 new Krea 2 ArtJobs (69761-69854) and 41 private mature Furrytoon ArtJobs (69855-69895), recorded on Conductor main. No final render delivery URLs or completed ArtImage IDs have been verified. After-hours candidate assets are still isolated from runtime; verify mature-only romance unlock enforcement, delivery and image display before marking t-012 done. Previous pre-anthro pictures are not accepted replacements.

      Art-first Deepheart app branch adds 122 approved normal-art references, a session-authenticated admin image endpoint, portrait/room/title/ending art bindings, and builder preference/romance discovery gating. Runtime final image delivery and the full t-012 gallery audit remain unverified. App PR is pending and t-012 must return ready after scoped merge.

      Deepheart art-first PR kind_robots#5641 merged and verified green. The approved ArtImage IDs are referenced by the preview, but end-to-end media delivery and visual review remain outstanding. Return t-012 to ready, and address the next discovery-knowledge leak in the optimizer so hidden pair histories and romance matches do not appear before being earned.

      Scoped Deepheart knowledge-and-synergy integration: choice reactions now explicitly reveal first-time likes/dislikes; the party optimizer only scores and explains learned relationship supports, known romances and discovered preference clashes. Actual combat, support scenes and romance mechanics are unchanged. Test cases added for hidden and revealed optimizer output and durable chronicle records. Art-delivery audit remains pending, so t-012 must return ready after the app PR merges.

      2026-11-25 PT reconciliation: #5646 merged 81107cf8 and #5665 merged b9b24fef; discovery and art bible increments landed, but full rendered/delivered/wired art coverage is not verified. Release abandoned review ownership.

      App commit 9440f855 connects all twelve existing approved court ArtImage references to the playable cast and choice-room art, with catalog regression assertions. CI, authenticated rendering, and the complete delivery audit remain outstanding; return ready after scoped merge.

      Kind Robots #5857 merged d8d0e15d after all seven successful CI runs; all twelve court ArtImages wired to cast and live encounter component. Actual authenticated delivery/visual audit remains outstanding. Return to ready.

      App commit f9c1347d binds seven already completed Krea 2 ArtImages (273855–273858, 273872–273873, 273875; ArtJobs 69511–69514, 69528–69529, 69531) to four canon-compatible non-anthro boss portraits and three artifact scrapbook plates. All 94 approved anthro repaint and 41 separate private mature jobs have DONE records. Actual live media delivery and remaining art still need verification; return ready after CI and partial merge.

      Kind Robots #5874 merged 7e6cb9fd after seven completed successful CI workflows, including Playbook Kit 45745943645. Four boss portraits and three artifact plates are mapped to completed Krea 2 ArtImages. Authenticated delivery and remaining art coverage still need verification; return ready.

      App commit e72a4e98 maps 20 already completed Krea 2 achievement ArtJobs 69637–69656 to the actual Deepheart achievement pane via the existing protected art endpoint; preserves fallback icons and catalog images if delivery fails. Adds assertions for all twenty distinct badge mappings. CI and authenticated delivery verification pending; return ready after scoped merge for remaining scrapbook art.

      Kind Robots #5895 merged at 101a403e after all seven latest-head CI workflows passed, including Playbook Kit 45815098940 and Contract Tests 45815099056. All twenty completed Krea 2 achievement badge ArtJobs 69637–69656 are now mapped. Live delivery remains unverified. Return ready for remaining visual coverage.

      App commit 114273d2 connects existing boss and Mimic art to combat targets, boss doors and boss stage; shows each existing layer landscape while choosing doors. Existing image access and fallback preserved. Added mapping assertions. CI and actual media delivery/geometry pending; return ready after scoped merge.

      2026-11-26 PT pr-medic: #5897 sat red 3h on TypeScript (TS2345 x3 in
      verifyDeepheart.test.ts, destructured pairs widened under noUncheckedIndexedAccess).
      Rescued as kind_robots#5902 (as const fix), merged 2478093b after all checks passed;
      #5897 closed. Boss/Mimic portraits in combat and layer art live on main. Remaining: full
      bestiary and dedicated boss plates. Return to ready.
<!-- raw:end t-012 -->
