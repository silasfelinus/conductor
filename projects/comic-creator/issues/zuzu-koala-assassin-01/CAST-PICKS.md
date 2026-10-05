# Zuzu Book One — locked character designs

Silas, 2026-10-04, from the round-5 cast sheets (ART-ROUND-5.yaml, Arthemy Western Art v3.0):
*"zuzu z2, z6 todler t2 t4, coyote c1, crocodile k2, nuns n2, x2 x4"*

These renders are the reference designs for Book One. They feed the 8-angle renders (t-015) and the
character LoRA datasets (t-016). All are private on Kind Robots.

| Character | Pick | ArtImage | Render | Settings |
|---|---|---|---|---|
| **Zuzu (final)** | **R6** | **241913** | Round 6 hero shot: rust-brown poncho, kasa, katana on the back | house |
| Zuzu | Z2 | 241873 | Turnaround, three views (superseded by R6) | author's |
| Zuzu | Z6 | 241877 | Emotion sheet | author's |
| The toddler | T2 | 241883 | Turnaround, checked tunic | author's |
| The sister | S2 | 241879 | Turnaround A, long torn pale dress | author's |
| The siblings | T4 | 241885 | Emotion sheet (mostly the sister) | author's |
| The one-eyed coyote | C1 | 241888 | Turnaround A | round-4 |
| The crocodile | K2 | 241893 | Erupting from the oasis | author's |
| The otter nuns | N2 | 241895 | Three nuns at the mission wall | author's |
| Scene | X2 | 241887 | Size lineup | author's |
| Scene | X4 | 241899 | Chapter 11, the road | author's |

## Follow-up decisions

Silas, 2026-10-05: *"Sister s2. Yes on house settings. I actually like Zuzu with two modification. The “cloak” should be a poncho, a callback to Eastwood. And he need a real samurai hat, I don’t know it’s name, but those long wide brims that partially hide the head."*

- **The sister is S2** (ArtImage 241879): the long torn pale dress, bandaged wrists and a hard stare.
- **House settings:** the Arthemy house lane uses the author's settings (Euler a, 30 steps, CFG 5, style tags).
- **Zuzu keeps Z2 with two changes.** The cloak becomes a **poncho**, the Man with No Name callback. The
  straw boater becomes a **kasa**, the wide straw travel hat whose brim shades his eyes (the *sandogasa*
  style). Round 6 (ART-ROUND-6.yaml) renders the redesign for a final pick.

## What the picks say

- **Settings.** Seven of the nine picks used the checkpoint author's settings: Euler a, 30 steps,
  CFG 5, plus the `toon (style), western comics (style)` tags. Only the coyote came from the round-4
  settings. Silas then made the author's settings the house default (2026-10-05).
- **Zuzu's design (Z2).** Stocky and koala-sized, in a dark blue tunic, brown trousers and an orange
  sash, with a straw hat and the katana on his back. Settled 2026-10-05: a poncho and a kasa replace the
  cloak and the straw boater.
- **The sister** was picked separately as S2 (2026-10-05).
- **Scale in the scene picks.** In both X2 and X4 the fox beside Zuzu is small enough to read as the
  toddler. The canon says the sister stands taller than Zuzu; these picks are scale references for
  Zuzu with the toddler, not for the sister.

## Zuzu final: R6

Silas, 2026-10-05: *"I like the poncho design in r6 best for zuzu. But noticed that some of the back images
in the tests fail to show the sword."*

- **Zuzu is R6** (ArtImage 241913): a rust-brown poncho with an orange zigzag trim, a conical straw kasa, a
  dark tunic, an orange sash, brown trousers, and the sheathed katana slung across his back.
- **The katana is always on his back**, in every view. Round 6's turnaround B lost it in the back view.
  Prompts now weight `(katana on back:1.4)` and say the hilt rises above his right shoulder.
- **Follow-ups:** ART-ROUND-7.yaml (Arthemy turnarounds of R6 that keep the sword) and ANGLES-ZUZU.yaml
  (the 8 Kontext angles re-posed from R6 itself, t-015).

### Round 7 results (2026-10-05)

- **The sword fix works.** All five Arthemy renders (ART-ROUND-7.yaml, ArtImages 241914–241918) keep the
  katana on his back in every view. The hat drifts to a flat straw brim and is lost in two views.
