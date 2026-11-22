# hybridizer — task history archive

Full `note:` prose for completed hybridizer tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-003 — Build art-led one-screen Hybridizer prototype in Kind Robots Admin

<!-- note:begin t-003 -->
First implementation needs full-size concept art slots, two interactive selection trays, fusion animation with reduced-motion alternative, a large hybrid reveal, shared discovery browsing and a real playable flow. Follow Kind Robots Admin route/tab convention, self-hosted UI verification, and project placement sync. Avoid claiming demo art as actual ArtJobs.

Kind Robots PR #4406 merged at 719c1b18c0457202641ba36b4eab939027ff6725. First Admin-only interactive console, 200-starter selection, accessible fusion animation, recursive local studies, visual discovery shelf and known Facet art integration landed. All 15 GitHub CI workflows succeeded, including full TypeScript and four contract shards. Pre-merge rendered frontend geometry unavailable without a deployed build. Global cache, asynchronous ArtJob generation, user submissions and notifications remain distinct uncompleted follow-on tasks.
<!-- note:end t-003 -->

## t-004 — Persist global canonical unordered pairs and recursive fusion provenance

<!-- note:begin t-004 -->
Model deduplicated pair keys on stable input identities, composition revision and model recipe, atomic claim/lookup and failure retry; preserve lineage and make prior hybrids reusable ingredients. Two inputs make 19,900 unique unordered starter pairs, not 4,000. Preserve provenance to prevent cache poison and enforce art visibility.

Durable unordered pair keys, recursive provenance DAG, authenticated public/owner visibility boundaries, global discovery lookup and local fallback added in Kind Robots worker branch. Await full PR checks.

Kind Robots PR #4408 merged at 31b44a1 after 23/23 checks green, including TypeScript, Prisma generated client and migration parity, four contract shards, and Docker production build. Shared fusion cache is on main, additive migration pending self-hosted rollout. Space Couch parser blocker repaired in separate green PR #4415.
<!-- note:end t-004 -->

## t-005 — Connect ArtJob queue, background completion notification and missed-result retry

<!-- note:begin t-005 -->
Existing Krea2/Arthemy queue and ArtImage linkage, idempotent request, bounded concurrency, retained status, polling plus optional in-app notification; never block play or pretend a requested render is complete.

Added Krea2 ArtJob enqueue/retry with scoped generation auth, durable global fusion/job link, bounded concurrency, stable seeds, status reconciliation and background UI completion notices on a Kind Robots worker branch. Preparing focused PR and CI; no jobs have been submitted to production and delivery is not yet verified.

Triage 2026-10-30: kind_robots #4418 merged and is live (production /api/version = main 0bb3088). Enqueue/status routes, server/utils/hybridizerArt.ts, store poll/notice/retry (same-job retry cap 2, 3 active jobs per user) are on main and test:hybridizer-art runs in contract CI. End-to-end delivery is not yet proven (no live fusion exists yet); that smoke test belongs to the t-007 pilot / t-009 QA. The #4408 migration is NOT pending: the compose migrate service runs every deploy and the HybridizerFusion query succeeds in production.
<!-- note:end t-005 -->

## t-006 — Reconcile all 200 input Facets and audit real image availability

<!-- note:begin t-006 -->
Audit existing animal Facets and art paths, resolve duplicates and aliases, create missing reusable Facets with canonical taxonomy. Monster concepts (vampire, zombie, etc.) must be SPECIES. Do not create an invented monster taxonomy; produce traceable ArtJobs for missing art.
2026-10-30 close-out: all 200 starters pinned to one canonical Facet each, 200 unique facetIds. 73 were already pinned. 34 title matches were confirmed as the correct Facets with no duplicates (Cat, Dog, Rabbit, Lion and Mantis Shrimp reuse SPECIES Facets that depict the literal animal). 3 aliases: Kiwi to Facet 243, Shoebill to 352, Hyena to 378. 90 Facets created via POST /api/facets, ids 2981-3070: 59 ANIMAL, 5 SPECIES, 3 ARCHETYPE, 23 OTHER. Ledger: projects/hybridizer/facets/STARTER-FACETS-ROUND-1.yaml. 90 self-hosted Krea 2 ArtJobs queued as 50561-50650 with entity_art onto Facet.imagePath (art/STARTER-INGREDIENTS-ROUND-1.yaml). 69 still-pending jobs were raised from priority 200 to 700 at about 13:47 UTC with the coordinator's approval. All 90 jobs are DONE. Verified on production at 20:40 UTC: 200/200 starters resolve to a Facet with a fetchable image, reviewed on contact sheets as literal and centred with no jars. Game: the store resolves art by facetId and shows an honest art-queued placeholder until delivery (kind_robots #4491, deployed). Follow-up: utils/hybridizer/starterCatalog.json still records artState art-queued for the 90 new starters. This is display-only because the UI shows the image once present; flip them to facet-image in the next catalog touch.
<!-- note:end t-006 -->

