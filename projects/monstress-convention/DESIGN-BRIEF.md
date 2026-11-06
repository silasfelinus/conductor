# Monstress Convention — Design Brief
_Date: 2026-11-05 PT · Status: active production brief · Conductor slug: `monstress-convention`_

## 1. High concept
**Tagline:** Everybody's a monster. Somebody's a murderer.

The Grand Gloaming Hotel is a slightly disintegrating two-storey roadside establishment hosting MONSTRESS-CON, the annual reunion of the cast of a cult monster-media franchise, *The Monstress Cinematic Menagerie*. Everyone is performing for fans, negotiating scandalous licensing deals, and hiding something. Our journalist has one last chance to save a nearly dead paranormal-culture blog. During the convention, a beloved cast member is murdered. Soon she returns as a ghost, unhelpfully unable to identify her killer. An unlikely two-person investigative team must investigate everybody, expose a lucrative franchise cover-up, and decide what truth is worth publishing.

**Dramatic question:** Can two struggling outsiders solve a locked-hotel murder without exploiting the very people whose stories pay their rent?

**Tone:** A knowingly ridiculous sexy-adjacent adult comedy with genuine detective stakes; affectionate point-and-click lampoon, monster-film sendup, tabloid satire and pulp noir. Homage to the *genre* of Leisure Suit Larry, Monkey Island, Thimbleweed Park, Tex Murphy and monster-girl comedies, with original characters, dialogue, puzzles and visual identities. No borrowed character designs, franchise names or plots. Erotic innuendo and optional cheeky cheesecake, not compulsory sexual access as a puzzle prize. All cast and potential romantic partners are adults.

## 2. Scope and framework
- **Framework:** Adopt Playbook Kit's settings, saves, cinematic moments, cast/secrets/endings panes when they fit. **Do not replace point-and-click exploration with a choice-card playbook.** Own a real 2D scene graph, walkable hotspots, inventory, verb wheel and topic interrogation system.
- **Prototype tier:** **Vignette**, 25–45 min, hotel lobby/registration/hot tub/one upstairs room, two playable investigators, the murder and the first ghost interview. Kit cap exceptions require a written allowance. The full game is an intended Standard/Saga expansion, gated by successful prototype playtests, not a promise that the prototype is the whole request.
- **Full target:** Three acts, 18–24 authored locations, 35–50 multi-verb hotspots, 20–30 item/puzzle dependencies, 10–12 major NPCs, several interviews per suspect and 4–6 substantially distinct endings. Exact counts must be audited for puzzle purpose and playing time before tier escalation. Prefer 5–8 hours of dense play to artificial filler.
- **Navigation:** /admin/monstress-convention is an internal preview only. A public /play route, homepage Highlight and nav entry require a separate human publication gate. **Not a family-friendly default.**

## 3. Player characters and dynamic dialogue
**Nico Vale**, adult, scruffy investigative blogger of *Last Call Cryptid*. Resourceful, charming at inconvenient moments, broke, overconfident, desperate for a scoop. Good at bluffing, improvisation, fan culture, shady trades and noticing physical evidence; prone to leaping to the wrong conclusion.

**Iris Quill**, adult, attractive, sardonic assistant/photojournalist and the superior investigator. Knows contracts, continuity, forensic photography and interpersonal cues. Sharp, independently motivated, and credited as a co-author, never reduced to decorative helper. Her conflict with Nico over what may ethically be published is a central choice.

The player freely switches between **Nico** and **Iris** except at motivated temporary separations. Each has unique examination lines, NPC attitudes, dialogue approaches, and in some cases alternate puzzle routes. They exchange evidence, but cannot both be in every place simultaneously. Their personal inventory may include held tools, while a **shared case file** stores learned subjects/evidence to avoid tedious item shuffling.

**Conversation topics:** persistent structured `Topic` graph, unlocked by observed clues, rumors, contradictions, timeline events and conversations. Both protagonists share topics; every `(speaker,target,topic,state)` can have a distinct line, response, reveal and next topic. New information is highlighted. Once a topic is exhausted for one protagonist it can remain fresh for the other. Support `Ask about…`, `Confront with evidence…`, `Compare accounts…`, a replayable transcript and a non-spoiler journal.

## 4. Franchise stars and other hotel residents
The monster women are performers with careers, rivalries and private interests, not monster specimens or interchangeable erotic rewards.

