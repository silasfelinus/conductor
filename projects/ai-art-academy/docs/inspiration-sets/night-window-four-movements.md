# Night Window: Four Movements, One Composition

## Teaching goal

This inspiration set holds one quiet interior composition steady while changing only the movement-level visual language. The comparison teaches learners to notice how artists organize shape, light, surface, and emotional distance without copying a protected artist or turning a movement into a costume filter.

## Shared source composition

A person sits beside an open apartment window at night. A small table holds a cup, a folded letter, and a vase with three stems. The room is seen from a slight diagonal. Outside, a few lit windows and a narrow slice of moon are visible. The figure's identity, pose, clothing, room layout, objects, and camera angle remain fixed across all four variants.

Keep constant:

- figure identity and body proportions
- seated pose and gaze direction
- table, cup, letter, vase, and window placement
- camera angle and crop
- night setting
- broad value structure

Allow to change:

- edge treatment
- color relationships
- spatial flattening or depth
- brush or print texture
- symbolic emphasis
- treatment of artificial and moonlight

## Variant 1: Tonalism

### Recognition cues

- compressed, closely related values
- atmosphere dominating local detail
- softened edges and low contrast
- restrained color with one or two temperature shifts
- mood carried by haze, dusk, and silence rather than narrative action

### Movement-level remix prompt

> Reinterpret the fixed night-window composition through late nineteenth-century Tonalism. Use a narrow value range, softened contours, muted blue-gray and umber harmonies, and atmospheric transitions that make the room and night feel continuous. Preserve the person's identity, pose, objects, layout, and camera angle. Avoid named artists, photographic sharpness, high-saturation neon, and theatrical spotlighting.

### Common failure

The model may merely apply a brown fog over a realistic image. A successful result should reorganize edges and value relationships, not just tint the source.

## Variant 2: Fauvism

### Recognition cues

- color chosen for expressive force rather than local accuracy
- broad, confident shape boundaries
- complementary color tensions
- simplified modeling
- spatial depth compressed by color planes

### Movement-level remix prompt

> Reinterpret the fixed night-window composition through early Fauvist visual language. Use bold nonlocal color, broad simplified shapes, complementary contrasts, and energetic painted edges while preserving the person's identity, pose, objects, room layout, and camera angle. Let color carry the emotional temperature. Avoid named artists, cartoon outlines, glossy digital gradients, and random rainbow color.

### Common failure

The model may produce arbitrary saturated colors with no structure. Require a small intentional palette and clear relationships between warm interior shapes and cool exterior shapes.

## Variant 3: Metaphysical painting

### Recognition cues

- ordinary objects arranged with uncanny stillness
- simplified architecture and long, deliberate shadows
- ambiguous scale or perspective
- quiet tension without explicit horror
- symbolic isolation created through spacing

### Movement-level remix prompt

> Reinterpret the fixed night-window composition through early twentieth-century Metaphysical painting. Preserve the person, pose, objects, layout, and camera angle, but simplify the architecture, lengthen selected shadows, clarify object silhouettes, and create an uncanny stillness through spacing and slightly uncertain perspective. Avoid named artists, surreal creature additions, horror imagery, empty plazas replacing the room, and dreamlike object melting.

### Common failure

The model may drift into generic Surrealism. Keep every original object recognizable and create unease through placement, shadow, and perspective rather than impossible transformations.

## Variant 4: Harlem Renaissance mural-era visual language

### Recognition cues

- rhythmic silhouettes and repeated arcs
- compressed, stage-like space
- strong figure-ground design
- narrative dignity and communal visual cadence
- selective geometric simplification informed by mural and graphic traditions

### Movement-level remix prompt

> Reinterpret the fixed night-window composition using movement-level visual language associated with Harlem Renaissance mural and graphic traditions: rhythmic silhouettes, repeated arcs, compressed stage-like space, dignified figure treatment, and a limited warm-cool palette. Preserve the person's identity, pose, clothing, objects, room layout, and camera angle. Do not imitate a named artist. Avoid caricature, racialized feature changes, generic jazz-club props, costume substitution, and decorative pattern that erases the quiet domestic subject.

### Common failure

The model may reduce the movement to nightlife clichés or alter the figure's identity. The lesson succeeds only when rhythm, silhouette, and spatial organization change while the person remains recognizably the same.

## Blind comparison exercise

Show the four outputs without labels and ask learners to identify each movement using only visible evidence. Require two observations before revealing the answer:

1. one observation about composition, edge, or space
2. one observation about color, value, or rhythm

Do not accept period props as sufficient evidence.

## Reflection prompts

- Which variant changes the emotional distance between viewer and figure most strongly?
- Which movement depends most on value structure? Which depends most on color structure?
- Where does simplification clarify the scene, and where does it erase useful information?
- Which output preserves the source composition most faithfully while still feeling transformed?
- What visual evidence distinguishes Metaphysical stillness from generic Surrealism?
- How can a Harlem Renaissance lesson teach rhythm and dignity without collapsing into stereotype?

## Reproducibility record

For every generated comparison, record:

- source image identifier and checksum
- engine and model version
- exact prompt and negative guidance
- seed
- dimensions and sampling settings
- remix strength or denoise value
- LoRA path, trigger, and weight when applicable
- generation date
- human review notes on identity preservation and movement recognition

## Rights and promotion boundary

This set uses movement-level instruction only. Do not include living-artist names, protected brands, or artist-name triggers in generation presets. Historical discussion may name relevant deceased artists, but any artwork displayed beside the lesson requires item-level public-domain or open-access verification under `PUBLIC-DOMAIN-POLICY.md`.

Before front-end promotion, verify that:

- all displayed source works have recorded provenance and license status
- no protected artist names appear in generation configuration
- the figure's identity and body proportions remain stable across variants
- the Harlem Renaissance variant passes representation review
- outputs demonstrate movement-level structure rather than surface filters
- prompt, model, seed, and source metadata are complete
