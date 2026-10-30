# Capes / Prom of Doom shared Western-art gate: Map + Portrait Coverage

**2026-10-29 PT, Silas-directed.** Keep the original six-by-six checkpoint comparison unchanged and add two production-critical subjects at the *same* six checkpoint settings. The combined **8×6 = 48 independent cells** cover the requested six essential kinds of images: hero poster, villain poster, henchman poster, large story illustration, geographic map and character portrait. The original batch also includes a lieutenant poster and a 2:1 tactical standee. These are **design samples**, not 48 production-ready identity images.

## Why the two new controlled scenes matter

**Campus and Comet City navigable map (1344×768):** The main plaza's giant circular fountain must be centered; the library is north, dormitory west, science laboratory east, picnic square south; the downtown road connects at the northwest and the field is southeast. The composition needs readable actual roads, cardinal relationships, distinct walkable terrain and large architectural features. No model may quietly substitute a labeled infographic or nonsensical disconnected road network. Compare models on spatial consistency, environment identity, linework clarity and coherent game-map usefulness. Draw **no text**; map labels belong in the UI.

**Firewall emotional mission portrait (896×1152):** Priya is a recognizably human South Asian adult in a blue/copper suit and braided bun. She reacts with restrained alarm and resolve to a threat, not an anonymous smiling model. Compare hairline/face completeness, eye direction, brows, character fidelity to the existing full-body standee, 32-pixel readability and clean backgrounds. No fur, animal ears, pinup posing or enormous anime eyes. Draw **no text**.

Both have exact matching concepts across six routes: Krea 2 prose, Arthemy Western v3 tagged, Nova Comic XL tagged, Illustrij tagged, DreamShaper XL Turbo prose, Unstable Diffusers SDXL prose. **No generic Flux, Flux2, Pony or furry-first checkpoint.** Model-specific sampler, CFG, steps, prompt grammar and negative prompts are copied from the six-cell original lane definitions. Both new subjects have deterministic, different fixed seeds (629107, 629108); job IDs, asset keys and accepted render provenance are distinct from the original 36.

### Production evidence and safeguards

- Original first 36 requests: `art/CAPES-WESTERN-STYLE-CHECK-ROUND-1.yaml`, owned by independently claimed high-priority t-028. Never reset, requeue or overclaim its individual accepted jobs.
- Companion 12 requests: `art/CAPES-WESTERN-STYLE-CHECK-MAP-PORTRAIT.yaml` (t-029). Project slug `comet-city-academy`, private, 900 priority, durable per-cell numeric ArtJob references.
- Both use the existing `scripts/enqueue_art_requests.py` via `POST /api/art/enqueue`, which handles checkpoint-specific workflows and records actual accepted IDs. A new main-only, idempotent follow-on workflow submits *only* the two new subjects. No public or release changes.
- **Authored:** 2 prompt briefs exist. **Queued:** count only cells with returned positive ArtJob IDs. **Rendered:** inspect DONE and actual ArtImage paths. **Game-ready:** separately attach delivered images to the appropriate game surfaces and pass visual/character consistency review.
- The private `/admin/capes` checkpoint comparison page owned by t-028 should consume both ledgers by their stable subject keys, display map and portrait as extra side-by-side rows and never fabricate image URLs or completed status. A high-scoring model on posters can still fail on maps or facial acting. Editorial selection is a human gate.

## Comic-character first-appearance panels are a shared asset family

**192 canonical role-based reveals**: 48 heroes, 48 villain forms, 48 one-hit henchman crews and 48 powered lieutenants. Keep intro clean-art compositions consistent with approved card posters, with enough clear negative space for a large overlaid name. The **stylized character name, role label, caption, comic issue tag and accessible text are native game UI**, never letters generated within the artwork. The reusable interface animation relies on slides, impact scale, halftone and aura, and respects `prefers-reduced-motion`. Its image slots and key hierarchy must be shared by Prom of Doom and Every Villain Tactics.

Character introductions are earned, replayable and later become scrapbook card-front unlocks (a different persistent state from simply seeing an intro). **An intro animation rendered using a placeholder or missing art is not a finished art asset**. Game content metadata and visual assets should remain separate until accepted into the central ArtImage manifest.
