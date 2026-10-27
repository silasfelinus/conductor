# Space Couch: The Miniaturized Redshirt Expedition Corps

**Direction from Silas, October 27 2026 PT.** The Space Couch is literally a long red sofa protected by an invisible force bubble. Its miniaturization systems unfold a bizarre barracks behind its backrest, supporting at most twelve active expedition volunteers drawn from a **catalogue of 100 individually written alien characters**.

Game tone: cynical interstellar military sitcom; late-night philosophical absurdism; enormous adult speculative-comic set pieces; wild inventions and dangerous public institutions. Parody bureaucracy and command incompetence, not personhood or disabilities. Never lift recognizable plot beats or protected dialogue from named reference works. Write original cosmic farces that force unanticipated ethical consequences.

## Gameplay round

1. **Travel.** The captain and three chosen protagonists chart a destination on the Act I galaxy map. They unfold the miniature dorm, receive an arrival vignette and spend ship time reaching the world.
2. **Local and galactic assignment board.** Every arrival draws **one to four major encounters** and **three to five minor encounters** from authored local and galaxy-wide decks. Local world stories are guaranteed; roaming encounters can interrupt at any destination. A chapter-specific seeded draw is reload-safe.
3. **Staffing.** Captain plus three main crew can each take **one assignment across the board**. Unassigned major and minor tasks may be filled by redshirts. The player may directly choose any hired redshirt or auto-dispatch the next available volunteer. Resolve major crises before leaving; minor encounters are optional, often uniquely rewarding.
4. **Skill, surprises and consequences.** Officers who attend apparently trivial minor events can discover secret clauses, safe routes, undeclared machine minds, and other authored narrative flags. An unskilled redshirt dispatched to important diplomacy may damage trust and reputation and create a special disaster. Matching a redshirt's hidden skill with a task unveils the redshirt's secret ability and can recover an extra resource.
5. **Casualties and replacement.** **Each redshirt deployment uses an independent deterministic 1-in-3 fatality bucket**. Death is permanent for that unique identity, tracked in the memorial ledger with chapter and encounter. The fallen recruit cannot be hired again. Fatalities never apply to the four protagonists in this mechanic. Casualty notices should use the person’s name and history, avoiding generic faceless counters. Replacements cost one supply, with a free emergency accession if every redshirt has been lost and the player has no supplies.
6. **Quest follow-through.** After all major encounters resolve, return to the couch for the original primary mission, crew's personally authored three-world detour, romance, villain counterplay and earned finale. Existing save key `game-of-captains-voyage-v1` and six captain/twelve crew IDs do not change; new state keys are optional, old voyages remain valid.

## Production content audit

| Required | Authored source | Coverage status |
| --- | --- | --- |
| 100 unique redshirt names, bodies, backstories, secret abilities | `utils/gameOfCaptains/redshirts{A,B}.ts` | 100 authored records |
| Stats in rescue, science, diplomacy, tactics, luck and culture | `redshirts.ts` | Deterministic per-person ratings, one rated-five specialty |
| All in identical bright red expedition uniform | `redshirts.ts` `portraitPrompt` | 100 illustration briefs, **not completed paintings** |
| Destination-specific local major/minor encounters | `expeditionLocal.ts` | 36 authored cards, 4 per each of 9 Act I worlds |
| Galaxy-wide interrupt major/minor encounters | `expeditionGalactic.ts` | 17 authored cards, playable on any world |
| 1–4 major, 3–5 minor per world arrival | `expedition.ts` | Seeded and unique per chapter/world |
| Redshirt fatalities, hires, persistent casualties | `expedition.ts`, `rules.ts` | Core engine and old-save extension |
| Accessible encounter controls and command allocation | `pages/play/game-of-captains.vue` | In app PR; device screenshot QA not yet completed |

**Art pipeline production gate:** No artwork was generated or delivered by writing the roster. Create **100 actual portrait ArtJobs** representing exactly these bodies, all in bright red shirts with the same insignia, unique expression and pose. The original game expects actual artwork, not generic SVG placeholders. Produce or commission minimum 53 encounter opener plates, plus reversal/consequence variants for the most important major encounters, and verified background images for the miniature bunk-drawer. ArtJobs must be submitted through the authorized image queue with verifiable job IDs and returned URLs connected to the manifest. Until then count rendered art as missing. A simple 100-portrait +53-opener + 2-stage 1–4 major illustration scheme suggests **at least 153–250 additional art slots**, pending quality curation and reuse.

## QA gates

- Explicit roster count 100; no repeated IDs/names/anatomical designs/secret powers/backstories; all alien silhouettes identifiable even when shirt art is absent.
- Deterministic seeded galaxy boards across all 9 systems with 1–4 major plus 3–5 minor; no duplicates.
- Only one command member can lead each expedition task, and the same individual cannot be deployed twice in one shore visit.
- One in three redshirt deployments killed under a deterministic bucket; casualties remain unavailable after save/reload and cannot be re-hired.
- Redshirt mistakes on major diplomatic encounters have actual trust/reputation penalties. Crew specialists on minor missions earn actual secret flags. Matching secret powers have an observable mechanical benefit.
- Players can still finish a major board after severe losses via affordable recruitment and main-officer staffing, while preserving all old quest and romance arcs.
- Fully verify no scroll traps or unreadable text on phone/tablet/desktop. Complete original portrait and illustrated encounter art before final human design gate.

**Satirical staffing note:** Personnel says, “There are always more if you need them,” while simultaneously printing named memorial cards. The contradiction is part of the game's ethical commentary: a captain may learn to remember people that the institution considers disposable.