- **Kontext angles from R6** (ANGLES-ZUZU.yaml) give five keepers for the front half: front 241919, 3/4 front
  left 241920, profile left 241921, profile right 241925 and 3/4 front right 241926. They match R6 closely,
  katana included.
- **Kontext cannot turn him around.** The three rear views (241922–241924) turn only the head; the body keeps
  the poncho's front. Restyling the Arthemy back views into R6's costume (back 241927 from A4, 3/4 back
  241928 from A5) gives true backs with the sword across them, but the poncho drifts red.
- **Next:** the front-half keepers plus the two restyled backs are the starting set for Zuzu's character
  LoRA (t-016), which is what fixes costume drift in the back views. The same recipe (Kontext front half,
  Arthemy back plus restyle) applies to the sister, toddler, coyote and nuns.

## The sword rig, and round 8

Silas, 2026-10-05, on the round-7 sheet: *"i'm not happy with them, given the sword problem, the angle is often
wrong and almost always consistently on his front when we have back views. Do again"*, and *"yes on the other
character sheets"*.

- **Canon:** the sheathed katana is strapped diagonally across his back, over the poncho, with the hilt above his RIGHT shoulder and the scabbard tip at his LEFT hip. From the front, only the hilt (over the right shoulder) and the scabbard tip (below the poncho at the left hip) show. From behind, the whole scabbard runs from upper right to lower left across the poncho.
- **Silas, clarifying:** *"when we have a back views, we should see the katana, but on many of those, the katana is still hidden, as if it's draped on his front"*. So the screen is strict: any back or 3/4-back view where the katana is not plainly visible across his back is rejected, however good the rest of it is.
- **Round 8, Stage A** (ART-ROUND-8.yaml): Arthemy renders, one figure per image, eight angles each (front,
  3/4 front left/right, profile left/right, 3/4 back left/right, back). Zuzu gets 3 seeds per angle; the
  sister, toddler, coyote and mother superior get 2 each. 88 private jobs.
- **Round 8, Stage B** (ANGLES-*.yaml): Kontext restyles the best Stage-A render per angle, with the pick
  stitched to its left as the reference. This replaces round 7's Kontext rotations, which could not turn a
  figure around.

### Round 8 screen (2026-10-05)

Every Stage-A render was read for orientation, the sword rig and clothing; nothing was undressed.

- **Zuzu** (24 renders + 12 retries): the back views are real backs with the katana across the back.
  Most failures were a second sword or a sword in hand. Stage B sources: front 241930, 3/4 front left
  242019, profile left 241936, 3/4 back left 241941, back 241942 (mirrored), 3/4 back right 241946,
  profile right = 241936 mirrored (all seven right-profile seeds failed), 3/4 front right 242023.
- **The sister:** all 16 clean. Stage B, with the S2 front figure as the reference (ANGLES-SISTER.yaml).
- **The toddler:** all 16 already match T2, so no Stage B. Angles: 241970, 241972, 241975, 241976, 241978,
  241980, 241982, 241984 (front, 3/4 front L, profile L, 3/4 back L, back, 3/4 back R, profile R,
  3/4 front R).
- **The coyote:** the checkpoint keeps drawing a feather duster into his hand (C1 has one too); Stage B
  removes it (ANGLES-COYOTE.yaml), plus a right-hand stump variant of C1.
- **The mother superior:** already matches N2, so no Stage B. Several back views drew a second small otter.
  Angles: 242002, 242004, 242007, 242013 (mirrored), 242011, 242013, 242014, 242016 (same order).

## Silas's notes on the round-8 angle sheets (2026-10-05)

*"Def shouldn't have the tiny real otter hanging out with mother superior. Not sure why coyote has a feather duster. Zuzu is still too tall, he looks more like a koala, less like a human, much squatter. The siblings are dressed too cleanly and seem too 'rich'. They should be in rags, as if animals literally tore at them. Zuzu needs consistently colored pants, not blue, those look too much like denim. Overall the characters can have a little darker tone, less Disney, more Tarantino."*

- **Zuzu:** squatter and more koala than human: stubby legs, a round belly, a big round head, animal
  proportions. His trousers are always dark brown cloth, never blue or denim-looking.
