# The Ruler Is Hooked — fish ecology and Fishopedia contract

Date: 2026-08-26
Source: Silas, in session

## Design pillar

Every catch belongs in a fantasy world. Ordinary real-world fish may inspire anatomy,
but the authored roster should have a fantastical identity: Rustfish, Choirfish, Drowned
Carp, and similarly memorable species rather than a conventional trout/bass catalog.

The fishing roster is also one of the clearest ways the player sees what their rule has
done to the kingdom. Fish availability changes as the world changes.

## Three Ruler Hooked ecology affinities

Every Ruler Hooked fish receives exactly one gameplay affinity:

- `GOOD` — appears in worlds transformed in broadly positive/restorative directions.
- `NEUTRAL` — appears because the world became *different*, not necessarily better or
  worse: trade choices, unusual alliances, civic fashions, magical experiments, specific
  regional decisions, and other branch flavor belong here.
- `EVIL` — appears in worlds transformed in broadly destructive/corrupt/exploitative
  directions.

These labels describe **the world state that makes a species available**, not the fish's
personal morality. A friendly undead fish can be an `EVIL`-affinity catch because the
conditions that permit it are grim. A predatory or spooky creature can still be
`NEUTRAL` if its habitat comes from a morally ambiguous branch.

Do not overload the shared Creature bible's free-text `alignment` field for this. In
Cthulhuquarium that field is flavor such as `obliging`, `persistent`, or `communal`.
Ruler Hooked's three-way ecology affinity is a separate game mechanic.

## Shared identity with Cthulhuquarium

Cthulhuquarium is an inspiration source and a shared creature catalog, **not a 1:1 roster
mirror**.

When the same creature appears in both games, reuse its canonical identity:

- stable creature slug;
- display name;
- species/taxonomic joke;
- core silhouette and creature concept;
- canonical rarity;
- shared bestiary illustration when appropriate.

In other words: if both games want the oxidation-themed starter fish, both should use
`parlour-rustfish`; do not invent an `iron-fish` merely because the second game lives in a
different setting.

Sharing remains selective. A creature or even an evolution-chain stage may belong to
only one game when its fiction or mechanic does not fit the other. As of this decision,
for example, `parlour-rustfish` and `drowned-carp` are already tagged for both games,
while `elder-rustfish` is currently Cthulhuquarium-only. That selectivity is valid.

The shared Creature record owns identity. Ruler Hooked owns its own availability,
catch history, affinity, habitat, lore presentation, and save-state data.

## Rarity

Ruler Hooked uses the same canonical rarity vocabulary as the shared Creature bible:

`COMMON | UNCOMMON | RARE | EPIC | LEGENDARY | MYTHIC`

For a shared species, preserve its canonical rarity rather than making a fish COMMON in
one project and RARE in another. The games can make the species *feel* differently scarce
through unlock conditions, catch weights, habitat access, lure requirements, and world
state without changing the label on the creature.

Ruler-only species use the same vocabulary so the Fishopedia remains coherent.

## Ruler-specific roster overlay

Ruler Hooked should keep a data-only roster keyed by Creature slug. Suggested shape:

```yaml
- creature: parlour-rustfish
  affinity: NEUTRAL
  habitats: [near_bank, village_edge]
  base_weight: 30
  unlock:
    any:
      - min_turn: 0
  lure_tags: [bread, bright]

- creature: drowned-carp
  affinity: EVIL
  habitats: [far_shore, lake]
  base_weight: 8
  unlock:
    any:
      - flags: [northWoodsSettled, metWarlock]
        sliders:
          nature: { lte: 35 }
      - flags: [lakeCurseAccepted]
```

The exact serialization can change during implementation. The contract should not:
Creature identity is referenced by stable slug, while Ruler-specific ecology is authored
outside the shared creature record.

## Availability is consequence, not a morality meter

Fish should unlock from a mixture of:

- kingdom-health thresholds;
- flags created by specific choices;
- region transformations;
- completed narrative arcs;
- rewards/items or fishing gear;
- combinations of the above.

This is intentionally richer than `nature high = good fish` and `nature low = evil fish`.
Some catches should tell the player exactly which fork they took.

Examples of the *kind* of relationship to author:

- restoring wetlands creates a luminous restorative species;
- industrializing the far shore permits an ash-fed or metal-adapted species;
- signing a strange trade treaty introduces an imported fish that is neither good nor
  evil, just part of that version of the kingdom;
- supporting a magical guild changes the lake enough to produce impossible geometric
  fry;
- protecting a community or festival tradition may make a social/singing species appear;
- accepting a curse or knowingly poisoning a region can unlock undead or corrupted
  catches.

The best fish are therefore miniature consequence cards. Catching one should sometimes
make the player think, "Right. *I did that.*"

## Fishopedia behavior

The Fishopedia is both collection book and history of the player's kingdom.

For each species it should support:

- unknown silhouette / undiscovered state;
- discovered but not yet caught, when the player has learned of a species through lore;
- caught state;
- rarity and ecology affinity;
- habitat and lure hints;
- field note / lore;
- first-caught turn;
- personal best size/quality where applicable;
- count caught;
- a subtle record of why it became available after discovery.

Do **not** spoil every exact unlock condition before discovery. Hints can point toward
world states and choices; after a fish is caught, the entry may reveal the relevant
kingdom consequence more explicitly.

This turns the collection screen into a readable fossil record of the run rather than a
static checklist.

## Catch resolution

The fishing engine should resolve in this order:

1. Build the available roster from current world state and permanent run flags.
2. Filter by reachable habitat/location and gear/lure compatibility.
3. Weight eligible species using canonical rarity plus authored `base_weight` and local
   modifiers.
4. Select deterministically from the run RNG.
5. Resolve specimen properties such as size/quality.
6. Update Fishopedia/catch records and present a catch card.

A seeded save must produce deterministic results from the same sequence of actions.
No wall clock or real-world day/night may affect availability; the project's no-time-lock
pillar still applies.

## Cross-project art rule

Shared species should share their **recognizable creature design**, but the two games do
not have to share every rendered asset.

Cthulhuquarium's Ichthyonomicon illustration can be reused directly where it fits.
Ruler Hooked may also need a catch-card composition, lake-context image, silhouette, or
other presentation asset derived from the same species design. Those are variants of one
creature, not inventions of a near-duplicate species.

Art generation should therefore key on creature slug plus presentation variant, e.g.:

- `parlour-rustfish/bestiary`
- `parlour-rustfish/ruler-catch-card`
- `parlour-rustfish/ruler-silhouette`

## Vertical-slice target

The first implementation slice should prove all three affinities rather than filling one
branch first. A useful target is 15 fish:

- 5 `GOOD`;
- 5 `NEUTRAL`;
- 5 `EVIL`;

Mix shared Cthulhuquarium creatures with Ruler-only concepts. Include at least one shared
species in each affinity where an existing creature fits naturally, but do not force a
shared creature into a branch merely to hit a quota.

The slice is successful when two meaningfully different runs produce visibly different
catch rosters and Fishopedia histories because of kingdom choices, not merely because of
RNG.
