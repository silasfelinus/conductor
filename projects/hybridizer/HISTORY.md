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

## t-011 — Hybridizer version history, primary selection, reactions, sharing and achievements

<!-- note:begin t-011 -->
Silas-requested 2026-10-31 PT: resubmit disappointing hybrid renders, keep old versions and promote any valid version to primary. Reuse ArtImage reactions/comments, add social sharing and three earned achievements. Preserve pair cache identity, visibility, owner permissions and ArtJob provenance.

The hybrid version history and community features are implemented on kind_robots worker/hybridizer-t011-20261031-7b9ac2. PR checks and front-end verification are the remaining reviewer steps.

Merged silasfelinus/kind_robots PR #4561 as 1a247eeeb831c2df59607231ee5d1a93d096ed13 after all 18 required workflow runs completed successfully. Added artwork revision history, resubmission, owner primary selection, ArtImage upvotes and comments, signed-in Play sharing and three native achievements. No production ArtJobs were submitted in this change; existing Play route used, with external launch still separately gated.
<!-- note:end t-011 -->
