# Shifting Desks: approved selectable art styles

**Decision: 2026-10-13 PT.** Silas has explicitly chosen three playable visual editions: **Classic**, **Noir**, and **Western Cartoon**. The selected Western Cartoon reference is Gus greeting a shocked employee in Supply Closet B, in a richly inked, high-contrast animated Western illustration with warm orange and fluorescent green light.

## Immutable Classic plus two additional image sets

Classic stays untouched at `/images/shifting-desks/<kind>/<id>.webp`. The same 110 station subjects are generated for each selected alternative at:

- `/images/shifting-desks/styles/corporate-noir/<kind>/<id>.webp`
- `/images/shifting-desks/styles/western-cartoon/<kind>/<id>.webp`

Scope: **60 encounters + 5 boss reviews + 15 locations + 5 department arrivals + 4 Window 9 applicants + 5 job portraits + 6 society portraits + 8 mutation portraits + 2 card backs = 110 subjects**, each appearing in both new lanes for **220 new ArtJobs**. Every source prompt and Classic image path is in [art/STYLE-CATALOG.json](art/STYLE-CATALOG.json). The `projects/art-prompts.yaml` request IDs start `shifting-desks-style-v2-`, and every request carries the correct `public/images/` media target, a unique image URL, a `variant: image`, and a real checkpoint family. No queue request points at Classic.

**Classic**: Existing Krea 2 mid-century safety posters and art. Remains available from launch and is the per-image fallback for any variant not yet rendered.

**Noir** (`corporate-noir`): Western graphic novel ink, substantial black shadows, strong action silhouettes, green phosphor accents and theatrical staging. Actual checkpoint `Illustrious/arthemyWesternArt_v30.safetensors`; author's 30 steps / CFG 5 / Euler ancestral.

**Western Cartoon** (`western-cartoon`): Rich western animation feature, dramatic low-angle staging, graphic ink, honey-orange highlights against luminous green fluorescents, charismatic facial acting, tactile detailed surfaces. **Not** the rejected flat office gag-strip aesthetic. Uses the same registered Arthemy Illustrious checkpoint with a different positive prompt style and individual render seeds.

The earlier Mandatory Fun/furrytoonmix and Endless Department/nihilmania pitches were **rejected** and are not in the new app style selector or queue. The original pitch experiments are historical only.

## Job submission architecture

All 220 requests use `engine: sdxl-checkpoint` rather than a mislabeled Krea workflow; `scripts/dream_sdxl_checkpoint_art.py` now admits these two specific families *only* for project `shifting-desks`, builds real `CheckpointLoaderSimple` → Illustrious `CLIPSetLastLayer(-2)` → KSampler → VAE → SaveImage graphs, and verifies the actual CHECKPOINT Resource registry at submission. The existing `scripts/consume_art_requests_to_media.py` attaches `targetRepo`, `imagePath`, `idempotencyKey`, records the resulting ArtJob ID, and verifies media delivery by HEAD. The existing `Auto Art Generate` workflow on main triggers when the ledger merges; its normal schedule resumes incomplete jobs. Daily Dream stays priority 200; these requests use priority 10.

**Queue file merged ≠ ArtJob created ≠ rendered ≠ media verified ≠ aesthetically approved**. Report these stages separately. Do not fake completed IDs or claim that image conditioning from Silas's chat-uploaded reference is implemented by the text-only pipeline. The reference is the art direction and target, with actual checkpoint output to be visually reviewed.

## Browser interaction

`/play/shifting-desks` has an accessible, global style selector separate from deterministic saved run state. Changing style changes the image namespace, and a missing alternative falls back to Classic. Style preference persists across page reloads. Choice text, routes, rolls, and existing save schema are identical.

The generated images are independent assets, not replacements. No deletion or mass regeneration of Classic. The user authorized these new art submissions on 2026-10-13 PT.

## 2026-10-14 PT: Illustrious is the default, and every station is covered

Silas: *"now we should have multiple art styles. Make sure they are integrated, and they are presented to the user. Illustrious should be the default."*

- **Default.** New players start in **Western Cartoon**, the Illustrious edition built on the Gus reference Silas selected. **Noir** is the other Illustrious edition. **Classic** (Krea 2) remains a choice and the per-image fallback. Kind Robots bumps the preference key to `shifting-desks-art-style-v2`, so earlier visitors, who were silently saved on Classic, also land on the Illustrious default once.
- **Presented.** The front desk shows the three editions as image tiles, each previewing the same card in that style, and the in-game toolbar keeps a compact switcher.
- **Coverage.** All 220 original renders are delivered: every media URL answers 200. The lane now also covers the 10 epilogue cards and the Window 9 desk card, which were added after the batch was cut. That makes 121 subjects and 242 requests on the same `shifting-desks-style-v2-` lane, bulk-submitted like the rest. Until those 22 render, those cards show Classic.


## 2026-10-14 PT (later): Classic is the default again

Silas, after playing the Illustrious editions: *"the new art is actually worse than the classic. classic should be default."*

- **Default.** New players start in **Classic** (Krea 2), and it leads the picker. Kind Robots bumps the preference key to `shifting-desks-art-style-v3` so visitors saved on Western Cartoon while it was the default land on Classic. **Western Cartoon** and **Noir** remain choices; their queued renders (including the clothed Jam in Tube 14 re-render, #6168) still land.
- **Front page.** The art-first front desk is one giant hero painted in the chosen style, so the default hero is now the Classic orientation art.
- Do not flip the default back to an Illustrious edition without a new decision from Silas.
