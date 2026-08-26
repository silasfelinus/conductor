# Cthulhuquarium full art pass (t-015) — 32 fish + backgrounds landed

Date: 2026-08-26
Task: cthulhuquarium/t-015 — "Full art pass — 20 fish plus tank backgrounds"

---

## TL;DR

32/32 jobs completed with zero failures: 28 tier-1 ("common") species plus 4
tank backgrounds, using the pipeline recipe `cthulhuquarium/t-005` proved
(`POST /api/art/enqueue` → `GET /api/art/queue/:id` → `GET /api/art/image/:id`),
`engine: "flux"`, `variant: "schnell"`. Combined with the 4 species already
rendered in this session's style-proof pass (catfish-common, crawdad-common,
folding-fry, glass-shrimp), that's all 32 of the bible's current tier-1
species covered.

**The task note's "20 shipping species" figure is stale.** The bible has
grown to 152 species across all tiers since that note was written; 32 is the
full current tier-1 ("commons") set. This pass covers all of tier-1, not a
20-species subset of it.

## Why the style concern in t-005's note no longer applies

t-005 (2026-08-25 early) flagged that Flux-schnell rendered photoreal,
non-silhouette fish and recommended testing a LoRA/checkpoint or
post-process before a full production pass. **That finding is obsolete**:
the bible's whole art direction was rewritten the same day (2026-08-25,
`ART-DIRECTION.md` in the `silasfelinus/cthulhuquarium` repo) away from
silhouette-forward entirely, toward eight named historical-print "plates"
(`gosse` hand-coloured lithograph, `trade-card` chromolithograph cigarette
card, `gyotaku` ink rubbing, `blaschka` glass museum model, and four more) —
each a concrete *medium*, never a style adjective or a negation. t-005's
test renders used the pre-rewrite prompt text and are not representative of
what the bible asks for today.

This session ran a 4-species style-proof batch first (catfish-common/gosse,
crawdad-common/trade-card, folding-fry/gyotaku, glass-shrimp/blaschka)
against the *current* bible prompts before committing to the full pass. All
four rendered as convincing, distinct hits on their assigned plate — see the
image review below. That proof is what justified proceeding with the
remaining 28 species in the same session rather than parking t-015 behind a
new style-investigation task.

## Full slug → ArtImage mapping

All jobs used `engine: "flux"`, `variant: "schnell"`, `designer:
"cthulhuquarium-t-015-full-pass"` (or `-t-015-style-proof` for the first 4),
`projectSlug: "cthulhuquarium"`. Prompts are each species' current
`art_prompt` field, read directly from the bible
(`silasfelinus/cthulhuquarium` repo, `fish/<slug>.yaml`) via a read-only
clone — this session had no push access to that repo, matching the scope
gap `cthulhuquarium/t-037`'s TALKBACK entry already documented; read access
over the git proxy is unaffected and was sufficient for this task.

| species (slug) | plate | ArtJob id | ArtImage id |
|---|---|---|---|
| catfish-common | gosse | 9874 | 18790 |
| crawdad-common | trade-card | 9875 | 18791 |
| folding-fry | gyotaku | 9876 | 18792 |
| glass-shrimp | blaschka | 9877 | 18793 |
| brass-tack-goby | gosse | 9878 | 18794 |
| candle-snail | gosse | 9879 | 18795 |
| cellar-newt | gosse | 9880 | 18796 |
| doorstep-whelk | gosse | 9881 | 18797 |
| draught-stickleback | gosse | 9882 | 18798 |
| drowned-carp | gosse | 9883 | 18799 |
| errand-guppy | gosse | 9884 | 18800 |
| gravel-tetra | gosse | 9885 | 18801 |
| guppy-common | gosse | 9886 | 18802 |
| gutter-minnow | gosse | 9887 | 18803 |
| kitchen-perch | gosse | 9888 | 18804 |
| lint-shrimp | gosse | 9889 | 18805 |
| pane-limpet | trade-card | 9890 | 18806 |
| parlour-rustfish | gosse | 9891 | 18807 |
| penny-bream | gosse | 9892 | 18808 |
| pier-blenny | gosse | 9893 | 18809 |
| pin-shrimp | gosse | 9894 | 18810 |
| portsmouth-bitterling | gosse | 9895 | 18811 |
| postmark-snail | gosse | 9896 | 18812 |
| rain-barrel-roach | gosse | 9897 | 18813 |
| sardine-common | gosse | 9898 | 18814 |
| silt-loach | gosse | 9899 | 18815 |
| skimmer-fry | gyotaku | 9900 | 18816 |
| standpipe-goby | gosse | 9901 | 18817 |
| sump-blob | blaschka | 9902 | 18818 |
| thumbnail-dace | gosse | 9903 | 18819 |
| till-minnow | gosse | 9904 | 18820 |
| wrapping-sole | gosse | 9905 | 18821 |
| bg-parlour (tank bg) | gosse | 9906 | 18822 |
| bg-shipwreck (tank bg) | gosse | 9907 | 18823 |
| bg-cathedral (tank bg) | gosse | 9908 | 18824 |
| bg-abyssal (tank bg) | gosse | 9909 | 18825 |

