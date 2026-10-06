# Zuzu intro: canon review of the live draft (music video 5)

Written 2026-10-06 by the comic-creator t-015 session (the one that ran the cast angle sets), at Silas's request:
*"I could use your insight on it since you know zuzu more than anyone. But caution, right now another agent is
working on it too."* This is a review only. Nothing in Kind Robots, `zuzu-intro.md` or the spec was edited;
whoever owns music-video t-029 decides what to take.

Sources:
- the live draft (`GET /api/music-video/5`, read 2026-10-06 ~11:30Z);
- `utils/musicVideoSpecs.ts` (`zuzuIntro`, kind_robots#3259);
- the cast as Silas locked it in `projects/comic-creator/issues/zuzu-koala-assassin-01/CAST-PICKS.md` and
  `VIDEO-GUARDRAILS.md`.

## The short version

The song and the shot plan are good. The pictures are not yet the comic.
- **Old designs.** Every Zuzu, sister and toddler keyframe is from round 5 or 6. That is before Silas locked the
  sword rig, the subtle belly, the rags and the darker look.
- **White-background sheets.** Several keyframes are character sheets on white, not shots.
- **Off-canon stills.** Half the fresh stills drew the wrong creature.
- **Continuity.** The coyote appears with his stump *before* the croc attack that takes his hand.

## The locked cast (use these, not the round-5/6 picks)

All are ArtImage ids, private, 832x1216, white background. "m" means the image is used mirrored.

| Character | Front | 3/4 front L | Profile L | 3/4 back L | Back | 3/4 back R | Profile R | 3/4 front R |
|---|---|---|---|---|---|---|---|---|
| Zuzu | 242395 | 242397 | 242193 | 242113 | 242117 | 242120 | m242193 | 242399 |
| Sister | 242128 | 242130 | 242132 | 242135 | 242137 | 242138 | 242140 | 242143 |
| Toddler | 242144 | 242146 | 242148 | 242150 | 242153 | 242154 | 242156 | 242158 |
| Coyote, both hands | 242531 | 242209 | m242404 | m242216 | 242214 | recolour pending | 242404 | 242220 |

Notes on the cast:
- **Zuzu:** a subtle belly, matched to A7. A single katana sits across his back, hilt over the RIGHT shoulder. He
  wears dark brown cloth trousers, never denim. His hat is the wide, shallow straw kasa from R6, not a conical
  rice hat.
- **The siblings:** claw-torn rags. The sister is no longer in the pale dress, and the toddler no longer wears the
  clean blue checked tunic.
- **The coyote:**
  - He is destitute, sick and underfed, never skeletal. The eyepatch is on his RIGHT eye and the revolver on his
    RIGHT hip.
  - His stump states come after chapter 1's croc fight: fresh is 242428, bandaged is 242435. Both still have the
    holster on the old (left) hip. A right-hip stump front is rendering now (ART-ROUND-16).
- **The abbess:** a flat, round sea-otter face (variant B). She is not in this video.

## Scene by scene

| # | Lyric | Now | Problem | Suggestion |
|---|---|---|---|---|
| 1 | (none) | 242506 | The "empty wasteland" has a horse-like animal standing in it | Re-roll with `(empty landscape:1.3), no animals, no figures`; "empty" alone is not enough for Arthemy |
| 2 | Ho... ha... ho... | 241913 (R6) | Old design (pre-rig, pre-belly), portrait on white | 242395, background placed by Kontext (see below); crop to the brim and eyes for the close-up |
| 3 | Dust on the ridge... | 241899 (X4) | Round-5 grey-robed Zuzu with the sister in a clean white dress | Fresh still from the locked look: a tiny figure on a ridge, back view (242117 as reference) |
| 4 | Straw hat low... | 242507 | Drew a dark wolf-like figure in a poncho, not Zuzu | Re-roll and name him: `anthro koala, close-up of short legs, worn boots and rust-brown poncho hem`. Or crop 242395's lower half onto dust |
| 5 | Two small shadows... | 241879 | A three-figure turnaround sheet, clean dress | 242137 (sister, back, rags) on a road background |
| 6 | Two hungry hearts... | 241883 | A four-figure turnaround sheet, clean blue tunic | 242153 (toddler, back, rags) on a road background |
| 7 | One eye watching... | 242435 | **The bandaged stump before the croc attack**; white background | 242531 (both hands, right-hip holster, eyepatch right) at a waterhole at dusk |
| 8 | Iron on his hip... | 242508 | A feral four-legged coyote with a floating revolver; no eyepatch | Crop 242531's right hip and holster, or re-roll with `anthro coyote, standing upright, close-up of the right hip, holstered revolver, gloved paw hovering` |
| 9 | Something hungry... | 241893 (K2) | A round-5 croc, bright and cartoony, with palms. The brief says shadow only | A fresh still: `dark oasis water, a long shadow beneath the surface, no visible crocodile` |
| 10 | The sand gives way... | 242509 | Usable. The croc design differs from #9 | Keep, or match the round-5 K2 croc if it shows again |
| 11 | Zuzu... Zuzu... | 241913 (R6) | Old design, white background | 242395 (front) on the road |
| 12 | Hand on the hilt... | 241920 | Old Kontext angle, pre-rig: the hilt is not over the right shoulder | 242397 (3/4 front left), where the hilt shows over his right shoulder |
| 13 | One flash of steel | 242511 | Drew a horned, demon-like figure holding a sword | Drop the figure: `a katana blade in extreme close-up, a single streak of light on steel, black background` |
| 14 | Koala assassin | (none yet) | | See the lyrics note on the empty hat |

### Getting the keyframes off white backgrounds

The vetted angle picks are sheets on white. For a 16:9 shot each one needs a scene. A Kontext single-image edit
does this well and keeps the character, which is what it did reliably all through the cast rounds:

> "Place him on a dusty desert road at dusk under a pale smoky sky, long shadows, small in the frame. Keep him
> exactly as he is: pose, clothes, the single katana across his back, colours and the inked western comic style."

That makes 6 to 8 jobs: scenes 2, 3, 5, 6, 7, 11 and 12. If the owner wants them, I can render these as
candidate ArtImages without touching the video, and hand the ids over.

## Lyrics

The ballad works and the scene-to-line matching is right. Four small notes:

1. **v1:2 / v1:3** rhyme "behind" with "behind". A suggestion: *"Two small shadows where the dry grass ends /
   Two hungry hearts and no other friends"*. Or keep line 3 and change line 4 to *"Two hungry hearts he was
   never meant to find"*.
2. **c1:1** *"Iron on his hip and a broken pledge"*: the coyote has no pledge in canon. What he has is a right
   hand he is about to lose. A suggestion: *"Iron on his right hip, one hand left to pledge"*. That keeps the rhyme
   with *edge* and quietly foreshadows chapter 1.
3. **o1:1** over scene 14, *"a lone straw kasa hat resting in the sand"*: an empty hat in the sand reads as Zuzu's
   death. That is a strong image, but it promises the wrong ending. A suggestion: the kasa on Zuzu, walking away
   small, with the siblings following close behind. That is Book One's closing silhouette, *"a pack"*.
4. The chant (*Ho... ha... ho...*) and *"Zuzu... Zuzu..."* are good; nothing to change there.

## Prompt hygiene (the `ZUZU` constant and the fresh stills)

- Add `single katana` and `chubby, standing upright`. Earlier rounds drew two swords, and "squat" made him crouch.
- `conical straw kasa hat`: "conical" pulls toward a rice hat. R6 is a wide, shallow-domed woven straw hat.
- Name the species and posture in every non-Zuzu still (`anthro coyote, standing upright`). Arthemy defaults to
  feral animals (scenes 1, 4 and 8).
- The words Arthemy draws literally, which stay out of positive AND negative prompts: duster, mother, muzzle,
  squat, ribs showing, sea otter (it adds real otters and water). See VIDEO-GUARDRAILS.md.

## For `zuzu-intro.md` (stale lines, for its owner)

- The keyframe table lists round-5/6 ids. The table above supersedes it.
- The coyote row says "242435 (stump bandaged pick)". That is wrong for a pre-attack waterhole shot.
- The abbess line says "short otter snout". Canon is now the flat, round sea-otter face.
