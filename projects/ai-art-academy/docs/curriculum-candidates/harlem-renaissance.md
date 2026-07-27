# Harlem Renaissance — curriculum candidate

## Why it belongs in the Academy

The Harlem Renaissance was not a single visual style. It was a broad Black cultural movement centered in 1920s and 1930s Harlem, with connected communities across the United States and the wider African diaspora. Its artists used portraiture, illustration, mural language, printmaking, design, photography, and modernist abstraction to define Black life on their own terms while negotiating patronage, publishing, segregation, migration, and competing ideas about representation.

The Academy should teach this as a cultural and historical movement, not as an aesthetic costume or a generic “jazz age” filter.

## Recognition cues

Look for combinations rather than a rigid formula:

- dignified portraiture and deliberate self-presentation;
- urban interiors, nightlife, performance, publishing, church, work, and neighborhood life;
- compressed print-like shapes, rhythmic repetition, and strong silhouettes;
- modernist geometry adapted to narrative or symbolic purposes;
- references to migration, ancestry, spiritual life, racial violence, aspiration, and community;
- illustration and graphic-design language shaped by magazines, books, posters, and murals.

A work can belong to the movement without using all of these cues. Avoid treating skin tone, jazz instruments, or Art Deco decoration as sufficient evidence by themselves.

## Historical frame

The movement grew alongside the Great Migration, expanding Black newspapers and magazines, new publishing networks, political organizing, and debates about who controlled Black representation. Harlem was a major center, but the movement was never geographically sealed inside one neighborhood.

Useful questions:

- Who commissioned, published, exhibited, or circulated the work?
- Was the intended audience local, national, diasporic, white-patronage driven, or some mixture?
- How does the work negotiate pride, respectability, protest, ordinary life, or stereotype?
- What does the image refuse to explain to an outside viewer?

## Artists for historical study

### Aaron Douglas

Aaron Douglas used flattened silhouettes, concentric light forms, repeated diagonals, and mural-like narrative sequences to connect African American history, migration, labor, music, oppression, and collective possibility.

Teach:

- layered silhouettes rather than individualized facial rendering;
- radial or spotlight geometry directing narrative attention;
- compressed timelines that place history and modern life in one field;
- the difference between studying Douglas's formal devices and asking a model to imitate a named artist.

Rights boundary: Douglas died in 1979. His works are not automatically public domain in the United States. Use him for historical discussion; do not ship his name in generation presets or display an image without item-level rights verification.

### Meta Vaux Warrick Fuller

Fuller’s sculpture joined historical allegory, Black emancipation, spiritual symbolism, and expressive figuration. Her work broadens the module beyond painting and print language.

Teach:

- symbolic grouping and gesture;
- narrative sculpture as public historical argument;
- how exhibition context shapes the meaning of a monument or tableau.

Rights boundary: Fuller died in 1968. Verify each work and photograph independently before display. Do not assume a sculpture’s age makes every photograph of it reusable.

### Archibald Motley

Motley painted portraits and crowded social scenes with heightened color, theatrical lighting, movement, and sharply observed social relationships.

Teach:

- crowd choreography and overlapping social groups;
- artificial light as emotional structure;
- color used to organize attention rather than merely describe local color;
- how caricature, performance, and social observation can coexist uneasily.

Rights boundary: Motley died in 1981. Historical discussion only unless a specific work is verified as reusable. Exclude his name from generation presets.

### Augusta Savage

Savage was a sculptor, teacher, organizer, and institution builder. Her career makes it impossible to teach the movement honestly as a parade of isolated masterpieces.

Teach:

- artistic labor includes teaching, organizing, fundraising, and creating access;
- lost or destroyed works are part of art history, not an empty space to fill with invention;
- surviving photographs of lost sculpture need their own provenance and rights review.

Rights boundary: Savage died in 1962. Verify the status of both artworks and documentary photographs individually.

## Public-domain and generation policy

This candidate is suitable for historical curriculum now, but not yet for automatic promotion into a named-artist generation style.

For displayed examples:

1. Verify the specific artwork’s publication and copyright status.
2. Verify the digital image or photograph separately.
3. Prefer museum or archive records with an explicit open-access statement.
4. Record creator, title, date, collection, source URL, and rights statement.
5. Do not substitute a newly generated “example” for a lost historical artwork.

For generation:

