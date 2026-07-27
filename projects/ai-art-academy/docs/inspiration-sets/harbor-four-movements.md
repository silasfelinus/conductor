# Harbor, Four Movements

A controlled comparison lesson for studying how movements reorganize the same visual facts.

## Fixed composition

Use one source image throughout:

- a small working harbor viewed from a slightly elevated quay
- two moored sailboats in the foreground
- a low warehouse and crane across the water
- three workers carrying crates
- late-afternoon light from camera left
- a broad strip of sky, calm water, and a clear horizon

Keep the camera position, principal silhouettes, boat count, worker count, horizon, and major light direction unchanged. The exercise is about visual language, not quietly replacing the assignment with a different postcard.

## Rights boundary

Teach movements and historically documented techniques, not imitation of a named artist. Use only public-domain reference works from artists who satisfy the Academy policy. Do not place artist names in generation prompts, negative prompts, presets, filenames, or promotional copy.

Learners may upload an image they own or are authorized to transform. Before promotion, confirm that every displayed example image is public domain or separately licensed for reproduction and that its source and rights statement are recorded.

## 1. Impressionism

### Recognition cues

- broken, visible brush-like marks
- high-key outdoor color
- light and atmosphere taking priority over hard contour
- reflected color in water and pale surfaces
- small figures integrated into the larger field of light

### Remix prompt

> Preserve the exact harbor composition and identities of all visible people. Reinterpret the scene through movement-level Impressionist ideas: broken color, open-air late-afternoon light, softened distant edges, lively water reflections, and visible painterly marks. Keep boats, workers, warehouse, crane, horizon, and camera position unchanged.

### Negative guidance

- no named artists
- no extra boats or workers
- no fantasy architecture
- no photographic sharpness
- no heavy black outlines
- no smeared faces or changed clothing identities

### Common failure

The model often translates “Impressionism” into generic blur. A successful result should retain readable boats, workers, and harbor structure while changing edge hierarchy, color interaction, and mark character.

## 2. Precisionism

### Recognition cues

- simplified industrial geometry
- crisp planes and controlled edges
- restrained human presence
- clean spatial organization
- strong shadows and economical detail

### Remix prompt

> Preserve the exact harbor composition and identities of all visible people. Reinterpret the warehouse, crane, boats, quay, and reflections through movement-level Precisionist ideas: simplified geometric masses, crisp edges, measured spacing, clean shadow shapes, and restrained surface detail. Keep the harbor believable and retain every worker.

### Negative guidance

- no named artists
- no futuristic machinery
- no factory replacing the harbor
- no deletion of workers
- no chrome science-fiction surfaces
- no text, logos, or signage

### Common failure

The model may decide that “industrial” means “build a completely different factory.” The fixed warehouse and crane must become more geometrically organized without the harbor changing jobs.

## 3. Tonalism

### Recognition cues

- narrow, unified color range
- atmospheric veils
- softened transitions
- quiet mood and broad masses
- subdued detail supporting a dominant tone

### Remix prompt

> Preserve the exact harbor composition and identities of all visible people. Reinterpret the scene through movement-level Tonalist ideas: a restrained blue-gray and muted amber harmony, soft atmospheric transitions, broad quiet masses, low-contrast distance, and a contemplative late-day mood. Keep boats, workers, warehouse, crane, horizon, and camera position unchanged.

### Negative guidance

- no named artists
- no night conversion
- no supernatural fog
- no vanished workers
- no monochrome filter pasted over unchanged detail
- no dramatic storm

### Common failure

A flat color wash is not enough. Tonal unity should reorganize contrast, depth, and emphasis while preserving the source scene.

## 4. Fauvism

### Recognition cues

- non-naturalistic high-intensity color
- simplified shapes
- energetic contour and color contrast
- expressive rather than descriptive local color
- flattened or compressed depth

### Remix prompt

> Preserve the exact harbor composition and identities of all visible people. Reinterpret the scene through movement-level Fauvist ideas: vivid non-naturalistic color, simplified harbor shapes, energetic contour, bold complementary contrasts, and compressed depth. Keep every boat, worker, building, crane, horizon, and the original camera position legible.

### Negative guidance

- no named artists
- no neon cyberpunk lighting
- no psychedelic patterns
- no extra people or boats
- no cartoon franchise styling
- no loss of facial or clothing identity

### Common failure

The model may substitute modern neon aesthetics for early twentieth-century expressive color. Favor large, purposeful color relationships over glow effects and decorative visual noise.

## Blind comparison exercise

Hide the movement labels and ask learners to rank each result on:

1. composition preservation
2. identity preservation
3. movement recognition
4. meaningful change in color structure
5. meaningful change in edge and shape treatment
6. absence of generic “art filter” behavior

Then ask learners to identify the movement and cite three visible cues before revealing the labels.

## Reflection prompts

- Which result changes space most strongly while keeping the same objects?
- Which movement makes workers feel most integrated with the setting, and which isolates them?
- Where does color describe observed light, establish mood, organize geometry, or act expressively?
- Which result is recognizable without relying on a famous artist’s signature mannerisms?
- Which prompt produced the most preservation failures, and what wording should be tightened?

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

- the four results preserve the fixed composition closely enough for a fair comparison
- all visible people retain consistent identity, count, role, and presentation
- movement recognition does not depend on protected artist names
- source and output rights are documented
- representation review finds no stereotyping, dehumanization, or erasure of workers
- prompts and metadata are sufficient to reproduce or audit the exercise
- weak results and negative findings remain documented rather than quietly replaced
