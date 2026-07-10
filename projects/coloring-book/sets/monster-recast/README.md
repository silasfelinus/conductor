# Monster Recast

slug: `monster-recast`
status: design-ready
book-format: physical + digital coloring book
content-rating: all-ages spooky

## The concept

**Monster Recast** is a gallery of original movie-monster royalty: classic horror and science-fiction archetypes reimagined through gender swap, drag performance, queer theatricality, and old-Hollywood spectacle.

The cast begins with recognizable genre lineages — vampire, stitched corpse, werewolf, mummy, lagoon creature, invisible illusionist, opera phantom, alien terror, masked slasher, giant creature, haunted doll, and more — but every design must become its own character before art generation. The goal is affectionate genre conversation, not near-copy parody.

The name works on three levels: movie casting, gender recasting, and recasting familiar monster ingredients into a new shared universe.

## V1 book shape

Target a **28-page illustrated interior**, not counting title, credits, test-swatch, or blank backing pages:

- 24 solo character pages
- 2 duo pages
- 1 cosmic trio page
- 1 full-cast premiere page
- 1 separate full-color cover illustration

This is large enough to feel like a real physical coloring book while keeping the first production pass finite. One illustration should sit on each right-hand page in print so marker bleed does not ruin another drawing.

## Production sequence

1. **Design** — lock names, bios, silhouettes, wardrobe, visual motifs, concept prompts, and copyright-distance notes.
2. **Concept art** — generate several full-color candidates per character across varied art traditions and cinema-era visual languages.
3. **Selection** — choose the strongest, most original design for each character and revise obvious echoes of protected characters.
4. **Character creation** — create a Kind Robots `Character` entry for every selected cast member, attach the chosen image, and preserve the final prompt.
5. **Coloring conversion** — convert selected art into clean black line work with closed, colorable regions and simplified backgrounds.
6. **Book assembly** — build the digital set manifest, print-ready interiors, cover, credits, and storefront-ready package.
7. **Pause** — once the set and Character entries are complete, hold publishing and POD setup until the coloring app and digital storefront are ready.

## Originality guardrails

Every piece should evoke an **archetype**, never reproduce a protected character.

- Do not use franchise character names, actor likenesses, studio logos, signature costumes, exact masks, exact makeup, exact weapons, or famous scene compositions.
- Change at least five major anchors from any obvious inspiration: silhouette, face, body plan, clothing era, color language, setting, prop, origin, personality, and movement.
- Prefer public-domain and folkloric roots where available: vampires, werewolves, mummies, ghosts, witches, golems, giant beasts, revenants, demons, and headless riders.
- Later-cinema archetypes such as dream killers, biomechanical aliens, masked slashers, killer dolls, shark terrors, and mischievous creatures must be especially transformed.
- Art prompts may describe broad periods, media, and public-domain movements. They should not request imitation of a living artist or a copyrighted studio style.
- No gore is required. Macabre details should read as theatrical, spooky, funny, glamorous, and colorable.

## Visual direction

The collection should feel curated rather than uniform. Concept art deliberately ranges across:

- Gothic portraiture and Art Nouveau poster work
- German Expressionist stage design
- 1950s pulp science fiction and creature-feature color
- 1960s fashion photography and beach-poster graphics
- 1970s airbrush fantasy, occult screen print, and glam rock
- 1980s practical-effects spectacle and neon video-store posters
- Victorian engraving, botanical plates, and entomology illustration
- woodblock-inspired monster prints, linocut, paper-cut theatre, watercolor, risograph, and stop-motion maquettes

The final coloring pages should unify these sources through bold black contours, mostly closed regions, clean white space, printable detail, and no gray shading.

## Character data

`characters.yaml` is shaped around the current Kind Robots `Character` fields where practical: `name`, `slug`, `gender`, `presentation`, `role`, `title`, `species`, `class`, `genre`, `alignment`, `backstory`, `drive`, `quirks`, `personality`, `artPrompt`, `imagePath`, `designer`, `isPublic`, `isMature`, and `isActive`.

These are seed records, not production database writes. The later Character-import task should verify the current API and enum requirements, create records privately, attach approved art, and only make them public when the book is ready.

## Files

- `characters.yaml` — 24 original cast members, bios, design anchors, and full-color concept prompts
- `pages.yaml` — cover plus the 28-page interior plan, including conversion prompts
- `README.md` — product shape, workflow, and originality rules
