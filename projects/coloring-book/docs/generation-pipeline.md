# Coloring-Page Generation Pipeline

date: 2026-07-10
task: coloring-book/t-004 (research portion)
status: research complete; prototype generations still to run
related: t-003 (engine spec), t-006/t-007 (launch sets), docs/pod-coloring-books.md (t-009)

## Scope and verification caveat

Research for the page-generation pipeline: LoRA survey, Kontext prompt-only
conversion patterns, region-fill approach for the interactive app, and the
print-ready page spec. Web verification was done 2026-07-10; the session proxy
**blocked direct fetches of civitai.com and huggingface.co**, so LoRA license
details below come from search-result snippets and secondary mirrors. Every
license MUST be re-verified on the model page itself before any commercial
launch (Civitai per-model permission flags — "sell generated images" /
"use on generation services" — are set per upload and were not directly
readable this session).

## 0. Licensing reality check (read first)

This shapes every engine choice:

- **FLUX.1 [dev] and FLUX.1 Kontext [dev] weights are under the FLUX
  Non-Commercial License** (bfl.ai/legal/non-commercial-license-terms).
  Key nuance: **outputs** may be used commercially ("Generated outputs can be
  used for personal, scientific, and commercial purposes"; outputs are not
  Derivatives), but **running the model as part of a commercial service** —
  which the KR page generator with paid tokens is — requires a commercial
  license.
- The clean path: **generate through a licensed API provider** (fal.ai,
  Replicate, Together, Runware — all serve FLUX.1 Kontext [dev] under
  commercial arrangements with BFL; e.g. Replicate states outputs from its
  Kontext dev endpoint are free for commercial use). BFL also sells self-serve
  self-hosted commercial licenses (usage-metered via their API) if we ever
  self-host.
- **LoRAs trained on FLUX.1-dev are arguably Derivatives** and inherit the
  base license regardless of the openrail/apache tag the uploader picked on
  HF. Practically: using a dev LoRA through a licensed endpoint (fal's
  `flux-kontext-lora` / `flux-lora` endpoints accept arbitrary LoRA URLs) is
  the industry-normal route.
- Bases with genuinely permissive licenses exist: **FLUX.2 klein (Apache
  2.0)**, **Z-Image Turbo (Apache 2.0)**, **HiDream-I1 (MIT)**. Coloring-book
  LoRAs exist for all three (see table) — these are the safest long-term
  bets for a paid generation feature.

## 1. LoRA survey — coloring book / line art

### Free, license-plausible for commercial use

| Name | Source | Base model | License (verify!) | Trigger | Weight / notes |
|---|---|---|---|---|---|
| Coloring Book Flux (renderartist) | civitai.com/models/794953 · huggingface.co/renderartist/coloringbookflux | FLUX.1-dev | HF tag: creativeml-openrail-m; Civitai listing under FLUX.1-dev non-commercial base. Author markets it "for coloring books, posters, print on demand, stock imagery" — author intent is commercial-friendly, base-model service restriction still applies | `c0l0ringb00k`, `coloring book page` | 0.7–0.9; DEIS sampler recommended; explicitly prompt "white background". Best-regarded FLUX coloring LoRA; 100-image synthetic training set (humans, vehicles, animals) |
| Coloring-Book-Flux-LoRA (prithivMLmods) | huggingface.co/prithivMLmods/Coloring-Book-Flux-LoRA | FLUX.1-dev | creativeml-openrail-m (HF tag) | `Coloring Book` | Community LoRA, decent samples; less documented than renderartist's |
| COLORINGBOOK-REDMOND-FLUXKLEIN9B (artificialguybr) | huggingface.co/artificialguybr/COLORINGBOOK-REDMOND-FLUXKLEIN9B | **FLUX.2-klein-9B (Apache 2.0)** | **Apache 2.0** — cleanest commercial story in this table | `ColoringBookAF`, `Coloring Book` | Trained on curated coloring-book dataset; author recommends ComfyUI. Best license + modern base combo |
| Coloring Book Z (renderartist) | civitai.com/models/2194923 · huggingface.co/renderartist/Coloring-Book-Z-Image-Turbo-LoRA | **Z-Image Turbo (Apache 2.0)** | Apache-2.0 base; check model page flags | see model page | Turbo base = very cheap/fast generations; good candidate for the free tier |
| Coloring Book HiDream (renderartist) | civitai.com/models/1518899 · huggingface.co/renderartist/coloringbookhidream | **HiDream-I1 (MIT)** | MIT base; check model page flags | see model page | LyCORIS; "great line art styles" per listing |
| ColoringBook.Redmond (artificialguybr) | civitai.com/models/136348 | SDXL (also SD1.5/2.1 variants) | CreativeML OpenRAIL++ family | `ColoringBookAF` | Older generation, weaker line quality than FLUX-era options; fallback only |

