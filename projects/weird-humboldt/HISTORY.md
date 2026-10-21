# weird-humboldt — task history archive

Full `note:` prose for completed weird-humboldt tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-006 — Develop art direction and queue project icon, card, hero and encounter art

<!-- note:begin t-006 -->
Silas opened the art gate in session on 2026-10-19 PT ("submit the art prompts"), so this no longer waits on t-004. Round 1 is art/ROUND-1.yaml: 24 house-lane (Arthemy) cells, ArtJobs 40841-40864 originally submitted, covering project icon/card/hero, Play title art, Mara/Kit/Juniper/Cedar (two seeds each), the six chapter regions, the prologue meadow, WH-006, WH-021, WH-061 and a card back. Next: --status, review keepers, export them to kind_robots public/ecotone/ (the /play/ecotone board overlays them on its drawn scenes) and projects/images/weird-humboldt-*.webp. Ending-signature art stays behind Keep/Modify/Reject prompt review. DONE 2026-10-19 PT: all 30 cells rendered (6 were rerolls, ArtJobs 40865-40870). 19 reviewed keepers (art/ROUND-1.yaml `keepers:`) are live in kind_robots#3870 under public/ecotone/, and project icon/card/hero are in projects/images/. The ch6 dragon is a provisional keeper.
<!-- note:end t-006 -->

## t-026 — Specify modular finale assembly and 56 ending signatures

<!-- note:begin t-026 -->
Apply ECOTONE-ENDING-GRAMMAR.md. Keep 8 fully written final companion x hope/dark 1/10/30-year core spines, 56 distinct opening x final companion x fate signature paragraphs with art concept prompts, and a small verified selection of optional causal callbacks. The older 32 IDs remain stable; 24 new lens variants are added. Scope value-to-debt, conditional truth provenance and one-screen montage. Do not impose 56 triple epilogues or generate images without the human art gate.

Completed a 120-card Ecotone authored quest / finale iteration with companion- and substance-specific sidequests, 56 companion signatures, 1/10/30-year future bookends and causal callbacks. Repairing confirmed PR #3903 gameplay reachability and formatting regressions before merging; Silas authorized publishing iterative content on 2026-10-20 PT while keeping editorial review open.

Implemented and merged kind_robots PR #3903 (e5bc799792eff4511d32d6eed941c7d1ffdd61e5). Authored first manuscript of 120 canonical encounter seeds, distinct narrative lenses, companion signatures, 1/10/30-year modular futures, and earned callbacks. All 13 final GitHub checks passed. Further second-draft editorial uniqueness and migration checks are explicitly separate follow-up work. Silas approved iterative content release.
<!-- note:end t-026 -->

## t-029 — Ship the Ecotone Play front page and playable prologue slice

<!-- note:begin t-029 -->
Silas, 2026-10-19 PT: "get a front end, pointed to Play". kind_robots /play/ecotone in the Play (arcade) channel, labelled Work in progress: one-screen board with code-drawn redwood/fog scenes (painted art from t-006 overlays as it lands), the four voluntary festival lenses mapping to Mara/Kit/Juniper/Cedar, seeded 2d6 checks on the three sample cards (WH-006, WH-021, WH-061), five skills, Clarity, journal, the six-chapter county map and a locked Endings 0/56 gallery that grants nothing until real finales exist. Text from SAMPLE-CARDS.md and COMPANIONS-AND-PROLOGUE.md. Ensure frontend character copy says Hmong American for Kit and Hispanic father for Cedar; never repeat Kit's withdrawn 1885 ancestry or show retired 40848/40849 portraits. The full engine (t-005/t-022) and 120 cards (t-003) replace this slice later. DONE 2026-10-19 PT: kind_robots#3870 squash-merged (a7d7620), all 24 checks green, with art round 1 and the Kit/Cedar heritage updates. Playwright at 390x844, 768x1024 and 1440x900 showed 0 document overflow in every state, and the run survives a reload.
<!-- note:end t-029 -->

## t-032 — Rebuild the opening: festival or Kinetic race, area then offer then companion, loner path, race conscription

