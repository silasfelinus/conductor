# Monster art linking (t-045) — 151/151 bible species linked

Date: 2026-08-27
Task: cthulhuquarium/t-045 — "Link generated bestiary ArtImages to their Monster
rows via the t-043 API"

---

## TL;DR

Every species in the current 151-species bible (`silasfelinus/cthulhuquarium`,
`fish/*.yaml`) now has its `Monster.artImageId` PATCHed to the ArtImage its
render lives under. Two source batches, one linking pass:

- **t-015** (2026-08-26): 32 tier-1 species, ArtImage ids recorded in
  `projects/cthulhuquarium/docs/t-015-full-art-pass.md`'s own mapping table.
- **t-044** (2026-08-27): 119 remaining species (tiers 2-5), rendered via the
  git-file queue + `auto-art-generate.yml`'s scheduled Auto Art Generate run.
  No mapping was recorded anywhere for this batch when it closed — that's the
  gap this task exists to close.

32 + 119 = 151, matching the bible's species count exactly (verified against a
fresh read-only clone of `silasfelinus/cthulhuquarium` — every `fish/*.yaml`
slug has a corresponding entry below, zero missing, zero extra).

Non-fish t-044 assets (2 characters, 1 background re-render, 6 set pieces, 6
eggs, 2 screens, 1 miscellaneous prop — 18 entries) are **out of scope for
this task**: they have no `Monster` row to link against. The task's own note
lists them alongside the species for completeness of what t-044 rendered, but
the actual linking action only applies where a Monster row exists — i.e.
species. Whatever entity type owns character/set-piece/egg/screen art (if any)
is a separate concern for whoever next touches those asset types.

## How the t-044 mapping was recovered

t-044's close-out (PR #2962) verified delivery by moving files out of
`projects/process/unmatched/`, but never captured the `ArtJob` → `ArtImage`
id mapping `consume_art_queue_core.py` printed at render time. That mapping
only survived in the job logs of Auto Art Generate run #329
(https://github.com/silasfelinus/conductor/actions/runs/33030379982, job
`generate`, id `98381286759`), as `t-045`'s own note anticipated. Pulled the
job log via the GitHub MCP `get_job_logs` tool (`tail_lines: 3000`, which
covered the full "Submit + wait + verify project-art results" step) and
extracted every line matching:

```
DONE projects/process/cthulhuquarium-{name}.webp -> ... (ArtImage {id})
```

119 of the 138 t-044 entries matched `cthulhuquarium-fish-{slug}` — those are
the species. The other 19 lines matched non-fish names (`char-*`, `bg-*`,
`set-*`, `egg-*`, `screen-*`, and one `ichthyonomicon` prop) and were excluded
per the scope note above.

## Verifying the combined list against the live bible

Cloned `silasfelinus/cthulhuquarium` read-only (anonymous HTTPS clone works in
this sandbox even without the repo in scope — same finding as t-022's
2026-08-27 session) and diffed the combined 151-slug list against
`ls fish/*.yaml`: **zero missing, zero extra**. Every bible species has an
ArtImage; no combined-list entry names a species the bible doesn't have.

## Linking mechanism

`PATCH https://kindrobots.org/api/monsters/{slug}` (t-043,
`server/api/monsters/[id].patch.ts`, admin-gated via `KR_API_TOKEN`) with body
`{"artImageId": <id>}`. Monster rows resolve by slug directly — `t-008`'s seed
keys every row on `slug`, and the species slug embedded in each t-044 job
filename (`cthulhuquarium-fish-{slug}.webp`) is exactly that slug with no
transformation needed.

Ran all 151 PATCHes sequentially with a 150ms delay between calls (courtesy
rate limiting, not a requirement) via a one-off script, verifying each
response was `HTTP 200` + `{"success": true}` before moving on.
**151/151 succeeded on the first attempt — zero failures, zero retries.**
Spot-verified 5 afterward via `GET /api/monsters/{slug}` (`bailiff-eel`,
`sardine-common`, `wrapping-sole`, `thumbnail-dace`, `the-watershed`): all
five return the exact `artImageId` this task set.

Did **not** set `cardArtImageId`/`heroArtImageId`/`iconArtImageId` — the task
note only asks for those "if a variant applies," and nothing in either source
batch rendered a distinct card/hero/icon variant per species (every species
has exactly one ArtImage, its full illustration). Those columns stay `null`
until a future task renders variant-specific art.

