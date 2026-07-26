# Hudson River School curriculum module

status: PROMOTED 2026-07-26 — curriculum-outline.md v1.12, section 32
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

## Notable artists

- **Thomas Cole** (1801-1848) — Founder of the movement, combining observed American scenery with allegory, historical cycles, and warnings about unchecked development.
- **Frederic Edwin Church** (1826-1900) — Cole’s pupil, known for enormous, scientifically detailed landscapes assembled from travel studies and displayed as public spectacles.
- **Albert Bierstadt** (1830-1902) — Painter of monumental western landscapes whose theatrical light and scale helped shape popular ideas of the American West.

All three artists died well before the Academy’s conservative 1956 death-year cutoff.

## Example works

### The Oxbow

- Artist: Thomas Cole
- Date: 1836
- Collection: Metropolitan Museum of Art
- Public-domain rationale: artist died 1848; work published well before 1931
- Source target: Wikimedia Commons or Met Open Access
- Verification status: source page still needs a final acquisition-time license check

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
```

## Teaching beats

### Try it

Ask learners to identify the darkest foreground mass, the brightest distant opening, and the smallest scale-setting human or architectural element. Then remix a landscape or outdoor photograph while preserving those three structural roles.

### Reflect

1. How does the painting use light to suggest spiritual or national meaning?
2. What evidence of human presence is included, minimized, or erased?
3. How would the same land look if the lesson foregrounded Indigenous history instead of Manifest Destiny?

## Integration checklist

- Add the movement to `docs/curriculum-outline.md` and its machine-readable skeleton.
- Add a prompt-mode row to `docs/style-lora-registry.md`.
- Add the Try-It / Reflect row to `docs/teaching-notes.md`.
- Queue `kind-robots-academy-style-preview-hudson-river-school` in `projects/art-prompts.yaml`.
- Mirror the entry into `kind_robots/stores/seeds/academyStyles.ts` in a later cross-repo task.
- Verify *The Oxbow* against an official open-access or Wikimedia source before acquiring an image.