<!-- note:begin t-032 -->
Silas, 2026-10-20 PT (notes_from_silas). In kind_robots /play/ecotone: the first choice is the event: a fictional cannabis festival (partner acro on the lawn leads to Kit, the drum circle in the woods to Juniper; offers sober, stoned or tripping) or the real Kinetic Grand Championship with a fictional afterparty (pit row leads to Cedar, the tattoo tent to Mara; offers sober, tipsy, or the party lenses still being written). Order is area, then the offer, then meet the companion or go alone. On the Kinetic route a racer is hurt at the afterparty and you are conscripted to ride the rest of the race with your companion, then the days that follow. Every beat offers at least two choices, each day opens with face-up "where to" cards, companions can be re-met in other capacities, the opening lens persists, and endings are the companion (or alone) x opening lens x hope/dark from end-of-journey stats. DONE 2026-10-20 PT: kind_robots#3872 squash-merged (f6e1b86), all 21 checks green. The Green Ribbon Fair and the Kinetic Grand Championship routes, Conscripted / The Bay Crossing / The Ferndale Finish, the fair's GR-4 and GR-5 spine beats, white-rabbit forks, the loner path and 70 endings with first-draft finales (bar 5 fair, 7 race; random play near 50/50). Playwright walked both routes to an ending at three widths with zero overflow. Design of record: OPENING-AND-ROUTES.md.
<!-- note:end t-032 -->

## t-033 — Playbook Manager: admin view of Ecotone beats as chained choices, with edits, comments and art requests

<!-- note:begin t-033 -->
Silas, 2026-10-20 PT (notes_from_silas). kind_robots /admin/playbook-manager with an Admin channel tab (requiredRole ADMIN): the playbook as chained choices with sub-choices; sort and filter by day, companion and lens variation; endings and story-spine beats highlighted against random encounters; edit text, comment, add choices, submit or flag images and request art for beats without it. Edits are a database overlay on the authored source, with an export so agents fold them into the code. Schema-affecting (additive tables). 2026-10-20 PT: implementation PR kind_robots#3875 (schema-affecting: additive PlaybookEdit and PlaybookNote tables), merging when CI is green. DONE 2026-10-20 PT: kind_robots#3875 squash-merged (51af450), all 30 checks green including the MariaDB migration replay. /admin/playbook-manager with an Admin tab: route chains, fork pools, crossroads, finale and the five ending storylines; filters by route, day, companion, lens variation and status; edit text, choices, variations and add choices; draft, live (applied in /play/ecotone via /api/playbook/ecotone/live) or revert; comments, image flags and submissions, art requests with job status; JSON export. Schema-affecting: additive PlaybookEdit and PlaybookNote, deployed by the normal Unraid migration step.
<!-- note:end t-033 -->

## t-035 — The Quiet Way: a third, solo opening (marsh, zoo, deer trail) and the Wild Way ecotopia endings

<!-- note:begin t-035 -->
Silas, 2026-10-20 PT (notes_from_silas). A third event at the opening: a contemplative day alone. The marsh leads to Juniper and the zoo to Kit (alternate routes to them), and a deer trail nobody knows goes straight onto the solo path. Animal-first choices are tagged across the route and the animal cards; finishing that route alone is the Wild Way: enough animal-first choices earns the ecological paradise, fewer the bittersweet hermit who never made a real choice. DONE 2026-10-20 PT: kind_robots#3877 squash-merged (dd34104), all 21 checks green. The Quiet Way: A Day to Yourself (marsh to Juniper, zoo to Kit, the deer trail straight to solo), The Bench by the Water (offer), the meeting only if the opening led to someone, The Elk Meadow and The Long Quiet. Animal-first choices are tagged on the route and the marsh, zoo-tribute and Bigfoot cards; finishing the route alone is the Wild Way: four or more is the ecological paradise, fewer the bittersweet Mad River hermit. 84 endings. A loner still meets a newcomer at the crossroads.
<!-- note:end t-035 -->

## t-036 — Playbook Manager for every story game: Shifting Lands, Shifting Desks, the Zuzu gamebook and Emperor of Dust follower and quest lines