- **The siblings:** in rags, as if animals tore at their clothes. Shredded, claw-torn, frayed, filthy. Never
  clean or well-off.
- **The coyote:** empty hands. The feather duster (it came from C1) is not part of him.
- **The mother superior:** alone. No small otter at her feet.
- **Tone:** darker, grittier and less Disney: more Tarantino, grindhouse contrast, muted and grimy.
- **Round 9** (ART-ROUND-9.yaml, ArtJobs 33698–33727) is a 30-render look test of these notes: three views
  per character, before full angle sets. Zuzu's pending round-8 Kontext jobs (33688–33697) were cancelled,
  since his proportions change.

### Round 9 look test results (2026-10-05)

The best of each character, front / profile / back, sent to Silas for a yes on the look:

| Character | Front | Profile | Back |
|---|---|---|---|
| Zuzu | 242083 | 242103 (Kontext: extra sword removed) | 242102 mirrored (Kontext: katana moved across the back) |
| The sister | 242060 | 242061 | 242064 |
| The toddler | 242065 | 242068 | 242069 |
| The coyote | 242090 | 242092 | 242093 |
| The mother superior | 242096 | 242098 | 242100 |

What fixed the stubborn problems:
- **Prompt words leak as objects.** "Duster coat" put a duster (or a frond) in the coyote's hand; it is a
  "trench coat / long riding coat" now. "Mother superior" added a small otter beside her; she is an "abbess,
  elderly head nun" now. Both had resisted heavy negatives.
- **"Squat" made Zuzu crouch.** "Chubby, standing upright" with stubby legs gives the short koala build.
- **Arthemy will not strap the katana across his back in back views.** A Kontext single-image edit
  ("move the sword across his back") does it in one pass; Kontext is reliable at moving objects, not at
  turning figures around.
- **Still open:** the coyote's coat drifted tan; the full set pins olive green.

## Round 10: the eight-angle sets (2026-10-05)

Silas approved the round-9 look ("Much better designs!"); round 10 (ART-ROUND-10.yaml, ArtJobs 33749–33836)
renders every character at eight angles in it. Picks, in turn order:

| Character | Front | 3/4 front L | Profile L | 3/4 back L | Back | 3/4 back R | Profile R | 3/4 front R |
|---|---|---|---|---|---|---|---|---|
| Zuzu | 242192 (Kontext: extra sword removed) | 242108 | 242110 | 242113 | 242117 | 242120 | 242193 mirrored (Kontext) | 242125 |
| The sister | 242128 | 242130 | 242132 | 242135 | 242137 | 242138 | 242140 | 242143 |
| The toddler | 242144 | 242146 | 242148 | 242150 | 242153 | 242154 | 242156 | 242158 |
| The coyote | 242160 | 242162 | 242165 | 242166 | 242168 | 242171 | 242173 | 242174 |
| The abbess | 242177 | 242179 | 242181 | 242182 | 242185 | 242186 | 242188 | 242191 |

- **Zuzu's back views now work as rendered:** one katana diagonally across his back over the poncho, hilt over
  his right shoulder. Only the front and right profile needed a Kontext edit (a second sword at the waist).
- **The coyote's holster** sits on his left hip in the front views; canon puts his gun hand on the right. Fix in
  the LoRA captions or a later pass.
- **The coyote's stump:** the first Kontext edit (242194) bandaged both wrists and kept both hands; two
  stronger retries are queued (ANGLES-COYOTE.yaml, r10-coyote-stump-b/c).
- **Next:** these 40 angles are the training sets for the character LoRAs (t-016).
- **Coyote stump, outcome:** stump-c (242196) is the only render with the right wrist ending in a bandaged
  stump, but it bloodied his other hand. The cleanup (stump-d, 242197) restored both hands. Kontext keeps
  "healing" the amputation when asked to change anything else; the next try should be a masked edit limited to
  the one hand.

## Silas's notes on the round-10 sets (2026-10-05)

*"Masked edit. Yes fix the holster. Zulu's angles have him differently weighted, portly is the best, a7 profile
right is where we want him"*

