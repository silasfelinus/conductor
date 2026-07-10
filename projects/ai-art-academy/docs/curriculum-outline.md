# AI Art Academy — v1 Art-History Curriculum Outline

date: 2026-07-10
task: ai-art-academy/t-005
status: draft for review (content complete, one source URL verified per movement)

This is the v1 curriculum: 14 movements in chronological order, from Greek vases to
De Stijl. Every artist named here is long dead (all listed artists died before 1955),
and every example work is a public-domain original held (or expected) in an
open-access collection. See the ethical boundary in DESIGN-BRIEF.md and the
forthcoming PUBLIC-DOMAIN-POLICY.md (t-006).

Verification method note: direct API/page fetches to museum hosts are blocked by the
session egress proxy, so verification was done via web search returning the live
collection URLs (titles + object pages confirmed per movement). Entries marked
"VERIFIED" have a confirmed collection URL; the rest are well-known holdings marked
"expected at <collection> (unverified)" and should be spot-checked when the seed
data ships (t-008 can batch-verify against the Met/AIC APIs from an unproxied
environment).

## Machine-readable skeleton

```yaml
movements:
  - slug: greek-vase-painting
    name: Ancient Greek Vase Painting
    era: "c. 600-400 BCE"
    artist_slugs: [exekias, euphiletos-painter, euphronios]
    example_count: 4
    remix_hint: "Redraw this image as an ancient Greek black-figure vase painting: silhouetted figures in glossy black on warm terracotta clay, incised details, decorative border bands"
  - slug: byzantine-mosaic
    name: Byzantine Mosaic
    era: "c. 500-1200 CE"
    artist_slugs: [anonymous-ravenna-mosaicists, anonymous-constantinople-mosaicists]
    example_count: 4
    remix_hint: "Recreate this image as a Byzantine mosaic made of small glass and gold tesserae, flat frontal figures, shimmering gold background, visible grout lines between tiles"
  - slug: illuminated-manuscript
    name: Medieval Illuminated Manuscript
    era: "c. 700-1450 CE"
    artist_slugs: [limbourg-brothers, jean-pucelle, jean-le-noir]
    example_count: 4
    remix_hint: "Repaint this image as a medieval illuminated manuscript miniature: jewel-toned tempera, gold leaf accents, flattened perspective, ornate foliate border"
  - slug: renaissance
    name: Renaissance
    era: "c. 1400-1600"
    artist_slugs: [leonardo-da-vinci, sandro-botticelli, raphael, albrecht-durer]
    example_count: 4
    remix_hint: "Repaint this image as a High Renaissance oil painting with sfumato shading, balanced composition, warm earth tones, and soft naturalistic light"
  - slug: baroque
    name: Baroque
    era: "c. 1600-1750"
    artist_slugs: [caravaggio, artemisia-gentileschi, rembrandt-van-rijn, johannes-vermeer]
    example_count: 4
    remix_hint: "Repaint this image as a Baroque oil painting with dramatic chiaroscuro lighting, deep shadows, rich saturated color, and theatrical contrast"
  - slug: ukiyo-e
    name: Ukiyo-e
    era: "c. 1650-1900"
    artist_slugs: [katsushika-hokusai, utagawa-hiroshige, kitagawa-utamaro]
    example_count: 4
    remix_hint: "Redraw this image as a Japanese ukiyo-e woodblock print: flat color planes, bold black outlines, stylized waves and clouds, subtle woodgrain texture"
  - slug: romanticism
    name: Romanticism
    era: "c. 1780-1850"
    artist_slugs: [caspar-david-friedrich, jmw-turner, francisco-goya, eugene-delacroix]
    example_count: 4
    remix_hint: "Repaint this image as a Romantic oil painting: dramatic sky, glowing atmospheric light, sublime scale, moody emotional tone"
  - slug: realism
    name: Realism
    era: "c. 1840-1880"
    artist_slugs: [gustave-courbet, jean-francois-millet, rosa-bonheur, honore-daumier]
    example_count: 4
    remix_hint: "Repaint this image as a 19th-century Realist oil painting: earthy palette, honest unidealized detail, natural daylight, dignified everyday subject"
  - slug: impressionism
    name: Impressionism
    era: "c. 1860-1890"
    artist_slugs: [claude-monet, pierre-auguste-renoir, berthe-morisot, camille-pissarro]
    example_count: 4
    remix_hint: "Repaint this image as a French Impressionist oil painting with visible broken brushstrokes, dappled natural light, and a bright plein-air palette"
  - slug: post-impressionism
    name: Post-Impressionism
    era: "c. 1885-1910"
    artist_slugs: [vincent-van-gogh, georges-seurat, paul-cezanne, paul-gauguin]
    example_count: 5
    remix_hint: "Repaint this image as a Post-Impressionist oil painting with bold expressive color, thick swirling impasto brushwork, and strong dark outlines"
  - slug: art-nouveau
    name: Art Nouveau
    era: "c. 1890-1914"
    artist_slugs: [alphonse-mucha, gustav-klimt, aubrey-beardsley]
    example_count: 4
    remix_hint: "Redraw this image as an Art Nouveau lithograph poster: flowing whiplash lines, ornamental floral halo, flat muted pastel color, elegant decorative border"
  - slug: expressionism
    name: Expressionism
    era: "c. 1905-1933"
    artist_slugs: [edvard-munch, franz-marc, ernst-ludwig-kirchner, paula-modersohn-becker]
    example_count: 4
    remix_hint: "Repaint this image as a German Expressionist painting: intense non-natural color, jagged energetic brushwork, and emotionally charged distortion"
  - slug: cubism
    name: Cubism
    era: "c. 1907-1925"
    artist_slugs: [juan-gris, albert-gleizes, roger-de-la-fresnaye]
    example_count: 4
    remix_hint: "Repaint this image as an early Cubist painting: fractured geometric planes, multiple shifting viewpoints, muted browns, grays, and blues"
  - slug: de-stijl
    name: De Stijl
    era: "1917-1931"
    artist_slugs: [piet-mondrian, theo-van-doesburg]
    example_count: 4
    remix_hint: "Reduce this image to a De Stijl composition: straight black lines and rectangles of pure red, yellow, blue, and white on a flat geometric grid"
```

