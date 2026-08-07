# The Nabis — Curriculum Candidate

academy-cultural-context: required

**Status: PROMOTED 2026-07-26** — now curriculum-outline.md §31 (`the-nabis`),
v1.11. Three institution-verified public-domain example works (Musée d'Orsay,
National Gallery of Art) satisfy this file's own "definition of done" below.
Kept here as the source research for the promoted entry; synced into
kind_robots' `stores/seeds/academyStyles.ts` (verified 2026-08-07, t-010
lane 2 roadmap-accuracy pass — the "not yet synced" note above was stale).

## Why this belongs in the Academy

The Nabis were a loose group of young artists working mainly in Paris during the 1890s. Their name comes from the Hebrew word for “prophets,” reflecting their belief that painting could move beyond literal description and become a deliberately designed surface of color, pattern, rhythm, and feeling.

This module is useful because it bridges several better-known movements. The Nabis absorbed the flattened space and strong contours of Japanese prints, carried forward lessons from Gauguin and Symbolism, and helped prepare the way for modern illustration, decorative design, and color-first painting.

## Recognition cues

Look for several of these traits together:

- Flattened or shallow space rather than convincing Renaissance depth
- Large interlocking areas of color
- Strong outlines or contour-like edges
- Wallpaper, textiles, screens, and domestic patterns treated as major visual structure
- Cropped viewpoints that feel influenced by photography or Japanese prints
- Quiet interiors, gardens, theater scenes, and intimate everyday moments
- Figures simplified into silhouettes or rhythmic shapes
- A mood that matters more than anatomical or spatial realism

A useful diagnostic question is: **Does the picture behave like a window into a room, or like a carefully arranged decorated surface?** Nabis work often leans toward the second.

## Historical frame

The group formed around 1888–1889 among students connected to the Académie Julian in Paris. Paul Sérusier’s small painting *The Talisman*, made after advice from Paul Gauguin, became a touchstone: instead of copying the landscape literally, Sérusier organized the scene as patches of emotionally chosen color.

The Nabis were not stylistically identical. Some leaned toward mysticism and Symbolism, while others focused on modern domestic life, theater, posters, book illustration, folding screens, and decorative panels. They rejected the idea that easel painting stood above the so-called decorative arts.

## Artists

**Rights boundary:** These artists are included for historical study. Generation guidance must describe movement-level visual decisions rather than invoking their names, and every displayed work still requires item-level rights verification.

### Paul Sérusier (1864–1927)

Use Sérusier to introduce the movement’s color-first theory and the shift from observed landscape to designed color relationships. Emphasize *The Talisman* as an instructional turning point rather than treating one tiny painting as the whole movement.

### Édouard Vuillard (1868–1940)

Vuillard is especially useful for teaching pattern, compressed interiors, and figures that nearly dissolve into wallpaper, clothing, and furnishings. His work can help students notice how a room’s decorative surfaces can carry narrative and emotion.

### Pierre Bonnard (1867–1947)

Bonnard connects the Nabis to later explorations of luminous color, memory, domestic space, and unusual cropping. Keep this module focused on his earlier Nabis context rather than flattening his long career into one label.

### Maurice Denis (1870–1943)

Denis provides the clearest theoretical entry point. His famous argument that a painting is first a flat surface covered with colors can be paraphrased for students as: before a painting depicts a person, horse, or story, it is an arrangement of shapes and colors.

## Public-domain and generation policy

All named artists died more than seventy years ago, but each work still receives item-level review. Use only specific artwork whose rights status is confirmed by the source institution or repository. Prefer open-access museum downloads and clearly marked public-domain reproductions.

Do not include artist names in remix presets or generation prompts. Do not use later artists merely described as “Nabis-inspired” as style references. The teaching target is the historical movement, not imitation of living illustrators or contemporary decorative painters.

Negative generation guidance should prevent caricature and shortcut aesthetics: avoid generic retro-poster output, copied compositions, modern typography, and reducing Japanese visual traditions to exotic decoration.

## Movement-level remix configuration

**Recommended mode:** prompt-first historical movement study

The movement is better represented through compositional and decorative instructions than through one artist-name trigger. A movement-level prompt also reduces the risk of producing a shallow imitation of one signature painter.

