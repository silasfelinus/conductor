# Gallery migration assessment

Task: `interface-vision/t-024`

## Decision

Do not migrate the remaining object galleries wholesale onto `kr-gallery`.

`kr-gallery` is a passive browse and presentation shell. The remaining candidates are either stateful CRUD pickers, taxonomy tools, or relationship-specific strips. Treating similar-looking grids as interchangeable would erase behavior that callers rely on.

## Candidate findings

| Candidate | Live responsibility | `kr-gallery` fit | Action |
|---|---|---:|---|
| `components/bots/bot-gallery.vue` | Stateful bot selection plus dashboard/dropdown modes, mature and construction filters, add/edit/clone/launch actions, inline form, refresh and store selection | No | Keep canonical. Any cleanup should extract picker chrome only after enumerating every dropdown and interact caller. |
| `components/dreams/dream-gallery.vue` | Dream selection and management with bespoke Dream cards, store-integrated selection and relationship-aware behavior | No | Keep canonical. First standardize Dream card composition and reaction behavior before attempting shared gallery plumbing. |
| `components/rewards/reward-gallery.vue` | CRUD picker with row/dropdown variants and reward-specific editing/selection behavior | No | Keep canonical. Reuse smaller primitives such as filter bars or card shells, not the passive gallery container. |
| `components/characters/character-gallery.vue` | Character picker and CRUD surface used by character/reward interaction flows | No | Keep canonical. Caller coupling makes a direct shell swap high-risk. |
| `components/scenarios/scenario-gallery.vue` | Scenario picker, relationship editing and management actions | No | Keep canonical. Relationship workflows are product behavior, not presentation detail. |
| `components/facets/facet-gallery.vue` | Taxonomy-grouped search and filtering surface | No | Keep separate. A taxonomy browser should not inherit project-gallery view modes. |
| `components/conductor/project-gallery-strip.vue` | Per-project `ArtCollection` image strip | No | Keep separate or merge only into another project-detail art surface. It is not a cross-project gallery. |
| `components/pages/plan-projects-grid.vue` | Small content-collection-driven project list | Partial, but not worth migration alone | Leave in place. Revisit only if its data source is unified with the canonical Project gallery; otherwise migration would add indirection without deleting behavior. |

## Shared work that is actually justified

The five object galleries repeat a *picker-management vocabulary*, not the `kr-gallery` browse recipe. A future bounded task may extract these pieces only after recording caller contracts:

1. header/count/add/refresh chrome;
2. search and maturity/status filter rows;
3. loading, error and empty states;
4. dropdown-mode selected-item summary;
5. inline add/edit form framing.

That shared layer must remain slot-driven and behavior-neutral. Object stores, selection semantics, CRUD actions, cards and relationship workflows stay owned by each gallery.

## Exit criterion

All named candidates were classified against their live responsibility. None is authorized for a wholesale `kr-gallery` migration. No deletion or migration task should be filed per object until it can name a shared behavior that will actually remove duplicate code while preserving dropdown, row, CRUD and relationship callers.