- **Zuzu's build is portly (superseded below: a bit of a beer belly, not fat all over).** A7 (profile right, 242193 mirrored) is the reference: a big round pot belly pushing
  the poncho out, wide hips, thick short limbs. Kontext re-weights the other seven picks toward it
  (ANGLES-ZUZU.yaml, r11-zuzu-portly-*).
- **The coyote's sides:** eyepatch on his right eye, revolver on his right hip; right is his gun hand, the one
  the croc takes. Round 10 mixed the sides from angle to angle, so 242160 is mirrored, 242165, 242166 and
  242171 stand, and masked Kontext edits move the eyepatch or holster on 242162, 242168, 242173 and 242174.
- **The coyote's stump** is now a masked edit: only his right hand can change (r11-coyote-stump-masked-*).
  `scripts/enqueue_art_requests.py` gained `mask_box` for this: one or more boxes, sent with a generated mask
  to Kind Robots' `/api/comfy/kontext/enqueue`.

## Silas's notes on the round-10 coyote and abbess (2026-10-05)

*"There are some issues with mother superior. Her snout is too long. Coyote vagrant is too clean cut. He's had a
harder life. Outfit should reflect that. He's very very poor. Every day is a fight to survive. Love the siblings.
No notes"*

- **The siblings are approved as they are** (round-10 sets).
- **The coyote is destitute:** a tattered, patched coat with a shredded hem, rags under it, ripped trousers,
  falling-apart boots, a crushed hat, mangy fur, starving and gaunt. Every day is a fight to survive.
- **The abbess has a short, blunt otter muzzle:** a round, flat face, never a long or pointed snout.
- **Round 12** (ART-ROUND-12.yaml, ArtJobs 33857–33888) re-renders both at eight angles. The coyote's pending
  side fixes and two stump seeds on the clean round-10 outfit were cancelled; the masked stump and side fixes
  rerun on the new coyote.


## Zuzu portly edits, round 11 screen (2026-10-05)

A7 (242193 mirrored) is the reference build and stays as it is. Kontext re-weighted the other seven picks:

| Angle | Source | Edit | Verdict |
| --- | --- | --- | --- |
| Front | 242192 | 242199 | Keep: heavier, close to A7 |
| 3/4 front left | 242108 | 242200 | Only slightly heavier; chained retry (33903) |
| Profile left | 242110 | 242201 | Keep: round belly matches A7 |
| 3/4 back left | 242113 | 242202 | Reject: turned to face front, lost the katana |
| Back | 242117 | 242203 | Reject: belly drawn on his back |
| 3/4 back right | 242120 | 242204 | Keep: wider, katana still across his back |
| 3/4 front right | 242125 | 242205 | Keep: heavier, sword unchanged |

"Pot belly" on a back view makes Kontext either turn him round or put the belly on his back, so the back retries
(r12-zuzu-portly-*, ArtJobs 33899–33902) ask for a broad, rounded back and a wide seat and never say "belly".

## Round 12 coyote screen (2026-10-05)

The destitute prompt helped the fronts: torn hems, ripped trousers, and 242207 shows his ribs. From behind, though,
the coat stayed whole and the boots sound, and two seeds came out grey-faced. The sides were still mixed. Picks are
chosen for pose and sides, then a Kontext destitute pass (ANGLES-COYOTE.yaml, r12-coyote-rags-*, ArtJobs
33904–33911) pushes each one further into rags:

| Angle | Pick | Sides |
| --- | --- | --- |
| Front | 242207 | Eyepatch right; holster on his left, needs a masked fix |
| 3/4 front left | 242209 | Both right |
| Profile left | 242218 mirrored | Patch and holster land on the near (left) side; needs a masked fix |
| 3/4 back left | 242216 mirrored | Holster right |
| Back | 242214 | Holster right |
| 3/4 back right | 242212 mirrored | Holster right |
| Profile right | 242218 | Both right |
| 3/4 front right | 242220 | Both right |

The masked stump goes on the front after the rags pass.

## Round 12 abbess: discarded, masked face edits instead (2026-10-05)

"(short blunt muzzle:1.4)" made Arthemy draw a literal muzzle, a dog-style restraint, on all 16 seeds, and the fur
drifted to purple and green. The round-10 set stays. A masked Kontext edit (ANGLES-ABBESS.yaml, ArtJobs 33912–33918)
redraws only the head box on seven angles as a short, round otter face. The back view (242185) shows no face and
stands as it is. VIDEO-GUARDRAILS.md now lists the words the models draw literally.

