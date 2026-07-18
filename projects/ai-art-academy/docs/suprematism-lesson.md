# AI Art Academy — Suprematism Lesson Module

Date: 2026-07-18  
Task: `ai-art-academy/t-010` continuous-improvement cycle, option (d) curriculum/content expansion  
Status: ready for front-end content integration

This module fills the pedagogy gap created when Suprematism became the Academy's 22nd movement. It follows the eight-beat lesson scaffold in `docs/teaching-notes.md` and draws its facts, recognition cues, example works, and remix direction from `docs/curriculum-outline.md` §22.

## Lesson metadata

- **Movement:** Suprematism
- **Slug:** `suprematism`
- **Era:** 1913–1919
- **Region:** Russia
- **Primary artist:** Kazimir Malevich (1879–1935)
- **Remix mode:** prompt
- **Difficulty:** hard
- **Core warning:** a faithful result discards the source subject rather than preserving it

## 1. Hook

What happens when a painter decides the picture does not need to depict anything at all?

Suprematism answers with floating squares, bars, circles, and pure color. Malevich was not simplifying the visible world; he was trying to leave it behind and make feeling itself the subject.

## 2. Look First

Spot these five things:

1. A small number of flat, hard-edged geometric shapes.
2. Shapes tilted and floating without a ground line, horizon, or perspective.
3. A white or near-white field treated as infinite space.
4. Black, red, and white dominating, with other pure colors used sparingly.
5. No recognizable objects, figures, texture, or modeled depth.

The fastest recognition test is subtraction: when every trace of ordinary subject matter disappears and only weightless geometry remains, Suprematism is a strong candidate.

## 3. The Big Idea

Kazimir Malevich called Suprematism the supremacy of pure feeling over the depiction of objects. His 1915 *Black Square* announced a complete break with representation: painting no longer had to imitate a person, landscape, or thing. Color and geometry could stand alone.

That makes Suprematism more radical than a decorative geometric style. Its blank field is not a wall or sky, and its shapes are not coded objects. They exist as independent visual forces—heavy, light, tense, balanced, falling, or flying.

## 4. Meet the Maker

### Kazimir Malevich (1879–1935)

Malevich moved through Cubo-Futurism before unveiling Suprematism at the 1915 “Last Futurist Exhibition 0,10” in Petrograd. He spent the following years developing its geometric vocabulary in painting, theory, and design.

He is the movement's founder and sole originator in the Academy curriculum. Presenting one primary maker here is more honest than padding the lesson with adjacent Constructivists whose goals and visual systems were different.

## 5. See It

All four works below are verified public-domain examples already recorded in the curriculum outline.

### *Black Square* — 1915

Notice how little information remains: one dark plane and a pale field. Its force comes from scale, placement, edge, and the refusal to explain itself through subject matter.

### *Suprematist Composition: Airplane Flying* — 1915

Look for the tension created by angled bars and rectangles. The title suggests motion, but the painting does not illustrate an airplane; geometry carries the sensation.

### *Suprematist Composition: White on White* — 1918

A tilted white square barely separates from its warmer white ground. This is the movement's logic pushed toward near-disappearance: difference without depiction.

### *Suprematist Painting: Eight Red Rectangles* — 1915

Watch how repetition, spacing, and tilt make simple red bars feel airborne. The blank field does as much compositional work as the shapes.

## 6. Try It

### Instruction

> Reduce this image to a Suprematist composition: a small number of flat geometric shapes—squares, circles, and bars—in black, red, and a few pure colors, floating freely against a plain white ground, with no outline, perspective, texture, or recognizable objects.

### What to expect

- The original subject may disappear almost completely.
- Composition should become a balance of shape, angle, scale, color, and empty space.
- A successful output should feel weightless rather than like a poster laid over the original photo.

### Common failure modes

- The model preserves a recognizable silhouette and merely decorates it with rectangles.
- Shapes gain shadows, gradients, bevels, or 3D depth.
- The result drifts into Bauhaus graphic design, Constructivist propaganda, or a generic modern poster.
- Too many shapes create visual confetti instead of a deliberate composition.

### How to iterate

- Add “no recognizable subject remains” when the source stays too literal.
- Add “flat matte color, no shadows, no gradients, no texture” when depth sneaks back in.
- Reduce the requested shape count when the result gets busy.
- Use a source with a simple silhouette first, then compare it with a complex source to discuss what the transformation chooses to discard.

### Product framing

Do not promise composition preservation for this movement. Label the exercise playfully as **“Malevich-ify: reduce your image to pure geometry.”** The loss of the source subject is the lesson, not a model defect.

## 7. Reflect

1. Which trace of the original survived longest: its dominant angle, color balance, or overall mass?
2. Does the result feel balanced, tense, falling, or floating? Which shape relationships create that feeling?
3. When a remix removes the subject entirely, is it still a remix of that image? Explain your boundary.
4. Compare the output with De Stijl: where does Suprematism feel freer, less gridded, or less architectural?
5. Did empty white space feel passive, or did it behave like an active part of the composition?

## 8. Provenance and ethics

Kazimir Malevich died in 1935, and the four example works date from 1915–1918. They clear the Academy's public-domain rule with wide margin and are recorded as verified public-domain works in `docs/curriculum-outline.md` §22.

The lesson teaches a historical movement and its sole originating artist. It does not imitate a living creator, active studio, or commercial brand.

## Front-end integration notes

- Add Suprematism to the per-style teaching-notes table when that document is next consolidated from 21 to 22 movements.
- Use `difficulty: hard` and a movement-specific failure mode rather than the generic prompt-mode fallback.
- Keep the warning visible before generation: **“This style intentionally replaces recognizable subject matter with pure geometry.”**
- Reuse the existing Try It and Reflect UI from `academy-style-detail.vue`; this module provides the content, not a new component contract.
- Keep example-work provenance linked to the existing curriculum records rather than duplicating a second manifest in this file.

## Suggested seed fields

```yaml
slug: suprematism
hook: What happens when a painter decides the picture does not need to depict anything at all?
teachingAngle: Pure feeling through weightless geometry, without depicted objects.
difficulty: hard
failureMode: The model may preserve the source as a decorated silhouette or drift into generic geometric poster design; a faithful result should discard recognizable subject matter.
tryItLabel: 'Malevich-ify: reduce your image to pure geometry'
reflectPrompts:
  - Which trace of the original survived longest: angle, color balance, or overall mass?
  - Does the result feel balanced, tense, falling, or floating? What creates that feeling?
  - When the subject disappears entirely, is the result still a remix of the source image?
```
