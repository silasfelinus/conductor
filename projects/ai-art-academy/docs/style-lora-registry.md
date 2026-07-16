# Style LoRA Registry — AI Art Academy (task t-003)

date: 2026-07-10
status: research complete — no downloads performed (registry only)
scope: openly available style LoRAs for FLUX.1 dev / FLUX.1 Kontext dev covering
historical art movements and artists dead 70+ years (per DESIGN-BRIEF ethical boundary)

## Coverage summary

Of the **16 target styles**, research found:

- **8 LoRA-backed** (openly downloadable from Hugging Face, no login): impressionism,
  art nouveau, renaissance (Raphael), illuminated manuscript, watercolor, oil painting,
  expressionism (Kirchner), sumi-e/ink wash (Chinese ink, see caveat)
- **8 prompt-mode** (no login-free, openly licensed FLUX LoRA found — rely on
  FLUX/Kontext base-model knowledge, which the design brief says is expected and fine):
  ukiyo-e, baroque/chiaroscuro, cubism, stained glass, pointillism, gothic,
  byzantine mosaic, art deco
- **+2 bonus LoRA-backed styles** beyond the target list: Van Gogh (post-impressionism)
  and Pop Art, both from the Kontext-native style pack

**v1.1 update (2026-07-16, t-010 cycle):** the curriculum grew from 16 to 21 movements,
so three more prompt-mode entries were added here — `northern-renaissance`, `rococo`,
and `symbolism` — bringing prompt-mode styles to **11** (the existing `gothic` and
`pointillism` entries already covered two of the five new curriculum movements). Each
new prompt-mode entry carries a provisional `prompt_hint` in the machine-readable block;
none has a login-free FLUX LoRA yet, so hunting LoRAs for the five new movements is
filed as follow-on **t-021**.
- **11 Civitai candidates** parked in the "needs Silas" list — Civitai model pages and
  API were unreachable from this session (proxy policy), and Civitai downloads are
  commonly login/API-key-gated at the creator's option, so none can be verified or
  treated as available. Several would upgrade prompt-mode styles to LoRA mode if
  Silas checks them while logged in.

### Licensing headline (flag for t-004 and Silas)

Almost every FLUX LoRA in the ecosystem is published under the **FLUX.1 [dev]
Non-Commercial License** (inherited from the base model). That license permits
non-commercial and non-production use only. Implications:

1. **For evaluation (t-004): all entries below are fine to use now.**
2. **For a monetized generation service:** the base-model question is handled by
   whichever hosted API KR uses (fal / Replicate / BFL API carry commercial
   base-model licenses), but NC-licensed *LoRA weights* are a gray zone for
   production use. This needs a policy call before launch — see needs-Silas item S-0.
3. The one clean, commercially permissive LoRA found is the **Apache-2.0 watercolor**
   LoRA (gokaygokay) — worth treating as the reference case for what "safe" looks like.

Where a model card's license could not be confirmed from search results, the entry
says `license: unverified` — verify on the model page before production use.

## Machine-readable registry

