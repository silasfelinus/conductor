# Art Prompts — Conductor Project Images

Each project in Conductor has three visual assets: an **icon** (1:1), a **card** (2:3 portrait), and a **hero** (16:9 banner). These are stored in `projects/images/` and displayed automatically in the kind_robots Workspace panel.

## Generating images

1. Copy the prompt below into ChatGPT (image generation) or call the OpenAI Images API (`model: gpt-image-1`).
2. Set the aspect ratio in the generation UI — **1:1** for icon · **2:3** for card · **16:9** for hero.
3. Export as `.webp` at the minimum size listed.
4. Save to `projects/images/{slug}-{type}.webp` (e.g. `conductor-card.webp`).
5. Update `projects/art-prompts.yaml` — set `status: done` for that image.

The workspace falls back to a generic placeholder automatically when an image file is missing, so you can generate them incrementally.

## Adding art for a new project

When you create or merge a new project, add a block to **`projects/art-prompts.yaml`** following this format:

```yaml
- project: my-new-project
  icon:
    image_path: projects/images/my-new-project-icon.webp
    status: pending
    size: "256x256"
    prompt: >
      flat minimal app icon, <describe the project essence in one phrase>,
      bold clean vector shapes, square composition, no text
  card:
    image_path: projects/images/my-new-project-card.webp
    status: pending
    size: "512x768"
    prompt: >
      flat minimal portrait illustration, <main visual element centered>,
      subject on soft gradient backdrop, no text, 2:3 portrait composition
  hero:
    image_path: projects/images/my-new-project-hero.webp
    status: pending
    size: "1280x720"
    prompt: >
      flat minimal wide panoramic, <scene describing the project world>,
      cinematic scale, no text, 16:9 landscape
```

The workspace reads image paths by slug convention (`{slug}-card.webp`, `{slug}-icon.webp`, `{slug}-hero.webp`), so the filename must match the project's slug exactly.

---

## Project prompts

### conductor

**Icon** · 256×256
> flat minimal app icon, orchestral conductor robot silhouette holding a glowing baton aloft, teal and deep indigo palette, bold clean vector shapes, square composition, no text

**Card** · 512×768
> flat minimal portrait illustration, orchestral conductor robot gesturing upward directing a glowing circuit-node network, teal and deep indigo palette, subject centered with dark atmospheric backdrop, no text, 2:3 portrait composition

**Hero** · 1280×720
> flat minimal wide panoramic, orchestral conductor robot before a vast network of glowing circuit-board constellations spanning the horizon, teal and deep indigo, cinematic scale, no text, 16:9 landscape

---

### kind-robots

**Icon** · 256×256
> flat minimal app icon, friendly round purple robot face with a warm smile, mint green accent highlights, bold simplified shapes, square composition, no text

**Card** · 512×768
> flat minimal portrait of a friendly smiling purple robot giving a thumbs up, warm purple and mint green tones, rounded shapes, centered subject on soft gradient backdrop, no text, 2:3 portrait composition

**Hero** · 1280×720
> flat minimal wide scene of cheerful purple robots collaborating and waving in a bright modern workshop, warm purple and mint green, playful detail across the full frame, no text, 16:9 landscape

---

### humboldt-scoop

**Icon** · 256×256
> flat minimal app icon, vintage camera lens with a redwood tree silhouette reflected inside the glass, earthy green and warm amber, bold simplified, square composition, no text

**Card** · 512×768
> flat minimal portrait illustration of a vintage news camera centered in frame with towering redwood trees rising behind it, earthy greens and warm amber, no text, 2:3 portrait composition

**Hero** · 1280×720
> flat minimal wide panoramic of a vintage newsroom overlaid with giant California redwood forest silhouettes, warm amber light filtering through the canopy, dramatic scale, earthy greens and amber, no text, 16:9 landscape

---

### humboldt-poop-scoop-cms

**Icon** · 256×256
> flat minimal app icon, cheerful cartoon paw print centered in a soft blue rounded square, clean white background ring, bold playful style, square composition, no text

**Card** · 512×768
> flat minimal portrait illustration of a clipboard with a cheerful cartoon paw print centered on it, soft blues and white, playful rounded style, clean backdrop, no text, 2:3 portrait composition

**Hero** · 1280×720
> flat minimal wide illustration of a cheerful pet care scene: clipboard, paw prints, a happy dog and a service route map spread across a sunny neighborhood, soft blues and white, no text, 16:9 landscape

---

### approval-portal

**Icon** · 256×256
> flat minimal app icon, bold glowing green checkmark inside a dark hexagonal badge, clean professional vector, square composition, no text

**Card** · 512×768
> flat minimal portrait illustration of a sleek dark dashboard screen with a large glowing green checkmark, clean professional style, centered composition on a deep dark surface, no text, 2:3 portrait composition

**Hero** · 1280×720
> flat minimal wide cinematic dashboard panorama with multiple dark screen panels and a sweeping green approval arc across the horizon, teal accents, professional interface aesthetic, no text, 16:9 landscape

---

### digital-storefront

**Icon** · 256×256
> flat minimal app icon, shopping bag with a single bold sparkle star, warm amber and teal, clean graphic shapes, square composition, no text

**Card** · 512×768
> flat minimal portrait illustration of a shopping bag centered in frame with sparkle stars and small floating digital product icons orbiting it, warm amber and teal, no text, 2:3 portrait composition

**Hero** · 1280×720
> flat minimal wide storefront scene with a row of glowing digital product cards, floating sparkles and shopping bags arranged across a warm panoramic backdrop, amber and teal palette, inviting atmosphere, no text, 16:9 landscape

---

### brainstorm

**Icon** · 256×256
> flat minimal app icon, glowing lightbulb with a single colorful thought spark radiating upward, warm yellow and purple, bold clean graphic, square composition, no text

**Card** · 512×768
> flat minimal portrait illustration of a large glowing lightbulb centered in frame with colorful thought bubbles radiating upward and outward, bright warm yellow and purple, no text, 2:3 portrait composition

**Hero** · 1280×720
> flat minimal wide panoramic creative idea landscape: dozens of lightbulbs, floating concept bubbles, and sketch lines spreading across the horizon, bright yellow and purple, energetic and expansive, no text, 16:9 landscape

---

### mermaids-of-venice

**Icon** · 256×256
> flat minimal app icon, mermaid tail silhouette curling above a small canal wave, deep teal and warm gold, elegant bold graphic, square composition, no text

**Card** · 512×768
> flat minimal portrait illustration of a mermaid silhouette rising from a Venice canal with a gondola and arched bridge in soft focus behind her, deep blues teals and warm gold, no text, 2:3 portrait composition

**Hero** · 1280×720
> flat minimal wide panoramic of a Venice canal at golden hour with multiple mermaid silhouettes gliding among gondolas under arched bridges, warm lantern light reflected in the water, deep blues teals and warm gold, no text, 16:9 landscape

---

### coat-dance

**Icon** · 256×256
> flat minimal app icon, abstracted coat silhouette caught mid-spin, bold navy and cream with a warm gold accent arc, square composition, no text

**Card** · 512×768
> flat minimal portrait illustration of a flowing coat caught mid-spin in a dramatic upward swirl, abstract arc lines suggesting dance, navy and cream palette, tall portrait composition, no text

**Hero** · 1280×720
> flat minimal wide panoramic of a coat in full flight across an open stage, sweeping fabric arcs filling the landscape frame, abstract motion lines, navy and cream with warm gold accents, no text, 16:9 landscape