### Kontext-specific (image→image editing base)

| Name | Source | Base | License | Trigger / usage | Notes |
|---|---|---|---|---|---|
| Kontext-Style-Loras — `Line` style (Owen777) | huggingface.co/Owen777/Kontext-Style-Loras | FLUX.1 Kontext-dev | **FLUX.1 Non-Commercial License (explicit LICENSE.md)** — flag: only via licensed endpoint, and re-check redistribution terms | prompt: "Turn this image into the Line style." | 20+ style pack (also Ghibli, American_Cartoon, etc.) trained on GPT-4o-generated pairs. The `Line` LoRA is the closest thing to a dedicated "make it line art" Kontext LoRA found |
| RefControl Reference-Lineart LoRA (thedeoxen) | civitai.com/models/1902256 · huggingface.co/thedeoxen/refcontrol-flux-kontext-reference-lineart-lora | FLUX.1 Kontext-dev | see model page | reference image + lineart map | **Different job**: applies a reference style onto existing lineart (coloring/rendering direction, i.e. the reverse of ours). Noted so we don't confuse it; could later power "color my page for me" |

### Paid / gated / unverified — flagged separately

- **Civitai "Coloring Book Flux LoRa" (civitai.com/models/1712954)** — third-party
  upload found only via the civitai.green mirror; uploader, license flags, and
  quality unverified. Do not use until checked.
- **No paid/gated coloring-book LoRA was found** on the marketplaces surveyed —
  this niche is well covered by free LoRAs. Some Civitai uploads restrict
  "use on generation services" via per-model flags; that flag could not be read
  through the proxy this session and is the #1 thing to re-verify per model.
- Training our own Kontext coloring LoRA is cheap if prompt-only quality
  disappoints: fal.ai's `flux-kontext-trainer` takes before/after pairs
  (colored art → extracted line art), and we can synthesize pairs from KR
  gallery assets.

## 2. Kontext prompt-only line-art conversion

FLUX.1 Kontext [dev] is an instruction-following image editor; community and
BFL guidance (docs.bfl.ml Kontext i2i prompting guide) converge on:

- **Name the transformation precisely** — "convert to coloring book line art"
  outperforms "make it a drawing".
- **State what to preserve** — composition, subject identity, framing.
  Explicit preservation clauses are what stop Kontext redrawing everything.
- **Enumerate the negative space** — say "no shading, no hatching, no gray"
  explicitly; Kontext honors stated exclusions better than implied ones.
- **Say "white background / pure white fill"** — known to matter for
  coloring-book outputs (same advice as the renderartist LoRA card).
- Iterate: run the conversion, then a second Kontext pass to fix residual
  gray fills ("remove all gray shading, keep only black outlines") if needed.

### Candidate prompt templates (to A/B in the prototype step)

**T1 — canonical conversion (start here):**
> Convert this image into a coloring book page: clean black outline drawing on
> a pure white background. All lines are smooth, closed, and uniform in weight.
> Every region is empty white, ready to be colored in. No shading, no hatching,
> no gray tones, no color. Preserve the original composition and subject.

**T2 — kid-friendly simplification (for busy source images):**
> Turn this image into a simple coloring book page for children: bold, thick
> black outlines, large simple shapes, pure white background. Simplify small
> details into clean closed regions. No shading, no cross-hatching, no gray
> fill, no texture. Keep the subject recognizable and the composition intact.

**T3 — detail-preserving (adult coloring / KR hero art):**
> Redraw this image as an intricate coloring book illustration: fine, even
> black line art on a pure white background, with every area enclosed by
> closed outlines so it can be colored. Convert textures and shadows into
> decorative line patterns with white space between them, not gray shading.
> No solid black areas larger than a line. Preserve composition and details.

**T4 — flood-fill-safe emphasis (regions must close):**
> Convert to a black-and-white coloring page: uniform-weight black outlines
> forming fully closed shapes on a pure white background. Lines must connect —
> no gaps, no broken strokes, no open contours. Interior of every shape is
> pure white. No shading, gradients, stippling, or gray pixels. Same
> composition as the input.

Text-to-image (new pages from prompts, t-007 path) uses the same style clauses
appended to a subject description, plus the LoRA trigger when a LoRA is
loaded, e.g. `c0l0ringb00k, coloring book page, a glamorous werewolf drag
performer with a giant wig and feather boa on stage, thick clean black
outlines, pure white background, no shading`.

