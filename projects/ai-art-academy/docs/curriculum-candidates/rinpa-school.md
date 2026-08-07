# Curriculum candidate: Rinpa school

**Proposed slug:** `rinpa-school`  
**Era:** early 1600s–mid-1800s, Japan  
**Status: PROMOTED 2026-08-06 (ai-art-academy/t-010, lane 4).** Landed in
`curriculum-outline.md` §46, v1.26. Three of this file's four cited Met
example works were re-verified live and confirmed `isPublicDomain: true`;
the fourth (object 748253, a Kiitsu/Yamamoto Sodō joint work) returned
`isPublicDomain: false` on re-check and was replaced in the promoted
section with a solely-Kiitsu-authored, confirmed-public-domain substitute
(*Irises and Moth*, object 53424) found via the same API rather than
assumed from this file. Kept here as the source research for the promoted
entry; synced into kind_robots' `stores/seeds/academyStyles.ts` (verified
2026-08-07, t-010 lane 2 roadmap-accuracy pass — the "not yet synced" note
above was stale).

## Why this earns a separate lesson

Rinpa is not another Ukiyo-e lesson. Ukiyo-e is primarily a print culture built around actors, courtesans, travel, city life, and reproducible woodblock color. Rinpa is a decorative painting and design tradition built around folding screens, hanging scrolls, fans, lacquer, ceramics, and textiles. Its teaching value is the collision of extreme flatness with close natural observation: flowers, grasses, water, trees, and seasonal motifs become bold arrangements of silhouette, rhythm, empty space, mineral color, ink, and gold or silver ground.

The lesson also gives the Academy a useful example of a tradition transmitted through admiration and deliberate revival rather than a single continuous workshop lineage. Ogata Kōrin looked back to earlier decorative masters; Sakai Hōitsu later codified and renewed Kōrin's vocabulary in Edo; Suzuki Kiitsu carried that revival into a sharper nineteenth-century form.

## Recognition cues

- Large gold- or silver-leaf grounds that remove ordinary landscape depth
- Asymmetrical compositions with major motifs cropped by the edge or folding-screen seam
- Broad, simplified silhouettes paired with a few sharply observed botanical details
- Repeated flowers, leaves, waves, or grasses arranged as visual rhythm rather than naturalistic space
- Pools of wet ink and color allowed to bloom into soft-edged forms, often beside crisp contour or metallic ground
- Strong use of empty space, with subjects floating against an unmodeled field
- Seasonal and literary nature motifs rather than urban genre scenes
- Decorative surface logic that can move between painting, lacquer, ceramics, fans, and textiles

## Artists for historical study

### Ogata Kōrin

Ogata Kōrin (1658–1716) is the central namesake figure. The Metropolitan Museum of Art describes *Flowers of Spring and Autumn* as combining highly stylized natural elements with Chinese-style ink training.

Rights boundary: Kōrin died in 1716 and clears the Academy's conservative death-date threshold. Display still requires an item-level museum rights statement; generation may use his name only while the current public-domain policy continues to permit dead-artist anchors this old.

### Sakai Hōitsu

Sakai Hōitsu (1761–1828) led the Edo Rinpa revival. The Met identifies him as one of the most important late-Edo Rinpa painters and documents his seasonal, literary compositions.

Rights boundary: Hōitsu died in 1828 and clears the death-date threshold. Verify each displayed object and digital image independently before front-end use.

### Suzuki Kiitsu

Suzuki Kiitsu (1796–1858), Hōitsu's leading pupil, is useful for the movement's later crisp, dramatic botanical forms.

Rights boundary: Kiitsu died in 1858. His works are old enough for movement-level historical study, but displayed examples still require item-level rights verification; do not infer image rights from artist death date alone.

## Verified example works

1. **Ogata Kōrin, _Flowers of Spring and Autumn_, shortly after 1701**  
   Metropolitan Museum of Art, object 53421. Pair of panels in ink and color on cryptomeria wood. The Met notes the work's highly stylized natural forms and identifies Kōrin's signature and seal.  
   https://www.metmuseum.org/art/collection/search/53421

2. **Sakai Hōitsu, _Activities of the Twelve Months_, late 1790s**  
   Metropolitan Museum of Art, object 752036. Eleven hanging scrolls using court ritual, seasonal customs, flowers, foliage, and a full moon; the Met identifies Hōitsu as a major late-Edo Rinpa painter.  
   https://www.metmuseum.org/art/collection/search/752036

