# AI Art Academy — v1 Art-History Curriculum Outline

date: 2026-07-10
task: ai-art-academy/t-005
status: draft for review (content complete, one source URL verified per movement)

This is the curriculum: 21 movements spanning the timeline from Greek vases to
Bauhaus. Every artist named here is long dead (all listed artists died before 1955),
and every example work is a public-domain original held (or expected) in an
open-access collection. See the ethical boundary in DESIGN-BRIEF.md and the
PUBLIC-DOMAIN-POLICY.md (t-006).

Sections 1-16 are the v1 set (chronological). Sections 17-21 are the 2026-07-16 v1.1
expansion (t-010 cycle): Gothic panel painting, Northern Renaissance, Rococo,
Symbolism, and Neo-Impressionism/Pointillism. They are appended (rather than
renumbered into place) but belong chronologically among the earlier movements — read
the `era` field in the machine-readable skeleton for true ordering; the front-end
seed (t-020) inserts them in chronological position.

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
  - slug: neoclassicism
    name: Neoclassicism
    era: "c. 1750-1830"
    artist_slugs: [jacques-louis-david, jean-auguste-dominique-ingres, antonio-canova, angelica-kauffman]
    example_count: 4
    remix_hint: "Repaint this image as a Neoclassical oil painting: crisp linear contours, cool restrained color, smooth invisible brushwork, and a calm, stage-like classical composition"
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
  - slug: bauhaus
    name: Bauhaus
    era: "1919-1933"
    artist_slugs: [wassily-kandinsky, paul-klee, laszlo-moholy-nagy]
    example_count: 4
    remix_hint: "Repaint this image as a Bauhaus-school geometric abstraction: pure circles, triangles, and squares in bold primary colors on a flat plane, precise linework, no realistic shading"
  # --- v1.1 expansion (2026-07-16, t-010 cycle) ---
  # These five belong chronologically among the movements above (see each `era`);
  # appended here to avoid renumbering the v1 sections. The seed-sync task (t-020)
  # inserts them in chronological order in academyStyles.ts.
  - slug: gothic
    name: Gothic Panel Painting
    era: "c. 1200-1450"
    artist_slugs: [duccio-di-buoninsegna, giotto-di-bondone, simone-martini, fra-angelico]
    example_count: 4
    remix_hint: "Repaint this image as a late-medieval Gothic panel painting: figures on a burnished gold-leaf ground, elongated bodies with gentle S-curves, jewel-toned tempera, pointed-arch framing, flattened space"
  - slug: northern-renaissance
    name: Northern Renaissance
    era: "c. 1420-1570"
    artist_slugs: [jan-van-eyck, rogier-van-der-weyden, hans-memling, pieter-bruegel-the-elder, hieronymus-bosch]
    example_count: 4
    remix_hint: "Repaint this image as an Early Netherlandish oil painting: microscopic detail, luminous layered glazes, crisp naturalism, cool northern daylight, and a meticulously rendered landscape or interior behind the figures"
  - slug: rococo
    name: Rococo
    era: "c. 1700-1780"
    artist_slugs: [antoine-watteau, francois-boucher, jean-honore-fragonard, jean-baptiste-simeon-chardin]
    example_count: 4
    remix_hint: "Repaint this image as a Rococo oil painting: pastel palette of rose, sky-blue, and cream, feathery loose brushwork, soft diffused light, playful ornamental curves, and a light, airy mood"
  - slug: symbolism
    name: Symbolism
    era: "c. 1880-1910"
    artist_slugs: [gustave-moreau, odilon-redon, arnold-bocklin, pierre-puvis-de-chavannes]
    example_count: 4
    remix_hint: "Repaint this image as a Symbolist painting: dreamlike mysterious mood, muted twilight color, mythic and allegorical atmosphere, soft glowing light, and a sense of reverie rather than plain reality"
  - slug: pointillism
    name: Neo-Impressionism / Pointillism
    era: "c. 1884-1910"
    artist_slugs: [georges-seurat, paul-signac, henri-edmond-cross, theo-van-rysselberghe]
    example_count: 4
    remix_hint: "Repaint this image using pointillist technique: thousands of tiny separate dots of pure unmixed color that blend in the eye, a luminous divisionist surface, even all-over stippling, and bright balanced light"
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