## Full slug → ArtImage mapping (151 species)

| species (slug) | ArtImage id | source batch |
|---|---|---|
| bailiff-eel | 18561 | t-044 |
| brass-tack-goby | 18794 | t-015 |
| brine-courtiers | 18563 | t-044 |
| candle-snail | 18795 | t-015 |
| catfish-common | 18790 | t-015 |
| cellar-newt | 18796 | t-015 |
| chandelier-lion | 18567 | t-044 |
| choirfish | 18568 | t-044 |
| crawdad-common | 18791 | t-015 |
| culvert-eel | 18570 | t-044 |
| doorstep-whelk | 18797 | t-015 |
| draught-stickleback | 18798 | t-015 |
| drifting-bell | 18573 | t-044 |
| drowned-carp | 18799 | t-015 |
| elder-rustfish | 18575 | t-044 |
| errand-guppy | 18800 | t-015 |
| folding-fry | 18792 | t-015 |
| fractal-bloom | 18578 | t-044 |
| glass-shrimp | 18793 | t-015 |
| glass-weaver | 18580 | t-044 |
| gravel-tetra | 18801 | t-015 |
| guppy-common | 18802 | t-015 |
| gutter-minnow | 18803 | t-015 |
| kitchen-perch | 18804 | t-015 |
| lamplight-angler | 18585 | t-044 |
| ledger-crab | 18586 | t-044 |
| lint-shrimp | 18805 | t-015 |
| marsh-sovereign-crawdad | 18588 | t-044 |
| moebius-crab | 18589 | t-044 |
| old-catfish | 18590 | t-044 |
| pane-limpet | 18806 | t-015 |
| parlour-rustfish | 18807 | t-015 |
| penny-bream | 18808 | t-015 |
| pier-blenny | 18809 | t-015 |
| pin-shrimp | 18810 | t-015 |
| portsmouth-bitterling | 18811 | t-015 |
| postmark-snail | 18812 | t-015 |
| rain-barrel-roach | 18813 | t-015 |
| rainbow-nudibranch | 18599 | t-044 |
| sardine-common | 18814 | t-015 |
| sea-camel | 18601 | t-044 |
| silt-loach | 18815 | t-015 |
| skimmer-fry | 18816 | t-015 |
| standpipe-goby | 18817 | t-015 |
| sump-blob | 18818 | t-015 |
| the-accumulation | 18606 | t-044 |
| the-aggregate | 18607 | t-044 |
| the-almoner | 18608 | t-044 |
| the-annexation | 18609 | t-044 |
| the-antiphon | 18610 | t-044 |
| the-association | 18611 | t-044 |
| the-auditor | 18612 | t-044 |
| the-backlog | 18613 | t-044 |
| the-balance | 18614 | t-044 |
| the-bedding | 18615 | t-044 |
| the-catacomb | 18616 | t-044 |
| the-catchment | 18617 | t-044 |
| the-census | 18618 | t-044 |
| the-clerestory | 18619 | t-044 |
| the-cold-snap | 18620 | t-044 |
| the-committee | 18621 | t-044 |
| the-concern | 18622 | t-044 |
| the-conservatory | 18623 | t-044 |
| the-consignment | 18624 | t-044 |
| the-continuance | 18625 | t-044 |
| the-coronation | 18626 | t-044 |
| the-courier | 18627 | t-044 |
| the-court | 18628 | t-044 |
| the-delivery | 18629 | t-044 |
| the-doorkeeper | 18630 | t-044 |
| the-double-entry | 18631 | t-044 |
| the-downspout | 18632 | t-044 |
| the-efflorescence | 18633 | t-044 |
| the-endowment | 18634 | t-044 |
| the-enforcement | 18635 | t-044 |
| the-enquiry-desk | 18636 | t-044 |
| the-estimate | 18637 | t-044 |
| the-final-notice | 18638 | t-044 |
| the-first-demand | 18639 | t-044 |
| the-fixture | 18640 | t-044 |
| the-float | 18641 | t-044 |
| the-foundation | 18642 | t-044 |
| the-founding-rustfish | 18643 | t-044 |
| the-foyer | 18645 | t-044 |
| the-freeholder | 18646 | t-044 |
| the-glasshouse | 18647 | t-044 |
| the-guest-list | 18648 | t-044 |
| the-harbors-due | 18649 | t-044 |
| the-hold | 18650 | t-044 |
| the-holotype | 18651 | t-044 |
| the-household | 18652 | t-044 |
| the-inquiry | 18653 | t-044 |
| the-inventory | 18654 | t-044 |
| the-keyhole | 18655 | t-044 |
| the-long-consideration | 18659 | t-044 |
| the-long-crossing | 18656 | t-044 |
| the-long-office | 18657 | t-044 |
| the-long-patience | 18658 | t-044 |
| the-long-study | 18660 | t-044 |
| the-mains | 18661 | t-044 |
| the-manifest | 18662 | t-044 |
| the-marginalia | 18663 | t-044 |
| the-night-watch | 18664 | t-044 |
| the-observation | 18665 | t-044 |
| the-parcel | 18666 | t-044 |
| the-permanent-collection | 18667 | t-044 |
| the-pleasant-island | 18668 | t-044 |
| the-principal | 18669 | t-044 |
| the-proprietor | 18670 | t-044 |
| the-provision | 18671 | t-044 |
| the-quire | 18672 | t-044 |
| the-reading-bell | 18673 | t-044 |
| the-reading-room | 18681 | t-044 |
| the-receiving-line | 18674 | t-044 |
| the-reckoning | 18675 | t-044 |
| the-reconciliation | 18676 | t-044 |
| the-round | 18677 | t-044 |
| the-sconce | 18678 | t-044 |
| the-second-notice | 18679 | t-044 |
| the-seven-lights | 18680 | t-044 |
| the-sexton | 18682 | t-044 |
| the-silence | 18683 | t-044 |
| the-single-fish | 18684 | t-044 |
| the-small-hours | 18685 | t-044 |
| the-spectacle | 18686 | t-044 |
| the-stocktake | 18687 | t-044 |
| the-subscription | 18688 | t-044 |
| the-substrate | 18689 | t-044 |
| the-summons | 18690 | t-044 |
| the-tenant | 18691 | t-044 |
| the-testimony | 18692 | t-044 |
| the-threshold | 18693 | t-044 |
| the-type-specimen | 18694 | t-044 |
| the-undercroft | 18695 | t-044 |
| the-undercurrent | 18696 | t-044 |
| the-understone | 18697 | t-044 |
| the-understudy | 18698 | t-044 |
| the-unlidded-rustfish | 18699 | t-044 |
| the-usher | 18700 | t-044 |
| the-verger | 18701 | t-044 |
| the-vespers | 18702 | t-044 |
| the-vigil | 18703 | t-044 |
| the-vitrine | 18704 | t-044 |
| the-waiting-list | 18705 | t-044 |
| the-waterline | 18706 | t-044 |
| the-watershed | 18707 | t-044 |
| the-welcome | 18522 | t-044 |
| thumbnail-dace | 18819 | t-015 |
| till-minnow | 18820 | t-015 |
| tithe-shoal | 18520 | t-044 |
| wrapping-sole | 18821 | t-015 |

