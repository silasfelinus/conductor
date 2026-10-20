# Emperor of Dust — front end vs. the painted drafts

2026-10-19 PT. Silas asked to work on "the discrepancy between our current front end and the
idealized drafts". The drafts are `art/concepts/painted-screens.webp` (six rooms),
`painted-fortress-cutaway.webp` and the canon map `painted-wasteland-canon.webp`. The
baseline was `/play/emperor-of-dust` after t-020: correct systems, but on the light Storybook
surface with text-first panels and no room art.

Task: t-029. Ledger for room art: `art/ROOMS-ROUND-1.yaml`.

## The gaps, by layer

| Layer | Draft | Shipped before t-029 | Status |
| --- | --- | --- | --- |
| Palette | Night-ink panels, tarnished gilt double edges, parchment text, crimson banners | Light paper theme, orange buttons | **Done** in kind_robots#3873: scoped `emperor` daisyUI theme |
| Type | Cinzel-style caps for titles, italic serif copy | Body serif only | **Done** (#3873): Cinzel on titles and room headings |
| HUD | Crest, "EMPEROR OF DUST / ACT II · DAY 17 / 50", meter chips with icon and bar, brass coin pill | Plain number boxes | **Done** (#3873) |
| Room frame | Medallion, title plate, italic tagline over a painted scene | Plain heading in a card | **Done** (#3873). The painted scenes are queued (ArtJobs 40949–40960); a gradient shows until they're exported |
| Throne | Petitioner in the hall, petition card with portrait, quote and choice rows | Briefing took half the screen; NPC art in a box inside the dialogue | **Done** (#3873): scene + petition card; briefing folds out |
| Quest room | Parchment notices on a board, party slots with portraits and "+", odds and injury risk, SEND | Text list and form grid | Next |
| Barracks | Roster with portraits and pips, follower card with quote, health and anxiety pips, trait chips, equipment slots, TALK | Avatar grid and a stats panel | Next |
| Market | Tabs (Buy / Sell / Equipment / Treatments / All), rows with item art and brass price pill | Card grid with text buttons | Next |
| Map room | Painted map with pins, faction banner crests with stance, legend, TRAVEL | Painted map with pins already; region list and support bars | Next: crests, legend |
| Chronicle | Dawn rows with icons and thumbnails, parchment rewind card | Save slots and day buttons | Next |
| Fortress overview | Painted cutaway with labelled rooms | None | Idea: a cutaway room picker |

## Art the drafts need that doesn't exist yet

- Six room backdrops (`public/emperor-of-dust/rooms/<room>.webp`). Queued, `ROOMS-ROUND-1.yaml`.
- Item icons for the market and equipment slots. Not queued.
- Quest notice vignettes (one per quest family). Not queued.
- Faction crests for the map room. Not queued; can start as live CSS/SVG banners.

## Rules kept

- No baked text in generated art. Names, numbers and labels stay live HTML (concept README).
  The exception is Silas's own canon map, which ships as he drew it.
- Viewport-first (kind_robots AGENTS.md): one screen per room, inner `.kr-scroll`, checked at
  390 / 768 / 1440.
- Public Play launch is still t-010's human gate. This work changes the look, not the release.
