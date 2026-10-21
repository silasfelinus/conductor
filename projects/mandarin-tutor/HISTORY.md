# mandarin-tutor — task history archive

Full `note:` prose for completed mandarin-tutor tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Build the Mandarin Tutor web MVP with 500+ beginner cards

<!-- note:begin t-001 -->
Ship the Play > Mandarin route, Pinia-owned study state, searchable/catalog study sets, a flashcard interaction that can reveal Hanzi, pinyin, meaning, components, and history, and a versioned starter catalog of at least 500 useful beginner lexical or component cards. Keep lexicon facts separate from learner state and generated-media state so the same curriculum can later back native clients. PR #2083 already covers this scope -- fix the two failing checks above and repush rather than starting over.


kind_robots PR #2083 final head 8cde56a6b14f0c29e50191cbdaa9650d287bf0bd fixes the fetch/typecheck root cause, adds the requested record -> unbiased Mandarin transcription -> target comparison -> local YIN tone-coach loop, and fixes the shared-component container-width layout contract. TypeScript, Layout Contract, Contract Tests (all 298 steps), and every other final-head workflow completed successfully; PR is mergeable with no unresolved review threads.

Merged kind_robots PR #2083 as c4b37e0a6a2f5c27b1cb65da13828bfc50966dc0 after final-head TypeScript, Layout Contract, Contract Tests (all 298 steps), and every other workflow completed successfully. MVP includes 500+ sourced beginner cards, curated/custom sets, browser reference pronunciation, microphone recording, target-blind Mandarin transcription, independent target comparison, local YIN tone-shape coaching, and durable Krea2 ArtJobs. Durable cached per-word reference audio remains t-004.
<!-- note:end t-001 -->

## t-002 — Confirm Mandarin Tutor learning priorities with Silas

<!-- note:begin t-002 -->
FOR SILAS: soft checkpoint only; implementation is not blocked. Redirect the balance among reading, speaking, handwriting, character history, or test preparation after the first study loop is usable. Current scope deliberately prioritizes recognition, pronunciation, decomposition, etymology, and practical vocabulary.


Closed under Silas's 2026-09-07 human-gate simplification instruction. The current learning balance is accepted as the default: recognition/reading, pronunciation, decomposition/character history, and practical vocabulary remain the priority; handwriting and test-prep specialization can evolve from usage rather than block the project behind a standing preference checkpoint.
<!-- note:end t-002 -->

## t-003 — Integrate source-backed character decomposition and historical forms

<!-- note:begin t-003 -->
DONE 2026-08-25. kind_robots PR #2085 merged (a953c4b) with all 37 checks green: sourced per-character decomposition/formation data from pinned Make Me a Hanzi dictionary.txt (LGPL-3.0-or-later, dictionary.txt only, not graphics.txt/SVG), distinguishing pictophonetic semantic/phonetic roles from dictionary radicals, preserving unresolved IDS components as uncertainty rather than invented etymology, and scoping formation notes per-character within multi-character words. (A concurrent task-events "review" transition landed on main after this close-out branched; superseded here since the implementation PR was already verified merged before this done transition was written.)
<!-- note:end t-003 -->

## t-004 — Add pronunciation playback and durable per-word audio

<!-- note:begin t-004 -->
DONE 2026-08-25. kind_robots PR #2084 merged (06942c2) with all checks green, including a line-by-line-audited additive-only migration (CREATE TABLE MandarinAudioAsset, one index, no DROP/ALTER of existing tables): deterministic SHA-256 asset identity over recipe version + provider + pinned model/voice/format + Hanzi + pinyin, lazy first-use synthesis via the pinned gpt-4o-mini-tts-2025-12-15 snapshot, immutable MP3 storage reused across web/iOS/Android, mana-gated generation with cache hits never re-charging, and browser SpeechSynthesis retained only as a Safari/iOS delayed-playback fallback. (A concurrent task-events "review" transition landed on main after this close-out branched; superseded here since the implementation PR was already verified merged before this done transition was written.)
<!-- note:end t-004 -->

## t-005 — Connect requested words and missing illustrations to durable Krea 2 ArtJobs

<!-- note:begin t-005 -->
A requested word should become a structured translation/learning card and enqueue one appropriate image through the existing /api/art/enqueue Krea 2 path. Tag jobs with deterministic Mandarin-card provenance, dedupe retries, and attach completed ArtImages back to cards without browser-owned rendering. Abstract components may intentionally remain text/glyph-only where an illustration would add noise.


Build durable requested-word cards using the shared Kind Robots text-provider service, keep generated linguistic fields explicitly marked as generated, reuse existing Mandarin character enrichment when available, enqueue missing concept art through /api/art/enqueue Krea2 with deterministic provenance/dedupe, and persist card-to-ArtImage linkage server-side rather than in browser-only state.

Requested-word implementation is complete on a fresh current-main branch: durable user-owned generated cards with provider/model provenance, sourced character enrichment, reusable Mandarin audio, Krea2 ArtJobs with server-side reconciliation/retry, and a learner-facing create-from-search flow. Preparing the implementation PR for full CI review.

Merged kind_robots PR #2089 as cecacf722bdda79234029c4ff7e3bf05cbd0f1a2 after TypeScript, the full Contract Tests suite, schema parity, and the production-container build all passed. Requested Mandarin words are now durable user-owned cards with generated-field provenance, sourced character enrichment, durable reference audio, Krea2 ArtJobs, retry/reconciliation, and the learner-facing create-from-search flow.
<!-- note:end t-005 -->

## t-006 — Build broad beginner categories and custom study sets

<!-- note:begin t-006 -->
Cover the ordinary beginner flashcard universe: numbers, colors, animals, family, people, body, food/drink, home, school, work, travel/transport, places, weather, time, dates, directions, clothing, shopping/money, common verbs, adjectives, question words, greetings, and high-frequency function words. Cards may belong to multiple sets. Users can create, rename, and study custom sets without duplicating lexical facts.


Expanded the learner-facing beginner deck taxonomy across people, body/health, home, school, work, travel/transport, places, weather/seasons, directions, clothing, shopping/money, descriptions/adjectives, and broader practical vocabulary while preserving shared canonical cards across sets. Added a persisted Pinia rename action and compact inline rename controls for custom decks so names can change without changing deck identity or duplicating lexical facts. Implementation branch is worker/mandarin-t006-categories-sk88.

Broad beginner categories and persisted custom-deck renaming shipped in kind_robots PR #2097, squash merge 513ee2d3950bb5ae9761988211315092d997eef6. The final head passed TypeScript, Layout Contract, Schema Migration Parity, Project Architecture, Contract Tests including the channel artwork audit, and all other head workflows. Cards remain canonical shared records across sets; renaming changes only the stable custom deck's display name.
<!-- note:end t-006 -->

