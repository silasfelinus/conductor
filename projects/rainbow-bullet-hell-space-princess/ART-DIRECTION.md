# Visual production bible: candy-colored cosmic deep sea

## Non-negotiable look

Polished hand-painted 2.5D space opera: candy pink, lilac, peach, powder cyan, soft butter-yellow and opalescent turquoise with rich deep navy negative space. Premium animation on gently iridescent metal and translucent jellyfish glass. Everything glows, floats and refracts, yet the world stays friendly and readable. **The world is soft; the combat is precise.** Aim for richly composed high-definition illustrations, not a coarse early-80s arcade reskin.

## Ship families

Four player princess ships, each unique in outline: **Petal Wing** (rose-gold swallowtail, spread), **Prism Lance** (long needle fin, piercing beam), **Halo Fin** (round ringed nacelles, defense drones), **Comet Crown** (triangular three-prong geometry, charge). Names describe ships, not preselected human appearance. Princess characters are original and have agency; cutscene portraits need continuity across all frames.

Enemy ship shape grammar: seahorse coil and upright prow with glowing thruster tail; jellyfish translucent lenticular hull and electric tentacle antennae; mantis-shrimp articulated forward punch cannons; shark wedge wedge-nose strike craft; dolphin paired curvilinear fast hulls; manta flat enormous ship-carriers; ray and whale capital bosses occupy believable silhouettes and leave battle-lane gaps.

## Art delivery plan

1. Production sheet: primary four ships side/top views, three animation poses and color-coded player ID glyphs.
2. Enemy catalog: 8 families × 3 evolutions, clean gameplay silhouette at 64–128 CSS pixels, separate boss multi-layer atlases and collision envelopes.
3. Stage plates: deep static color background; slow far plane; near/environment plane; foreground atmospheric layer, each independently parallaxed. Combat foreground *never* hides bullets.
4. Effects atlas: bright but uniquely shaped friendly shots, crisp-edged dangerous enemy orbs, shield contours, warning ribbons, powerup beacons, controlled supers, explosions.
5. Cinema: 12–20 storyboard frames for intro, three stage interludes and route endings; localized/subtitled text drawn by UI instead of baked into image.
6. Music/sound cues: distinct boss escalation, warning charge, shield impact, pickup feedback, big wave-sweep super and victory. Only own or properly licensed material.

## Contrast and accessibility

Enemy bullets get a dark stroke and high-contrast saturated center; friendly bullets have a different shape and motion class. Never rely on hue alone. Set hard maximum for bloom, screen shake and projectile opacity. Reduced-motion and high-contrast bullet modes are required. At four players verify distinction in grayscale and crowded boss phase; if a shot is unreadable, fix that before adding particles.

## Reproducible generation

Use Conductor art queue → durable Kind Robots ArtJobs → rendered ArtImage → verified delivered URL, with project slug, aspect ratio, engine, prompt, seed, intended sprite sheet/layer and rights provenance. Image generations are inspiration until the actual game atlas is cropped, keyed, animated and tested on a real scrolling scene. No paid generation without explicit authorization.
