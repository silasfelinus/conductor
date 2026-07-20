# SLUG-POLICY.md — the one slug rule for dream-cycle content

**Status:** canonical (maintained). Supersedes the ad-hoc slug guidance that was
scattered across the brief and never kept in sync. `build_dream_proposal.py` and
`build_dream_records.py` enforce this; `scripts/dream_slug_image_cleanup.py` is the
one-time migration that brought existing rows into line.

Applies to every kind_robots row a dream build creates — Dreams (PITCH / GENRE /
LOCATION), Characters, Rewards, Bots, Scenarios, Facets — and to the image folders
that hold their art.

## The rules

1. **kebab-case, ASCII only.** Lowercase `[a-z0-9]` words joined by single hyphens.
   No spaces, underscores, apostrophes, or accents. `sound-cannery`, not
   `Sound_Cannery` or `sound--cannery`.

2. **Prefer two words. Avoid 3+ words unless the extra word adds real clarity.**
   Two words is the target — it keeps titles scannable and indexes clean. Three or
   more words are allowed only when every word earns its place (a genuine multi-word
   name where dropping a word loses meaning): `serendipity-space-bar` keeps all three
   because `space-bar` alone is ambiguous. Trim filler suffixes — `-festival`,
   `-collection`, `-sanctuary` used as generic tails — down to the core name:
   `cthulian-jam-band-festival` → `cthulian-jam-band`.

3. **No leading article.** Drop a leading `the-` / `a-` / `an-` — a wall of `the-…`
   slugs wrecks alphabetical indexing on the gallery and every dropdown.
   `the-lantern-greenhouse` → `lantern-greenhouse`.
   **Carve-out:** keep the article only when removing it would leave a single bare
   word *and* the article is part of the proper name — `the-marrow`, `the-tangle`
   stay, because `marrow` / `tangle` alone read as fragments. Two-word `the-` names
   are the exception, not the pattern; never let a 3+ word slug keep its `the-`.

4. **Globally unique per entity type.** Dream slugs are globally unique in
   kind_robots — a PITCH world card and its LOCATION must NOT collide (that collision
   is what produced `comet-market` + `the-comet-market-2`). Give the world card the
   proposal's own slug and each location a distinct, meaningful slug; never resolve a
   collision by bolting on `-2` or a stray `the-`.

5. **One slice, one slug, everywhere.** The dream's slug is the through-line: its
   PitchSheet, its characters/rewards/bots/scenarios, and its art all reference the
   same clean slug. A dream slice's art lives under one collection folder named for
   the world slug.

## Image folders follow the slug

Every image lives under a **typed** folder keyed by the entity's clean slug:

```
/images/dreams/<world-slug>/<element-slug>-card.webp   # a dream slice's cards
/images/rewards/<reward-slug>.webp                     # NOT /rewards/<type>/…
/images/characters/<character-slug>.webp
/images/scenarios/<scenario-slug>.webp
/images/facets/<facet-slug>.webp                       # NOT under /images/dreams/
/images/bots/<bot-slug>.webp
```

No `the-…-collection` folders, no images parked at the `/images/` root, no reward art
missing its `/images/` prefix. If the slug changes, the folder moves with it.

## creationSource (not a slug rule, but the same "be correct" spirit)

Dreams created by the fully-autonomous daily fast-lane carry `creationSource: "AI"`
(no human authored that specific dream). Use `"HYBRID"` when Silas seeds the idea and
the loop builds it out; reserve `"HUMAN"` for rows a person hand-authored. The default
was silently landing everything as `HUMAN` — fixed in `build_dream_records.py`.

## Enforcement

- **Generators** apply rules 1–4 mechanically (`normalize_slug`) and the brief tells
  the author to honor 2-word preference and genre variety.
- **CI / review**: a slug that starts with `the-` and has 3+ words, or any 4+ word
  slug, should be questioned in review.
- **Migration**: `scripts/dream_slug_image_cleanup.py` is the record of the one-time
  cleanup (merges, renames, imagePath normalization) applied on 2026-07-20.