## 3. Region-fill approaches for the interactive app

The app needs "tap a region, it fills with the selected color". Three options,
honestly compared:

### (a) Raster flood fill on the line art — RECOMMENDED for v1

Canvas bucket fill (scanline flood fill with color-distance tolerance)
directly on the generated PNG.

- **Pros:** cheapest thing that ships — ~150 lines of well-understood canvas
  code or a tiny dependency (e.g. `q-floodfill`); zero preprocessing, works on
  *any* line-art image including user-generated pages the moment Kontext
  returns them; this is how essentially every casual mobile coloring app works;
  undo = keep fill history; export = the canvas itself.
- **Cons / issues and mitigations:**
  - *Line gaps leak fill into neighbors.* Mitigate at generation time (prompt
    T4 "closed shapes, no gaps"; pick the best of N candidates) and at
    post-process time: threshold to pure B/W, then **morphological dilate the
    line layer by 1–2 px (line closing)** on a hidden "boundary mask" canvas
    used only for the fill algorithm — display stays crisp while fills respect
    the fattened boundaries. A one-time gap check (flood from outside; regions
    that merge with the page background are leaky) can flag bad pages in the
    pipeline before they ship in a set.
  - *Anti-aliased edges leave gray halos.* Fill with tolerance (~32/255
    RGB distance) and post-fill edge blend, or fill on a thresholded mask and
    composite under the original line layer (line art stays on top via
    `multiply` blend — fills can never paint over lines).
  - *No semantic regions* (can't do mural-style "group fills" without extra
    data). Acceptable for v1; the pipeline can later emit a region map
    (approach c) without changing the UI.

### (b) Vectorize to SVG regions (potrace / vtracer)

Trace the raster line art to SVG, extract enclosed paths as clickable regions,
and feed the existing mural WonderLab SVG engine (PR #135).

- **Pros:** reuses the shipped mural interaction model verbatim (per-section
  fills, group fills, swatches, Pinia persistence); resolution-independent;
  regions have identity → named/grouped regions, per-region undo, saved
  palettes map cleanly.
- **Cons:** a real pipeline stage with real failure modes — potrace traces
  *strokes as filled shapes*, so "the white region inside" must be derived
  (even-odd holes → region polygons), which gets messy on intricate pages;
  vtracer output needs cleanup (speckles, merged regions across line gaps —
  the same gap problem, now baked into geometry); per-page QA burden; large
  SVGs (thousands of nodes) can be heavier to render than one bitmap. This is
  days-to-weeks of tuning vs hours for (a).

### (c) Generation-time region maps

Emit a machine-readable region map alongside the page (e.g. flood-fill label
map computed once server-side, or a second model pass / segmentation like SAM).

- **Pros:** best of both — raster display with semantic regions; server does
  the gap-closing once; enables group fills and "color by numbers" modes.
- **Cons:** most machinery of the three; only works for pipeline-produced
  pages unless user generations also run the mapping step; premature before
  the coloring surface exists.

### Recommendation

**Ship (a) raster flood fill for v1**, with the post-processing steps
(threshold, line-close mask, outside-leak QA check) built into the generation
pipeline so pages are flood-fill-safe by construction. Design the page data
model (t-003) so a page = `{raster, optional regionMap, optional svg}` — that
keeps (c) as a drop-in upgrade and lets the mural SVG engine consume the same
sets later, instead of blocking v1 on it. This matches the design brief's
bias: cheapest thing that ships, proven by every casual coloring app.

## 4. Print-ready page spec (8.5×11 POD interiors)

Verified against KDP's published requirements (kdp.amazon.com help topics
G201834340 / GVBQ3CMEQW3W2VL6); Lulu/IngramSpark use compatible conventions
(0.125" bleed, 0.5" margin guidance). Full provider detail in
docs/pod-coloring-books.md.

| Property | No-bleed page | Full-bleed page |
|---|---|---|
| Trim size | 8.5 × 11 in | 8.5 × 11 in |
| File page size | 8.5 × 11 in | **8.625 × 11.25 in** (trim + 0.125" bleed on outside/top/bottom) |
| Pixels @300 DPI | **2550 × 3300** | **2588 × 3375** |
| Outside/top/bottom margin (safe zone) | ≥ 0.375" (0.5" recommended) | ≥ 0.375" from trim edge |
| Inside (gutter) margin | ≥ 0.375" for ≤150 pages (KDP table); use 0.5–0.75" so art never dives into the spine | same |
| Resolution | 300 DPI minimum, grayscale or pure B/W | same |

