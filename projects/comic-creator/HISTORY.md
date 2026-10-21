# comic-creator — task history archive

Full `note:` prose for completed comic-creator tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Confirm scope with Silas

<!-- note:begin t-002 -->
FOR SILAS: soft checkpoint, nothing is blocked on it. Read projects/comic-creator/DESIGN-BRIEF.md and confirm or redirect the agent picks listed in notes_from_silas. If there is no answer within 7 days the next gate-triage session adopts them as written under the 2026-09-30 default-recommendation rule.

Silas approved all proposals in session on 2026-10-02 ("I like all proposals"); agent picks in notes_from_silas stand as written.
<!-- note:end t-002 -->

## t-003 — Survey kind_robots for reusable parts and confirm the editor approach

<!-- note:begin t-003 -->
Read-only survey, write projects/comic-creator/docs/survey.md: which existing gallery, character, scenario and canvas utilities can be reused; whether any existing canvas, drag or PDF code exists; where /play/* pages and the store pattern live; which public image APIs can fill a panel without auth. Recommend PDF library (or hand-rolled) and the sticker file format. No code changes.
2026-10-03: survey written to projects/comic-creator/docs/survey.md (reusable KR parts, editor approach, PDF/sticker recommendations); Silas-directed session.
<!-- note:end t-003 -->

## t-013 — Comic Studio vetting loop at /play/comics/studio (kind_robots, admin)

<!-- note:begin t-013 -->
Silas, 2026-10-03: the one thing he likes in the coloring studio is vetting, side-by-side variants, an editable prompt and "New <variant>" resubmits with history and final/rejected badges, but not its UI or its Conductor-YAML backend. Build it Kind Robots-native: additive Prisma models (series, entities, slots, attempts, issues), lanes (engine + checkpoint) rendered through POST /api/art/enqueue, verdicts, attempt history, series/entity notes with a secret-until marker, and an import endpoint seeded from the round-2 and round-3 ledgers. Schema-affecting (additive). Design: docs/survey.md, docs/inspiration.md.
Built in kind_robots PR #3208 (schema-affecting, additive). Live only after the Alexandria deploy runs migration 20261003120000_add_comic_studio.
kind_robots#3208 merged (squash 3e8ce36). Schema-affecting: live only after the Alexandria deploy runs migration 20261003120000_add_comic_studio; then seed with scripts/import_comic_studio.py --live.
<!-- note:end t-013 -->

## t-014 — Comic Studio page composer (kind_robots, admin)

<!-- note:begin t-014 -->
Issues as ordered pages built from panel segments: layout templates, drag to reorder pages and panels, move panels between pages, split/merge cells, assign any vetted attempt as panel art, captions and dialogue as data. Each panel is a studio slot with its own prompt, lanes and history. The pure layout engine (utils/comicLayouts.ts) is shared with t-004.
Built in kind_robots PR #3208 (schema-affecting, additive). Live only after the Alexandria deploy runs migration 20261003120000_add_comic_studio.
kind_robots#3208 merged (squash 3e8ce36). Schema-affecting: live only after the Alexandria deploy runs migration 20261003120000_add_comic_studio; then seed with scripts/import_comic_studio.py --live.
<!-- note:end t-014 -->

## t-015 — Character 360 spinner: 8 consistent angles per approved design (Flux Kontext)

<!-- note:begin t-015 -->
Silas chose sheets first, angles later. Once he selects a Zuzu and a fennec design in the studio, render 8 angles from the approved front view through the kontext lane and show them as a draggable 360 spinner on the entity. Waits on his design pick.
FOR SILAS: t-013 is done, so this waits only on your pick. In the Comic Studio (once deployed), mark one Zuzu design and one fennec-siblings design as final, and an agent renders the 8 Kontext angles from them. Until then, round 3's Z-Image Turbo sheets are the strongest candidates (see the round-3 contact sheet).
2026-10-04: with Arthemy chosen as the house checkpoint, the design candidates now come from round 5 (ART-ROUND-5.yaml, t-021): every Book One character in Arthemy. Silas picks one design per character from those sheets; the 8-angle renders and the LoRAs (t-016) follow.
2026-10-04: Silas picked designs (CAST-PICKS.md, t-021), so this is agent work now. Render the 8 Kontext angles from each picked front view: Zuzu Z2 (ArtImage 241873), the toddler T2 (241883), the coyote C1 (241888), the otter nuns N2 (241895). The sister waits on a standalone pick. Needs the Zuzu series in the Comic Studio first (t-022).
2026-10-05: the sister is S2 (ArtImage 241879); add her to the angle list. Zuzu's angles wait for his round-6 pick (poncho and kasa); the toddler, coyote and nuns can go now.
2026-10-05 Silas: Zuzu is R6 (ArtImage 241913). His 8 Kontext angles are queued from R6 (ANGLES-ZUZU.yaml, ArtJobs 33554-33561), plus Arthemy R6 turnarounds that keep the katana in back views (ART-ROUND-7.yaml, 33549-33553). Sister, toddler, coyote and nuns follow the same recipe once Zuzu's angles come back clean.
2026-10-05 agent: repaired lost claim (status claimed with null claimed_by/claimed_at); Zuzu angle jobs 33554-33561 are queued, remaining characters follow.
2026-10-05: round 10 delivered the eight-angle sets for Zuzu, the sister, the toddler, the coyote and the abbess in Silas's approved look (picks in CAST-PICKS.md). Remaining: the coyote's right-hand stump edit (retrying) and Silas's verdict on the sets; then the sets feed the LoRAs (t-016).
2026-10-05 agent: repaired a second lost claim (status claimed with null claimed_by/claimed_at); still awaiting the coyote stump retry and Silas's verdict on the sets.
Done 2026-10-07. All five eight-angle sets are locked (Zuzu, the sister, the toddler, the coyote with both right-hip stump states, the abbess variant B), recorded in CAST- PICKS.md and imported into the Comic Studio as cast-* slots with final picks (model sheets in the Cast tab, kind_robots#3271). Silas reviewed the final cast sheet and moved on to the LoRA sets ("go ahead with the LoRA sets").
<!-- note:end t-015 -->

## t-016 — Character LoRA datasets for Zuzu and the fennec siblings

<!-- note:begin t-016 -->
Silas, 2026-10-03, "later maybe we can make a lora". Dataset from the t-015 angles plus emotion sheets (views x poses x expressions, per the PortOS character LoRA plan in docs/inspiration.md), captions, trigger word; training through the lora-ingestion / model-builder path.
Silas approved 2026-10-07 ("go ahead with the LoRA sets"; trainer: kohya sd-scripts). No trainer exists in Conductor or KR, so agents build the datasets (scripts/build_lora_dataset.py + LORA-SETS.yaml) and Silas runs train.ps1 on the box; finished LoRAs land in Lora/import for lora_import_agent. Setup and testing: projects/comic-creator/docs/lora-training.md.
Reset stale claimed (null claimed_by/at) back to ready: lost close-out write, per check_recurring_claim_drift.
2026-10-07: ready -> waiting. t-015 (the angle sets) is still open, and the roadmap audit refuses a ready task with unmet dependencies; the resolver promotes this to ready when t-015 closes. Silas's approval stands.
All five datasets built and sent to Silas 2026-10-07 (zuzukoala, zkasister, zkatoddler 17 images; zkacoyote 19 with both stump states; zkaabbess 17). Expression retries: coyote surprised 243052, abbess surprised 243053. Remaining: Silas sets up kohya sd- scripts on the box and runs each train.ps1 (docs/lora-training.md); finished LoRAs land in Lora/import for lora_import_agent. Known nit: abbess profile-left (m242561) carries a small teal ground strip.
Soft access gate (not a decision): Silas already approved; the only remaining step is running train.ps1 on the render box, which agents cannot reach. Nothing else waits on it.
2026-10-08: Silas asked whether he is needed; yes, once. build_lora_dataset.py now writes train_all.ps1 (one overnight paste: setup, relay paused, all five sets, relay restarted). Sent to Silas.
Silas 2026-10-10 in session: train_all.ps1 is on his todo for tonight (runs overnight when he goes to bed). Stays needs-human until the LoRAs land in Lora/import.
2026-10-11: done. Silas trained all five sets on Ferngrotto (train_all.ps1, CUDA, ~1 h each); registered as private KR LoRA resources 4571-4595. Tested (LORA-TEST.yaml, jobs 36909-36942): final epoch is the pick for all five and four hold their locked design; the coyote LoRA ignores the stump, follow-up t-023. Picks and verdicts in issues/zuzu- koala-assassin-01/CAST-PICKS.md.
<!-- note:end t-016 -->

## t-017 — Adversarial editor in the Comic Studio (kind_robots, admin)

<!-- note:begin t-017 -->
Silas, 2026-10-03: "I need an adversarial editor. If I am proposing an idea, they need to only accept something if it is GREAT... a challenging muse that will actually test the ideas we are presenting. that should be both front and center on the comic editing page, and have a voice with anything that develops that relates to plot, character, theme, etc." Built as the editor desk at the top of /play/comics/studio: Claude judges pitches, series notes, entities, subjects and issues against the series notes (great / close / not-yet / reject with problems, questions, the bar and strengths), threads replies, and speaks up automatically when notes change substantially (toggleable). Secret-until entities reach it marked as secrets. Needs ANTHROPIC_API_KEY on the Kind Robots server. Built in kind_robots PR #3208 (schema-affecting, additive: ComicCritique).
kind_robots#3208 merged (squash 3e8ce36). Schema-affecting: live only after the Alexandria deploy runs migration 20261003120000_add_comic_studio; then seed with scripts/import_comic_studio.py --live.
<!-- note:end t-017 -->

## t-018 — Checkpoint bake-off: furrytoonmix vs its V3B update and five lookalikes

<!-- note:begin t-018 -->
FOR SILAS: download the six checkpoints listed in docs/checkpoints.md into ComfyUI models/checkpoints/Illustrious/ under the file names in issues/zuzu-koala-assassin-01/ART-ROUND-4.yaml, then say so (or flip this to ready). Silas, 2026-10-03: furrytoonmix is "hands down the best model for this project"; find updates and about five lookalikes, "work done finding the right checkpoint should pay off dividends down the road". Agent work once the files exist: run scripts/enqueue_art_requests.py on ART-ROUND-4.yaml (--live, then --status; 42 private jobs, identical prompts, family profile), publish a contact sheet (rows = subjects, columns = checkpoints), then a second pass with author settings (euler_ancestral, cfg 4-5) on the best two, and add the winners as Comic Studio lanes.
2026-10-04: four of six files in place and visible to ComfyUI; 30 jobs submitted (33458-33487: furrytoonmix V3 control plus Nova Furry B, Nova Comic, Arthemy Western, AnthroBlend). V3B and Mol_Keun downloads came back empty; Silas is re-downloading with curl and an API key. Their lanes run when the files land.
2026-10-04 (agent sweep): recurring-claim drift repaired — claim fields were already null while status stayed claimed. Parked as soft needs-human (gate_reason physical- access): waiting on Silas to land the V3B and Mol_Keun checkpoint files; the 30 submitted jobs need no further action.
2026-10-04 round 4 done (30/30, ArtImages 241823-241852, all private, nothing withheld). Contact sheet: https://claude.ai/artifact/QRRDHtVxaCWYEmN69sU8iE. Read: furrytoonmix V3 stays the house (widest expression range, only true turnaround). Best challengers Nova Comic XL v2.0 (grittiest, closest to mature Leone) and Arthemy Western v3.0 (best light, sister attitude); AnthroBlend v3.0 has the best koala anatomy but narrow range; Nova Furry B weakest (near-identical faces). Shared misses across all five are prompt problems, not checkpoint ones: koala/komodo bleed (no komodo dragon anywhere; render the dragon solo) and no otters at the gate (needs a reference sheet then LoRA/IP-Adapter). Next: V3B + Mol_Keun lanes once Silas's downloads verify, then an author-settings pass (euler_ancestral, cfg 4-5) on Nova Comic and Arthemy Western.
2026-10-04 (agent sweep 2): status was still claimed with null claim fields after the #5555 results note; set to needs-human (soft gate, physical-access): waiting on Silas to land the V3B and Mol_Keun checkpoint files.
2026-10-04 round 4 extended with furrytoonmix V3B and Mol_Keun DeepCobalt V2 (ArtJobs 33488-33499, ArtImages 241853-241864, all private). Sheet republished at the same URL. V3B: strongest acting of the round and the only checkpoint to draw Zuzu's canon ear notch and scar, but it dropped his clothes on two of three turnaround views (ArtImage 241853, private, withheld from the sheet). Real house contender pending a clothing- weighted retest (clothed in the prompt, nude in the negative). Mol_Keun: best huddled- siblings mood and fullest costume, but Zuzu reads as a bear and its Komodo became an upright lizard swordsman. House stays V3 until Silas decides; next pass is a V3B clothing retest plus author settings on V3B and Nova Comic.
2026-10-04 round 4b, V3B clothing retest (ART-ROUND-4B.yaml, ArtJobs 33500-33506, ArtImages 241865-241871, all private, nothing withheld). Weighted clothing tags up front plus a hardened negative: 6 of 6 full-body frames dressed (4 turnarounds = 12 views, 2 walks), so the round-4 nudity failure is fixed by prompt. Side effects: a skull-and- crossbones crest on two cloak backs (straw hat + red band pulls in One Piece; negate skull/jolly roger/emblem/logo, describe the hat as plain); back-angle walks drifted to a dog snout and invented koala children; the emotion sheet lost range (two similar sneers) when the outfit was enumerated. Recommendation: V3B is viable as the house checkpoint if full-body prompts carry the clothing block and headshots carry only the hardened negative. House switch is Silas's call; sheet section: https://claude.ai/artifact/QRRDHtVxaCWYEmN69sU8iE#round-4b.
2026-10-04 Silas: Arthemy Western Art v3.0 stands out as the strongest checkpoint for him (house switch not yet decided). All 97 bake-off renders (rounds 3, 4, 4b) are in one viewer with a sheet per checkpoint: https://claude.ai/artifact/5noUSSzS6Avkxe3mAESuA9. Building it surfaced three more undressed round-3 frames from furrytoonmix V3 (241681 Zuzu in underwear, 241683 the sister unclothed in one view, 241725 Zuzu unclothed); round 3 was submitted is_public: true, so all three were set private on Kind Robots and are withheld from the viewer. Clothing drift is not unique to V3B. The rest of round 3 is still public, including the twist subjects. New canon from Silas the same day: Zuzu is koala-sized or a little bigger, Danny DeVito build (SERIES-BIBLE, BRAINSTORM-ROUND-3 decisions, VIDEO-GUARDRAILS).
2026-10-04 DECIDED by Silas: "arthemy is the winner." Arthemy Western Art v3.0 becomes the Zuzu house checkpoint (docs/checkpoints.md; Kind Robots lane change is t-022). The tier list put Arthemy first for tone, a naturally stocky Zuzu and no withheld frames; V3B, V3, Nova Comic and Z-Image (for sets) were next.
<!-- note:end t-018 -->

## t-019 — Video guardrails: Zuzu intro (music-video t-024) and Issue 1 film (comic-film)

<!-- note:begin t-019 -->
Silas, 2026-10-04: Zuzu gets an intro music video (music-video t-024..t-029) and an animated film of issue 1 (new project comic-film). issues/zuzu-koala-assassin-01/VIDEO-GUARDRAILS.md records what both inherit: the house lane for stills, vetted attempts as character keyframes, canon rules, the mature rating (Silas, 2026-10-04, correcting a v0 'teen' assumption), and the bannedTerms list that keeps the human-ruins twist out of every prompt. Downstream video tasks copy that list into settings.bannedTerms.
<!-- note:end t-019 -->

## t-021 — Round 5: Book One cast design candidates in Arthemy

<!-- note:begin t-021 -->
ART-ROUND-5.yaml, ArtJobs 33507-33534, private. Every Book One character (Zuzu, the sister, the toddler, the one-eyed coyote, the crocodile, the otter nuns) plus a size lineup and the chapter 11 road image, in two Arthemy lanes: round-4 settings and the author's (Euler a, 30 steps, CFG 5). Next: per-character sheets for Silas, who picks final designs for t-015.
Re-armed to ready: status was stuck at claimed with null claim fields after PR #5564 merged (claim-drift sweep, 2026-10-04). Remaining: per-character sheets for Silas. 2026-10-04 round 5 done: 28/28, ArtImages 241872-241899, all private, nothing withheld. Single characters now work in Arthemy: Zuzu stocky and koala-sized and dressed in every view; the sister, toddler, one-eyed coyote, crocodile and otter nuns (otters at last, alone in their prompt) are consistent across views. Multi-character scenes still fail on relative size (the sister came out shorter than Zuzu; Zuzu became a fox once; the road drew him tall), so page art needs the character LoRAs (t-016) or composited panels. Costume notes: 'cloth sash' became an orange sash everywhere and the grey cloak comes and goes. Seven cast sheets with pick codes sent to Silas. FOR SILAS: reply with one pick code per character (Zuzu Z1-Z6, sister S1-S4, toddler T1-T4, coyote C1-C4, croc K1-K2, nuns N1-N4); those designs feed t-015's angle renders.
2026-10-04 DECIDED by Silas: "zuzu z2, z6 todler t2 t4, coyote c1, crocodile k2, nuns n2, x2 x4". Recorded with ArtImage ids in issues/zuzu-koala-assassin-01/CAST-PICKS.md. Seven of nine picks used the author's settings (Euler a, 30 steps, CFG 5, style tags). Still open: a standalone sister pick (T4 shows her best), and whether Zuzu keeps the grey road-cloak (Z2 has none).
2026-10-05 Silas: "Sister s2. Yes on house settings." Zuzu keeps Z2 with a poncho (Eastwood callback) and a kasa (sandogasa-style wide straw hat that shades his eyes). Round 6 (ART-ROUND-6.yaml, ArtJobs 33543-33548) renders the redesign for a final Zuzu pick.
2026-10-05: the coyote loses a hand to the croc in chapter 1 and returns later as an ally, so his design needs a bandaged-stump variant next to C1.
2026-10-05 Silas: the coyote loses his RIGHT (gun) hand. Stump variant is the bandaged right wrist. Later books: he fails to shoot left-handed, then gets a knife lashed to the stump.
<!-- note:end t-021 -->
