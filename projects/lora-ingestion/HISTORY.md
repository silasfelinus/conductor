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

## t-009 — Generalize model discovery/download and watched imports beyond LoRA-only routing

<!-- note:begin t-009 -->
Silas-directed 2026-09-19: audit the downloader against the full Resource model taxonomy, preserve automatic Lora/import ingestion, add equivalent checkpoint/import ingestion, and stop routing every non-CHECKPOINT download into the LoRA directory. Keep Civitai discovery aligned with the Resource types it can actually supply and with ComfyUI's canonical model directories.

Generalized Civitai discovery and download routing across file-backed Resource types, preserved the existing Lora/import watched ingestion path, added checkpoints/import watched ingestion using the generic model scanner, removed the duplicate DownloadRequest consumer from the filesystem watcher, and added focused contracts for routing and import behavior. Implementation branches are reconciled with current main and ready for PR review.

2026-09-19 Reviewer: rejected pass 1 -- conductor PR #4737 has 3 real Python test
failures from an unfinished lora-import->model-import/checkpoints-path rename, plus a
PR-handoff-template violation. See retry_context. kind_robots#2877 companion PR is green
and unaffected.

Follow-up from Silas on the merged downloader work: the Discover base-model filter was still hardcoded to five families. Replaced it with a grouped taxonomy covering every generation/base family recognized by the LoRA/model catalog, including Krea 2, Flux.2, ZImage, Qwen, video/multimodal families, and all SD/SDXL variants. Added a contract that cross-checks the UI list against scan_loras.py BASEMODEL_MAP and scan_models.py FOLDER_BASE_HINTS so future catalog families cannot disappear from Discover silently.

Completed after the original downloader/import pair landed as kind_robots#2877 and conductor#4737, then Silas spotted the remaining base-filter drift. kind_robots#2882 replaced the five hardcoded Discover base choices with the shared catalog-aligned taxonomy and added CI coverage against both model scanners. All 47 checks passed, including TypeScript and the Model download taxonomy contract.

Silas follow-up: the exhaustive base-model menu is too noisy. Reopen to condense Discover to base families, surface the bases Kind Robots actually supports, and keep exact Civitai variant coverage behind the family choice.

Condensed Discover from exact Civitai base-version entries to 14 useful families. Kind Robots-supported LoRA bases are grouped first with checkmarks: Krea 2, FLUX.2, SDXL, Pony, SD 1.5, and Z-Image. Family choices expand server-side to Civitai's exact BaseModel enum strings, so SDXL still covers Turbo/Lightning/etc. without showing them all. Legacy exact-value URLs remain accepted. Also corrected several exact Civitai enum spellings used by the prior exhaustive list.

2026-09-19 closed: kind_robots#2894 merged (family-based Civitai base filter, retry pass
addressing pass-1 rejection). All CI green, mergeable_state clean.
<!-- note:end t-009 -->

## t-010 — Type every LoRA by what it is FOR, and randomize art batches from those pools

