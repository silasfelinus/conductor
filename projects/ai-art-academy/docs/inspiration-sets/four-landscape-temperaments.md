# Four Landscape Temperaments

A controlled comparison lesson for studying how four landscape traditions treat the same scene with radically different scale, palette, and mood. The shared source stays intentionally simple so learners can distinguish temperament and technique from subject choice — this curriculum already teaches all four movements individually (Hudson River School §32, Tonalism §39, Barbizon School §40, Impressionism §10); this lesson is the first to place them side by side on one fixed composition.

## Fixed composition

Use one source image throughout:

- a single solitary tree at the water's edge, left or right of center
- a still lake or pond filling the lower half of the frame
- a low wooden dock or fence post visible near the tree
- a distant, unbroken tree line along the horizon
- an open sky filling roughly the top third of the frame
- no human figures, or at most one small, incidental figure near the dock
- landscape orientation, wide and calm

Keep the tree, water, dock, horizon line, and overall composition unchanged across all four treatments. The exercise is about how each movement handles scale, light, and paint handling — not about swapping in a different scene.

## Rights boundary

Teach movements and historically documented techniques, not imitation of a named artist. Use only public-domain reference works from artists who satisfy `PUBLIC-DOMAIN-POLICY.md`. Do not place artist names in generation prompts, negative prompts, presets, filenames, or promotional copy.

Learners may upload an image they own or are authorized to transform. Before promotion, confirm that every displayed example image is public domain or separately licensed for reproduction and that its source and rights statement are recorded.

## 1. Hudson River School

### Recognition cues

- panoramic sense of scale even within a modest frame — the tree and dock read as small against sky and distance
- luminous, often golden light breaking through cloud or mist
- meticulously rendered foliage, bark, and water reflection
- a staged progression from a shadowed, detailed foreground to a glowing, hazier distance
- calm reflective water used as a compositional hinge, doubling the sky's light
- an overall sublime, spiritual, or morally instructive mood — nature as spectacle

### Remix prompt

> Preserve the exact tree, dock, shoreline, horizon, and camera position. Repaint the scene as a Hudson River School landscape: panoramic depth and scale, meticulously rendered natural detail, a shadowed foreground opening toward luminous golden distant light, calm reflective water doubling the sky, dramatic clouds, and a sublime, theatrical sense of nature. Keep every object in its original place.

### Negative guidance

- no named artists or specific real-world locations
- no added human figures beyond at most one small incidental figure
- no loss of the tree, dock, or horizon line
- no photographic haze without the staged light progression
- no nighttime or storm-only palette that removes the golden light

### Common failure

The model may simply brighten and saturate the source rather than rebuilding the shadowed-foreground-to-glowing-distance staging. A successful result must show a clear light progression across the frame, not a uniform glow.

## 2. Tonalism

### Recognition cues

- a muted, close-value palette unified by one dominant tone (soft gray, brown, or blue-green)
- soft, blurred edges; the tree and tree line read as near-silhouettes
- dawn, dusk, or misty light rather than clear daylight
- thin, translucent glazes of color rather than opaque local color
- a quiet, contemplative, melancholic mood; the scene feels remembered rather than observed
- no incidental figure — Tonalism's version of this scene should read as empty and still

### Remix prompt

> Preserve the exact tree, dock, shoreline, horizon, and camera position. Repaint the scene as an American Tonalist landscape: a muted, close-value palette unified by a single dominant tone, soft diffused light at dawn or dusk, the tree and tree line reduced to near-silhouettes against a glowing sky, thin translucent glazes, and a quiet, melancholic mood. Keep the composition and every object legible as shapes even where detail is lost.

### Negative guidance

- no named artists
- no bright or high-key color of any kind
- no crisp edges or fine surface detail on the tree or water
- no loss of the tree, dock, or horizon as recognizable silhouettes
- no added figures

### Common failure

The model may just desaturate the source photographically. A successful result must also blur and simplify forms toward silhouette and unify the palette under one tone — desaturation alone is not Tonalism.

## 3. Barbizon School

### Recognition cues