---

## 1. Ancient Greek Vase Painting (`greek-vase-painting`)

**Era:** c. 600-400 BCE (Archaic and Classical Greece)

**Key ideas.** Before canvas and paper, some of the greatest drawing in history
happened on pottery. Greek artists painted athletes, gods, and everyday life onto
clay vessels used for wine, oil, and prizes — so a "painting" might also be the
trophy you won at the games. The two great techniques are black-figure (dark
silhouettes on orange clay, with details scratched in) and red-figure (the reverse:
the background painted black so figures stay clay-colored and can be drawn with a
brush). If you have ever admired a great comic-book inker, you already understand
why these artists are heroes: it is all about confident line and silhouette.

**Recognition cues:**
- Warm terracotta orange and glossy black, almost never any other dominant colors
- Figures shown in crisp profile, like a frieze marching around the vessel
- Details created by fine incised lines (black-figure) or brushed lines (red-figure)
- Decorative border bands: meander (Greek key), palmettes, rays
- The artwork wraps around a 3D pot — handles and curvature are part of the design

**Notable artists:**
- **Exekias** (active c. 545-530 BCE) — The undisputed master of black-figure,
  famous for quiet, psychologically loaded scenes like Ajax and Achilles playing a
  board game. Potter and painter both.
- **Euphiletos Painter** (active c. 530-520 BCE) — An Athenian black-figure painter
  known for Panathenaic prize amphorae showing sprinters and charioteers mid-race.
- **Euphronios** (c. 535 - after 470 BCE) — A pioneer of red-figure who drew anatomy
  with new naturalism; one of the first artists in history whose signed works we
  can follow as a career.

**Example works:**
- *Terracotta Panathenaic prize amphora*, attributed to the Euphiletos Painter,
  ca. 530 BCE — **VERIFIED**, Met Open Access (CC0):
  https://www.metmuseum.org/art/collection/search/248902
- *Terracotta amphora (jar) with a singing kitharode*, attributed to the Berlin
  Painter, ca. 490 BCE — expected at Met Open Access (unverified)
- *Terracotta lekythos (oil flask)*, attributed to the Amasis Painter,
  ca. 550-530 BCE — expected at Met Open Access (unverified)
- *Terracotta neck-amphora*, attributed to Exekias, ca. 540 BCE — expected at
  Met Open Access (unverified)

**remix_hint:** "Redraw this image as an ancient Greek black-figure vase painting:
silhouetted figures in glossy black on warm terracotta clay, incised details,
decorative border bands"

---

## 2. Byzantine Mosaic (`byzantine-mosaic`)

**Era:** c. 500-1200 CE

**Key ideas.** The Byzantine Empire built pictures out of thousands of tiny cubes of
glass, stone, and gold called tesserae. Set at slightly irregular angles, they
catch candlelight and shimmer — a mosaic ceiling was the closest thing the medieval
world had to a glowing screen. These artists were not trying to copy reality; they
wanted figures that felt eternal: frontal, still, wide-eyed, floating on fields of
pure gold. Most of the makers are anonymous, which is a lovely reminder that great
art does not require a famous name.

**Recognition cues:**
- Images visibly built from small square tiles with grout lines between them
- Radiant gold backgrounds instead of sky or landscape
- Flat, frontal, elongated figures with large solemn eyes and halos
- Rich jewel colors: deep blue, emerald, ruby, and lots of gold
- Little or no shadow or perspective — figures float rather than stand

**Notable artists:**
- **Anonymous mosaicists of Ravenna** (6th century) — The imperial workshops that
  lined San Vitale and Sant'Apollinare with the most famous mosaics in the world,
  including the court portraits of Justinian and Theodora.
- **Anonymous mosaicists of Constantinople** (6th-13th centuries) — Generations of
  craftspeople behind Hagia Sophia's golden interiors, whose techniques spread
  from Sicily to Kyiv.

**Example works:**
- *Fragment of a Floor Mosaic with a Personification of Ktisis*, Byzantine,
  500-550 CE — **VERIFIED**, Met Open Access (CC0):
  https://www.metmuseum.org/art/collection/search/469960
- *Empress Theodora and Her Court*, Basilica of San Vitale, Ravenna, ca. 547 CE —
  expected as PD photograph at Wikimedia Commons (unverified)