## t-007 — Pre-generate and verify curated 4,000 launch hybrids

<!-- note:begin t-007 -->
Bias coverage to strong readable animal x animal and oddball combinations without cross-product explosion; schedule batches with immutable pair keys and explicit art-workflow provenance. Verify each delivered image, not a submitted prompt count. Human-visible progress against 4,000.
2026-10-30 progress: launch pipeline live. kind_robots #4484 (art prompt: the hybrid itself as one blended creature or object on a plain backdrop, no jar/specimen/lab staging; admin POST /api/hybridizer/batch) and #4512 (batch priority 90: behind interactive 100 and project runtime art, ahead of bulk backfill). conductor #6815: deterministic 4,000-pair LAUNCH-PAIRS.json (36-pair showcase first, every starter used 35-75 times) and the 20-minute 'Hybridizer launch batch' workflow, which keeps a 60-render window full and marks a hybrid delivered only after its image URL answers. At close: 96/4,000 submitted, 36 verified delivered (the full showcase, reviewed on a contact sheet; Silas approved the look). The workflow keeps running unattended; reopen to done when the ledger reaches 4,000 verified.

Curation round 1 (2026-11-21 PT). Silas set the acceptance bar this session: "While one pass for quality is warranted, after those are resubmitted, I'm happy as long as we have the hybridized fully working to react and resubmit bad hybrids in game." All 4,000 launch hybrids are rendered and delivered (live status READY for every pair; the ledger lagged by 1,004 because GitHub ran the 20-minute schedule only 3-4 times a day and each run refreshed only 400 entries; the workflow now refreshes every open entry). Every one was reviewed visually on labeled contact sheets: 1,856 FAIL (769 one ingredient only, 567 two separate creatures, 515 missing fruit/object ingredient, 5 other incl. an echidna+ninja IP lookalike), 398 WEAK, 1,746 PASS. Committed as projects/hybridizer/art/CURATION-ROUND-1.json. The launch batch workflow files one admin curation re-render per FAIL (new seed, fused-body guidance, priority 1, up to 1,000 per run), drops the ledger's verifiedAt until the new image answers, and refuses to post until the deployed server advertises the curation contract. kind_robots #5490 adds the in-game "Not a hybrid? Re-roll" for any signed-in player on public discoveries plus admin curation mode, a large phone reveal and requester-only ready toasts. Close as done once #5490 is live and the workflow reports the 1,856 curation resubmits filed; WEAK entries and any disappointing re-renders are handled by in-game re-roll.

