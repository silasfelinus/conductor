# AI Art Academy — Teaching Notes & Lesson Scaffolding

date: 2026-07-16
task: ai-art-academy/t-010 (continuous-improvement cycle; options b + d)
status: draft for review (content complete; example works marked unverified pending open museum egress)

This is the pedagogy layer that sits on top of `docs/curriculum-outline.md`. The outline
is the *content* (movements, artists, example works, remix hints); this file is the
*teaching structure* — a reusable lesson scaffold, per-style teaching notes, and fully
worked example lessons — so every style page in the Academy teaches the same way and
converts cleanly into front-end lesson copy.

Companion files:
- `docs/curriculum-outline.md` — the 22 movements (source of truth for facts/works/hints)
- `docs/style-lora-registry.md` — per-style remix mode (`prompt` vs `lora`) + `prompt_hint`
- `PUBLIC-DOMAIN-POLICY.md` — the eligibility rule every example work must pass (§1.3) and
  the provenance schema (§3)
- `DESIGN-BRIEF.md` — product shape (Timeline / Style pages / Remix Studio / Style Lab)

---

## 1. Purpose & where this shows up in the product

Per the DESIGN-BRIEF, a learner moves **Timeline → Style page → Remix Studio**: they meet
a movement in historical context, read its style page, then remix a starter image (or
their own upload) in that style and reflect on the result. The scaffold below is written
to drive the **Style page + Remix Studio pairing** — the "read it, then try it" loop that
is the core Academy promise. Each beat maps to a slot a front-end component can render, so
this doc is also the content contract for the lesson-detail component (see follow-on
t-023).

The teaching goal is not "make a pretty picture." It is **visual literacy**: after a
lesson, a learner should be able to *recognize* the movement in the wild and *explain*
one thing about why it looks the way it does. The remix is the hook and the memory aid,
not the point.

---

## 2. The reusable lesson scaffold (8 beats)

Every style lesson follows the same eight beats. Keep each beat short — this is a museum
wall-label, not a textbook. Fields in `code` map to data already in the curriculum outline
or style registry.

1. **Hook** *(1-2 sentences).* One vivid, human way in. Why should anyone care about this
   movement today? Lead with a surprise or a connection to something the learner already
   knows (comics, posters, cinema lighting, video-game art).

2. **Look First** *(recognition drill).* Before any history, show the learner *how to
   see* it. Present the movement's `recognition_cues` as a short "spot these five things"
   checklist over an example work. This is the highest-retention beat — recognition is the
   skill that lasts.

3. **The Big Idea** *(1 short paragraph).* The `key_ideas` distilled to a single throughline
   — the problem these artists were solving or the thing they cared about. One idea, not a
   survey.

4. **Meet the Makers** *(2-4 artist cards).* Pull from `notable_artists`: name, dates, and
   one memorable sentence each. All artists are long dead and public-domain (that is the
   Academy boundary, not an accident — see beat 8). Prefer the human, surprising detail
   over the résumé.

5. **See It** *(2-4 example works).* The movement's `example_works`, each with a one-line
   "what to notice." Every image carries its provenance record (PUBLIC-DOMAIN-POLICY.md §3);
   no record → the image does not ship.

6. **Try It** *(the remix exercise — the interactive heart).* Send a starter image through
   the Remix Studio using this style's `remix_hint` / registry `prompt_hint`. Give the
   learner:
   - **the instruction** (the prompt-mode string or LoRA, from the registry),
   - **what to expect** (which recognition cues should appear in the output),
   - **common failure modes** (what tends to go wrong — see per-style table §3),
   - **how to iterate** (one concrete knob to turn: strength, a phrase to add/remove,
     a different starter image).

7. **Reflect** *(2-3 prompts).* Cheap comprehension + critique questions that close the
   loop: *Which recognition cue survived the remix best? Which got lost? Does the result
   feel like the movement, or just "an old painting"? Why might that be?* This converts a
   fun output into an actual observation.

