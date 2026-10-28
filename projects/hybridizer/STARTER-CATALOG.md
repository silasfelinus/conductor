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