Done 2026-11-21 PT against Silas's bar. kind_robots #5490 is live (production
4c22a520+). All 1,856 FAIL pairs have a curation re-render filed: launch-batch runs 87
and 89 recorded 1,002 in the ledger with job IDs; run 88 filed the other 854 but lost
its checkpoint, and every one of those 854 was confirmed QUEUED live under a newer job
(the server's one-revision-at-a-time guard rejected 990 duplicate attempts). The
conductor follow-up makes queued runs start from latest main and adopts already-running
re-renders so none is filed twice. 398 WEAK and any disappointing re-renders are handled
by the in-game re-roll.
<!-- note:end t-007 -->

## t-008 — Accept user-submitted ingredient images securely

<!-- note:begin t-008 -->
Auth/consent, ownership and visibility, allowed content, size and type validation, abuse controls, safety review, provenance and rights; user art must not silently become a public reusable input.

Silas, 2026-11-21 PT: "Just build the upload option." Implemented in kind_robots #5493: signed-in players add their own picture as a private ingredient (name, optional description for the illustrator, creature/object, explicit rights and consent checkbox). Never public: private non-mature ArtImage owned by the uploader, no listing or sharing route, upload:<id> keys resolve only for the active owner through one shared resolver used by fusion creation, first render and revisions, and any fusion using an upload inherits isPublic=false. Magic-byte sniffing (client MIME ignored), 5 MB and 128-6000 px bounds, full sharp decode and WebP re-encode that strips EXIF/GPS (verified 0 EXIF bytes from a GPS-tagged JPEG), 10/day and 30-active limits, plain-text name/description that pass the art prompt contract, remove deactivates the ingredient and its image. Additive HybridizerUpload migration. Contract tests, vue-tsc and Prettier pass locally. Close as done when #5493 merges green; live behaviour is rechecked with t-009's post-deploy 390/768/1440 pass.

Merged green as kind_robots #5493 and live on production (b7a1821c, 2026-11-21 PT):
signed-out GET and POST /api/hybridizer/uploads return 401; the signed-out drawer shows
the sign-in-to-upload link and the MINE filter.
<!-- note:end t-008 -->

## t-009 — Adversarial QA, full-width layout review and final subjective acceptance

<!-- note:begin t-009 -->
Test cache races, A+B equivalence B+A, recursive lineage, unavailable artwork, auth, private uploads, failed/retried jobs, stale notifications, reduced motion, 390/768/1440/XL UI; no fake image completeness. Move to final human design verdict only after all agent work clears.

Adversarial privacy audit found cross-account persistence of remote private discovery metadata. Scoped QA patch isolates offline drafts by authenticated user, discards legacy unscoped cached discoveries, rejects stale async session responses, and hides sharing/reactions for private discoveries. Further upload/production/art coverage and rendered viewport checks remain before final acceptance.

Adversarial privacy QA slice merged in kind_robots PR #4565 as aa72390c0790c79e1dda6f8caf8df1251d6249fb after all 18 GitHub workflow runs completed successfully (including TypeScript, contract shards, formatting, layout and content visibility). Fixes unscoped localStorage leakage of private server discoveries, scopes offline studies to authenticated user, guards cross-account stale async responses, and hides sharing/reactions for private fusions. Test assertions added. This is NOT completion of t-009: t-008 private custom uploads are still unimplemented, t-007 artwork is incomplete, and remaining auth/cache/job adversity plus rendered 390/768/1440/XL acceptance checks must be done before final human design verdict. No public-release approval.

2026-11-02 PT: Scoped atlas/remix QA implementation is in progress. Correct global discovery totals, image status visibility, browsable saved hybrids, and custom-weight revisions. t-009 remains open after this slice for the larger adversarial and cross-width acceptance campaign.

Scoped atlas/remix implementation in Kind Robots PR #4643. Data-backed atlas totals and pagination, reused-art badge, saved-hybrid gallery with rating and versions, editable-weight prompt resubmission. TypeScript, formatting, layout, visibility, architecture, migration, and other completed workflows green; four Contract Tests shards green. Auto-merge enabled after the queued Contract verifiers aggregator finishes. Not live until Unraid container deploy. Keep t-009 open for remaining private-upload coverage, adversarial art QA and rendered 390/768/1440/XL acceptance.

2026-11-21 PT rendered check of production /play/hybridizer (commit 0d422b75) at 390, 768 and 1440: no horizontal overflow, 30/30 images loaded, 0 broken. Found and fixed in kind_robots #5490: at <=820px container width the discovery reveal collapsed to a ~30px thumbnail and its actions were clipped (console now scrolls, reveal clamps 220-460px; verified by injecting the CSS on production at 390/768), and signed-out visitors received "X is illustrated!" toasts for shared launch renders they never requested (now only fusions, retries, remixes and re-rolls the player requested). Community re-roll adversarial contracts: injected direction/weight ignored, no escalation to curation, private discoveries stay creator-only. Remaining before handoff: t-008 private uploads (unbuilt) and a post-deploy recheck at 390/768/1440.

Agent QA complete 2026-11-21 PT on production b7a1821c (includes #5490 and #5493):
390/768/1440 no horizontal overflow, 0 broken images, reveal 326x256 / 678x460 / 531x373
(was a ~30px thumbnail on phones), no ready toasts for signed-out visitors, upload
endpoints 401 when signed out. Contract coverage: community re-roll cannot inject prompt
text or escalate to curation; private discoveries and uploads are owner-only; uploads
sniffed by magic bytes, re-encoded without EXIF/GPS, rate-limited. The subjective
fun/design verdict moves to human playtesting after handoff (GAME-PLAYTEST-
CLOSEOUT-2026-11-18), not this finite task.
<!-- note:end t-009 -->

## t-011 — Hybridizer version history, primary selection, reactions, sharing and achievements

<!-- note:begin t-011 -->
Silas-requested 2026-10-31 PT: resubmit disappointing hybrid renders, keep old versions and promote any valid version to primary. Reuse ArtImage reactions/comments, add social sharing and three earned achievements. Preserve pair cache identity, visibility, owner permissions and ArtJob provenance.

The hybrid version history and community features are implemented on kind_robots worker/hybridizer-t011-20261031-7b9ac2. PR checks and front-end verification are the remaining reviewer steps.

Merged silasfelinus/kind_robots PR #4561 as 1a247eeeb831c2df59607231ee5d1a93d096ed13 after all 18 required workflow runs completed successfully. Added artwork revision history, resubmission, owner primary selection, ArtImage upvotes and comments, signed-in Play sharing and three native achievements. No production ArtJobs were submitted in this change; existing Play route used, with external launch still separately gated.
<!-- note:end t-011 -->