- *Emperor Justinian and His Retinue*, Basilica of San Vitale, Ravenna,
  ca. 547 CE — expected as PD photograph at Wikimedia Commons (unverified)
- *Deesis mosaic (Christ Pantocrator)*, Hagia Sophia, Istanbul, ca. 1261 —
  expected as PD photograph at Wikimedia Commons (unverified)

**remix_hint:** "Recreate this image as a Byzantine mosaic made of small glass and
gold tesserae, flat frontal figures, shimmering gold background, visible grout
lines between tiles"

---

## 3. Medieval Illuminated Manuscript (`illuminated-manuscript`)

**Era:** c. 700-1450 CE

**Key ideas.** For centuries, Europe's most precious paintings lived inside books.
"Illumination" means lighting the page up — with burnished gold leaf, brilliant
mineral pigments, and miniature scenes tucked into initial letters and margins.
These books were handmade from vellum (calfskin) and could take years; the margins
often overflow with vines, beasts, and jokes the scribes hid for each other. Think
of it as the medieval love child of painting, calligraphy, and bookbinding — art
you could hold in your hands.

**Recognition cues:**
- A page, not a canvas: text, decorated capital letters, and painted scenes together
- Gold leaf that reads as solid shining panels, especially in halos and backgrounds
- Saturated jewel tones — ultramarine blue, vermilion red — on creamy vellum
- Elaborate borders of ivy, flowers, and occasionally mischievous creatures
- Charmingly flattened space: tiled floors and buildings tilt toward the viewer

**Notable artists:**
- **The Limbourg Brothers** — Herman, Paul, and Johan (c. 1385-1416) — Three
  Netherlandish brothers, teenagers when they started, who painted the most
  celebrated manuscripts of the Middle Ages for Jean de France, duc de Berry.
  All three died in 1416, probably of plague.
- **Jean Pucelle** (c. 1300-1355) — Parisian illuminator who brought delicate
  grisaille (gray-tone) painting and playful margin life to royal prayer books.
- **Jean Le Noir** (active c. 1331-1375) — Pucelle's artistic heir, painter of the
  Prayer Book of Bonne of Luxembourg.

**Example works:**
- *The Belles Heures of Jean de France, duc de Berry*, Limbourg Brothers,
  1405-1409 — **VERIFIED**, The Met Cloisters (Open Access, CC0):
  https://www.metmuseum.org/art/collection/search/470306
- *The Hours of Jeanne d'Evreux*, Jean Pucelle, ca. 1324-28 — expected at Met
  Cloisters / Met Open Access (unverified)
- *The Prayer Book of Bonne of Luxembourg*, attributed to Jean Le Noir,
  before 1349 — expected at Met Cloisters / Met Open Access (unverified)
- *The Cloisters Apocalypse*, Norman workshop, ca. 1330 — expected at Met
  Cloisters / Met Open Access (unverified)

**remix_hint:** "Repaint this image as a medieval illuminated manuscript miniature:
jewel-toned tempera, gold leaf accents, flattened perspective, ornate foliate
border"

---

## 4. Renaissance (`renaissance`)

**Era:** c. 1400-1600

**Key ideas.** "Renaissance" means rebirth: European artists rediscovered classical
antiquity and, along with it, an obsession with how things actually look — anatomy,
perspective, light. Painters became scientists of seeing. Leonardo dissected bodies
to draw them better; architects worked out the mathematics of perspective so a flat
wall could open into deep space. The result is art that feels both idealized and
startlingly human: real faces, real weight, real air between things. If a painting
seems calm, balanced, and impossibly skillful all at once, you may be looking at
the Renaissance.

**Recognition cues:**
- Convincing depth: linear perspective pulling your eye to a vanishing point
- Sfumato — soft, smoky transitions between light and shadow, especially on faces
- Balanced, often triangular compositions with a serene, ordered feel
- Classical architecture, drapery, and mythological or biblical subjects
- Oil paint or tempera rendered so finely you rarely see a brushstroke

**Notable artists:**
- **Leonardo da Vinci** (1452-1519) — Painter, engineer, anatomist, and eternal
  question-asker; painted fewer than 20 surviving works and changed art forever
  with nearly all of them.
- **Sandro Botticelli** (1445-1510) — Florentine master of graceful line and
  wistful faces, painter of mythologies for the Medici.
- **Raphael** (1483-1520) — The great harmonizer of the High Renaissance, beloved
  for tender Madonnas and perfectly poised compositions; dead at 37.
- **Albrecht Dürer** (1471-1528) — The Renaissance genius of the North, who made
  printmaking a fine art and signed everything with a famous monogram.

**Example works:**
- *Ginevra de' Benci*, Leonardo da Vinci, c. 1474/1478 — **VERIFIED**, National
  Gallery of Art open access:
  https://www.nga.gov/artworks/50724-ginevra-de-benci-obverse
- *The Alba Madonna*, Raphael, c. 1510 — expected at National Gallery of Art open
  access (unverified)
- *The Last Communion of Saint Jerome*, Botticelli, early 1490s — expected at Met
  Open Access (unverified)
- *Melencolia I* (engraving), Albrecht Dürer, 1514 — expected at Met Open Access
  (unverified)