```yaml
slug: the-nabis
prompt_guidance:
  - flatten depth into interlocking color shapes
  - simplify figures into rhythmic silhouettes
  - use contour edges and decorative surface rhythm
  - let textiles, wallpaper, foliage, or architecture organize the composition
negative_guidance:
  - no named-artist imitation
  - no copied historical composition
  - no modern typography or generic vector-poster treatment
  - no exoticizing Japanese motifs
```

### Prompt template

> Reinterpret the source image as a late-1890s Nabis decorative painting. Preserve the main subjects, but flatten the depth into interlocking color shapes, simplify figures into rhythmic silhouettes, use strong contour edges, and let textiles, wallpaper, foliage, or architectural patterns organize the composition. Favor intimate mood and designed surface rhythm over photographic realism. Avoid modern graphic-design typography and avoid copying any single painting.

### Adjustable controls

- **Pattern intensity:** restrained / balanced / immersive
- **Depth:** shallow / very flat
- **Contour strength:** soft / clear / poster-like
- **Palette:** muted domestic / jewel-toned / warm garden
- **Subject preservation:** high / interpretive

## Failure modes

- **Generic “vintage poster” output:** The model may substitute modern retro graphic design. Reinforce painted surface, domestic pattern, and no typography.
- **Gauguin pastiche:** The movement’s influences can overwhelm its own identity. Ask for intimate interiors, decorative panels, or theater scenes rather than tropical Symbolist imagery.
- **Pattern wallpaper pasted behind realistic figures:** Require the figures and environment to share the same flattened shape language.
- **Total loss of subject:** Heavy flattening can erase the source image. Raise subject preservation and reduce pattern intensity.
- **One-artist caricature:** Avoid using only “in the style of Bonnard” or “in the style of Vuillard.” Describe movement-level visual decisions.

## Try It

### Exercise 1 — The decorated room

Choose a photo with one or two people in an interior. Remix it with balanced pattern intensity and shallow depth. Compare the original and result:

- Which objects became pattern?
- Did the figures remain separate from the room, or become part of its visual rhythm?
- Where does your eye move first now?

### Exercise 2 — Landscape as color arrangement

Choose a simple landscape and use very flat depth with clear contours. Before generating, list five large color areas you expect the image to contain. After generating, compare your list with the result.

### Exercise 3 — Same subject, different surface

Run the same source twice:

1. restrained pattern, high subject preservation
2. immersive pattern, interpretive subject preservation

Decide which version communicates mood more effectively and which preserves the source more honestly.

## Reflect

- When does simplification clarify an image, and when does it erase important information?
- Why were painting, theater design, posters, screens, and domestic decoration treated as related practices by the Nabis?
- What changes when a picture stops pretending to be a transparent window and openly behaves like a flat designed object?
- Domestic interiors were often associated with women’s labor and private life. How should we discuss those spaces without treating them as merely decorative scenery?
- Japanese prints strongly influenced the group. How can the lesson acknowledge that influence without presenting Japanese art only as raw material for European modernism?

## Teaching cautions

Do not present the Nabis as a perfectly unified movement or as a simple step on a conveyor belt toward abstraction. Their religious beliefs, politics, careers, and later styles differed substantially.

The lesson should also name the asymmetry in nineteenth-century cultural exchange: European artists gained prestige by adapting Japanese visual ideas while Japanese artists and design traditions were often discussed through exoticizing language. Include Japanese prints as works with their own histories, makers, audiences, and purposes—not merely as “inspiration” for Paris.

## Suggested source search

Prioritize open-access collections from institutions such as:

- Musée d’Orsay
- National Gallery of Art
- Metropolitan Museum of Art
- Art Institute of Chicago
- Wikimedia Commons files with institution-backed public-domain status

Record the institution, object page, artist, title, date, and rights statement for every starter image before it enters the Academy seed set.

## Promotion checklist

- [x] At least three institution-verified public-domain example works are selected and each work has an item-level reusable-rights record.
- [ ] Recognition cues are tested against those works and one non-Nabis comparison.
- [ ] The prompt is trialed on an interior and a landscape.
- [ ] A cultural-history or representation reviewer checks the treatment of Japanese influence and domestic labor.
- [x] Remix configuration excludes artist names and named-artist imitation.
- [ ] The result avoids typography, generic retro-poster styling, and single-artist caricature.
- [x] Source and rights metadata are recorded for every displayed artwork.