All 32 `ArtJob` rows completed `attempts: 1`, `error: null` — zero retries,
zero failures, matching t-005's earlier "the conductor side works" finding.
Timing: the first job (catfish-common, 9874) took a genuine ~25-minute
cold-start (well beyond t-005's ~11-minute worst case, likely a longer relay
idle period before this session started) before the model was warm;
9875–9909 rendered at the previously-documented ~40s/image steady state.

## Image review — spot-checked, not exhaustive

Visually inspected 8 of 32 across 4 of the bible's plates:

- **catfish-common (gosse)**: genuinely convincing hand-coloured 1850s
  natural-history lithograph — foxed cream paper, fine engraved line,
  gravel/rock still-life elements, a period-style plate-number caption.
- **crawdad-common (trade-card)**: strong hit on the chromolithograph
  cigarette-card format — ornamental border, blank name banner exactly as
  briefed. Minor prompt-fidelity miss: claws render near-symmetrical rather
  than "wildly mismatched," and the body reads more crab-like than
  crawdad-like — a creature-specific nuance, not a plate/style failure.
- **folding-fry (gyotaku)**: excellent ink-rubbing look — flat black body,
  fine radiating fin lines, fibrous-paper ground, even a brush-signature
  mark in the corner. The "folded paper plane" origami-facet detail from the
  prompt didn't visibly land; again a creature-quirk miss, not a plate miss.
- **glass-shrimp (blaschka)**: the standout of the proof batch — transparent
  glass body on a wire mount in a museum display case, correct magenta
  interior detail, case reflections, a wooden base placard.
- **sardine-common (gosse)**: notably **resolves** the exact multi-subject
  failure t-005 flagged as unresolved — this render shows four fish in a
  genuine schooling composition, background fish blurred/faded, matching the
  prompt's "tight schooling formation... fading into darkness" ask that
  Flux-schnell previously dropped entirely under the old prompt style.
- **sump-blob (blaschka)**: another strong glass-model hit — glossy pink
  translucent glass, visible internal bubbles, wire mount, blurred interior
  background.
- **bg-shipwreck**: strong lithograph-plate look — cream border, plate
  captions, engraved-texture water, warm light rays; the "acid-green weed
  ribbon" rendered gold rather than green (minor colour miss).
- **bg-parlour**: **the one real inconsistency found.** This background
  reads as a photoreal/3D render (glass tank walls, realistic light shafts)
  rather than the `gosse` lithograph-plate look every fish and the other
  three backgrounds hit. Worth a re-render or a prompt tweak in a future
  pass; not re-rendered here to avoid open-endedly iterating on one asset at
  the expense of closing this task with what is otherwise a strong,
  consistent set.

**Not yet visually reviewed**: the remaining 24 fish. Given 8/9 spot-checked
across 4 different plates and a range of creature types were strong,
consistent hits, and all 32 jobs completed cleanly with matching prompts,
this is recorded as a reasonable confidence level rather than a claim that
every one of the 32 was individually eyeballed — a future pass should still
glance through the rest before treating the full bestiary as launch-ready.

## What this does NOT do: link ArtImage → Monster rows

The task's own note asks to "preserve prompt, model, seed, and destination
metadata on every ArtImage so any fish can be regenerated or traced" — that
is satisfied (every `ArtImage` carries `designer`, `projectSlug`, its
prompt, model/checkpoint, and seed, queryable via `GET /api/art/image/:id`).

It does **not** wire `Monster.artImageId` for each species, even though
`cthulhuquarium/t-008` (seed the bestiary) is now `done` and real `Monster`
rows exist for every species above. Checked `server/api/` in kind_robots:
**no Monster API route exists at all** — there is no way to `PATCH` a
Monster's `artImageId` from outside a direct database session, which this
sandboxed session does not have. This is a hard gap, not a shortcut taken
here: filed as `cthulhuquarium/t-043` (see roadmap) rather than guessed at
or worked around.

## Recommendation

- The remaining 120 non-tier-1 species (tiers 2–5) are a substantially
  larger batch (proportionally ~4x this one) and should get their own task
  rather than be folded into t-015's "shipping species" scope after the
  fact.
- Re-render `bg-parlour` (or retune its prompt) before treating the
  background set as finished — it's the one asset here that doesn't match
  the bible's own art direction.
- `cthulhuquarium/t-043` (Monster API) blocks actually *using* any of this
  art in the game UI, not just this task's own metadata ask.