**remix_hint:** "Repaint this image as a High Renaissance oil painting with sfumato
shading, balanced composition, warm earth tones, and soft naturalistic light"

---

## 5. Baroque (`baroque`)

**Era:** c. 1600-1750

**Key ideas.** If the Renaissance is a held breath, the Baroque is the exhale — art
turned up to eleven. Painters discovered that a single shaft of light cutting
through darkness could make a picture feel like theater, and they used it for
everything from saints to tavern brawls. This is the age of chiaroscuro (bold
light-dark contrast), sweeping diagonals, and paint that seems to move. It is also
the age of the Dutch masters, who pointed all that drama at quiet kitchens and
thoughtful faces — proof that ordinary life deserves a spotlight too.

**Recognition cues:**
- Dramatic spotlight lighting: bright figures emerging from deep darkness
- Strong diagonals and swirling motion instead of calm symmetry
- Rich, saturated color and sumptuous fabric, metal, and skin textures
- Intense emotion — faces caught mid-gasp, mid-prayer, mid-laugh
- In Dutch Baroque: everyday interiors rendered with jewel-like devotion

**Notable artists:**
- **Caravaggio** (1571-1610) — The brawling revolutionary who painted saints with
  dirty feet and invented the lighting style half of cinema still uses.
- **Artemisia Gentileschi** (1593-c. 1656) — The most celebrated woman painter of
  the age, whose heroines are fierce, capable, and unmistakably real.
- **Rembrandt van Rijn** (1606-1669) — Master of light and human depth; his
  self-portraits chart an entire life with unmatched honesty.
- **Johannes Vermeer** (1632-1675) — Painter of stillness: about 35 known works,
  most of them quiet rooms where daylight becomes the main character.

**Example works:**
- *The Milkmaid*, Johannes Vermeer, c. 1660 — **VERIFIED**, Rijksmuseum
  (object SK-A-2344, open access):
  https://www.rijksmuseum.nl/en/collection/object/The-Milkmaid--42dd0e658c2979aec8e144d2357c55c0
- *The Night Watch*, Rembrandt van Rijn, 1642 — expected at Rijksmuseum
  (SK-C-5, open access) (unverified)
- *The Denial of Saint Peter*, Caravaggio, 1610 — expected at Met Open Access
  (unverified)
- *Esther before Ahasuerus*, Artemisia Gentileschi, ca. 1630s — expected at Met
  Open Access (unverified)

**remix_hint:** "Repaint this image as a Baroque oil painting with dramatic
chiaroscuro lighting, deep shadows, rich saturated color, and theatrical contrast"

---

## 6. Ukiyo-e (`ukiyo-e`)

**Era:** c. 1650-1900 (Edo period Japan)

**Key ideas.** Ukiyo-e means "pictures of the floating world" — the theaters,
teahouses, landscapes, and celebrities of Edo-period Japan. These are woodblock
prints, made by a team: an artist drew the design, a carver cut it into cherry
wood blocks, and a printer inked one block per color. Because prints were cheap
and popular, this was art for everyone, not just the wealthy — the poster art and
manga ancestor of its day. When these prints reached Europe in the 1860s, they
blew the minds of the Impressionists and changed Western art's sense of
composition forever.

**Recognition cues:**
- Flat planes of color with little or no shading, bounded by confident outlines
- Bold, cropped compositions and daring viewpoints — subjects sliced by the frame
- Stylized natural forms: claw-like waves, cloud bands, patterned rain
- Gradated color skies (bokashi) fading from deep blue to pale
- Japanese calligraphy and red seal cartouches integrated into the design

**Notable artists:**
- **Kitagawa Utamaro** (1753-1806) — The great portraitist of women, famous for
  intimate close-up "large head" beauty prints.
- **Katsushika Hokusai** (1760-1849) — Restless genius of landscape who made
  Mount Fuji a global icon; changed his artist name over 30 times and claimed he
  was only getting good at 70.
- **Utagawa Hiroshige** (1797-1858) — Poet of weather and travel: rain, snow, and
  moonlight along Japan's great roads.

**Example works:**
- *Under the Wave off Kanagawa (The Great Wave)*, Katsushika Hokusai,
  ca. 1830-32 — **VERIFIED**, Met Open Access (CC0):
  https://www.metmuseum.org/art/collection/search/36491
- *South Wind, Clear Sky (Red Fuji)*, Katsushika Hokusai, ca. 1830-32 — expected
  at Met Open Access (unverified)
- *Sudden Shower over Shin-Ohashi Bridge and Atake*, Utagawa Hiroshige, 1857 —
  expected at Met Open Access / Art Institute of Chicago CC0 (unverified)
- *A beauty print from "Ten Types in the Physiognomic Study of Women"*, Kitagawa
  Utamaro, ca. 1792-93 — expected at Met Open Access (unverified)

**remix_hint:** "Redraw this image as a Japanese ukiyo-e woodblock print: flat
color planes, bold black outlines, stylized waves and clouds, subtle woodgrain
texture"

---

## 7. Romanticism (`romanticism`)

**Era:** c. 1780-1850

