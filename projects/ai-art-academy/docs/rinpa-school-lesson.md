# AI Art Academy — Rinpa School Lesson Module

Date: 2026-08-07  
Task: `ai-art-academy/t-010` continuous-improvement cycle, option (d) curriculum depth  
Status: ready for front-end content integration

This module gives Rinpa School the same deeper eight-beat treatment already used by the Academy's dedicated Suprematism, Ancient Egyptian Painting, and Fayum Mummy Portraits lessons. It follows the scaffold in `docs/teaching-notes.md` and deliberately reuses the facts, recognition cues, verified example works, and remix direction already established in `docs/curriculum-outline.md` §46 rather than introducing a second source of historical claims.

## Lesson metadata

- **Movement:** Rinpa School
- **Slug:** `rinpa-school`
- **Era:** early 1600s–mid-1800s (Edo period, Japan)
- **Region:** Kyoto and Edo, Japan
- **Primary makers:** Ogata Kōrin (1658–1716), Sakai Hōitsu (1761–1828), Suzuki Kiitsu (1796–1858)
- **Remix mode:** prompt
- **Difficulty:** medium
- **Core warning:** a successful remix has to hold extreme decorative flatness (gold ground, empty space) and close natural observation (a few precise botanical details) together at once, rather than settling for only one half of that combination

## 1. Hook

What if a painting were also a piece of furniture — something you lived beside, not just looked at?

Rinpa artists made images meant to fold, gleam, and catch lamplight across a room: screens, scrolls, fans, lacquer boxes. A single spray of irises can float on a wall of gold leaf with no horizon, no shadow, no described room at all — and still read, instantly, as recognizably natural.

## 2. Look First

Spot these six things:

1. A broad, unmodeled ground of gold or silver leaf standing in for ordinary depth or setting.
2. Motifs cropped by the edge of the screen or scroll, arranged off-center rather than centered.
3. Bold, simplified silhouettes paired with a handful of sharply observed botanical details — flatness and close observation in the same image.
4. Flowers, leaves, waves, or grasses repeated as visual rhythm rather than laid out as a naturalistic, evenly-lit scene.
5. Soft-edged pools of wet ink and color ("tarashikomi") bleeding into shape, often sitting right next to a crisp contour line or metallic ground.
6. Generous deliberate empty space, with the subject floating rather than occupying a described room, garden, or landscape.

The quickest recognition test is the flatness-plus-detail combination: if a scene keeps naturalistic shading and a described setting, it has borrowed Rinpa's *subject matter* (flowers, seasons) without adopting its pictorial *logic* (flat gold ground, cropped asymmetry, tarashikomi bloom).

## 3. The Big Idea

Rinpa is not a print culture and not a single continuous workshop. It is a decorative painting tradition — screens, scrolls, fans, lacquer, ceramics, textiles — organized around the collision of extreme flatness with close natural observation, and it survived by deliberate revival rather than unbroken teacher-to-student lineage. Ogata Kōrin looked back a full generation to earlier Kyoto decorative masters; a century later Sakai Hōitsu rediscovered and codified Kōrin's vocabulary in Edo, compiling a facsimile of Kōrin's own work; Hōitsu's pupil Suzuki Kiitsu then carried that revival into a sharper, more graphic nineteenth-century form.

That makes Rinpa a useful counterpoint to the Academy's other Japanese movement, Ukiyo-e (§7): Ukiyo-e is reproducible woodblock print culture — actors, courtesans, travel — while Rinpa is brushed, one-of-a-kind, and built for interior spaces rather than mass circulation. The lesson should keep that distinction explicit rather than let both movements blur into one generic "traditional Japanese art" bucket.

## 4. Meet the Makers

### Ogata Kōrin (1658–1716)

The movement's central namesake figure. His *Flowers of Spring and Autumn* combines highly stylized natural elements with formal Chinese-style ink training — the Metropolitan Museum of Art's own description of the work. Kōrin worked a generation after the earlier Kyoto decorative masters he revived, rather than inventing the vocabulary from nothing.

