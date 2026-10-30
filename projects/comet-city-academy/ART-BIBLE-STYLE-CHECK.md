# Shared Capes Art Bible · Style Check v1

**Direction:** Silas, October 29, 2026 PT. Mature Western animated superhero storytelling, clean ink, expressive faces, graphic silhouettes and hand-painted cel shadows. References for *qualities*, not prompts to copy: the acting and clarity of Legend of Korra, dramatic superhero impact of Invincible, and the color/costume confidence of She-Ra.

## Selected production model and original checkpoint benchmark

**Human selection, 2026-10-29 PT:** After evaluating art-model tests, Silas selected **Unstable Diffusers nihilmania** as the **preferred primary checkpoint for both Prom of Doom and Every Villain Tactics**. This is the default working visual direction for **new** character posters, villain art, henchman species, powered lieutenants, narrative expressions, character portraits, maps and 2:1 tactical standees. The other five benchmark checkpoints remain opt-in comparison/exception lanes, not co-equal defaults. Do not change old ArtJob checkpoint metadata or regenerate finished work without a specific continuity or quality reason.

**Generation recipe:** `SDXL/sdxlUnstableDiffusers_nihilmania.safetensors` through Comfy, scene-first SDXL prose, DPM++ 2M, 28 steps, CFG 7 as the existing tested starting profile. Preserve concrete character anatomy, signature costume shapes and silhouette, mature Western comic/animation linework, expressive faces and readable action at both illustrated-card and small tactical sizes. Adapt prompts by asset category; use consistent character-reference and seed/provenance tracking. A failed checkpoint load is a visible failure to fix, never permission to silently substitute another model.

The model choice is **not** a claim that all checkpoint test ArtJobs completed, that all Unstable images passed visual QA or that production art has been delivered. Keep actual ArtJob/ArtImage IDs, final media paths, continuity review and visual checks as separate requirements.

### Original 36 checkpoint-comparison ArtJobs

Source-of-truth request ledger: `art/CAPES-WESTERN-STYLE-CHECK-ROUND-1.yaml`. It is a **6 subjects × 6 checkpoint lanes** experiment with six fixed seeds, one per subject, the exact same spatial scene for each model, different prompt grammar tuned to the checkpoint. **Queue priority 900**, private ArtJobs via the dedicated main-only submission workflow; `auto_submit: false` avoids colliding with the general Art Generate sweep. The generic Flux, Flux2, Pony and furry-first engines are excluded. **Krea 2 is explicitly required** even though its Qwen lineage differs from SDXL/Illustrious. No other Flux model is used.

**Lanes**
1. **Krea 2:** concrete spatial scene prose, caption-friendly, no unexplained abstractions or metaphor-only art direction.
2. **Arthemy Western Art v3:** Illustrious tag prompt, `toon (style)` and `western comics (style)`, Euler ancestral 30 steps CFG5 (known author settings).
3. **Nova Comic XL v2:** Illustrious ink/cel tag prompt, Euler ancestral 28 CFG5.
4. **Illustrij v2.1:** Illustrious clean-line tag prompt, Euler ancestral 28 CFG5.
5. **DreamShaper XL Turbo:** concrete scene prose, distilled six steps CFG2 DPM++2M SDE. Do not give Turbo a conventional 30-step sampler.
6. **Unstable Diffusers nihilmania:** SDXL prose, 28 steps CFG7 DPM++2M.

The exact checkpoint paths come from the existing Kind Robots Playbook art lanes and the established Ecotone checkpoint bake-off. This is an experiment across verified configuration names, **not a live machine inventory assertion**. A failed model-load must remain FAILED, be investigated and explicitly revised; never silently route a cell to an unrelated checkpoint.