```yaml
# mode: lora  -> curated LoRA below (t-004 A/B may still demote to prompt)
# mode: prompt -> FLUX/Kontext base-model knowledge only, no LoRA
# weight is a starting suggestion; undocumented cases default to 0.9
# base_model "kontext-dev" LoRAs are Kontext-native (best for the Remix studio);
# "flux-dev" LoRAs generally also load against Kontext dev but need t-004 eval.
# prompt_hint (optional, prompt-mode only): a provisional Kontext prompt-mode
#   instruction to seed the Remix studio before t-004 records the tuned template
#   in style-remix-configs.yaml. Added 2026-07-16 (t-010) for the newer prompt-mode
#   styles; older prompt-mode entries keep their recipe in the per-style prose below
#   and can be backfilled (t-021 kaizen).
styles:
  - style_slug: impressionism
    mode: lora
    lora_name: UmeAiRT/FLUX.1-dev-LoRA-Impressionism
    source_url: https://huggingface.co/UmeAiRT/FLUX.1-dev-LoRA-Impressionism
    license: "FLUX.1 [dev] Non-Commercial License (commercial: no; generation-service: no without BFL license)"
    base_model: flux-dev
    trigger: "impressionist"
    weight: 0.9
  - style_slug: ukiyo-e
    mode: prompt
  - style_slug: art-nouveau
    mode: lora
    lora_name: dvyio/flux-lora-art-nouveau
    source_url: https://huggingface.co/dvyio/flux-lora-art-nouveau
    license: "flux-1-dev-non-commercial-license (commercial: no)"
    base_model: flux-dev
    trigger: "illustration in the style of ARTNV"
    weight: 0.9
  - style_slug: baroque-chiaroscuro
    mode: prompt
  - style_slug: cubism
    mode: prompt
  - style_slug: renaissance-fresco
    mode: lora
    lora_name: davidrd123/Flux-Raphael-LoRA
    source_url: https://huggingface.co/davidrd123/Flux-Raphael-LoRA
    license: "other (unverified; FLUX.1-dev derivative, assume non-commercial)"
    base_model: flux-dev
    trigger: "in the style of a Raphael oil painting"
    weight: 0.9
  - style_slug: stained-glass
    mode: prompt
  - style_slug: illuminated-manuscript
    mode: lora
    lora_name: dvyio/flux-lora-medieval-illustration
    source_url: https://huggingface.co/dvyio/flux-lora-medieval-illustration
    license: "flux-1-dev-non-commercial-license (commercial: no)"
    base_model: flux-dev
    trigger: "illustration in the style of MDVL"
    weight: 0.9
  - style_slug: watercolor
    mode: lora
    lora_name: gokaygokay/Flux-Watercolor-Strokes-LoRA
    source_url: https://huggingface.co/gokaygokay/Flux-Watercolor-Strokes-LoRA
    license: "Apache-2.0 (LoRA weights commercial: yes; base-model service terms still apply)"
    base_model: flux-dev
    trigger: "WTRCLR"
    weight: 0.9
  - style_slug: oil-painting
    mode: lora
    lora_name: Kontext-Style/Oil_Painting_lora (Owen777/Kontext-Style-Loras)
    source_url: https://huggingface.co/Owen777/Kontext-Style-Loras
    license: "FLUX.1 [dev] Non-Commercial License v1.1.1 (commercial: no)"
    base_model: kontext-dev
    trigger: "Turn this image into the Oil_Painting style."
    weight: 1.0
  - style_slug: pointillism
    mode: prompt
    prompt_hint: "Repaint this image using pointillist technique: thousands of tiny separate dots of pure unmixed color that blend in the eye, a luminous divisionist surface, even all-over stippling, bright balanced light, in the manner of Seurat and Signac"
  - style_slug: expressionism
    mode: lora
    lora_name: davidrd123/lora-Kirchner-flux
    source_url: https://huggingface.co/davidrd123/lora-Kirchner-flux
    license: "other (unverified; FLUX.1-dev derivative, assume non-commercial)"
    base_model: flux-dev
    trigger: "in the style of an Ernst Ludwig Kirchner painting"
    weight: 0.9
  - style_slug: gothic
    mode: prompt
    prompt_hint: "Repaint this image as a late-medieval Gothic panel painting: figures on a burnished gold-leaf ground, elongated bodies with gentle S-curves, jewel-toned tempera, pointed-arch framing, flattened space, no modern shading"
  - style_slug: northern-renaissance
    mode: prompt
    prompt_hint: "Repaint this image as an Early Netherlandish oil painting: microscopic detail, luminous layered glazes, crisp naturalism, cool northern daylight, a meticulously rendered landscape or interior behind the figures"
  - style_slug: rococo
    mode: prompt
    prompt_hint: "Repaint this image as a Rococo oil painting: pastel palette of rose, sky-blue, and cream, feathery loose brushwork, soft diffused light, playful ornamental curves, a light and airy mood"
  - style_slug: symbolism
    mode: prompt
    prompt_hint: "Repaint this image as a Symbolist painting: dreamlike mysterious mood, muted twilight color, mythic and allegorical atmosphere, soft glowing light, a sense of reverie rather than plain reality"
  - style_slug: byzantine-mosaic
    mode: prompt
  - style_slug: sumi-e
    mode: lora
    lora_name: Kontext-Style/Chinese_Ink_lora (Owen777/Kontext-Style-Loras)
    source_url: https://huggingface.co/Owen777/Kontext-Style-Loras
    license: "FLUX.1 [dev] Non-Commercial License v1.1.1 (commercial: no)"
    base_model: kontext-dev
    trigger: "Turn this image into the Chinese_Ink style."
    weight: 1.0
  - style_slug: art-deco
    mode: prompt
  # Bonus styles (not in the t-003 target list, free wins from the Kontext pack)
  - style_slug: post-impressionism-van-gogh
    mode: lora
    lora_name: Kontext-Style/Van_Gogh_lora (Owen777/Kontext-Style-Loras)
    source_url: https://huggingface.co/Owen777/Kontext-Style-Loras
    license: "FLUX.1 [dev] Non-Commercial License v1.1.1 (commercial: no)"
    base_model: kontext-dev
    trigger: "Turn this image into the Van_Gogh style."
    weight: 1.0
  - style_slug: pop-art
    mode: lora
    lora_name: Kontext-Style/Pop_Art_lora (Owen777/Kontext-Style-Loras)
    source_url: https://huggingface.co/Owen777/Kontext-Style-Loras
    license: "FLUX.1 [dev] Non-Commercial License v1.1.1 (commercial: no)"
    base_model: kontext-dev
    trigger: "Turn this image into the Pop_Art style."
    weight: 1.0
```