<!-- note:begin t-036 -->
Silas, 2026-10-20 PT (notes_from_silas). Generalize /admin/playbook-manager to a game picker with adapters reading each game's authored source: Shifting Lands (lands, locations, deck pools, trials), Shifting Desks (departments, locations, encounters, window shifts, bosses), the Zuzu gamebook (chapters and scenes with explicit next pointers), and Emperor of Dust (days, audiences and options, quests, follower lines and flag-gated quest lines). Read, comment, flag and request art everywhere; text edits go live only where a game reads the overlay (Ecotone first). Emperor of Dust is read-only here, so it never collides with its own active tasks. DONE 2026-10-20 PT: kind_robots#3878 squash-merged (e278cf1), all 23 checks green. The game picker loads Ecotone, Emperor of Dust (50 days, 77 audiences, 77 quests, 20 follower lines, 20 flag-gated quest lines, 8 endings), Zuzu: Shifting Lands (15 location draws, 120 cards, 5 trials), Shifting Desks (draws, window shifts, bosses, 10 endings) and the Zuzu gamebook (377 scenes with explicit turns, no special case needed). Text edits stay Ecotone-only; notes and art requests work for every game, tagged to each game's project and preferred lane.
<!-- note:end t-036 -->

## t-037 — Playbook content layer: live text edits in Shifting Lands, Shifting Desks, the Zuzu gamebook and Emperor of Dust

<!-- note:begin t-037 -->
Step 1 of Silas's 2026-10-20 plan (notes_from_silas). Each game's single lookup (v6Card and trialForLand; encounterById and the boss in currentCard; scene(); questDef and dayDef) consults a live text overlay loaded from /api/playbook/<game>/live, so Save and go live in the Playbook Manager works for every game. Text only: titles, story text, choice labels and outcome text; ids, rolls, effects and structure stay authored, and seeded play is unchanged. Touches those games' lookup functions and stores in a few lines each (cross-project: zuzu-shifting- lands, shifting-desks, zuzu-gamebook, emperor-of-dust).
DONE 2026-10-20 PT: kind_robots#3880 squash-merged (06cc4fe), all checks green. Shifting Lands (v6Card, trialForLand), Shifting Desks (encounterById, windowApplicant, boss), the Zuzu gamebook (scene) and Emperor of Dust (questDef, dayDef with audiences) read a live text overlay loaded from /api/playbook/<game>/live, so Save and go live works in every game. Words only; ids, rolls, effects and links stay authored. verifyPlaybook proves the round trip for every editable beat in all four games. The image-first manager layout Silas asked for next follows in kind_robots#3881.
<!-- note:end t-037 -->

## t-038 — Ecotone play layout to the 2026-10-20 mockups

<!-- note:begin t-038 -->
Silas's mockups (design/2026-10-20/). The play view takes the mockup structure: - top bar: the mark, the day and event line, place and time, and Clarity
  and Endings pills;
- full-bleed scene art, with a left headline column (kind pill, serif
  title, subtitle, narration, and a companion block on encounters with
  the portrait on the right);
- a dialogue panel with a gold kicker, and a choices panel where each
  choice shows its roll and where it leads;
- a bottom nav on every width (Journey, Guides, Map, Journal, Endings). Navy, gold and cream throughout. Real stats and the real ending count replace the mockup's placeholder numbers.
DONE 2026-10-20 PT: kind_robots#3882 squash-merged (ce628a6), all 20 checks green. The play view follows the mockups: navy, gold and cream; top bar with the mark, day and event line, place and day, Nerve, Clarity and Endings pills; full-bleed scene with a left headline column (kind pill, serif title, subtitle, and on companion encounters the name, role and line with the portrait on the right); dialogue and choices panels (each choice shows its roll and where it leads); a Journey / Guides / Map / Journal / Endings bottom nav. Phones stack art, panel and choices in one scroll.
<!-- note:end t-038 -->

## t-039 — Ecotone art styles, the Shifting Desks way

<!-- note:begin t-039 -->
A player-selectable art style, like Shifting Desks. It is view-only, so runs and saves are unaffected, and the choice is remembered per browser. Styles: Painted (the current Z-Image house lane) and Storybook (the code-drawn scenes the mockups show). Each further style keeps its renders under /ecotone/styles/<id>/; any beat it hasn't drawn yet falls back to the base painting, then to the drawn scene. Which checkpoints become styles waits on Silas's bake-off review (t-034).
DONE 2026-10-20 PT: kind_robots#3882 squash-merged (ce628a6). utils/ecotone/artStyles.ts: Painted (default, the shipped paintings) and Storybook (the drawn scenes), picked from the palette button and remembered per browser; view-only, never in the run. A further style lists its renders under /ecotone/styles/<id>/ and falls back to Painted, then the drawn scene, per beat. Which checkpoints become styles is Silas's call after the bake-off review (t-034).
<!-- note:end t-039 -->

