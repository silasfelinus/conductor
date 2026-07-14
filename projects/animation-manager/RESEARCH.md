# Animation Research Baseline

## Browser primitives

### `requestAnimationFrame`

Use the callback timestamp for movement. Browser refresh rates vary, and timestamp-based motion avoids effects running faster on 120 Hz or 144 Hz displays. Browsers also pause most animation-frame callbacks in background tabs, which is preferable for battery and heat.

Primary reference: https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame

### `ResizeObserver`

Effects can render full-screen or inside clipped header, sheet, page, and hand regions. Observe the actual canvas or containing surface rather than assuming viewport dimensions.

Primary reference: https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver

### Canvas performance

Keep the drawing surface aligned with CSS size, cap device-pixel ratio, minimize state churn, and avoid unnecessary full-scene complexity. Transparent effects should clear only their own canvas and should not create opaque page-sized backgrounds.

Primary reference: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas

### Reduced motion

`prefers-reduced-motion` is part of the product contract, not a final CSS patch. Each pitch states how motion, density, contrast, and interaction change when reduction is requested.

Primary reference: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion

## Creative reference families

These are technique families, not instructions to reproduce a branded screensaver:

- particle ecosystems with individual behaviors instead of uniform confetti
- reaction-diffusion, cellular automata, boids, and flow fields
- translucent paper, glass, ink, sand, smoke, and caustic-light simulations
- impossible architecture and slow parallax worlds
- biological rhythms: jellyfish, moths, koi, spores, roots, coral, plankton
- environmental cycles: weather fronts, tide pools, cloud cities, auroras, eclipses
- nostalgic screensaver grammar transformed into original Kind Robots behavior
- quiet surprises that emerge only after time: rare visitors, pattern convergence, hidden messages, seasonal mutations

## Quality heuristics

A strong opening wallpaper has three timescales:

1. **Immediate read:** the screen looks intentionally alive within one second.
2. **Loop character:** movement has a recognizable rhythm within ten seconds.
3. **Long surprise:** something uncommon or emergent can happen after thirty seconds or more.

A weak animation usually fails because it is merely a particle emitter, repeats too obviously, muddies the interface, requires interaction to become interesting, or spends too much CPU on visual noise.

## Performance budget

Default target for one full-screen effect on a modern desktop:

- one canvas unless the technique clearly benefits from layers
- device-pixel ratio capped at 2
- approximately 20–60 major moving entities, scaled by area
- delta time bounded after tab suspension
- no per-frame DOM creation
- no synchronous network or storage work in the render loop
- no uncancelled RAF, timers, observers, or listeners after unmount
- reduced-motion mode uses materially fewer entities and slower motion

Mobile and low-power devices may need lower counts through area scaling or explicit capability checks. A beautiful laptop fan is still a fan, not a feature.

## Optional interaction rule

Preferred optional interaction listens without taking ownership of the page:

- observe pointer movement or clicks at `window`
- never call `preventDefault` or `stopPropagation`
- keep the visual canvas `pointer-events: none`
- treat interaction as a temporary perturbation of an already-complete passive loop

Effects that truly require captured input may set `blocksInput: true`, but they are Screen FX-only and excluded from random startup wallpaper selection.

## First build rationale: Bioluminescent Tide

Bioluminescent Tide was selected first because it proves the full contract with no external assets:

- passive drifting lantern organisms and tide bands
- cursor movement creates a subtle wake
- clicks create additive ripples while the original click continues normally
- transparent canvas works over themes and layouts
- area-aware particle count and ResizeObserver support clipped regions
- device-pixel ratio cap and bounded delta protect performance
- reduced-motion mode lowers count, speed, and opacity
- all resources are cleaned up on unmount

It also differs clearly from the existing bubbles, fireflies, ripple, constellation, and aquarium effects: it combines a living ecosystem, fluid bands, and non-blocking interaction rather than duplicating one of those mechanisms.