### Sakai Hōitsu (1761–1828)

Led the later Edo Rinpa revival roughly a century after Kōrin. The Met identifies him as one of the most important late-Edo Rinpa painters, working in seasonal, literary compositions — his *Activities of the Twelve Months* tracks court ritual and seasonal custom across a full year in eleven surviving hanging scrolls. He compiled a facsimile reproduction of Kōrin's work, making him as much a historian of the tradition as a practitioner of it.

### Suzuki Kiitsu (1796–1858)

Hōitsu's leading pupil, and the tradition's latest phase taught here. His botanical forms are sharper and more graphic than his teacher's — visible in *Irises and Moth*, which returns to a motif Kōrin himself made famous.

All three clear PUBLIC-DOMAIN-POLICY.md's death-date threshold with wide margin. Per §2, an artist's death date alone does not settle an individual displayed work's rights, so every example below carries its own institution-confirmed status rather than inheriting one from the artist.

## 5. See It

These examples are already recorded as verified public-domain works in `docs/curriculum-outline.md` §46, all confirmed live via the Metropolitan Museum of Art's Collection API.

### *Flowers of Spring and Autumn*, Ogata Kōrin, shortly after 1701

A pair of panels in ink and color on cryptomeria wood. Notice how the highly stylized botanical motifs sit against an unmodeled ground while retaining enough natural specificity to identify each plant.

### *Activities of the Twelve Months*, Sakai Hōitsu, late 1790s

Eleven hanging scrolls (of a set of twelve) in ink and color on silk, tracking court ritual and seasonal custom across a full year. Look for how a whole calendar's worth of narrative content is organized through repeated seasonal motifs rather than continuous scenic depth.

### *Cherry and Maple Trees*, Sakai Hōitsu, early 1820s

A pair of six-panel folding screens in ink, color, and gold leaf on paper, organized around spring and autumn plants for strong decorative impact. This is the clearest single example of the gold-ground-plus-cropped-asymmetry combination described in beat 2.

### *Irises and Moth*, Suzuki Kiitsu, ca. 1850

A hanging scroll in ink and color on silk: a single spray of irises — a motif reaching back to Kōrin's own famous *Irises* screens — with a moth worked into the composition. Useful for showing how little a Rinpa composition needs in order to read as complete.

## 6. Try It

### Instruction

> Repaint this image as a Rinpa-school folding-screen composition: a broad gold- or silver-leaf ground with no ordinary horizon, an asymmetrical cropped arrangement of seasonal flowers, grasses, or water, bold simplified silhouettes mixed with a few precise botanical details, pooled ink-and-color edges, rhythmic repetition, and generous empty space in place of realistic depth. Preserve the source composition and subject.

### What to expect

- The background should collapse into a flat metallic or near-flat field, not a described room or landscape.
- The subject should shift toward bold silhouette, with only a few areas kept sharply, naturalistically detailed.
- Composition should read as asymmetrical and edge-cropped rather than centered.
- Soft-edged, pooled color transitions should appear somewhere in the image, distinct from the crisp contour lines elsewhere in it.
- The original subject should stay identifiable even as its setting and shading logic change substantially.

### Common failure modes

- **Gold wallpaper filter:** the model adds a gold or metallic tint over the existing photographic scene without removing the described depth, camera perspective, or lighting.
- **Uniform gilding:** the whole image flattens evenly instead of holding flatness (ground) and close observation (botanical detail) in tension — the core Rinpa signature per beat 3.
- **Centered symmetry:** the composition stays centered and fully contained instead of asymmetrical and edge-cropped.
- **Missing tarashikomi:** color fills flatly everywhere with no soft-edged pooled bleed anywhere in the image.
- **Ukiyo-e drift:** the result reads as a woodblock print (visible line-block texture, flat uniform color fields, print-culture subject matter like actors or travel scenes) rather than a brushed decorative panel — watch for this specifically since Rinpa and Ukiyo-e share a country and era but not a visual logic (see beat 3).