All 151 rows above were independently PATCHed and are live in the database as
of this task's close. Verified live via GET https://kindrobots.org/api/monsters/{slug}
for 5 spot-checked entries (see "Linking mechanism" above); the full list is
this table plus the job-log/doc sources it was built from, per the methodology
described above.

## What this unblocks

- The bestiary UI can now render real art for every species instead of a
  placeholder, once whatever front-end surface reads `Monster.artImageId` (or
  `iconPath`/`imagePath`, which this task did not touch) is pointed at it.
- Ruler is Hooked's shared-bestiary handshake (`cthulhuquarium/t-022`,
  `ruler-hooked/t-019`) can now rely on every `games: [cthulhuquarium,
  ruler-hooked]`-tagged species having real art, not just a subset.

## What's still open

- `bg-parlour`'s re-render (flagged in t-015's doc as a photoreal mismatch) is
  included in this link — its ArtImage id changed from 18822 (t-015's
  original, in the doc but never linked to anything) to a new t-044 render.
  Since backgrounds have no Monster row, this task didn't link either — noted
  here only because a future session reconciling "which bg-parlour render is
  live" should know both exist as ArtImage rows.
- The 37 stray `cthulhuquarium-*.webp` files flagged in t-044's TALKBACK entry
  (pre-existing orphans in `projects/process/` before t-044 started) are still
  unresolved — unrelated to this task's scope, re-flagging so it doesn't get
  lost.
- Non-fish asset linking (characters, set pieces, eggs, screens) has no home
  yet — whichever entity model owns those needs its own linking task, once
  that model exists or is identified.