- a muted, earthy palette of greens, browns, and greys — closer to observed color than Tonalism's single-tone unity
- loose, visible, but controlled brushwork — looser than academic finish, tighter and more tonally unified than Impressionist broken color
- soft, overcast, or late-day light rather than dramatic or golden illumination
- the scene read as a specific, humble, unidealized stretch of countryside
- if a figure is present, it is small, unposed, and engaged in quiet rural activity — never a dramatic focal point

### Remix prompt

> Preserve the exact tree, dock, shoreline, horizon, and camera position. Repaint the scene as a Barbizon School landscape: a muted, earthy palette of greens, browns, and greys, loose but controlled brushwork, soft overcast or late-day light, and direct, unidealized observation of this specific stretch of shoreline. Keep the mood humble and quiet, with no theatrical or academic staging.

### Negative guidance

- no named artists or specific real-world locations
- no golden or theatrical light
- no polished academic finish
- no loss of the tree, dock, or horizon line
- no mythological, historical, or symbolic additions

### Common failure

The model may confuse "muted" with Tonalism's single-tone unity. A successful Barbizon result keeps distinguishable, if subdued, local color (green foliage, brown bark, grey sky) rather than collapsing everything into one dominant tone.

## 4. Impressionism

### Recognition cues

- visible, broken brushstrokes — dabs and commas of color side by side
- bright, high-key palette with colored (often violet-blue) shadows, rarely black
- a sense of a fleeting instant — light and reflection that feel caught mid-change
- soft edges from optical mixing rather than blur; forms dissolve into color at close range but stay legible from a distance
- water rendered as broken, dancing reflections rather than a smooth mirror

### Remix prompt

> Preserve the exact tree, dock, shoreline, horizon, and camera position. Repaint the scene as a French Impressionist oil painting: visible broken brushstrokes, a bright plein-air palette with colored shadows, dappled natural light, and water rendered as broken, dancing reflections. Keep every object recognizable at a short viewing distance even as edges dissolve up close.

### Negative guidance

- no named artists
- no smooth, blended brushwork
- no muted or single-tone palette
- no loss of the tree, dock, or horizon line
- no black shadows

### Common failure

The model may apply a generic "painterly" filter without the broken-color optical-mixing structure. A successful result should look like confetti up close and resolve into light from a normal viewing distance — the same test the movement's own founders used.

## Blind comparison exercise

Hide the movement labels and ask learners to rank each result on:

1. preservation of the source composition (tree, dock, horizon, water)
2. sense of scale (intimate vs. sublime/panoramic)
3. movement recognition without artist names
4. light treatment (staged progression, single tone, overcast, or fleeting instant)
5. brushwork character (meticulous, blurred, loose-but-controlled, or broken)
6. absence of generic filter behavior

Then ask learners to identify the movement and cite three visible cues before revealing the labels.

## Reflection prompts

- Which two results are easiest to confuse, and what one cue would a learner check first to tell them apart?
- Where does the water read as a mirror, a silhouette, a quiet unposed surface, and a field of broken color — and how does each choice change the mood?
- Which movement treats scale as sublime, and which treats the same scene as intimate or humble?
- Does the Hudson River School result still read as the same shoreline, or has panoramic staging pulled it toward an unrelated grand vista?
- Which prompt produced the most generic "painting filter" result, and what wording should be tightened?

## Reproducibility record

For every generated comparison, record:

- source image identifier and rights status
- generation engine and model version
- workflow or endpoint version
- complete positive and negative prompts
- seed
- dimensions
- guidance, steps, sampler, and scheduler where applicable
- LoRA path, trigger, and weight where applicable
- generation date
- ArtJob and ArtImage identifiers where available
- manual notes on composition and identity preservation

## Promotion gate

Promote a set only when:

- all four outputs preserve the fixed tree/dock/horizon/water layout closely enough for a fair comparison
- the four palettes and light treatments are visibly distinct from each other, not variations on one filter
- movement recognition does not depend on protected artist names
- source and output rights are documented
- representation review finds no unwanted symbolism added by the model
- prompts and metadata are sufficient to reproduce or audit the exercise
- weak results and negative findings remain documented rather than quietly replaced
