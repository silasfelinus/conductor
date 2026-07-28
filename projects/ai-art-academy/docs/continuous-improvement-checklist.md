# AI Art Academy continuous-improvement checklist

Use this checklist for recurring `t-010` cycles so each pass produces a distinct, verifiable improvement instead of re-auditing the same blockers.

## Rotation

Choose the first useful lane that has not run in the previous cycle:

1. Front-end polish
2. Roadmap accuracy
3. Inspiration and preview assets
4. Curriculum depth

Record the lane, files changed, and verification in the task note before rearming `t-010`.

### Rotation state

Live rotation state lives on the roadmap task itself: `projects/ai-art-academy/roadmap.yaml`
t-010's `continuous_improvement:` field (`last_lane`/`next_lane`/`last_run`/`last_pr`) is
authoritative and kept current every cycle (t-039, 2026-07-26) — read that field instead of
parsing prose here. Full historical narrative for every past cycle (per-file findings,
verification detail, blocker timelines, back to 2026-07-19) is preserved unedited in
`continuous-improvement-lane-rotation-history.md`, moved out 2026-07-27 (t-010, lane 2) once
this section grew to ~1,290 lines — append fresh cycle history there, not here.

This explicit state is the handoff between recurring cycles. Update it in the same PR as each `t-010` improvement so the next Worker does not infer rotation from a long roadmap note.

## Current curriculum coverage

