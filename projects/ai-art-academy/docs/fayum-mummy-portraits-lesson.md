# AI Art Academy — Fayum Mummy Portraits Lesson Module

Date: 2026-08-07
Task: `ai-art-academy/t-010` continuous-improvement cycle, option (d) curriculum depth
Status: ready for front-end content integration

This module gives Fayum Mummy Portraits the same deeper eight-beat treatment already used by the Academy's dedicated Suprematism and Ancient Egyptian Painting lessons. It follows the scaffold in `docs/teaching-notes.md` and deliberately reuses the facts, recognition cues, verified example works, and remix direction already established in `docs/curriculum-outline.md` §28 rather than introducing a second source of historical claims. The Ancient Egyptian Painting lesson's own reflection prompt (§7.4) already points learners here for a direct comparison; this module completes that pairing.

## Lesson metadata

- **Movement:** Fayum Mummy Portraits
- **Slug:** `fayum-mummy-portraits`
- **Era:** c. A.D. 50–250 (Roman Egypt)
- **Region:** Roman Egypt (Fayum oasis, Antinoopolis, Memphis, and elsewhere along the Nile)
- **Primary makers:** anonymous painters (`anonymous-fayum-painters`)
- **Remix mode:** prompt
- **Difficulty:** medium
- **Core warning:** a successful remix has to reproduce the wax-built modeling and direct psychological presence, not just add "ancient" texture to a modern photographic portrait

## 1. Hook

What if the most lifelike painted faces to survive from the ancient world were never meant to be looked at by the living?

Fayum portraits were painted from life or near-life, then bound face-up into mummy wrappings, sealed away in the dark. Nearly two thousand years later, they are still some of the most direct, individualized human gazes in all of ancient art — more intimate than most Roman sculpture, more personal than nearly any Egyptian tomb painting.

## 2. Look First

Spot these six things:

1. Large, dark, almond-shaped eyes with heavy brows, looking straight at (or just past) the viewer.
2. Warm, honey-toned skin built up in visible ridges of thick wax, not smoothly blended.
3. A plain, flat, dark or muted background — no setting, no landscape, no architecture.
4. Simple Roman-style hair and dress, sometimes with a thin gold-leaf wreath, diadem, or jewelry.
5. Close head-and-shoulders framing, three-quarter or frontal, cropped at the chest with no hands.
6. Even, frontal illumination — no cast shadow, no single dramatic light source.

The quickest recognition test is textural as much as compositional: if the skin reads as smooth digital shading rather than built-up wax ridges, and the gaze is casual rather than fixed and direct, the image has borrowed the setting without the technique.

## 3. The Big Idea

Fayum portraits sit at a genuine cultural seam: Egyptian funerary ritual (a portrait bound permanently to the body, meant to preserve identity for the afterlife) fused with an imported Greco-Roman painting technique (encaustic portraiture, otherwise almost entirely lost from the ancient Mediterranean). The result is not a compromise between two styles but a third thing — a naturalism aimed at the dead rather than the living, a likeness with nowhere to be displayed.

That makes this an unusually direct contrast case with Ancient Egyptian Painting (Lesson 37, `egyptian-painting`), which this Academy also teaches. Both traditions come from Egypt and both serve funerary purposes, but one flattens the body into diagrammatic registers while the other models an individual face with almost photographic specificity. Teaching them back to back makes clear that "Egyptian art" is not one style — it is a set of different systems for different purposes across three thousand years.

The Academy treats this as a tradition of anonymous artisans, the same choice already made for Ancient Egyptian Painting and Byzantine Mosaic. No surviving Fayum portrait carries a painter's signature.

## 4. Meet the Makers

### Anonymous Fayum painters

No Fayum portrait survives with an attribution, and no ancient text names an individual practitioner. The painters worked to a shared technical and compositional convention — encaustic on thin wood panel, frontal gaze, plain background — while still capturing enough individual variation in age, features, and expression that art historians can distinguish sitters, and sometimes workshops, without ever recovering a name.

This is the same lesson the Academy draws from Ancient Egyptian Painting's anonymous scribes: durable visual traditions were often maintained by skilled communities whose individual names were never recorded, and inventing an artist to fill that gap would be worse history than naming the tradition honestly.

## 5. See It

These examples are already recorded as verified public-domain works in `docs/curriculum-outline.md` §28.

### *Portrait of the Boy Eutyches* — A.D. 100–150

Notice how young the sitter is, and how the same direct, wide-eyed gaze convention is applied regardless of age. The Metropolitan Museum of Art record (accession 18.9.2) is CC0/public domain.

### *Portrait of a Thin-Faced Man* — A.D. 140–170

Look for the gold leaf worked into the composition alongside the encaustic modeling, and the way individualized bone structure still fits inside the shared formula of gaze, framing, and lighting. The Met record (accession 09.181.3) is CC0/public domain.

### *Portrait of a Young Woman with a Gilded Wreath* — A.D. 120–140

Use this portrait to study hair and jewelry convention: a thin gold wreath, simple Roman-style styling, and how ornament stays modest compared to the intensity of the gaze. The Met record (accession 09.181.7) is CC0/public domain.

## 6. Try It

### Instruction