<!-- note:begin t-010 -->
Silas-directed 2026-09-22: "identify their type, such as character, style, setting, action, clothing, etc, and then be able to randomize them for art generation, for example, asking for '{character} running in {style}, batch 10', should give ten different characters running in ten random styles for the selected checkpoint." Auto-configure from Civitai where possible, and make it editable from the Resource card or the LoRA editor. Also asked whether random selection already works for other objects (character, location, facet) -- it did not, for art generation.
Landed as one vertical slice on kind_robots: Resource.loraCategory + loraCategorySource (additive migration, ten categories), a shared classifier (utils/loraCategory.ts) mirrored into scan_loras.py so the Civitai tags are read at the one moment they exist, category editing in the LoRA editor and the triage page (with a suggest pass and bulk apply), and a new POST /api/art/randomize that rolls a templated prompt into a batch plan. server/utils/promptVariants.ts became the shared roll engine for both the Challenge Center and art, dealing WITHOUT replacement so ten variants genuinely give ten different values, with a replayable seed. Facets, Characters and Scenarios answer placeholders too, so the "other objects" half of the ask is covered.
SCHEMA-AFFECTING: prisma/migrations/20260922120000_add_lora_category. Additive (two nullable columns + one index), so it is safe for the unattended Alexandria deploy window.
FOR SILAS, after deploy: the pools start EMPTY -- every existing LoRA row is unclassified, so {character} rolls nothing until the catalog is classified. Run `npm run backfill:lora-categories` (dry run first, then --apply; add --fetch-tags with CIVITAI_TOKEN set to reach the Civitai tags the rows never stored). Then use the triage page's "Suggest for all unclassified" for whatever the heuristics could not reach. Hand corrections are stamped HUMAN and are never overwritten by a later scan or backfill.
2026-09-22 closed: kind_robots#2967 merged. All 62 checks on the final head passed except the pre-existing tests/python/test_powershell_syntax_contract.py::test_the_paths_ filter_covers_every_ps1_in_the_repo, which reproduces identically with the whole branch stashed and is documented on the PR with a one-line proposed patch (its helper matches only double-quoted .ps1 globs while powershell-syntax-contract.yml writes single quotes, so it reads a coverage hole that does not exist). Green on this PR's own ground: TypeScript, Contract verifiers (383 tests, including the three new steps), Replay migrations on MariaDB, Failed-migration repair, Generator + importer regression, Build production image, GitGuardian.
Independent reviewer close-out (same session, conductor scheduled sweep): re-verified the above before this task's own close-out landed -- reproduced the powershell-syntax- contract failure directly against origin/main (confirmed pre-existing/unrelated) and audited migration.sql line-by-line (two nullable ADD COLUMN statements plus one CREATE INDEX, no DROP/data rewrite) per AGENTS.md's Reviewer migration-audit requirement. Filed the regex fix as lora-ingestion/t-011 (kaizen, ready).
<!-- note:end t-010 -->

## t-011 — Fix the PowerShell-syntax-contract Python test's quote-only regex so it recognizes single-quoted workflow path globs

