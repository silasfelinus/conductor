# Mural Design Brief

## Project goal

Create the final design plan for repainting and extending Silas's fence mural. The output should stay grounded in the real fence, be achievable by a non-expert painter using a grid, and preserve the joy of the original Catbus mural that became a Pokestop.

The desired end state is not just a pretty mockup. It is a paintable plan: flat colors, thick outlines, clear shape boundaries, a chosen palette, a practical order of operations, and a Kind Robots WonderLab coloring tool that lets the palette be tested section by section before painting.

## Current project files

Silas has uploaded the current mural image and the first-draft mural image files in the `projects/mural-design/` project root. Use those as the visual references for the next comparison pass: the current image is the physical-fence baseline, and the first-draft image is the first composition/color direction to improve.

The first-draft image is now also the primary source for the WonderLab coloring-page workflow. It should be segmented into fillable fence/mural sections while the rest of the environment stays visibly colored as context.

## Current preferred direction

The strongest direction so far is a simple Ghibli-inspired alien garden:

- **Right side:** fully refreshed Catbus, cleanly repainted, bold and happy, with orange-brown body, black stripes, yellow eyes, pale cream grin, and teal/aqua windows.
- **Left side:** ivy portal with a secret Totoro-like forest spirit tucked into the greenery.
- **Across the middle:** stylized alien-botanical foliage with large simple leaves, pods, curls, and a few mushrooms.
- **Characters:** normal-sized hidden soot sprites, small Kind Robots-style robots, kodama-like spirits, and rainbow butterflies.
- **Mood:** magical neighborhood transit stop, but more personal and mural-friendly than complicated fan art.

## Interactive coloring workflow

Silas wants a front-end page under the Kind Robots `wonder` dashboard key / WonderLab where the mural can be recolored interactively.

The page should use the first-draft image as the visual source, turn the painted fence into a coloring-page layer, and let each fillable section be assigned by reusable color id. The interface should support setting a selected section to a color id and globally swapping color ids so every section using that color updates at once.

The surrounding environment should remain colored in the preview: sky, clouds, house, roofline, antenna/wires, palm and real plants outside the fence, sidewalk, curb, street, and other off-fence context. The editable area is the actual fence surface and everything painted on it, including the background color, leaves, pods, Catbus, spirits, robots, butterflies, sprites, mushrooms, curls, sparkles, and mural details.

The strongest technical target is an SVG-backed section map with stable path ids, plus JSON metadata for sections and colors. A canvas preview/export layer is fine later, but the first useful version should make section ids and color ids inspectable so the exported assignments can become the paint specification.

See `projects/mural-design/WONDERLAB-COLORING-SPEC.md` for the front-end and asset-pipeline requirements.

## What to keep

- Thick black outlines.
- Flat single-color fills.
- Minimal shading or no shading.
- Board-aware composition that can be transferred with a grid.
- Real ivy integration on the left and right edges.
- Secret details that reward close viewing without making the street-view read messy.
- Catbus as the main anchor on the right.
- Totoro-like secret figure as a quieter anchor on the left.
- Rainbow butterflies as the Kind Robots/rainbow-butflies connective motif.
- Fillable, closed regions that can be mapped to color ids.

## What to change

- The background was brick red / terracotta, but the next palette should push darker and moodier: closer to a purple, magenta, or wine-red family if the foreground colors still pop.
- The final colors should be selected from the PPG Voice of Color deck, not vague digital-only color names.
- Prefer non-sun-fading / exterior-stable choices. The palette can lean slightly blue overall to compensate for sun-fading limits and keep the mural from drifting too warm or washed-out.
- The next generator pass should prioritize coloring-page source assets and section mapping over more fully rendered mural variations.

## What to avoid

- Giant soot sprite. It looked dramatic in mockups but defied the physical fence layout and overpowered the mural.
- Too many tiny details.
- Painterly shading, soft gradients, rendered texture, or anything that requires advanced blending.
- Overcrowded alien plants that erase the simple charm.
- Exact copies of copyrighted Pokemon characters. The mural can evoke creature-collecting magic through original creatures and symbols.
- Text-heavy design. Signs may work, but only if they remain simple and optional.
- Color choices that only work on-screen but fail as practical outdoor paint.
- Turning the whole uploaded photo into black-and-white line art; only the fence/mural layer should become editable coloring-page source art.

## Palette direction

Use a small repeatable palette so touch-up is realistic. The final palette should choose specific PPG Voice of Color swatches for each role.

- **Three greens for leaves:** one yellowish green, one true green-green, and one blueish green. Leaves should carry an overall blueish tint where possible so the mural stays vivid after sun exposure.
- **Black:** thick black linework and cleanup outlines.
- **Off-white:** random beings, eye highlights, small spirits, and Totoro's belly.
- **Yellow:** Catbus eyes.
- **Dark red / magenta / purple-red:** background color. It started as brick red, but the next direction should test a deeper purple, magenta, or wine-red background while preserving foreground contrast.
- **Orange:** Catbus skin/body color.
- **Brown:** Catbus secondary body/stripe color.
- **Robin blue / teal:** Catbus windows.
- **Purple and violet:** butterfly accents.
- **Gray:** robot parts and Totoro body.

## Next generator pass

Ask for source assets that enable the WonderLab coloring page rather than another single flattened mockup:

> From the uploaded first-draft mural image, create a clean coloring-page source for the painted fence only. Preserve the sky, house, sidewalk, curb, street, real plants, and other off-fence environment in full color as locked context. Convert the mural painted on the fence into crisp black outlines with closed, flat fillable regions. Include the fence background itself as fillable regions. Keep the Catbus on the right, the hidden spirit/ivy area on the left, foliage, robots, soot sprites, butterflies, mushrooms, pods, sparkles, and small spirits. No shading, no gradients, no painterly texture. Keep the linework thick, simple, and hand-paintable.

If a variation pass is still needed after sectioning works, ask for variations that restore simplicity and minimalism while keeping the preferred composition and the PPG-palette constraint:

> Create a wide realistic mockup painted onto the actual fence, using the uploaded current mural image as the physical baseline and the uploaded first-draft image as the rough design reference. Keep the Catbus freshly painted on the right, an ivy portal with hidden Totoro-like spirit on the left, normal-sized hidden soot sprites, several small Kind Robots-style robots, rainbow butterflies, and a slightly alien plant landscape. Restore simplicity: fewer leaf types, large readable shapes, flat single-color fills only, no shading, no gradients, thick black outlines, clear negative space, and a practical grid-friendly mural layout. Design around a practical PPG Voice of Color exterior-paint palette: three greens for leaves, black outlines, off-white beings and Totoro belly, yellow Catbus eyes, dark purple-red/magenta background, orange Catbus body, brown Catbus secondary color, robin-blue/teal windows, purple/violet butterfly accents, and gray robot/Totoro body parts. Favor slightly blue-tinted color choices to offset outdoor sun fading. Avoid the giant soot sprite. Make the composition feel magical, personal, and achievable to repaint by hand.

## Practical painting assumptions

- Silas can follow a grid.
- The fence boards themselves can serve as vertical grid columns.
- Existing greenery should be treated as part of the composition, not a problem to fight.
- Black outlines should be painted late because they clean up imperfect color fills.
- The final plan should break the mural into left, middle, and right sections so repainting can happen over multiple sessions.
- The final paint specification must list the chosen PPG Voice of Color swatch name/number for every color role before painting starts.
- The interactive tool's exported color assignments should be usable as the first draft of the final paint specification.