**Key ideas.** Romanticism put feeling first. Reacting against the tidy rationalism
of the Enlightenment, these artists chased the sublime — that shiver you get before
a storm at sea, a mountain at dusk, a ruin under the moon. Nature became enormous
and humans became small, contemplative figures at its edge. It is also art about
inner weather: dreams, terror, longing, and rebellion all belong here. If a
painting makes you feel awe first and only then asks you to think, it is probably
Romantic.

**Recognition cues:**
- Vast dramatic landscapes and skies that dwarf any human figures
- Figures seen from behind, gazing into the distance (you are invited to join them)
- Glowing, atmospheric light: moonrises, sunsets, fog, storms
- Emotional, sometimes turbulent brushwork and deep moody palettes
- Subjects of awe and extremity: shipwrecks, ruins, revolutions, nightmares

**Notable artists:**
- **Francisco Goya** (1746-1828) — Spanish court painter who became the era's
  darkest, most modern conscience, in paint and in print.
- **Caspar David Friedrich** (1774-1840) — German painter of contemplative souls
  facing mist, moon, and mountain; practically invented the wanderer-gazing motif.
- **J. M. W. Turner** (1775-1851) — English painter who dissolved ships and cities
  into storms of light; a bridge from Romanticism toward abstraction.
- **Eugène Delacroix** (1798-1863) — French colorist of passion and movement whose
  loose, vibrating color paved the road to Impressionism.

**Example works:**
- *Two Men Contemplating the Moon*, Caspar David Friedrich, ca. 1825-30 —
  **VERIFIED**, Met Open Access (CC0):
  https://www.metmuseum.org/art/collection/search/438417
- *The Grand Canal, Venice*, J. M. W. Turner, 1835 — expected at Met Open Access
  (unverified)
- *The Sleep of Reason Produces Monsters* (Los Caprichos, plate 43), Francisco
  Goya, 1799 — expected at Met Open Access (unverified)
- *The Abduction of Rebecca*, Eugène Delacroix, 1846 — expected at Met Open
  Access (unverified)

**remix_hint:** "Repaint this image as a Romantic oil painting: dramatic sky,
glowing atmospheric light, sublime scale, moody emotional tone"

---

## 8. Realism (`realism`)

**Era:** c. 1840-1880

**Key ideas.** Realism said: enough angels, enough emperors — paint the world in
front of you. Courbet and his allies made monumental canvases of stone breakers,
gleaners, farm horses, and third-class train carriages, granting working people
the scale and dignity that had been reserved for kings and gods. It was genuinely
scandalous at the time; critics called it vulgar, which usually means an artist is
onto something. Realism's honesty about ordinary life laid the groundwork for
photography-age art and for every artist since who has painted what they actually
see.

**Recognition cues:**
- Everyday, working-class subjects treated at grand, heroic scale
- Earthy palette — browns, grays, greens — and truthful, unflattering light
- Solid, weighty figures with none of the porcelain finish of academic art
- No mythology, no idealization, no visible fantasy
- Compositions that feel observed rather than staged

**Notable artists:**
- **Honoré Daumier** (1808-1879) — Painter and razor-sharp caricaturist who
  chronicled (and skewered) modern urban life in thousands of lithographs.
- **Jean-François Millet** (1814-1875) — Painter of peasant labor whose gleaners
  and sowers became icons of quiet dignity; a hero to Van Gogh.
- **Gustave Courbet** (1819-1877) — The movement's swaggering standard-bearer:
  "Show me an angel and I will paint one."
- **Rosa Bonheur** (1822-1899) — The most famous woman artist of the 19th century,
  celebrated for meticulously observed animal paintings on a monumental scale.

**Example works:**
- *Woman with a Parrot*, Gustave Courbet, 1866 — **VERIFIED**, Met Open Access
  (CC0): https://www.metmuseum.org/art/collection/search/436002
- *The Horse Fair*, Rosa Bonheur, 1852-55 — expected at Met Open Access
  (unverified)
- *Haystacks: Autumn*, Jean-François Millet, ca. 1874 — expected at Met Open
  Access (unverified)
- *The Third-Class Carriage*, Honoré Daumier, ca. 1862-64 — expected at Met Open
  Access (unverified)

**remix_hint:** "Repaint this image as a 19th-century Realist oil painting: earthy
palette, honest unidealized detail, natural daylight, dignified everyday subject"

---

## 9. Impressionism (`impressionism`)

**Era:** c. 1860-1890

**Key ideas.** The Impressionists dragged their easels outdoors and tried to paint
not things, but the light bouncing off things — a riverbank at noon, steam in a
train station, the flicker of a garden party. To catch moments that changed by the
minute, they worked fast, in broken dabs of unmixed color that your eye blends at
a distance. The art establishment laughed ("mere impressions!"), so they mounted
their own exhibitions and won. Up close it looks like confetti; step back and it
becomes sunlight. That magic trick never gets old.

**Recognition cues:**
- Visible, broken brushstrokes — dabs and commas of color side by side
- Bright, high-key palette with colored (often violet-blue) shadows, rarely black
- Everyday modern-life subjects: cafes, boating, gardens, city streets
- A sense of a fleeting instant — weather and light you can almost feel changing
- Soft edges everywhere; forms dissolve when you lean in

**Notable artists:**
- **Camille Pissarro** (1830-1903) — The movement's steady mentor figure, the only
  artist to show in all eight Impressionist exhibitions.
