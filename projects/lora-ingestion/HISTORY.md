# lora-ingestion — task history archive

Full `note:` prose for completed lora-ingestion tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Build the watched-folder LoRA import agent

<!-- note:begin t-002 -->
conductor/ops/home-server/lora_import_agent.py — stdlib poller; on a stable drop it runs kind_robots scan_loras.py (--organize move) then import_catalog.py --upsert. Runs embedded as a daemon thread inside kr-relay (relay_media_agent.start_lora_watcher) — one process/token/log, watcher and render loop cannot stall each other. Host: the pm2 render box (alexandria is a locked-down NAS; SMB is case-insensitive so Windows moves are safe post case_merge). Verified live 2026-07-28 with ume_classic_impressionist (detected Flux, moved, Resource created:1); Civitai flagged it nsfw so it sorted NSFW — override to SFW via scan --overrides if wrong.
<!-- note:end t-002 -->

## t-004 — Add civitaiModelId/civitaiModelVersionId + fix resourceMutationSelect

<!-- note:begin t-004 -->
Landed on kind_robots branch claude/lora-organization-catalog-coyhav (commit f1a9585). Migration 20260728120000 adds civitaiModelId + civitaiModelVersionId (Int?, indexed, ADD COLUMN IF NOT EXISTS); create.ts validates/emits them and allows them through the field guard; batch.post.ts carries them in the upsert update; resourceMutationSelect now also echoes triggerWords/defaultTrigger/hash/previewImageUrl + the two new columns; scan_loras.py captures modelId/modelVersionId (Civitai + CivArchive) and emits them from to_resource(); prisma client regenerated. Needs: a PR opened + merged to kind_robots main, then migrate deploy on kindblank_fresh.

Reconciled during the open-roadmap drift audit. Kind Robots PR #1124 merged the Civitai model/version columns, migration, mutation-select fields, and catalog import support described by this task. The implementation is on main, so review is complete.
<!-- note:end t-004 -->

## t-005 — Front-end My Library LoRA browser

<!-- note:begin t-005 -->
Landed on kind_robots branch claude/lora-organization-catalog-coyhav (commit c4bdb60). pages/lora.vue (My Library + Discover-stub tabs) + components/lora/{lora-card,add-lora,lora-gallery}.vue built on reactable-card; resourceStore.visibleLoras adds LORA/LYCORIS + maturity gating. Search + base-model + maturity + sort filters, client-side pagination, add/edit via updateResource (PATCH) / batch upsert. All SFCs compile clean. Ships with t-004 in the same PR.

Reconciled during the open-roadmap drift audit. Kind Robots PR #1124 merged the My Library LoRA browser, filtering, maturity handling, pagination, and add/edit surfaces described by this task. The implementation is on main, so review is complete.

CORRECTION (2026-08-16, lora-ingestion/t-007): the file paths above are stale. The front end was later rebuilt content-driven and none of `pages/lora.vue`, `components/lora/lora-card.vue`, or `components/lora/lora-gallery.vue` exist on current kind_robots main. The actual shipped surface is `content/resources.md` (route `/resources`, channelKey `play`, tabKey `resources`) mounting `components/resources/resource-manager.vue`, which embeds the Library/Discover tabs, backed by `components/resources/resource-gallery.vue` and `components/resources/resource-card.vue`. `components/lora/add-lora.vue` and `components/lora/lora-discover.vue` still exist and match. Functionally equivalent rename/rebuild, not a regression.
<!-- note:end t-005 -->

## t-006 — Discover tab + DownloadRequest queue + version-update flow

<!-- note:begin t-006 -->
Landed + gaps closed. kind_robots (PR #1124): DownloadRequest model + migration 20260728133000; /api/lora/download-request (dedupes owned + in-flight), /download/claim (atomic claim + reaper), /download/[id]/complete; browse.get.ts is source-aware — Civitai keyword search AND CivArchive by-id/URL lookup (recovers removed models), owned-flag + updatable (own-a-different-version) + maturity clamp; lora-discover.vue with source toggle + Update action + Discover tab. conductor (088ebfdc): lora_import_agent.py download loop (claim -> fetch, Civitai token redacted, .part atomic write -> complete; direct URLs cover CivArchive downloads). Verified: npm run test (vue-tsc) clean + resource-ownership contract passes; gallery/mutation selects echo the new columns. Remaining nicety: resourceId back-link on complete is best-effort null (owned-detection reads Resource.civitaiModelVersionId set by the catalog).

Reconciled during the open-roadmap drift audit. Kind Robots PR #1124 merged the Discover browser and DownloadRequest queue, while the Conductor import agent landed the matching claim/download/complete loop. The task note already records the implementation and verification; review is complete. End-to-end relay verification remains separately and correctly tracked by t-003.
<!-- note:end t-006 -->

## t-007 — Correct t-005/t-006's stale file-path claims (front end was later rebuilt content-driven)

<!-- note:begin t-007 -->
Kaizen from the 2026-08-16 weekly site audit. t-005/t-006 (both done) describe the front end as `pages/lora.vue` (My Library + Discover tabs) plus `components/lora/{lora-card,lora-gallery}.vue`. None of those three exact files exist on current kind_robots main. The actual shipped surface is content-driven: `content/resources.md` (route `/resources`, channelKey `play`, tabKey `resources`) mounting `components/resources/resource-manager.vue`, which itself embeds the Library/Discover tabs, backed by `resource-gallery.vue` and `resource-card.vue` (`components/lora/add-lora.vue` and `components/lora/lora-discover.vue` do still exist and match). This is a live, functionally-equivalent rename/rebuild with no correction note anywhere recording it -- unlike ruler-hooked/t-013 or alexa- integration/t-019, which self-corrected the same class of drift. Add a short dated note to t-005 and/or t-006 recording the actual current file paths.
DONE (2026-08-16): added a dated correction note directly to t-005 recording the actual current file paths (content/resources.md + components/resources/{resource-manager,resource-gallery,resource-card}.vue). Conductor-repo-only doc fix; no kind_robots implementation needed since the front end already matches reality, only the roadmap note was stale.
<!-- note:end t-007 -->

## t-008 — Add temporary admin LoRA maturity triage page with local review progress

<!-- note:begin t-008 -->
Silas-directed 2026-08-24 cleanup tool. Add a disposable Kind Robots admin page that loads canonical LoRA/LyCORIS Resource records, stages SFW/NSFW classifications in localStorage, supports batch classification and hiding already-confirmed rows, and saves only changed Resource.isMature values through the existing Resource update API. Keep the implementation self-contained so the page/store can be deleted after the catalog cleanup is complete.


Implemented the temporary Kind Robots /admin/lora-triage page and dedicated localStorage-backed Pinia store on the worker branch. The page batch-stages SFW/NSFW decisions, hides confirmed rows, paginates the catalog, and saves only changed Resource.isMature values through the existing Resource PATCH path.

Merged Kind Robots PR #2077. Added temporary /admin/lora-triage and a dedicated localStorage-backed triage store; batch SFW/NSFW decisions, hide-confirmed progress, filtering/pagination, and changed-only Resource.isMature saves now use the existing PATCH path. Final PR head passed TypeScript, Layout Contract, Contract Tests, architecture/scroll/API/facet and all other PR workflows.
<!-- note:end t-008 -->
