# Arts and Crafts Movement — curriculum candidate

status: PROMOTED
project: ai-art-academy
task: t-010
lane: curriculum depth
created: 2026-07-27
promoted: 2026-07-27 (t-010, lane 4) — see curriculum-outline.md §35 and its
  "v1.15 addition" re-check paragraph. All three example works verified
  directly via the Met Collection API (`isPublicDomain: true`, matching
  accession numbers exactly). Synced into kind_robots'
  `stores/seeds/academyStyles.ts` (verified 2026-08-07, t-010 lane 2
  roadmap-accuracy pass — the "not yet synced" note above was stale).

## Why this belongs

The Arts and Crafts movement gives the Academy a lesson about design ethics rather than a single painting look. Emerging in late nineteenth-century Britain, it answered industrial mass production with visible handwork, honest materials, integrated interiors, and the idea that useful objects could also be beautiful. It connects the curriculum's Gothic, Art Nouveau, and Bauhaus entries while explaining why those movements disagree about ornament and machines.

The movement did not enforce one visual style. The lesson should therefore teach a family of cues and a design philosophy, not pretend every Arts and Crafts object looks like William Morris wallpaper.

## Proposed curriculum record

```yaml
slug: arts-and-crafts
name: Arts and Crafts Movement
era: "c. 1860-1914"
region: Britain, later international
artist_slugs:
  - william-morris
  - may-morris
  - walter-crane
  - charles-robert-ashbee
example_count: 3
remix_hint: "Redesign this image as an Arts and Crafts decorative composition: hand-drawn botanical forms, rhythmic repeating pattern, honest natural materials, flattened color, and visible craft structure rather than glossy machine-perfect finish"
negative_guidance:
  - "Do not imitate a named artist's signature or reproduce a specific Morris pattern"
  - "Avoid generic Art Nouveau poster framing, photorealistic flowers, and seamless computer-perfect repetition"
  - "Do not add industrial chrome, plastic surfaces, or minimalist Bauhaus geometry"
```

## Recognition cues

- Repeating botanical or animal motifs organized into dense, readable rhythms.
- Flat or shallow space, with outlines and simplified natural forms rather than illusionistic depth.
- Visible evidence of process: block printing, embroidery, joinery, hammered metal, woven structure, or hand-set type.
- Materials and construction treated as part of the design instead of hidden beneath surface decoration.
- Domestic-scale objects and integrated rooms: wallpaper, textiles, books, furniture, stained glass, and metalwork designed as a coherent environment.
- Medieval and vernacular references used as alternatives to anonymous industrial production.

## Historical context

The movement emerged in industrial Britain from criticism of mechanized production and divided labor. John Ruskin's writing and Gothic-revival ideas shaped its intellectual background; William Morris became its best-known designer and organizer. Morris argued for reuniting design and making, while workshops associated with Morris & Company produced wallpapers, textiles, furniture, stained glass, and books.

The social promise and the market reality should both appear in the lesson. Arts and Crafts reformers wanted dignified labor and beautiful everyday surroundings, but labor-intensive objects were often too expensive for the workers whose lives the movement hoped to improve. The lesson should present that contradiction plainly rather than turning the movement into cozy floral branding.

May Morris must be named as a designer, embroiderer, workshop leader, lecturer, and historian of her father's work—not merely as William Morris's daughter. Her leadership of the Morris & Co. embroidery workshop helps keep the lesson from collapsing a collaborative decorative-arts movement into one famous man.

## Artist boundaries

All proposed named creators died more than seventy years ago:

- William Morris (1834-1896)
- May Morris (1862-1938)
- Walter Crane (1845-1915)
- C. R. Ashbee (1863-1942)

Use their work for historical study and public-domain examples. Generation prompts should target movement-level qualities. Do not use creator names as a shortcut in user-facing remix presets, and do not imply that a generated result is an authentic design by any historical workshop.

## Institution-verified public-domain examples

1. **William Morris, _Daisy_, 1864** — block-printed wallpaper, Metropolitan Museum of Art, object 23.163.4b. The Met marks the image Public Domain and provides an open-access download.
   - https://www.metmuseum.org/art/collection/search/384017
2. **William Morris, _Wild Tulip_, 1884** — block-printed wallpaper, Metropolitan Museum of Art, object 23.163.4f. The Met marks the image Public Domain and identifies its hand-blocked repeating floral design as typical of Morris's later work.
   - https://www.metmuseum.org/art/collection/search/375808
3. **Morris & Company, _Five pink flowers with foliated tendrils_, last quarter of the nineteenth century** — silk embroidery on linen, Metropolitan Museum of Art, object 2021.7.4. The Met marks the image Public Domain and describes the embroidery workshop under May Morris's leadership.
   - https://www.metmuseum.org/art/collection/search/760427

## Remix exercise

Use one ordinary interior photograph or still life for two passes:

1. **Pattern pass:** flatten the subject into a repeatable botanical or animal motif while preserving its main silhouette.
2. **Object pass:** redesign the same subject as a crafted household object whose joinery, weave, print blocks, or hammered surface remain visible.

Compare whether the result communicates hand process and material structure. A merely floral image is not enough; a successful result should make the method of making legible.

## Common generation failures

- Producing a direct copy or near-copy of a famous Morris wallpaper.
- Treating Arts and Crafts as interchangeable with Art Nouveau.
- Rendering realistic flowers over a generic luxury interior.
- Making the repeat perfectly seamless and digitally sterile, erasing the hand-process cue.
- Using medieval motifs as fantasy-costume decoration without the movement's labor and material context.
- Omitting May Morris and the collaborative workshop structure.

## Representation and promotion review

Before promotion:

- Confirm that May Morris receives an independent biographical note and is not reduced to family relationship.
- Explain the movement's labor-reform goals and the affordability contradiction.
- Distinguish British origins from later American and international Arts and Crafts developments; do not flatten them into one national style.
- Keep Gothic and non-European source traditions in historical context rather than presenting them as a decorative grab bag.
- Verify every displayed object at its institution page and store object-level rights metadata in the starter/example manifest.
- Confirm no protected artist name appears in remix presets, prompt templates, or marketing copy.

## Definition of done for promotion

- Add the movement to `curriculum-outline.md` and the machine-readable skeleton.
- Add a matching front-end seed entry in `kind_robots` with movement-level prompt wording.
- Download at least three verified public-domain examples and record source, accession number, creator attribution, date, and rights statement.
- Add a prompt-mode remix config and test it against the Academy's fixed reference image.
- Run the Academy curriculum candidate guard and the example-manifest contract.