8. **Provenance & ethics note** *(standing footer).* One plain-language line: every artwork
   here is public-domain and every artist died long ago; the Academy never imitates living
   creators. Links to the policy. This is a teachable value, not fine print — say it out loud.

### Scaffold-to-data map (for the component builder, t-023)

| Beat | Source field | Notes |
|------|--------------|-------|
| Hook | (authored per style, this file / seed) | short, human |
| Look First | `recognitionCues` (academyStyles.ts) | render as a checklist |
| The Big Idea | `keyIdeas` / curriculum `Key ideas` | one paragraph max |
| Meet the Makers | `notable_artists` (curriculum) | 2-4 cards |
| See It | `example_works` (curriculum) + provenance record | image + "what to notice" |
| Try It | registry `mode` + `prompt_hint`/`trigger` + `remix_hint` | the Remix Studio call |
| Reflect | (authored, reusable prompts) | critique/comprehension |
| Provenance | PUBLIC-DOMAIN-POLICY.md | standing footer |

---

## 3. Per-style teaching notes (all 22 movements)

Remix-difficulty tiers match `curriculum-outline.md`'s "Lesson-only vs remixable" section:
**Easy** = strong transfer, ship first; **Medium** = good but watch the output;
**Hard** = the honest remix fights the style (keep the lesson, frame the remix playfully).
"Remix mode" is from `style-lora-registry.md` (note the registry uses a few different
slugs — e.g. `renaissance-fresco`, `baroque-chiaroscuro`, `post-impressionism-van-gogh`).

