# tzaddik-gallery — task history archive

Full `note:` prose for completed tzaddik-gallery tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Write the design brief and audit reusable Kind Robots infrastructure

<!-- note:begin t-001 -->
Turn Silas's direction into a concrete Kind Robots implementation plan. Audit existing Reaction/user identity patterns, submission/moderation surfaces, image/source handling, and reusable gallery/card components. Keep Tzaddik Gallery a first-class Kind Robots feature rather than a parallel auth/reaction stack.


Existing DESIGN-BRIEF.md on main already covers the product brief. This cycle audited reusable Kind Robots reaction, gallery, auth, moderation, image provenance, project identity, and Pinia/API boundaries. Connector safety checks rejected both attempted branch file writes, so no documentation diff could be landed; releasing the claim for normal retry without consuming a pass.

DONE 2026-09-26 (claude-scheduled-20260926T115739Z-tzaddik-t001, PR #5209): Added an
Infrastructure audit section to DESIGN-BRIEF.md covering reactions (reuse the existing
Reaction model/enum + reactionStore.ts, no new table), gallery/detail components (kr-
gallery.vue + kr-card-flip/kr-card-back, following character-gallery.vue),
auth/attribution (userStore.ts + authGuard.ts), moderation/overrides
(SocialPostDraftStatus-style approval enum, plus mandarin_curation.prisma's override-
with-provenance-preserved pattern for MandarinCatalogOverride/MandarinCatalogChange),
and Pinia/API conventions (reactionStore.ts as the template). Flagged one genuine gap:
no existing sourceUrl/license/attribution fields or external-image-fetch/cache route
anywhere in the schema -- recommended building on server/utils/safeFetch.ts (SSRF-safe)
plus a TTL cache modeled on cthulhuquariumCuration.ts. This lands the audit a prior
connector-only session (openai-scheduled-2026-09-26T101656Z) found but could not write
due to connector safety-check rejections. Unblocks t-003.
<!-- note:end t-001 -->

## t-003 — Add Tzaddik candidate and provenance data model

<!-- note:begin t-003 -->
Model a candidate/person record with living/historical state, short rationale, Wikipedia article URL, Wikipedia/Wikimedia image provenance, optional explicit admin overrides, submitter attribution, curation state, multi-select controlled editorial tags, structured country/region metadata, a sourced controversy/objections section, last source refresh/revision metadata, and auditable recheck-request state. Preserve source provenance even when display fields are overridden.
DONE 2026-09-26 (claude-scheduled session): pass 1's rejection was verified accurate — silasfelinus/kind_robots#3057's schema.prisma change (TzaddikCandidate/TzaddikCandidateTag/TzaddikRecheckRequest) had never run `npx prisma generate`, so test:generated-client-parity failed CI. Fixed by regenerating and committing the Prisma client diff exactly as retry_context described (8 modified generated files + 3 new per-model files, no schema changes). All 32 checks green, mergeable_state clean, merged as fb056ab. No new task needed.
<!-- note:end t-003 -->

## t-005 — Build sourced person detail view with objections section

<!-- note:begin t-005 -->
Show image, concise biography/rationale, source links/provenance, status, submitter attribution, reactions, a visible controversy/objections section, and a Request recheck control with last-checked/pending state. Keep objections factual and source-backed; absence of a substantial documented objection should not trigger invented balance.
DONE 2026-09-27 (claude-scheduled session): implemented tzaddik-detail-sheet.vue plus the reaction access-rule wiring (getExpectedTargetField/assertReactionTargetAccessible/g etContentOwnerId/reactionVisibility) that tzaddik-gallery/t-021 deliberately deferred here. silasfelinus/kind_robots#3060 merged clean (all checks green including verifyReactionTargetCoverage.ts, verifyReactionRouteAuth.ts, verifyEarnedKarmaWiring.ts, and the full vue-tsc typecheck).
<!-- note:end t-005 -->

## t-006 — Add authenticated candidate submission workflow

<!-- note:begin t-006 -->
Let Kind Robots users submit candidates with a rationale and Wikipedia article. Default new submissions to pending/community state rather than automatically entering the canonical 36. Record submitter user identity.
Opened kind_robots PR #3065: authenticated candidate submission workflow (POST /api/tzaddik + tzaddik-submit-form.vue). vue-tsc/eslint/prettier clean; CI running.
silasfelinus/kind_robots#3065 merged clean (all 33 checks green: vue-tsc, eslint, contract verifiers, layout-contract, etc). Signed-in users can now submit a Tzaddik candidate (name, LIVING/MEMORIAL, rationale, Wikipedia source, optional biography) via a new modal on /tzaddik-gallery; POST /api/tzaddik validates the wikipedia.org source, reserves a unique slug, and creates the row at curationState: PENDING with submittedByUserId recorded. Submitter sees their own pending entry immediately via the existing [id].get.ts visibility carve-out. No karma/reaction wiring added -- out of scope. t-007 (upvote/downvote) and t-008 (moderation/override) remain waiting on this and can now be picked up.
<!-- note:end t-006 -->

## t-007 — Add user upvotes/downvotes using Kind Robots reaction patterns

<!-- note:begin t-007 -->
Reuse the site's existing user/reaction conventions where practical. Reactions express community sentiment and discovery; they must not silently define the canonical 36 or turn the page into an unmoderated popularity leaderboard.
AUDITED, not reimplemented (zero-diff close): the reaction write/read/access-rule stack for TzaddikCandidate is already fully wired end-to-end and satisfies this task as written. Confirmed by direct code read plus an independent Explore-agent pass: (1) server/api/reactions/index.post.ts's getExpectedTargetField maps TZADDIK -> tzaddikCandidateId with its own assertReactionTargetAccessible/getContentOwnerId branches (t-005, kind_robots#3060); (2) server/api/reactions/tzaddikCandidate/[id].get.ts is the dedicated read route, gated by reactionVisibility.ts's canViewReactionsOn; (3) utils/karmaRefTypes.ts registers 'tzaddikCandidate' in KARMA_REF_TYPES/KARMA_REF_TARGET_COLUMNS so REACTION_RECEIVED karma flows correctly; (4) components/tzaddik/tzaddik-detail-sheet.vue already embeds <reaction-card target-type="tzaddikCandidate" reaction-category="TZADDIK" .../> plus <review-list target-type="tzaddikCandidate" .../>, preserved through t-017's rebuild -- the exact same reaction-card/review-list pattern every other gallery (character, bot, dream, reward, scenario) uses for its own detail view. All three CI-enforced verifiers (verifyReactionTargetCoverage, verifyReactionRouteAuth, verifyEarnedKarmaWiring) already pass for tzaddikCandidate today. Users can submit LOVED/CLAPPED/BOOED/HATED/NEUTRAL/FLAGGED reactions (this codebase's upvote/downvote vocabulary -- there is no literal thumbs-up/down component anywhere in the site) and see others' reactions, exactly matching 'reuse the site's existing user/reaction conventions where practical.' Genuinely missing (filed as tzaddik-gallery/t-025, not built here to avoid guessing at an unreviewed UX/architecture call): any in-grid reaction/earned-karma affordance on the Living/Memorial gallery cards themselves -- bot-gallery.vue's bot- card.vue wraps reactable-card with an earned-karma badge in-grid, but tzaddik- gallery.vue renders through the generic kr-gallery/GalleryItem (no reaction slot) and no userStore.trackEarnedKarma('tzaddikCandidate', ...) call exists yet anywhere. Deliberately not adding this now: it requires choosing between extending kr-gallery's generic GalleryItem (cross-cutting, touches every other gallery using it) or building a bespoke tzaddik-card.vue and swapping the page off kr-gallery's renderer (nontrivial, touches the page t-017 just rebuilt) -- a real design decision, not a mechanical follow- on, and the task's own note ('must not turn the page into an unmoderated popularity leaderboard') argues for deliberately not surfacing a raw vote count in-grid without an explicit call on it.
<!-- note:end t-007 -->