- use movement-level instructions;
- do not include living artists or artist names whose bodies of work remain protected;
- do not prompt for “Black features,” dialect caricature, poverty spectacle, or a generic exoticized Africa;
- do not reduce the movement to saxophones, flappers, smoky clubs, and sepia nostalgia;
- require users to choose a subject and historical angle rather than applying identity as surface decoration.

## Movement-level remix configuration

```yaml
slug: harlem-renaissance
mode: prompt
label: Harlem Renaissance
instruction: >-
  Recompose the image as a 1920s–1930s Black modernist narrative illustration:
  strong silhouettes, deliberate figure grouping, rhythmic geometric repetition,
  compressed print-like shapes, and a clear social or historical point of view.
  Preserve the source subject and composition. Avoid imitation of any named artist,
  nostalgic sepia clichés, minstrel imagery, and generic jazz-club decoration.
negative_guidance:
  - named-artist imitation
  - minstrel or blackface imagery
  - exaggerated racial caricature
  - generic tribal motifs
  - poverty tourism
  - decorative jazz symbolism without narrative purpose
preserve:
  - subject identity
  - major spatial relationships
  - intended emotional register
```

## Try It — one composition, three arguments

Start with a present-day scene containing at least three people in a shared public space.

Create three movement-level remixes while preserving the same people and layout:

1. **Migration:** emphasize movement, thresholds, luggage, routes, or changing horizons.
2. **Community:** emphasize institutions, mutual attention, gathering, teaching, worship, publishing, or performance.
3. **Public image:** emphasize clothing, posture, framing, and who appears to control the act of looking.

Compare what changed besides color and decoration. A successful remix should make a different argument about the same scene.

## Reflect

- Does the generated image give its Black subjects interior lives and social relationships, or merely turn them into period scenery?
- Which details came from historical evidence, and which came from model stereotype?
- Who appears to be the intended viewer?
- Does the image treat nightlife as the whole movement?
- What institutions, labor, domestic spaces, political conflicts, or ordinary routines are missing?
- Would the image still communicate a meaningful idea if every musical instrument were removed?

## Common generation failures

### “Jazz wallpaper”

Symptoms: saxophones, spotlights, cocktails, Art Deco borders, no social argument.

Correction: specify the scene’s historical question and remove decorative music cues unless performance is genuinely the subject.

### Identity as costume

Symptoms: contemporary composition with arbitrary vintage clothing and racialized facial exaggeration.

Correction: preserve faces and bodies from the source; ask for period structure, publishing language, figure grouping, and narrative emphasis rather than changed ethnicity.

### Generic African pattern overlay

Symptoms: unrelated textile motifs applied as a catch-all signifier of Blackness.

Correction: remove invented motifs. Use documented setting, geometry, typography, silhouette, and narrative structure.

### Respectability-only history

Symptoms: every subject becomes solemn, polished, middle-class, and posed.

Correction: include ordinary work, humor, nightlife, domestic life, protest, faith, fatigue, pleasure, and disagreement without collapsing into stereotype.

## Promotion checklist

Before this candidate becomes a front-end Academy style:

- [x] At least three display examples have explicit, item-level reusable rights.
      See "Research update: a rights-clear sourcing option" below — four Winold
      Reiss portraits, all CC0, verified 2026-07-27.
- [x] Example metadata records both artwork and image rights.
      Recorded in the research update below (title, artist, date, medium,
      collection, accession, license, source).
- [ ] No protected artist name appears in the generation instruction.
- [ ] A Black cultural-history reviewer checks the framing and exercises.
      **Not satisfied by the rights research below** — see that section's own
      caveat: Reiss himself was not a Harlem Renaissance artist, and using his
      portraits as a generation-style anchor raises a distinct framing question
      this checklist item exists to catch. Closing the rights item does not
      close this one.
- [ ] The movement-level prompt is tested for caricature and identity drift.
- [ ] The lesson links the Great Migration, publishing, institutions, and patronage—not only nightlife.
- [ ] The generated examples retain source-person identity rather than racializing uploads.

## Research update: a rights-clear sourcing option (2026-07-27, ai-art-academy/t-010 lane 4)

None of the four artists discussed above (Douglas d. 1979, Fuller d. 1968,
Motley d. 1981, Savage d. 1962) clears PUBLIC-DOMAIN-POLICY.md §1.3's prong 1
(died before 1956) — so none of their own works can ever become a display
example or generation-style anchor under current policy, regardless of a
given work's publication date. This is unchanged by this update; they remain
historical-discussion-only, exactly as scoped above.