**The six exact concepts**
1. **Cornerstone** hero form, full-body poster in the college quad at the central fountain. Identity/costume/silhouette.
2. **Backdraft** villain form, full-body poster in a burning municipal insurance archive. Same-character good/evil visual discipline.
3. **Warren Wreckers** henchmen with Foreman Thumpkin, emerging beneath picnic tables. Test intentional rabbit-person design without biased furry style drift across *human* subjects.
4. **Mags Hardpan**, the independent stone-drummer lieutenant. Complex silhouette and readable effects.
5. **Human Dr. Frog scientist and teammate**, emotionally contrasted in a cramped science lab. Wide 16:9 narrative acting, no premature frog transformation.
6. **Firewall** hero model on a simple neutral backdrop. Full-body 2:1 standee layout with complete feet and strong readability under UI transforms.

**Scoring:** mature Western animation, facial acting, silhouette at tactical scale, cross-category consistency; 1–5 each, plus written notes. Judge six rows, not a single attractive poster. Unstable Diffusers is the preferred working model across poster, story and standee categories by Silas's decision. Split individual categories to another checkpoint only with a recorded comparison-based reason; do not treat automatically averaged ratings as a new editorial override. First-party `/admin/capes` style-check board is the review entrypoint; it shows only real ArtJobs and protected ArtImages, not simulated completions. Ratings are local browser drafts, not an automatically approved globally deployed style.

## One shared asset system for both games

Each of the **48 permanent power identities** needs a Hero Poster and Villain Poster (96), six emotion-aware large story illustrations (288 first-pass character reactions, with reusable same-design crops where possible), portrait-format variations, and separate 2:1 full-body transparent-ready tactical standees for both forms (96). Each of the **48 named henchman species** needs its own collectible poster (48), a group story image, named captain and generic troop portraits, and one generic tactical standee (48). Each **48 independent lieutenant** also needs a poster (48), story reactions, portrait, and a durable 2:1 standee (48). All 192 poster fronts share a **rendered stats-card reverse template**, not 192 newly painted backs.

Back faces are deterministic data driven from canonical name/codename, origin, affinity, role, unique powers, attack range, AP/movement, HP/armor, defenses, lore, weakness/counter and discovered secrets. **A poster is unlocked as a playable collectible card in either game**, with persistent earned provenance. An image being queued is not an unlock or owned card.

**Tactical animation v1:** no frame-by-frame animation debt. Idle bob, selected bounce, hit shake/flash, critical recoil, defense crouch/overlay, movement lean, buff glow, knockout rotate sideways and subdued desaturation. Respect reduced-motion preferences; keep true positions and hit results in the combat engine, animation is visual-only.

**Stable naming:** `identities/<signature>/poster-hero`, `poster-villain`, `story-<emotion>`, `portrait-<emotion>`, `model-hero-2x1`, `model-villain-2x1`; `henchmen/<signature>/poster`, `captain-portrait`, `model-2x1`; `lieutenants/<signature>/poster`, `portrait`, `model-2x1`. Use existing ArtImage and ArtJob provenance, not new generic URL placeholders.

**Rollout:** With the preferred checkpoint now selected, inspect the real eight-subject benchmark output and verify asset-specific continuity before bulk production. Then fully produce 3 linked character families (Cornerstone, Backdraft, Firewall) through card front/back, emotional story art, UI portraits and tactical standees, preserving physical identity across outputs. Complete 48 permanent hero/villain forms before mass-producing supporting cast. Include negative-story, hit, knockout and unlock cards in adversarial device tests. Review the actual rendered screenshots at phone/tablet/desktop/XL.

## Evidence boundaries

- **Written prompt:** exists only in the ledger.
- **Accepted ArtJob:** requires a numeric `subjects[].jobs[lane-key]` returned by `/api/art/enqueue`.
- **Rendered:** completed job with valid ArtImage ID.
- **Delivered:** final accessible image path, intended game surface linked, visual QA passed.
- **Chosen house model:** Silas selected Unstable Diffusers on 2026-10-29 PT. This satisfies checkpoint preference selection only; asset quality, delivered-art coverage, accessibility and final game acceptance remain separate checks.

The dedicated Capes submission workflow runs the approved ledger on reviewed `main` with the connected production secret. The tool that submits records accepted IDs in-place and deduplicates further runs. A PR containing YAML **is not** proof of ArtJobs, and a green CI run is not a self-hosted deployment.