## t-008 — Add moderation and explicit source/content overrides

<!-- note:begin t-008 -->
Admin/editor controls can approve/archive submissions and override Wikipedia-derived display text or images. Overrides must retain the original source/provenance and make the edited state inspectable.
Merged silasfelinus/kind_robots#3068 (squash bf9b42f) -- admin approve/archive routes, an explicit-override route (never touches sourced columns, only the *Override siblings), an admin-gated curationState query param on index.get.ts so PENDING/ARCHIVED candidates are discoverable, store actions, and a new admin-only Review queue tab + in-sheet moderation panel in tzaddik-detail-sheet.vue. Verified: vue-tsc/eslint/prettier clean; v erifyReactionTargetCoverage/verifyReactionRouteAuth/verifyEarnedKarmaWiring/auditServerA piCallers/verifyLayoutContract/auditIcons all still pass unchanged; full CI (33/33) green before merge.
<!-- note:end t-008 -->

## t-009 — Seed Silas's named historical and living candidates

<!-- note:begin t-009 -->
Import the accepted first gallery membership from seed-sets.yaml. Silas explicitly accepted the full 2026-09-26 discovery docket plus his direct nominations on 2026-09-26. Dolly Parton died on 2026-08-25 and belongs in Memorial. Direct Memorial additions include Nelson Mandela and Harriet Tubman. Preserve suggested_by and accepted_by_user_id metadata. Refresh living/memorial status and Wikipedia/Wikimedia provenance from current sources at ingest time; never trust stale model memory or cached prose. Seed-set membership is not the same thing as final canonical top-36 selection.
IN PROGRESS 2026-09-28 (claude-scheduled session): kind_robots#3069 adds the missing admin bulk-import capability (server/api/tzaddik/import.post.ts) plus the live Wikipedia/Wikidata/Commons source-refresh util (server/utils/tzaddikSourceRefresh.ts) that recheck.post.ts's own docstring noted was never built. Neither existing route (index.post.ts, override.patch.ts) could preserve seed-sets.yaml's suggested_by ("llm-daily-discovery" vs a real user) or set acceptedByUserId/wikipediaPageId/wikipediaRevisionId/image provenance directly, so this was a genuine prerequisite, not scope creep. vue-tsc/eslint/prettier clean locally; full CI running on the PR. Remaining for t-009 to actually close: once #3069 merges and deploys (Unraid auto-deploy; no PR preview exists for this repo), POST the 29 seed-sets.yaml entries (12 living + 17 memorial) to /api/tzaddik/import with rationale text sourced from projects/tzaddik-gallery/discovery/2026-09-26.md's Pitch fields for the 20 llm-daily-discovery entries, and freshly authored rationale for the 9 silasfelinus direct nominations (Cassandra Peterson, Greta Thunberg, Dolly Parton, Steve Irwin, Fred Rogers, Martin Luther King Jr., Stanislav Petrov, Nelson Mandela, Harriet Tubman) which have no discovery pitch text. Verify all 29 created records afterward (curationState APPROVED, correct lifeState from live Wikidata, suggestedBy/acceptedByUserId preserved).
UPDATE 2026-09-28 (claude-scheduled session): kind_robots#3069 merged to main (3cf718c). Confirmed live production (kindrobots.org) has NOT yet picked up this commit -- POST /api/tzaddik/import currently returns the Nuxt SPA shell (200 HTML), not the route, meaning Unraid auto-deploy hasn't run yet (see AGENTS.md's documented merge-is-not-deploy gap). Re-claimed at status:claimed rather than done, since the actual deliverable (29 seeded candidate records) doesn't exist yet. Next session: recheck whether POST https://kindrobots.org/api/tzaddik/import responds as JSON (not the SPA shell) before attempting the import; if so, run the 29-entry payload built from seed-sets.yaml + discovery/2026-09-26.md's Pitch/Review-note fields (rationale/objections) for the 20 llm-daily-discovery entries, with freshly authored rationale for the 9 silasfelinus direct nominations, using KR_API_TOKEN as the admin bearer. Verify all 29 created (curationState APPROVED, lifeState matches live Wikidata) before marking t-009 done.
RECHECKED 2026-09-28T04:46:00Z (claude-scheduled session): POST https://kindrobots.org/api/tzaddik/import still returns the Nuxt SPA shell (HTTP 200, text/html), not JSON -- Unraid auto-deploy of kind_robots#3069 (merged 3cf718c) still has not run. No import attempted (against an undeployed route this would 404/render- shell, not actually seed records). Releasing without consuming a pass -- same deploy- timing gap the prior session already documented, no new work possible from this session. Next session: recheck POST https://kindrobots.org/api/tzaddik/import for a JSON response before attempting the 29-entry seed-sets.yaml + discovery/2026-09-26.md import described above.
RECHECKED 2026-09-28T06:51Z (claude-scheduled session): POST https://kindrobots.org/api/tzaddik/import still returns the Nuxt SPA shell (HTTP 200, text/html), not JSON -- Unraid auto-deploy of kind_robots#3069 still has not run, over 2 hours after it merged. No import attempted (same reasoning as the prior recheck: against an undeployed route this would 404/render-shell, not actually seed records). Releasing the stale claim without consuming a pass -- same known deploy-timing gap AGENTS.md documents, not a new incident. Next session: recheck POST https://kindrobots.org/api/tzaddik/import for a JSON response before attempting the 29-entry seed-sets.yaml + discovery/2026-09-26.md import.
RECONCILED 2026-09-28T~07:30Z (claude-scheduled session, tzaddik-gallery/t-012 cycle): live production now serves the deployed route and the deliverable exists. Verified via GET https://kindrobots.org/api/tzaddik?lifeState=LIVING|MEMORIAL: 12 living + 17 memorial = 29 records, all curationState APPROVED, matching seed-sets.yaml exactly. All 9 silasfelinus direct nominations (Cassandra Peterson, Greta Thunberg, Dolly Parton, Steve Irwin, Fred Rogers, Martin Luther King Jr., Stanislav Petrov, Nelson Mandela, Harriet Tubman) carry suggestedBy=silasfelinus and acceptedByUserId=1; the 20 llm-daily- discovery entries carry suggestedBy=llm-daily-discovery. Dolly Parton correctly MEMORIAL with deathDate 2026-08-25. kind_robots#3074 ("fix(tzaddik): restore production publishing and seed the gallery", merged after #3071) appears to be what carried the deploy/import through -- not re-verified against that PR's own diff since the live data is conclusive either way.
<!-- note:end t-009 -->