3. **Sakai Hōitsu, _Cherry and Maple Trees_, early 1820s**  
   Metropolitan Museum of Art, object 765976. Pair of six-panel screens in ink, color, and gold leaf, organized around spring and autumn plants with strong decorative impact.  
   https://www.metmuseum.org/art/collection/search/765976

4. **Suzuki Kiitsu and Yamamoto Sodō, _Mount Fuji and flowering plants_, Edo period**  
   Metropolitan Museum of Art, object 748253. Mounted painting pairing Kiitsu's Mount Fuji with autumn flowers by another Hōitsu pupil; the Met records Kiitsu as Hōitsu's prolific and highly regarded student.  
   https://www.metmuseum.org/art/collection/search/748253

## Public-domain and generation policy

This candidate is suitable for movement-level curriculum and testing. Promotion must preserve the distinction between artwork copyright, object-record availability, and the rights attached to a museum's digital image.

For display:

1. Perform item-level review for each work and digital image.
2. Record creator, title, date, collection, object URL, and the institution's explicit image-rights statement.
3. Prefer downloadable museum images marked Public Domain or CC0.
4. Treat an old artwork with unclear digital-image terms as metadata-only until rights are confirmed.
5. Do not hotlink an image merely because the object page is public.

For generation:

- prefer the movement-level prompt below;
- protect uploaded subject identity and major composition;
- use Kōrin, Hōitsu, or Kiitsu only as historically eligible anchors under the current policy;
- do not include protected artist names, modern Rinpa-inspired artists, contemporary brands, or living illustrators;
- avoid turning Japanese identity into costume, calligraphy garnish, or generic "Zen" atmosphere.

## Movement-level remix configuration

```yaml
slug: rinpa-school
mode: prompt
label: Rinpa School
instruction: >-
  Repaint the source as a Rinpa-school folding-screen composition: a broad gold-
  or silver-leaf ground with no ordinary horizon, an asymmetrical cropped arrangement
  of seasonal flowers, grasses, trees, or water, bold simplified silhouettes mixed
  with a few precise botanical details, pooled ink-and-color edges, rhythmic repetition,
  generous empty space, and an elegant decorative surface rather than realistic depth.
negative_guidance:
  - woodblock-print outlines
  - actor portraits or urban street scenes
  - photographic depth or cast shadows
  - atmospheric landscape recession
  - dense all-over detail
  - generic Japanese watercolor shorthand
  - invented calligraphy or identity costume
preserve:
  - subject identity
  - major composition
  - intended emotional register
```

## Try It — one subject, three surfaces

Use one simple source containing a branch, flower, animal, or household object. Keep its identity and placement fixed while testing three Rinpa surface decisions:

1. Gold ground with broad cropped silhouettes.
2. Silver ground with pooled ink and larger empty areas.
3. Plain paper with rhythmic repeated seasonal motifs.

A successful comparison should change decorative structure and spatial logic, not merely recolor the source.

## Common generation failures

### Ukiyo-e drift

Symptoms: heavy black print outlines, flat commercial-print color, cartouches, actors, or street scenes.

Correction: specify folding screen, metallic ground, pooled ink, botanical rhythm, and empty space.

### Generic botanical illustration

Symptoms: centered specimen, white background, evenly described leaves, no asymmetry or decorative rhythm.

Correction: crop the motif, introduce metallic ground, repeat forms selectively, and remove ordinary depth.

### Gold wallpaper

Symptoms: realistic subject pasted over a gold texture with no compositional transformation.

Correction: flatten the forms, rebuild the negative space, and make repetition and cropping carry the composition.

## Promotion checklist

Before this candidate becomes a front-end Academy style:

- [x] Distinct from an existing curriculum movement.
- [x] At least three dead-artist generation anchors.
- [x] At least three institution-hosted example records.
- [x] Recognition cues and remix prompt are concrete enough to test.
- [x] Public-domain-policy death-date threshold is satisfied.
- [x] Rights verification records artwork and digital-image status for every displayed example (all four via the Met Collection API's `isPublicDomain` field, live-checked 2026-08-06).
- [ ] Representation review confirms the lesson distinguishes Rinpa from generic Japanese visual shorthand.
- [x] No protected artist name appears in the generation instruction.
- [ ] The movement-level prompt is tested for Ukiyo-e drift and subject-identity loss.
- [x] Mirror the approved lesson into `docs/curriculum-outline.md` (§46, v1.26).
- [ ] Add a matching front-end seed entry and preview request in a later scoped cycle.