| # | Movement (`slug`) | Remix mode | Difficulty | Teaching angle (the one idea) | Key failure mode / watch-for |
|---|-------------------|------------|-----------|-------------------------------|------------------------------|
| 1 | Greek Vase Painting (`greek-vase-painting`) | prompt | Medium | Confident line & silhouette; painting before canvas | May add vessel curvature/border framing; loses fine facial detail |
| 2 | Byzantine Mosaic (`byzantine-mosaic`) | prompt | Medium | Pictures built from light-catching tiles; the eternal, not the real | Grout/tesserae texture can flatten faces; gold field can swallow the subject |
| 3 | Illuminated Manuscript (`illuminated-manuscript`) | lora | Medium | Painting that lived inside books; gold + margins | Page/text context crowds small subjects |
| 4 | Renaissance (`renaissance` / `renaissance-fresco`) | lora (Raphael) | Easy | Artists as scientists of seeing (perspective, sfumato) | Under-cooks into generic "old master"; keep sfumato + balance explicit |
| 5 | Baroque (`baroque` / `baroque-chiaroscuro`) | prompt | Easy | A single shaft of light makes a picture into theater | Model may just darken the photo instead of restructuring light |
| 6 | Neoclassicism (`neoclassicism`) | prompt | Easy | Noble simplicity; line over paint; civic seriousness | Over-flattens texture into a "marble statue" look |
| 7 | Ukiyo-e (`ukiyo-e`) | prompt | Easy | Art for everyone; flat color + bold line; the manga ancestor | Adds spurious calligraphy/stamps/borders — append "no text, no stamps, no border" |
| 8 | Romanticism (`romanticism`) | prompt | Easy | Feeling first; the sublime; nature dwarfs us | Reads as "dramatic sky filter"; push mood + scale, not just clouds |
| 9 | Realism (`realism`) | prompt | Easy | Dignity for ordinary life; paint what you actually see | Subtle style — can look like a lightly-graded photo; lean on earthy palette |
| 10 | Impressionism (`impressionism`) | lora | Easy | Painting light, not things; broken color your eye blends | Can over-blur into mush; keep "broken brushstrokes" + high-key palette |
| 11 | Post-Impressionism (`post-impressionism` / `-van-gogh`) | lora (Van Gogh) | Easy | Structure & feeling beyond fleeting light; four personal answers | The Van Gogh LoRA pulls toward one artist; movement prompt keeps it broad |
| 12 | Art Nouveau (`art-nouveau`) | lora | Easy | Beauty everywhere; the whiplash line; posters as fine art | Great transfer; watch for over-busy borders eating the subject |
| 13 | Expressionism (`expressionism`) | lora (Kirchner) | Easy | Paint the world as it *feels*; "wrong" color is truer | LoRA leans Kirchner-specific; A/B vs the movement prompt (registry note) |
| 14 | Cubism (`cubism`) | prompt | **Hard** | One subject from many viewpoints at once | "Preserve composition" fights faceting — often a shallow "crystallized photo" |
| 15 | De Stijl (`de-stijl`) | prompt | **Hard** | A universal language of line + primary color | A faithful remix discards the photo entirely — frame it playfully ("Mondrian-ify") |
| 16 | Bauhaus (`bauhaus`) | prompt | Medium | Art = design; a shared vocabulary of shape + color | Three distinct hands average into generic "geometric abstract"; pick one (Kandinsky) |
| 17 | Gothic Panel Painting (`gothic`) | prompt | Medium | The hinge from Byzantine gold to Renaissance weight | "Gothic" pulls toward horror; may bolt haloes/altarpiece frames onto secular subjects |
| 18 | Northern Renaissance (`northern-renaissance`) | prompt | Easy | Oil paint's jewel-like realism; symbols hidden in objects | Under-cooks into "generic old oil"; differentiators are microscopic detail + deep sharp background |
| 19 | Rococo (`rococo`) | prompt | Easy | Lightness as a skill; pleasure, pastel, soft light | Keeps the photo's saturated/contrasty color — push high-key pastel |
| 20 | Symbolism (`symbolism`) | prompt | Easy | Suggest, don't describe; dreams, myth, the unseen | Loosest visual signature — transfers as mood/palette; guard vs modern digital-surreal |
| 21 | Neo-Impressionism / Pointillism (`pointillism`) | prompt | Easy | The technique *is* the lesson; dots your eye blends | Dots render too coarse/sparse at low res — evaluate at higher output size |
| 22 | Suprematism (`suprematism`) | prompt | **Hard** | Feeling over depiction; geometry alone as the subject | Faithful remix discards the source subject almost entirely — frame as a reduction exercise, not a restyle (see `docs/suprematism-lesson.md`, this movement's dedicated worked lesson) |

---

## 4. Worked example lessons

Three full instantiations of the §2 scaffold, chosen to span the range: a strong
non-Western remixer (Ukiyo-e), the canonical crowd-pleaser (Impressionism), and a
technique-driven new addition (Pointillism). These are written as ready-to-ship lesson
copy — a content author or the seed pipeline can lift them close to verbatim.

A fourth full worked lesson exists for Suprematism (movement #22, the newest and the
curriculum's only "Hard, discards-the-subject" case) but lives in its own file,
`docs/suprematism-lesson.md`, rather than inline here — it was authored after this
document and follows the same eight-beat scaffold.

### 4.1 Ukiyo-e — "Pictures of the Floating World"

- **Hook.** The bold, flat, wave-and-outline look behind a thousand posters, album
  covers, and manga panels started as cheap, mass-produced prints for ordinary people in
  1600s-1800s Japan — and when a batch reached Paris, it rewired Western art overnight.

- **Look First — spot these five:** (1) flat planes of color with almost no shading;
  (2) confident black outlines around everything; (3) bold, cropped framing that slices
  figures off at the edge; (4) stylized nature — claw-like waves, banded clouds, patterned
  rain; (5) skies that fade smoothly from deep blue to pale (bokashi).

- **The Big Idea.** This was a team art form (designer → carver → printer) made to be
  affordable and popular, so it prized clear, reproducible design over fussy realism —
  the same instinct that makes great graphic design and comics work today.

- **Meet the Makers.** *Katsushika Hokusai (1760-1849)* — restless genius of landscape
  who made Mount Fuji a global icon and claimed he was only getting good at 70.
  *Utagawa Hiroshige (1797-1858)* — poet of rain, snow, and moonlight on Japan's roads.
  *Kitagawa Utamaro (1753-1806)* — the great portraitist of women, master of the
  intimate close-up.

- **See It.** *Under the Wave off Kanagawa (The Great Wave)*, Hokusai, ca. 1830-32 —
  notice the claw-foam and how tiny Mt. Fuji sits under the wave's arc (Met Open Access,
  CC0, curriculum-verified). Plus a Hiroshige rain scene — watch how the rain is drawn as
  straight ruled lines.

- **Try It.** Remix mode: **prompt** (registry `ukiyo-e`).
  Instruction: *"Redraw this image as a Japanese ukiyo-e woodblock print: flat color
  planes, bold black outlines, stylized waves and clouds, subtle woodgrain texture — no
  text, no stamps, no border."*
  Expect: flat color, hard outlines, a graphic poster-like flatten.
  Common failure: the model sprinkles fake Japanese text, red seals, or a border frame —
  that is why the instruction explicitly forbids them.
  Iterate: if it stays too photographic, add "strong black outlines, no gradients" and try
  a starter image with a simple, bold subject (the style hates clutter).

- **Reflect.** Which survived best — your subject's outline or its color? Ukiyo-e throws
  away realistic shading; did losing the shadows make the image read as *flatter and
  bolder*, or just *unfinished*? Why might flatness have been a feature, not a bug, for a
  print sold cheap by the thousand?

- **Provenance & ethics.** Every artist here died over 150 years ago and every print shown
  is public-domain. The Academy teaches and remixes historical styles — never living
  artists' work. (See PUBLIC-DOMAIN-POLICY.md.)

### 4.2 Impressionism — "Painting the Light, Not the Thing"

- **Hook.** Up close it looks like confetti; step back and it becomes sunlight on water.
  That magic trick — and the outdoor, everyday-life subjects — got these painters laughed
  out of the official salon, so they threw their own show and won.

- **Look First — spot these five:** (1) visible broken brushstrokes, little dabs of color
  side by side; (2) a bright, high-key palette; (3) colored shadows (often violet-blue),
  almost never black; (4) everyday modern subjects — cafés, boating, gardens; (5) soft
  edges everywhere — forms dissolve when you lean in.

- **The Big Idea.** They tried to paint not objects but the *light bouncing off* objects
  at one fleeting moment — which meant working fast, outdoors, in unmixed dabs your eye
  blends at a distance.

- **Meet the Makers.** *Claude Monet (1840-1926)* — painted haystacks and cathedrals over
  and over as the light changed. *Berthe Morisot (1841-1895)* — founding member whose
  feathery brushwork made domestic scenes shimmer. *Camille Pissarro (1830-1903)* — the
  steady mentor, the only one to show in all eight Impressionist exhibitions.

- **See It.** *Two Sisters (On the Terrace)*, Renoir, 1881 — notice the dappled color and
  how the background dissolves into pure light (Art Institute of Chicago, CC0,
  curriculum-verified). Plus a Monet water-lilies work — look for the violet-blue shadows.

- **Try It.** Remix mode: **lora** (registry `impressionism`, UmeAiRT FLUX LoRA; trigger
  `impressionist`) — *or* the base prompt, which is a good A/B here (the LoRA author admits
  FLUX already does impressionism well).
  Instruction: *"Repaint this image as a French Impressionist oil painting with visible
  broken brushstrokes, dappled natural light, and a bright plein-air palette."*
  Expect: broken color, softened edges, a sunnier palette.
  Common failure: over-blurring into mush (edges gone, no brush texture) — that is *not*
  the same as broken brushwork.
  Iterate: if it's muddy, add "distinct visible brushstrokes, high-key color" and lower the
  style strength a notch so your subject stays legible.

- **Reflect.** Did the remix keep your subject *recognizable* while changing *how* it's
  painted? That balance — new style, same composition — is exactly the Academy's promise.
  Where did the light get brighter, and did any real detail get lost in the dabs?

- **Provenance & ethics.** All artists shown died before 1927; all works are public-domain
  and pre-1930. No living artist is imitated. (See PUBLIC-DOMAIN-POLICY.md.)

### 4.3 Pointillism — "The Technique Is the Lesson"

- **Hook.** One painter got so curious about how color works that he built entire huge
  canvases out of thousands of separate dots — and let your *eye*, not his brush, mix them.

- **Look First — spot these five:** (1) the whole image is tiny distinct dots or dashes;
  (2) colors are kept separate, not blended on the palette; (3) an even, all-over, almost
  woven surface; (4) a calm, frozen, oddly monumental stillness; (5) complementary pairs
  (orange/blue, red/green) sitting side by side to make the color "vibrate."

- **The Big Idea.** Georges Seurat wanted to put Impressionism on a *scientific* footing:
  place pure colors next to each other so they blend optically in the viewer's eye instead
  of on the palette. It's the most method-driven movement in the whole curriculum — which
  is exactly why it's such a satisfying one to *try*.

- **Meet the Makers.** *Georges Seurat (1859-1891)* — invented pointillism and died at 31.
  *Paul Signac (1863-1935)* — carried divisionism forward into brighter, mosaic-like
  harbors. *Henri-Edmond Cross (1856-1910)* — luminous Mediterranean color that pointed
  toward Fauvism. *Théo van Rysselberghe (1862-1926)* — brought the dot-technique to
  elegant portraiture.

- **See It.** *Circus Sideshow (Parade de cirque)*, Seurat, 1887-88 — lean in to see the
  dots, then step back and watch them fuse (expected at Met Open Access, acc. 61.101.17;
  URL unverified this session — museum egress blocked). Plus a Signac harbor scene — notice
  the bigger, tile-like touches.

- **Try It.** Remix mode: **prompt** (registry `pointillism`, `prompt_hint`).
  Instruction: *"Repaint this image using pointillist technique: thousands of tiny separate
  dots of pure unmixed color that blend in the eye, a luminous divisionist surface, even
  all-over stippling, bright balanced light, in the manner of Seurat and Signac."*
  Expect: a visible dot-field, luminous even color, a calm stillness.
  Common failure: at small output sizes the "dots" come out too coarse, or the model
  quietly reverts to ordinary Impressionist dabs (no real stippling).
  Iterate: render at a **larger output size** than usual (this style needs the resolution
  to hold its dots), and add "fine even stippling, distinct dots" if the texture is too
  loose. This is the top LoRA-upgrade candidate — see registry S-7.

- **Reflect.** Get close to your result, then step back: does the dot-field actually fuse
  into a coherent image, or stay as scattered specks? Seurat's whole bet was that your eye
  does the mixing — did it work here? What did the even, all-over texture do to the *mood*
  compared to your original photo?

- **Provenance & ethics.** Every artist here died between 1891 and 1935; all example works
  predate 1930 and are public-domain. Pointillism ships as a *movement/technique* lesson —
  no living artist is imitated. (See PUBLIC-DOMAIN-POLICY.md §1.3.)

---

## 5. Provenance & the dead-artists boundary (why this is baked into teaching)

The Academy's hard rule (DESIGN-BRIEF.md, enforced by PUBLIC-DOMAIN-POLICY.md §1.3):
a work is teachable/remixable only if **both** the artist died more than 70 years ago
(before 1956 in 2026) **and** the work was published on or before the rolling US cutoff
(1930 or earlier in 2026). Every image the Academy ships carries the §3 provenance record
(workTitle, artist, artistDied, year, collection, accessionId, sourceUrl, license,
licenseTermsUrl, retrievedDate) — no record, no ship.

This is a **teaching point in beat 8**, not just compliance: learners should leave knowing
*why* we remix Hokusai and Seurat but never a living illustrator. Frame it as respect for
creators, not as a legal disclaimer.

Note for this cycle (2026-07-16): the five newest movements' example-work URLs are marked
`(unverified)` in the curriculum outline because museum egress is 403-blocked in the
current session. They carry real accession numbers and should be spot-checked from a
session with open museum egress (batches with t-008/t-013 image work) before any of those
images ship as seed data.