## t-010 — Research an internationally broad candidate pool for the living 36

<!-- note:begin t-010 -->
Build a sourced research pool spanning multiple world regions, languages, professions, and forms of public service. Deliberately counter US/Anglosphere celebrity bias. Assign provisional controlled tags so the pool can be inspected for domain concentration as well as geography. Research is not automatic canonization: record why each person is notable, meaningful objections/controversies, Wikipedia availability, and uncertainty. Favor genuine educational discovery over quota-box geography.
IMPLEMENTED 2026-09-28 (claude-scheduled session): built projects/tzaddik- gallery/discovery/living36-research-pool.md -- 24 sourced, internationally diverse living candidates with controlled tags and review notes, deduplicated against seed- sets.yaml and both existing dockets. Placed in discovery/ (not project root) so excluded_names() picks it up automatically.
MERGED 2026-09-28: silasfelinus/conductor#5329 merged (CI green, 25/25 checks). Closing done.
<!-- note:end t-010 -->

## t-012 — Add accessibility, responsive gallery polish, and empty/loading/error states

<!-- note:begin t-012 -->
Make cards and detail content usable at phone/tablet/desktop widths, with alt text and keyboard-accessible reactions/submission controls. Source failures should degrade to explicit missing-source/image states rather than broken cards.
MERGED 2026-09-28 (found via direct kind_robots PR listing, not surfaced by select_role.py's own kind_robots reviewable-PR check): silasfelinus/kind_robots#3071 implemented and merged -- ARIA tab semantics + roving-focus keyboard nav on tzaddik- gallery.vue's section tabs, plus radiogroup/radio semantics and a live status announcement on the shared reaction-card.vue star rating (used by every reaction surface, not just Tzaddik). Verified: npm run test (vue-tsc) clean, eslint/prettier clean, verifyLayoutContract.ts holds, live-browser check at phone/tablet/desktop widths (against the still-undeployed older production build, per the documented merge-is-not- deploy gap). Confirmed loading/error/empty/image-failure states were already satisfied by existing shared kr-gallery/art-pending-placeholder/kr-art-plate infra, no new page- level code needed for those. All 31 kind_robots CI checks green before merge.
<!-- note:end t-012 -->

## t-014 — Build the Daily Tzaddik discovery docket

<!-- note:begin t-014 -->
Build a daily research pipeline analogous to Daily Dream, but editorial rather than generative-canon: produce exactly 10 living and 10 deceased candidate suggestions per Pacific day. Each item needs a concise sourced bio, a short "why this person" pitch, Wikipedia/Wikimedia provenance, meaningful controversy/objection notes when documented, living/deceased verification, structured region/context metadata, controlled editorial tags, and dedupe against existing canonical, historical, pending, and recently-suggested people. Suggestions never auto-enter the canonical 36 or historical gallery.
<!-- note:end t-014 -->

## t-015 — Surface each daily 20-person roster for Silas's vetting

<!-- note:begin t-015 -->
Give Silas an easy daily review surface, integrated with the same attention/digest patterns used by Daily Dream and other daily creative commitments. He must be able to approve, reject, defer, or open the full sourced profile. Preserve prior decisions so rejected suggestions are not immediately recycled. This is an inbound review queue only; do not send or publish anything externally.
Landed as silasfelinus/conductor#5323: scripts/tzaddik_review.py (--check/--pending/--show/--decide) plus projects/tzaddik-gallery/discovery- decisions.yaml as the human-editable decision ledger, wired into CLAUDE.md's session- startup report. Conductor-side only, matching how Daily Dream's own state is surfaced (scripts + session digest) -- no kind_robots UI/DB build. t-016 (recurring cadence) remains the next follow-on.
<!-- note:end t-015 -->

## t-017 — Build the lg/xl single-page gallery and person-review shell

<!-- note:begin t-017 -->
On lg/xl, make Living / Memorial / Info switch inside one composed viewport-level interface. The person/submission view should fit the large image, atmospheric background, concise bio/pitch, provenance, controversies, review controls, navigation, and an internally scrollable comments region without routine page-level scrolling. Preserve the currently selected Living/Memorial context when opening and closing a person. On sm/md, deliberately fall back to a normal stacked, scrollable page rather than squeezing the desktop arrangement into miniature panels.


Replaced the narrow filler-style gallery shell with the scoped lg/xl composed workspace and person-review layout on worker/tzaddik-gallery-t-017-20260927T215700Z-a7f3; mobile remains stacked and scrollable. Opening the implementation PR for CI verification.

Merged silasfelinus/kind_robots#3067 (squash dda94d7) after CI green (TypeScript,
layout-contract, verify, GitGuardian, all Storybook/narrative contracts) and a diff
audit of the 2 changed files (tzaddik-detail-sheet.vue, tzaddik-gallery.vue page) for
scope/safety -- no admin/moderation controls added (correctly deferred to t-008), no
v-html/eval/secret patterns, splash art deliberately deferred to t-018 per PR body.
Reviewed by conductor sweep session.
<!-- note:end t-017 -->

