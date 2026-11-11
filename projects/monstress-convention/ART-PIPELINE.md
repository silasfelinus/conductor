# MONSTRIQUE — Character Models, Art Styles and Cutscenes

_2026-11-11 PT, from Silas's brief of the same day (verbatim below). This is the production
contract for how one story is drawn in several media. CHARACTER-LOOKBOOK.md stays the visual
canon for the cast; this file says how that canon becomes models, LoRAs, sprites and cutscenes.
Code lives in Kind Robots under `utils/monstrique/` (model sheets, styles, cutscenes) and is
covered by `utils/scripts/verifyMonstriqueArtPipeline.test.ts`._

> Make meaningful improvements on Monsterique. Remember we expect a leisure suit Larry vibe, both
> in humor and in character models and interactions, outside the animated cut scenes interspersed.
> We can use generation of character models that will eventually be Lora's. The story should be
> able to be told in multiple art styles, between 2d point and click adventure and 3d animated
> cutscenes.

## The split that makes multi-style work

**Identity lives in a character model sheet. Style lives in a style. Neither describes the other.**

- `characterModels.ts` holds one sheet per recurring character (Iris, Norb, Odette, Violet,
  Marta, Dolores, Gavin, Pip, Cleo, Draculina, Siobhan, Nyx, Albina): species, a stated adult
  apparent age, a 64-px silhouette line, ordered identity traits, wardrobe, Larry-style acting
  notes, an expression set, a `never` list (Norb never handsome, Albina never human-faced,
  Draculina never a schoolgirl) and a vector sprite rig.
- `artStyles.ts` holds the styles: **2D point-and-click** (the playable game), **retro pixel**
  (optional skin), **3D animated cutscene** (interstitials), **storyboard** (animatic previz),
  **model sheet** (LoRA datasets) and **scrapbook pin-up** (mature edition only, never explicit).
- `composeCharacterPrompt` / `composeShotPrompt` join one sheet (or a cutscene shot's cast) with
  one style and return an ArtJob-shaped request. Every prompt carries the character's LoRA
  trigger and a universal negative (child, minor, teen, school uniform, nude, explicit, gore,
  real-person likeness). The general edition can never compose the pin-up style or a cast member
  not yet approved for it.

## LoRA plan

1. **Identity LoRAs, not style LoRAs.** Each character trains on ten style-neutral model-sheet
   renders (`loraDatasetPlan`): front / three-quarter / profile / back turnarounds, two busts,
   walk, point, sit and signature-prop poses, all on plain grey. A LoRA that never saw a style
   can be stacked with any style.
2. **Trigger tokens** are `mnstq_<name>` (e.g. `mnstq_norb`). Captions start with the trigger and
   then tag what the LoRA must *not* absorb (framing, view, pose, background).
3. **Status per character**: `dataset-needed → dataset-ready → training → trained`. Until
   `trained` the composer writes the full identity description; after it, the LoRA is stacked via
   the enqueue `loras` field (ComfyUI chain, never `<lora:…>` text) and the description shortens.
4. **Human gate:** Silas approves every dataset image before training. Generated is not
   approved; queued is not delivered; delivered is not verified.
5. **Order:** Iris and Norb first (on screen in every scene), then Odette and Violet, then the
   motel regulars, then the stars by chapter.

## Cutscenes: one script, two media

`cutscenes.ts` scripts each cutscene as a shot list. Each shot carries a 2D panel caption, cast
with stage positions and expressions, an optional line and SFX, a **comic cutaway gag**, and a 3D
`camera` block (move, lens, seconds, character animation). The game plays shots as letterboxed 2D
panels with the vector cast; the admin build also shows the 3D director's notes. The same shot
renders as a 2D panel, a storyboard frame or a 3D key frame through `composeShotPrompt`.

Shipped scripts: **Cold Open** (built from the existing general and mature intro cards, so the
editions stay in lockstep), **Your New Client**, **Elbow Deep**, **A Cold Kiss** (mature only;
cuts away to the ice machine and Norb facing the wall) and **Get the Car**. Cutscenes trigger
when their flag first appears and never replay on load.

## Larry vibe in the playable game (outside cutscenes)

- **The cast is on stage.** Iris walks to whatever the player selects; Norb trails at a
  germ-safe distance inside a dashed "two-metre" ring; NPCs and both ghosts stand at their
  hotspots; whoever is speaking animates, and the dialogue box shows their portrait and name.
- **Caricature proportions.** Norb is 0.68 of Iris's height on a 3.2-head body; Albina towers at
  1.2; ghosts float and glow. The vector rigs are stand-ins with image-shaped slots; generated
  sprites replace them per character once delivered and approved.
- **A sardonic narrator** answers verbs that don't apply, Sierra-style.
- **Sierra points:** score out of **205** (one point per room number), derived from evidence and
  flags so saves didn't change. The general edition's maximum is lower because mature gags are
  hidden, never because evidence is.
- **Every wrong combination gets a joke** (bribing Marta with Odette's cash, handing Norb money,
  offering Odette the fangs).
- **New mature-only gags:** the Last Call Lovin' vending machine sells "garlic-scented protection"
  with a joke for every character it's offered to, and the one cramped bed in Room 207 sends Norb
  onto the balcony. Neither gates a clue.

## Gates (unchanged)

No ArtJobs were enqueued by this work. Public Play/nav/highlights, any adult art, and LoRA
datasets still need Silas's explicit visual review (t-013). Spoilers never go into model sheets
or prompts: Draculina's sheet and the cutscene scripts are tested to contain no culprit language.