| Character | Star persona | Private stake / playable interview difference |
| --- | --- | --- |
| **Countess Vespera Nocturne** | Glamorous female Dracula | Controls her image, buried royalties dispute; Nico gets bravado, Iris gets contract facts |
| **Francesca Stein** | Larger-than-life stitched-together star and inventor | Wants credit for unlicensed science props and the creative work behind them |
| **Roxie Lupin** | Fierce werewolf star | Publicly temperamental, privately protecting a vulnerable castmate |
| **Moxie Mire** | Mutable slime/blob diva | Remembers hotel plumbing routes and can witness through vents |
| **Marina Brine** | Lagoon creature star | Has secrets concerning the hot tub/filtration system and her own image rights |
| **Dr. Vespa Vane** | Oversized fly-headed scientific-horror performer | Hears and smells things others overlook; humorous but incisive, never merely a gross-out joke |
| **Celestine Veil** | Elegantly theatrical ghostly/mummy franchise icon | Murder victim, later an actual ghost; retains emotions, fragments of sensory detail, and agency without knowing who struck her |
| **Odette Harker** | Human franchise licensing executive | Commercially ruthless, always physically plausible in the scene; privately stands to gain from silencing Celestine |
| **Gavin Spindle** | Creepy obsessive fan/stalker | Deeply intrusive and suspicious, **canonically not the murderer**. His conduct has consequences and cannot be played as harmless romantic pursuit |
| **Marta Rook** | World-weary hotel manager | Knows access keys, hidden rooms and the building's history; may protect staff over celebrities |
| **Pip Calder** | Overworked night porter | Maintains switchboard, laundry lift and staff logs; genuine puzzle helper with labor concerns |

Provisional author mystery canon: **Odette killed Celestine** to bury a fraudulent posthumous likeness-rights agreement and unauthorized licensing scheme. The hotel trap/staging used a time-shifted service corridor and impersonated an on-site prop demonstration; the ghost did not see her assailant. This is a **spoiler for writers/tests**, not public title/preview text. Preserve a fair physical timeline and a verifiable alternate alibi. No twist that makes the stalker the killer.

## 5. Hotel geography and scene grammar
**Ground floor:** parking lot and flickering marquee; lobby/reception; lounge/press corner; diner and kitchen; convention hall/panels; autograph and merchandising aisle; wellness courtyard/hot tub; laundry/service stair; service alley/dumpster.
**Upper floor:** split corridor with squeaky floorboard; Vespera's velvet suite; Francesca's prop lab/guest room; Marina's damp room; Celestine's locked room and later haunting; fan-room 207; housekeeper closet; landing/view over ballroom; odd locked maintenance room.
Everything occupies one two-storey building plus immediate exterior; **no aimless procedural corridors**. Day/evening/after-hours states repurpose places. Every room has a visual joke, a purposeful clue, a character beat or a puzzle affordance, not just wallpaper.
Paths use a clear map with discovered shortcuts. Doors persist in their state; item combinations and access checks are deterministic. Softlocks forbidden.

**Visual language:** panoramic hand-painted backgrounds, tactile 1990s animation adventure shapes, neon motel fluorescents, ugly patterned carpets, monster glamour and cinematic character sprites. Adult camp without generic gold fantasy trim or a web-dashboard look. Large illustration first, small contextual tool wheel, readable high-contrast notebook drawer. On 390px phones: one viewport stage plus bottom action strip and bounded sheets; tablet and desktop retain image dominance.

## 6. Interactions and puzzle contract
Verb/icon menu: **Walk, Look, Talk, Take, Use, Combine, Photograph, Ask Topic, Switch Investigator**, with context disabling only where justified. Mouse/right click, keyboard, touch/long-press and accessible button alternatives work identically. Inventory icons and evidence cards are image-led. Character speech bubbles belong over stage, not a scrolling transcript page.

Three intertwining puzzle webs:
1. **Press access:** get credential and reach closed events by either Nico's hustle or Iris's legitimate photo/contract trail. Neither is mandatory.
2. **Locked-room murder:** reconstruct a 30-minute timeline using service lift bell, room key log, call-sheet, costume chemistry, unusual scent and staff route. No arbitrary item use or pixel hunting.
3. **Rights conspiracy:** prove Celestine challenged a likeness contract; connect a forged agreement, missing negatives and licensing ledger to Odette. Verify the non-killer stalker's frightening activities separately, and let players report him without falsely accusing him of murder.