- **Claude Monet** (1840-1926) — The purest Impressionist: haystacks, cathedrals,
  and water lilies painted over and over as the light changed.
- **Berthe Morisot** (1841-1895) — Founding member of the group whose feathery,
  audacious brushwork made intimate domestic scenes shimmer.
- **Pierre-Auguste Renoir** (1841-1919) — Painter of dappled light on happy
  gatherings; nobody has ever painted a nicer afternoon.

**Example works:**
- *Two Sisters (On the Terrace)*, Pierre-Auguste Renoir, 1881 — **VERIFIED**,
  Art Institute of Chicago (CC0):
  https://www.artic.edu/artworks/14655/two-sisters-on-the-terrace
- *Paris Street; Rainy Day*, Gustave Caillebotte, 1877 — expected at Art
  Institute of Chicago CC0 (unverified)
- *Bridge over a Pond of Water Lilies*, Claude Monet, 1899 — expected at Met
  Open Access (unverified)
- *Young Woman Knitting*, Berthe Morisot, ca. 1883 — expected at Met Open Access
  (unverified)

**remix_hint:** "Repaint this image as a French Impressionist oil painting with
visible broken brushstrokes, dappled natural light, and a bright plein-air palette"

---

## 10. Post-Impressionism (`post-impressionism`)

**Era:** c. 1885-1910

**Key ideas.** The Post-Impressionists loved what Impressionism had unlocked but
wanted more than fleeting light — they wanted structure, symbol, and raw feeling.
This is less one movement than four brilliant personal answers to the same
question: Seurat rebuilt light out of scientific dots; Cézanne rebuilt nature out
of planes and patient looking; Van Gogh turned color and brushstroke into pure
emotion; Gauguin flattened the world into bold symbolic shapes. Between them they
opened every door that 20th-century art would walk through.

**Recognition cues:**
- Color used for feeling or design rather than strict realism
- Highly personal, recognizable mark-making: dots, swirls, patient parallel strokes
- Stronger outlines and flatter, more deliberate shapes than Impressionism
- Thick impasto and writhing energy (Van Gogh) or cool systematic order (Seurat)
- A sense that the picture is built and composed, not just glimpsed

**Notable artists:**
- **Paul Cézanne** (1839-1906) — Patient rebuilder of nature into planes of color;
  "the father of us all," Picasso and Matisse both said.
- **Paul Gauguin** (1848-1903) — Stockbroker turned painter of flat, saturated,
  dreamlike scenes; a complicated man whose color changed art.
- **Vincent van Gogh** (1853-1890) — Sold almost nothing in life, wrote the most
  moving letters in art history, and painted feeling itself in about a decade.
- **Georges Seurat** (1859-1891) — Inventor of pointillism, who built luminous
  monumental scenes from tiny dots of pure color; dead at 31.

**Example works:**
- *A Sunday on La Grande Jatte — 1884*, Georges Seurat, 1884-86 — **VERIFIED**,
  Art Institute of Chicago (CC0):
  https://www.artic.edu/artworks/27992/a-sunday-on-la-grande-jatte-1884
- *The Bedroom*, Vincent van Gogh, 1889 — expected at Art Institute of Chicago
  CC0 (unverified)
- *Wheat Field with Cypresses*, Vincent van Gogh, 1889 — expected at Met Open
  Access (unverified)
- *Still Life with Apples and a Pot of Primroses*, Paul Cézanne, ca. 1890 —
  expected at Met Open Access (unverified)
- *Ia Orana Maria (Hail Mary)*, Paul Gauguin, 1891 — expected at Met Open Access
  (unverified)

**remix_hint:** "Repaint this image as a Post-Impressionist oil painting with bold
expressive color, thick swirling impasto brushwork, and strong dark outlines"

---

## 11. Art Nouveau (`art-nouveau`)

**Era:** c. 1890-1914

**Key ideas.** Art Nouveau ("new art") wanted beauty everywhere — not just in
gilded frames but in posters, subway entrances, lamps, jewelry, and typography.
Its signature is the whiplash line: a long, sinuous curve borrowed from vines,
lilies, dragonfly wings, and flowing hair. When Alphonse Mucha's first Sarah
Bernhardt poster appeared on Paris streets in 1895, people cut them down to keep —
advertising had accidentally become fine art. This is a wonderful movement for
learning that "decorative" is not an insult.

**Recognition cues:**
- Long flowing S-curves — hair, smoke, stems, and fabric that ripple like water
- Figures (often women) framed by halos, arches, or mosaic-like ornament
- Flat, poster-like color with elegant contour lines; lithograph texture
- Nature stylized into ornament: irises, peacocks, insects, tendrils
- Custom lettering woven into the composition

**Notable artists:**
- **Alphonse Mucha** (1860-1939) — Czech master of the poster whose "le style
  Mucha" defined the look of the era overnight.
- **Gustav Klimt** (1862-1918) — Vienna Secession leader who wrapped figures in
  shimmering gold and pattern until painting became mosaic.
- **Aubrey Beardsley** (1872-1898) — English illustrator of sinuous, scandalous
  black-and-white ink work; dead at 25 with an outsized legacy.