The Academy currently has 35 movement entries in `curriculum-outline.md` —
Arts and Crafts Movement (§35) was promoted this cycle (2026-07-27, lane 4)
from `docs/curriculum-candidates/arts-and-crafts-movement.md`, a 6th
candidate file that appeared after the previous cycle's "all 5 resolved"
accounting. All three example works (Morris's *Daisy* and *Wild Tulip*,
Morris & Co.'s *Five pink flowers with foliated tendrils*) were VERIFIED
directly against the Met Collection API (`isPublicDomain: true`) this cycle.
Not yet synced into `academyStyles.ts` (see "Lesson seed entries" row below)
— deferred to a future kind_robots PR, matching how every prior movement
addition landed. This cycle also backfilled a missing run_log entry and
corrected stale `continuous_improvement` metadata left by the immediately
prior lane-3 harbor-lesson cycle (PR #1257) — see run_log for detail.

Pre-Raphaelite Brotherhood (§34) was added 2026-07-27 (lane 4):
no source candidate file existed for it (all 5 files in
`docs/curriculum-candidates/` were already resolved — 4 promoted, 1 correctly
held at ai-art-academy/t-043), so this was fresh research rather than a
promotion. All three example works (Millais's *Ophelia*, Hunt's *The
Awakening Conscience*, Rossetti's *Beata Beatrix*) were VERIFIED directly
against their live Wikimedia Commons file pages this cycle. Not yet synced
into `academyStyles.ts` (see "Lesson seed entries" row below) — deferred to
a future kind_robots PR, matching how every prior movement addition landed.

Precisionism (§33) was promoted from
`docs/curriculum-candidates/precisionism.md` this cycle (2026-07-27,
scheduled agent run, lane 4 — lane 3/inspiration-assets re-confirmed blocked
via `scripts/recheck_render_queue.py`, PENDING=144/oldestPending~61h/still
`growing`, before falling back). Precisionism's source candidate named four
figures (Demuth, Sheeler, Crawford, O'Keeffe) but only Demuth (d. 1935)
clears PUBLIC-DOMAIN-POLICY.md's 1956 death-date cutoff — the other three
died after 1956 and are excluded from the generation target and from
exhibited example works, named only as historical-context prose (same
treatment as Picasso/Braque in Cubism and Thomas Hart Benton in American
Regionalism). Verified all three of Demuth's example works (*My Egypt* 1927,
*I Saw the Figure 5 in Gold* 1928, *Incense of a New Church* 1921) directly
via live Wikimedia Commons file pages. Did every axis together in one cycle:
skeleton YAML entry, section 33 prose (key ideas, recognition cues, artist
note, 3 verified example works, remix_hint), a remix-quality paragraph in
"Lesson-only vs remixable", a `v1.13 addition re-check` public-domain
paragraph, a `style-lora-registry.md` row, `teaching-notes.md` row 33, and
`kind-robots-academy-style-preview-precisionism` in `art-prompts.yaml`.
Marked `docs/curriculum-candidates/precisionism.md` itself `PROMOTED`.

**Update (2026-07-27T10:20:00Z lane-4 cycle).** Per this section's own
instruction below, checked `docs/curriculum-candidates/` before adding a 34th
movement: all 5 files are already resolved (ashcan-school, hudson-river-school,
precisionism, the-nabis promoted; harlem-renaissance correctly held at its own
gate, ai-art-academy/t-043). Closed the "Lesson seed entries" gap instead: The
Nabis, Hudson River School, and Precisionism are now synced into kind_robots'
`stores/seeds/academyStyles.ts` (kind_robots PR #1045) — all 33 curriculum-outline.md
movements are now represented in the front-end seed. `exampleWorks`/
`previewImageSrc` remain deferred on all three (and on every other
not-yet-imaged movement), matching every prior sync.

Before adding a 36th movement, finish the known coverage gaps below
unless a newly discovered issue is more urgent — every remaining gap is
blocked solely on home-relay/media-server reachability, not on research or
write access to this repo.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | 33 of 35 movements in curriculum-outline.md are synced to `academyStyles.ts` — The Nabis, Hudson River School, and Precisionism landed 2026-07-27T10:20:00Z via kind_robots PR #1045. Pre-Raphaelite Brotherhood (§34) and Arts and Crafts Movement (§35, promoted this cycle) are not yet synced | Sync `pre-raphaelite` and `arts-and-crafts` into `academyStyles.ts` the same way (`exampleWorks`/`previewImageSrc` still deferred on all of them, see the row below) |
| Example works | 25 movements complete, including Persian Miniature Painting (3 works, all **VERIFIED** by direct `WebFetch` of their Wikimedia Commons file pages — 2026-07-20 egress to commons.wikimedia.org worked, unlike the earlier `artic.edu` 402s), Song Dynasty Landscape Painting (3 works, all **VERIFIED** the same way, 2026-07-21), and Mughal Miniature Painting (3 works, all **VERIFIED** the same way, 2026-07-21). Fayum Mummy Portraits (3 works, **VERIFIED** against the Met Collection API's `isPublicDomain` field, 2026-07-22), Vienna Secession (3 works, **VERIFIED** via the Wikimedia Commons API, 2026-07-24), Joseon Dynasty Korean Genre Painting (3 works, **VERIFIED** via direct Wikimedia Commons file pages, 2026-07-25), The Nabis (3 works, **VERIFIED** via direct Wikimedia Commons file pages, 2026-07-26), Hudson River School (3 works, all **VERIFIED** via direct Wikimedia Commons file pages — 2 already verified in the source candidate, the third, *The Oxbow*, live-verified this cycle, 2026-07-26), and Precisionism (3 works, all **VERIFIED** via direct Wikimedia Commons file pages, 2026-07-27) are all written up but not yet in `examples.manifest.json`. Ashcan School's 4 VERIFIED works are written up in curriculum-outline.md §23 but not yet in `examples.manifest.json` (confirmed absent: no `exampleWorks` field on the `ashcan-school` entry in `stores/seeds/academyStyles.ts` as of 2026-07-19). American Regionalism's 4 works are written up in curriculum-outline.md §24 (sourced, but marked "unverified this cycle" — `WebFetch` to museum hosts returned HTTP 402 through the session egress proxy) | Blocked on media-server write access — same blocker as t-033 (confirmed 2026-07-19: `examples.manifest.json` lives on `media.acrocatranch.com`, not in the kind_robots git repo; this session has `KR_API_TOKEN` but no `KR_RELAY_TOKEN`/`KR_RELAY_USER_ID` and found no in-repo upload path, so it cannot write the manifest or upload images from here). Research/sourcing is already done (curriculum-outline.md §23-33); only the write step remains, plus a direct-fetch spot-check of §24's four URLs when museum/Commons egress is open. Resume once a session with media-server/relay write access is available — do not re-attempt from a sandbox without it |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | UPDATE (2026-07-28 lane 3): all 36 `kind-robots-academy-style-preview-*` requests in `art-prompts.yaml` are now `status: done` (36/36 — t-035's original 33-movement batch, plus Pre-Raphaelite/Arts and Crafts drained shortly after, plus Italian Futurism §36 drained this cycle: job 2733, ArtImage 13038). Render relay confirmed healthy (`recheck_render_queue.py`: `oldestPending: none`) at drain time. Every generated image is RETAINED in `projects/process/` per the fixed `distribute_images.py` invariant (t-035) — none are confirmed live at the production media path yet except `greek-vase-painting` (spot-verified 2026-07-27) | Generation is caught up with curriculum coverage; the remaining gap is delivery. Confirm each retained file lands at `https://media.acrocatranch.com/images/academy/styles/<slug>.webp` (relay/media-server write access this sandbox doesn't hold — same blocker class as t-033/t-034) before wiring the matching `previewImageSrc` in `academyStyles.ts`. A future lane-3 cycle should re-check `projects/process/` for any newly-retained files awaiting delivery, and re-queue a preview for any future new movement (lane 4) promptly so this gap doesn't reopen |
| Remix configs | Registry exists; A/B generation blocked | Resume only after the relay, database, and approved generation path are available |
| Teaching scaffold | Written in `docs/teaching-notes.md`, covering all 35 movements — rows 34 (Pre-Raphaelite Brotherhood) and 35 (Arts and Crafts Movement, added this cycle) are both present; wired into `academy-style-detail.vue`'s Try It / Reflect sections (t-023, done — verified 2026-07-18 via `grep -n "Try it\|Reflect" components/academy/academy-style-detail.vue` on kind_robots main) | No gap — table is current through row 35 |

## Blocker discipline

Do not re-probe a blocker when the roadmap already contains fresh evidence with the same failure signature. Recheck only when capabilities, credentials, egress, relay state, database state, or instructions materially change.

A soft blocker never consumes the whole recurring cycle. Rotate to another lane and land a reversible improvement.

## Completion test

A `t-010` cycle is complete when all of the following are true:

- exactly one primary lane was selected;
- the change is scoped and reversible;
- verification is recorded;
- no live generation, publishing, deployment, spend, secrets, or production mutation occurred;
- **if the cycle opened a kind_robots PR, its CI status was polled and the PR was
  either merged or explicitly left open with a documented reason** (do not treat
  "PR opened" as the cycle's terminal state — a green, unmerged PR stranded at
  session end is not done; see the PR #814/t-036 incident below);
- the recurring task is rearmed to `ready` after merge.

Kaizen from a Reviewer pass, 2026-07-21 (t-036): a lane-1 cycle opened kind_robots
PR #814 (all 3 CI checks green) but ended the session without merging it or
rearming `t-010`, leaving the recurring task stranded at `status: claimed` with an
unmerged-but-green PR — the same failure shape as the earlier PR #942 incident
logged in this task's own roadmap note (2026-07-21 ~01:00 UTC: status field never
flipped after a merge). A later Reviewer-role session had to notice the open PR,
verify CI, and merge + rearm manually. The bullet above closes this gap for every
lane, not just lane 1 — any cycle that opens a kind_robots PR owns polling its CI
and merging (or explicitly parking it) before the cycle ends.
