# Monstress Convention — Changelog

## 2026-11-05 PT
- Registered original adult mystery point-and-click as active Conductor software project.
- Added complete first-pass design bible, hotel location map, writing and clue guardrails.
- Laid out implementation and human-gated release milestones. No game code or public release yet.

## 2026-11-05 PT — Revised canon from Silas
- User-facing game and franchise name now MONSTREXX, convention is a city venue, motel a separate starting cluster; internal slug retained.
- Iris becomes primary, Nico germophobic deduction foil; two murdered adult women become independently interrogable ghosts.
- Separate convention, occult gag shop, vampire mansion and sewers with albino alligator woman; mummy actress and idol group; optional romance scrapbook.
- Old Celestine murder/Odette killer canon superseded; mature access and public launch gate unchanged.

## 2026-11-06 PT — Monstrexx title-front implementation
- Kind Robots PR #4848 adds `/admin/monstrexx` cinematic console front with New Game, Continue, Settings and Scrapbook, plus internal account-scoped progress.
- Boss art direction changed to short, ugly, geeky comic caricature; provisional display name Norb Vale (runtime key `nico` retained).

## 2026-11-06 PT — Canonical MONSTRIQUE identity and historical album run
- Silas selected **MONSTRIQUE** as game/franchise name, superseding the earlier MONSTREXX display brand without changing internal coordination/save identifiers.
- Added FRANCHISE-HISTORY.md with seven expulsions/replacements, music eras, public-versus-real stories, Pack and NEXT acts, aspirant hot-tub lounge and Odette's archive contracts.
- Added ALBUM-ART-REGISTER.md recording the seven generated concept covers and the distinction between draft images and art actually delivered to the game.
- Restated mature-only internal-preview and separate human-publication gate.