> Repaint this image as a Fayum mummy portrait: give the subject a direct frontal or slightly turned gaze with large, dark, almond-shaped eyes and heavy dark brows, build warm honey-toned skin from thick encaustic wax brushstrokes with visible ridge texture rather than smooth shading, simplify hair and dress into plain Roman style, place the figure against a flat dark background with no setting, crop close at the head and shoulders, and light the face evenly with no cast shadow. Optionally add a thin gold-leaf wreath or simple jewelry.

### What to expect

- The gaze should become fixed and direct, not candid or mid-expression.
- Skin should read as built up in visible strokes, not airbrushed.
- The background should flatten to a single dark or muted tone.
- Framing should crop tightly at the chest, with no hands or surrounding scene.
- Lighting should go flat and even, losing any dramatic shadow from the source image.

### Common failure modes

- **Costume filter:** the model adds a wreath or toga to an otherwise untouched modern photographic portrait, keeping soft camera lighting and shallow depth of field.
- **Waxwork skin without the gaze:** skin texture changes but the eyes stay naturalistic in proportion and expression instead of becoming large, dark, and fixed.
- **Scene creep:** a background setting (architecture, sky, landscape) survives instead of flattening to plain dark tone.
- **Confusing this with Ancient Egyptian Painting:** composite perspective, hierarchical scale, or hieroglyphic marks creep in — those belong to Lesson 37, not this one. Fayum portraits are naturalistic, not diagrammatic.
- **Over-restoration:** the result looks like a pristine modern painting rather than an aged encaustic panel; some texture and warmth loss is part of the visual identity, though the exercise should not fake damage or cracking as a shortcut for style.

### How to iterate

- If the eyes stay small or naturalistic, emphasize **"large dark almond-shaped eyes, heavy brows, fixed direct gaze"** explicitly.
- If skin looks airbrushed, add **"visible ridges of thick wax brushwork, not smooth blended shading."**
- If a background setting survives, add **"flat plain dark background, no scene, no architecture."**
- If the result drifts toward diagrammatic Egyptian registers or profile-composite figures, remove those cues and restate **"naturalistic Roman portrait painting, not Egyptian pictorial convention."**
- Compare an adult portrait with a child's, as the two verified examples above do, to see how the gaze convention holds constant across age.

## 7. Reflect

1. What single feature made the result feel most "Fayum": the eyes, the skin texture, the background, or the framing?
2. This portrait was painted to be sealed into darkness forever, not displayed. Does knowing that change how you look at the direct gaze?
3. Compare the result with Ancient Egyptian Painting (Lesson 37). Both are Egyptian funerary traditions — why does one flatten the body into diagrammatic registers while the other builds a highly individualized, naturalistic face?
4. Almost nothing is known about any individual Fayum painter. Does that change how much credit or authorship you associate with the image?
5. Did the remix learn the wax-built modeling technique, or did it only add "ancient portrait" mood lighting to an otherwise modern face? Point to evidence in the image.

## 8. Provenance and ethics

The lesson's three exhibited examples are Roman-Egyptian funerary portraits by unidentified makers. Their institutional records are already verified as public domain (CC0, Met Open Access) in `docs/curriculum-outline.md` §28: *Portrait of the Boy Eutyches* (accession 18.9.2), *Portrait of a Thin-Faced Man* (accession 09.181.3), and *Portrait of a Young Woman with a Gilded Wreath* (accession 09.181.7), all The Metropolitan Museum of Art.

No named living or recently deceased creator is used as a style target. The Academy credits the anonymous tradition instead of inventing authorship. These are funerary portraits of real, once-living individuals; the lesson frames the remix exercise around technique and historical context rather than treating the sitters as interchangeable decorative subjects.

## Front-end integration notes

- Use the existing Academy lesson-detail scaffold; this module adds content, not a new component contract.
- Treat the lesson as **medium** remix difficulty — the technique (wax-built modeling, direct gaze, flat background) is more approachable to a diffusion model than the compositional restructuring Ancient Egyptian Painting requires, since it works with rather than against ordinary photographic portrait framing.
- Keep the structural warning visible before generation: **"Aim for wax-built modeling and a fixed direct gaze, not just an old-photo filter."**
- Surface the explicit contrast with Ancient Egyptian Painting (Lesson 37) in the lesson UI if a "related lessons" affordance exists — the two make a strong paired teaching moment.
- Keep provenance linked to the curriculum records rather than duplicating a second image manifest here.
- A future teaching-notes consolidation should add the missing §28 row and can lift the teaching angle/failure mode below.

## Suggested seed fields

```yaml
slug: fayum-mummy-portraits
hook: What if the most lifelike painted faces to survive from the ancient world were never meant to be looked at by the living?
teachingAngle: A Roman-Egyptian funerary portrait tradition whose naturalistic, wax-built faces contrast directly with Ancient Egyptian Painting's diagrammatic figures -- same region and purpose, opposite visual logic.
difficulty: medium
failureMode: The model may apply an "old photo" filter to an otherwise untouched modern portrait; a strong result must build visibly wax-textured skin, large dark fixed-gaze eyes, and a flat plain background.
tryItLabel: 'Repaint the portrait in Fayum encaustic style'
reflectPrompts:
  - What single feature made the result feel most Fayum: the eyes, the skin texture, or the background?
  - Compare with Ancient Egyptian Painting -- why does one tradition flatten the body while the other models a naturalistic face?
  - Did the remix learn the wax-built technique, or just add "ancient" mood lighting?
```
