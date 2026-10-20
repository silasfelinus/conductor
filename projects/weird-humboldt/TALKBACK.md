# Weird Humboldt talkback

Append-only reviewer/worker notes. Project created 2026-10-19 PT; no entries yet.

## 2026-10-19 — reviewer: merged #6353 (56 modular ending signatures)
- Docs/roadmap spec only, reversible, CI green, mergeable clean; squash-merged (fc0616a).
- Supersedes #6352 and `worker/ecotone-story-loop-32-endings-20261019-c4r8` (32-ending sibling); that branch is stale and can be deleted by the janitor.
- Pattern: three parallel Ecotone worker branches edited CONTROL.md and roadmap.yaml at once and conflicted; claim the task before starting to avoid duplicates.
- Suggestion: lint ending counts (56 / 32 / 8) across Ecotone contract docs (worker's kaizen).
- 56 system is spec only; nothing implemented yet.

## 2026-10-19 — reviewer session: Play front page and art round 1 (t-029, t-006)
- Silas asked in session for a front end pointed to Play and for the art prompts to be submitted. CONTROL.md
  and notes_from_silas record that opening; it covers the WIP Play page and foundation art only.
- kind_robots#3870: `/play/ecotone` (arcade channel, Work in progress). Shows the prologue's four lenses, the
  guide meeting, WH-006/021/061 with seeded 2d6, one seeded stay/follow crossroads, Guides / County / Journal
  tabs and a locked Endings 0/56. The engine is a pure reducer (`utils/ecotone/engine.ts`); it is a slice for
  t-005/t-022 to replace, not the full engine. Verified with Playwright at 390/768/1440, with 0 document
  overflow in every state.
- Art round 1 (`art/ROUND-1.yaml`): 24 cells plus 6 rerolls, ArtJobs 40841-40870, all DONE. 19 keepers are
  exported (see `keepers:`). Pattern: the house Arthemy lane defaulted Cedar to a young woman until the tags
  said `1boy, male focus, mature man` with female terms in the negative, and it ignores multi-figure scenes
  (Sasquatch family, plunge queue) unless the count and subject are weighted.
- Open for Silas: whether ch6's dragon-on-the-dunes fits the Impossible Festival (Keep/Modify), and the
  Tribal Community Organizer background, left out of the Play page pending cultural review.

## 2026-10-19 — reviewer session: Kit and Cedar portraits re-rendered
- Silas: Kit is Hmong American; Cedar's father is a Hispanic logger and his mother is from a grower family (#3870
  comment). The canon docs are revised in conductor#6358, not here.
- Re-rendered both portraits from corrected prompts (ArtJobs 40871-40874). Keepers: kit-r3-2 (248815) and cedar-r3-2
  (248817), now on kind_robots#3870. This covers #6358's t-030 requeue. The stale 40848/40849/40852/40853 renders
  are not exported. The house lane barely changes Kit's look between the old and new prompts, and still paints
  glowing orbs instead of juggling clubs.

## 2026-10-19 reviewer: #6358 (Hmong Kit, Hispanic father for Cedar) merged
- Branch conflicted with main (#6357/#6359 had already rendered and exported the revised Kit/Cedar portraits). Resolved by keeping main's ArtJobs/keepers ledger, keeping the PR's revised prompts and cast-canon docs, and dropping the now-moot t-030 requeue task.
- Pattern: worker branches that touch `art/ROUND-1.yaml` and `roadmap.yaml` collide with concurrent art close-outs; fetch main before writing art-ledger notes.
- Left open on purpose: #6321 (Emperor of Dust concept art) holds an explicit human art-direction gate for Silas.

10 reviewer: stale worker branches not merged (2026-10-20)
- `worker/ecotone-story-loop-32-endings-20261019-c4r8` (11 commits) and `worker/ecotone-modular-56-ending-signatures-20261019-r7k3` (6 commits) have no open PR and conflict in every shared file (CONTROL.md, ECOTONE-*.md, JOURNEY-LOOP-CONTRACT.md, roadmap.yaml): both add files main already carries. Main absorbed this design line via #6353 (modular 56 signatures), #6344, #6358 and #6397, so a merge would regress newer canon (e.g. Hmong Kit / Hispanic Cedar).
- Decision: do not merge; docs-only so nothing lost. Branches left for `branch-janitor` (`force_delete_branches`) once Silas confirms nothing unique remains.
- Pattern: parallel manual branches on the same spec docs diverge from main within a day; open the PR early so the conflict is resolved while small.