## 2026-11-06 PT — Renamed MONSTRIQUE; story bible; Chapter 1 rewrite
- Silas renamed the game and franchise **MONSTRIQUE**, set it in **Midnight City**, made Odette's ghost the client and Violet a companion hired to play a vampire. Tone is ribald Larry-style comedy with "low morals".
- New `STORY-BIBLE.md`: verbatim brief, tone rules, Midnight City districts (reconciled to defer to FRANCHISE-HISTORY.md's seven-era ledger), the five-Hexblade case with a **proposed** culprit (creative-approval), gratitude system, six-chapter plan and puzzle principles.
- Kind Robots (branch `claude/monsterique-game-dev-4wwv1i`, built on PR #4848): route `/admin/monstrique` (old routes redirect), Monstrique branding, new cold open, Odette hires Norb, Flirt verb with Norb's escalating rebuffs, Violet's fangs and fee favours with use-item inventory, gratitude-gated non-explicit kiss, versioned save upgrade (v2 → v3).

## 2026-11-07 PT — Silas's decisions: Draculina in the last act; Cleo Pappatra
- Culprit locked: **Draculina**, revealed only in Chapter 6. Marta ("Little Miss Nobody") becomes the Chapters 2–5 misdirect and a Chapter 6 witness. STORY-BIBLE's case, endings and chapter plan were rewritten; mist, the mirror and a borrowed alibi tape carry the fair-play reveal.
- Mummy star renamed **Cleo Pappatra** across DESIGN-BRIEF, FRANCHISE-HISTORY, ALBUM-ART-REGISTER, ART-PROMPTS and STORY-BIBLE. Kind Robots game code was renamed to match.

## 2026-11-11 PT — Larry-style staging, character models, multi-style art and cutscenes
- New `ART-PIPELINE.md`: identity lives in character model sheets, style lives in styles; identity LoRAs (`mnstq_<name>`) train on style-neutral model-sheet datasets so one LoRA stacks with 2D, pixel and 3D styles. Silas approves every dataset image before training.
- Kind Robots: 13 character model sheets, six art styles (2D point-and-click, retro pixel, 3D cutscene, storyboard, model sheet, mature-only pin-up), a prompt composer with universal adult/no-explicit negatives, and per-character LoRA dataset plans. No ArtJobs enqueued.
- Cutscenes are shot lists playable as 2D letterboxed panels and directable as 3D key frames: Cold Open (from the existing edition intro cards), Your New Client, Elbow Deep, A Cold Kiss (mature only) and Get the Car.
- Playable scene: Iris walks to selections, Norb trails inside a germ ring, NPCs and ghosts stand on stage as caricature vector stand-ins, speaker portraits, Sierra score out of 205, a sardonic narrator, wrong-item jokes, and mature-only vending-machine and bed gags.

## 2026-11-10 PT — Painted title splash and Play-card hero
- Silas: "A really artistically generated front end, with a racier splash if the maturity is on, not this svg stuff. And we need a hero on the highlight page."
- Rendered on Krea 2 via `art/FRONT-SPLASH-GENERAL-R1.yaml` and `art/FRONT-SPLASH-MATURE-R1.yaml` (priority 100; 18 jobs, all delivered). Re-rendered once to keep painted lettering out of the logo area and keep Norb homely.
- Picks: general landscape ArtImage 268790, portrait 268796, hero 268789 (shipped as static files in Kind Robots `public/monstrique/front/`). Mature landscape 268798 and portrait 268801 stay private `isMature` ArtImages, served only through the gated `/api/monstrique/splash` route, and await Silas's visual approval before their ids are switched on.

## 2026-11-10 PT — Series bible, Norb and Iris redesign, monster-women pin-ups
- Silas's direction: Bakshi-meets-monster-squad look, an uglier Quasimodo/Igor Norb in a hand-me-down
  MONSTRIQUE shirt, a 100% professional Norb whose harassment complaint becomes a power-structures debate,
  and Iris as a baddie with a white streak, a necker boyfriend's neck plaster and a high-school tramp stamp.
- Kind Robots: `/admin/monstrique-bible` series bible (new additive `MonstriqueBibleEntry` table), five new
  monster-star model sheets, sprite rig hump/shirt/streak/plaster, new dialogue topics.
- Queued `art/MONSTER-WOMEN-PINUPS-R1.yaml`: 160 mature, private pin-ups across seven Illustrious
  checkpoints and Krea 2.

## 2026-11-11 PT — Pin-up batch: two checkpoints retired
- Realism Illustrious By rendered explicit nudity in shower pin-ups and Miaomiao 3D rendered near-explicit,
  hyper-exaggerated bodies, despite the no-nudity negatives. Their 24 pending jobs were cancelled; both lanes
  are removed from the series bible (Kind Robots PR #4999), which also adds weighted no-nudity negatives.
  The already-rendered images remain private `isMature` ArtImages pending Silas's call on deletion.

## 2026-11-11 PT — Softcore unlock tier and nudity lane
- Silas wants softcore nudity as possible mature-edition unlocks. Realism Illustrious By returns as the
  series bible's nudity lane with a "Softcore unlock" art kind (adults only; explicit sex acts excluded).
  Miaomiao 3D stays retired. First ten softcore renders queued: `art/MONSTER-WOMEN-SOFTCORE-R1.yaml`.

## 2026-11-11 PT — Batch review, Monstrique Studio card
- Pin-up batch complete (136 renders on 7 lanes). Verdict: Krea 2 and Arthemy hold monster anatomy and the
  Bakshi look best; Furrytoon is strong on anthro but exaggerated (one uncovered Albina shower render);
  Illustrij and Illustrious Realism humanize most stars.
- Softcore batch complete (10 renders): all adult, no sex acts. Roxie shows genital detail and Draculina has a
  blood smear; Realism-By humanized Albina, Roxie, Siobhan and Vespa.
- The admin preview and series bible became one "Monstrique Studio" tile with art-server card art
  (`art/STUDIO-CARD-R1.yaml`, ArtImage 269001).

## 2026-11-11 PT — Mature splash approved; softcore test on Arthemy and Furrytoon
- Silas approved the mature title splash (ArtImages 268798 and 268801), now served through the gated splash route.
- Softcore round 2 queued on Arthemy and Furrytoon (`art/MONSTER-WOMEN-SOFTCORE-R2.yaml`, 20 renders) with extra
  negatives against genital detail and gore; both lanes may take softcore requests in the series bible.
