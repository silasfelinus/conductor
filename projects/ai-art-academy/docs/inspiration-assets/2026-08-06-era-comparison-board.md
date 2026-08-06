# Academy era-comparison board

Date: 2026-08-06
Task: ai-art-academy/t-010, continuous-improvement lane 3

## Purpose

The Academy already has one square preview per curriculum movement. The next useful inspiration asset is not another isolated style tile. It is a single comparison board that helps learners see how visual priorities change across broad eras while holding subject and composition constant.

This brief defines four prompt-ready panels for one educational board. It is intentionally an internal asset specification only. No publication or production render is authorized by this document.

## Shared composition lock

Use the same scene, crop, and camera position in all four panels:

- a small friendly robot seated beside a potted plant on a windowsill;
- three-quarter view, waist-up robot, plant fully visible;
- one window, one table edge, uncluttered background;
- square source composition, later assembled into a 2x2 board;
- no text, logos, signatures, watermarks, contemporary brands, or living-artist references.

The comparison only works if subject placement is stable. Style cues may change material, lighting, contour, depth, and ornament, but not the basic arrangement.

## Panel A: Sacred and symbolic space

Curriculum anchors: Byzantine mosaic, illuminated manuscript, Gothic.

Prompt cues:

> A small friendly robot seated beside a potted plant on a windowsill, rendered as a sacred symbolic image with flattened frontal space, luminous gold ground, jewel-like tesserae and manuscript pigments, patterned borders, deliberate hierarchy of scale, crisp contour, restrained naturalism, no modern text or logos.

Acceptance cues:

- shallow or flattened depth;
- gold or jewel-toned field;
- ornamental border logic;
- symbolic clarity outweighs realism.

Reject if it becomes generic fantasy concept art, photorealistic, or merely adds a gold filter.

## Panel B: Observed world and theatrical light

Curriculum anchors: Northern Renaissance, Baroque chiaroscuro, Neoclassicism.

Prompt cues:

> The identical robot, plant, windowsill, crop, and camera position, rendered with meticulous observed textures, convincing perspective, sculptural anatomy, controlled classical structure, and a strong directional shaft of light emerging from deep shadow, historically grounded materials, no modern text or logos.

Acceptance cues:

- believable volume and perspective;
- tactile surfaces;
- disciplined composition;
- light organizes the scene rather than decorating it.

Reject if it becomes a generic cinematic still or loses the fixed composition.

## Panel C: Perception, rhythm, and expressive surface

Curriculum anchors: Impressionism, Pointillism, Post-Impressionism, Expressionism.

Prompt cues:

> The identical robot, plant, windowsill, crop, and camera position, rebuilt through visible color marks: broken light, optical color mixing, rhythmic directional brushwork, simplified shapes, emotionally charged but coherent color relationships, painterly surface, no modern text or logos.

Acceptance cues:

- visible mark-making carries form;
- color relationships matter more than polished edges;
- the fixed subject remains readable;
- expression comes from surface and rhythm, not facial melodrama.

Reject if it becomes smooth digital painting, random rainbow noise, or a single named artist imitation.

## Panel D: Structure, reduction, and modern design

Curriculum anchors: Cubism, Bauhaus, De Stijl, Art Deco.

Prompt cues:

> The identical robot, plant, windowsill, crop, and camera position, reorganized through geometric planes, reduced forms, modular construction, disciplined primary-color relationships, functional graphic balance, selective machine-age ornament, clean edges, no modern text or logos.

Acceptance cues:

- geometry changes the organization of space;
- reduction remains legible;
- ornament is controlled and structural;
- the panel avoids copying any modern brand identity.

Reject if it becomes a generic vector icon, corporate infographic, or living-designer pastiche.

## Assembly contract

- Render each panel independently from the same locked source image and seed family.
- Preserve the four raw panels as separate evidence assets.
- Assemble only after all four pass the recognition checks above.
- Final board layout: 2x2, equal panel area, narrow neutral gutters, no baked-in labels.
- Labels and lesson links belong in accessible HTML around the image, not inside the bitmap.
- Suggested eventual destination: `public/images/academy/inspiration/era-comparison-board.webp` with four sibling source panels.

## Why this is the next asset

The existing movement thumbnails answer “what does this style look like?” This board answers the more educational question: “what changed in how artists organized space, light, surface, and structure?” It reuses the Academy’s established constant-subject comparison method, avoids redundant one-off thumbnails, and can support timeline, lesson, and remix-selection surfaces without inventing a new curriculum entry.

## Follow-through gate

A later rendering cycle may queue these four panels through the existing Academy art pipeline. Before queuing, verify that no equivalent era-comparison request or completed board already exists in `projects/art-prompts.yaml`, the Academy asset manifest, or recent ArtJobs. Do not create duplicates merely because this brief exists.
