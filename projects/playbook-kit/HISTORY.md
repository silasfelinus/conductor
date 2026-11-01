# playbook-kit — task history archive

Full `note:` prose for completed playbook-kit tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Playbook Kit framework: spec, complexity budget, one-screen shell, scaffold and templates

<!-- note:begin t-001 -->
Created and built in the same Silas-directed session (no prior task to claim).
kind_robots PR #4214: PlaybookKitSpec, Vignette/Standard/Saga budget with
attention and parallel-thread caps, written allowances, integrity rules and
a nine-rung ladder; shell with Cast/Factions/Secrets/Scrapbook/Endings/Settings
panes, spoiler-free trailer and moment view; playbookKitStore; /admin/playbook-kit
console; npm run playbook:new; test:playbook-kit + playbook-kit.yml; reference
Vignette "The Lantern Ferry". Conductor: this project, templates/ (design brief
and roadmap ladder) and scripts/new_playbook.py.
DONE 2026-10-26 PT: kind_robots #4214 merged as c9428c3 after 23/23 green checks;
conductor half lands with this roadmap (#6678). Silas then asked for the next
layer (playbook-kit t-010+): Playbook Forge admin console, manager integration and
an AAA console visual pass replacing the web-app look of the first shell.
<!-- note:end t-001 -->

## t-010 — Forge design: common core vs extras across every playbook, save/load, character creation, estimator model, AAA console spec

<!-- note:begin t-010 -->
Silas, 2026-10-26 PT: "This should integrate with the playbook manager for each
project, with consistency. Figure out what is similar and what are extras, and how
to create a front end manager that allows any of those options and more. In a
minimalist straightforward interface. This investigation should be including: how
to handle save load. Different factors for character avatar: opening creator,
images, factors to build from." Final version: "a front end admin project where I
can input an idea, configure factors like character, end sequences, acts, with an
aim to have a strong helper with estimates of how each factor will affect estimated
gen time (based on checkpoint, text needs, image gen average, etc.) ... create a new
project, kind robots front end (placed in admin or play or projects), and give it
genre, expectations: stats, followers, quests, character gen, number of unique
endings, pass/fail versus always interesting, skill checks, etc. It should also be
able to analyze and adjust prospected plans for existing projects." And: "Every one
of those screenshots is backwards. We should be using aaa console game design specs,
those shots were 100% old webapp."
Deliverable: DESIGN-FORGE.md in this project.
DONE 2026-10-26 PT: DESIGN-FORGE.md (three read-only surveys of eight playbooks plus
202 measured ArtJob render times).
<!-- note:end t-010 -->

## t-011 — AAA console visual system for the kit shell and the Forge (dark full-bleed theme, safe area, focus/gamepad navigation, bumper tabs, button prompts)

<!-- note:begin t-011 -->
The Forge ships the console system (forge theme, safe area, focus/gamepad,
bumper tabs, prompt bar). Remaining: move playbook-kit-shell and /admin/playbook-kit
onto it (shared CSS out of the forge console component into one stylesheet).
DONE 2026-10-26 PT: kind_robots #4227 merged as 329b435 (shared assets/css/playbook-console.css, console
kit shell, settings as option rows; fixed a scoped @layer in playbook-kit-art that let
Tailwind's preflight beat component styles when its chunk loaded first).
<!-- note:end t-011 -->

## t-012 — Playbook Forge admin console: idea, genre, placement, factor loadout, live forecast and per-factor deltas, launch as a Kind Robots project

<!-- note:begin t-012 -->
Built in kind_robots claude/playbook-forge: /admin/playbook-forge console (title,
library, idea, seven-page loadout, forecast HUD with per-step previews, launch,
assumptions), utils/playbookForge (blueprint, 51 factor rows, calibrated estimator,
handoff), playbookForgeStore, scoped `forge` theme, utils/consoleInput.ts (focus
navigation + gamepad), verifyPlaybookForge.test.ts. Conductor: new_playbook.py
--blueprint.
DONE 2026-10-26 PT: kind_robots #4219 merged as d90a1b5 (25/25 checks green after a
nav-summary length fix); conductor #6684 merged as 497f6b2.
<!-- note:end t-012 -->

## t-016 — Production ledger: load any game, enumerate every beat's art and words, spent vs left, stars, super shiny, discrepancies, submit sections to relay or agent

