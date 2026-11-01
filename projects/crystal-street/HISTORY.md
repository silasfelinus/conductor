# crystal-street — task history archive

Full `note:` prose for completed crystal-street tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Design brief, writing guide, and the playable first slice at /admin/crystal-street

<!-- note:begin t-001 -->
DONE 2026-10-24 PT. kind_robots #4101 merged as 5274977 (all 24 checks green). Ships the seeded engine (utils/crystalStreet/rules.ts), 20 nightmares, 22 companions, 11 locations with 44 daylight beats, 8 night decks (48 cards), 17 items, illustrated success and failure on every choice (1,768 contract-clean prompts), the single-screen console UI at /admin/crystal-street with SVG art fallbacks, scrapbook, Playbook Manager adapter with live text overlay, contract test with seeded autoplay balance (Best 49% for a near-optimal policy) and its CI workflow. Cover art is the approved Monster Recast "Masking Up" pair. Verified at 390, 768 and 1440 widths in a local dev server with Playwright: no page scroll. Admin-only; reaches production with the next Alexandria deploy.
<!-- note:end t-001 -->

## t-003 — Deliver art round 1 into the runtime paths

<!-- note:begin t-003 -->
art/ROUND-1.yaml (auto_submit) renders 21 villain posters and 22 portraits, 22 companion posters, 132 companion mood portraits and 11 locations as ArtImages. Wire delivery: the runtime looks for /crystal-street/villains/<id>-poster.webp (the cover and Counselor Jess poster already ship), /crystal-street/companions/<id>-<emotion|poster>.webp and /crystal-street/locations/<id>.webp and falls back to code-drawn SVG. Either export DONE ArtImages to those media paths (follow the Emperor of Dust / Shifting Lands export pattern) or map ids to ArtImage URLs in a manifest the store reads. Verify final URLs, not job status.
DONE 2026-10-24 PT. kind_robots #4122 merged as 72a14f7: 208 round-1 renders (21 villain posters, 22 portraits, 22 companion posters, 132 moods, 11 locations) exported as WebP (max edge 1024, 12 MB) into public/crystal-street/ by scripts/export_crystal_street_art.py; contact sheet reviewed. Every existing runtime path now resolves to painted art.
<!-- note:end t-003 -->

## t-006 — Balance pass from the seeded autoplay report

<!-- note:begin t-006 -->
verifyCrystalStreet.test.ts prints the ending mix across 240 autoplayed weeks. Tune BEST_WINS, targets, dread penalties, perk strength and night card difficulty so a careful week reaches Best for every nightmare without making it automatic, and so weak archetype matchups stay winnable. Add per-villain and per-archetype rates to a BALANCE-REPORT.md.
Claimed 2026-10-25 PT: a reusable report script in kind_robots (per nightmare, clique, look, style, typecast vs against type, careful vs careless policy, special endings), BALANCE-REPORT.md here, and tuning toward the #4143 targets (every nightmare 40-75% best under near-optimal play; typecast within 5 points of against type).
Closed 2026-10-25 PT: kind_robots #4154 merged as 11d6d74. Report script utils/scripts/crystalStreetBalanceReport.ts (careful and careless policies); Typecast capped at +2 (gap 9 -> 2 points); 88 villain-card target edits across 12 nightmares, no card all-easy or all-hard; best-ending spread 32-85% -> 41-81% (46-75% on a second seed set). Known high edge: The Hungry House, Counselor Jess, Mickey Moore. Report: projects/crystal-street/BALANCE-REPORT.md.
<!-- note:end t-006 -->

## t-007 — Narrative audit: voice, continuity, and the queer-positive rules across all cards

