# Inspiration: PortOS comic services and other comic makers

date: 2026-10-03
PortOS reference checkout: atomantic/PortOS at 0fc48e9 (silasfelinus/PortOS is synced to the same commit).
We are learning from it, not integrating it.

## What PortOS does

- **Create Suite:** Story Builder → Writers Room → Universe Builder canon → Series Pipeline.
- **Series Pipeline:** per-issue stages (script → storyboard → comic pages or video), covers, back covers and volume covers, plus PDF export (`server/services/pipeline/comicPdf.js`).
- **Comic pages:** each page is rendered as a single image. The model draws the panel borders and letters the balloons from one structured prompt.
- **Support tools:** LoRA training, Mood Boards, Annotate (sketch over a still) and Sprites (8-direction turnarounds).

## Lessons worth borrowing, ranked

1. **Script as source of truth.** A plain Marvel/DC full script (`## Page N`, `Panel N`, Description / Caption / Dialogue / SFX) parsed deterministically into `{coverConcept, pages:[{panels}]}`. See `server/lib/comicScriptParser.js`. Our v0 script already uses this shape; the studio import can parse it.
2. **Descriptors injected by name.** When a character, place or prop name appears in panel text, its canon description is added as "Featuring — Name: description", instead of being hand-copied into every prompt. See `composeComicPagePrompt` in `server/services/pipeline/comicPages.js`, `server/lib/scenePrompt.js` and `server/lib/canonPrompt.js`.
3. **Approval locks.** An approved stage or variant is frozen against regeneration (`assertStageUnlocked`, lockable canon fields). Studio equivalent: a `selected` verdict protects the final.
4. **Proof then final, with scene chaining.** A cheap proof render comes first; the final render uses the proof as its base so the layout survives. Within a scene the prior page is chained in as a reference (`resolveComicPageReference`, `resolveAutoReferenceIndex`).
5. **Dense character reference sheets.** Four views at consistent scale with a height chart, an expression progression, micro-expressions, head angles, and palette, wardrobe and props. See `server/services/universeCharacterSheet.js`.
6. **Character LoRA path.** Build a dataset from a views × poses × expressions matrix plus reference-sheet slices, caption it with a vision model, give it a trigger word, and auto-apply the LoRA when the character appears. See `docs/plans/2026-06-12-character-lora-training.md`. This is our route to a Zuzu LoRA after the 8-angle Kontext set.
7. **Information-economy checks.** Info-dumping, premature reveal, reveal-gated canon, and Chekhov setup and payoff (`server/lib/editorial/checkInfra/revealForeshadowing.js`). These fit Silas's "no exposition, drip-feed" rule and the buried human twist. The studio's notes carry a "secret until" marker.
8. **Several candidate prompts per panel**, not one (`generateComicPanelImagePrompts`).
9. **Serialized writes** to shared records (`issueWriteTail` in `server/services/pipeline/issues.js`). The studio uses a versioned layout document for the same reason.
10. **Balloon hygiene when the model letters.** Speaker names never go inside a balloon, and parentheticals become style hints (`formatBalloon`).

## Where we deliberately differ

PortOS letters whole pages inside the image. We compose panels in the studio and keep lettering as data. That gives Silas the freedom to rearrange, and lettering stays editable.

## Other comic makers

| Tool | Worth noting |
|---|---|
| comic-alpha (MIT) | JSON script → live sketch-layout preview used as the layout reference for generation; prior pages and pasted images as consistency references |
| Dashtoon | Trains a per-character model for consistency; script-to-comic; inpaint and eraser fixes per panel |
| Anifusion | Template layouts plus character locking |
| LlamaGen / AI Comic Factory | Free, automatic layouts; weaker consistency |
| Kumanga | Local-first, non-destructive editor with reusable characters |
| PortOS | Full pipeline, above |