## Silas's notes on round 12 and the portly edits (2026-10-05)

*"Much better overall look on the vagrant. Otter has a weird face mask on some of the gens, and still has too long of
a snout. She should have a flatter, but not totally flat face. Zuzu should have a bit of a beer belly, but not
overall fat like the latest looks."*

- **The coyote's round-12 look is approved in direction.** The destitute pass (33904–33911) still runs; it will be
  shown beside the plain picks so Silas can choose.
- **The abbess:** a snout about half as long, a little flatter, never completely flat. The r12 face edits were
  cancelled before they ran. The r13 masked edits (ArtJobs 33927–33935) ask for exactly that.
- **Zuzu has a bit of a beer belly**, not a fat body. The r11 portly edits (242199–242205) are dropped, and the r12
  retries were cancelled. Masked waist edits on the round-10 picks (r13-zuzu-belly-*, ArtJobs 33919–33926) add a
  paunch and leave his limbs, shoulders and hips alone. The back views keep their round-10 build.

## Masked edits cannot reshape (2026-10-05)

The r13 masked edits on Zuzu's waist and the abbess's face hardly changed anything. The abbess's snouts came back
the same length. Two of Zuzu's came back with a flat, unshaded blob on the belly (242269, 242271). Masked Kontext
suits adding or removing a small thing, such as the coyote's hand. It does not suit changing a shape. The r14 jobs
are plain, unmasked Kontext edits on the round-10 picks, with modest prompts:

- Zuzu: a beer belly only (ArtJobs 33967–33974).
- The abbess: a snout half as long (ArtJobs 33975–33983).

The coyote's extra rags pass (242247–242254) went to Silas beside the round-12 picks (cast sheet 13). Row B is
grittier, but on the front angles his face drifted toward a bear and two lost the eyepatch. The recommendation is row
A, the round-12 picks.

## r14 results (2026-10-05)

**Zuzu's beer belly** (cast sheet 14). The picks:

| Angle | Pick | Note |
| --- | --- | --- |
| Front | 242316 | Both front tries widened him all over; this is the milder one |
| 3/4 front left | 242317 | |
| Profile left | 242320 | |
| 3/4 back left | 242113 | Round 10; back views hide the belly |
| Back | 242117 | Round 10 |
| 3/4 back right | 242120 | Round 10 |
| Profile right | 242193 mirrored | A7 |
| 3/4 front right | 242321 | |

The alternates are 242315, 242318, 242319 (a balloon belly) and 242322.

**The abbess:** the unmasked edits (242323–242331) also left her snout as it was; Kontext keeps redrawing the
round-10 face. Two new tries ask for a sea otter, whose face is naturally short and round:

- ART-ROUND-13.yaml: an Arthemy look test, front and profile, 3 seeds each (ArtJobs 33997–34002).
- r15-abbess-sea-otter-*: Kontext species-change edits on three key angles (ArtJobs 34003–34005).

## The abbess's sea-otter face (2026-10-05)

Asking Arthemy for a sea otter worked. The front tries (242334–242336) and profile tries (242337–242339) came out with
a short, rounded otter face that is still clearly a snout, not flat. The Kontext species edits (242340–242342) barely
moved, as before. The face test went to Silas (cast sheet 15), and the other six angles are rendering with the same
tags (ART-ROUND-13.yaml, ArtJobs 34006–34017).

## The abbess, round 13 full set (2026-10-05)

| Angle | Pick | Note |
| --- | --- | --- |
| Front | 242336 | |
| 3/4 front left | 242344 | |
| Profile left | 242338 | |
| 3/4 back left | 242345 | A sea otter lies behind her; Kontext removes it (34018) |
| Back | 242347 | Water at her feet; Kontext removes it (34019) |
| 3/4 back right | 242350 | A small otter peeks out; Kontext removes it (34020) |
| Profile right | 242352 | |
| 3/4 front right | 242354 | |

"(sea otter:1.3)" also drew real sea otters and water on 242345, 242348, 242350 and 242351. VIDEO-GUARDRAILS.md now
warns about it.
