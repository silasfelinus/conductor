# Shifting Desks: Art Direction

The visual rules for every Shifting Desks card. The world is in [DESIGN-BRIEF.md](DESIGN-BRIEF.md) ("Decided world"); this sheet says how it looks. Round 1 (the two card backs and three style-test faces) is tracked in [art/ROUND-1.yaml](art/ROUND-1.yaml).

## The look in one line

**A mid-century corporate safety poster that has been hanging in a retro-futurist beige office for sixty years.** Cheerful mascot-poster composition up front, dread in the details.

- **Medium:** screen-printed gouache. Flat, confident shapes, crisp silhouettes, visible halftone grain and slight ink misregistration at the edges. It should look printed, not rendered.
- **World texture:** pneumatic tubes, endless cubicle horizons, silver ducts overhead, beige terminals with green phosphor glow, fluorescent tube banks, wood-paneled executive gloom the deeper you go.
- **Mood:** sunny company optimism with something wrong on the second look. Darkly comic, PG-13 (see the brief's tone guardrails). Deaths stay offscreen or slapstick.

## Tone ladder: the deeper you go, the more the building is alive

Silas, 2026-10-20 PT: *"In later levels, things might get more cronenbergian. I loved the giant cockroach appearance in the first act. Great tone."* Each floor keeps the poster look; what changes is how much of the office has quietly become a body.

| Floor | Register | What the art may show |
| --- | --- | --- |
| Orientation, Records & Forms | **One impossible thing, treated as normal.** The benchmark is Gus: a cockroach as tall as a man, in a cardigan and reading glasses, filing a grievance. | Ordinary offices. The strangeness is a single creature or object that everyone politely accepts. |
| Toy Division | **Toys a little too alive.** | Plush that seems to breathe, a bear with a warm heartbeat glow. Nothing organic on anything a child would hold, and no children (brief guardrail). |
| Wellness & Testing | **The body starts doing paperwork.** | Small, cheerful, clinical mutations on staff (an extra blinking eye, a third hand holding a pen, a phosphor glow under the skin); furniture and ducts with ribs, breath and cilia. |
| Sub-Level Zero | **Corporate biology.** The building is one organism and the Board is its face. | Walls veined with leather, cables like tendons, grilles that pucker like mouths, typewriters grown shells and feelers, eleven executives fused into one long suit. |

The flesh is always **smooth, glossy, upholstered and tidy**, like expensive furniture. That keeps it funny rather than gross, and keeps it in the register an 11- and 14-year-old would laugh at. Never show blood, wounds, open or exposed organs, gore, pain, nudity or anyone in distress. People react with office politeness: the horror is that nobody minds. Cronenberg is a register, not a source, so copy none of his creatures or props (Original designs only, below).

## Palette

Five inks plus paper. Each card leads with two of them; the rest appear only as accents.

| Ink | Role | Approx. hex |
| --- | --- | --- |
| **Manila** | the paper itself, folders, beige walls, skin of the office | `#E8D3A2` |
| **Carbon-paper blue** | linework, shadows, security stamps, uniforms | `#2B3F73` |
| **Safety orange** | warnings, hazards, the one thing you should look at | `#E8692A` |
| **Fluorescent-tube green** | phosphor screens, tube light, the vault, anything glowing | `#9BD88A` |
| **Oxblood** | executives, reviews, bosses, leather, wax, consequences | `#6E1F24` |

Deeper departments shift the lead pair: Orientation leans manila and blue, Records leans manila and oxblood, Toy Division leans orange and green, the Vault leans green, Sub-Level Zero leans oxblood.

## Card faces

- **Format:** 2:3 portrait (render at 832x1248, export `.webp`).
- **One readable scene per card.** One subject, one action, one strong silhouette that reads at thumbnail size.
- **The second-look gag:** every face hides one comic detail you notice later (a red stapler on a high shelf, an atomic swirl stitched on a plush paw, a colleague standing a little too far back).
- **Cast stays on model.** Recurring characters follow the `cast[].visual_description` in the encounter pack every time (Gus: seven-foot cockroach, glossy chestnut shell, mustard cardigan, half-moon glasses; Dale: mild mustache, short-sleeved shirt, clip-on tie, pocket protector). Background workers are a diverse mix of ages, bodies and presentations.
- **Composition:** subject in the upper two thirds; the lower third stays calm so the UI can overlay the card title and choices.

## Card backs

- **Encounter back:** a closed manila folder seen flat from above, a coffee ring near the corner, a round carbon-blue stamp impression (a plain double ring around a watchful eye) at the center, one brass paperclip on the top edge, a thin safety-orange tab. Symmetrical and calm.
- **Review / boss back:** a closed oxblood leather executive folder with brass corner caps and a glossy wax seal (a simple keyhole emblem) on a safety-orange ribbon. Ominous and dignified.
- Backs carry **no lettering**, no department names, no numbers. The UI says which department a card belongs to.

## Text lives in the UI, never in the art

Card titles, form numbers, signage, labels and badges are all UI. Renders are text-free so nothing comes back as garbled pseudo-letters. Where a scene needs a sign or a form, the prompt describes it as a plain shape or a solid color block.

## Prompt contract

Kind Robots rejects any prompt containing a negation, so prompts are **positive-only**: describe what is there, never what is absent. Exclusions go in `negative_prompt` only.

Every prompt follows this order: subject and action, then setting, then the second-look detail, then the lead colors, then the house style tail:

> mid-century corporate safety-manual illustration crossed with a retro-futurist beige office, screen-printed gouache with halftone grain, flat confident shapes and crisp silhouettes, limited palette of manila, carbon-paper blue, safety orange, fluorescent-tube green and oxblood, vertical 2:3 portrait composition, every surface bare and unmarked

The last words are always **"every surface bare and unmarked"**. Check a new prompt with `scripts/repair_negation_art_prompts.py` (its `violations()` must return nothing) before queueing it.

## Original designs only

Homage is welcome in the writing (see the brief's IP guardrails). The art copies nobody:

- No likeness of Vault Boy or any Vault-Tec mascot, poses or thumbs-up gag.
- No Aperture Science iconography, test-chamber panels, portal shapes or a GLaDOS-like ceiling AI.
- No Paranoia clearance-color uniforms or its computer's eye motif.
- No Brazil characters, costumes or the film's specific duct designs. Ducts are our own: silver, ribbed, friendly.
- No real company logos, products or living people.

PAL, our proctor, is a round cheerful speaker grille with a soft green glow, not an eye and not a face.

## Queueing and ledgers

- Art is queued as rows in `projects/art-prompts.yaml` under `requests:` (`source: shifting-desks`, `engine: krea2`, `variant: image`, `target_repo: silasfelinus/kind_robots`, `image_path: public/images/shifting-desks/...`). Keep `variant: image`: the `icon`/`card`/`hero` variants overwrite the Kind Robots project cover.
- Paths: backs at `public/images/shifting-desks/backs/<name>.webp`, faces at `public/images/shifting-desks/cards/<department>/<card-id>.webp`, served from `https://media.acrocatranch.com/images/shifting-desks/...`.
- Every subject goes in an `art/ROUND-N.yaml` ledger with its prompt, engine, size, seed, ArtJob id and ArtImage id.
- **Never mark art delivered before its URL loads** (`curl -s -o /dev/null -w '%{http_code}' <media_url>` returns 200). Only then set the card's `art.art_ref` in the encounter pack.
- Generated internal art is pre-approved (AGENTS.md "Generated art is pre-approved"). No paid third-party generation, nothing published.
