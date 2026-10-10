# Zuzu Gamebook: illustration bible and ArtJob queue contract

## This game is built around imagery
Illustrate *consequences*, not only locations. For a failed stealth test, show the shadow and a startled guard. For a costly victory, show a torn poncho, a bandaged wrist, dust over the water. A decision should feel like it cut to a new graphic-novel panel.

## Canon lock
Start at the shared Zuzu world registry ([worlds/zuzu](../../worlds/zuzu/README.md)), then read `CAST-PICKS.md`, `BOOK-ONE.md` and `VIDEO-GUARDRAILS.md` before new prompts. Use the comic series `zuzu-koala-assassin` house lane (Arthemy Western Art v3.0; its actual series settings). Reference the registry's **locked** ArtImages, not a generic new koala and not the historical R6 hero (241913): Zuzu front 242395, sister 242128, toddler 242144, coyote before the attack 242531, bandaged stump 242588, abbess front 242559 (the Kontext source for the crypt plate). Zuzu: rust-brown dusty poncho, wide kasa, dark brown cloth trousers, orange sash, katana rig across BACK, right-shoulder hilt; short koala proportions, quietly severe expression. Coyote: right eyepatch, gun on right hip and both hands before the watering-hole fight, bandaged right-hand stump afterward. Fennec siblings: sister taller than Zuzu, toddler smaller, tattered clothes and dignified depictions. Abbess: flat round sea-otter face. No overtly detailed injuries to the children, never sexualized.

**Reuse before rendering.** Search the registry's ledger inventory (`worlds/zuzu/assets/ledger-part-*.json`) and the vetted music-video keyframes first; 15 of the first 20 plates came from there. Plates ship as webp exports in kind_robots `public/zuzu-gamebook/scenes/` with ArtImage provenance in `utils/zuzuGamebook/art.ts` (the registry lists them in `assets/repository-media.json`), because a public reader cannot load private ArtImages. Every new round's ledger joins the registry inventory in the same PR.

Do not include the buried-twist vocabulary in prompt, caption, title, alt text or filenames; inherit `VIDEO-GUARDRAILS.md` bannedTerms verbatim. Avoid model-literal trap words documented there. Graphic-novel grim weird-west, windswept ruins, amber lantern lights, ink-rich shadows. Characters' clothes and anatomy must remain consistent. Respect commercial-use licensing for any future commercial release.

## Required imagery
| Plate | Aspect | Narrative reason |
| --- | --- | --- |
| Book cover | 3:2 | Pull readers into the story |
| Section environment | 16:9 | Where and when; Zuzu scale reference |
| Consequence variants | 16:9 | Visible success/failure state, wounds or gained ally |
| Confrontation / combat art | 3:2 | Foreshadow enemy intent, not generic battle |
| Portrait / character sheet | 3:4 | Locked hero, major allies and antagonists |
| Major ending plates | 4:5 or 16:9 | Emotional aftermath, unique to each ending |
| Inventory / power glyphs | 1:1 | Recognizable kit and skill aids |

First batch: cover and gamebook hero, watering-hole arrival, uneasy coyote standoff, crocodile eruption, wrist bandaging, Hollow Bell long street, siblings under boardwalk, apples on stone, mission arch, missing posters, abbess shadow, road with three silhouettes, and two distinct endings. Prioritize a beautiful playable opening and consistent identity over producing 100 mediocre images blindly.

## Prompt wording (Silas, 2026-10-10)
- **Lane: Arthemy house lane for every plate.** Silas, 2026-10-10: "why flux dev for those images? ... arthemy was the default for a reason." Round 8 tried Flux Kontext restages of the Zuzu front to stop costume fusion; they came back as human-fennec hybrids, extra koalas and over-bright flat colour, off the house look. Kontext stays a narrow tool for a single deliberate restage (the abbess crypt plate above), never a bulk lane for gamebook sections. Fix fusion inside the house lane: separate-character weights, fusion negatives, more seeds.
- **Describe the picture; never instruct the model.** Flux and Kontext read the T5 prompt as a description, so meta wording gets drawn: "place this exact koala into a new scene", "replace the white background" (black voids), "there is only one koala" (more koalas), "she never wears his hat" (his hat on her). A Kontext restage prompt is the scene, one sentence for each character's look, a light line, and "Western comic book illustration with clean ink lines, rich natural color and a fully drawn setting". No negations; those go in the negative prompt on lanes that have one.
- **Keep the grindhouse look but give each plate its own light.** The house prefix keeps gritty / dark atmosphere / grindhouse / high contrast / heavy shadows / weathered / grimy, but drops "muted earthy palette" and "desaturated", which flattened every plate to one brown-grey. Each scene instead gets a light-and-colour tag matched to its prose: moonlight, firelight, dawn, sunset, storm, desert sun, or window light.

- **Zuzu's tags come from the approved comic prompt, not a paraphrase.** Silas, 2026-10-10: "zuzu is appearing weirdly thin". The gamebook token had drifted to "(short), (stocky), slight paunch, conical straw kasa", which Arthemy draws slim. Use the ART-ROUND-10 build and costume (chubby, very short, stubby legs, small round belly, wide body, big round head, animal proportions, short arms; dark terracotta poncho, orange scarf and sash, dark brown cloth trousers, wide-brimmed woven straw hat, sheathed katana on back) toned to "a bit of a beer belly" (CAST-PICKS, A7), with thin / skinny / long torso / human proportions in the negative. Leave out "(koala:1.3)" in shared scenes; it invites a second koala.

- **One figure per plate until the character LoRAs exist.** Silas, 2026-10-10: "go ahead for workarounds. We can fix things later when we have the LoRAs built." The house lane fuses Zuzu with anyone who shares the frame, or leaks his costume onto them, so a section that pairs characters is drawn around one figure, a detail (a paw, an object, a shadow) or a place, and the text carries the rest. t-012 redraws them once comic-creator/t-016 delivers the LoRAs.

## Structured manifest
Each illustration record should carry: `key`, `sectionIds`, `shotType`, `aspect`, `alt`, `canonicalRefs`, `positivePrompt`, `negativePrompt`, `generationLane`, `model`, `seed`, `width`, `height`, `jobRequestId`, `artJobId`, `artImageId`, `source`, `license`, `deliveryUrl`, `verifiedAt`, `editorialVerdict`.
Never synthesize delivery URLs from guessed IDs. Use stable job request IDs per art key/version and prevent duplicate enqueues. Route through durable ArtJob; `DONE` isn't enough: verify image returned and loads. Reject broken anatomy, Zuzu-without-sword, wrong hat, sword-on-front in a back view, unfaithful character scale, generic anime/pixel-art drift, text gibberish. For narration, the gamebook *can* carry readable authored prose and interface words; the comic/film no-dialogue rule pertains to film output, while visual canon remains binding.

Agents have standing permission to submit **internal, task-scoped generation** without seeking a new signoff. They do not have permission to use paid services, publish promotional material or bypass other project gates.
