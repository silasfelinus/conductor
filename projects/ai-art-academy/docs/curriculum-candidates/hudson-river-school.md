# Hudson River School curriculum module

**Status: PROMOTED 2026-07-26** — now curriculum-outline.md §32
(`hudson-river-school`), v1.12. Kept here as the source research for the
promoted entry.

movement_slug: hudson-river-school
era: c. 1825-1875
region: United States
remix_mode: prompt

## Why this belongs in the Academy

The Hudson River School adds a major nineteenth-century landscape tradition that is visually distinct from Romanticism, Realism, American Regionalism, and Song Dynasty landscape painting. Its signature is not merely “dramatic nature”: it combines panoramic scale, precise botanical and geological detail, theatrical light, deep atmospheric distance, and tiny human figures that turn the landscape into a moral or spiritual stage.

The lesson should also address the movement’s cultural framing honestly. These paintings often present American land as sublime, abundant, and apparently unoccupied. That visual language overlaps with Manifest Destiny and can erase Indigenous presence and displacement. The Academy should teach the beauty and technique without treating the ideology as neutral scenery.

## Recognition cues

- Panoramic wilderness compositions with a high horizon and enormous depth
- Luminous, often golden light breaking through clouds or mist
- Meticulously rendered trees, rocks, water, and distant terrain
- Tiny people, buildings, boats, or animals used mainly to establish scale
- A staged progression from shadowed foreground to glowing distance
- Calm reflective water or a dramatic weather break used as a compositional hinge
- Nature presented as sublime, spiritual, national, or morally instructive

## Artists for historical study

- **Thomas Cole** (1801-1848) — Founder of the movement, combining observed American scenery with allegory, historical cycles, and warnings about unchecked development.
- **Frederic Edwin Church** (1826-1900) — Cole’s pupil, known for enormous, scientifically detailed landscapes assembled from travel studies and displayed as public spectacles.
- **Albert Bierstadt** (1830-1902) — Painter of monumental western landscapes whose theatrical light and scale helped shape popular ideas of the American West.

All three artists died well before the Academy’s conservative 1956 death-year cutoff.

Rights boundary: Cole, Church, and Bierstadt each died more than 100 years ago
(1848, 1900, 1902), so their paintings are in the public domain in the United
States and in life+70 jurisdictions — unlike this project's copyright-sensitive
candidates (e.g. Precisionism's Sheeler/Crawford), no living-artist or
recently-deceased-artist boundary applies here. The remaining rights question is
per-*reproduction*, not per-artist: verify each displayed image's specific
digital source (museum open-access grant, Wikimedia Commons license tag) rather
than assuming the artist's death date alone clears a particular photograph or
scan for use.

## Example works

### The Oxbow

- Artist: Thomas Cole
- Date: 1836
- Collection: Metropolitan Museum of Art, accession 08.228
- Public-domain rationale: artist died 1848; work published well before 1931
- Verified source: https://commons.wikimedia.org/wiki/File:Thomas_Cole_-_View_from_Mount_Holyoke,_Northampton,_Massachusetts,_after_a_Thunderstorm-The_Oxbow.jpg
- License signal: Public Domain Mark 1.0 and PD-Art (PD-old-auto-expired)

### The Heart of the Andes

- Artist: Frederic Edwin Church
- Date: 1859
- Collection: Metropolitan Museum of Art, accession 09.95
- Public-domain rationale: artist died 1900; work published before 1931
- Verified source: https://commons.wikimedia.org/wiki/File:Frederic_Edwin_Church_-_The_Heart_of_the_Andes.jpg
- License signal: Public Domain Mark; faithful reproduction of a public-domain two-dimensional work

### Among the Sierra Nevada, California

- Artist: Albert Bierstadt
- Date: 1868
- Collection: Smithsonian American Art Museum
- Public-domain rationale: artist died 1902; work published before 1931
- Verified source: https://commons.wikimedia.org/wiki/File:Albert_Bierstadt_-_Among_the_Sierra_Nevada,_California_-_Google_Art_Project.jpg
- License signal: Public Domain Mark; author died more than 100 years ago

## Public-domain and generation policy

For displayed examples:

1. Verify each specific artwork's publication and copyright status (all three
   named artists died well before the Academy's 1956 cutoff, so the artwork
   itself is not in question).
