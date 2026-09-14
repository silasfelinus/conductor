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