<!-- note:begin t-016 -->
Silas 2026-10-26: any game loads and enumerates all its computations, what they took
and what is left; complete sections star, all complete is super shiny; discrepancies
shown; sections submit to the relay or the next agent. Design: DESIGN-FORGE.md section 10.
DONE 2026-10-26 PT: shipped in kind_robots #4232, merged as ae77ac8 (Forge Load a game
ledger, /api/admin/playbook-ledger/[slug], Submit art / Send writing per section).
<!-- note:end t-016 -->

## t-018 — One admin manager: Playbook Studio beats and the Kit console inside the Forge; library percent complete, sortable

<!-- note:begin t-018 -->
Silas 2026-10-26: "we don't need two admin managers ... playbook studio was built next to
playbook kit, instead of implementing it." The Forge absorbs the Studio (Beats screen: list
or cards, Edit / As played) and the Kit console; /admin/playbook-manager and
/admin/playbook-kit redirect into it. Then: "the percentage complete should be viewable, and
sortable" on Load a game. DONE 2026-10-26 PT: kind_robots #4251 merged as f781cff.
<!-- note:end t-018 -->

## t-019 — Ledger Adjust panel: change plan numbers, add elements, post direction to the game's GitHub issue; openings multiply endings

<!-- note:begin t-019 -->
Silas 2026-10-26: "type out adjustments that ideally get posted to the github issues ... add
elements from this screen, or change assumptions like number of followers ... adding a
captain to the mix will multiply [the endings]." New factors: places on the map, follower
quest steps, ending versions (one each / per hero). Posts go to the master issue in
docs/agents/master-issues.yaml via POST /api/playbook-forge/adjustment (server GITHUB_TOKEN).
DONE 2026-10-26 PT: kind_robots #4255 merged as ed3e614. Live posting is unverified until a
production admin posts one (the token's kind_robots issue scope is not confirmed).
<!-- note:end t-019 -->

## t-020 — Kind Robots Facets as design material in the Forge: genre shelf, spark deck, draw elements

<!-- note:begin t-020 -->
Silas 2026-10-26: "use the kind robots facets: genres for more ideas. The other facets can be
used to generate other ideas to go into a design." GENRE Facets start from the nearest
loadout; MOOD/SETTING/THEME/ARCHETYPE/OCCUPATION/SPECIES/QUIRK/BACKSTORY/MATERIAL/ART_DIRECTION
are dealt into tone, world, question, hero, companion, quirk, villain, artifact and look slots,
carried on the blueprint as sparks into the Conductor pitch; Draw from Facets names ledger
additions. DONE 2026-10-26 PT: kind_robots #4258 merged.
<!-- note:end t-020 -->

## t-021 — Never prompt art from titles; progress credits writing; Memory Dungeon in the Forge

<!-- note:begin t-021 -->
Silas 2026-10-26: Forge-submitted prompts carried chapter titles; "ecotone is more developed
than you give it credit for"; "can we also get support for memory dungeon?" Authored
PlaybookNode.artPrompt is the only prompt; beats without one queue a prompt-writing Todo.
Progress is half writing, half art. Memory Dungeon is a Studio adapter (240 beats) whose
image-store art the ledger API confirms per file. 317 title-built jobs were cancelled and 363
notes resolved on production. DONE 2026-10-26 PT: kind_robots #4261 merged as 6e2aedf.
<!-- note:end t-021 -->

## t-023 — The Forge as an art-forward command center: design boards and the Catalogue

<!-- note:begin t-023 -->
Silas 2026-10-26: "I should see designs or text prompts for all pitches, or have the ability
to add/edit, etc new designs ... more like an interface than a museum ... facets, characters,
locations, rewards, scenarios, viewable as a catalogue for brainstorming." Design boards (image,
else prompt) with add/edit and render through /api/art/enqueue; a Catalogue of Facets,
Characters, Locations, Scenarios, Rewards and game art with a brainstorm tray that starts a
playbook or adds designs to the open game; pitches carry designs (conductor #6708 requires
them from 2026-10-27). DONE 2026-10-26 PT: kind_robots #4265 merged as cd04cae; conductor
#6708 merged as e476cb7.
<!-- note:end t-023 -->

## t-024 — Memory Dungeon planned at sixteen realms; ledger progress counts unbuilt scope

