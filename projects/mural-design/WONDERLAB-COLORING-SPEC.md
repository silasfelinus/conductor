# WonderLab Mural Coloring Tool Spec

Date: 2026-07-09
Project: `mural-design`
Target app surface: Kind Robots `wonder` dashboard key / WonderLab
Primary source image: `projects/mural-design/firstdraft.jpg`

## Intent

Build a Kind Robots front-end tool that lets Silas test mural paint colors before touching the real fence. The tool should use the first-draft mural image as the design reference, turn the painted fence area into a coloring-page style layer, and let each fillable section be assigned by reusable color id.

This is not just an art mockup. It is a practical paint-planning interface: click a leaf, pod, sprite, robot, butterfly, Catbus part, or fence-background section; assign a palette color; swap a color id globally; and keep iterating until the mural becomes a paintable specification.

## Editable vs locked areas

The locked environment should remain visibly colored in the preview:

- sky
- clouds
- house and roofline
- antenna / wires
- palm / real plants outside the fence
- sidewalk, curb, and street
- any other off-fence context

The editable area is the actual fence surface and anything painted on it:

- fence background color, including the current red / future wine-red-magenta-purple candidate
- foliage and pods
- Catbus body, face, eyes, windows, legs, stripes, and details
- hidden soot sprites
- Totoro-like/forest-spirit figure
- kodama-like spirits
- Kind Robots-style robot(s)
- butterflies
- mushrooms, curls, sparkle marks, and other mural details

The rule is simple: if it is on the actual fence, it can change color. If it is outside the fence, it stays as colored context.

## Asset pipeline

Use the existing Kontext setup to produce the coloring-page source assets. The first useful output should be a layered/fillable asset set rather than another generic rendered variation.

Recommended outputs:

1. `firstdraft.jpg` — original colored reference.
2. `mural-environment.webp` — locked colored background/environment with the fence/mural layer prepared for overlay.
3. `mural-lineart.svg` or `mural-lineart.webp` — crisp black linework for the fence/mural area.
4. `mural-section-map.svg` — closed vector regions for each fillable section.
5. `mural-sections.json` — section metadata keyed by stable section id.
6. `mural-palette.json` — reusable color ids, labels, roles, and eventual PPG Voice of Color swatches.

The ideal interaction is SVG-first because closed paths are naturally fillable and can be assigned by id. A canvas compositor is acceptable for preview/export, but the component should not rely on canvas-only hit detection if SVG sections are available.

## Kontext prompt direction

Use prompt language like:

> From the uploaded first-draft mural image, create a clean coloring-page source for the painted fence only. Preserve the sky, house, sidewalk, curb, street, real plants, and other off-fence environment in full color as locked context. Convert the mural painted on the fence into crisp black outlines with closed, flat fillable regions. Include the fence background itself as fillable regions. Keep the Catbus on the right, the hidden spirit/ivy area on the left, foliage, robots, soot sprites, butterflies, mushrooms, pods, sparkles, and small spirits. No shading, no gradients, no painterly texture. Keep the linework thick, simple, and hand-paintable.

The key constraint: do **not** turn the entire photograph into a black-and-white coloring page. Only the fence/mural layer becomes editable linework; the surrounding environment stays colored.

## Section model

A section should have a stable id and minimal metadata:

```ts
export type MuralSection = {
  id: string
  label: string
  group: 'background' | 'foliage' | 'catbus' | 'spirit' | 'robot' | 'butterfly' | 'sprite' | 'detail'
  defaultColorId: string
  colorId: string
  pathId: string
}
```

Color assignments should be stored by id, not by raw hex value:

```ts
export type MuralColor = {
  id: string
  label: string
  role: string
  hex: string
  ppgName?: string
  ppgCode?: string
  locked?: boolean
}
```

The app should support:

- selecting one or more sections
- assigning selected sections to a color id
- changing a color id's hex/name once and updating every section using it
- swapping two color ids globally
- restoring defaults
- exporting the assignment JSON for paint-spec work

## Kind Robots front-end requirements

Add the tool under the existing `wonder` dashboard key as a WonderLab tab/page. The current WonderLab manager already switches tabs by `activeTab`; this should become another tab rather than a one-off detached page.

Suggested front-end shape:

- Add `mural-design` to `dashboardConfigs.wonder.tabs`.
- Add a branch in `components/wonderlab/lab-manager.vue` for `activeTab === 'mural-design'`.
- Create a dedicated component such as `components/wonderlab/mural-coloring-page.vue`.
- Create a Pinia store such as `stores/muralColoringStore.ts` for palette, section selection, color assignment, swapping, import/export, and local persistence.
- Store static seed data under a public asset/data path, for example `public/data/mural-design/` and `public/images/mural-design/`.

Component interactions should go through the store. Do not call API routes directly from the front-end component. If a later version calls Kontext/generation endpoints, route that through a store action or existing art/comfy store pattern.

## Minimum useful prototype

The first PR does not need perfect segmentation. It should still be genuinely usable:

1. The WonderLab tab appears.
2. The first-draft mural reference appears.
3. A fillable overlay has a starter set of sections grouped by mural area.
4. Clicking a section selects it.
5. Clicking a color assigns that color id to the selected section(s).
6. Swapping two colors updates all affected sections.
7. The environment remains colored and visually separate from the editable fence layer.
8. The assignment JSON can be copied/exported for the final paint plan.

Perfect section tracing can follow as a refinement task. Shippable enough beats theoretical goblin architecture.