2. Verify the digital image or photograph separately — item-level, per
   reproduction, not inferred from the artist's death date.
3. Prefer museum or archive records with an explicit open-access statement, or
   a Wikimedia Commons file page carrying an unambiguous public-domain tag.
4. Record creator, title, date, collection, source URL, and rights statement
   for each work.

For generation:

- Use movement-level instructions; exclude artist names (Cole, Church,
  Bierstadt) from end-user-facing generation presets — teach them as
  historical context, not as an imitation shortcut.
- Do not prompt for or accept an "empty wilderness" framing that erases
  Indigenous presence as historical fact — the lesson's own Reflect prompts
  exist to surface this, and generation copy should avoid presenting the
  Manifest Destiny framing as neutral or celebratory.
- Do not reduce the movement to a generic "pretty nature" or fantasy-landscape
  filter; avoid magical, futuristic, or storybook elements that erase the
  movement's specific 19th-century American geography and ideology.

## Remix configuration

```yaml
slug: hudson-river-school
name: Hudson River School
era: "c. 1825-1875"
artist_slugs: [thomas-cole, frederic-edwin-church, albert-bierstadt]
example_count: 3
remix:
  mode: prompt
  template: >-
    Repaint this image as a Hudson River School landscape: panoramic wilderness,
    meticulous natural detail, deep atmospheric distance, tiny figures for scale,
    a shadowed foreground opening toward luminous golden light, reflective water,
    dramatic clouds, and a sublime theatrical sense of nature.
  failure_mode: >-
    The model may produce a generic fantasy landscape or oversaturated wallpaper.
    Preserve believable geology and vegetation, keep human figures subordinate,
    and use light to structure depth rather than adding magical objects.
  negative_guidance:
    - named-artist imitation (Cole/Church/Bierstadt signature copying)
    - fantasy or sci-fi landscape elements
    - oversaturated "digital wallpaper" color
    - triumphalist or celebratory Manifest Destiny framing
    - erasing all human/Indigenous presence as if the land were empty by nature
```

## Teaching beats

### Try it

Ask learners to identify the darkest foreground mass, the brightest distant opening, and the smallest scale-setting human or architectural element. Then remix a landscape or outdoor photograph while preserving those three structural roles.

### Reflect

1. How does the painting use light to suggest spiritual or national meaning?
2. What evidence of human presence is included, minimized, or erased?
3. How would the same land look if the lesson foregrounded Indigenous history instead of Manifest Destiny?

## Promotion checklist

Before this candidate becomes a front-end Academy style:

- [x] At least three display examples have explicit, item-level reusable rights (Met accession 08.228, Met accession 09.95, Smithsonian American Art Museum — all Public Domain Mark / PD-Art on Wikimedia Commons).
- [x] Example metadata records both artwork and image rights (see Example works above).
- [x] No protected artist name appears in the generation instruction (`remix.template` names no artist; the movement-level prompt only).
- [ ] A cultural-history reviewer checks the Manifest Destiny/Indigenous-erasure framing and Reflect prompts before this ships to end users (soft gate — not a rights blocker, but a representation-quality one).
- [ ] The movement-level prompt is tested for the two-sided over-cook/under-cook failure mode noted in `curriculum-outline.md`'s "Good but watch the output" tier.
- [x] The lesson's Reflect prompts explicitly ask what the image includes, minimizes, or erases about human/Indigenous presence, not just aesthetic questions.

## Integration checklist

- [x] Add the movement to `docs/curriculum-outline.md` and its machine-readable skeleton (§32, v1.12).
- [x] Add a prompt-mode row to `docs/style-lora-registry.md`.
- [x] Add the Try-It / Reflect row to `docs/teaching-notes.md` (row 32).
- [x] Queue `kind-robots-academy-style-preview-hudson-river-school` in `projects/art-prompts.yaml`.
- [ ] Mirror the entry into `kind_robots/stores/seeds/academyStyles.ts` in a later cross-repo task.
- [x] Verify *The Oxbow* against an official Wikimedia source before acquiring an image (Met accession 08.228, Public Domain Mark + PD-Art).
