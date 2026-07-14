# Image-Generation Quality Review

Date: 2026-07-14
Author: Reviewer (Claude, Silas-directed)
Scope: efficacy of the current auto-generated uploads across the two live art paths —
the **Monster Recast** text-to-image coloring-book pipeline (Flux-dev) and the
**Superkate Hair Studio / Kontext remix** image-to-image pipeline.
Status: assessment only — no generation settings changed yet. Fix menu at the end.

---

## TL;DR verdict

**The pipeline works, and at its best it is genuinely excellent — but two of its lanes
are shipping off-brief results, and the failures cluster in exactly the two places you
flagged.** The infrastructure (queue, relay, distribution, gates) is sound and the
human-approval gate is correctly catching the bad runs (they sit in `generated/`, not
`approved/`). What's broken is *prompt fidelity*, not plumbing:

1. **Monster Recast (text-to-image):** the *approved* set is on-target and print-worthy.
   The *recent auto-generated* pairs drift hard into cosmic/space poster art, lose the
   character, ignore the "no border / no text" rules, and — worst — the black-and-white
   "coloring page" slot is coming back in **full color**.
2. **Hair Studio / Kontext (image-to-image):** structurally can't do what you asked. There
   is **no masking at all** (every restyle repaints the whole frame → face/identity drift,
   the "glamour shot" problem), **no reference-weight knob** (the "weight from the original
   picture" you want to change literally doesn't exist as a parameter), and a **random seed
   every run** (good results can't be reproduced).

Your three asks — *tweak generation settings*, *add adaptive masking to the hair styler*,
*change the weights from the original picture* — are all correct and each maps to a concrete
finding below.

---

## 1. The good news — the pipeline can deliver

The `approved/` folder proves the ceiling is high. These are on-brief, faithful, and
production-usable:

- `perfect-woman-color.webp` / `-bw.webp` — monumental stitched Frankenstein-woman in a
  lab; the BW is a clean, faithful line conversion of the color master. Textbook.
- `moon-torn-bw.webp` — colossal she-wolf howling on rooftops under a full moon; perfect
  coloring-page line weight, closed regions, readable silhouette.
- `masked-countess-color.webp`, `masking-up`, `screwhead`, `prom-king`, `victorian-barber`,
  `draculina`, etc. — consistent graphic-horror voice, strong composition.

So when the specific subject survives to the model, the output is exactly right. The
failures below are about the subject **not** surviving.

---

## 2. Monster Recast — what's going wrong

### 2a. "I expected monsters, I got outer space" — two stacked causes

**Cause A (by design): a large share of the cast is intrinsically cosmic.** A run of these
concepts genuinely *is* space art, not monster art:
- `characters.yaml:11,15` — "cosmic ringmaster", "cosmic circus horror"
- `characters.yaml:367,390` — Hex Appeal, "cosmic witch… stirring a galaxy in a teacup"
- `characters.yaml:446,468` — Stella Vore, "crystalline extraterrestrial empress and cosmic diplomat"
- `pages.yaml:274-285` — "cosmic-quick-change", "cosmic runway finale", "asteroid runway under laughing moons"
- `coloring-book/DESIGN-BRIEF.md:57` — "1 cosmic trio page" is baked into the 28-page plan

If you were shown a batch weighted toward those, "outer space" is the accurate read of the
*prompts*, not a pipeline bug.

**Cause B (a real defect): non-cosmic concepts are also collapsing into generic space
posters.** This is the one that shouldn't happen. Two recently auto-generated pairs, both
marked `done` in `unapproved-art-jobs.yaml`, have prompts with **zero** cosmic content yet
rendered as cosmic pulp posters:

| Concept | Actual prompt (`art-modeler-request.yaml`) | What generated | Verdict |
|---|---|---|---|
| `mr-010` "The Madam in the Hat" | tall undertaker-governess apparition, black-paper body, mourning hat, grief-haunted domestic room, expressionist geometry (`:130`) | split yellow/blue **bald man's face** on a grungy poster field w/ orange orb + border | unrelated to prompt |
| `mr-013` "Ansel Bell" | haunted antique **boy doll** in a nursery, porcelain skin, pageboy hair, toys in rows (`:159`) | color: cosmic tree-creature under a red moon on an alien planet; bw: full-color **glamour portrait of a young woman** w/ paint splotches | unrelated to prompt |

Both share the same signature — poster vignette, garbled fake title text, split-tone
faces — and neither resembles its concept. When two different prompts produce the *same*
generic look, the specific subject text is being under-weighted and the model is free-running
into its default "cool poster" prior. Contributing factors:

- The style block is **front-loaded**: `consume_monster_recast_art.py:130` sends
  `COLOR_PREFIX + scene_prompt`, and `queue_monster_recast_art.py:74` sends
  `f"{HOUSE_STYLE} {prompt}"`. A ~60-word style preamble ahead of the subject makes Flux-dev
  weight composition/style over the (later) subject noun. The distinctive character gets lost.
- Flux-dev's "poster / theatrical illustration" attractor loves borders, title bars, and
  cosmic backdrops — none of which are being suppressed (see 2c).

**Note:** the confirmed-cosmic explanation (Cause A) does *not* cover `mr-010`/`mr-013` — their
prompts are grief-domestic and haunted-nursery. Those two are genuine subject-collapse
failures, not "cosmic concept" cases.

### 2b. The black-and-white "coloring page" slot is returning full color

`generated/bw/mr-010-madam-hat.webp` and `generated/bw/mr-013-ansel-bell.webp` are **full
color**, not line art — one is a surreal color tree-monster, the other a color photo-portrait.
The whole point of the BW slot is the printable coloring page (`BW_PREFIX` in
`consume_monster_recast_art.py:43`, and the `coloring_conversion_prompt` in `pages.yaml:22`).
The approved BW pages (`moon-torn-bw`, `perfect-woman-bw`) are correct line art, so a working
path exists — but the recent automated BW conversion **did not apply** (wrong slot content,
color instead of ink). This is the clearest instance of "losing vital information when we
prompt for a specific scenario": the line-art instruction is being dropped on the automated
path.

### 2c. Negative prompts are effectively dead on the Flux path

`art-modeler-request.yaml:22` and the per-job `negativePrompt` forbid "border, readable text,
watermark, collage, multiple panels" — yet the failed outputs have all of those. Reason:
`consume_art_queue.py:182-186` wires the KSampler's `negative` input to the **same** node as
`positive` (the FluxGuidance/positive encode), with `cfg: 1`. There is no negative-conditioning
encode, so **every negative prompt in the repo has no effect** on Flux output. All cleanup
constraints ("no text", "no border", "not cosmic") currently depend entirely on *positive*
wording.

### 2d. Expectation gap: "comic pages" vs a coloring book

Worth naming directly: nothing in the spec ever requested **comic pages** (multi-panel
sequential art). `monster-recast` is defined as a **coloring book of one illustration per
page** (`coloring-book/DESIGN-BRIEF.md:53`), and the generators *explicitly exclude* comic
panels (`queue_monster_recast_art.py:34` "no comic panels";
`consume_monster_recast_art.py:39` lists "comic panels" as a thing to avoid). So if you're
picturing comic pages, the pipeline is currently built to produce the opposite on purpose. If
comic/sequential pages are actually what you want, that's a scope change to the prefixes and
the book framing — not a tuning fix.

### 2e. Minor consistency issues

- **Settings drift between manifests:** `art-modeler-request.yaml:19` says `steps: 30`;
  `unapproved-art-jobs.yaml` defaults `steps: 36`. Pick one.
- **Engine mismatch vs the documented reference:** the model-builder reference runs use
  **SDXL/comfy** with seed-locking for identity (`character-deck-amibot.generate.yaml:9`), and
  TALKBACK frames the styler strategy as **"Kontext-first"** (`TALKBACK.md:895`). But live
  monster generation actually runs on **Flux-dev GGUF** (`consume_art_queue.py:73`). The docs
  and the running engine disagree.

---

## 3. Hair Studio / Kontext remix — why your own photo comes back wrong

Path: `stylist-restyle.vue` → `stylistStore.ts:240` → `POST /api/comfy/kontext/enqueue` →
`server/api/comfy/kontext/utils/workflow.ts` (the authoritative graph). The store sends only
`prompt + imageData` — **no** denoise, guidance, steps, seed, or size — so every restyle runs
on the hardcoded defaults, and **nothing is exposed in the UI**.

| Lever | Where | Current value | Adjustable? |
|---|---|---|---|
| Denoise | `workflow.ts:35,130` | 1.0 (full) | No |
| FluxGuidance | `workflow.ts:32,159` | 2.5 | No |
| Steps | `workflow.ts:31,129` | 20 | No |
| Sampler / scheduler | `workflow.ts:33,34` | res_multistep / sgm_uniform | No |
| **ReferenceLatent weight** | `workflow.ts:219` | **none — node takes no weight param** | **No** |
| Canvas / aspect | `workflow.ts:29-30` | **1024×1024 square; input aspect ratio discarded** | No |
| **Masking** | — | **absent entirely (full-frame img2img)** | **No** |
| Seed | `workflow.ts:37-43` | **random every run** | No |
| Negative prompt | — | none in the Kontext graph | No |

This directly explains your two failure modes:

- **"Over-modified / glamour shot / turned into a different person":** with **no mask**, the
  whole frame is reconditioned every run, so the face, skin, and background all drift — not
  just the hair. Identity is defended only by a *text suffix* ("keep the same person, same
  face", `stylist-restyle.vue:469`) with no structural anchor (no mask, no ControlNet, no
  IP-Adapter). At full denoise (1.0) + guidance 2.5, the prompt easily overpowers that suffix
  and "improves" the subject into someone else. The forced **1024×1024 square** also crops/
  reshapes portrait photos, compounding the "that's not me" feeling.
- **"Pure gibberish":** the model is `flux1-kontext-dev-Q5_K_M.gguf` (a fairly aggressive
  quant, `workflow.ts:231`) running at full denoise with a short prompt and a random seed. When
  the reference conditioning is weak relative to guidance, Kontext can collapse into texture
  mush — and with a random seed you can't just re-roll back to a good state.

**Your three asks, confirmed against the code:**

1. *Tweak generation settings* — correct. Guidance (2.5), steps (20), denoise (1.0) are all
   hardcoded with no UI. Add a real negative prompt (the graph has none). Lower guidance and/or
   preserve input aspect ratio.
2. *Add adaptive masking to the hair styler* — **there is no masking anywhere in the Kontext
   pipeline** (no `LoadImageMask`, `SetLatentNoiseMask`, `InpaintModelConditioning`, or any
   hair segmentation). This is net-new work: add hair/face segmentation (SAM or a face-parsing
   model) → feed a hair-only mask so only the hair region is repainted. That single change fixes
   most of the "it changed my whole face" problem.
3. *Change the weights from the original picture* — the current graph mixes the source photo
   via `ReferenceLatent` (`workflow.ts:219`) **at fixed, un-weighted strength** — ComfyUI's
   stock node has no scalar. To dial "how much of the original survives" you must swap in a
   weighted-reference / conditioning-strength node or add a timestep-range mechanism. The knob
   you want to turn doesn't physically exist yet.

---

## 4. Recommended fixes, priority-ordered

**Monster Recast (fast, high-leverage):**
1. **Fix the BW slot** so coloring pages come back as line art, not color — verify the
   color→line conversion step actually runs on the automated path (`consume_monster_recast_art.py`).
   This is the most concrete "lost information" bug.
2. **Move the subject to the front** of the assembled prompt (subject first, style block after)
   so Flux-dev stops collapsing distinctive characters into generic posters.
3. **Make the negative prompt real** on the Flux path: add a proper negative CLIP encode instead
   of pointing `negative` at the positive node (`consume_art_queue.py:182-186`), or bake the
   bans ("no border, no text, no cosmic background unless specified") into *positive* phrasing,
   since negatives are currently inert.
4. **Reconcile settings** (steps 30 vs 36) and decide the canonical engine (Flux-dev vs the
   SDXL/Kontext the docs describe). Consider **seed-locking** per concept for reproducible reruns,
   as the character-deck reference run already does.
5. **Decide the "comic vs coloring book" question** — the current output matches the coloring-book
   spec, not comics. If you want comics, that's a deliberate reframing.

**Hair Studio / Kontext (bigger, but this is the core of your ask):**
6. **Add hair masking** (segmentation → `SetLatentNoiseMask`/inpaint conditioning) so only the
   hair changes. Biggest single win against the "glamour shot" drift.
7. **Add a reference-strength / original-weight control** by swapping the stock `ReferenceLatent`
   for a weighted variant, and expose it (plus guidance and a "subtle→bold" slider) in the UI.
8. **Preserve input aspect ratio** instead of forcing 1024×1024, and **let the user lock a seed**
   so a good result can be reproduced and iterated.
9. **Add a negative prompt** to the Kontext graph (e.g. "different person, distorted face,
   oversmoothed skin, plastic, deformed").

Items 1–4 are quick config/prompt edits in **conductor**. Items 6–9 are code changes in
**kind_robots** (`server/api/comfy/kontext/`) and would each be a scoped, reversible PR.

---

---

## 5. Fixes applied (2026-07-14, Silas-directed "take the evening")

**conductor — Monster Recast (commit on this branch):**
- `queue_monster_recast_art.py` + `consume_monster_recast_art.py`: subject now
  leads the prompt; the house-style block trails (was style-first → subject
  collapse on non-cosmic concepts). BW leads with an unambiguous line-art
  instruction. Bans stated positively (negatives are inert on Flux cfg=1).
- `scripts/art_quality.py` (new): objective quality gate, pure/self-tested
  (`--selftest` 7/7). Rejects a "bw" render that came back colored, a
  blank/degenerate frame, or a landscape where portrait was expected. Wired
  into the live consumer — a failing render moves to `rejected/` and stays
  pending instead of being marked done. Also the objective floor for the
  autonomous promote-to-`approved/` curation goal.
- Reconciled steps drift (30 → 36).

**kind_robots — Hair Studio / Kontext (commit on this branch):**
- `workflow.ts`: `originalWeight` (0..1) img2img init from the encoded source
  at denoise = 1 − weight — the "weight from the original picture" knob; also
  restores the source aspect ratio (no more forced square). Real
  `negativePrompt` + `cfg` via CFGGuider (Flux ignores negatives at cfg=1).
  `maskName` support (LoadImageMask + SetLatentNoiseMask, core nodes) so a hair
  mask restricts changes to the hair region.
- `enqueue.post.ts` / `stylistStore.ts` / `stylist-restyle.vue`: controls
  threaded through; a live "how much should it still look like them?" strength
  slider (defaults toward preservation), an opt-in extra-protect toggle, and
  advanced guidance/steps.

### Still open (needs the studio box / a live run — cannot verify from here)
1. **Mask SOURCE.** The mask *path* is shipped and ready, but nothing generates
   a hair mask yet — there is no hair-segmentation node on the ComfyUI box and
   no client-side seg lib. True adaptive hair-only masking needs either (a) a
   segmentation custom node installed on the box, or (b) an in-browser
   hair-segmentation / quick-brush step feeding `maskData`. Until then the
   shipped identity fix is `originalWeight`. → superkate `t-018`.
2. **Live tuning pass.** The default preserve strength (0.3), guidance, and the
   negative wording want one real run on the studio box to dial in — too subtle
   vs. too loose is a box-only judgement. → superkate `t-019`.
3. **Verify the Monster Recast re-render** on the box: confirm the subject-first
   prompts hold the character and the BW slot now returns line art (the guard
   will reject it if not).
4. **Negative prompt on the automated Flux path** (`consume_art_queue.py`) is
   still inert by design; making it real needs cfg>1 + a negative encode and a
   live test — left as a deliberate, separate change.

*Evidence: direct visual inspection of `projects/coloring-book/sets/monster-recast/{approved,generated}/*.webp`
and the settings/prompt-assembly code cited inline.*