## 6. Neoclassicism (`neoclassicism`)

**Era:** c. 1750-1830

**Key ideas.** Neoclassicism was a deliberate correction: after Rococo's pastel
frivolity, artists turned back to the "noble simplicity" of Greece and Rome,
freshly fueled by the excavations at Pompeii and Herculaneum. The style prized
clear drawing over loose paint, moral seriousness over decoration, and stoic
self-sacrifice over romance. Its timing was not an accident — this is the art of
the Enlightenment and the age of revolutions, and its painters used togas and
Roman senators to talk, quite pointedly, about civic virtue and their own
turbulent present.

**Recognition cues:**
- Crisp, precise contours — line does the work, not visible brushwork
- Cool, restrained color and even, theater-lit illumination (no Baroque murk)
- Friezelike compositions: figures arranged shallowly, almost like a stage set
- Classical props — togas, columns, Roman furniture, marble — used with intent
- Frozen, deliberate gestures at a moment of moral or political decision

**Notable artists:**
- **Jacques-Louis David** (1748-1825) — The movement's central figure and
  eventual court painter to Napoleon; his Roman history paintings doubled as
  political manifestos on the eve of the French Revolution.
- **Jean-Auguste-Dominique Ingres** (1780-1867) — David's most brilliant pupil,
  who pushed line into near-abstraction and became the era's defining
  portraitist of French society.
- **Antonio Canova** (1757-1822) — The age's greatest sculptor, whose marble
  figures combine antique cool with an almost tender softness.
- **Angelica Kauffman** (1741-1807) — Swiss-born history painter and a founding
  member of Britain's Royal Academy, one of only two women among its founders.

**Example works:**
- *The Death of Socrates*, Jacques-Louis David, 1787 — expected at Met Open
  Access (unverified): https://www.metmuseum.org/art/collection/search/436105
- *Oath of the Horatii*, Jacques-Louis David, 1784 — Musée du Louvre; expected
  as PD scan at Wikimedia Commons (unverified)
- *Joseph-Antoine Moltedo*, Jean-Auguste-Dominique Ingres, 1810 — expected at
  Met Open Access (unverified): https://www.metmuseum.org/art/collection/search/438818
- *Psyche Revived by Cupid's Kiss*, Antonio Canova, 1787-93 — Musée du Louvre;
  expected as PD photograph at Wikimedia Commons (unverified)

**remix_hint:** "Repaint this image as a Neoclassical oil painting: crisp linear
contours, cool restrained color, smooth invisible brushwork, and a calm,
stage-like classical composition"

---

## 7. Ukiyo-e (`ukiyo-e`)

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

## 8. Romanticism (`romanticism`)

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

## 9. Realism (`realism`)

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

## 10. Impressionism (`impressionism`)

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

## 11. Post-Impressionism (`post-impressionism`)

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

## 12. Art Nouveau (`art-nouveau`)

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

## 13. Expressionism (`expressionism`)

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

## 14. Cubism (`cubism`)

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
- *Portrait of Pablo Picasso*, Juan Gris, 1912 — CORRECTION 2026-07-17
  (ai-art-academy/t-013): previously marked VERIFIED/CC0, but api.artic.edu
  reports `is_public_domain: false` for this object — re-verify before use
  (unverified): https://www.artic.edu/artworks/8624/portrait-of-pablo-picasso
- *The Musician's Table*, Juan Gris, 1914 — expected at Met Open Access (Leonard
  A. Lauder Cubist Collection) (unverified)
- *Man on a Balcony*, Albert Gleizes, 1912 — expected as PD scan at Wikimedia
  Commons (unverified)
- *The Conquest of the Air*, Roger de La Fresnaye, 1913 — expected as PD scan at
  Wikimedia Commons (unverified)

**remix_hint:** "Repaint this image as an early Cubist painting: fractured
geometric planes, multiple shifting viewpoints, muted browns, grays, and blues"

---

## 15. De Stijl (`de-stijl`)

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

## 16. Bauhaus (`bauhaus`)