## Per-style notes

### impressionism — LoRA

- **UmeAiRT/FLUX.1-dev-LoRA-Impressionism** (Hugging Face, anonymous download).
  Trigger `impressionist`. License: FLUX.1 [dev] Non-Commercial. Quality: purpose-built
  movement LoRA ("give a unique touch of impressionism"); UmeAiRT is an established
  FLUX LoRA author. Note the author concedes FLUX already does impressionism well —
  a good first A/B case for t-004 prompt-vs-lora.
- Rejected: Civitai "Flux Open Impressionism" (model 723757) — trained on the style of
  **Erin Hanson, a living artist**. Excluded under the ethical boundary. Do not revisit.
- Civitai alternates in needs-Silas list (S-1).

### ukiyo-e / woodblock — prompt-mode

- No login-free, openly licensed FLUX ukiyo-e LoRA found on Hugging Face (the good
  candidates all live on Civitai; see S-2/S-3/S-4). Hokusai (d. 1849) and Yoshitoshi
  (d. 1892) are firmly in-bounds ethically, so upgrading later is fine.
- Base-model knowledge is strong here (Hokusai is among the most-represented artists in
  training data). Prompt recipe: "Repaint this image as an ukiyo-e woodblock print in
  the style of Hokusai, flat color planes, bold outlines, visible woodgrain texture."
  Community notes: raw FLUX ukiyo-e output often adds calligraphy/stamps/borders —
  add "no text, no stamps, no border" to the template.

### art-nouveau — LoRA (+ Mucha artist variant)

- **dvyio/flux-lora-art-nouveau** (HF). Trigger `illustration in the style of ARTNV`.
  License: flux-1-dev-non-commercial-license (confirmed on the dvyio model family).
  Quality: dvyio's fal-trained style LoRAs are consistent and well-regarded.
- Artist-level variant for the Mucha lesson page: **derekl35/alphonse_mucha_qlora_flux**
  (also `derekl35/alphonse-mucha-fp8-lora-flux`), trigger "alphonse mucha style".
  From the official Hugging Face flux-qlora blog post; quality shown in the blog is
  good (decorative motifs, Mucha palette). Mucha d. 1939 — in-bounds.

### baroque / chiaroscuro — prompt-mode

