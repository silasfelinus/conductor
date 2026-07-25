# Ashcan School curriculum module

status: ready for curriculum integration
movement_slug: ashcan-school
era: c. 1900-1915
region: United States
remix_mode: prompt

## Why this belongs in the Academy

The Ashcan School adds an urban-realist tradition that is visually and socially distinct from Impressionism, American Regionalism, Social Realism, and the Hudson River School. Its painters turned away from polished society portraiture and idealized national landscapes toward crowded streets, tenements, boxing clubs, theaters, bars, docks, and ordinary city leisure.

The lesson should avoid reducing the movement to “gritty old New York.” Ashcan artists made working-class and immigrant neighborhoods visible to gallery audiences, but they still observed those communities from individual positions of class, race, and privilege. Learners should ask who is depicted with agency, who becomes scenery, and which parts of city life remain outside the frame.

## Recognition cues

- Crowded urban scenes framed at street level rather than from a monumental viewpoint
- Dark, earthy palettes punctuated by signs, clothing, electric light, or wet pavement
- Loose, vigorous brushwork that preserves motion and visual noise
- Cropped figures and oblique viewpoints that make the scene feel witnessed rather than staged
- Everyday leisure and labor: markets, ferries, boxing, theaters, bars, rooftops, and sidewalks
- Architecture used as lived environment rather than pristine backdrop
- A tension between journalistic observation, humor, empathy, and spectacle

## Notable artists

- **Robert Henri** (1865-1929) — Teacher and organizing influence whose portraits and city scenes argued for direct observation and artistic independence.
- **George Bellows** (1882-1925) — Painter and printmaker known for forceful boxing scenes, crowded streets, riverfront labor, and rapidly changing New York neighborhoods.
- **John Sloan** (1871-1951) — Former newspaper illustrator whose paintings and etchings focused on sidewalks, rooftops, shops, theaters, and private moments glimpsed through the city.

All three artists died before the Academy's conservative 1956 death-year cutoff.

## Example works

### Snow in New York

- Artist: Robert Henri
- Date: 1902
- Collection: National Gallery of Art
- Public-domain rationale: artist died 1929; work predates 1931
- Source target: National Gallery of Art open-access collection
- Verification status: confirm the object page and downloadable-image rights before acquisition

### Stag at Sharkey's

- Artist: George Bellows
- Date: 1909
- Collection: Cleveland Museum of Art
- Public-domain rationale: artist died 1925; work predates 1931
- Source target: Cleveland Museum of Art open-access collection or Wikimedia Commons
- Verification status: confirm the exact reproduction license before acquisition

### McSorley's Bar

- Artist: John Sloan
- Date: 1912
- Collection: Detroit Institute of Arts
- Public-domain rationale: artist died 1951; work predates 1931
- Source target: museum object page or Wikimedia Commons
- Verification status: confirm the exact object record and reproduction license before acquisition

## Remix configuration

```yaml
slug: ashcan-school
name: Ashcan School
era: "c. 1900-1915"
artist_slugs: [robert-henri, george-bellows, john-sloan]
example_count: 3
remix:
  mode: prompt
  template: >-
    Repaint this image in the manner of the Ashcan School: an immediate street-level
    urban scene, dark earthy color, loose vigorous brushwork, compressed crowds,
    cropped figures, wet pavement or smoky interior light, ordinary labor and leisure,
    and architecture treated as a lived environment rather than a polished backdrop.
  failure_mode: >-
    The model may turn the result into sepia nostalgia, noir concept art, or generic
    Victorian illustration. Keep the palette varied but subdued, preserve observed
    human gestures, avoid cinematic spotlighting, and let visual clutter feel specific
    rather than decorative.
```

## Teaching beats

### Try it

Ask learners to locate three kinds of motion in an Ashcan image: a moving body, a moving crowd, and a moving mark made by the painter. Then remix a contemporary street or interior photograph while preserving those three layers of movement without adding historical costumes.

### Reflect

1. Which people are presented as individuals, and which become part of the crowd?
2. Does the scene invite empathy, curiosity, judgment, entertainment, or several at once?
3. How would the image change if it were made by someone who lived or worked in the depicted neighborhood rather than an outside observer?

## Integration checklist

- Add the movement to `docs/curriculum-outline.md` and its machine-readable skeleton.
- Add a prompt-mode row to `docs/style-lora-registry.md`.
- Add the Try-It / Reflect row to `docs/teaching-notes.md`.
- Queue `kind-robots-academy-style-preview-ashcan-school` in `projects/art-prompts.yaml`.
- Mirror the entry into `kind_robots/stores/seeds/academyStyles.ts` in a later cross-repo task.
- Verify all three example works against official open-access or Wikimedia source pages before acquiring images.