**Era:** 1919-1933 (Weimar → Dessau → Berlin, Germany)

**Key ideas.** The Bauhaus school treated painting, craft, and design as one
discipline: "form follows function," taught through hands-on workshops
(weaving, typography, metalwork, furniture) alongside foundational theory
courses. Kandinsky and Klee both taught the first-year "form" class, codifying
color and shape into a shared visual vocabulary — De Stijl's flat grids were a
direct influence, feeding straight into the school's founding years. When the
Nazi government forced the school to close in 1933, its faculty scattered
worldwide and carried the style into modern graphic design, architecture, and
art education.

**Recognition cues:**
- Pure geometric forms — circles, triangles, squares — used as a symbolic
  color-form vocabulary (Kandinsky's "point, line, plane" theory)
- Bold primary and secondary color fields, often crossed by black grid lines
  or radiating diagonals
- Whimsical, sign-like pictograms layered over precise geometric grids (Klee)
- Camera-less "photograms" — ghostly silhouettes made by placing objects
  directly on light-sensitive paper (Moholy-Nagy)
- Sans-serif geometric typography and ornament-free composition in adjacent
  design work

**Notable artists:**
- **Wassily Kandinsky** (1866-1944) — Led the Bauhaus's foundational "form"
  class, teaching that geometric shapes and colors carry specific emotional
  meaning (to him, a circle is calm, a triangle is aggressive).
- **Paul Klee** (1879-1940) — Taught alongside Kandinsky and filled private
  notebooks with pedagogical diagrams; his own paintings mix deceptively
  childlike pictograms with dry, precise geometry.
- **László Moholy-Nagy** (1895-1946) — Ran the Bauhaus's metal workshop and
  pioneered the photogram, treating light itself as an art medium; later
  founded the New Bauhaus in Chicago after the school's closure.

**Example works:**
- *Orange*, Wassily Kandinsky, 1923 — CORRECTION 2026-07-17
  (ai-art-academy/t-013): previously marked VERIFIED/CC0, but
  api.artic.edu reports `is_public_domain: false` with a live copyright
  notice ("© 2018 Artists Rights Society (ARS), New York / ADAGP,
  Paris") for this object — re-verify before use (unverified):
  https://www.artic.edu/artworks/72690/orange
- *Circles in a Circle*, Wassily Kandinsky, 1923 — Philadelphia Museum of Art
  (Louise and Walter Arensberg Collection); expected as PD scan at Wikimedia
  Commons (unverified)
- *Architecture*, Paul Klee, 1921 — CORRECTION 2026-07-17
  (ai-art-academy/t-013): previously marked VERIFIED/CC0, but
  api.artic.edu reports `is_public_domain: false` with a live copyright
  notice ("© 2018 Artists Rights Society (ARS), New York / VG
  Bild-Kunst, Bonn") for this object, from Klee's "Magic Squares"
  series painted the year he joined the Bauhaus faculty — re-verify
  before use (unverified):
  https://www.artic.edu/artworks/17540/architecture
- *Fotogramm*, László Moholy-Nagy, 1926 — Metropolitan Museum of Art
  (accession search/265197); expected as open-access image (unverified CC0
  status this session)

**remix_hint:** "Repaint this image as a Bauhaus-school geometric abstraction:
pure circles, triangles, and squares in bold primary colors on a flat plane,
precise linework, no realistic shading"

---

## 17. Gothic Panel Painting (`gothic`)

**Era:** c. 1200-1450 (late-medieval Italy and beyond)

**Key ideas.** Before the Renaissance learned to fake deep space, painters worked on
wooden panels in glowing tempera against skies of solid gold leaf. Gothic painting is
the hinge between the flat, eternal figures of Byzantine art and the breathing bodies
of the Renaissance: artists like Giotto began letting saints stand with real weight,
turn in space, and show tenderness or grief on their faces, while keeping the medieval
love of gold, pattern, and pointed-arch framing. It is devotional art built to shimmer
by candlelight on an altar — the ancestor of every stained-glass-and-gold sacred image
you have ever seen.

**Recognition cues:**
- Burnished gold-leaf backgrounds instead of sky or landscape, often tooled with punched patterns
- Slender, gently swaying figures with small features and haloed heads
- Jewel-toned tempera — ultramarine, vermilion, rose — with fine, decorative linework
- Pointed-arch and gabled frames; multi-panel altarpiece (polyptych) formats
- Space that tilts toward the viewer — thrones and floors read as slightly "wrong," and that is the style, not a mistake

**Notable artists:**
- **Duccio di Buoninsegna** (c. 1255-1319) — The founder of the Sienese school, who
  softened Byzantine rigidity into a new tenderness of line and color.
- **Giotto di Bondone** (1267-1337) — The great pivot of Western painting, who gave
  figures real weight, emotion, and believable space a full century before the
  Renaissance caught up.
- **Simone Martini** (c. 1284-1344) — Sienese master of elegant, courtly line and
  sumptuous gold, whose refinement defined "International Gothic."
- **Fra Angelico** (c. 1395-1455) — Dominican friar and painter who fused Gothic gold
  with early-Renaissance light and perspective; devout, luminous, and precise.

**Example works:**
- *Madonna and Child*, Duccio di Buoninsegna, ca. 1290-1300 — expected at Met Open
  Access (acc. 2004.442) (unverified — museum egress 403 this session)
- *The Epiphany (Adoration of the Magi)*, attributed to Giotto and workshop, ca.
  1320 — expected at Met Open Access (unverified)
- *Saint Andrew*, Simone Martini, ca. 1326 — expected at Met Open Access (Robert
  Lehman Collection) (unverified)
- *The Crucifixion*, Fra Angelico, ca. 1420-23 — expected at Met Open Access
  (unverified)

**remix_hint:** "Repaint this image as a late-medieval Gothic panel painting:
figures on a burnished gold-leaf ground, elongated bodies with gentle S-curves,
jewel-toned tempera, pointed-arch framing, flattened space"

---

## 18. Northern Renaissance (`northern-renaissance`)

**Era:** c. 1420-1570 (the Low Countries and Germany)

**Key ideas.** While Italy rediscovered antiquity, the artists of Flanders and the
Netherlands staged a quieter revolution: oil paint. Building color up in transparent
glazes, they achieved a jewel-like realism the south could not match — every hair,
brass rivet, and distant church tower rendered with almost microscopic devotion. This
is art you lean in to. It hides symbols in ordinary objects (a single candle, a dog, a
convex mirror), sets sacred scenes in real Flemish rooms, and looks out of the frame
with startlingly modern, individual faces. Later, Bruegel turned that same sharp eye on
peasant weddings and snowy villages, inventing the everyday landscape.

**Recognition cues:**
- Astonishing fine detail and hard, crisp edges — texture you can almost feel
- Luminous, glowing color from layered oil glazes; cool, even northern daylight
- Deep, meticulously painted landscapes or interiors behind the main figures
- Symbolic everyday objects loaded with hidden meaning
- Direct, particular, un-idealized faces — real people, not classical types

**Notable artists:**
- **Jan van Eyck** (c. 1390-1441) — The pioneer who pushed oil painting to jewel-like
  perfection; his surfaces still look impossibly real six centuries on.
- **Rogier van der Weyden** (c. 1399-1464) — Master of restrained, piercing emotion,
  whose grieving figures set the standard for devotional feeling in the North.
- **Hans Memling** (c. 1430-1494) — Bruges portraitist of serene, gentle faces,
  hugely popular with the international merchants of his city.
- **Hieronymus Bosch** (c. 1450-1516) — Inventor of teeming, surreal panoramas of
  temptation and torment; a singular imagination centuries ahead of its time.
- **Pieter Bruegel the Elder** (c. 1525-1569) — The great painter of peasant life,
  seasons, and proverbs, who made the humble landscape a serious subject.

**Example works:**
- *The Annunciation*, Jan van Eyck, ca. 1434-36 — expected at National Gallery of Art
  open access (acc. 1937.1.39) (unverified — museum egress 403 this session)
- *Portrait of a Lady*, Rogier van der Weyden, ca. 1460 — expected at National Gallery
  of Art open access (acc. 1937.1.44) (unverified)
- *Tommaso di Folco Portinari and Maria Portinari*, Hans Memling, ca. 1470 — expected
  at Met Open Access (acc. 14.40.626-627) (unverified)
- *The Harvesters*, Pieter Bruegel the Elder, 1565 — expected at Met Open Access
  (acc. 19.164) (unverified)

**remix_hint:** "Repaint this image as an Early Netherlandish oil painting:
microscopic detail, luminous layered glazes, crisp naturalism, cool northern
daylight, and a meticulously rendered landscape or interior behind the figures"

---

## 19. Rococo (`rococo`)

**Era:** c. 1700-1780 (France, then across Europe)

**Key ideas.** After the thunder of the Baroque, the 18th century exhaled into
something lighter and more playful. Rococo is the art of pleasure: garden parties,
flirtation, silk and porcelain, painted in a pastel palette of rose, cream, and
sky-blue with feathery, dissolving brushwork. Where Baroque used dark drama, Rococo
uses soft diffused light and swirling ornamental curves. It can be pure frothy delight
(Boucher, Fragonard) or something quieter and more tender — Chardin, working in the
same era, turned the same soft light on a soap bubble or a kitchen still life and found
real poetry there. It is a wonderful movement for learning that lightness is its own
kind of skill.

**Recognition cues:**
- Pastel palette — rose pink, powder blue, cream, mint — and gilded highlights
- Soft, diffused light with no harsh shadows; a hazy, tender atmosphere
- Feathery, loose, sparkling brushwork, especially in silk and foliage
- Playful curves and asymmetric ornament (shells, scrolls, garlands) everywhere
- Light-hearted subjects: courtship, music, gardens, mythological romps

**Notable artists:**
- **Antoine Watteau** (1684-1721) — Inventor of the dreamy *fête galante* — elegant
  figures drifting through parkland — and a poet of wistful, fleeting pleasure.
- **François Boucher** (1703-1770) — The decorative genius of the age, favorite
  painter of Madame de Pompadour, all rose-and-blue mythology and charm.
- **Jean-Honoré Fragonard** (1732-1806) — The most dazzling brush of late Rococo,
  whose flickering strokes turn silk and leaves into pure sparkle.
- **Jean-Baptiste-Siméon Chardin** (1699-1779) — The quiet counterweight: still lifes
  and domestic scenes of grave, luminous simplicity that later painters revered.

**Example works:**
- *Mezzetin*, Antoine Watteau, ca. 1718-20 — expected at Met Open Access (acc.
  34.138) (unverified — museum egress 403 this session)
- *The Toilette of Venus*, François Boucher, 1751 — expected at Met Open Access
  (acc. 20.155.9) (unverified)
- *The Love Letter*, Jean-Honoré Fragonard, early 1770s — expected at Met Open
  Access (acc. 49.7.49) (unverified)
- *Soap Bubbles*, Jean-Baptiste-Siméon Chardin, ca. 1733-34 — expected at Met Open
  Access (acc. 49.24) (unverified)

**remix_hint:** "Repaint this image as a Rococo oil painting: pastel palette of rose,
sky-blue, and cream, feathery loose brushwork, soft diffused light, playful
ornamental curves, and a light, airy mood"

---

## 20. Symbolism (`symbolism`)

**Era:** c. 1880-1910 (France, Belgium, and beyond)

**Key ideas.** While the Impressionists painted sunlight on water, the Symbolists
turned inward, toward dreams, myths, and the unseen. Reacting against both cold realism
and mere prettiness, they wanted painting to *suggest* rather than describe — to give
form to longing, mystery, death, and the sacred. Expect twilight color, allegorical
figures, and scenes that feel like something remembered from a dream you cannot quite
place. Symbolism is the mood-music of art history, and it fed straight into
Expressionism, Surrealism, and modern fantasy imagery.

**Recognition cues:**
- Dreamlike, mysterious mood — reverie rather than a report of the real world
- Mythological, allegorical, or spiritual subjects, often melancholy or uncanny
- Muted, twilight color and soft, glowing, sourceless light
- Flattened, decorative, or hazy space that resists ordinary depth
- A sense of hidden meaning — the picture is a riddle or a symbol, not a scene

**Notable artists:**
- **Gustave Moreau** (1826-1898) — Painter of jewel-encrusted myths and femmes
  fatales, whose shimmering, detailed fantasies made him the movement's grand elder.
- **Pierre Puvis de Chavannes** (1824-1898) — Master of pale, calm, dreamlike murals
  whose flattened simplicity quietly influenced nearly every modernist who followed.
- **Arnold Böcklin** (1827-1901) — Swiss painter of haunting mythologies; his
  brooding *Isle of the Dead* became one of the most reproduced images of its era.
- **Odilon Redon** (1840-1916) — Poet of the strange and the floating — dream-eyes,
  spiders, and, later, radiant flowers in luminous pastel color.

**Example works:**
- *Oedipus and the Sphinx*, Gustave Moreau, 1864 — expected at Met Open Access (acc.
  21.134.1) (unverified — museum egress 403 this session)
- *Isle of the Dead*, Arnold Böcklin, 1880 — expected at Met Open Access (acc. 26.90)
  (unverified)
- *The Shepherd's Song*, Pierre Puvis de Chavannes, 1891 — expected at Met Open
  Access (acc. 06.177) (unverified)
- *Vase of Flowers*, Odilon Redon, ca. 1914 — expected at Met Open Access (acc.
  16.20) (unverified)

**remix_hint:** "Repaint this image as a Symbolist painting: dreamlike mysterious
mood, muted twilight color, mythic and allegorical atmosphere, soft glowing light,
and a sense of reverie rather than plain reality"

---

## 21. Neo-Impressionism / Pointillism (`pointillism`)

**Era:** c. 1884-1910 (France and Belgium)

**Key ideas.** Georges Seurat loved what Impressionism had discovered about light but
wanted to put it on a scientific footing. Instead of loose dabs mixed on the palette,
he built entire canvases from thousands of tiny, separate dots of pure color, placed so
your eye — not the brush — does the blending. Up close it is a field of confetti; step
back and it fuses into a glowing, oddly still, luminous whole. His followers, the
Neo-Impressionists, spread this "divisionism" across France and Belgium. It is the most
*method-driven* movement in the curriculum, which makes it a brilliant one to teach:
the technique itself is the lesson.

**Recognition cues:**
- Whole image built from tiny, distinct dots or short dashes of pure color
- Colors kept separate and left to blend optically in the viewer's eye
- An even, all-over, almost woven surface texture
- Luminous, balanced light and a calm, frozen, monumental stillness
- Complementary color pairs (orange/blue, red/green) placed side by side to vibrate

**Notable artists:**
- **Georges Seurat** (1859-1891) — Inventor of pointillism, who built vast, serene,
  scientifically composed scenes from pure dots; dead at just 31.
- **Paul Signac** (1863-1935) — Seurat's great champion, who carried divisionism
  forward into brighter, mosaic-like harbors and coastlines after Seurat's death.
- **Henri-Edmond Cross** (1856-1910) — Painter of luminous Mediterranean color whose
  broad, tile-like touch helped point the way toward Fauvism.
- **Théo van Rysselberghe** (1862-1926) — The leading Belgian Neo-Impressionist, who
  brought the dot-technique to elegant, sensitive portraiture.

**Example works:**
- *Circus Sideshow (Parade de cirque)*, Georges Seurat, 1887-88 — expected at Met
  Open Access (acc. 61.101.17) (unverified — museum egress 403 this session)
- *Study for "A Sunday on La Grande Jatte"*, Georges Seurat, 1884 — expected at Met
  Open Access (acc. 51.112.6) (unverified)
- *The Jetty at Cassis, Opus 198*, Paul Signac, 1889 — expected at Met Open Access
  (acc. 1999.363.75) (unverified)
- *Coast Scene (Provence)*, Henri-Edmond Cross, ca. 1891-92 — expected at open-access
  collection (Met / AIC) (unverified)

**remix_hint:** "Repaint this image using pointillist technique: thousands of tiny
separate dots of pure unmixed color that blend in the eye, a luminous divisionist
surface, even all-over stippling, and bright balanced light"

---

## Lesson-only vs remixable

Every movement above maps to a remix config (mode `prompt` to start; t-003/t-004
decide where LoRAs help). Expected remix quality, flagged honestly:

**Strong remix candidates (ship first):** `ukiyo-e`, `impressionism`,
`post-impressionism`, `art-nouveau`, `expressionism`, `baroque`, `romanticism`,
`renaissance`, `realism`, `neoclassicism`, `northern-renaissance`, `rococo`,
`symbolism`, `pointillism`. These are heavily represented in
FLUX/Kontext training data and their styles transfer while preserving the
user's composition — the core Academy promise. `neoclassicism`'s smooth,
invisible-brushwork finish and restrained palette should be an easy transfer;
watch that the model doesn't over-flatten skin/fabric texture into a "marble
statue" look when the source photo has strong texture. `northern-renaissance`
and `rococo` are painterly oil styles the model handles gracefully — the risk is
under-cooking (a generic "old painting" look); lean on the specifics in the
remix_hint (microscopic glazed detail vs. feathery pastel brushwork). `symbolism`
transfers as mood and palette more than as a hard signature, so results read as
"dreamy twilight repaint" — set that expectation in UI copy. `pointillism` is the
strongest *technique* transfer in the set (the dot-field is unmistakable), but the
model may render the dots too coarse or too sparse at low resolution — t-004 should
check dot density and consider a higher output size for this style.

**Good but watch the output:** `greek-vase-painting` and `byzantine-mosaic` are
strong graphic transformations (silhouette-on-terracotta, tesserae-and-gold) that
usually look delightful, but the model may add vessel curvature/border framing or
lose fine facial detail — test in t-004. `illuminated-manuscript` remixes well as
"miniature with gold border," though the page/text context can crowd small
subjects. `gothic` shares the gold-ground look of `byzantine-mosaic` and
`illuminated-manuscript`: the burnished gold background and pointed-arch framing
transfer well, but the model may add unwanted altarpiece framing or halos to secular
subjects — the remix_hint keeps "flattened space" and "gold-leaf ground" without
forcing a religious frame; watch that portraits don't sprout haloes. `bauhaus` spans three quite different hands (Kandinsky's spiritual
geometry, Klee's whimsical pictograms, Moholy-Nagy's camera-less photograms) —
expect the model to default to a generic "geometric abstract art" look rather
than a specific recognizable Bauhaus signature; the prompt template should pick
one sub-style (likely Kandinsky's point/line/plane vocabulary) rather than
average all three.

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
Munch 1944, Mondrian 1944, Kandinsky 1944, Mucha 1939, Kirchner 1938). No
living or post-1990 deceased artist appears anywhere. Picasso (d. 1973) and
Braque (d. 1963) are mentioned in Cubism lesson prose as historical context
only — no works of theirs are exhibited, remixed, or attributed as style
targets. Every example work predates 1930, so all are US public domain; the
most recent is Moholy-Nagy's Fotogramm (1926), with van Doesburg's
Counter-Composition V (1924), the Klimt (1907-08), Marc (1913), and Mondrian
(1921) works also comfortably pre-1930.

**v1.1 expansion (2026-07-16) re-check.** The five added movements (§17-21) clear
the PUBLIC-DOMAIN-POLICY.md §1.3 both-prongs rule (artist died before 1956 AND work
published 1930 or earlier) with margin. Newest death among the additions is Paul
Signac (d. 1935) — still comfortably inside the "died 1953 or earlier" statement
above; every other added artist died between 1319 and 1926. The newest added example
work is Redon's *Vase of Flowers* (ca. 1914), so Moholy-Nagy's 1926 Fotogramm remains
the most recent example work in the whole curriculum. Fauvism was deliberately *not*
added this pass: its central figures (Matisse, Derain, both d. 1954) pass prong 1 but
their signature works are post-1930, which the policy flags as "mostly ineligible" —
excluded to stay clear of the boundary. All §17-21 example-work URLs are marked
`(unverified)` because museum egress is 403-blocked this session; they carry real
accession numbers to spot-check when a session with open museum egress runs (batches
with t-008/t-013).