- No dedicated FLUX baroque-painting LoRA found. Only lighting-effect LoRAs
  ("Chiaroscuro Lighting", "Rembrandt Lighting" in unofficial dump repos) — lighting,
  not painting style, and unverifiable licensing. Prompt-mode: "as a baroque oil
  painting with dramatic chiaroscuro lighting, in the style of Caravaggio / Rembrandt,
  deep shadows, single warm light source, rich dark palette."
- Partial LoRA assist if wanted: **renderartist/classic-painting-flux** (see
  oil-painting notes) leans old-master and covers much of this look.

### cubism — prompt-mode

- HF has only weak/undocumented candidates (`cosfil/cubism`, provenance unclear;
  `lichorosario/flux-lora-cubist-cartoon` is cartoon-cubism, wrong register for a
  history lesson). Picasso died 1973 — **less than 70 years ago** — so a
  "Picasso style" LoRA is out anyway; teach cubism as a movement. Braque d. 1963:
  also out for artist-name imitation. Prompt-mode: "repaint as an analytic cubist
  painting, fragmented geometric planes, multiple simultaneous viewpoints, muted
  browns and greys." (Movement prompt, no artist name, keeps us clean here.)

### renaissance-fresco — LoRA (Raphael), fresco texture via prompt

- **davidrd123/Flux-Raphael-LoRA** (HF). Raphael d. 1520 — maximally in-bounds.
  Descriptive trigger ("in the style of a Raphael oil painting"), license listed
  "other" (unverified — assume non-commercial). Caveat: it is a **LyCORIS** adapter —
  confirm the KR/relay loader supports LyCORIS before wiring it in; if not, demote
  this style to prompt-mode. Same author has other dead-artist LoRAs
  (Maurice Prendergast d. 1924, etc.) worth browsing for lesson pages.
- Fresco surface specifically (plaster texture, matte pigment) had no LoRA anywhere —
  handle in the prompt template: "as a renaissance fresco painted on aged plaster,
  matte mineral pigments, cracked surface."
- Civitai "Renaissance Art Style - FLUX" is a documented alternate (S-5).

### stained-glass — prompt-mode

