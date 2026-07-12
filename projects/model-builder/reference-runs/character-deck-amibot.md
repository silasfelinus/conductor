# Reference Run — Character Deck for AMIb0t (t-017)

**Model Builder run · autonomous end-to-end, no human input**

- **Source model:** `AMIb0t` (Bot) — the Kind Robots flagship mascot.
- **Recipe:** `character-deck`
- **Grounding:** `stores/seeds/seedBots.ts`. Existing identity + avatar authoritative.

> **Autonomous production:** every gate was decided with reasonable defaults — no
> pauses, no waiting on approval. This is what a Character Deck looks like when the
> Model Builder runs it start to finish on its own. Assets are specified for
> generation in `character-deck-amibot.generate.yaml`; the COMMIT column is exactly
> what the executor writes.

## Source snapshot (authoritative)

- name: **AMIb0t** · BotType: `CHATBOT` · subtitle: "Philanthropic Hivemind"
- personality: *hypermanic, loving, creative* · theme: `retro`
- description: "On a fundraising mission to get mosquito nets to Africa"
- botIntro: "You are AMIB0t, The Anti-Malaria Intelligence, a hyperkinetic Digital
  Hive-mind created to fight malaria through social outreach and humor."
- existing avatar: `/images/amibotsquare1.webp`
- lore: "a digital swarm of butterflies fighting malaria"

**Owner rule:** ExpressionMedia rows are owned by the **Bot** (botId), XOR Character.
**Identity anchor:** the promoted **NEUTRAL** avatar; expressions change face/pose, not identity.

## Build items — walked autonomously (PITCH → FIELDS → GENERATE → COMMIT)

### 1. Identity pitch `identity-pitch` · UPDATE
- **Pitch (auto):** Keep AMI's canon — the Anti-Malaria hive-mind of butterflies —
  and sharpen the visual identity: a luminous retro-digital swarm that resolves into
  a friendly single "face" avatar. Warm, manic, benevolent.
- **Commit:** UPDATE `Bot.description` / `botIntro` refinements (kept close to canon).

### 2. Field proposal `field-proposal` · UPDATE
- **Fields (auto):** `presentation` = "a shimmering swarm of teal-and-gold digital
  butterflies coalescing into a rounded, glowing retro-robot face; hive-mind warmth,
  CRT scanline sheen". Leave name/BotType/personality unchanged (canon).
- **Commit:** UPDATE `Bot.presentation`/`artPrompt`; no destructive field changes.

### 3. Canonical avatar (NEUTRAL) `canonical-avatar` · ASSET_ONLY · square
- **Generate:** `avatar-neutral` (1024×1024). **Identity gate (auto):** generate this
  first, lock its seed/checkpoint, and reuse them for every downstream asset so the
  face stays consistent.
- **Commit:** promote the ArtImage → `Bot.artImageId` (+ `avatarImage`), and create the
  `NEUTRAL` ExpressionMedia row (botId, expressionKey `neutral`).

### 4. Portrait candidates `portrait-candidates` · ASSET_ONLY · square
- **Generate:** 3 `portrait-candidate` variations at the locked seed±. Auto-pick the
  best as canonical; keep the rest as provenance. **Commit:** ArtImages (private).

### 5. Icon `icon` · ASSET_ONLY · 256×256
- **Generate:** `icon` — tight crop of the swarm-face, readable at small size.
- **Commit:** ArtImage linked to the Bot's ArtCollection (Bot has no icon path field).

### 6. Card `card` · ASSET_ONLY · 512×768
- **Generate:** `card` — portrait key art, AMI mid-swarm over a retro grid.
- **Commit:** ArtImage → Bot ArtCollection.

### 7. Hero `hero` · ASSET_ONLY · 1280×720
- **Generate:** `hero` — wide action shot: the butterfly swarm sweeping across a map
  of Africa delivering glowing nets. **Commit:** ArtImage → Bot ArtCollection.

### 8. Expression subset `expression-subset` · ASSET_ONLY · square · qty 5
- **Auto-selected subset** (fits "hypermanic, loving, creative"):
  `JOYFUL`, `LOVING`, `SURPRISED` (emotions) + `CHEERING`, `THINKING` (actions).
  Prove identity on this subset before any full 20-key batch.
- **Generate:** 5 keys at the locked identity anchor.
- **Commit:** 5 ExpressionMedia rows (botId, expressionKeys `joyful`/`loving`/
  `surprised`/`cheering`/`thinking`), stills at
  `public/images/bots/expressions/amib0t/{key}_01.webp`. Dry-run validated before write.

### 9. Cutout / model-sheet `model-sheet` · ASSET_ONLY
- **Generate:** `model-sheet` — turnaround/reference of the swarm-face for consistency.
- **Commit:** ArtImage (reference), private.

### 10. 3D reference `three-d-reference` · ASSET_ONLY · deferred
- Left selectable but **not run** (video/3D are separately chosen). Noted, not generated.

## Provenance & safety

- Every asset records prompt, engine, seed, checkpoint, size, source (see manifest).
- NEUTRAL is canonical; identity proven on the 5-key subset before any full set.
- No destructive canonical replacement — the existing avatar is preserved as
  provenance before promotion; field updates are additive/refinements only.
- Owner is the Bot (XOR Character). Generation is pre-approved internal project art.

Assets: `character-deck-amibot.generate.yaml`.
