# Hybridizer — playable laboratory design brief

## The fantasy
Two lovingly illustrated ingredients roll into luminous observation chambers.
An oversized brass-and-neon laboratory machine hums, snaps two pictures into
fragmented light, then spits out an absurdly specific new creature. The reveal
is a poster-sized illustration, not a text response.

**Experience:** select left/right concepts; open an ingredient drawer with
art, search, and rarity filters; trigger HYBRIDIZE; see kinetic animation
and result; save/share the discovery, drop the hybrid into either chamber
for a new generation, or continue exploring the machine while an ArtJob
works. A shared discovered-combinations atlas records provenance and
creator credit. Previously generated images resolve immediately.

**Visual direction:** eccentric Victorian natural-history lab crossed with
90s arcade creature-collector console. Deep ink-plum panels, luminous
acid-lime specimens, copper mechanisms, berry-magenta lightning, illustrated
drawers and hand-inked field-journal cards. Full-screen art stage at desktop
and legible compact stage at 390px. Animation is expressive rather than
essential: reduced-motion users receive a quick dissolve and equivalent status.

## Taxonomy contract
* Existing real animals: canonical Facet taxonomy `ANIMAL`.
* Vampires, zombies, ghosts, skeletons, werewolves, dragons, unicorns,
  phoenixes, aliens, robots, cyborgs: canonical `SPECIES`. Users may
  combine these in the same way as animals, but we do not mint a
  `MONSTER` taxonomy.
* Fruits: Facet `OTHER`, grouped as `fruit` until a shared
  taxonomy is designed; not imaginary ANIMAL or SPECIES records.
* Costumed occupations and archetypes: `ARCHETYPE`.
* Other curios: `OTHER`.
* Starter catalog entries with existing `facetId` are confirmed
  *named in a committed facet-content batch*, NOT proven active/live
  or illustrated. Missing and new records need a reconciliation pass.

## Counts and production
200 starters: 73 existing named animal records, 87 additional animals,
20 fruits, 11 fantasy/species, 6 roles and 3 curios. There are
`200 choose 2 = 19,900` unordered distinct pairs, excluding self-fusion.
Pre-generate a curated 4,000 as the launch seed set, then generate
cache misses on demand. Recursive hybrids make the combinatorial domain
open-ended. Every finished generation is a reusable `ArtImage`.

## Identity and caching
Canonical key = SHA-256 of a versioned, sorted pair of immutable
ingredient identities plus recipe/style version. Never key only on
user-entered names or picture labels. Track status, ArtJob, ArtImage,
timestamps, owner and visibility, error/retry count, content flags,
recipe/seed, and a directed provenance DAG for recursive discoveries.
Enforce a depth/cost budget and cycle protection; mirror results only
when visibility/permissions allow it.

## Queue behavior
Cache hit: instant reveal. Cache miss: create one deduplicated request,
display an animated chamber and a nonblocking tracking toast; leave
both selectors usable. Poll job state with backoff and surface an
in-app notice and discoverable ready-results tray on completion.
Notifications persist across tab reloads until acknowledged; do not
require browser push permission. Failed jobs expose honest status and
safe retry without duplicate work.

## User images
Use the existing upload/ArtImage path, validate file types, size
and provenance, require rights and sharing opt-in for public library
reuse, and avoid exposing private or mature inputs to other users.
Uploads become private ingredients by default. Sharing and abuse
moderation need explicit implementation before public launch.

## Visual art requests
1. hybridizer-icon.webp, 256 square: enchanted copper collision
   chamber with two specimen capsules feeding one luminous creature
   silhouette, amethyst enamel and electric-lime sparks.
2. hybridizer-card.webp, 512x768: vivid painterly portrait of a
   vampire bananacat in front of an eccentric brass fusion machine,
   wry grotesque delight, vertically composed.
3. hybridizer-hero.webp, 1280x720: wide retrofuturist laboratory
   with two giant specimen jars, animal and banana on input sides,
   kinetic coils converging on a spectacular new hybrid creature;
   atmosphere, paper labels left blank for UI typography.

All image slots require real traced ArtJob/ArtImage verification before
they can be reported completed. SVG mockup treatments are concept
references, not substitutes for generated art.
