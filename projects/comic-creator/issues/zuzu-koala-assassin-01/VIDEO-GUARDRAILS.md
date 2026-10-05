# Zuzu: Koala Assassin — guardrails for videos made from this comic

Two Kind Robots video projects consume this issue (Silas, 2026-10-04):

| Video | Project | Tasks |
|---|---|---|
| Intro / title music video | `music-video` | t-024 brief → t-029 render and verdict |
| An animated experience of Book One | `comic-film` | t-003 shot list → t-009 render and verdict |

The film does not have to tell the whole story. Silas, 2026-10-04: *"an animation doesn't need to tell this full story, but just needs to give an experience"* The story of
record is BOOK-ONE.md (which replaced the v0 issue 1 script); Old Komodo is not in it.

Both inherit the comic's look and canon from here. BRAINSTORM-ROUND-3.md is the source of truth
wherever it disagrees with the v0 SERIES-BIBLE.md or ISSUE-01-SCRIPT.md.

## Look

- **Stills and keyframes:** render through the Comic Studio series `zuzu-koala-assassin` house lane, `Illustrious/arthemyWesternArt_v30.safetensors` (Silas, 2026-10-04, after the round-4 bake-off: "arthemy is the winner."). Use the lane's prefix and suffix, plus the series negatives.
- **Character shots:** start from vetted comic attempts (verdict selected or liked) rather than fresh renders, until the design pick (t-015) and the character LoRAs (t-016) land.
- **Clip motion prompts:** write them in prose: camera movement plus one action. No art-direction jargon.

## Canon in every prompt

- **Zuzu is always serious:** Clint Eastwood stillness, never a smiling sensei.
- **Zuzu's costume (2026-10-05):** a dusty poncho, the Eastwood callback, and a kasa whose wide brim shades his
  eyes, over a dark tunic, brown trousers and an orange sash. Tags: `poncho, kasa, sandogasa, brim shading the eyes`.
- **Zuzu's sword rig (2026-10-05, after round 7):** the sheathed katana is strapped diagonally across his back, over the poncho, with the hilt above his RIGHT shoulder and the scabbard tip at his LEFT hip. From the front, only the hilt (over the right shoulder) and the scabbard tip (below the poncho at the left hip) show. From behind, the whole scabbard runs from upper right to lower left across the poncho.
  Negate `straw boater, cowboy hat, cloak, cape`.
- **Look (2026-10-05, after round 8):** Zuzu is squat with koala proportions (stubby legs, round belly, big head) and dark brown cloth trousers, never denim. The siblings wear claw-torn rags. The coyote's hands are empty. Overall tone: darker and grittier, less Disney, more Tarantino.
- **Builds and sides (2026-10-05, after round 10):** Zuzu is portly (big round belly, wide hips; the round-10 A7 profile is the reference). The coyote's eyepatch is on his right eye and his revolver on his right hip; the croc takes that right hand in chapter 1.
- **Poverty and faces (2026-10-05):** the coyote is destitute (tattered, patched, filthy, starving); the abbess has a short, blunt otter muzzle.
- **Zuzu is koala-sized, or a little bigger:** Silas, 2026-10-04: *"zuzu should be koala sized, or a little bigger. if he was an actor doing mocap, it would be danny devito."*
  Short, stocky, barrel-chested, short legs. In shared frames he is the shortest adult, and the sister is taller
  than him. Tags that carry it: `short, stocky, chubby, small stature, short legs`. Round 4b's walking shots drew
  him tall and lanky, which is the failure to watch for.
- **The siblings are fennec foxes:** a gaunt sister of about ten and a toddler brother who only babbles. Both are starving, beaten and frightened.
- **No dialogue, no narration.** Silas, 2026-10-04: *"no dialogue or narration, just the occasional sign or poster."*
  The only words on screen are diegetic signs and posters, plus a title card. The v0 script's lines become wordless beats.
  Backstory comes through movement.
- **A mature comic with mature themes.** Silas, 2026-10-04: *"I never explicitly said zuzu was teen rated. This is a mature comic with mature themes."*
  Violence can be on the page and on screen. An earlier "rated teen, aftermath only" note came from the
  LLM-written v0 script, not from Silas, and is withdrawn.
- **Children (absolute, independent of the rating).** The siblings can be endangered, hurt, starving
  and terrified, because that is the story. But no image or prompt ever sexualises them or shows them
  undressed, and their injuries stay implied rather than detailed. The art pipeline's own content rules
  apply on top of the comic's rating.
- **Placeholders, not canon:** the v0 Kind Robots world (Gallowsun Junction, the Stationmaster, Tomoe, Old Shelba, contract-language captions). Use none of it.

## bannedTerms (never in any positive prompt, lyric, caption or title)

This list guards one thing: the buried twist stays secret until Silas picks the issue that reveals it. Copy this list into
`settings.bannedTerms` on every Zuzu video. The server refuses any scene prompt containing a term,
on every engine (music-video t-025).

```
human, humans, humanity, mankind, people, pharmacy, great wall, skyscraper, highway,
billboard, road sign, english lettering
```

`people` is on the list because every character is an animal. In a prompt, say "townsfolk" or name
the species instead. The words "statue" and "ruins" are allowed for ordinary weird-west sets. Never
pair them with a giant figure or with lettering.

## Words the image models draw literally (keep them out of positive AND negative prompts)

The house checkpoint draws some words as objects, even when they appear only in the negative prompt:

- **"duster"** (the coat) draws a feather duster. Say "long riding coat".
- **"mother"** (as in "mother superior") adds a small otter child. Say "abbess" or "elderly head nun".
- **"muzzle"** (the snout) draws a muzzle restraint over the face, as in round 12. Describe the face instead,
  for example "a round, flat otter face with a small nose pad".
- **"squat"** makes Zuzu crouch. Say "chubby, standing upright".