Researched a distinct, rights-clear option: **Winold Reiss** (1886-1953), a
German-American illustrator and graphic designer commissioned in 1924 by
Survey Graphic editor Paul Kellogg to portray leading Harlem Renaissance
figures for the magazine's March 1, 1925 special issue, "Harlem: Mecca of
the New Negro" — later expanded as the frontispiece portraits in Alain
Locke's anthology *The New Negro* (1925), a founding document of the
movement. Reiss clears both PUBLIC-DOMAIN-POLICY.md §1.3 prongs: he died in
1953 (before the 1956 cutoff), and the portraits were published in 1925
(before the 1930/1931 US-publication cutoff).

Four of his portraits from this series are explicitly marked **CC0** on the
Smithsonian's own object pages (verified via `WebSearch` excerpts of
`si.edu`/`npg.si.edu` object records — direct `WebFetch` to both domains
returned HTTP 403 in this sandbox, the same museum-egress limitation
PUBLIC-DOMAIN-POLICY.md's own verification log documents for its 2026-07-10
checks):

- *W. E. B. Du Bois*, pastel on paper, 1925 — National Portrait Gallery,
  Smithsonian Institution, accession NPG.72.79. CC0. Cross-confirmed on its
  Wikimedia Commons file page, which independently cites both prongs: "in
  the public domain in the United States because it was published... before
  January 1, 1931" and "the author died in 1953... life plus 70 years."
  https://www.si.edu/object/npg_NPG.72.79
- *Roland Hayes*, pastel on illustration board, 1924/1925 (cover portrait,
  Survey Graphic, March 1, 1925) — National Portrait Gallery, accession
  NPG.72.81. CC0. https://www.si.edu/object/npg_NPG.72.81
- *James Weldon Johnson*, pastel on illustration board, 1925 — National
  Portrait Gallery, accession NPG.72.78. CC0.
  https://www.si.edu/object/npg_NPG.72.78
- *Countee Cullen*, printed illustration, 1925 — National Portrait Gallery,
  accession NPG.98.129.c. CC0. https://www.si.edu/object/npg_NPG.98.129.c

**Caveat — do not treat every Reiss portrait in this series as CC0.** Two
sibling works from the same artist, era, and 1972 gift — *Alain Leroy Locke*
(NPG.72.84) and *Langston Hughes* (NPG.72.82) — carry an outwardly identical
legal fact pattern (same artist, same death year, same 1925 creation) but
are marked "Usage conditions apply, © Estate of Winold Reiss" on the
Smithsonian's own site, not CC0. Per PUBLIC-DOMAIN-POLICY.md §5
(default-deny under ambiguity), do not use those two for display; use only
the four confirmed-CC0 works above until/unless the institution's own
metadata changes.

**Open question this does not resolve.** Reiss was not a participant in the
Harlem Renaissance as a movement — he was a white, German-American
commercial illustrator hired by a white-edited magazine to portray Black
cultural figures for a white and Black readership. Every prior curriculum
entry that kept one artist while excluding others on death-date grounds
(Precisionism §33, American Regionalism §24) kept an artist who was an
actual participant in the movement being taught. Using Reiss's portraits as
the generation-style anchor for a *Harlem Renaissance* lesson is a
materially different situation, and it's exactly what this checklist's
"Black cultural-history reviewer checks the framing" line exists to catch —
resolving the rights question does not resolve that one. Recommend Silas or
a qualified reviewer decide between at least two paths before promotion:
(a) use the four Reiss works as historical-context display images only,
with the movement-level generation preset staying artist-anchor-free (as
already drafted above), or (b) hold this candidate at historical-curriculum-
only, no display images, until a rights-clear work by an artist who was
actually part of the movement is found. See ai-art-academy/t-043 for the
roadmap-side tracking of this question.

## Suggested source hunt

Prioritize institutions with explicit open-access metadata and strong Harlem Renaissance holdings, including the Smithsonian American Art Museum, Smithsonian National Museum of African American History and Culture, Library of Congress, Schomburg Center, National Gallery of Art, and major university archives. Treat every object and reproduction as a separate rights decision; collection reputation is not a blanket license.
