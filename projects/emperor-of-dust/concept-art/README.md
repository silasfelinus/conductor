# Emperor of Dust · cartographic and room composition studies

These **concept vectors** follow [MAP-LAYOUT.md](../MAP-LAYOUT.md) and the governing [SYSTEMS-V03.md](../SYSTEMS-V03.md). Created for Silas's 2026-10-18 PT request for two maps and one example of each primary game screen. **Not approved final painted art, not ArtJobs, and not a public game release.**

## Assets

- `wasteland-base.svg` is the **unlabelled** art under a future UI map layer; `wasteland-labelled.svg` is an annotated Day 1 geography reference. Position: Fortress (C2), Mirefen (B-D1), Black Stones (B2), Abbey (D1), Hollow Bell (E2), Black Verge (E1-E3), Saltroad (row 3), Eastern Ford (D3), Thistledown (D4), Badlands and Mole tunnels (B4-5), Jackalwire canyon (C5), Sunken Rail Yards (D4-E5).
- `wasteland-day41-overlay.svg` is a **transparent overlay** sketch for the Act V fracture and war-front beat, not a baked map texture.
- `fortress-cutaway-base.svg` is the unlabelled architectural art; `fortress-cutaway-labelled.svg` is the labelled reference. Five playable rooms: throne, quests, barracks, market, map. Supporting spaces: archive, yard, Komodo's study, gatehouse.
- `screen-throne.svg`, `screen-quests.svg`, `screen-barracks.svg`, `screen-market.svg`, `screen-map.svg`, `screen-chronicle.svg` are six **UI/art composition mockups**. They are not screenshots of the implemented game.

All are editable standalone SVGs. UI text and sample values are illustrative, not rules/data migrations. Their anthropomorphic shapes are intentionally anonymous silhouette placeholders; use the separately approved Zuzu cast artwork for named characters in actual implementation.

## Implementation handoff

1. Base maps must be kept free of world labels, fog, borders, faction crests, markers, and quest status. Layer all of those separately for Days 1/11/21/31/41 and localize/announce the labels in the UI.
2. Keep the **five-room, single-viewport** structure on desktop, tablet, and phone. On mobile, fit the stage and move support/choices into a bounded drawer; avoid page scrolling.
3. Depict Hollow Bell **inhabited and structurally intact** in this pre-Zuzu era. The aqueduct must be visibly repairable. Never bake the Abbey Day 40 fracture into the base.
4. The throne room houses audiences and Young Komodo's adjacent study; the quest room's dispatch balcony is the day/night transition; barracks has 6 initial beds with 9/12 expansions and infirmary; market sells equipment/healing for brass; map room displays factions/taxes/tensions. Chronicle includes save/load/rewind.
5. Once Silas chooses the visual direction, promote the selected designs to production rendering via durable Kind Robots ArtJobs. Do not call a queued job delivered, and do not publish this private game's art/screens without the separate release gate.

**Colour/art lane:** ash slate, brass, kiln ochre, salvaged cedar, salt parchment, oxidized green. The mockups explore hierarchy and scale; final paintings should keep hand-inked textures and original architecture without copying the Sovereign Tower reference.