**Example works:**
- *Gismonda* (poster for Sarah Bernhardt), Alphonse Mucha, 1894 — **VERIFIED**,
  Wikimedia Commons PD:
  https://commons.wikimedia.org/wiki/File:Alfons_Mucha_-_1894_-_Gismonda.jpg
- *The Kiss*, Gustav Klimt, 1907-08 — Belvedere, Vienna; expected as PD scan at
  Wikimedia Commons (unverified)
- *Job* (cigarette-paper poster), Alphonse Mucha, 1896 — expected as PD scan at
  Wikimedia Commons (unverified)
- *The Peacock Skirt* (illustration for Oscar Wilde's "Salome"), Aubrey
  Beardsley, 1893 — expected as PD scan at Wikimedia Commons / Smithsonian Open
  Access (unverified)

**remix_hint:** "Redraw this image as an Art Nouveau lithograph poster: flowing
whiplash lines, ornamental floral halo, flat muted pastel color, elegant
decorative border"

---

## 12. Expressionism (`expressionism`)

**Era:** c. 1905-1933 (mainly Germany, Austria, and Scandinavia)

**Key ideas.** Expressionists painted the world not as it looks, but as it feels.
A sky can scream, a street can lurch, a blue horse can be truer than a brown one.
Sparked by Munch and van Gogh and carried by German groups like Die Brücke
("The Bridge") and Der Blaue Reiter ("The Blue Rider"), these artists used
clashing color and jagged, urgent marks to get inner life onto canvas fast, before
politeness could interfere. It is some of the most honest art ever made — and a
gift to anyone who has ever felt too much.

**Recognition cues:**
- Deliberately "wrong," emotionally charged color: blue horses, green faces, red skies
- Angular, distorted figures and tilting, unstable spaces
- Rough, urgent brushwork or stark carved-looking woodcut lines
- Faces and poses stretched toward anxiety, ecstasy, or tenderness
- City nightlife, nature-as-refuge, and raw psychological subjects

**Notable artists:**
- **Edvard Munch** (1863-1944) — Norwegian forerunner whose "The Scream" made
  anxiety itself a painting subject.
- **Paula Modersohn-Becker** (1876-1907) — German painter of startlingly modern,
  tender portraits; the first known woman artist to paint a nude self-portrait.
- **Franz Marc** (1880-1916) — Co-founder of Der Blaue Reiter who painted animals
  in radiant symbolic color; killed at Verdun in the First World War.
- **Ernst Ludwig Kirchner** (1880-1938) — Die Brücke's electric chronicler of
  Berlin streets, all nervous angles and acid color.

**Example works:**
- *The Bewitched Mill*, Franz Marc, 1913 — **VERIFIED**, Art Institute of Chicago
  (CC0): https://www.artic.edu/artworks/9021/the-bewitched-mill
- *The Scream* (1893 tempera version), Edvard Munch — National Museum of Norway;
  expected as PD scan at Wikimedia Commons (unverified)
- *Berlin Street Scene*, Ernst Ludwig Kirchner, 1913 — expected as PD scan at
  Wikimedia Commons (unverified)
- *Self-Portrait with Amber Necklace*, Paula Modersohn-Becker, 1906 — expected as
  PD scan at Wikimedia Commons (unverified)

**remix_hint:** "Repaint this image as a German Expressionist painting: intense
non-natural color, jagged energetic brushwork, and emotionally charged distortion"

---

## 13. Cubism (`cubism`)

**Era:** c. 1907-1925

**Key ideas.** Cubism asked a wild question: why should a painting show only one
moment from one angle? Instead, the Cubists shattered subjects into facets and
reassembled them so you see the front, side, and top of a guitar — or a friend's
face — all at once. Early "analytic" Cubism is quiet and almost monochrome, like a
puzzle in browns and grays; later "synthetic" Cubism gets playful, with brighter
shapes and collaged newspaper. It rewired how humans think about images, and its
fingerprints are on everything from graphic design to video-game art.

*A note on names:* Cubism was launched by Picasso and Braque, whom you will meet in
the lesson text — but because they died in 1973 and 1963, their works are still
under copyright in most places. Our example gallery instead features their
brilliant early-generation colleagues whose art is safely in the public domain.

**Recognition cues:**
- Objects and figures broken into overlapping geometric planes and facets
- Several viewpoints of one subject fused into a single image
- Analytic phase: near-monochrome palettes of brown, gray, ochre, and blue
- Shallow, compressed space — no deep perspective to escape into
- Fragments of legible reality: lettering, guitars, bottles, pipes, table edges

**Notable artists:**
- **Albert Gleizes** (1881-1953) — Painter and co-author of the first book on
  Cubism (1912), who helped turn a studio experiment into a public movement.
- **Roger de La Fresnaye** (1885-1925) — French painter who fused Cubist geometry
  with warm color and grand, legible subjects.
- **Juan Gris** (1887-1927) — The "third musketeer" of Cubism, whose crystalline,
  elegant compositions made the style sing; died at just 40.

**Example works:**
- *Portrait of Pablo Picasso*, Juan Gris, 1912 — **VERIFIED**, Art Institute of
  Chicago (CC0): https://www.artic.edu/artworks/8624/portrait-of-pablo-picasso
- *The Musician's Table*, Juan Gris, 1914 — expected at Met Open Access (Leonard
  A. Lauder Cubist Collection) (unverified)