- Plenty of FLUX stained-glass LoRAs exist — but all on Civitai (best-reviewed:
  "[Pinkie] Stained Glass Art", 67 positive reviews — S-6). Nothing login-free on HF
  (ostris's stained glass is SDXL-only). Base model handles "stained glass window with
  black lead lines, jewel-toned translucent glass, gothic tracery" well; expected fine.

### illuminated-manuscript — LoRA

- **dvyio/flux-lora-medieval-illustration** (HF). Trigger
  `illustration in the style of MDVL`. License: flux-1-dev-non-commercial-license.
  Quality: consistent dvyio family output; suits marginalia-style illustration.
- Fun alternate for lesson flavor: **multimodalart/medieval-animals-lora** (HF,
  manuscript-marginalia animals; from a Hugging Face staff account).

### watercolor — LoRA (best license in the registry)

- **gokaygokay/Flux-Watercolor-Strokes-LoRA** (HF). Trigger `WTRCLR`.
  **License: Apache-2.0** — the only confirmed commercially permissive style LoRA
  found. Primary pick for that reason.
- Alternates: **SebastianBodza/flux_lora_aquarel_watercolor** (HF, trigger
  `AQUACOLTOK`, very popular/high quality — the community reference for FLUX
  watercolor; license unverified, check the card) and
  **fal/Watercolor-Art-Kontext-Dev-LoRA** (HF, **Kontext-native**,
  flux-1-dev-non-commercial) — the natural A/B pairing for t-004 since it was
  trained for image-to-image restyling, exactly our Remix use case.

### oil-painting — LoRA (Kontext-native)

- **Kontext-Style/Oil_Painting_lora** from **Owen777/Kontext-Style-Loras** (HF) —
  a 22-style pack trained specifically **on FLUX.1 Kontext dev** with paired
  restyling data; the highest-relevance find of this research for the Remix studio.
  Prompt convention: "Turn this image into the Oil_Painting style." License:
  FLUX.1 [dev] Non-Commercial v1.1.1. Individual repos exist per style under the
  `Kontext-Style` HF org (e.g. huggingface.co/Kontext-Style/Oil_Painting_lora).
- Alternates: **renderartist/classic-painting-flux** (HF + Civitai; trigger
  `class1cpa1nt` + "oil painting", documented strength 0.7–1.0; **trained on
  public-domain Art Institute of Chicago masterpieces** — the most ethically
  aligned training set found; license unverified) and **bingbangboom/flux_oilscape**
  (HF, trigger `Oilstyle002`, landscape-leaning).

### pointillism — prompt-mode

- Backs curriculum movement §21 (Neo-Impressionism / Pointillism: Seurat d. 1891,
  Signac d. 1935, Cross d. 1910, van Rysselberghe d. 1926 — all in-bounds).
- Only Civitai candidates ("Pointillism Art Style - FLUX", trained on Signac /
  van Rysselberghe — both dead 70+ years, ethically fine — S-7). Prompt-mode
  (`prompt_hint` in the block above): "Repaint this image using pointillist
  technique: thousands of tiny separate dots of pure unmixed color that blend in
  the eye, a luminous divisionist surface, even all-over stippling, bright balanced
  light, in the manner of Seurat and Signac."
- **Teaching note / t-004 watch-item:** this is the most *mechanical* style in the
  set — the dot-field either reads or it doesn't. Base FLUX/Kontext tends to render
  the dots too coarse or to lapse into ordinary Impressionist dabs at small output
  sizes; evaluate at a higher resolution than the other styles and check actual dot
  density before shipping. A dedicated LoRA (S-7) is the most likely of the
  prompt-mode set to beat the base prompt — flag as a priority A/B pair for t-004.

### expressionism — LoRA (Kirchner)

- **davidrd123/lora-Kirchner-flux** (HF). Ernst Ludwig Kirchner d. 1938 — in-bounds.
  Descriptive trigger; license "other" (unverified, assume non-commercial). Quality
  unreviewed — t-004 should A/B against the movement prompt: "as a German
  Expressionist painting, jagged angular forms, clashing non-naturalistic colors,
  raw visible brushwork."
- Adjacent but rejected as primary: fal/Expressive-Art-Kontext-Dev-LoRA
  (Kontext-native but "expressive art" is a general painterly look, not the
  historical movement).

### gothic — prompt-mode

- Backs curriculum movement §17 (Gothic Panel Painting: Duccio d. 1319, Giotto
  d. 1337, Simone Martini d. 1344, Fra Angelico d. 1455 — all deeply in-bounds).
- FLUX candidates on Civitai only, and mostly gothic-*horror* or gothic-anime rather
  than the medieval Gothic art of the lesson ("Gothic Oil Painting Style" is closest —
  S-8). Prompt-mode (`prompt_hint` above): "Repaint this image as a late-medieval
  Gothic panel painting: figures on a burnished gold-leaf ground, elongated bodies
  with gentle S-curves, jewel-toned tempera, pointed-arch framing, flattened space,
  no modern shading."
- **Teaching note / t-004 watch-item:** shares the gold-ground family with
  `byzantine-mosaic` and `illuminated-manuscript`, so the gold background and
  tempera color transfer reliably. Two risks: the word "gothic" pulls the base model
  toward gothic-horror aesthetics (add nothing about darkness/skulls; keep the
  medieval-devotional cues explicit), and the model may bolt haloes or an altarpiece
  frame onto secular subjects — acceptable for portraits, distracting for landscapes.

### northern-renaissance — prompt-mode

- Backs curriculum movement §18 (Early Netherlandish/German: van Eyck d. 1441, van
  der Weyden d. 1464, Memling d. 1494, Bosch d. 1516, Bruegel the Elder d. 1569).
- No dedicated FLUX Early-Netherlandish LoRA found on Hugging Face (login-free); the
  `renderartist/classic-painting-flux` old-master LoRA (see oil-painting notes) partly
  covers the look and is the natural LoRA A/B partner. Prompt-mode (`prompt_hint`
  above): "Repaint this image as an Early Netherlandish oil painting: microscopic
  detail, luminous layered glazes, crisp naturalism, cool northern daylight, a
  meticulously rendered landscape or interior behind the figures."
- **Teaching note / t-004 watch-item:** distinct from the Italian `renaissance` entry
  (`renaissance-fresco` / Raphael LoRA) — this is the *northern*, oil-glaze, hyper-
  detailed tradition, not sfumato and classical balance. The failure mode is
  under-cooking into a generic "old oil painting"; the differentiators are the
  microscopic detail and the deep, sharply-focused background, so keep those in the
  template. Bruegel's peasant-genre subjects are a good demo image for showing how the
  style handles everyday scenes, not just portraits.

### rococo — prompt-mode

- Backs curriculum movement §19 (Rococo: Watteau d. 1721, Boucher d. 1770, Fragonard
  d. 1806, Chardin d. 1779 — all centuries in-bounds).
- No login-free FLUX Rococo LoRA found; base-model knowledge of 18th-century French
  painting is strong. Prompt-mode (`prompt_hint` above): "Repaint this image as a
  Rococo oil painting: pastel palette of rose, sky-blue, and cream, feathery loose
  brushwork, soft diffused light, playful ornamental curves, a light and airy mood."
- **Teaching note / t-004 watch-item:** the pastel palette and soft light are what
  sell it — a common miss is the model keeping the source photo's saturated/contrasty
  color, which reads as generic portraiture rather than Rococo. Consider adding
  "desaturated pastel, high-key lighting" if early A/Bs come back too punchy. Chardin's
  quieter still-life register is a useful counter-example in the lesson (same era, very
  different mood) but the remix template should target the Boucher/Fragonard sparkle.

### symbolism — prompt-mode

- Backs curriculum movement §20 (Symbolism: Moreau d. 1898, Puvis de Chavannes
  d. 1898, Böcklin d. 1901, Redon d. 1916 — all in-bounds).
- No dedicated FLUX Symbolism LoRA found (the term collides with modern "symbolic/
  surreal" aesthetic LoRAs, which are off-register). Prompt-mode (`prompt_hint`
  above): "Repaint this image as a Symbolist painting: dreamlike mysterious mood,
  muted twilight color, mythic and allegorical atmosphere, soft glowing light, a
  sense of reverie rather than plain reality."
- **Teaching note / t-004 watch-item:** Symbolism is the loosest *visual* signature
  in the set — it transfers as mood and palette (twilight, haze, glow) more than as a
  hard technique, so evaluate it on atmosphere, not on a recognizable brush handling.
  Expect results that read as "dreamy twilight repaint"; set that expectation in UI
  copy. Guard against the base model sliding into modern digital-fantasy or
  airbrushed-surrealism looks — anchor on the named 19th-century painters in the
  lesson, not on generic "surreal."

### byzantine-mosaic — prompt-mode

- No byzantine-specific LoRA anywhere; Civitai has only generic/modern mosaic-tile
  LoRAs. Base model knows the look: "as a Byzantine mosaic of small glass tesserae,
  gold background, frontal iconographic figures, visible grout lines."

### sumi-e / ink wash — LoRA (with a naming caveat)

- **Kontext-Style/Chinese_Ink_lora** (Owen777 pack, HF, Kontext-native). This is
  Chinese ink-wash (shuǐmò) rather than Japanese sumi-e — same technique family,
  different tradition; the lesson copy should teach the distinction even if the
  LoRA is shared. License: FLUX.1 [dev] Non-Commercial v1.1.1.
- Japanese-specific alternate on Civitai: "Mystic Sumi" (S-9).

### art-deco — prompt-mode

- Civitai-only candidates (best: "Art Deco LoRA [FLUX+SD+XL+Pony]", trigger
  `artdeco_v4` — S-10). HF's only hit (ClashR) is a noir-deco hybrid, off-register.
  Base-model prompt: "as a 1920s Art Deco poster, streamlined geometric forms,
  strong symmetry, gold and jewel tones, sunburst motifs" — Deco is extremely well
  represented in training data; expected fine.

### Bonus: post-impressionism (Van Gogh) and pop-art — LoRA

- **Kontext-Style/Van_Gogh_lora** and **Kontext-Style/Pop_Art_lora** from the same
  Kontext-native pack. Van Gogh d. 1890 — in-bounds. Pop Art enters as a *movement*
  entry only (Warhol d. 1987 and Lichtenstein d. 1997 are inside the 70-year window,
  so no artist-name imitation or artist-branded remixing — movement-level lesson only,
  or hold for a PUBLIC-DOMAIN-POLICY.md (t-006) ruling if that feels too close).

## Needs Silas (login-walled / unverifiable — NOT treated as available)

**S-0 (policy, most important):** nearly all usable LoRAs carry the FLUX.1 [dev]
Non-Commercial License. Fine for t-004 evaluation; a decision is needed on whether
NC-licensed LoRA weights can run inside a monetized KR generation service (depends on
how the relay runs Kontext — hosted API with commercial base license vs self-hosted —
and on risk appetite for NC LoRA weights in production). Until decided, only the
Apache-2.0 watercolor LoRA is unambiguously production-safe.

All Civitai entries below are candidates only: the Civitai site/API was unreachable
from this session, per-model permissions (commercial use flags, "sell generated
images", download gating) could not be read, and Civitai downloads are frequently
login/API-key-gated at the creator's option. Silas (logged in) should check the
permissions box on each model page before any are promoted into the registry.

| # | Model | URL | Would upgrade |
|---|-------|-----|----------------|
| S-1 | Impressionism Flux Dev. LoRa | https://civitai.com/models/744438 | impressionism alternate |
| S-2 | Historic Ukiyo-e Style [Lora] Flux (Edo-period-trained) | https://civitai.com/models/933366 | ukiyo-e → lora |
| S-3 | Ukiyo-e Style by Hokusai [FLUX] | https://civitai.com/models/706042 | ukiyo-e → lora |
| S-4 | Ukiyo-e Japanese Woodblock (Tsukioka Yoshitoshi) | https://civitai.com/models/1054574 | ukiyo-e artist variant |
| S-5 | Renaissance Art Style - FLUX (trigger "Renaissance", 0.8–1.3) | https://civitai.com/models/672567 | renaissance alternate |
| S-6 | [Pinkie] Stained Glass Art [Flux] (67 positive reviews) | https://civitai.com/models/728275 | stained-glass → lora |
| S-7 | Pointillism Art Style - FLUX (Signac/van Rysselberghe-trained) | https://civitai.com/models/767804 | pointillism → lora |
| S-8 | Gothic Oil Painting Style - Flux | https://civitai.com/models/910493 | gothic → lora |
| S-9 | Mystic Sumi (sumi-e) | https://civitai.com/models/921689 | sumi-e Japanese variant |
| S-10 | Art Deco LoRA [FLUX+SD+XL+Pony] (trigger artdeco_v4) | https://civitai.com/models/516682 | art-deco → lora |
| S-11 | Expressionism / Painting style / Emotional expression | https://civitai.com/models/1190042 | expressionism alternate |

No paid-only LoRAs were encountered; the gate on everything above is Civitai login,
not payment.

## Ethical exclusions applied (do not revisit)

- "Flux Open Impressionism" (Civitai 723757) — trained on **Erin Hanson (living)**.
- Ghibli / Makoto Shinkai / Snoopy / JoJo / Irasutoya / American Cartoon / LEGO /
  Clay Toy entries in the Owen777 Kontext pack and InstantX LoRAs — living-artist
  styles or active brands/studios. The pack is used **only** for its historical-
  technique styles (Oil_Painting, Chinese_Ink, Van_Gogh, Pop_Art).
- Picasso (d. 1973) and Braque (d. 1963) artist-name LoRAs — inside the 70-year
  window; cubism ships as a movement-only prompt style.

## Research method note

Hugging Face and Civitai were not directly fetchable from this session (proxy policy
denial for both WebFetch and curl); everything above was assembled from web-search
snippets and cross-checked across multiple queries. Licenses marked "unverified"
should be read off the model card at download time (t-004 setup step). No weights
were downloaded.
