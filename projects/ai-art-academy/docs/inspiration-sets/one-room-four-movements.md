# One Room, Four Movements

A prompt-first Academy teaching sequence that keeps one interior composition stable while changing the movement-level visual language. This is a planning artifact, not a claim that the four outputs reproduce any particular artist or protected work.

## Learning goal

Students should be able to distinguish a movement's visual grammar from its subject matter. Every image depicts the same modest room: a seated reader beside a window, a small table with a bowl of fruit, patterned curtains, and late-afternoon light.

The controlled composition makes the comparison legible. Changes should come from shape, color, space, surface, and emphasis—not from swapping the scene for a different one.

## Shared source description

> A quiet domestic room viewed from the doorway. One person sits in profile reading beside a tall window. A round table holds a ceramic bowl with three pieces of fruit. Patterned curtains frame the window. Late-afternoon light crosses the floor. Keep the same camera position, furniture placement, figure pose, and object count in every variation.

Use a user-owned photograph, an Academy starter image with verified public-domain provenance, or a newly generated neutral source. Record the source identifier and license in the generation metadata.

## Variation 1 — Impressionism

### Recognition cues

- broken color rather than polished local color
- soft, atmospheric edges
- light treated as the primary event
- visible brushlike surface rhythm
- ordinary modern life without theatrical staging

### Remix instruction

> Preserve the room's layout and the reader's pose. Translate the scene into an Impressionist movement-level treatment: broken touches of color, luminous reflected light, softened edges, and an immediate observed atmosphere. Keep the figure recognizable and the furniture structurally coherent. Do not imitate a named painting or use an artist name.

### Watch for

The model may dissolve the furniture and hands along with the edges. Reject outputs where “atmospheric” becomes structurally unreadable.

## Variation 2 — The Nabis

### Recognition cues

- flattened decorative space
- large interlocking color shapes
- patterned textiles carrying compositional weight
- intimate domestic subject
- ambiguous boundary between object and ornament

### Remix instruction

> Preserve the same room, objects, and pose. Rebuild the image using Nabis movement-level visual grammar: flattened depth, broad decorative color fields, strong textile patterns, simplified contours, and an intimate interior mood. Let the curtains and tabletop pattern organize the composition without obscuring the reader's face or hands. Do not imitate a specific artist or artwork.

### Watch for

The model may turn the room into generic Art Nouveau decoration. The interior should remain quiet, compressed, and domestic rather than becoming a poster full of ornamental borders.

## Variation 3 — Precisionism

### Recognition cues

- crisp geometric simplification
- controlled tonal transitions
- clean planes and hard edges
- architectural order
- little or no visible brush texture

### Remix instruction

> Preserve the room's exact arrangement and the seated reader. Translate the scene into Precisionist movement-level form: clean geometric planes, sharply controlled edges, simplified volumes, measured light, and architectural clarity. Keep the human presence understated but intact. Do not remove evidence of use, labor, or habitation merely to make the room pristine.

### Watch for

The model may erase the person or convert the room into an empty luxury interior. The reader is part of the controlled comparison and must remain present.

## Variation 4 — Harlem Renaissance mural language

### Recognition cues

- rhythmic silhouettes and repeated arcs
- compressed, stage-like space
- strong value grouping
- dignified monumental figures
- visual rhythm that supports historical narrative

### Remix instruction

> Preserve the room, reader, table, fruit, curtains, and camera position. Use broad Harlem Renaissance mural-era movement language: rhythmic silhouettes, compressed spatial layers, repeated arcs, strong value organization, and a dignified monumental treatment of the reader. Keep identity-specific details grounded in the source image. Avoid caricature, costume shorthand, jazz-age clichés, and imitation of any named artist.

### Watch for

This movement cannot be reduced to a decorative “jazz” filter. Reject outputs that invent racialized features, period costumes, nightlife props, or cultural symbols absent from the source.

## Comparison exercise

Place the four outputs in a 2×2 grid without labels. Ask learners to identify each movement using only formal evidence.

For every guess, require three observations from this list:

- edge treatment
- spatial depth
- shape language
- surface texture
- color organization
- role of pattern
- treatment of the human figure
- relationship between light and structure

Reveal the labels only after the observations are recorded.

## Reflection prompts

1. Which variation changed the perceived meaning of the room most while preserving the composition?
2. Where did the generator confuse a movement with a collection of props or stereotypes?
3. Which output best preserved the reader's identity and pose?
4. What evidence distinguishes movement-level remixing from copying a recognizable artwork?

## Generation record

Store the following for every output:

- source image identifier and provenance
- movement slug
- complete positive instruction
- complete negative guidance
- backend and model version
- seed
- sampler, steps, guidance, and remix strength where applicable
- LoRA path, trigger, weight, and license when used
- generated asset identifier
- reviewer notes on composition preservation, style fidelity, identity preservation, and stereotype risk

## Promotion gate

This sequence may be promoted into the Academy UI only when:

- the source image is user-owned or has verified public-domain provenance
- all four outputs preserve the controlled composition well enough for comparison
- protected artist names are absent from generation presets
- the Harlem Renaissance variation receives representation-aware review
- prompts, negative guidance, model details, and seeds are reproducible
- no output is presented as an authentic work of the historical movement