### How to iterate

- If the background stays a described scene, emphasize **"a single unmodeled field of gold or silver leaf, no horizon, no room."**
- If the whole image goes uniformly flat, add **"a few sharply observed botanical details kept naturalistic against the flat ground"** to restore the flatness-plus-detail contrast.
- If the composition stays centered, ask for **"asymmetrical, cropped by the frame edge, not centered."**
- If nothing pools or bleeds, add **"soft pooled ink-and-color edges (tarashikomi) beside crisp contour line."**
- If the result reads as a woodblock print, remove any reference to prints/blocks and reinforce **"brushed, one-of-a-kind panel painting, not a print."**

## 7. Reflect

1. Which change made the result feel most Rinpa: the gold ground, the cropped asymmetry, the pooled color, or the mix of flat silhouette with sharp botanical detail?
2. Rinpa passed across three artists (Kōrin, Hōitsu, Kiitsu) who never directly studied under one another, through deliberate revival rather than continuous teaching. Does the remix exercise feel more like continuing a lineage or reviving one?
3. Compare the result with Ukiyo-e (§7). Both are Japanese and roughly contemporaneous — what specifically in your remix marks it as brushed decorative painting rather than print culture?
4. Empty space does real work in a Rinpa composition. What did the remix lose, or gain, by leaving part of the image empty rather than filling it?
5. Did the remix learn the flatness-plus-detail combination, or did it only add gold color to an otherwise unchanged photograph? Point to evidence in the image.

## 8. Provenance and ethics

The lesson's four exhibited examples are already verified as public domain in `docs/curriculum-outline.md` §46, all confirmed `isPublicDomain: true` via the Metropolitan Museum of Art's Collection API (objects 53421, 752036, 765976, and 53424). A fifth candidate citation (a joint Kiitsu/Sodō work, Met object 748253) was checked and found not public domain — held back per PUBLIC-DOMAIN-POLICY.md §2's default-deny rule and already excluded from the curriculum entry this lesson draws from.

All three named makers (Kōrin, Hōitsu, Kiitsu) died well over a century ago and clear PUBLIC-DOMAIN-POLICY.md's death-date threshold with wide margin. No named living or recently deceased creator is used as a style target.

## Front-end integration notes

- Use the existing Academy lesson-detail scaffold; this module adds content, not a new component contract.
- Treat the lesson as **medium** remix difficulty: the source subject usually survives, but the model must actively construct the flatness-plus-detail contrast rather than get it for free.
- Keep the structural warning visible before generation: **"Hold flat gold ground and precise botanical detail together — don't just tint the photo gold."**
- Explicitly flag the Ukiyo-e distinction in the lesson copy (see beat 3 and reflect prompt 3) so learners don't collapse the Academy's two Japanese movements into one.
- Keep provenance linked to the curriculum records rather than duplicating a second image manifest here.

## Suggested seed fields

```yaml
slug: rinpa-school
hook: What if a painting were also a piece of furniture — something you lived beside, not just looked at?
teachingAngle: A decorative tradition that holds extreme flatness (gold ground, empty space) and close natural observation (precise botanical detail) together in one image, passed forward by deliberate revival rather than continuous lineage.
difficulty: medium
failureMode: The model may tint the source photo gold while keeping its described depth and even shading; a strong result must flatten the ground, crop the composition asymmetrically, and hold a few sharply observed botanical details against that flatness.
tryItLabel: 'Repaint the image as a Rinpa gold-ground screen composition'
reflectPrompts:
  - Which change made the result feel most Rinpa: gold ground, cropped asymmetry, pooled color, or the flat-silhouette-plus-sharp-detail mix?
  - How does this remix differ from an Ukiyo-e remix of the same source image?
  - Did the result learn the flatness-plus-detail combination, or just add gold tint?
```
