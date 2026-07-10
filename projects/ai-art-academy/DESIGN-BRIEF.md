# AI Art Academy — Design Brief

date: 2026-07-10
status: active (autonomous project initiative — test run #1)
author: Claude (Silas-directed session)

## What it is

AI Art Academy teaches people about the history of art: movements, styles, techniques,
and the (dead, public-domain) artists who created them. It is a learning surface first
and a creation surface second — the payoff loop is *learn about a style → see real
public-domain examples → remix your own image in that style*.

The user either picks a **starter image** from a curated public-domain library or
**uploads their own**, then uses the Kind Robots Kontext network to remix it in the
style they just learned about. The existing `components/art/art-styler.vue` is the
seed of the front end: it already does upload/gallery source selection, LoRA-backed
style entries, Kontext generation via `artStore.generateArt({ engine: 'kontext' })`,
and resource-DB LoRA hydration. Art Academy wraps that machinery in a curriculum;
the plain style-transfer tool remains available inside the Academy as its "Style Lab."

Adjacent project: **sketchy** teaches people *how to draw* (assignments + AI critique).
Art Academy teaches people *about art*. They share the KR token economy and art
backend but stay separate projects. Cross-links between them are welcome
("you just learned about gesture in Impressionism — try a Sketchy assignment").

## Ethical boundary (hard, non-negotiable)

- The curriculum covers **only public-domain art and artists who are no longer
  living** — historical movements, styles, and creators whose work is free to
  study and remix. We do not teach, imitate-by-name, or monetize the signature
  styles of living or recently deceased working artists.
- Style entries in the Academy registry must reference either an art **movement**
  (Impressionism, Ukiyo-e, Art Nouveau, Bauhaus…) or a **dead artist** whose work
  is in the public domain (see PUBLIC-DOMAIN-POLICY.md, task t-006).
- Example imagery comes from open-access collections: Met Open Access (CC0),
  Art Institute of Chicago (CC0), National Gallery of Art open access,
  Rijksmuseum, Smithsonian Open Access, Wikimedia Commons PD scans.
- Note for t-008: some existing art-styler entries reference living creators or
  active brands (e.g. "Disney", "Gorillaz", "DB4RZ"). Those may remain in the
  generic Style Lab tool as-is (Silas's existing call), but they are **excluded
  from the Academy curriculum registry** — the Academy never presents them as
  history lessons or attaches creator biographies to them.

## Model strategy: Kontext-first, LoRA-assisted (answers Silas's question)

Silas asked whether Kontext is the right engine given LoRA availability vs model
knowledge. Recommendation: **keep Kontext primary**, for three reasons:

1. **Dead famous artists are the best case for base-model knowledge.** Van Gogh,
   Monet, Hokusai, Mucha, Klimt, Vermeer and the canonical movements are heavily
   represented in FLUX/Kontext training data. Prompt-only instructions
   ("Repaint this image as an ukiyo-e woodblock print in the style of Hokusai,
   flat color planes, visible woodgrain texture") work today with zero LoRAs.
   The obscure-style gap LoRAs usually fill barely applies to a curriculum built
   on the most famous styles in history.
2. **It's already wired.** art-styler.vue, the resource store's LORA/KONTEXT
   entries, and the relay pipeline all speak Kontext now. Switching engines
   costs integration work with no proven quality win.
3. **Kontext is an *editing* model** — it preserves the user's composition while
   restyling, which is exactly the "remix YOUR image in this style" promise.
   Plain SD/SDXL img2img drifts from the source much more.

So each Academy style entry carries a `mode`: `prompt` (model knowledge only),
`lora` (curated public LoRA + trigger), or `hybrid` (both). Task t-003 hunts
openly licensed Kontext/FLUX style LoRAs; task t-004 runs an A/B evaluation per
style and records which mode wins. **Fallback documented, not built:** SDXL
img2img + IP-Adapter has the largest style-LoRA ecosystem if Kontext proves weak
for specific movements — t-004 should note any styles that would justify it, but
we don't add a second engine until the evaluation demands it.

## Product shape (v1)

1. **Timeline / movements browser** — art history as an explorable timeline:
   movement → era, key ideas, 3–6 public-domain example works, notable (dead)
   artists with short bios.
2. **Style pages** — one per movement/artist style: what defines it, how to
   recognize it, example gallery, and a "Remix in this style" call-to-action.
3. **Remix studio** — starter image picker (curated public-domain works +
   KR gallery + upload), style applied via Kontext, result saved to the user's
   gallery with style + lesson metadata. This is art-styler.vue, extended.
4. **Style Lab** — the existing free-form art-styler experience, kept as a tool
   inside the Academy for users who just want to play.
5. **Progress hooks (later)** — lessons completed, styles tried, KR milestone
   integration.

Token economy: same pattern as sketchy — align with the Kind Robots mana/token
economy, free tier with limited remixes, no separate economy (spec task t-009's
economy section; hard-gate anything that touches billing).

## Data / content model (app-owned, shared backend read-only)

- `academy-styles` registry (JSON/seed first, DB later if warranted): slug, name,
  movement/artist, era, description, recognition cues, example image refs
  (source museum + license), remix config (mode, loraPath, triggerPhrase, weight,
  prompt template).
- Curriculum outline lives in this project's `docs/` until the front end needs
  seeds, then ships as kind_robots seed data. Backend schema changes = pitches,
  never direct edits (BOUNDARY.md rule).

## Autonomy contract (test run of the autonomous project initiative)

Silas granted full reign over this project and art-styler.vue. Operating rules:

- Keep the project moving every cycle without waiting for input. Escalate only
  **actual human gates**: spend, publishing/outward-facing steps, licensing
  doubts a policy doc can't resolve, backend schema needs.
- Generated art is pre-approved (AGENTS.md 2026-07-06 rule) — icons, heroes,
  inspirations, starter-library candidates, style preview thumbnails.
- When no ready task exists, the never-idle rule applies (AGENTS.md
  "Autonomous projects"): style pass, roadmap upgrade, more inspirations,
  curriculum expansion.
- Silas checks in occasionally; scope confirmations run as **soft** gates in
  parallel with development, never parked.