## t-018 — Create and integrate the Tzaddik Gallery splash/background art

<!-- note:begin t-018 -->
Use the queued tzaddik-gallery splash request as the atmospheric large screen backdrop / landing visual. The image must support overlaid UI, portrait cards, and readable text rather than competing with them. Verify cropping at lg/xl and provide a simpler mobile treatment for sm/md.
Queued the splash art render (conductor/projects/art-prompts.yaml entry tzaddik-gallery- splash, prompt from ART-PROMPTS.md, target public/images/tzaddik-gallery/tzaddik- gallery-splash.webp) and wired the front-end (pages/tzaddik-gallery.vue) to reference that path as a full-bleed lg/xl-only background-image with a gradient overlay, degrading cleanly on sm/md and until the image renders. kind_robots#3078 open, CI pending. Image delivery is async via auto-art-generate.yml (triggered on this push since art- prompts.yaml changed, or its 6h schedule) -- a future cycle should verify the file actually resolves at that path before closing this task done.
RECHECKED 2026-09-28 (scheduled conductor sweep): kind_robots#3078 (front-end wiring) confirmed merged 2026-09-28T12:03:51Z. Splash asset still not delivered -- GET https://kindrobots.org/images/tzaddik-gallery/tzaddik-gallery-splash.webp returns 404, and projects/art-prompts.yaml's tzaddik-gallery-splash entry is still status: pending (not yet picked up by auto-art-generate.yml). Leaving at status: review per the task's own note ('verify the file actually resolves at that path before closing this task done') rather than closing done on code-merge alone. Next session: recheck the source_url and re-check art-prompts.yaml status before closing done.
2026-09-28 conductor sweep: check_pr_merged_drift.py flagged this at status: review with its implementing PR (kind_robots#3078) already merged 2026-09-28T12:03:51Z. Reconciled to done. Splash art render (tzaddik-gallery-splash.webp) still delivers async via auto- art-generate.yml per the PR's own flag -- worth a visual confirmation once it lands, but code integration is complete and merged.
<!-- note:end t-018 -->

## t-019 — Add community Wikipedia recheck / correction requests

<!-- note:begin t-019 -->
Add a visible Request recheck action on every person page for authenticated users. A request queues a controlled server-side refresh of the record's canonical Wikipedia/Wikimedia sources and compares the latest revision to the stored normalized snapshot. Recheck living/deceased status and death date, source-derived biography fields, redirects/article identity, and image/license provenance. Record requester, timestamps, source revision, diff/result, and dedupe/cooldown state. Safe source-derived changes may refresh automatically; a verified death/living-status change must move the record between Living and Memorial. Never silently overwrite explicit editor overrides: preserve override provenance and route conflicts or ambiguous source changes to editor review. Show users last-checked, requested/pending, success, or needs-review state so repeated requests do not hammer Wikipedia.
Wired recheck.post.ts to actually run fetchTzaddikSource synchronously (fetch/diff/apply-or-needs-review/cooldown), extended the detail sheet's status label to show the terminal outcome. PR: silasfelinus/kind_robots#3080.
MERGED 2026-09-28: silasfelinus/kind_robots#3080. recheck.post.ts now actually runs fetchTzaddikSource synchronously on each request: applies safe source-derived changes (including moving Living<->Memorial on a verified Wikidata death-date change), routes a changed Wikipedia page id to NEEDS_REVIEW without auto-applying, records NO_CHANGE/UPDATED/NEEDS_REVIEW/FAILED with a resultJson diff, adds a 1-hour cooldown, and never touches the *Override columns. Detail sheet's status label extended to show the terminal outcome. vue-tsc/eslint/prettier clean; all 32 kind_robots CI checks green before merge.
<!-- note:end t-019 -->

## t-020 — Add multi-select editorial tags and gallery filtering

<!-- note:begin t-020 -->
Add a controlled multi-select tag taxonomy for Politics, Pop Culture, Humanitarian, Science & Medicine, Education, Environment, Civil Rights & Justice, Peace & Diplomacy, Community & Mutual Aid, Arts & Culture, Journalism & Truth, and Courage & Rescue. Show tags on cards and person pages and support filtering by one or more tags in Living, Memorial, and review surfaces. Treat tags as descriptive editorial metadata, not scores or endorsements. Keep country/region as separate structured metadata and living/memorial as record state. Editors may extend the controlled set when repeated real cases do not fit, but avoid arbitrary one-off tags.
Merged silasfelinus/kind_robots#3063: tag badges on Living/Memorial gallery cards and the person detail sheet, plus a chip-based multi-select tag filter (AND semantics) above the gallery. TzaddikCandidateTag/TzaddikEditorialTag and the API's Tags payload already existed; this PR is the first UI consumer. Scoped to Living/Memorial only -- no review/admin surface exists yet (pending tzaddik-gallery/t-006), so 'review surfaces' filtering from the task description is deferred until that surface is built. Verified via vue-tsc --noEmit, eslint, and prettier --check on the changed files (all clean); no live DB/browser path was available in this sandbox. CI green (30/30 checks) before merge.
<!-- note:end t-020 -->

## t-021 — Add a TZADDIK reactionCategories enum value ahead of the detail-view/reactions work

<!-- note:begin t-021 -->
Kaizen from t-004 (silasfelinus/kind_robots#3058): stores/reactionStore.ts + the reactionCategories enum (server/api/reactions/*) currently has no TZADDIK value -- ART_IMAGE, ART_COLLECTION, BOT, CHARACTER, CHAT_EXCHANGE, DREAM, FACET, MESSAGE, PROJECT, PROMPT, RESOURCE, REWARD, SCENARIO, THEME are the full set today. t-005 (detail view) and t-006 (submission workflow) both need to attach reactions to a TzaddikCandidate. Landing the enum/schema migration now, decoupled from either task's own UI work, means neither one needs its own migration cycle just to wire up reactions.
Merged silasfelinus/kind_robots#3059: TZADDIK reaction category + Reaction.tzaddikCandidateId column/FK/migration landed, getExpectedTargetField deliberately maps it to null pending t-005/t-006's access-rule wiring (TzaddikCandidate has no userId/isPublic pair for the generic content-access check).
<!-- note:end t-021 -->

## t-022 — Fix the pre-existing eslint-disable-next-line/no-explicit-any mismatch in reactions/index.post.ts's getContentOwnerId

<!-- note:begin t-022 -->
Kaizen from t-005 (silasfelinus/kind_robots#3060): server/api/reactions/index.post.ts's getContentOwnerId declares `const modelMap: Record<string, {findUnique: (args: any) => ...}>` across three lines, with an `eslint-disable-next-line @typescript-eslint/no-explicit-any` comment directly above it. Because the type is wrapped across multiple lines, the actual `any` usage lands two lines below the comment it was meant to cover, so ESLint reports both "Unexpected any" AND "Unused eslint-disable directive" on the same block. Confirmed pre-existing on main (not introduced by t-005) via `npx eslint` against the committed file before t-005's own changes landed. Fix: either reformat the disable comment onto the line that actually has the `any` (e.g. `eslint-disable-line` on the closing brace line, or restructure the type to fit one line) or give the map a real (non-`any`) callable type. Small, mechanical, one file.
<!-- note:end t-022 -->

## t-023 — Extend the editorial-tag filter to the review/submission surface once it exists

<!-- note:begin t-023 -->
Kaizen from t-020 (silasfelinus/kind_robots#3063): t-020 built tag badges (gallery cards + person detail sheet) and a chip-based multi-select tag filter, but only for the Living/Memorial tabs -- no review/admin/moderation surface exists yet in the codebase for a submitted-but-not-yet-approved candidate, so the "review surfaces" half of t-020's own description could not be built. Once t-006 (authenticated candidate submission workflow) lands and a review surface exists, wire the same filter chips (reuse utils/tzaddikTags.ts's TZADDIK_TAG_ORDER/labels) into it. Also confirm with Silas at that point whether the filter's AND semantics (must match every selected tag) is the intended UX, or whether OR (match any selected tag) reads better once there's a larger, more filterable pending-review queue -- t-020 picked AND without an explicit human decision either way.
<!-- note:end t-023 -->

## t-024 — Surface editor-only moderation actions in the t-017 composed detail rail instead of a separate admin page

<!-- note:begin t-024 -->
Kaizen from t-017 (silasfelinus/kind_robots#3067): the new composed lg/xl person-review shell places the existing reaction/recheck/discussion controls but deliberately does not invent nonfunctional approve/reject/defer buttons ahead of t-008. Once t-008 lands moderation/override actions, let the detail rail surface editor-only approve/archive/override controls in the same composed panel rather than introducing a separate admin page.
Already delivered by t-008 (silasfelinus/kind_robots#3068, merged): that PR's admin-only moderation panel (Approve/Archive buttons + override form) landed directly inside tzaddik-detail-sheet.vue's composed aside -- the exact 't-017 composed detail rail' this task asked for, not a separate admin page. The 'Review queue' tab t-008 also added to pages/tzaddik-gallery.vue is an in-page admin-only tab (for discovering PENDING/ARCHIVED candidates that are otherwise invisible on the public Living/Memorial rosters), not a separate admin page/route -- confirmed no pages/admin/tzaddik*.vue or similar exists. Verified by reading current tzaddik-detail-sheet.vue (aside section, admin-gated on userStore.isAdmin) and tzaddik-gallery.vue (REVIEW_TAB, admin-only) on kind_robots main (47b533a). No further code change needed; closing as done with no new diff.
<!-- note:end t-024 -->

## t-025 — Decide and build in-grid reaction/discovery affordance for Living/Memorial gallery cards

<!-- note:begin t-025 -->
Filed from the t-007 audit (2026-09-27): the reaction submit/read UI for a Tzaddik candidate is fully wired in the detail sheet (reaction-card + review-list, same pattern every other gallery uses), but nothing surfaces a reaction/earned-karma signal on the gallery grid cards themselves -- bot-gallery.vue's bot-card.vue wraps reactable-card with an in-grid earned-karma badge, but tzaddik-gallery.vue renders through the generic kr-gallery/GalleryItem, which has no reaction slot, and no userStore.trackEarnedKarma('tzaddikCandidate', ...) call exists anywhere yet. Two real implementation paths, different blast radius: (a) extend kr-gallery's GalleryItem to optionally carry an earned-karma badge / react-toggle -- cross-cutting, touches every other gallery using kr-gallery, audit siblings first per AGENTS.md; or (b) build a bespoke tzaddik-card.vue wrapping reactable-card (mirroring bot-card.vue) and swap the Living/Memorial grids off kr-gallery's generic renderer onto it. Whichever path: keep the surfaced signal a soft discovery cue, not a raw vote count or sort key -- t-007's own note warns against turning this into an unmoderated popularity leaderboard, and t-011 (FOR SILAS) already gates canonical-36 membership as an editorial decision, not a mechanical reaction score.
Path (b) from the task note: built tzaddik-card.vue wrapping reactable-card + kr-entity- card-body (mirroring bot-card.vue/reward-card.vue), swapped the Living/Memorial/Review grids onto it via kr-gallery's #item slot, and wired earned-karma tracking via the existing generic userStore.trackEarnedKarma('tzaddikCandidate', ...) -- tzaddikCandidate was already a registered KarmaRefType, so no backend change was needed. Card shows a soft Living/Memorial + review-state badge and editorial tag chips, not a raw vote count, per the note's warning against an unmoderated popularity leaderboard. Registered tzaddik-card in verifyCardActionContract.ts's entity-card list. PR: silasfelinus/kind_robots#3076. Verified: vue-tsc, eslint, prettier, test:gallery- adoption, test:gallery-consistency, test:card-action-contract, test:reaction-targets, test:reaction-route-auth all clean/green locally; opening PR for CI.
Merged silasfelinus/kind_robots#3076 (squash e3daa2d). All CI green: vue-tsc, eslint, prettier ratchet, test:gallery-adoption, test:gallery-consistency, test:card-action- contract (10 entity cards), test:reaction-targets, test:reaction-route-auth, plus the full 412-step Contract verifiers job. No further action needed.
<!-- note:end t-025 -->

## t-026 — Confirm before archiving an already-APPROVED (live) Tzaddik candidate

<!-- note:begin t-026 -->
Kaizen from t-008 (silasfelinus/kind_robots#3068): the admin Archive button in tzaddik-detail-sheet.vue fires immediately with no confirmation step, for both a PENDING submission (low stakes -- nothing public changes) and an already-APPROVED candidate (higher stakes -- this removes a live entry from the public Living/Memorial roster with one click). Add a confirmation prompt specifically for the APPROVED-to-ARCHIVED transition (curationState === 'APPROVED' before the click), leaving the PENDING-to-ARCHIVED path as an immediate action since it was never public in the first place.
Implemented on worker/tzaddik-gallery-t-026 (kind_robots): added a window.confirm prompt in tzaddik-detail-sheet.vue's archive() specifically for the APPROVED-to-ARCHIVED transition, matching the existing window.confirm pattern used elsewhere in the repo (art-gallery.vue, stylist-clients.vue, etc.). PENDING path unchanged. Verified via eslint (clean) and vue-tsc --noEmit (clean, exit 0). PR: silasfelinus/kind_robots#3072.
Reconciled 2026-09-28 (check_pr_merged_drift.py): implementation PR silasfelinus/kind_robots#3072 merged 2026-09-28T04:06:26Z; conductor roadmap was still at status=review. Closing to done -- no further verification needed beyond what the implementer already recorded (eslint/vue-tsc clean); this is a local confirm-dialog UI change with no deploy-gated behavior to re-check.
<!-- note:end t-026 -->

## t-027 — Extend the discovery pipeline's dedup to cover pending/rejected/deferred names once t-015 exists

<!-- note:begin t-027 -->
Kaizen from t-014 (silasfelinus/conductor#5320), premise updated now that t-015 (silasfelinus/conductor#5323) has landed: this task assumed pending/rejected/deferred state would live in a future kind_robots database, requiring excluded_names() to pull it via KR_API_TOKEN. t-015 instead built a conductor-side review surface (scripts/tzaddik_review.py + projects/tzaddik-gallery/discovery-decisions.yaml), and excluded_names() already keeps every docketed name in its dedup pool permanently regardless of decision (approved/rejected/deferred/pending all included via all_dockets(), independent of the ledger) -- confirmed in #5323's docstring update to excluded_names(). There is no remaining dedup gap to fix: DESIGN-BRIEF.md's "dedupe against canonical, historical, pending, rejected, deferred, and recently suggested people" is already fully satisfied. No kind_robots integration is needed here. Close this out at the next opportunity (verify excluded_names() still has no logic gap, then status: done citing this note) rather than attempting the now-unnecessary KR_API_TOKEN pull.
Verified, no code change needed: excluded_names() (scripts/build_tzaddik_discovery.py) already keeps every docketed name in the dedup pool permanently via all_dockets(), independent of any approved/rejected/deferred/pending decision -- confirmed by inspection and by tests/test_build_tzaddik_discovery.py's existing dedup-violation coverage. t-015 (silasfelinus/conductor#5323) built the decision ledger (discovery- decisions.yaml) as documentation/review-state, not as a dedup input, so there was never a kind_robots-database dependency to build here. Closing as satisfied by t-015's docstring clarification; ran the full tzaddik test suite (29 passed) to confirm no regression.
<!-- note:end t-027 -->

## t-028 — Give editors a queue of NEEDS_REVIEW recheck requests instead of one-candidate-at-a-time discovery

<!-- note:begin t-028 -->
Kaizen from t-019 (silasfelinus/kind_robots#3080): the recheck pipeline now actually runs and can leave a TzaddikRecheckRequest at NEEDS_REVIEW (a Wikipedia page-id change -- possible redirect/article identity change -- that was deliberately not auto-applied). Today an editor can only discover this by opening that specific candidate's detail sheet, which shows the reason via the new recheckDetailLabel. There is no cross-candidate view. Add an admin-only filter/queue (e.g. extend the existing admin Review queue tab from t-008, or a small dedicated list) surfacing every TzaddikCandidate with a latest RecheckRequest at NEEDS_REVIEW, so editors don't have to remember to check each candidate individually.
MERGED 2026-09-28: silasfelinus/kind_robots#3081. Added an admin-only needsReview=true filter to GET /api/tzaddik and a third Needs-review toggle on the Review queue tab, reusing the existing gallery/card/detail-sheet flow. vue-tsc/eslint/prettier clean; all 33 kind_robots CI checks green before merge.
<!-- note:end t-028 -->

## t-029 — Surface the NEEDS_REVIEW recheck reason directly on the Needs-review queue card

<!-- note:begin t-029 -->
Kaizen from t-028 (silasfelinus/kind_robots#3081): the new Needs-review queue lists every flagged candidate, but the actual reason (the old vs. new Wikipedia page id, and the diff) is only visible after clicking through to that candidate's detail sheet -- the same recheckDetailLabel t-019 added. For a queue meant to be scanned, showing a short reason (or at least the changed page id) directly on tzaddik-card.vue when rendered inside this queue would save an editor a click per candidate.
implementation_pr: silasfelinus/kind_robots#3082
MERGED 2026-09-28: silasfelinus/kind_robots#3082 (queue card now renders the recheck reason inline; recheckReasonLabel extracted to utils/tzaddikRecheck.ts and shared with the detail sheet). vue-tsc/eslint/prettier clean; kind_robots CI green before merge.
<!-- note:end t-029 -->

## t-030 — Add an inline accept/dismiss action for a NEEDS_REVIEW recheck directly on the Needs-review queue card

<!-- note:begin t-030 -->
Kaizen from t-029 (silasfelinus/kind_robots#3082): the queue card now shows *why* a candidate needs review (the recheck reason, e.g. a changed Wikipedia page id), but resolving it still requires opening the detail sheet to act. Add a compact accept/dismiss control directly on the card -- e.g. "Update to new page id" / "Keep current source" -- backed by the existing recheck-resolution logic, so an editor can clear the whole queue without a click-through per candidate.
MERGED 2026-09-28: silasfelinus/kind_robots#3083 (Update/Keep current buttons on the queue card, backed by new resolveTzaddikRecheckReview + POST /api/tzaddik/recheck- resolve). vue-tsc/eslint/prettier clean; kind_robots CI green before merge.
<!-- note:end t-030 -->

## t-031 — Give the detail sheet the same NEEDS_REVIEW accept/dismiss controls the queue card has

<!-- note:begin t-031 -->
Kaizen from t-030 (silasfelinus/kind_robots#3083): the queue card can now resolve a NEEDS_REVIEW recheck inline (Update / Keep current, backed by resolveTzaddikRecheckReview + POST /api/tzaddik/recheck- resolve), but tzaddik-detail-sheet.vue's own recheck section still only offers the "Recheck" button -- an editor who opens a candidate from the queue (rather than acting from the card directly) has no way to resolve it without closing the sheet and finding the card again. Wire the same two actions into the detail sheet's existing recheck section, reusing store.resolveRecheckReview.
<!-- note:end t-031 -->

## t-032 — Tighten tzaddik-card.vue's recheck-resolve buttons to require status === NEEDS_REVIEW, matching the server's actual guard

<!-- note:begin t-032 -->
Kaizen from t-031 (silasfelinus/kind_robots#3084): the detail sheet's new Update/Keep-current buttons are gated on latestRecheck.status === 'NEEDS_REVIEW', matching what POST /api/tzaddik/recheck-resolve (resolveTzaddikRecheckReview) actually accepts -- it 409s for any other status. tzaddik-card.vue's own buttons (t-030) instead show whenever recheckReasonLabel(...) is non-empty, which is also true for a FAILED recheck (it has a non-empty error string). That's a latent 409 path on the card, currently unreachable per t-029's note that only the needsReview=true queue filter's response carries RecheckRequests at all. Tighten the card's show condition to require status === 'NEEDS_REVIEW' too, closing the gap even if it stays unreachable today.
Merged as silasfelinus/kind_robots#3085 (squash 9aa72d9). Server verified: resolveTzaddikRecheckReview 409s on any status != NEEDS_REVIEW; card now gates its buttons on that exact status instead of non-empty recheckReason (which was also true for FAILED).
<!-- note:end t-032 -->

## t-033 — Rename to Tzaddikim, add a nominee blacklist, and deepen every tag section to 72+ nominees

<!-- note:begin t-033 -->
Silas, 2026-09-30 (verbatim in notes_from_silas): at least 72 nominees per tag section, best people (Keanu Reeves, Abraham Lincoln, Jimmy Carter named), a blacklist (Gandhi, Mother Teresa, Thomas Jefferson named), and the Tzaddikim name.
Done in this session: blacklist.yaml (29 entries, reasons stated) enforced by build_tzaddik_discovery.py and mirrored in kind_robots utils/tzaddikBlacklist.ts (submission 422, admin import, model discovery), with a parity test. Six research passes (two tags each) produced 856 new nominees; every one is deduped, blacklist-checked, and verified against Wikidata for article identity and life state (six recent 2025-26 deaths moved to Memorial; Zainab Salbi dropped for a bad Wikidata death date; Shakira dropped over a tax-fraud plea). Per-tag totals with the 29 live seeds: Politics 118, Pop Culture 102, Humanitarian 154, Science & Medicine 159, Education 164, Environment 117, Civil Rights & Justice 318, Peace & Diplomacy 136, Community & Mutual Aid 134, Arts & Culture 121, Journalism & Truth 121, Courage & Rescue 188. Membership is in seed-sets.yaml and kind_robots config/tzaddik-initial-seeds.json; research text in discovery/2026-09-30-nominee-expansion.md. Display name is Tzaddikim; the /tzaddik-gallery route stays (with /tzaddikim redirecting) so links keep working.
Close when: the kind_robots PR is merged and deployed, the Bootstrap seeds workflow reports its verification line, and GET /api/tzaddik shows 72+ per tag.
DONE 2026-09-30T12:20Z: kind_robots#3117 merged and deployed; the bootstrap import ran across several deploy-cancelled runs (idempotent resume) and created every seed. Live GET /api/tzaddik: 885 approved (397 living, 488 memorial), every tag 72+ (lowest Pop Culture 102, highest Civil Rights & Justice 317). Two seeds (Patricia Bath, Jocelyn Bell Burnell) had already been created PENDING by the discovery pool and were skipped by the import; approved by hand, and the import now promotes such rows. Also fixed while verifying: the admin Suggestions pool had never filled because OpenAI strict mode rejected 'uniqueItems' in the replenish schema (kind_robots#3119), and replenish deduped against only 400 recent rows, re-suggesting approved people; 29 such duplicates and blacklisted names (Leila Khaled, Tariq Ramadan, now on blacklist.yaml) were archived from the pool, leaving 91 pending suggestions.
<!-- note:end t-033 -->

## t-034 — Community Top 36 per Tzaddikim category, explicit up/downvotes, and tutorial-sidebar consolidation

<!-- note:begin t-034 -->
Silas, 2026-10-11 PT: each category (living, deceased, pop culture, and contribution filters) needs a Top 36 ordered by reviews and upvotes, with other eligible nominees in a distinct gallery on the same page. Enable upvoting and downvoting submissions. Move all Info explanations into the tutorial page and add a visible tab/control opening the ? workspace sidebar. Keep approval separate from community scoring, prevent repeat votes from stacking, and preserve moderation visibility.

Implementation in silasfelinus/kind_robots#3562. CI typecheck, layout, and most contracts passed; final full contract run pending. User-facing presentation remains unverified until self-hosted deployment and review.

Kind Robots PR #3562 was squash merged at ad29e90f87ed7cf70cde6f4c636b92c12097d470 after all 33 head workflow runs completed successfully. Top-36 community scoring, voting, and tutorial consolidation reached main. The live self-hosted production deployment and visual acceptance are separate from the code merge.
<!-- note:end t-034 -->