- *Man on a Balcony*, Albert Gleizes, 1912 — expected as PD scan at Wikimedia
  Commons (unverified)
- *The Conquest of the Air*, Roger de La Fresnaye, 1913 — expected as PD scan at
  Wikimedia Commons (unverified)

**remix_hint:** "Repaint this image as an early Cubist painting: fractured
geometric planes, multiple shifting viewpoints, muted browns, grays, and blues"

---

## 14. De Stijl (`de-stijl`)

**Era:** 1917-1931 (Netherlands)

**Key ideas.** Born in the neutral Netherlands during World War I, De Stijl
("The Style") believed art could help rebuild a broken world by finding a
universal visual language: straight horizontal and vertical lines, rectangles, and
only the purest ingredients — red, yellow, blue, black, white, and gray. Mondrian
spent decades nudging lines millimeter by millimeter until a composition felt
perfectly balanced; it looks simple and is anything but. The movement's DNA is
everywhere today, from architecture and furniture to interface design. (Its German
cousin, the early Bauhaus school, carried the same dream of art-meets-design into
workshops and classrooms.)

**Recognition cues:**
- Only straight lines, meeting at right angles — no curves anywhere
- Primary colors (red, yellow, blue) plus black, white, and gray, and nothing else
- Asymmetric grids of rectangles balanced with uncanny precision
- Completely flat surfaces: no shading, no depth, no texture illusion
- Occasionally the whole canvas turned 45 degrees into a diamond ("lozenge")

**Notable artists:**
- **Piet Mondrian** (1872-1944) — The movement's purist soul, who journeyed from
  Dutch landscapes to total abstraction and never stopped refining; also a
  passionate ballroom-dancing and jazz enthusiast.
- **Theo van Doesburg** (1883-1931) — Painter, writer, and tireless promoter who
  founded the De Stijl journal — then split with Mondrian over whether a diagonal
  line was allowed. (Really.)

**Example works:**
- *Lozenge Composition with Yellow, Black, Blue, Red, and Gray*, Piet Mondrian,
  1921 — **VERIFIED**, Art Institute of Chicago (CC0):
  https://www.artic.edu/artworks/109819/lozenge-composition-with-yellow-black-blue-red-and-gray
- *Tableau I*, Piet Mondrian, 1921 — Kunstmuseum Den Haag; expected as PD scan at
  Wikimedia Commons (unverified)
- *Composition VIII (The Cow)*, Theo van Doesburg, c. 1918 — expected as PD scan
  at Wikimedia Commons (unverified)
- *Counter-Composition V*, Theo van Doesburg, 1924 — expected as PD scan at
  Wikimedia Commons (unverified)

**remix_hint:** "Reduce this image to a De Stijl composition: straight black lines
and rectangles of pure red, yellow, blue, and white on a flat geometric grid"

---

## Lesson-only vs remixable

Every movement above maps to a remix config (mode `prompt` to start; t-003/t-004
decide where LoRAs help). Expected remix quality, flagged honestly:

**Strong remix candidates (ship first):** `ukiyo-e`, `impressionism`,
`post-impressionism`, `art-nouveau`, `expressionism`, `baroque`, `romanticism`,
`renaissance`, `realism`. These are heavily represented in FLUX/Kontext training
data and their styles transfer while preserving the user's composition — the core
Academy promise.

**Good but watch the output:** `greek-vase-painting` and `byzantine-mosaic` are
strong graphic transformations (silhouette-on-terracotta, tesserae-and-gold) that
usually look delightful, but the model may add vessel curvature/border framing or
lose fine facial detail — test in t-004. `illuminated-manuscript` remixes well as
"miniature with gold border," though the page/text context can crowd small
subjects.

**Flagged as likely-poor remixers:**
- `cubism` — faceting while "preserving the composition" is partly contradictory;
  Kontext may produce shallow "crystallized photo" effects rather than true
  analytic fragmentation. Keep the lesson regardless; ship the remix only if
  t-004 A/B results look credible.
- `de-stijl` — the honest version of this style *discards* the source image
  (pure abstraction). A faithful remix leaves nothing of the user's photo; a
  recognizable remix isn't faithful De Stijl. Recommend lesson-first, with the
  remix framed playfully ("Mondrian-ify: reduce your image to its grid") and
  expectations set in the UI copy.

No movement is lesson-only in v1 — even the flagged two get a remix config — but
`cubism` and `de-stijl` should carry a "results vary, that's part of the fun" note
until t-004 evaluates them.

## Public-domain safety check (t-006 preview)

All named artists died in 1953 or earlier (most recent deaths: Gleizes 1953,
Munch 1944, Mondrian 1944, Mucha 1939, Kirchner 1938). No living or post-1990
deceased artist appears anywhere. Picasso (d. 1973) and Braque (d. 1963) are
mentioned in Cubism lesson prose as historical context only — no works of theirs
are exhibited, remixed, or attributed as style targets. Every example work
predates 1930, so all are US public domain; the most recent is van Doesburg's
Counter-Composition V (1924), with the Klimt (1907-08), Marc (1913), and
Mondrian (1921) works also comfortably pre-1930.