## t-007 — Create a practical gambling and casino Mandarin study set

<!-- note:begin t-007 -->
Build a substantial specialist set for casino work: bets/wagers, chips, cash, table and card vocabulary, suits/ranks, dealer/player roles, shuffle/cut/deal actions, odds and payouts, wins/losses/ties, limits, buy-ins/cash-outs, common table instructions, polite customer-facing phrases, and number/money expressions. Include usage notes where casino Mandarin differs from literal dictionary translations.


Reclaiming the abandoned t-007 lease after independently verifying its 2026-08-25T09:35:01Z claimed_at is far beyond Conductor's 90-minute stale-claim TTL. Continue the research-backed practical casino Mandarin curriculum without colliding with a live session.

Practical casino Mandarin curriculum is implemented in kind_robots PR

DONE. Practical casino Mandarin shipped in kind_robots PR
<!-- note:end t-007 -->

## t-008 — Map the curriculum to official Mandarin proficiency tests

<!-- note:begin t-008 -->
Track source/version-specific proficiency metadata rather than baking one exam revision into the product. Build coverage reports for the currently applicable HSK/Chinese proficiency standards: vocabulary, characters, pronunciation/listening, reading, and other tested competencies. Make gaps measurable so future roadmap work can target an actual proficiency level instead of an arbitrary card count.
PR opened: silasfelinus/kind_robots#2117 -- HSK 3.0 coverage report (proficiency standard metadata + pure coverage module + CLI audit script). Live run against production: only HSK levels 1-2 of 7 sourced; levels 3-7 available upstream and named in nextTargets. Watching CI.
DONE: silasfelinus/kind_robots#2117 merged (squash d0354264). Added utils/mandarinProficiencyStandards.ts (HSK 3.0 metadata, 7 official cumulative levels + reference vocabulary sizes) and utils/mandarinProficiencyCoverage.ts (pure coverage computation, sourced-status derived from live cards so it can't drift). CLI wrapper utils/scripts/auditMandarinProficiencyCoverage.ts with a self-test wired into contract- tests.yml and a live mode. Live finding: only HSK levels 1-2 of 7 sourced (1,256 cards); levels 3-7 fully available upstream (2,225/3,197/4,258/5,384/10,993 cumulative entries) and not yet ingested -- concrete next targets for future roadmap work, replacing the arbitrary card-count framing. All 40 kind_robots checks green before merge.
<!-- note:end t-008 -->

## t-009 — Add spaced repetition, mastery history, and study diagnostics

<!-- note:begin t-009 -->
Record card exposure and recall outcomes, schedule review with a simple inspectable spaced-repetition model, and distinguish recognition of meaning, Hanzi, and pronunciation when useful. Preserve exportable learner state so a later mobile client can share progress rather than starting over.

Claim t-009 with an interaction-first sequence based on Silas's approved UX assessment. Establish explicit Study vs Explore modes before persisting SRS/mastery. Study becomes a deliberate recall loop (challenge -> reveal -> pronunciation -> self-rating -> next) with answer-bearing pinyin, art, and history hidden before reveal. Explore keeps search, requested words, decomposition/history, provenance, and deck curation. SRS/mastery history will attach to Study outcomes rather than cementing the current all-purpose page.
IMPLEMENTED 2026-08-26 (conductor scheduled Agent run): established explicit Study vs Explore modes per this note's own sequencing ("modes before persisting SRS/mastery"). Study is a deliberate recall loop (challenge -> reveal -> pronunciation via the existing MandarinVoiceCoach -> self-rating Again/Hard/Good/Easy -> next), with pinyin/illustration/meaning hidden until reveal. Explore is the prior all-purpose page, unchanged. Self-ratings are logged client-side only (studySessionLog, in-memory, not persisted server-side) -- durable SRS scheduling and mastery-history persistence is filed as its own follow-up, t-015, since it is genuinely separable scope this note itself called out. See silasfelinus/kind_robots#2118 for the full diff and verification (eslint, vue-tsc, layout-contract, existing mandarin self-tests all clean).
RECONCILED (conductor scheduled Agent run, 2026-08-26): implementation PR silasfelinus/kind_robots#2118 merged (Study/Explore mode split, self-rating loop, all CI green). Follow-up conductor PR #2896 (roadmap status -> review, filed t-015 for durable SRS/mastery persistence) also merged. Flipping to done -- t-009s own scope (modes before persistence) is fully delivered; t-015 tracks the deferred persistence half.
<!-- note:end t-009 -->

## t-010 — Reach and audit Krea 2 illustration coverage across the core catalog

<!-- note:begin t-010 -->
FOR SILAS: nothing to decide here yet -- this gate is waiting on the production render host in t-020. Reopen the coverage audit once the box renders again.
2026-08-28: the corpus IS submitted. All 577 illustrate cards are durable ArtJobs (ids 10291-10867, one per request, recorded as last_art_job_id in projects/art-prompts.yaml). Measured coverage immediately before submission was 0/577 -- every sampled v2 media path answers 200 text/html, which is Nuxt's catch-all page, not an image.
Two blockers were found and cleared, neither of which was the container update this task had been waiting on since 2026-08-25 (production has served the v2 manifest since before this session):
1. The v2 prompts could never be enqueued. All 577 came back HTTP 422 from the art
   prompt contract's conditional-instruction rule -- "ground it in Chinese detail
   only when it naturally belongs to the concept". The corpus was unsubmittable by
   construction from the day the recipe was written. Fixed in kind_robots#2174,
   which also adds the recipe/contract test that was missing.
2. probeCanonicalIllustration treated Nuxt's 200 text/html as a hit, so every
   unrendered card reported V2 READY, painted a broken img, and hid the request
   button. Also fixed in kind_robots#2174.

