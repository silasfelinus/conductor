# Gold and Geometry, Four Movements

A controlled comparison lesson for studying how four traditions flatten space and organize a single ceremonial portrait through material, border, ornament, and geometry. The shared source stays intentionally simple so learners can distinguish structural choices from subject replacement.

## Fixed composition

Use one source image throughout:

- one seated adult figure facing forward
- hands resting visibly on the lap
- a high-backed chair centered in the frame
- a small round table at camera right holding one closed book
- a plain wall behind the figure
- a narrow floor band visible along the bottom edge
- soft, even frontal lighting
- portrait orientation, with the figure filling roughly two-thirds of the frame

Keep the person, pose, chair, table, book, camera position, crop, and major silhouettes unchanged. The exercise is about how each movement constructs space and status, not swapping in a different sitter or scene.

## Rights boundary

Teach movements and historically documented techniques, not imitation of a named artist. Use only public-domain reference works from artists who satisfy `PUBLIC-DOMAIN-POLICY.md`. Do not place artist names in generation prompts, negative prompts, presets, filenames, or promotional copy.

Learners may upload an image they own or are authorized to transform. Before promotion, confirm that every displayed example image is public domain or separately licensed for reproduction and that its source and rights statement are recorded.

## 1. Byzantine Mosaic

### Recognition cues

- frontal, hieratic figure with limited naturalistic depth
- shimmering gold ground made from visible tesserae
- small glass or stone tiles with clear grout lines
- simplified folds and facial planes built from color blocks
- symmetrical, ceremonial presentation rather than observed domestic space

### Remix prompt

> Preserve the exact sitter, pose, chair, table, book, crop, and camera position. Reconstruct the image as a Byzantine mosaic made from small glass and gold tesserae: a flat frontal figure, shimmering gold background, visible grout lines, simplified garment folds, and solemn symmetrical presentation. Keep every object and silhouette in its original place.

### Negative guidance

- no named artists or specific churches
- no extra attendants, halos, crowns, or religious symbols
- no photorealistic skin texture
- no loss of the table, chair, or book
- no deep perspective or receding room

### Common failure

The model may apply a gold sparkle filter while leaving the image spatially photographic. A successful result must rebuild surfaces from tiles and flatten the room into a ceremonial field.

## 2. Illuminated Manuscript

### Recognition cues

- jewel-toned tempera color and gold-leaf accents
- flattened or stacked perspective rather than optical depth
- ornate foliate border framing the scene
- crisp, small-scale linework and patterned fabric
- the portrait treated as a miniature page image rather than a freestanding canvas

### Remix prompt

> Preserve the exact sitter, pose, chair, table, book, crop, and camera position. Repaint the image as a medieval illuminated manuscript miniature with jewel-toned tempera, gold-leaf accents, flattened perspective, patterned textiles, and an ornate foliate border around the complete scene. Keep the person and every object clearly recognizable and in place.

### Negative guidance

- no named artists or specific manuscripts
- no added text, pseudo-Latin, marginal creatures, or religious emblems
- no removal of the chair, table, or book
- no photographic depth of field
- no border that covers the sitter's face or hands

### Common failure

The model may generate a decorative frame around an otherwise unchanged portrait. The figure, furniture, and room should all participate in the miniature's flattened, patterned visual grammar.

## 3. Vienna Secession

### Recognition cues

- flat decorative fields combined with selective naturalistic detail
- gold ornament used as pattern rather than as atmospheric light
- geometric motifs, repeated circles, rectangles, and mosaic-like surfaces
- strong contour and compressed depth
- figure and surrounding design integrated into one ornamental composition

### Remix prompt

> Preserve the exact sitter, pose, chair, table, book, crop, and camera position. Reinterpret the portrait through Vienna Secession movement-level ideas: compressed depth, strong contour, selective naturalistic detail, flat gold ornament, and repeated geometric motifs that integrate the sitter, chair, wall, and floor into one decorative composition. Keep the face, hands, and all objects legible.

### Negative guidance

- no named artists
- no copied signature motifs from a specific painting
- no extra jewelry, costume changes, or exposed skin not present in the source
- no removal of the table or book
- no generic Art Deco poster treatment

### Common failure

The model may confuse Secession design with a generic gold luxury filter. The important change is the tension between recognizable anatomy and surrounding flat ornament, not merely metallic color.

## 4. Suprematism

### Recognition cues

- non-objective geometric planes and sharply defined shapes
- limited, high-contrast palette
- strong diagonals and floating spatial relationships
- rejection of descriptive detail in favor of visual weight and rhythm
- the source composition translated into geometry without becoming random decoration

### Remix prompt

> Preserve the source portrait's exact layout as an abstract map: translate the sitter, chair, table, book, wall, and floor into a disciplined Suprematist arrangement of rectangles, circles, bars, and diagonal planes. Maintain the original relative positions and visual weight of every major element while removing descriptive surface detail. Use a limited high-contrast palette and crisp edges.

### Negative guidance

- no named artists or copied canonical compositions
- no readable face or photorealistic body detail
- no random confetti pattern
- no extra shapes without a source-composition role
- no loss of the chair, table, or book as mapped geometric masses

### Common failure

The model may produce arbitrary modern abstraction unrelated to the source. A successful result should remain traceable as a geometric diagram of the original portrait, with each major mass preserved.

## Blind comparison exercise

Hide the movement labels and ask learners to rank each result on:

1. preservation of the source composition
2. recognizable treatment of flatness and depth
3. movement recognition without artist names
4. meaningful use of gold, border, or geometry
5. preservation of the sitter's identity where the movement calls for a figure
6. absence of generic filter behavior

Then ask learners to identify the movement and cite three visible cues before revealing the labels.

## Reflection prompts

- Which result uses gold as material, which uses it as page ornament, and which uses it as flat design?
- Where does the sitter remain an individual, and where does the sitter become a symbol or geometric mass?
- Which movement most clearly turns the frame or border into part of the artwork's logic?
- How do the first three approaches flatten space differently even though all can appear decorative?
- Does the Suprematist result still preserve the source composition, or has it become unrelated abstraction?
- Which prompt produced the most unauthorized additions, and what wording should be tightened?

## Reproducibility record

For every generated comparison, record:

- source image identifier and rights status
- generation engine and model version
- workflow or endpoint version
- complete positive and negative prompts
- seed
- dimensions
- guidance, steps, sampler, and scheduler where applicable
- LoRA path, trigger, and weight where applicable
- generation date
- ArtJob and ArtImage identifiers where available
- manual notes on composition and identity preservation

## Promotion gate

Promote a set only when:

- all four outputs preserve the fixed layout closely enough for a fair comparison
- the sitter's identity and presentation remain stable in the three figurative versions
- the Suprematist version maps every major source mass rather than becoming random abstraction
- movement recognition does not depend on protected artist names
- source and output rights are documented
- representation review finds no unwanted religious, ethnic, gendered, or status symbolism added by the model
- prompts and metadata are sufficient to reproduce or audit the exercise
- weak results and negative findings remain documented rather than quietly replaced
