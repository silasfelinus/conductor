# Newsfeed Bias Controls

## Direction

Kind Robots should borrow the best idea from Ground News without cloning its product: make political viewpoint balance visible and user-adjustable.

The feed should never silently decide what "balanced" means. It should expose the mix, explain the labels, and let the user choose how much ideological contrast they want.

## User-facing controls

### Perspective mix

A simple control should let users choose among modes such as:

- **Focused** — prioritize the user's selected viewpoint range while still surfacing major opposing coverage when relevant.
- **Balanced** — deliberately mix left, center, and right-leaning coverage.
- **Broad spectrum** — maximize viewpoint variety and include more contrasting sources.
- **Custom** — user-adjustable weights for left, center-left, center, center-right, and right.

These labels are presentation vocabulary, not a required database enum. The implementation should use normalized numeric weights so more dimensions can be added later.

### Bias visibility

Each item may show a compact source-perspective indicator when reliable metadata exists. Users should be able to:

- show or hide perspective labels
- filter by perspective range
- request contrasting coverage for a story
- see why a source received its label
- disable political balancing entirely for non-political feeds

## Modular contract

Political perspective is one optional ranking dimension, not a property welded into every feed item.

Suggested normalized metadata:

- `perspectiveScore`: optional number on a documented scale
- `perspectiveLabel`: optional display bucket
- `perspectiveSource`: where the rating came from
- `perspectiveConfidence`: optional confidence or coverage quality
- `topicPolitical`: whether the article should participate in political balancing

Suggested preference shape:

- perspective mode
- per-bucket weights
- label visibility
- contrast preference
- minimum confidence threshold

The feed-ranking layer consumes these preferences. Source adapters only normalize metadata; homepage components only render the result.

## Guardrails

- Never infer a user's politics from unrelated behavior.
- Never describe source bias ratings as objective fact; expose methodology and provenance.
- Do not force artificial left/right symmetry when evidence quality differs.
- Keep factual reliability and political perspective as separate dimensions.
- Do not downgrade primary sources merely because they lack a political label.
- Unrated sources remain usable and visibly unrated.
- Politics controls should not distort technical, artistic, health, or malaria feeds unless an item is genuinely political.

## MVP path

The first release does not need a perfect global media-rating database.

1. Build the registry and ranking contracts so perspective is pluggable.
2. Seed a small, transparent source metadata catalog for the initial political and activism feeds.
3. Add a single Balanced / Focused / Broad spectrum control.
4. Show labels only where metadata exists.
5. Add custom weighting and "show me contrasting coverage" after the core feed works.

This preserves the fast MVP while preventing a future rewrite into a monolithic recommendation engine.