Remaining gate is the render host, not this task's design: Alexandria's ComfyUI has lost sight of its model directory (VAELoader.vae_name='qwen_image_vae.safetensors' not in the live model list) and has rendered nothing since 2026-08-27T09:04Z. See t-020. Coverage cannot be audited until the box renders again; the recovery path is scripts/drain_failed_art_backlog.py, which canaries before draining.
HUMAN ANSWER from silasfelinus via Kind Robots. Gate released for the next agent. love the work, this looks very passable. approved
RESOLVED 2026-09-02: Alexandria render host confirmed back UP (scripts/check_render_box.py: 221 renders completed in the last 6h). Ran a direct HEAD- probe coverage audit against the live media origin (https://media.acrocatranch.com) for all 577 strategy:illustrate v2 manifest entries (44 glyph-only excluded, correctly image-less) -- wrote scripts/audit_mandarin_illustration_coverage.py for this, reusable for future re-checks. Result: 577/577 rendered, 0 absent, 0 unknown -- 100% coverage. The 2888-row FAILED backlog documented in t-020's note has already fully drained/rendered (drain_failed_art_backlog.py's dry-run now reports only 16 stragglers, all already rendered, nothing retryable left). Reach is confirmed complete -- do NOT re- run scripts/queue_mandarin_tutor_art.py to double-check this: doing so during this session's audit incorrectly re-staged the entire already-rendered 577-card corpus as 'missing' and would have duplicate-submitted it, because the original request rows are no longer present in art-prompts.yaml (removed by some later step) and the script has no live-media dedup check. Caught before commit, reverted, never pushed. Filed conductor/t-142 to fix that script's dedup logic properly.

Oversight bookkeeping repair by openai-scheduled-20260903T011608Z-roadmap-audit-k4m8. Records the explicit existing human approval already preserved in this task note ("love the work, this looks very passable. approved"); no new product or production permission is inferred.
<!-- note:end t-010 -->

## t-012 — Prepare the Mandarin Tutor domain for iOS and Android clients

<!-- note:begin t-012 -->
Once the web learning loop is stable, document and expose a portable API/domain boundary for catalog, sets, media, and learner progress. Evaluate PWA/native packaging and native iOS/Android clients without forking curriculum logic or media identities.
DOCUMENTED 2026-08-26 in silasfelinus/kind_robots, docs/mandarin-tutor-mobile-domain.md (PR #2120). Audited every /api/mandarin/* endpoint against its auth guard: auth is already portable (requireApiUser resolves JWT bearer/API-key headers, not cookie-only, so a native client authenticates exactly like the web app). Pronunciation audio is already durable and shared (deterministic hash-keyed MandarinAudioAsset served by stable id -- no per-platform re-synthesis). Curriculum/SRS logic (getMandarinCatalog, mandarinSrs.ts) is 100% server-side, so any client is a thin renderer -- no fork risk. One real gap found: customSets and artJobs in mandarinTutorStore are still localStorage-only per the store's own deferred-follow-up comment, so a learner's custom decks/queued art would not follow them to a second device or a native client. Filed t-016 to close it. PWA: already installable site-wide via @vite-pwa/nuxt at zero extra cost for /play/mandarin. Native: recommended path is a thin shell over the existing JSON API, not a parallel Swift/Kotlin rewrite (which would violate the task's own no-fork constraint).
<!-- note:end t-012 -->

## t-013 — Build a Mandarin catalog curation admin

<!-- note:begin t-013 -->
HIGH INTERNAL PRIORITY: take this immediately after the active tutor-facing requested-word work. Add Mandarin to the existing Admin Curation Studio beside Cthulhuquarium and Coloring Book. Admins need a dense browse/search view of canonical cards, sorting/filtering by Hanzi, pinyin, English meaning, HSK/source, category, media coverage, and override state; category editing; source/provenance inspection; and a straightforward submit-change form for meaning, pinyin, traditional form, usage note, and categories. Source datasets remain immutable. Apply changes through one canonical global override per card plus an append-only audit/change trail. Do not create Coloring Book-style editions or parallel copies of the same lexical card merely because it has been corrected. Generated/requested cards may be surfaced for inspection later, but v1 curation should not silently promote user-specific generated facts into the sourced core.


Build the high-priority Mandarin catalog curation admin inside the existing Curation Studio. Keep source data immutable, use one global override per canonical card plus append-only audit history, and deliberately avoid an edition/version proliferation model.

Re-claim the Mandarin catalog curation admin after pass 1 was returned for the layout-contract failure. The implementation branch now replaces viewport grid breakpoints with container-responsive auto-fit grids; TypeScript, Layout, Schema Migration Parity, and all 298 Contract Tests steps are green on the corrected PR head.

Corrected admin pass is ready for review on kind_robots PR #2092. The viewport-grid violation was replaced with container-responsive auto-fit layouts. The corrected head has TypeScript, Layout Contract, Schema Migration Parity, and all 298 Contract Tests steps green. Keep the implementation PR open until the code-only Mandarin v2 art image has been rolled onto Alexandria; #2092 adds MandarinCatalogOverride/MandarinCatalogChange migrations and should be deployed as a separate migration-bearing release rather than accidentally coupling schema changes to the art-manifest rollout.

Mandarin catalog curation admin is merged in kind_robots PR #2092 as 2d299d609bb978ea998966944d52ec4fd8100384. The corrected final head passed TypeScript, Layout Contract, Schema Migration Parity, all Contract Tests, and the production-container build. Source vocabulary remains immutable beneath one canonical override per card plus append-only audit history.
<!-- note:end t-013 -->

## t-014 — PRODUCTION: GET /api/mandarin is 400ing -- the whole catalog is unservable

<!-- note:begin t-014 -->
Found while implementing t-011 (2026-08-25 sweep): `curl https://kindrobots.org/api/mandarin` returns `{"success":false,"statusCode":400,"message":"HSK level 1 source was not an array.","data":null}`, reproduced 4 times over several minutes (not a one-off flake). This is server/utils/mandarinCatalog.ts's `fetchLevel()` failing on the pinned HSK source (raw.githubusercontent.com/jelleverheyen/hsk-vocabulary@a66fd30/wordlists/inclusive/new/1.min.json). The source itself is fine -- fetching that exact URL directly from this sandbox returns valid JSON (a real array) every time. Likely root cause: GitHub serves raw file content with `content-type: text/plain; charset=utf-8` even for a `.json` path (confirmed via `curl -I`), and `fetchLevel()` calls `$fetch<SourceEntry[], string>(url, { retry: 2, timeout: 20_000 })` with no explicit `responseType`/parse override -- if ofetch's content-type sniffing on the production box's ofetch/ nitro version resolves that as text rather than attempting a JSON parse, `$fetch` would return a raw string, `Array.isArray(string)` is false, and that is exactly the error message thrown. Not proven yet -- didn't have a way to reproduce the literal $fetch call outside the Nuxt/Nitro runtime from this sandbox (no live DATABASE_URL, and $fetch is a Nuxt auto-import, not callable from a plain tsx script) -- but it is the leading theory and cheap to test: force `responseType: 'json'` (or parse `response.text()` with `JSON.parse` manually) in `fetchLevel()` and `loadDictionary()` (mandarinCharacterData.ts has the identical pattern against a different raw.githubusercontent.com source and would have the same exposure) and confirm against a live deploy. Until fixed, the Mandarin Tutor page is fully broken for every user -- getMandarinCatalog()/getMandarinSourceCatalog() throw before building sets, cards, or serving anything.
<!-- note:end t-014 -->

## t-015 — Persist study ratings into real spaced-repetition scheduling and mastery history

<!-- note:begin t-015 -->
Follow-up split from t-009 (2026-08-26 conductor scheduled Agent run, silasfelinus/kind_robots#2118): t-009 established explicit Study vs Explore modes and a deliberate recall loop (challenge -> reveal -> pronunciation -> self-rating Again/Hard/Good/Easy -> next), but self-ratings only land in a client-only, in-memory `studySessionLog` on `mandarinTutorStore` -- nothing is persisted server-side and nothing schedules a card's next review. This task is the deferred second half the original note called out ("Establish explicit Study vs Explore modes before persisting SRS/mastery"): design and land the actual spaced-repetition schedule (a simple, inspectable model per t-009's original description -- e.g. Leitner or a basic SM-2 variant, not a black box), a durable mastery-history record per card/user distinguishing recognition of meaning, Hanzi, and pronunciation, and study diagnostics surfaced back to the learner (retention over time, weak cards, due-for-review counts). Preserve exportable learner state so a later mobile client (t-012) can share progress rather than starting over. Needs a schema decision (new Prisma model(s) for review history / scheduling state) -- treat that as part of this task's own scope, not a separate gate, per normal additive-migration rules.
RECONCILED (conductor scheduled Agent run, 2026-08-26): implementation PR silasfelinus/kind_robots#2119 merged. Added MandarinCardProgress + MandarinReviewEvent (additive-only migration 20260826013500_add_mandarin_srs), a standard SM-2 scheduler (server/utils/mandarinSrs.ts, self-tested), POST /api/mandarin/study/rate + GET /api/mandarin/study/progress, and store/UI wiring (due-count/retention badge in Study mode). Migration verified end-to-end against a local MariaDB through the full 63-migration history. The dimension column (always overall this pass) is forward-compat groundwork for decomposed meaning/Hanzi/pronunciation ratings, deliberately not built this pass -- that remains a separate future UX task if wanted. All CI green except Build production image, which was still in_progress after 40+ minutes with every other of 42 checks green; PR mergeable_state read unstable (not blocked), confirming per the t-106/t-124 precedent that this check is not required -- merged past it.
<!-- note:end t-015 -->

## t-016 — Move custom study sets and queued art-job bookkeeping off localStorage-only state

<!-- note:begin t-016 -->
Found while auditing t-012's mobile domain boundary (docs/mandarin-tutor-mobile-domain.md, kind_robots PR #2120). `mandarinTutorStore`'s `customSets` (user-created study-set membership/names) and `artJobs` (queued illustration job IDs) persist to `localStorage` only -- the store's own comment already flags this as deliberately deferred. Everything else a learner accumulates (SRS/mastery state via t-015, requested cards via GET/POST /api/mandarin/requests) is already server-side and follows them across devices; these two do not, and would show up empty on a reinstalled PWA, a second device, or a future native client. Give customSets the same authenticated-backend treatment MandarinCardProgress got in t-015: an additive migration for a MandarinCustomSet-shaped table keyed on userId, GET/POST endpoints under /api/mandarin/sets, and store wiring that treats localStorage as first-load cache/offline fallback rather than the record of truth. artJobs can ride the same migration and endpoints or a lighter sibling table -- small integer job-id map keyed per user/cardKey. This is the concrete blocker for m4's "portable learning state" milestone, not auth, media, or curriculum logic (all three already confirmed portable in t-012's audit). DONE 2026-08-26. Merged silasfelinus/kind_robots#2121 (squash f985143): additive migration 20260826070000_add_mandarin_custom_sets adding MandarinCustomSet (userId+clientId unique, name, cardKeys as serialized JSON per house convention) and MandarinArtJobLink (userId+cardKey unique, jobId), GET/POST /api/mandarin/sets (load, upsert-one-set-by-clientId) and POST /api/mandarin/sets/art-jobs (upsert one card's queued ArtJob id). Store wiring: loadCloudState() runs on initialize(), treats the server as authoritative but keeps and re-pushes any local-only set/link the server doesn't have yet so offline-created data is never silently dropped; createCustomSet/renameCustomSet/ toggleCardInCustomSet/queueIllustration each fire a best-effort persist alongside the existing saveLocalState() call. Verified: installed a local MariaDB and ran `prisma migrate deploy` through the full 74-migration history (clean, no drift for either new table); vue-tsc --noEmit, eslint, prettier --check all clean; test:layout-contract holds; verifyNoPrismaJsonCast passed. All 38 required PR checks green (only the known-flaky non-required "Build production image" job was still in_progress at merge time -- same documented stall pattern as conductor/t-106, t-124, and today's earlier t-015 note; mergeable_state read `unstable`, not `blocked`). m4's "portable learning state" milestone blocker is now resolved -- auth, media, curriculum, SRS/mastery, and customSets/artJobs are all confirmed server-side and cross-device.
<!-- note:end t-016 -->

## t-017 — Add self-test coverage for mandarinTutorStore's cloud-state merge logic

<!-- note:begin t-017 -->
Kaizen from t-016 (2026-08-26, kind_robots PR #2121): `mandarinTutorStore` has no automated test coverage today, unlike `server/utils/mandarinSrs.ts`'s self-test. `loadCloudState`'s merge behavior (server state is authoritative, but any local-only customSet/artJob the server doesn't know about yet is kept and re-pushed rather than dropped) is exactly the kind of logic a future refactor could silently break without a real backend to catch it. Add a lightweight self-test (matching the `verifyMandarinSrs.test.ts` pattern -- pure-function/mockable, no DB needed) covering at minimum: server-only sets/links pass through untouched, local-only entries are preserved and trigger a re-push, and entries present on both sides prefer the server's value.
<!-- note:end t-017 -->

## t-018 — Show a visible confirmation when an illustration is queued on the study card

<!-- note:begin t-018 -->
Kaizen from t-017/mandarin-study-ux-gallery (2026-08-28, kind_robots PR #2171). pages/play/mandarin.vue's queueCurrentIllustration/refreshCurrentIllustration set an `artNotice` ref (e.g. "Illustration queued as ArtJob <id>.") but nothing in the template renders it -- contrast `newSetNotice`, which IS rendered. A user clicking "Request illustration" gets no visible feedback that anything happened. Render `artNotice` the same way `newSetNotice` is rendered (a small transient banner near the study card), and clear it on the same triggers `newSetNotice` clears on, or on a short timeout if none of those apply here. Small, self-contained, reversible.
<!-- note:end t-018 -->

## t-019 — Show a confirmation when "Check art" actually finds the illustration

<!-- note:begin t-019 -->
Kaizen from t-018 (2026-08-28, kind_robots PR #2173). `refreshCurrentIllustration` in pages/play/mandarin.vue clears `artNotice` on start but never sets a success message when the refresh actually finds art (`probeCanonicalIllustration` or `refreshRequestedIllustration`/`refreshIllustration` returning a url) -- a user clicking "Check art" gets the same "nothing visibly happened" gap t-018 just fixed for the queue action. Mirror t-018's `setArtNotice()` pattern: set a short-lived success notice (e.g. "Illustration ready.") when a url comes back, leave it silent when it doesn't (avoids implying failure on a job that's still processing). Small, self-contained, reversible.
<!-- note:end t-019 -->

## t-020 — PRODUCTION: the render host cannot see its models, so no art renders at all

<!-- note:begin t-020 -->
FOR SILAS: only you can fix this one -- it is a production Alexandria/Unraid mount, not code. Every project's art generation is down until it is remounted.
Every COMFY ArtJob fails immediately with:
  ComfyUI has no matching file for: VAELoader.vae_name='qwen_image_vae.safetensors'
  (ComfyUI listed 1 file(s) for that input). Not in the live model list at
  http://127.0.0.1:8188.

The same VAE name rendered successfully as recently as job 10069 at 2026-08-27T09:04Z, so the file is not misnamed -- the render host lost sight of its model directory. ComfyUI reporting exactly one file for that input is the tell: the directory is unmounted or unreadable, not empty.
Nothing has rendered since. This is not specific to Mandarin: it burns every job the queue hands the box, and it was already eating the queue before the Mandarin corpus was submitted into it (the 2026-08-27 backlog fails earlier, at CLIPTextEncode with hostbuf_file_reader_read, which is the same story one node upstream).
As of 2026-08-28T09:20Z the queue has fully drained and all 577 Mandarin jobs are FAILED at attempts=3 with this error (sampled 15 across the range, all identical). The requests and their job ids survive in projects/art-prompts.yaml, so nothing is lost -- but requeueing is now a REQUIRED step after the mount is fixed, not an optional one. The corpus will not render on its own.
Once the mount is back, requeue with `python scripts/drain_failed_art_backlog.py` rather than the bare reenqueue endpoint -- it renders a canary first and refuses to drain into a host that is still down, which is what keeps 500+ jobs from burning three attempts each and flushing the original error text.
UPDATE 2026-08-28T14:10Z (Silas asked whether the network was back and whether the failures could be requeued): still down, and the backlog is now much bigger than the 577 recorded above.
The ComfyUI *link* is healthy -- the Silas-PC relay is heartbeating every few seconds (agent version conductor-relay-completion-proof-v1, supportsInputImages true, both engines) and ComfyUI answers on 127.0.0.1:8188 well enough to return a model list. What is still broken is the model share behind it. Both of this incident's error signatures are documented in ops/home-server/README.md as the Alexandria SMB mount dropping: the 2026-08-27 rows fail at CLIPTextEncode with hostbuf_file_reader_read (a read against a dead session), the 2026-08-28 rows fail at VAELoader with a shrunken model list (folder_paths re-enumerated a half-readable share). Same outage, two faces. This is the third recurrence of the same mount.
Current state at 14:10Z: FAILED 2888, PENDING 0, RUNNING 0, DONE 5495. Zero ArtImages created in 24h. scripts/check_render_box.py now correctly returns DOWN ("2095 render(s) failed and none completed in the last 6h"), so auto-art-generate will gate itself off on its next run -- it was returning UP throughout the burn, which is why enqueueing continued.
The 2888 are NOT 2888 distinct requests. They are 709 distinct targets; 2173 rows (75%) are duplicate enqueues of the same work, most targets appearing 4-5 times. Cause filed as conductor/t-133 -- auto-art-generate drains art-prompts.yaml twice per run through two lanes that do not mark rows in-flight, so a run against a dead box re-submits the whole corpus. conductor/t-134 covers why the relay's own model-share gate did not stop it (its probe passes on a share that can list one file).
Note that duplicate rows are NOT duplicate renders: the relay claims one job at a time throughout, and RUNNING never exceeded 1 in any sample. ArtJob 12921 did hold RUNNING for 15m01s (13:50:33Z-14:05:34Z, exactly STALE_CLAIM_MINUTES) while 36 other jobs claimed and failed past it at ~10s each -- a stale claim overlapping the normal serial queue, which is what makes a dashboard look like two jobs are running at once. staleRunningCount distinguishes the two.
NOT requeued this session, deliberately: drain_failed_art_backlog.py's dry run classifies all 2888 as retryable render-host faults (2716 render-host-model-vanished, 172 render-host-io) with zero payload faults, so nothing is lost and nothing needs repair -- but firing them at a host that still cannot see its VAE would burn 8664 render attempts and flush the error text this diagnosis rests on. Requeue is a post-fix step, unchanged from above.
HUMAN ANSWER from silasfelinus via Kind Robots. Gate released for the next agent. this was a temporary outage, should be fixed
RECOVERY CONFIRMED 2026-09-02: scripts/check_render_box.py reports UP (221 renders completed in the last 6h) -- the Alexandria SMB mount is readable again. scripts/drain_failed_art_backlog.py's dry-run classifies the remaining 16 FAILED rows as already-rendered (target image exists), zero retryable-and-still-wanted -- confirms Mandarin's 577-card v2 corpus and the wider backlog fully drained with nothing left to requeue (see mandarin-tutor/t-010, closed this session, for the full illustration- coverage confirmation: 577/577 rendered). Root-cause tracking for the duplicate-enqueue amplification during the outage is already closed separately (conductor/t-133, t-134). Per docs/state-reconciliation.md: closing this recovery task now that its explicit recovery criteria are met, not holding it on root-cause completeness.

Oversight bookkeeping repair by openai-scheduled-20260903T011608Z-roadmap-audit-k4m8. Records the explicit existing human gate release already preserved in this task note ("this was a temporary outage, should be fixed") after the documented recovery confirmation; no new production permission is inferred.
<!-- note:end t-020 -->

## t-021 — FOR SILAS: visually accept Mandarin Tutor at phone/tablet/desktop widths to close the project out

<!-- note:begin t-021 -->
FOR SILAS: all 20 roadmap tasks across all four milestones (foundation, depth, curriculum, expansion) are done -- nothing agent-actionable remains in the queue. Reconciled 2026-09-07 (scheduled Agent sweep) per AGENTS.md's rule that a user-facing software project isn't `finished` on task count alone: the live front end must be checked at phone/tablet/desktop widths and you must accept the visual state (or explicitly waive the check) before it flips. What I could verify from this sandbox: `https://kindrobots.org/mandarin-tutor` returns 200 with real SSR markup (confirmed live Mandarin content in the response, not the bare SPA shell). What I could NOT verify: actual layout, spacing, or anything pixel-level at any width -- headless Chromium fails through this sandbox's proxy regardless of target host (documented, unrelated to this project). TO APPROVE: open /mandarin-tutor yourself at phone/tablet/desktop widths. If it looks right, set `approved_by_human: true` and flip project-overrides.yaml's mandarin-tutor entry to `status: finished`. If something needs fixing first, note what and I'll file it as a fresh `ready` task. What unblocks when you do: nothing else is waiting on this -- it's the project's own closing step, and it also clears a currently-failing CI assertion (`test_current_project_lifecycle.py`) that flags any `active` project sitting with zero open tasks.
ACCEPTED BY SILAS, 2026-09-11 (in session): "mandarin is acceptable. layout confirmed good." This is the cross-width visual acceptance this task was holding for, and it closes the project.
What this gate was waiting on, per the 2026-09-07 reconciliation above: a human to look at the live front end at phone, tablet and desktop widths, because AGENTS.md does not let a user-facing software project flip to finished on task count alone. The sandbox could confirm only that https://kindrobots.org/mandarin-tutor returned 200 with real SSR markup rather than a bare SPA shell; it could not judge layout, spacing, or whether the thing is pleasant to use. Silas has now done that and confirmed the layout is good.
Project state at acceptance: 21/21 tasks done across all four milestones (foundation, depth, curriculum, expansion), nothing agent-actionable left in the queue. project-overrides.yaml flips mandarin-tutor to `finished` in the same change, and priority.yaml drops it from the selectable worker queue, since finished projects are historical records rather than pickable work.
NOTE ON THE PRIORITY QUEUE: mandarin-tutor was order[0] in projects/priority.yaml -- Silas's own 2026-08-25 decision to make it the lead project, pinned by tests/test_project_priority_contract.py. Removing it required editing that test, which the test's own docstring says may only be done alongside a named human decision. That decision is this acceptance. Cthulhuquarium, which Silas pinned immediately behind Mandarin Tutor in the same 2026-08-25 call, now leads.
<!-- note:end t-021 -->

## t-022 — Teach the word first: per-word lesson pages with pinyin anatomy, component roles, and phonetic series

<!-- note:begin t-022 -->
The component/etymology data m2 already fetches (Make Me a Hanzi decomposition, etymology.semantic / etymology.phonetic, dictionary radical, IDS leaves) is currently buried behind a `<details>` labelled "Parts & history" that only opens AFTER the learner has been drilled. Silas's request inverts that: instruction first, flashcard second.
Build `utils/mandarinLesson.ts` as a pure derivation over a MandarinCard plus the rest of the catalog, producing: (1) pinyin anatomy per syllable -- initial, final, tone number, tone contour, and the third-tone sandhi already computed by `parsePinyinToneTargets`; (2) per-character component roles saying what each piece CONTRIBUTES (semantic field, sound clue, indexing radical, structural leaf, or explicitly unresolved), reusing the honest "the source makes no claim here" fallbacks `server/utils/mandarinCharacterData.ts` already writes rather than inventing mnemonics; (3) the character's phonetic series -- other catalog cards sharing the same `role: 'phonetic'` glyph, which is the 青 → 请/清/情/晴 relationship Silas actually means; (4) true homophone groups, same pinyin syllable with and without tone, kept visually and structurally distinct from (3); and (5) the existing history string with its source line.
Ship it at `/play/mandarin/learn/<key>`. This requires moving `pages/play/mandarin.vue` to `pages/play/mandarin/index.vue` -- the URL is unchanged, but Nuxt makes a sibling `mandarin.vue` a parent route needing `<NuxtPage />` the moment a `mandarin/` directory exists. `utils/projectPlacements.ts` and `content/channels/plan/mandarin.md` reference the route string, not the file, so neither needs touching.
No schema and no writes in this task -- it is pure derivation plus a read-only page, so it is verifiable by self-test without a database. Gating and points are t-023. Add `utils/scripts/verifyMandarinLesson.test.ts` in the established pure-function style (see verifyMandarinSrs.test.ts) and wire it into contract-tests.yml alongside the other mandarin self-tests.
DONE 2026-09-19. Shipped utils/mandarinLesson.ts (pure lesson derivation: pinyin anatomy per syllable with tone contour and third-tone sandhi; per-character component roles rendered as full sentences that state what a piece does AND what it does not claim; phonetic series built from role:'phonetic' components, with drifted families flagged rather than hidden; true homophone groups split into exact-reading and tone-variant buckets; and a teachability verdict that reports 'vocabulary' instead of padding a bare IDS dump into a fake explanation), the tutorial page at /play/mandarin/learn/<key>, GET /api/mandarin/lessons/[key] (public and cacheable, like GET /api/mandarin), and the required pages/play/mandarin.vue -> pages/play/mandarin/index.vue move plus ?card= deep- link return path. Added MandarinComponent.character (additive, optional) so a multi- character word's pieces attribute to the right character instead of being label-parsed. Verified: vue-tsc exit 0; new test:mandarin-lesson self-test wired into contract- tests.yml, all assertions passing; layout contract holds with no new violations; page- backdrop passed.
<!-- note:end t-022 -->

## t-023 — Soft-gate drilling on comprehension and add the Mandarin point ledger

<!-- note:begin t-023 -->
Silas chose the SOFT gate explicitly: un-lessoned cards sort to the back of the study queue and the study card offers "Learn this first" with a link to t-022's lesson page, but a learner who insists can still drill. Nothing blocks mid-session, and a fresh account must never face an empty deck.
Schema, additive, following every other Mandarin model's established pattern -- plain `userId` scalar, no relation added to the already-crowded User model, no native Json column: `MandarinLessonProgress` (userId, cardKey, viewedAt, completedAt, unique on userId+cardKey) and `MandarinPointEvent` (append-only ledger: userId, cardKey, reason, amount, balanceAfter, refType/refId, mirroring KarmaTransaction's shape) plus `MandarinLearnerProfile` (userId unique, totalPoints, lessonsCompleted, cardsLearned) as the denormalized current-state summary derived from the ledger, exactly as MandarinCardProgress summarizes MandarinReviewEvent.
Silas said the point system "may require a user upgrade to the schema" -- the upgrade belongs in this per-domain profile row, NOT in a new User column. `User` already carries questPoints, karma, mana, tokens and earnedTokens; a sixth global balance for one study surface would be the wrong place, would collide with the kind-economy ledgers, and would not be reversible.
Award rules, per Silas's selection (lesson comprehension + recall, nothing else): points for completing a lesson, and points for a recall rating WEIGHTED BY SRS DIFFICULTY, so re-drilling a card at a long interval earns near zero and genuinely recalling a lapsed card earns a lot. Deliberately NOT in scope: daily streaks, daily point targets, notifications, or any nudge mechanic -- Silas ruled those out by name in the reopening request ("insistent and focused on interactions, notifications, nudges").
DONE 2026-09-19. Shipped the SOFT gate (cards whose lesson has been read sort to the front of the study queue; unread cards sort to the back and carry a 'Learn this one first' prompt, but Reveal answer stays live and the partition is a no-op for a learner with no completed lessons, so a fresh account never faces an empty deck) and the point ledger. server/utils/mandarinPoints.ts is pure and owns all the arithmetic: a lesson read through pays 10 once per card ever (re-completion is idempotent and pays nothing); a recall pays base(rating) x dueFactor x lapseFactor x maturityFactor, with hard > good > easy because effortful recall is where the learning is, and 'again' paying 0 with nothing ever deducted. dueFactor is the anti-grinding rule -- a review is scored against how much of its scheduled interval actually elapsed, computed from the card's state BEFORE the upsert, so re-drilling an easy card pays the 1-point floor while the same card actually due pays full value, and a late review caps at 1 rather than rewarding neglect. Schema is additive and per-domain (MandarinLessonProgress, MandarinPointEvent append-only ledger, MandarinLearnerProfile summary), all on the plain userId ownership scalar: the 'user upgrade' Silas asked about is deliberately NOT a sixth balance column on User alongside questPoints/karma/mana/tokens/earnedTokens. Streaks, daily targets and nudges were ruled out by name and MandarinLearnerProfile carries no streak or last- active field on purpose. Verified: vue-tsc exit 0; new test:mandarin-points self-test wired into contract-tests.yml covering the grinding exploit, the lapsed-card payoff, the neglect cap and clock-skew edges; Replay migrations on MariaDB green in CI against a real database; schema-migration-parity, no-prisma-json-cast and migration-drift-check all green; layout contract holds. NOT verified: no migration applied to any live database from the session, and no live points round trip exercised.
<!-- note:end t-023 -->

## t-024 — Sound-family index: browse the catalog by phonetic series

<!-- note:begin t-024 -->
Once t-022 computes a card's phonetic series, the same derivation supports the inverse view: an index of every sound component in the catalog (兑, 青, 马, 可 ...) with its family underneath, showing how one sound component threads through many characters and where the sound drifted. This is the browsable form of the thing Silas said he REALLY loves about the writing system, and it is the natural entry point for an academic learner who wants to read outward from a component rather than drill a deck.
Keep it honest: only assert a phonetic relationship the pinned Make Me a Hanzi source actually claims (`etymology.phonetic`), never one inferred from a shared-looking shape, and show the modern readings side by side so a drifted family (说 shuō / 税 shuì) reads as the interesting case it is rather than as a data error.

Implemented the browsable phonetic-series index on the Kind Robots worker branch. The page derives families only from source-asserted role: phonetic components, shows modern readings and drift, and links each member to its lesson page.

Reviewer rejection (pass 1, quality): kind_robots#2891 fails layout-contract --
pages/play/mandarin/sound-families.vue renders its own <h1>, violating the one-header
rule. Fix posted on the PR: delete the <h1>, keep the eyebrow/description/badges.
status: ready, passes: 1, retry_context set.

Retry addresses the reviewer layout finding and the subsequent TypeScript route-inference failure on kind_robots#2891; waiting for fresh CI on exact head 1a706fb3414faabb0a59e7bc303302d8882faf8b.

State reconciliation (2026-09-19, Reviewer sweep): kind_robots#2891 was already merged
(all 49 checks green, merged_by silasfelinus) but the roadmap task was still status:
review on main -- flipping to done.
<!-- note:end t-024 -->

## t-025 — Phonetic-series completion bonus

<!-- note:begin t-025 -->
NOT SELECTED BY SILAS. Offered in the 2026-09-19 reopening conversation as a fourth point-earning rule -- a bonus for learning every member of a sound family -- and he selected only "lesson comprehension + recall". The original task deliberately parked this behind t-024 so the idea stayed visible until the sound-family index existed. That dependency is now complete, and leaving the declined option at `waiting` would violate the roadmap dependency contract and retrigger portfolio oversight. Closed as a no-op, not implemented; preserve this note as the historical option and only reopen/create implementation work if Silas explicitly asks for the bonus later.
<!-- note:end t-025 -->

## t-026 — Audit that every catalog card can produce a usable lesson

<!-- note:begin t-026 -->
m2's provenance audit (t-011) checks the catalog's source data. This checks the new teaching layer on top of it: for every card in the live catalog, does t-022's derivation produce a lesson a human could actually learn from -- pinyin anatomy that parses, at least one component with a stated role, a history line that is either a real source claim or an explicit no-claim, and no lesson whose only content is "the source makes no claim".
The last case is the interesting one. A card that decomposes into nothing teachable is not a bug in the derivation, it is a card that should either be enriched from a second source or shown as a vocabulary item rather than a structural lesson. The audit's job is to report how many of those exist and which they are, so the coverage gap is a number Silas can look at instead of something a learner discovers one dead lesson at a time. Follow `auditMandarinCatalog.ts`'s shape: a `--self-test` mode for CI plus a live mode.
<!-- note:end t-026 -->

## t-027 — FOR SILAS: visually accept the COMPREHENSION slice at phone/tablet/desktop widths

<!-- note:begin t-027 -->
FOR SILAS: the selected m5 COMPREHENSION work is implemented: per-word teaching pages, the soft learn-before-drill flow, comprehension + SRS-weighted recall points, the phonetic-series browser, and the lesson-coverage audit. The optional phonetic-series completion bonus was not selected and is closed as a no-op in t-025. This is the same final target-environment visual acceptance gate used for the original m1-m4 closeout: confirm the evolved Mandarin experience at phone, tablet, and desktop widths before m5 and the reopened project are marked finished. No publish, billing, DNS, secret, or destructive production action is attached to this gate.
GATE TRIAGE 2026-09-30 (session 20260930T0600Z-gate-triage, requested by Silas in session): Legitimate: a look/feel or play verdict that only Silas can give.
APPROVED by silasfelinus in session (session 20260930T0600Z-gate-triage, Claude Code, 2026-09-30; recorded under CONTROL.md's human gate clearance rule): The COMPREHENSION slice is accepted at phone/tablet/desktop. The project stays active for t-030 (glyph history).
<!-- note:end t-027 -->

## t-028 — Guided course: an introduction, then one teaching card at a time

<!-- note:begin t-028 -->
Silas, 2026-09-20: "i want a real front end interface. We start, are given an introduction, then shown cards that give info, basically, a streamlined teaching interface. do you grok?"
m5 gave the project a teaching LAYER (t-022's lesson derivation), a reference page for it, and a sound-family browser (t-024). What it did not give is a front door. `/play/mandarin` opened onto a TOOL -- two interaction modes, four workspace views, a deck picker, a gallery -- which is the right shape for someone who already knows what they want and the wrong shape for someone who wants to be taught. A newcomer had to make three choices before the app taught them anything.
Build the guided course as the front door. Silas made two decisions when asked:
  * The guided flow BECOMES `/play/mandarin`; the existing workspace moves to
    `/play/mandarin/browse`, unchanged and one click away, and the start screen also
    points at `/play/mandarin/sound-families`. Nothing is removed -- the deck picker,
    search, gallery, custom sets and free drilling all keep working, they just stop
    being the first thing a newcomer sees. He rejected both alternatives (course on a
    separate route, and replacing the workspace outright).
  * A word's teaching run is FIVE BEATS with empty beats auto-skipped: meet it, how it
    sounds, what each piece does, who shares its sound, recall it. A word whose source
    asserts nothing structural, or that no other catalog card shares a sound component
    with, silently drops those beats rather than showing an empty screen -- padding
    would teach the learner that the course pads, which is exactly what t-022's honesty
    contract exists to avoid. He rejected the always-three-beats and pick-your-depth
    alternatives.

The orientation sequence is the "introduction" he asked for by name, and it should do real work rather than be a welcome mat: the biggest obstacle for an English-speaking beginner is believing characters are pictures of their meanings, and every card after that belief is gone is easier to read. Its last screen should state out loud that nothing here is timed, streaked, or notified -- he asked for something "closer to duolingo" but explicitly not "insistent and focused on interactions, notifications, nudges", and saying so is cheaper than a learner waiting for a nag that never comes.
Three constraints worth stating up front. The course must NOT fetch a lesson per screen: `buildMandarinLesson` is pure and lives in `utils/`, so derive lessons client-side from the already-loaded catalog and keep `GET /api/mandarin/lessons/[key]` for the standalone reference page, which is public, cacheable and server-renderable. The recall beat must advance by rating only -- a card a learner can Continue past without answering is not a recall test. And an already-learned word's run collapses to a single recall beat, which is what turns the course into a review session once a deck is learned instead of making someone re-read a lesson to reach a card they know.
NOTE ON t-027: that human-acceptance gate was written against the m5 slice as it stood on 2026-09-19 and predates this task. Silas should accept the guided course as part of the same visual pass rather than accepting the old front door and then being handed a different one.
DONE 2026-09-20. The guided course is now the front door at /play/mandarin; the workspace moved to /play/mandarin/browse unchanged, with a link back, and the course's start screen also points at t-024's /play/mandarin/sound-families. utils/mandarinCourse.ts (pure) turns a lesson into a sequence -- five beats with empty ones dropped, so a word the source asserts nothing structural about, or with no sound family in the catalog, loses those screens rather than showing them blank. teachability is deliberately NOT the pieces test; having components is. MANDARIN_COURSE_INTRO is the orientation: characters are not pictures (氵+青 -> 清), a tone is a letter of the syllable (ma x4), learn the family not the character (青 -> 请/清/情/晴), and an explicit statement that nothing here is timed, streaked or notified -- a self-test asserts that last line keeps saying it. An already-learned word collapses to a single recall beat, so the course becomes a review session. Progress counts WORDS not steps, so the bar does not lurch on longer runs. The recall beat advances by rating only. Lessons derive client- side via the new store.lessonFor() so no round trip is paid per screen, and store.rateCard() splits rating from cursor-advancing so the course cannot have the deck moved underneath it. Session length is 8 words. Verified: all 51 CI checks green including TypeScript, Contract verifiers, layout-contract and Build production image; new test:mandarin-course wired into contract-tests.yml; no regressions in t-022/t-023/t-026. The ESLint ratchet caught a real unused import mid-review and it was fixed before merge. NOT verified: no browser ran this -- how the course feels at phone/tablet/desktop widths is t-027's gate, which now covers this front door too.
<!-- note:end t-028 -->

## t-029 — Parts first: teach each part's meaning and origin before the word it builds

<!-- note:begin t-029 -->
Silas, 2026-09-29, on the 我 course card ("Its parts don't explain this one — learn it whole"): "If I am learning wo, I should learn how the parts of the symbols mean, and what they used to mean, and how they connect. there is a history for each symbol, and it's VERY important that this is part of the instruction." Then: "we should learn the parts before we learn the combinations" and "I should learn roof before I learn house, for example."
Root cause: the pinned Make Me a Hanzi source DOES analyse 我 -- ideographic, "A hand 扌 holding a weapon 戈" -- but only semantic/phonetic roles counted as teachable, so all 1,840 ideographic entries (我 你 好 休 明 ...) fell through to `form` leaves and the 2026-09-20 的 fix then hid them as "learn it whole". And t-028's pieces beat ran after `meet`, so 家 was shown whole before 宀 roof / 豕 pig.
Implemented in silasfelinus/kind_robots#3097: a new `idea` component role (a leaf only when the source's own hint names it); every meaning/sound/idea part is looked up as a character in its own right and carries its reading, meaning and origin from the source's entry for THAT part (戈 "A spear pointing to the bottom-right"); per-character formations on cards, with a `pictograph` teachability for 人/日-type characters; the course's pieces beat now runs BEFORE meet ("First, the parts"), and meet shows how they combine; orderPartsFirst pulls unlearned catalog words that are parts (日, 月) into the session ahead of the word they build (明) within the 8-word session. Intro card rewritten as "Parts first, then the whole" (宀 + 豕 -> 家). New test:mandarin-parts-first in contract-tests.yml, built on verbatim source lines. NOT verified in a browser -- the visual check folds into t-027's gate.
DONE 2026-09-29: silasfelinus/kind_robots#3097 merged (squash 9f2e2bf) with all 34 checks green, including TypeScript, Contract verifiers (runs the new test:mandarin-parts-first) and Build production image.
<!-- note:end t-029 -->

## t-031 — Remove repetitive per-part 'In the next word' copy

<!-- note:begin t-031 -->
Silas, 2026-09-29, reviewing the new parts-first course card: the repeated per-component helper lines ("In the next word, ...") are redundant beneath the already-labeled Meaning / Sound / Picture part cards. Remove those repeated lines and their unused helper without changing the sourced origin text, component labels, or the top-level explanation that these parts build the next word.

Removed the redundant per-component "In the next word" helper lines and the now-unused helper from the Mandarin course card; preserved the sourced origin text, role labels, and the single top-level parts-first explanation.

DONE 2026-09-29: silasfelinus/kind_robots#3102 merged (squash 1951b614) after all 28 exact-head PR workflows completed successfully. Removed only the repeated per-component "In the next word" helper copy and its unused helper; preserved the sourced origin sentence, component labels, and the single top-level parts explanation.
<!-- note:end t-031 -->
