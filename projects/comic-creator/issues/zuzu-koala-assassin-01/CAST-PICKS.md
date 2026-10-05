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