Practical choices for our pages:

- **Generate no-bleed pages with a white margin frame.** Coloring pages don't
  benefit from bleed (art running off the page edge is anti-user here), and
  no-bleed avoids the harder 8.625×11.25 layout and looser trim tolerances.
  Target: art box ≈ 7.5 × 9.75 in (2250 × 2925 px) centered with ≥0.5"
  margins on a 2550 × 3300 canvas.
- **One source serves both uses.** Master = 2550×3300 PNG (300 DPI,
  thresholded line art). Print path: place 1:1 into the interior PDF.
  Screen path: serve a downscaled copy (e.g. 1275×1650 or responsive sizes);
  flood fill runs fine at screen resolution, and export-to-image can render
  fills at full master resolution by scaling fill coordinates (or simply
  re-running the fill history against the master).
- Generation-native resolution is lower (FLUX ~1–2 MP; e.g. 1088×1408 ≈
  0.773 aspect matches 7.5:9.75 well). Upscale to 2250×2925 with a line-art
  friendly method (threshold → 2–3× lanczos or ESRGAN-lineart → re-threshold);
  clean 1-bit line art upscales nearly losslessly, unlike photos.

## 5. Recommended per-page generation config (v1)

- **Engine:** FLUX.1 Kontext [dev] via a **BFL-licensed API endpoint**
  (fal.ai `flux-kontext-lora` or Replicate `flux-kontext-dev`) — covers both
  image→page conversion (KR assets, user images) and the commercial-service
  license problem. Text→page generation: same provider's FLUX dev/klein
  endpoint + coloring LoRA.
- **Prompt:** template **T1** as default for conversions, **T4** clauses
  appended when the page is destined for the interactive app; **T2** for a
  "simple/kids" toggle; T3 reserved for detailed adult-style sets.
- **LoRA:** start prompt-only on Kontext (zero extra license surface); if
  style consistency disappoints, add **renderartist Coloring Book Flux**
  (trigger `c0l0ringb00k, coloring book page`, weight 0.8) for text→image
  pages, and evaluate **COLORINGBOOK-REDMOND-FLUXKLEIN9B** (Apache 2.0,
  trigger `ColoringBookAF`) as the long-term commercially-clean default.
- **Generation size:** 1088×1408 (or provider-closest 0.77 aspect).
- **Post-processing (deterministic, in order):**
  1. Grayscale → Otsu/fixed threshold to pure 1-bit black/white
  2. Despeckle (remove connected components < ~20 px)
  3. Upscale to 2250×2925, re-threshold
  4. Build fill-boundary mask: dilate lines 1–2 px (used by the app's flood
     fill, not displayed)
  5. Leak QA: flood from canvas corner; flag pages where interior regions
     merge with background
  6. Compose 2550×3300 master with centered art box + white margins
  7. Write metadata JSON (prompt, template id, model+endpoint, LoRA+weight,
     seed, source image ref, date) — generated-art rule
- **Per-set:** manifest (title, cover, ordered page list, source
  attributions) as specified in the design brief.

## Sources

- https://civitai.com/models/794953/coloring-book-flux · https://huggingface.co/renderartist/coloringbookflux · https://renderartist.com/portfolio/coloring-book-flux-lora/
- https://huggingface.co/prithivMLmods/Coloring-Book-Flux-LoRA (license/trigger via search snippets + dataloop.ai mirror)
- https://huggingface.co/artificialguybr/COLORINGBOOK-REDMOND-FLUXKLEIN9B
- https://huggingface.co/Owen777/Kontext-Style-Loras (+ LICENSE.md, discussion #2 for the Line style)
- https://huggingface.co/thedeoxen/refcontrol-flux-kontext-reference-lineart-lora · https://civitai.com/models/1902256
- https://huggingface.co/renderartist/Coloring-Book-Z-Image-Turbo-LoRA · https://civitai.com/models/1518899/coloring-book-hidream
- https://bfl.ai/legal/non-commercial-license-terms · https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev · https://replicate.com/black-forest-labs/flux-kontext-dev · https://bfl.ai/announcements/flux-1-kontext-dev
- https://docs.bfl.ml/guides/prompting_guide_kontext_i2i (403 through proxy; principles corroborated via kontext-dev.com and academy.techpresso.co prompt guides)
- https://fal.ai/models/fal-ai/flux-kontext-lora · https://help.scenario.com/en/articles/flux-kontext-loras-use-cases
- https://kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6 (trim/bleed/margins; snippets via kdpeasy.com and coverlabpro.com)