## t-040 — Playbook Studio: Story Atlas gallery and focused scene editor

<!-- note:begin t-040 -->
The Playbook Manager becomes the Playbook Studio of the 2026-10-20 mockups. - Story Atlas: a left rail (your stories with beat counts, a Collection
  of routes and sections, live story health with art requests), the
  STORY ATLAS headline with filter pills, and art cards with a numbered
  kind pill, a serif title, the place line, a status dot and an open
  arrow.
- Scene editor: a back link, a serif title, a breadcrumb, a gold-framed
  art card (scene and variant pills, a quoted line, art candidates,
  View art options), and the Edit Scene panel (draft pill, underlined
  Story / Choices / Variants / Art / Notes tabs, a summary footer and a
  gold Save draft button).
Chain view stays available from the Atlas. Every existing edit, note and art tool keeps working.
DONE 2026-10-20 PT: kind_robots#3883 squash-merged (29f1bef), all 21 checks green. The Playbook Manager is now the Playbook Studio (same /admin/playbook-manager route): navy, gold and cream; the Story Atlas (stories rail with beat counts, Collection of routes and sections, Refine filters, live story health with open art requests; art cards with numbered kind pill, serif title, place, status dot) and the scene editor (back link, title and breadcrumb, gold-framed art card with candidates and View art options, Edit Scene panel with draft pill, underlined Story / Choices / Variants / Art / Notes tabs, player choices with rolls, summary and gold Save draft / Save and go live). Chain view one tap away. The mockup's + New beat is left for Silas: adding beats needs engine routing.
<!-- note:end t-040 -->

## t-043 — Temporary checkpoint review page with generation times