<!-- note:begin t-011 -->
Kaizen from t-010's merge (kind_robots PR #2967). CI on that PR was red on
tests/python/test_powershell_syntax_contract.py::test_the_paths_filter_covers_every_ps1_in_the_repo
even though the diff touched no .ps1 file and no PowerShell workflow -- confirmed
independently on origin/main itself before merging past it (see t-010's note).

Root cause: utils/scripts/../tests/python/test_powershell_syntax_contract.py's
_ps1_path_patterns() only matches double-quoted globs:
`re.findall(r'^\s*-\s*"([^"]*\.ps1)"', text, re.M)`. .github/workflows/powershell-
syntax-contract.yml writes its `paths:` filter in single quotes
(`- 'scripts/**.ps1'`), so the regex finds nothing and the test wrongly asserts a
coverage hole that does not exist. It has stayed invisible because
python-scripts.yml only runs on scripts/**.py changes, and t-010 (scan_loras.py)
was the first thing in a while to touch one.

Fix: make the quote character optional in _ps1_path_patterns(), e.g.
`re.findall(r"""^\s*-\s*['"]([^'"]*\.ps1)['"]""", text, re.M)`. Verify by running
the test against main both before (red) and after (green) the fix, and confirm it
still correctly fails if a real .ps1 is added without updating the paths filter
(don't let the fix accidentally make the test unconditionally pass).

Fixed the PowerShell syntax contract parser to recognize both single- and double-quoted .ps1 workflow path globs, with a focused regression test covering both quote styles. Implementation branch worker/lora-ingestion-t-011-openai-scheduled-2026-09-22T061509Z-lora-ingestion-t011-a11.

Reconciled 2026-09-22T07:10Z: this task's own PR (kind_robots#2969, opened
2026-09-22T06:18:52Z by an OpenAI Worker cycle) was superseded by kind_robots#2970, an
independent same-bug fix from a different session that merged first
(2026-09-22T06:45:31Z) with broader coverage (accepts double-quoted, single-quoted, and
bare YAML scalars, plus a quote-backreference guard, vs. #2969's single/double-only
fix). #2969 showed mergeable_state=dirty against current main as a result; closed it as
redundant (comment posted) rather than resolving the conflict, since #2970 already fully
covers the fix. Closing done with implementation_pr pointing at the PR that actually
landed.
<!-- note:end t-011 -->

## t-012 — Polish art-generator random pools, facet picker placement, image sizes, and Krea 2 preset

<!-- note:begin t-012 -->
Silas-directed follow-up to t-010 on 2026-09-22. The newly merged random-batch
surface needs a usability pass: the Facet picker opens below the bottom of the
scrollable generator and is clipped; random choices should visibly expose LoRA
categories, Facet types, and Kind Robots objects instead of hiding Facet/object
fallbacks behind duplicate placeholder names; object picks should contribute a
compact visual clause derived from their existing artPrompt rather than only a
name/title or an enormous context dump; width and height should be selects with
common model-family-appropriate dimensions; and the Random batch helper text must
stop repeating the original "{character} running in {style}" implementation prompt.

Also audit the Krea 2 Detailed preset. Krea 2 Turbo is the repo's 8-step default,
while the current Detailed button asks for 16 steps even though the distilled
engine contract caps Krea 2 below that. Remove or replace the misleading preset
rather than promising quality from unsupported extra steps.

Prefer existing artPrompt fields plus a deterministic compacting rule before adding
new schema columns. Add focused contracts for the source-explicit random placeholders
and model-size choices, preserve the existing random-batch/LoRA compatibility and
maturity rules, and keep this as a reversible front-end/server utility change.

Implementation is scoped on the Kind Robots worker branch: random source-explicit LoRA/Facet/object controls, compact persisted artPrompt context, upward Facet picker, checkpoint-aware dimension selects, and removal of the misleading 16-step Krea 2 preset.

Retry completed and merged as kind_robots#2972 at 2026-09-22T08:43:15Z. The lint-ratchet regression from pass 1 was repaired before merge; exact-head GitHub Actions on ca670db0e5a0d35643ef2ebbcb40808b8ab303a4 completed successfully, including TypeScript Type Check 35705843124, Contract Tests 35705843079, Layout Contract 35705843239, Art Prompt + Icon Safety 35705842988, Facet Catalog Contract 35705843228, Project Architecture Contract 35705843150, Generated Client Parity 35705843226, and Schema Migration Parity 35705843156. No deploy was triggered.
<!-- note:end t-012 -->

## t-013 — Align LoRA/checkpoint imports through one enriched Resource path and queue a custom preview ArtJob

<!-- note:begin t-013 -->
Silas-directed 2026-09-22. Audit both watched-folder imports and Discover/DownloadRequest
imports so LoRAs and checkpoints follow the same lifecycle: move into their canonical
local model directories, upsert the canonical Resource with Civitai provenance, classify
LoRAs from Civitai tags into character/style/setting/etc. without overwriting HUMAN
corrections, and queue one durable custom preview ArtJob whose completed ArtImage attaches
back to the Resource. Re-scans/retries must not create duplicate preview jobs.

Implementation is in review as kind_robots#2992 and conductor#5059. The paired change unifies watched and DownloadRequest LoRA/checkpoint imports through the canonical scanners, restores Civitai tag category classification in the home-server vendor copy, preserves checkpoint Civitai ids, queues attached Resource preview ArtJobs, and deduplicates in-flight resource previews.

REVIEWED & MERGED (Reviewer, 2026-09-22): both companion PRs audited and merged —
kind_robots#2992 (canonical scanner/import/preview source, 51/51 checks green) and
conductor#5059 (ops home-server vendor copy + kr-download routing, 23/23 checks green).
Diff is scoped to the scanner/import/preview surface plus regression tests; fixes a real
mislabeling bug (Civitai collection versions bleeding model-level title into
triggerWords, e.g. Resources 2427/2429) and adds LoRA category classification from
Civitai tags without guessing CHARACTER. No schema/secrets/deploy changes. Merged
kind_robots#2992 first (canonical source), then conductor#5059.
<!-- note:end t-013 -->

## t-014 — Add an automated parity check between the home-server vendored LoRA/model scanners and their kind_robots app-source originals

<!-- note:begin t-014 -->
Kaizen from t-013 (Reviewer, 2026-09-22). The vendored copies in
ops/home-server/lora-catalog/ (scan_loras.py, scan_models.py, import_catalog.py) had
silently drifted from their kind_robots app-source originals -- t-013 found the vendored
scan_loras.py was missing the Civitai tag category classifier entirely, with nothing
catching the gap until a downstream symptom (garbled preview classification) surfaced it.
Add a scripted diff/parity check (e.g. a CI job or a `check_vendored_scanner_parity.py`
comparing the shared logic surface between the two copies) so a scanner feature change in
kind_robots cannot land without the home-server executable copy following, and a stale
vendor copy fails loudly instead of drifting invisibly.

Implemented and merged: scripts/check_vendored_scanner_parity.py
(silasfelinus/conductor#5063), wired into CLAUDE.md's session-sweep list. Verified clean
against the live repos at merge time.
<!-- note:end t-014 -->

## t-015 — Automate the vendored-scanner re-sync PROVENANCE.md still documents as a manual cp + hand-edited note

<!-- note:begin t-015 -->
Kaizen from t-014 (Worker, 2026-09-23). check_vendored_scanner_parity.py now detects
drift between ops/home-server/lora-catalog/{scan_loras,scan_models,import_catalog}.py
and their kind_robots originals, but fixing it is still the manual `cp` + hand-edited
"Re-synced" note PROVENANCE.md documents. Add a
`scripts/resync_vendored_scanner.py --file <name>` that fetches the current kind_robots
original via the same GitHub Contents API t-014 added, writes it over the local vendored
copy, and appends a dated "Re-synced" line to PROVENANCE.md automatically -- removing the
last manual step in the drift-repair loop t-013/t-014 built the detection half of.
<!-- note:end t-015 -->

## t-016 — Feed check_vendored_scanner_parity.py's drift findings directly into resync_vendored_scanner.py

<!-- note:begin t-016 -->
Kaizen from t-015 (Worker, 2026-09-23). check_vendored_scanner_parity.py --json emits a
findings list naming exactly which vendored file(s) drifted; resync_vendored_scanner.py
--file <name> fixes one file per invocation. Once resync_vendored_scanner.py has been used
for a real re-sync or two, consider a --from-parity-report mode (or similar) that reads the
parity checker's findings and re-syncs every drifted file in one command, instead of a human
or agent having to read the parity report and hand-type one --file invocation per finding.

Added a parity-report mode to resync_vendored_scanner.py that consumes the checker's JSON findings, refuses unresolved/untracked entries, preserves the report ref, deduplicates filenames, and re-syncs all drifted scanners in one command; added focused tests.

Reviewer (2026-09-23): merged #5074. CI was all-green except a PR-handoff template check
(Worker's body was missing required AGENTS.md headings); fixed by editing the PR body in
place to the full handoff template, no code changes needed. Squash-merged to main at
22f725b.
<!-- note:end t-016 -->

## t-017 — Print a dry-run byte-delta summary before a multi-file parity-report resync

<!-- note:begin t-017 -->
Kaizen from t-016 (Worker, 2026-09-23). resync_vendored_scanner.py --from-parity-report
now re-syncs every drifted vendored file in one command, but --dry-run only prints which
files it *would* re-sync, not how much each one would actually change. Add a small
byte-delta (or line-delta) summary per file to --dry-run output for the parity-report
path, so a human or agent reviewing a multi-file resync before applying it can tell a
one-line provenance-comment change from a substantial content rewrite at a glance.

Added per-file current/source byte counts and signed byte deltas to parity-report dry runs, with regression coverage proving dry-run remains non-mutating.

Reviewer rejected pass 1 (quality): CI test failure caused by this diff, not a flake.
See silasfelinus/conductor#5077 review comment and retry_context.

Retry addresses pass-1 feedback by updating the pre-existing no-change-path regression to assert current_bytes, source_bytes, and byte_delta: 0. Existing PR #5077 updated on the same worker branch; full GitHub Actions verification pending.

Retry fixed the stale no-change-path assertion identified in pass 1. PR #5077 exact head 424ceedfd73c8b7764d19087b7d965c7186559dc passed Worker PR CI 35814013642, Security Audit 35814013588, Worker PR handoff 35814028404, and Process task events 35814013581, then squash-merged as 63c1e597d259593c022a3db4f1ca4317716c48dd.
<!-- note:end t-017 -->