<!-- note:begin t-024 -->
Silas 2026-10-27: "Each overworld has 64 encounters, there are 16 overworlds." The plan follows
projects/memory-dungeon/SIXTEEN-REALM-PRODUCTION.md (1,600 positions, 96 enemies, 128
sidequests, 32 photographs, 64 achievements, 12 endings); the count measures every overworld
tile and House room (200 of 1,600); ledger progress scales by encounters built of planned.
DONE 2026-10-26 PT: kind_robots #4267 merged as d163a90.
<!-- note:end t-024 -->

## t-025 — Forge gallery: sections and people as large art, with prompts, renders and comments

<!-- note:begin t-025 -->
Silas 2026-10-27: "images representing each section, it's interactive and allows comments,
resubmissions, and reart gen prompt writing and reviewing ... if followers are an important
junction, I should see their page and a gallery of all entries, or acknowledgements of the
missing." Ledger -> Gallery: section and person shelves, large beat cards with honest status,
an inspector with renders, the prompt to review/render/propose/ask for, and notes on beats,
sections (section:<kind>) and people (person:<id>). DONE 2026-10-26 PT: kind_robots #4271
merged as 1286537.
<!-- note:end t-025 -->

## t-027 — Cthulhuquarium and The Ruler Is Hooked in the Forge (adapters, plans, ledgers, galleries)

<!-- note:begin t-027 -->
Silas 2026-10-27: "next we need support for cthulhuquarium and the ruler is hooked." Studio
adapters over each game's authored content with art paths and prompts, plans from their design
briefs, ledger and gallery entries.
DONE 2026-10-26 PT: kind_robots #4275 merged as cc3a878 (adapters over the bestiary, scenes,
backgrounds and shopkeepers; the opening, decks, arcs, endings, Fishopedia, cast, rulers, rewards
and shop; plans from their design docs; section names per game; bundled art resolved in the browser).
<!-- note:end t-027 -->

## t-028 — Forge production board: hero poster, rich follower galleries and full-scope progress

<!-- note:begin t-028 -->
Silas 2026-10-26 PT: Show prominent selected-playbook hero poster; let a follower section reveal visually grouped real roster members with hero/sidekick/villain character cards, portraits, biographies, and quest/romance outcomes. Creative directions such as zodiac or tarot should be sent to the game's master issue. Progress must distinguish completed authored beats from the overall unbuilt plan and unpainted images, especially Memory Dungeon (only first two of sixteen realms substantially authored).
Implementation task created and claimed in this directed GitHub session.

Kind Robots worker/forge-production-board-t028-20261027-f7ac contains the visual selected-poster, cast family gallery, full identity art variants and story bible, scoped GitHub creative direction, and an unbuilt-scope-aware progress denominator. Review CI on the implementation PR.

DONE 2026-10-26 PT: kind_robots PR #4287 merged as 6bf3a7153b04b20465a356c53e4d3539e0705458. All 16 GitHub workflows completed with success, including the four Contract Tests shards, TypeScript, Prettier, layout, art-safety and Playbook Kit. Selected-game key art and title, group gallery with 48 Prom identities and full story variants/stats, Space Couch cast lore, master-issue creative directions and estimate-aware Memory Dungeon 16-realm unbuilt progress. Implementation branch auto-deleted after merge. This merge does not assert Alexandria deployment.
<!-- note:end t-028 -->

## t-029 — Playbook Forge upgrade: literal Krea 2 prompts for The Lantern Ferry's 19 unpainted beats

<!-- note:begin t-029 -->
Silas, 2026-10-27 PT: "Anything that is in playbook forge and has quests unwritten or art prompts unwritten should be upgraded. (Memory dungeon will take the longest and should be last). Space couch has a lot of fresh writing still in need and still looking to capture that right blend of space comedy and satire. All art prompts should be written for the appropriate engine, no metaphors for krea2." Shared bar: kind_robots PR #4308 (verifyPlaybookArtPrompts, artPromptsComplete). Forge 2026-10-27: 19 unpainted kit beats have no prompt. Feeds t-009.
DONE 2026-10-27 PT: kind_robots #4328 merged as 70894b4 after 19/19 checks. The Lantern Ferry has literal Krea 2 prompts for all 19 beats plus 2 faction emblems, every one of the 21 t-009 briefs rewritten (format and mood words removed). KitArt.prompt and spec artPromptsComplete now pass through kit.ts, and verifyPlaybookKit runs every picture through the enqueue contract. Rendering and src wiring remain t-009.
<!-- note:end t-029 -->
