# Shifting Desks: complete card-art style bake-off

**Status:** creative pitches for Silas to review, 2026-10-13 PT. None of these proposals replaces or deletes Classic. No alternate card render is claimed as finished. Pilot requests are **staged only**, not added to the live `projects/art-prompts.yaml` queue before the checkpoint/render payload and outcome can be verified.

## What changes

The existing **Classic** set remains the baseline and default. Offer one **global per-player art style** at public `/play/shifting-desks`, usable on the front desk and during play; remember it across refreshes independently of seeded saves. Every card, location, department arrival, review/boss, job, society, mutation, Window 9 applicant and card back resolves its chosen style from a separate image namespace. If that one file is missing, show the existing Classic version, not a broken blank. Changing style must never change choices, dice, saves, script, progression, or UI text.

There are **110 distinct art subjects** in the current runtime inventory: **60 encounters, 5 reviews, 15 locations, 5 department arrivals, 4 Window 9 applicants, 5 job portraits, 6 secret societies, 8 mutation portraits and 2 backs**. Full IDs, titles, source scene descriptions and Classic paths are in [STYLE-CATALOG.json](art/STYLE-CATALOG.json). The catalog preserves the original source scene, so each candidate is a *different artistic reading of the same actual card*, not a generic style image.

## Four choices

| Style | Render lane | Mood | Where it should shine | Watch out for |
| --- | --- | --- | --- | --- |
| **Classic: The Company Smile** | Existing Krea 2 | Mid-century corporate safety posters, gouache, manila and carbon blue, second-look horror | Silly bureaucracy and the existing art library | Too uniform and too beige across 65 encounters/reviews |
| **Corporate Noir: A Stamped Confession** | **Illustrious Arthemy Western Art v3.0** (`Illustrious/arthemyWesternArt_v30.safetensors`) | Graphic novel acting, bold inks, deep shadows, violent perspective and conspicuously cheerful corporate props | Conspiracy, PAL's tests, Gus's labor organizing, the vault | Darkness can crush faces or bury the visual joke; preserve the scene silhouette |
| **Mandatory Fun: Department Cartoon** | **Illustrious furrytoonmix XL v3** (`Illustrious/furrytoonmix_xlV3.safetensors`) | Expressive animation cels, strong saturated accent colors, surreal machines, physical office comedy | Comedy and character acting, toy division, roaches and successors | Can become too childish; keep the dread in *consequences*, not gore |
| **Endless Department: Infinite HR** | **SDXL nihilmania** (`SDXL/sdxlUnstableDiffusers_nihilmania.safetensors`) | Eerie painterly halls, cavernous scale, ominous clinical light, office infrastructure swallowed by the vault | Records & Forms, Wellness & Testing, the Board | Repetitive empty hallways; each card must retain the character and action |

The above checkpoints are literal paths already listed in the Kind Robots Comic Studio lane registry. That is **repository evidence**, not confirmation of current render-box inventory or delivered Shifting Desks outputs. Comfy/Illustrious lanes use family-aware CLIP profile and tags. Arthemy's known author settings are Euler a, 30 steps, CFG 5. Classic Krea 2 stays unchanged.

## Fair pilot before anyone picks a winner

Render **the same three scenes in each alternate lane**, 9 candidate faces total. `art/STYLE-BAKEOFF.json` contains the complete scene-specific prompts, render lanes, fixed per-style seeds, image targets, and explicit `proposed` state. Compare each triptych alongside the already-delivered Classic face:

1. **Gus, Shop Steward:** seven-foot chestnut cockroach in mustard cardigan and half-moon glasses offers a handshake in Supply Closet B; a red stapler waits high on the shelf. Tests character identity, empathy, hands/claws, sincerity, and the second-look gag.
2. **Trust Fall Over the Shredder:** a worker tips back above giant industrial shredding rollers; Dale in a clip-on tie holds his arms out just a little too far away. Tests visual timing, slapstick hazard, expression, spatial clarity, and readable silhouettes.
3. **Something Ticking in the Toner:** a honey-colored plush bear with quilted hatch, mismatched button eyes and tiny atomic paw motif sits in the toner stacks while an adult worker reaches in. Tests cute/ominous tension, invented product design, material detail, and toy safety humor.

Each candidate keeps **one readable scene, subject in the upper two-thirds, breathing room for actual UI text, and the same recognizable character design**. The images themselves contain no lettering. Retain the positive-only prompt contract, checkpoint-specific positive styles, and the shared negative prompt for generated text, logos, watermarks, low-quality anatomy and multiframe compositions. No copied media designs.

## Prompt adaptation for *every* subject

`art/STYLE-CATALOG.json` includes all 110 source descriptions and each style's `prefix` / `tail` / checkpoint. For production use the original scene from the catalog plus the chosen lane's prefix and tail, while removing the **Classic medium terms only** (e.g., “mid-century safety-manual illustration,” “halftone grain,” and palette instructions). **Never strip concrete subjects, actions, locations, props or relationships.** This transforms a single authored source into three coherent checkpoint-specific variants for **all 110** cards/stations. All individual variants have distinct output paths; no asset should overwrite another style or Classic.

Path contract:

- Classic (unchanged): `/images/shifting-desks/cards/orientation/gus-shop-steward.webp`
- Corporate Noir: `/images/shifting-desks/styles/corporate-noir/cards/orientation/gus-shop-steward.webp`
- Mandatory Fun: `/images/shifting-desks/styles/mandatory-fun/cards/orientation/gus-shop-steward.webp`
- Endless Department: `/images/shifting-desks/styles/endless-department/cards/orientation/gus-shop-steward.webp`

These conventions apply to `backs/`, `locations/`, `departments/`, `jobs/`, `societies/`, `mutations/`, and `window/`. Art by style may be rolled out department-by-department, but **the selectable style remains global**, not a separate dice/game mode. Keep it outside the saved run version. Every missing variant falls back at the image component boundary.

## Review criteria and next gate

Inspect the 9 **actual completed checkpoint render images**, not only prompts or reference mood boards. Prefer a look that gives all three cards a shared visual identity without burying a gag, distorting Gus, or rendering the bear as a generic prop. Once Silas picks a winner, produce the full 110-image run with a durable per-style ledger and verified ArtJob/ArtImage IDs, first filling that winning variant and retaining all Classic files. If Silas prefers multiple full skins, the selector already supports them. Do not mark a style complete while fallback images are still showing.

**Gate:** no bulk generation, publication, home/Arcade promotion, or creative “winner” declaration until the human review; UI/source proposals remain on PRs under the normal outward-facing release gate. The user-facing selector may expose concepts only with an explicit "(concept)" label while render coverage is incomplete.