<!-- note:begin t-007 -->
Content was written in parallel. Read every nightmare, companion meeting, beat and deck card against WRITING-GUIDE.md: consistent NPC names, no villain contradicting the cast table, no slurs or queer-coded menace, PG-13, parody brand names, each choice a real dilemma, clue trios that actually explain the central issue. Fix in place; log findings.
Open flags to settle (2026-10-24 PT): The Shape's Mickey vanished in 1972 (bury-your-gays risk); Chip's bio outs him; Goody Hale's Nisenan reference; Glory sings the real song "I Am What I Am"; and Mister Fuzzbutton's Act II card "Secrets on the Request Line", where a bear threatens to air a secret about Chip (written as consent, "it isn't the bear's to tell", Chip never outed on any path; Silas to make the final call). 198 villain cards and 66 edge choices landed 2026-10-24 by parallel writers and need this read too.
2026-10-25 PT: red team done. Seven independent reviewers read 22 nightmares (Dot was reviewed at landing), companions and decks against WRITING-GUIDE.md: about 30 blocking and 120 polish fixes, a global brand sweep, quoted lyrics removed, two death-reading bad endings now Taken (kind_robots #4159). An art audit of every shipped image pulled Counselor Jess's poster, portrait and ending (gore and a sexualized minor in the background) and queued 10 re-rolls (art/REROLL-1.yaml). The creative calls left for Silas, including the open flags above, are listed in RED-TEAM-2026-10-25.md and fold into the t-011 final gate.
<!-- note:end t-007 -->

## t-008 — Companion depth: personal arcs and nightmare-specific reactions

<!-- note:begin t-008 -->
Give each companion a three-step personal thread across the week (Chip's coming out to a crew that has his back, Delphine and Roz's last dance, Glory and Frieda, Wade's poetry), plus reactions when their friendship tag matches a nightmare. Loyalty should matter to endings without adding new ending slots.
2026-10-25 PT: done in kind_robots #4164. Every companion has a three-step hangout arc (one hangout a day at their spot while in the crew); finishing it makes them Loyal, +1 each (cap +2) on finale rolls. 2-4 nightmare-tag reactions each. 121 outcomes got alone text for when the bonus companion isn't in the crew. Named threads as specified (Chip coming out on his own terms, Delphine's dance for Roz, Glory and Frieda, Wade's poetry). Balance: 20 villain-deck choices 9->11, every nightmare inside 40-75%; BALANCE-REPORT.md refreshed.
<!-- note:end t-008 -->

## t-009 — Scrapbook polish: highlight polaroids, ending gallery, run sharing

<!-- note:begin t-009 -->
Show each run's highlight outcome art as polaroids, a full ending gallery per nightmare (80 tiles), and a share card with seed so a friend can replay the same week.
Scrapbook shipped in kind_robots #4167 (merged 14bed77): highlight polaroids using round-3 outcome plates with drawn-scene fallback, the 92-tile endings wall, and share-a- week links (?week=&nightmare=) validated by sharedWeekFrom with round-trip and same-deal tests.
<!-- note:end t-009 -->

## t-010 — Content expansion: more daylight beats and night cards for replay variety

<!-- note:begin t-010 -->
Grow decks from 6 to 10 cards per tag and locations from 4 to 6 beats, keep the validator green, and add weekday-specific beats (school on weekdays, the Saturday midnight movie). From t-018 (2026-10-25 PT): regroup the street decks around monster types that read at a glance (supernatural, slasher, creature, alien, biohazard, tech, cult, camp, dream, generic suburban trouble) as part of the growth.
2026-10-25 PT: done in kind_robots #4166. Street decks 6 -> 10 cards each plus two new monster-type decks, Biohazard and Suburban trouble (dealt to Bog Baby, Sugarlings, Big Gertie / Hungry House, MOM-3000, Brightwaters, Screwhead); tags show as readable monster types. Locations 4 -> 6 beats; beats may carry days (weekday school, Saturday midnight- movie marquee, Sunday mass and swap meet, Halloween-day beats). 78 new cards; balance holds (careful 64% Best, every nightmare 40-75%).
<!-- note:end t-010 -->

## t-012 — Re-cast the nightmares as gender-flipped and gender-bent classic villains

<!-- note:begin t-012 -->
DONE 2026-10-24 PT: kind_robots #4103 merged as 34ea24f (all 22 checks green). Session 2026-10-24 PT. Every villain gains an inspiration block (classic original, film, year, flip/bend/remix, old script, new lens) shown on the arrival splash and case board. Counselor Chad becomes Counselor Jess (Jason flipped, matching the cover art), Screwhead becomes Magda Szabo (Pinhead flipped), and two are added: The Shape in the Cardigan (Michael Myers flipped) and The Final Cut (the killer-reveal trope as the villain, with the slandered actress as hero). Roster 22. Rules: WRITING-GUIDE.md "The re-cast".
<!-- note:end t-012 -->

## t-013 — Play front end: /play/crystal-street, arcade tab, and the home highlight reel

<!-- note:begin t-013 -->
Silas asked for it in session 2026-10-24 PT ("Create the front end in Play, and include a link to Terrors on the user dashboard highlight reel"), which is the publish approval for the Play front end; visual acceptance of the finished game stays t-011. Move the game from /admin/crystal-street to /play/crystal-street (admin route redirects, as Save the Plumber does), add content/channels/arcade/crystal-street.md, set the Kind Robots Project presentation fields (liveUrl, channelKey, tabKey), and add Terrors to components/home/home-visitor-directory.vue (an Explore feature card and a Just updated entry). Update the route contract tests together.
2026-10-24 PT: implemented in kind_robots #4128 (open, together with t-014): /play route, 301 admin redirect, arcade tab, projectPlacements entry, highlight-reel card and update, route contracts. Close when it merges.
DONE 2026-10-24 PT. kind_robots #4128 merged as b3fcf57 (all checks green): /play/crystal-street with the /admin URL 301-redirecting, the arcade tab (mask icon), projectPlacements, and a home highlight-reel feature card plus Just updated entry; route contracts updated.
<!-- note:end t-013 -->

## t-014 — Main menu shell: title screen, start and continue, settings, monster gallery, endings, crew

<!-- note:begin t-014 -->
One-screen console menu over the cover: Start a week, Continue, Settings, Monster Gallery, Endings, Crew, Scrapbook, How to Play, Credits. Settings (store-owned, persisted): text size, reduced motion, high contrast, music and effects volume, dice animation speed. Monster Gallery: all 22 nightmares with delivered poster and portrait art, locked silhouettes until met, backstory and the old script / new lens once faced, endings found per nightmare. Endings viewer: the 88 endings (22 x 4) as a gallery; found ones open full text and art, locked ones show the tier and a hint. Crew gallery with the six mood portraits and poster toggle. Check 390, 768 and 1440 widths with screenshots.
2026-10-24 PT: implemented in kind_robots #4128 (open). Per Silas's follow-ups the title is now an idyllic daytime Crystal Street with TERRORS set large and "on Crystal Street" below, then a slideshow of every survived nightmare's ending photo; New week has a Pick your look avatar strip. Settings shipped: text size, contrast, motion, give up the week, erase the scrapbook (music and effects volume arrive with t-015 and sound). Screenshots at 390, 768 and 1440 show no page scroll. Close when it merges.
DONE 2026-10-24 PT. kind_robots #4128 merged as b3fcf57: main menu over the idyllic street title (TERRORS large) with a slideshow of survived nightmares' ending photos, monster gallery, endings reel (88), friends roster, scrapbook, how to play, settings, credits, and the Pick your look avatar strip. Verified at 390, 768 and 1440 with no page scroll.
<!-- note:end t-014 -->

## t-015 — Theme music video: 60-second high-energy punk theme, Addams-meets-Halloween

<!-- note:begin t-015 -->
Build with scripts/build_music_video.py (MusicVideo doc, lyrics, ACE-Step song, beat-grid scenes, stills through the ArtJob queue, ffmpeg MP4). Brief: a 60-second, about 170 BPM punk song with a macabre finger-snap, harpsichord and organ hook (the Addams side) and a cold five-four synth slasher pulse (the Halloween side), gang vocals, lyrics about Crystal Street and its nightmares. Use style words only; pass --banned-terms for the film and franchise names. Scenes reuse the round-1 cast and cover art where they fit. Export the MP4 into kind_robots public/crystal-street/video/ (pattern: scripts/export_rainbow_opening.py) and give the title screen a "Watch the theme" player. Renders take hours on the one GPU; the run resumes.
DONE 2026-10-24 PT. kind_robots #4133 merged as eab79a3: the 60-second horror-punk theme (Kind Robots MusicVideo 15, final ArtImage 253094, private) ships at public/crystal- street/video/theme.mp4 (5.8 MB) behind a Watch the theme menu item with the lyrics beside it. Fixed before shipping: the lyric now says Jess 'she creeps' (song re- rendered), the lake monster and vampire re-rendered on-model as Jess and the Countess, and a crew frame with a rifle and knife re-rendered with flashlights and a boombox.
2026-10-25 PT: Silas asked for this intro to run in the Music Video creator. kind_robots#4165 (merged 7421ad0) adds the prepared spec crystal-street-theme: the same song (ArtImage 253093) and 14 reviewed stills, plus 4 hero shots to animate (ride in, Jess rising, the Countess, the closing circle). A re-run is optional; the shipped theme.mp4 stays until a new cut is approved.
<!-- note:end t-015 -->

## t-017 — Front-end art: the idyllic title street, an ending photo per nightmare, sixteen avatars

<!-- note:begin t-017 -->
Silas 2026-10-24 PT (notes above). art/FRONT-1.yaml (auto_submit) queued 38 renders on 2026-10-24 (ArtJobs 45095-45132): title/crystal-street (white clapboard cul-de-sac in autumn sun), villains/<id>-ending for 21 nightmares in an inked horror-comic lane matching the Masking Up cover (which is Counselor Jess's ending photo, already shipped), and avatars/<id> for the sixteen player avatars in kind_robots utils/crystalStreet/avatars.json. Review the contact sheet (scripts/export_crystal_street_art.py --sheet), re-roll misses, then export into kind_robots public/crystal-street/ and open the PR. The runtime already reads all three paths and falls back to drawn art until they land.
DONE 2026-10-24 PT. kind_robots #4130 merged as a972eae (all checks green): the idyllic title street (native 1216 px), 21 ending photos in the Masking Up inked style (Jess's is the cover) and the 16 avatars, delivered from art/FRONT-1.yaml after contact-sheet review; the title holds on the street for ten seconds before the slideshow, TERRORS set heavy, 'on Crystal Street' legible beneath.
<!-- note:end t-017 -->

## t-018 — Acts and villain decks: a deck choice every night, three cards per act, finale edges

<!-- note:begin t-018 -->
Silas 2026-10-24 PT (both notes above; the second supersedes the six-scene pool). Design: the week runs in three acts (nights 1-2, 3-4, 5-6) and Halloween. Each night deals two cards and the player picks the deck for each: the nightmare's villain deck (cards of the current act, harder) or the street deck its kind shares. Beating any villain card of an act earns that act's edge; each edge adds +1 to every finale roll and unlocks an edge choice (target 7) that remembers the act and counts as fight, trick or heart. Base finale checks are all hard (11); Best needs the heart and ten night wins, so first-act failures cost edges but never lock the finale.
Progress 2026-10-24 PT: kind_robots #4129 merged (66 extra villain cards). #4131 merged as 45d3043: acts, the nightly deck choice, edges (+1 per edge on finale rolls), approach-aware endings, the night deck screen, base finale checks at 11, Best at ten night wins. #4134 merged as 5020e8c: three villain cards per act for every nightmare (198 in all) and three finale edge choices each (edge-1 trick, edge-2 fight, edge-3 heart plus the three leads; all target 7, each remembering its act). Seeded autoplay: best 65%, good 14%, bittersweet 17%, bad 5%. Still to do: regroup the street decks around monster types that read at a glance (supernatural, slasher, creature, alien, biohazard, tech, cult, camp, dream, generic suburban trouble) and grow them (t-010), and add the nurse and market daytime stops Silas listed.
Closed 2026-10-25 PT: #4135 merged as 5f8107d (Mercy Valley Clinic with Nurse Inez Duarte: See the nurse for +3 nerve and steadies shaken friends; Thriftee-Mart: comfort food for 2 quarters, +1 nerve and -1 dread), and #4137 delivered both location paintings (art/STOPS-1.yaml). The street-deck regroup by monster type moves to t-010. Best now needs twelve night wins (#4141, after character style bonuses).
<!-- note:end t-018 -->

## t-019 — Factions (friends, family, officials, neighbors) and their special endings, including Final Girl

<!-- note:begin t-019 -->
Silas 2026-10-24 PT: "We could do factions: friends family officials neighbors. if any of them drop to zero that could trigger a special end sequence depending on which dropped. If it's friends then they enter Final Girl sequence (if we can find a way to make that inclusive)." Four standing meters moved by choice effects and shown in the HUD. Zero in one triggers its own end sequence: family (grounded, locked in your room the night it comes for you), officials (the sheriff and the principal blame you), neighbors (the cul-de-sac turns on you, torches and casseroles). Friends at zero starts the Final Girl sequence: a solo last-stand chapter where "Final Girl" is a title the player earns whatever their pronouns, with its own cards and an ending in each nightmare's scrapbook row. Write it so the role is about who survives, never about gender. Each sequence needs effects on existing cards, new cards, endings and art prompts; the scrapbook and endings reel gain a special-endings row.
Claimed 2026-10-25 PT. Design: four standings (friends, family, officials, neighbors) 0-5, start 3, moved systemically so existing cards need no rewrite: family -1 per nightmare-deck draw, +1 rest at home or comfort food; officials -1 on failed sneaky/reckless night rolls, +1 training at school or library; neighbors -1 on failed street-deck rolls, +1 on kind successes; friends -1 when a friend is shaken or dismissed, +1 per recruit. Zero ends the week in a special ending (grounded, blamed, run out of the cul-de-sac); friends at zero starts the Final Girl sequence: the finale comes early, solo, crew bonuses off and edges kept, and a win earns the Final Girl title whatever the player's pronouns. Scrapbook gains a special-endings row.
Closed 2026-10-25 PT: kind_robots #4151 merged as ae5a572. Final rules: failures cost standing (family once a night for a lost nightmare card; officials for failed sneaky or reckless night rolls; neighbors once a night for a failed street card; friends for a shaken or dismissed friend or a night faced alone), and rest, comfort food, study at library or high school, kind successes and recruits mend it. Family starts at 4, others at 3, max 5. Collapses end the week as Grounded, Blamed or Run Out of the Cul-de-Sac; friends at zero bring the finale that night with no crew bonuses and a win stamps Final Girl. Near-optimal autoplay best 59% with ~2% special endings; random play collapses ~23% and wins Final Girl ~5%. Art: art/SPECIAL-1.yaml jobs 45341-45344, delivery pending.
<!-- note:end t-019 -->

## t-020 — New nightmare: frat house drag night, a slumber-party-massacre remix

<!-- note:begin t-020 -->
Silas 2026-10-24 PT: "a story using slumber party massacre setup, but it's a boys fraternity doing a drag night. so you get the classic tropes of the woman breaking her heel in the woods, but as the stalker gets closer, your "damsel" is Chad in a bad wig and lipstick." Add it as the 23rd nightmare (a remix of The Slumber Party Massacre's driller killer) with full cast data: leads, a signature pool, finale, four endings, poster, portrait and ending photo. Guardrails from WRITING-GUIDE.md: the joke is the old damsel tropes landing on the frat brothers (the heel snaps, the phone line is dead, someone says "I'll be right back"), never drag or queerness as the punchline. The drag night is sincere, coached by Glory Hallelujah from the Glitter Box, and the brothers who commit to it are the ones who make it to morning.
Claimed 2026-10-25 PT (Silas: "start the frat drag night nightmare next"). Design: Dot Ruskin, the Slumber Party Driller (id dot-ruskin), a 1966 shop-class girl humiliated by Valley State's Gamma Rho panty-raid tradition and blamed for fighting back; the 1986 brothers' sincere drag night for the Glitter Box roof, coached by Glory Hallelujah; Best ending returns the trophies, apologizes and puts Dot at the workbench building the stage.
Closed 2026-10-25 PT: kind_robots #4148 merged as 6649d83. Dot Ruskin, the Slumber Party Driller, is the 23rd nightmare (3 clues, 9 villain cards, 6-choice finale, 4 endings), reviewed by an independent agent (3 blocking and 27 polish findings, all fixed). Seeded autoplay with 23 nightmares: best 59%; Dot alone 73%. Art: art/NIGHTMARE-23.yaml jobs 45329-45331 (poster, portrait, ending photo), delivery pending.
<!-- note:end t-020 -->

## t-021 — Look + clique = character: 96 profiles with style synergy, their portraits, and the screen dial

<!-- note:begin t-021 -->
Silas 2026-10-24 PT: "I'll accept the avatar and then class choice if we plan out the synergy for each character and have a profile built for each combination with a fresh piece of illustrated art ... please feel free to redesign these choices for optimum fun", "there is definitely some confusion between role and character in the select screen", and "settings, info, character bio, scrapbook can be reached via icons on the top, rotating for which is selected". Design: each of the 16 looks has a style (brave, clever, kind, camp, sneaky, reckless) that adds to choices played that way (+2 for the rarer camp/sneaky/reckless, +1 otherwise); each clique has a home style, Typecast when it matches (+1 more), Against type otherwise (+1 on the clique's style). 96 characters with name, tagline, bio, catchphrase and portrait prompt in kind_robots utils/crystalStreet/characters.json; the wizard is Pick a look, Pick a clique, Meet your character, The nightmare; "The Prep" look is now Match Point. Best ending moved to twelve night wins (near-optimal autoplay 58%). Portraits: art/CHARACTERS-1.yaml (jobs 45217-45312), delivered with scripts/export_crystal_street_art.py. Done when #4141 is merged and all 96 portraits are delivered to /crystal-street/characters/.
2026-10-25 PT: all 96 character portraits delivered (#4149, #4152, #4157; the Parking Lot Howler re-roll shipped in #4157). Profiles, synergy and the rotating front-end dial live since #4141.
<!-- note:end t-021 -->

## t-022 — Separate player identity from nightmare selection on final new-week screen

<!-- note:begin t-022 -->
Silas 2026-10-25 PT provided an iPad screenshot: the player's portrait and name immediately beneath "The nightmare" makes it look like the player is the antagonist. Move the player identity above that heading or to a distinct footer, clearly label the player, retain villain-selection controls and one-screen bounded layout.

Player portrait/name relocated above the Nightmare heading on the final new-week step. The villain selector stays beneath its heading, without changes to game state.

DONE 2026-10-25 PT. kind_robots PR #4187 merged as 0c0cb4280133b45c3c9ace875a886608d0876383. The final wizard places a labeled player character summary above the Nightmare title, leaving villain selection distinct and gameplay unchanged. All 19 PR check runs passed, including formatting, TypeScript, layout and Crystal Street gameplay contract. Self-hosted release remains a separate deployment state; no manual deploy triggered.
<!-- note:end t-022 -->

## t-023 — Playbook Forge upgrade: literal prompts for all 591 unpainted Crystal Street beats

<!-- note:begin t-023 -->
Silas, 2026-10-27 PT: "Anything that is in playbook forge and has quests unwritten or art prompts unwritten should be upgraded. (Memory dungeon will take the longest and should be last). Space couch has a lot of fresh writing still in need and still looking to capture that right blend of space comedy and satire. All art prompts should be written for the appropriate engine, no metaphors for krea2." Shared bar: kind_robots PR #4308 (verifyPlaybookArtPrompts, artPromptsComplete). Forge 2026-10-27: 591 unpainted beats have no prompt surfaced to the Forge (Z-Image first lane). Port and fix this project's ledger prompts, and write the rest.
DONE 2026-10-27 PT: kind_robots #4318 merged as 98c0278 after 19/19 checks. All 591 unpainted beats (23 nightmares with leads, nights, finales and endings; 78 daylight beats; 100 night-deck cards; 22 companion meetings) now carry rewritten literal prompts in the game's own data. They run 356-734 chars and keep one look per recurring character. artPromptsComplete is on, and crystalStreetArtContract finds 0 violations across 3771 prompts. allArtPrompts and future rounds inherit them.
<!-- note:end t-023 -->