Every critical clue has at least two discovery paths; every puzzle has a tested hint ladder, a cause-and-effect payoff and at least one non-lethal recovery if a player uses/loses an item. Optional red herrings add character, never secretly steal required evidence. Accusations require defensible evidence, but a failed accusation opens more leads instead of hard-stopping the run.

## 7. Plot structure and agency
**Act I: Check In, Check Out.** Arrive with no press badge, get an interview, explore the convention, meet the fan, attend an increasingly chaotic brand panel. Celestine is found dead, staged as promotional performance. A ghost appears later and remembers sensations but not the face of her killer.

**Act II: Dead Air.** The duo split interviews, interrogate the ghost, revisit rooms by night, uncover the hotel's plumbing and service routes, and expose the stalker's real alibi. Monster-world absurdity becomes essential detective reasoning.

**Act III: Last Call.** A storm and a contractual announcement converge. Reconstruct the true timeline, catch Odette in a falsifiable statement, and choose whether to publish a sensational exposé, defend the cast's rights, keep some intimacies private or compromise with the franchise. The culprit is fixed; the **outcome, evidence strength, bystander harm and ethics** vary.

Possible endings: jointly credited truthful exposé; truthful but predatory tabloid win; cast-owned rights victory; inconclusive ethical retreat; wrongly accused scandal; attempted cover-up with consequences. Track no arbitrary morality meter if world flags suffice.

## 8. Mature access, content and safety rules
**Mandatory access predicate, server authoritative:** authenticated user **AND** persisted `showMature === true` **AND** no `CHILD` role across primary or secondary roles. Reuse `viewerShowsMature` / `effectiveShowMature` from `server/utils/contentAccess.ts`; privilege roles never override child restriction. Guest, mature-off or child users must see neither the game in homepage Highlights/nav/Play lists/conductor discovery nor its content in SEO/search/API/server rendering/preloads. Direct route loads and game data/art endpoints deny access (not merely a hidden link). Test `?showMature=true` cannot widen access.

Optional adult content: cheeky double entendres, pinup glamour, consensual flirtation, suggestive hotel-hot-tub antics, private comic encounters. Allow a **romance/cheesecake setting** to reduce optional sexualized scenes even for opted-in adults; disabling does not invalidate the murder investigation or hide required clues. No minors in adult/romantic cast. Avoid coercion-as-reward, sexual assault as titillation, and treating the stalker's violations as courting. Mature art or scene prompts must stay within provider rules and carry traceable metadata. Avoid publishing explicit images or private content in issue/PR previews.

**Security/launch:** Access controls are a separate acceptance test. Internal admin preview still follows the maturity predicate and admin requirements. Public /play nav/highlights release is `gate_human: true` for both visual approval and publishing.

## 9. Art, animation, audio
First image: rain-streaked late-night view of cheap hotel with neon MONSTRESS CON marquee, asymmetrical second-floor balconies, a creature silhouette behind lit curtains, overstuffed convention foyer visible through doors. Title screen is a *game*, with animated sign buzz, soft rain and an inviting **Check In** control. Distinct illustrated rooms, cast portraits with several expressions, two protagonist walk cycles, four directions, item thumbnails and 6–12 cinematic moments per prototype. Pan/zoom only inside the stage; art assets fall back to intentionally illustrated placeholders.

Prompt batches are independent of functional puzzle/code progress; art queued is not art delivered. Final asset acceptance demands durable ArtJob IDs and verified images at rendering destinations.

## 10. Quality gates and playtests
- Deterministic seeded runs (no paid LLM dependency at play time), event-sourced/serializable save schema, versioned migrations, more than one save slot if kit supports it.
- Automated graph checks for reachable rooms, topic reveal state, clue redundancy, required items never deleted, and all intended endings/accusation failures reachable.
- Adversarial runs: always switch characters, never switch, exhaust topics out of order, use items prematurely, click 100 random hotspots, disable cheesecake, wrong accusation, save/reload mid-interview, block the fan, narrow screen/touch input.
- Verify keyboard focus, icon tooltips, speech captions, colorblind cues, no stage overflow at 390/768/1440px.
- **Gates:** finished art/visual acceptance and public discovery/route release remain separate human approval. All reversible implementation and tests continue without waiting on art.