<!-- note:begin t-043 -->
Silas asked where to see the example generations; there was none. /admin/art-review (kind_robots) shows every Ecotone art ledger (the bake-off's 8 subjects x 8 lanes and rounds 1-3) side by side with live status, render time (claim to image saved) and queue wait, per-lane median, fastest and slowest, a lightbox with prompt and settings, and a shortlist per lane for picking the 2-4 styles. Temporary: retire it once the styles are picked.
DONE 2026-10-20 PT: kind_robots#3886 squash-merged (2825122), all 25 checks green. /admin/art-review (Admin > Checkpoint Review, admin only) shows the bake-off's 8 subjects x 8 lanes and rounds 1-3 side by side with live status, render time (relay claim to image saved, so it includes model load and upload) and queue wait; per-lane median, fastest and slowest; a lightbox with prompt and settings; and a per-lane shortlist. Retire the page (and its admin tab) once Silas picks the styles for t-042.
<!-- note:end t-043 -->

## t-046 — Second draft I: make high-leverage regional decisions genuinely distinct

<!-- note:begin t-046 -->
Silas (2026-10-20 PT): publish/review/iterate, 80% improve and test vs 20% targeted new prose. Audit 120 authored encounters for mechanical sameness. Replace the invest-or-help boilerplate at 10+ pivotal cards across the six regions with third/fourth specific alternatives, authored outcomes, surprising failures, persistent distinct flags and earned callbacks. Preserve the 2d6/save/art-slot schema, no mandatory moral/substance verdict, 2-4 choices, history/cultural gates, and add deterministic tests for uniqueness and reachability.

Scoped user-approved second-draft implementation adds 13 region-spanning bespoke third alternatives, six complete seven-lens narrated encounters, six uniquely earned future callbacks and conditional ballot/journey memory. Kind Robots PR forthcoming; retain active editing/review loop and no historical/tribal publication waiver.

Merged kind_robots PR #3908 as 8932bb0659c103e1f14c9a7b31eaf5578ede8520. Added 13 bespoke third choices across all six regional chapters, six seven-lens passages (42 path-specific asides), six earned future callbacks and conditional county ballot acknowledgments. All 13 current head workflows passed including Ecotone gameplay, TypeScript, Prettier, and full contract shards. Editorial examples are distinct wry narrative, not imitation of named authors.
<!-- note:end t-046 -->

## t-047 — Second draft II: companion continuity and chosen-family optional scenes

<!-- note:begin t-047 -->
Audit every lead/lens encounter and stay/follow relationship for contradictions; create bespoke recurring callbacks, optional scenes with former companions, and earned found-family outcomes without forcing romance or implying unseen meetings. Coordinate with t-045 chosen-family design and preserve the existing 56 primary companion signatures and 84 overall solo/Wild Way gallery slots.

Implemented four individually gated former-guide meetings and an optional two-meet community potluck, with consequential choices, seven-lens potluck narration, six earned future callbacks, and seeded-eligibility regression tests. This independent portion intentionally does not overwrite the separate pending t-045 chosen-family design from Conductor PR #6394. Kind Robots PR forthcoming.

Kind Robots PR #3910 merged at fa8ebb9d83cda4545b3b652683cb4cc27273385d. The four former-guide encounters plus optional multi-meeting potluck, six earned callbacks, and eligibility/reachability tests shipped. The final PR head passed all 13 required checks, including full contract tests, Ecotone gameplay, TypeScript, and changed-file Prettier. Branch janitor subsequently passed. The separately approved Conductor #6394 art and chosen-family plan is merged; future full seed coverage and save migration remain t-048 and editorial redline is t-049.
<!-- note:end t-047 -->

## t-048 — Second draft III: thousands of seeded journeys and save compatibility

<!-- note:begin t-048 -->
Simulate seeded campaigns across openings, routes, archetypes and switches to prove all reachable endings, safe choice offers, coherent flags, no duplicate cards, no phantom callbacks, replay variety and 45-75 minute pacing. Explicitly protect legacy WH-004/WH-037/WH-058 save IDs as LX variant cards replaced these bonus identifiers. Add regression coverage for recoverable failures, gallery counts and art-outcome identity.

Seeded QA implementation: 8400 additional deterministic playthroughs with card/result art, callbacks, continuity and save roundtrips; title-confirmed migration of older WH-004/037/058 chemical quest references. Audit found that Quiet Way has only three opening lenses while the 84-slot ending gallery includes seven, making four Wild Way lens pairs unreachable. Review PR, preserve release gates, and file a dedicated seven-lens opening fix.

Stage 3 automation complete: merged kind_robots #3932 as ddab6cc and #3939 as 351264e2bbfd83a8e24a4004503f60878ca770d5, each after full passing CI (13 and 15 workflows). The final 8400-run report witnessed all 84/84 ending slots, 564 distinct card/outcome art keys, 17408 failed checks and 1048 earned callbacks. All three routes now offer every voluntary opening lens with authored outcomes; save IDs remain stable and legacy WH-004/037/058 chemical quest references migrate only when log titles prove the old identity. Issue kind_robots #3933 fixed by the merged PR. Human 45-75-minute pacing is NOT validated by automated click counts; carry that as a manual editorial/playtest follow-up during t-049.
<!-- note:end t-048 -->

## t-049 — Second draft IV: prose, history, culture and quality redline

<!-- note:begin t-049 -->
Run chapter-by-chapter editorial review for humor, character agency, distinct mood, source provenance, sober parity, diverse lived-in identities and real-world historical care. Human consultation is required before Tuluwat/Wiyot historical player-facing text ships; do not randomize atrocity or frame history as occult explanation. Leave final publication and creative acceptance gates intact.

First editorial batch underway: twelve rewritten encounters across six regional chapters. Reconciled playable JSON with editorial chapter Markdown, added manuscript synchronization tests and a provenance-conscious redline checklist. Keep 108 other canonical cards and deeper cultural/historical review as remaining scope. No new published Indigenous historical text, production deployment or ArtJobs were included.

Editorial batch one merged on Kind Robots PR #3941 as 01bd03dd299010429f6c7201f5f4d1463ae477bf after all 13 workflows passed. Sharpened WH-001/002, 023/025, 041/044, 063/064, 081/082, 102/103 across all six regional chapters, synchronized six editable reading-kit documents with playable narrative data, and added regression checks for synchronization. Keep t-049 READY for the remaining 108 scene reviews, cultural provenance checks, chemical-path voice consistency and real 45-75-minute human-paced playtesting. Wiyot/Tuluwat player-facing history still requires living-community consultation before publication. Learning (moved from a learning: field, which the processor only accepts on done or blocked events): Prefer a small verified sample from each region and keep the playable manuscript and art-informed editorial copies synchronized. Dry comedy works best after believable details and consequences, not purple prose.

Second focused prose review adds 18 newly redlined regional encounters across six chapters (now 30 of 120 reviewed in this stage), synchronized all six chapter reading kits, and authored 42 distinct lens observations across six representative encounters. Code review and test suite are under way; 90 remaining scenes plus history/provenance and human 45-75 minute playtest gates stay open. No Wiyot/Tuluwat historical prose, image jobs or external publication changed.

PR #3943 merged after all 13 checks green as 65b2df85c831d25a5e4aa76b51969fb375d79d17. Second editorial batch completed 18 additional scenes, 42 new lens asides and storybook parity. Leave 90 canonical scenes plus human playtesting and consultation review open for subsequent sessions. Return t-049 to ready for continued work.

Third editor pass includes 18 more fictional encounters (48/120 cumulative) and 42 new lens-specific asides (84 new asides across rounds two and three). All six editable chapter manuscripts updated, gameplay parity contract extended to 48 selected cards and 12 seven-lens collections. Awaiting CI/review before merge. Cultural consultation, 72 other scene passes and human 45-75-minute gameplay pacing remain open.

Third editorial batch merged to Kind Robots main on PR #3949 as 33b9e928b99389e978cfd969e87c1763588998c6 after all 13 exact-head workflows passed, including seeded Ecotone gameplay, TypeScript, changed-file Prettier and the full contract suite. Added 18 more distinct regional scene revisions (48/120 cumulative), 42 more unique seven-path narrator asides (84 total in rounds 2-3), synchronized six playable/editorial chapter manuscripts and expanded contract tests. Return t-049 to ready for 72 remaining canonical scene line edits, provenance/consultation and measured human 45-75-minute playtesting. Indigenous historical release gates remain intact, with no new art jobs or external deployment.

Editorial completion PR prepared: 63 remaining regional scenes reviewed and revised, all six canonical chapter reading kits synchronized, nine original encounter cards audited and targeted, and test parity expanded to all 111 regional scripts. Full 120/120 encounter editorial coverage; separate historical consultation, subjective creative acceptance, and human 45–75-minute playtesting remain gated.

Editorial completion merged to kind_robots main in PR #3952 at a9cdf8cc1c09e41c9bbba159a6d82b0b1848637b. All 13 exact-head GitHub workflow checks completed successfully including Ecotone gameplay, TypeScript, Changed-file Prettier and the four Contract Tests shards. Finished 63 previously unreviewed regional encounter revisions across all six chapters, synchronized 111 of 111 playable regional scripts with their six chapter reading kits, and audited all nine legacy original encounters for 120/120 editorial coverage. Added full manuscript parity checks and seven-lens Moonstone picnic continuity. This closes the manuscript redline task only; genuine timed human playtesting, Wiyot/Tuluwat community consultation, art matching, subjective creative approval and any public release remain unapproved and tracked by the separate acceptance/creative gate tasks (t-004 and t-007). No ArtJobs or deploys.
<!-- note:end t-049 -->

## t-050 — Third pass: adversarial playthroughs, meaningful setbacks and art-brief completeness

<!-- note:begin t-050 -->
Silas-directed 2026-10-20 PT: simulate many full seeded Ecotone journeys across events, archetypes, lenses, companions, successes and failures. Add permanent quality regressions for dead ends, inert or indistinguishable options, meaningful interesting failed rolls and earned lasting consequences. Audit concept art briefs for every playable event, alternative and result; enforce unique provenance-bearing slot keys and flag weak or missing briefs without stealing the separately claimed t-042 art generation work. Repair concrete defects found, keep canonical manuscript parity and Wiyot/Tuluwat consultation and publication gates intact.

Ecotone adversarial runtime and art-brief coverage implementation staged on worker/weird-humboldt-t-050-adversarial-20261020-b7e2 for CI and review. Distinct event-choice illustration pitches, all authored win/loss branches, thousands of seeded end-to-end personas, saved-state and earned callback checks.

Merged Kind Robots PR #3972 at 55ba1daf8a29b77f7fe7432acdd5b3fe891d2b34 after all 13 GitHub Actions workflows completed green, including TypeScript, formatting, Ecotone gameplay, and four full contract-test shards. The new permanent suite simulates 1764 seeded journeys across 3 events, 7 lenses, all archetypes and six strategies per entry, verifies 566 result branches including 206 forced failures, 5540 real successful and 4145 real failed rolls, earned callback provenance and save/reload. It checks 1236 unique concept-art briefs and adds 3 missing event-choice illustration slots. No production deployment, art-generation job, public release or historic Wiyot/Tuluwat content approval performed. t-042 separately owns the production art ledger and generation; human pacing and creative acceptance remain outside this automated QA completion.
<!-- note:end t-050 -->

## t-051 — Fourth pass: six distinct failed-roll echoes across the regional chapters

<!-- note:begin t-051 -->
Silas-directed follow-up to t-050, 2026-10-20 PT: one intentionally interesting failed investigation per chapter across the six-region Ecotone journey. Strengthen the prose where needed, keep source JSON and the six chapter reading kits exactly synchronized, and give failed rolls meaningful, non-fabricated downstream finale callbacks. Each setback retains agency and consequences distinct from success; no failure should grant the winning evidence or be a disguised success. Include source-linked independent art prompts for each result and consequence, plus deterministic forced-roll and callback provenance tests. Do not interfere with separately claimed t-042 generated art or change historical Wiyot/Tuluwat consultation and publication gates.

Fourth-pass implementation staged on Kind Robots branch worker/weird-humboldt-t-051-failure-echo-29b. One grounded failed investigate result rewritten in each of six regional chapters, all six editorial chapter documents synchronized, six opt-in earned finale callbacks with distinct art moments, and explicit failed-branch art prohibitions with automated provenance tests. Awaiting complete GitHub CI.

Merged Kind Robots PR #3976 as commit 1f12e1a5dc8ecf1c7546de44bd7980fbcae1fe10 after all 13 exact-head Actions checks passed, including Ecotone gameplay, TypeScript, changed-file Prettier and all four contract shards. Rewrote the failed investigations WH-014, WH-026, WH-052, WH-074, WH-094 and WH-114 across the six regions. Synchronized six chapter manuscripts including failure art descriptions, authored six new earned future callbacks and art briefs, prohibited fake success imagery in failure-echo art pitches, and tested every new callback for provenance and absent-flag exclusion. The game suite passed 1764 end-to-end seeded journeys with 566 tested result branches including 206 forced failures, and 1242 unique editorial art briefs. No new ArtJobs, production deploy, Wiyot/Tuluwat publication or final creative acceptance was performed. Art production remains with separately claimed t-042.
<!-- note:end t-051 -->

## t-052 — Submit six failed-roll finale consequence pictures through durable YAML backup

<!-- note:begin t-052 -->
2026-10-21 PT, Silas says keep developing Ecotone and asks whether the established YAML backup can submit art prompts. Use the actively consumed projects/art-prompts.yaml requests queue for six NEW investigation-failure future callback illustration slots added by kind_robots PR #3976, one per chapter. These scenes are additional to the 237 card/outcome/ending subjects already owned by t-042; do not edit t-042's four-style art ledger or duplicate submitted ArtJobs. Use conditional provenance-bearing unique image paths, concrete diffusion-friendly prompts with canonical local scenery, and submit only through the existing queue with no code deployments, external publishing, or history-tribal gated scenes. Verify the workflow accepted the entries, distinguish queued from rendered, and leave images pending if render box unavailable.

Authored six Krea 2 callback illustrations as durable pending requests in projects/art-prompts.yaml on branch worker/weird-humboldt-t-052-art-yaml-20261021-a39c. Unique render paths under public/images/ecotone/failure-echoes and scene-grounded prompts depict only the earned failed rolls in WH-014, WH-026, WH-052, WH-074, WH-094 and WH-114. Existing t-042 four-style ledger and all prior ArtJobs are untouched. No ArtJob claimed or rendered; awaiting PR CI and merge to activate Auto Art Generate trigger.

Merged Conductor PR #6451 at 1f7e8da285e44c0eb598790d3d4fa45bda54a66b after all exact-head CI workflows green. Added six uniquely keyed pending Krea2 art requests for WH-014, WH-026, WH-052, WH-074, WH-094 and WH-114 earned failed-investigation future callbacks to projects/art-prompts.yaml. Only additive YAML rows; existing art jobs and t-042 four-style ledger untouched. The merge triggered Auto Art Generate run #39565956764. Render box and Kind Robots API health both passed, and the workflow reached its live 'Submit + wait + verify art requests' step. Actual ArtJob IDs, finished images and successful file deliveries are NOT yet verified; the six requests remain durable and retriable in the YAML queue. No production deploy or history consultation/publishing gate crossed.
<!-- note:end t-052 -->

## t-053 — Fifth editorial pass: sixteen pivotal scenes, sharp voices and costly choices

<!-- note:begin t-053 -->
Explicit user authorization 2026-10-21 PT: deepen 12-20 pivotal Ecotone scenes across all six regional chapters, the three opening event contexts and the four main companion viewpoints. Rewrite 16 canonical pressure, dilemma, result, and care beats to replace repeated bureaucratic closure with sharp dialogue, humor, surprising character agency and earned losses. Where appropriate, add optional third choices carrying genuine cost or a check rather than pretending every encounter has a binary solution. Keep the regional JSON, editor-facing chapter reading kits and provenance-specific illustration pitches synchronized; preserve intentional continuity, outcome flags, Wiyot/Tuluwat consultation and publishing gates. Regression-test representative costly third choices and rerun adversarial full-path gameplay; do not overlap separately claimed art standard (t-042) or kinetic-course task (t-044).

Fifth-pass implementation staged in kind_robots branch worker/weird-humboldt-t-053-editorial-20261021-c8f4. Sixteen rewritten regional encounter pressures, investigation win/losses and care outcomes across six chapters, mirrored to all six editorial kits; six costly optional third choices (four checks with distinct failed outcomes), conditional returning flag-lines, sixteen unique actual-lead reactions at four pivot scenes, tests enforcing paid choices and no fake companion, and a focused human editorial review packet. No generated art jobs, deploy, public release or Wiyot/Tuluwat consultation gate crossed. PR tests next.

Merged Kind Robots PR #3985 as commit e34793a18c994706acaf448bb9f61c20021305e9, after all 13 exact-head GitHub Actions workflows succeeded, including all four Contract Tests shards, TypeScript, Prettier and Ecotone gameplay. Rewrote 16 pivotal regional encounter pressures, successful and failed investigations and care outcomes, with exact synchronized chapter kits. Six costly third-way options include four checked outcomes with genuine alternative failures and downstream flag-lines. Four pivot scenes feature sixteen authored Mara, Kit, Juniper and Cedar asides gated on the actual traveling guide, plus regression tests and a human editorial packet. Dedicated Ecotone QA passed 1764 seeded journeys, 576 result branches (210 forced failures) and 1252 source-backed unique editorial art briefs. No generated ArtJobs, deployment, public release or Wiyot/Tuluwat gate approval performed. Production art standard t-042 remains separately claimed.
<!-- note:end t-053 -->

## t-054 — Editorial Ecotone art rerolls and live delivery tracking

<!-- note:begin t-054 -->
Owner asked 2026-10-21 PT to edit and submit the Ecotone art. The 237-subject, four-lane standard already contains 948 ArtJob IDs, so never reset or duplicate those requests to repair an all-PENDING reporting ledger. Editorial round 1 revises 15 independent safe card/result/ending scenes (60 additional private art variants) with clearer visual cause/effect, recurring race-machine identity, four genuinely distinct styles and a no-lettering composition. Wire the existing six-hour art workflow to enqueue these missing revisions, refresh real delivery status for both ledgers, and validate privacy, original job integrity and cultural exclusions before submission. Exclude held WH-121, Mara-specific Indigenous imagery, Wiyot/Tuluwat history and sacred designs. Distinguish requests submitted from actual completed renders. Visual curation and integration remain a separate review step; human final release and cultural consultation gates remain unchanged.

Editorial Ecotone art reroll and status pipeline shipped on Conductor PR #6466, merged as 613d58ae3ca85274145492485d52282b1bd5a23f after all six checks green. Original 237 subject x four style ArtJob IDs (948 unique requests) preserved. Authored 15 culturally independent, specifically retouched scene prompts x four distinct private style lanes (60 more requests) plus pre-submit safety validator. The merge started Auto Art Generate run #39586689813, and its "Submit private Ecotone editorial art revisions" step finished successfully. The workflow's subsequent --status pass reconciles queued versus rendered images; do not represent either batch as accepted visual keepers, integrated or publicly published. Held WH-121 and Mara/Wiyot/Tuluwat content was excluded from new art generation. Human image curation and cultural consultation gates remain open.
<!-- note:end t-054 -->
