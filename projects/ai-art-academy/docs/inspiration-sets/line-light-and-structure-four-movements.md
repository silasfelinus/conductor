# Line, Light, and Structure: Four Movement Remix Set

This inspiration set gives the Academy a controlled comparison exercise across four historically distinct visual systems while keeping the subject and composition fixed. It is designed for prompt-mode Kontext remixing and can later be upgraded with verified LoRA evidence without changing the lesson structure.

## Fixed source composition

Use one neutral source image for all four remixes:

> A solitary cyclist paused beside a narrow river at dusk, viewed from a slight distance. A low bridge crosses the water behind them. Reeds occupy the near bank, three small houses sit on the far bank, and a pale moon appears in the upper-right sky.

Keep the cyclist, bridge, river, three houses, reeds, moon, camera angle, and broad light direction stable. The movement should change the visual grammar, not quietly replace the scene.

## 1. Ukiyo-e woodblock

### Recognition cues

- Flat, clearly bounded color areas
- Strong contour lines with selective interior detail
- Compressed depth and deliberate asymmetry
- Patterned water, clouds, foliage, and fabric
- Cropping that feels designed rather than accidental

### Remix prompt

> Reinterpret the source as an Edo-period ukiyo-e woodblock print. Preserve the cyclist, bridge, river, reeds, three houses, moon, and original viewpoint. Use crisp carved contour lines, flat limited pigments, patterned ripples, simplified atmospheric bands, compressed perspective, and an asymmetrical print composition. Let the river and sky carry rhythmic graphic shapes. Keep the result recognizably woodblock-printed rather than painterly or photorealistic.

### Negative guidance

Avoid glossy digital gradients, cinematic depth of field, realistic lens flare, thick oil texture, neon cyberpunk color, anime character rendering, and pseudo-Japanese lettering.

### Failure signs

- The image becomes generic anime instead of printmaking.
- The cyclist or bridge is redesigned so heavily that composition parity is lost.
- Fine photographic shading replaces flat color blocks.
- Decorative symbols are invented as if they were readable Japanese text.

## 2. Romanticism

### Recognition cues

- Landscape and weather carry emotional force
- Strong value contrast and luminous distance
- Human figures feel small against nature
- Diagonal movement through clouds, water, or terrain
- Atmosphere is heightened without becoming fantasy illustration

### Remix prompt

> Reinterpret the source through early nineteenth-century Romantic landscape painting. Preserve the cyclist, bridge, river, reeds, three houses, moon, and original viewpoint. Make the human figure modest in scale against an emotionally charged landscape. Use dramatic cloud movement, deep shadow against luminous evening distance, reflected moonlight on the river, and energetic diagonals in reeds and sky. Keep the scene grounded in observed nature, with grandeur coming from atmosphere and light rather than supernatural objects.

### Negative guidance

Avoid fantasy castles, glowing magic, horror imagery, modern cinematic teal-and-orange grading, photographic HDR, smooth concept-art rendering, and decorative gold ornament.

### Failure signs

- The scene gains fantasy props not present in the source.
- The cyclist becomes a heroic central portrait rather than a small landscape figure.
- Contrast is globally crushed, leaving no luminous depth.
- The result reads as a movie poster instead of a painting.

## 3. Pointillism

### Recognition cues

- Small discrete touches of color remain visibly separate
- Optical mixing replaces blended gradients
- Warm and cool complements structure light
- Shapes remain legible at normal viewing distance
- Surface rhythm is consistent across foreground and background

### Remix prompt

> Reinterpret the source as a late nineteenth-century Pointillist painting. Preserve the cyclist, bridge, river, reeds, three houses, moon, and original viewpoint. Build all forms from small, distinct touches of color with optical mixing instead of smooth blending. Use complementary warm and cool notes to describe dusk, reflected light, foliage, masonry, and the cyclist. Maintain clear silhouettes and spatial depth while keeping the dotted or divided-color surface visible throughout the image.

### Negative guidance

Avoid halftone comic dots, uniform noise overlays, airbrushed gradients, watercolor blooms, chunky mosaic tiles, impressionistic smearing, and photographic texture filters.

### Failure signs

- Dots appear as a superficial filter over an otherwise smooth image.
- The mark scale is so large that objects dissolve.
- The image uses monochrome stippling rather than chromatic optical mixing.
- Foreground and background use incompatible mark systems.

## 4. Bauhaus

### Recognition cues

- Composition organized through geometric hierarchy
- Reduced forms and a disciplined palette
- Functional visual rhythm rather than decorative naturalism
- Strong relationships among circles, bars, planes, and negative space
- The source remains readable through abstraction

### Remix prompt

> Reinterpret the source through a Bauhaus geometric design language. Preserve the cyclist, bridge, river, reeds, three houses, moon, and original viewpoint, but reduce them into a disciplined arrangement of circles, bars, planes, and economical silhouettes. Use a restrained primary-and-neutral palette, strong negative space, clear visual hierarchy, and functional rhythm. Let the bridge become a structural horizontal, the river a sequence of directional planes, the moon a simple circle, and the cyclist a compact readable sign. Keep the result balanced and purposeful rather than merely decorative.

### Negative guidance

Avoid random Memphis-style squiggles, glossy 3D shapes, corporate infographic icons, dense ornamental pattern, photorealistic materials, vaporwave gradients, and illegible total abstraction.

### Failure signs

- The source scene can no longer be identified.
- Geometry is scattered without hierarchy or balance.
- The palette expands into unrelated decorative colors.
- The result resembles a modern app illustration rather than historical design experimentation.

## Blind comparison exercise

Present the four outputs without labels and ask learners to match each image to its movement. Require one observation from each of these categories:

1. **Edge:** carved contour, painted transition, divided touch, or geometric boundary.
2. **Depth:** compressed, atmospheric, optically mixed, or constructed through planes.
3. **Light:** patterned, emotionally luminous, chromatically mixed, or symbolic.
4. **Human scale:** integrated motif, small witness, color-built figure, or reduced sign.

A correct answer without visual evidence does not count. The point is recognition, not movement-name bingo.

## Production record

For each generated image, record:

- source image ID and checksum
- engine and model version
- complete prompt and negative prompt
- seed
- dimensions
- LoRA path and weight, when applicable
- ArtJob and ArtImage IDs
- generation date
- whether composition parity passed manual review

## Promotion gate

Promote an output into the Academy inspiration gallery only when:

- all fixed source elements remain identifiable;
- at least four recognition cues are visible;
- none of the movement-specific failure signs dominate;
- the movement can be identified by a reviewer who has not seen the prompt;
- provenance and generation metadata are complete.

Until the render relay backlog is healthy, this set is complete as a reproducible prompt and evaluation asset. It does not require speculative queue submissions to count as useful curriculum progress.
