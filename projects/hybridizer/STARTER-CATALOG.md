# Hybridizer concept roster
Source of truth: `STARTER-CATALOG.json`. Exactly 200 curated starting concepts,
including **73 named existing animal Facets** linked by IDs to the committed
`kind_robots/config/facet-content/batch-0002-animal.json` batch. Remaining
records are proposals to reconcile to the live canonical Facet catalog.

Taxonomy: real animals = ANIMAL; monsters and fantastical lifeforms = SPECIES;
fruit and other curios = OTHER (with a fruit group); roles = ARCHETYPE.
The 4,000 initial pairs are a prioritized production subset, not
the mathematical total of 19,900 two-item starter pairings.

The full JSON preserves stable IDs and audit states, so a pipeline
can safely distinguish existing named records from proposed ones.

## Facet reconciliation (t-006, 2026-10-30)
Every starter is now pinned to one canonical Facet by `facetId`; the game no
longer resolves art by title.

- **73** were already pinned to batch-0002 ANIMAL Facets with images.
- **34** title-only matches were confirmed as the right Facet (unique titles,
  no duplicates) and pinned. Cat, Dog, Rabbit, Lion and Mantis Shrimp resolve
  to SPECIES-taxonomy Facets whose own copy and art are the literal animal
  ("Not a lion-person. An actual lion."), so they are reused, not duplicated.
- **3** aliases pinned to existing Facets: Kiwi -> Kiwi Bird (243),
  Shoebill -> Shoebill Stork (352), Hyena -> Spotted Hyena (378). Generic
  Penguin, Swan, Gecko, Tortoise and Jellyfish stay separate from the specific
  species Facets (Fairy Penguin, Black Swan, ...).
- **90** Facets created (2981-3070): 59 ANIMAL, 5 SPECIES, 3 ARCHETYPE,
  20 fruit and 3 curios as OTHER. Titles that would repeat a COLOR Facet are
  qualified: Orange Fruit, Blueberry Fruit, Pomegranate Fruit. Ledger:
  `facets/STARTER-FACETS-ROUND-1.yaml`.
- Their images are queued as self-hosted Krea 2 ArtJobs in
  `art/STARTER-INGREDIENTS-ROUND-1.yaml`; each attaches to its Facet's
  `imagePath` on completion. `artState` is `facet-image` (110) or
  `art-queued` (90) until delivery is verified.
