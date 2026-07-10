# TALKBACK — superkate-hairstyle-ai

Append-only cross-vetting log for the Hair Studio project. Never edit or delete prior entries.
Format is defined in the root `AGENTS.md` ("How to write a talkback entry").

## 2026-07-09 | Claude (Silas-directed) → Worker | superkate-hairstyle-ai/t-001 | pattern

**Subject:** Project created as an independent sibling of superkate-services-calculator.

**Detail:**
- Silas asked for a surprise Hair Studio feature for Hair by Superkate: upload/snap a client
  photo, pick color/style/enhance (any combo), send to the Kind Robots Kontext Comfy backend,
  get the same photo back with new hair; navigable loading; per-client before/after gallery.
- Made it a **new project** rather than folding into the calculator: different tech surface
  (generative image editing vs. Flutter appointment math), a different eventual monetization
  path (paid + free trial, possibly a separate app), and it keeps the deep calculator roadmap
  clean. Associated via DESIGN-BRIEF + shared customer-profile identity anchor.
- Verified the backend already exists: `POST /api/comfy/kontext/generate` takes `imageData` +
  `prompt` and returns the transformed `data.imageData`, gated by mana/`authAndGate`. MVP is
  frontend + prompt building + gallery only — no backend build needed.
- Recommended a **web-first surface in Kind Robots** (t-002, soft gate) because the Kontext
  backend and gallery infra live there and Flutter build/verify is human-gated (calculator
  t-014), which keeps stalling that roadmap.

**Suggested action:** Worker — start on t-003 (prompt-builder design) and t-004 (staged tab
shell). Keep everything behind a preview flag; the feature is a surprise for Superkate. Do NOT
build billing or reveal the feature — t-011/t-012 are hard human gates. Silas — answer t-002
(web-first vs Flutter-first) when convenient; the team proceeds web-first meanwhile.

## 2026-07-09 | Claude (Silas-directed) → Worker | superkate-hairstyle-ai/t-004..t-008 | pattern

**Subject:** First working cut of the Hair Studio tab landed in kind_robots (branch
claude/superkate-hairstyle-ai-nse06o). Silas confirmed web-first.

**Detail:**
- Reused existing infra instead of building a model backend: artStore.generateArt with
  engine:'kontext' already generates via /api/comfy/kontext/generate AND persists the result
  via /api/art/save-generated. art-styler.vue was the working reference for kontext + server
  resolution. New surface is a thin component + config, no backend work.
- Privacy requirement satisfied structurally: every generated ArtImage is saved with
  isPublic:false, so client photos never surface in public galleries or the memory-match game
  (the game/getters filter on image.isPublic). Tagged designer "stylist:<client>" for later
  per-client grouping.
- Files: components/art/stylist-manager.vue, content/stylist.md (/stylist → :stylist-manager),
  dashboardHelper "stylist" tab (route /stylist), tutorialCards "stylist" art section, and two
  placeholder webp tab/tutorial images (real art queued in art-prompts.yaml requests).
- Fixed a reactivity bug pre-commit: was mutating a raw object after pushing it into a ref
  array (Vue 3 proxy won't track that) — switched to patchResult(id, patch) by id.

**Flags for Reviewer / Silas:**
- NOT verified in a running app — no local build env (no node_modules) and no live Comfy
  server here. Typecheck/lint could not run. Needs a real run before merge to main.
- The tab is registered in the art dashboard config but is NOT yet behind a preview/role flag,
  so it is technically reachable. The surprise constraint wants it hidden from Superkate until
  Silas approves the reveal — added as a follow-up under t-012 and noted on t-004.
- Client field is free text for now; binding to real calculator customer profiles is the
  cross-project coordination in t-008.

**Suggested action:** Silas — run kind_robots locally (or a preview deploy) with an active
Comfy/Kontext server and try /stylist end-to-end; confirm results save private. Worker — pick
up t-007 (store-level background job so it survives leaving the tab) and t-008 (durable
per-client gallery) next.

## 2026-07-09 | Claude (Silas-directed) → Worker | superkate-hairstyle-ai/t-007+t-008 | pattern

**Subject:** t-007 (navigable async) done and t-008 (durable per-client gallery) first cut, via a
dedicated stylistStore. kind_robots PR #134.

**Detail:**
- Root fix for "navigable while waiting": job state was component-local and died on tab switch.
  Moved it into stores/stylistStore.ts, so the generateArt promise resolves against the store
  even after the component unmounts — the result lands when Superkate returns to /stylist. This
  is the correct Pinia pattern (store outlives component lifecycle).
- t-008 first cut: durable "Past looks for <client>" loads the user's saved private stylist
  images (GET /api/art/user/:id, filtered by the "stylist:" designer tag) and groups by client.
- Honest gap called out and turned into t-013: save-generated only persists the RESULT, so the
  before image isn't durable and the client key is still a free-text tag. Full durable
  before/after + real customer-profile link needs the source saved and cross-project
  coordination with the calculator.

**Flags for Reviewer / Silas:**
- Still not runtime-verified (no node_modules / live Comfy server in this environment). Followed
  existing artStore + performFetch conventions and self-reviewed reactivity (store refs read
  inside component computeds track correctly). Needs a real /stylist run.

**Suggested action:** Silas — merge #134 after a local /stylist smoke test. Next up unless you
redirect: t-009 (harden Kontext API client error/timeout/mana states) and t-010 (polish
empty/loading/error + before/after compare), then t-013.

## 2026-07-09 | Claude (Silas-directed) → system | superkate-hairstyle-ai dashboard bugfix | pattern

**Subject:** Live-run feedback from Silas surfaced two dashboard bugs; diagnosed and fixed in
kind_robots PR #136. PRs #133/#134 merged by Silas — t-004..t-009 are done.

**Detail:**
- Bug 1: selecting the Hair Studio tab still showed the image generator. The dashboard header's
  tab buttons only set store state (no navigation); art-manager renders the active tab
  internally and its validTabs didn't include "stylist", so it fell back to "generate". Fix:
  stylist renders inline in art-manager like every other art tab.
- Bug 2: returning to the Art channel forgot the remembered tab. content/art.md pinned
  dashboardTab: generate — a VALID art tab — so every /art visit force-reset tab memory via
  setDashboardShellFromContent + the header's route-enforced watch. Other channels' landing
  pages carry non-tab hints (bots.md → "overview"), which is why only Art misbehaved. Fix:
  setDashboardShellFromContent only enforces a frontmatter tab that names a real tab of that
  dashboard (page-as-tab identity, e.g. /stylist, /memory); otherwise it preserves the
  remembered tab. art.md no longer pins a tab.
- Ops note: the git relay's push path failed persistently this session (hangups/413); the fix
  went up via the GitHub API (push_files), which also normalized navStore.ts and
  art-manager.vue from legacy CRLF to the .gitattributes-declared LF — PR #136 flags to review
  with whitespace hidden.

**Suggested action:** Silas — merge #136, hard-refresh, and retest: pick Hair Studio (should
render in place), hop to Rewards and back to Art (should return to Hair Studio). Worker — next
up: t-013 (durable before/after source persistence + real client link) and t-010 (state polish).

## 2026-07-09 | Claude (Silas-directed) → system | superkate-hairstyle-ai/t-014 | pattern

**Subject:** Production styling failed (ENOTFOUND on the ts.net Comfy host from Vercel).
Root-caused and re-routed through the durable ArtJob queue. kind_robots PR #138 + relay
change on conductor PR #320. Silas also expanded scope: full Superkate app replica on the
Hair Studio page (t-015, claimed).

**Detail:**
- The direct /api/comfy/kontext/generate route dials the Comfy box from the deployed backend,
  which is not on the home tailnet — ts.net names don't resolve there. The repo already had
  the working pattern: the ArtJob queue that ops/home-server/relay_agent.py claims OUTWARD
  (pull model, no inbound path, "all policy lives in kind_robots").
- New /api/comfy/kontext/enqueue: mana-gated at enqueue, job payload carries the kontext
  workflow + input image + a save block. relay_agent.py gained stdlib multipart upload of
  payload images to ComfyUI's input folder (LoadImage support — image-to-image jobs).
- Ownership subtlety: save-generated rejects foreign userIds, so relay uploads land owned by
  the relay machine user. The queue COMPLETE endpoint (already admin-gated) now applies the
  job's save block + ownership by the enqueuing user — keeping stylist photos private and in
  Superkate's Past-looks history. Legacy jobs without a save block are untouched.
- DEPLOY STEP FOR SILAS: restart the home relay agent with the updated relay_agent.py after
  merging, or queued stylist jobs will fail at the LoadImage node.

**Suggested action:** Silas — merge kind_robots #138 + conductor #320, update the home relay
agent, then run /stylist on the deployed site end-to-end. Claude — t-015 (full app replica
suite on /stylist: Calculator | Clients | History | Hair Studio) is in progress.

## 2026-07-09 | Claude (Silas-directed) → system | superkate-hairstyle-ai/t-015 | pattern

**Subject:** Full Superkate app replica built on /stylist (kind_robots PR #138, part 2).

**Detail:**
- New suite shell on /stylist: Hair Studio | Calculator | Clients | History, view choice held
  at store level so it survives navigation (consistent with the dashboard-tab fix).
- superkateStore is the approved "easy mock": localStorage-persisted customers, appointments,
  and receipt settings. Calculator SPEC honored — rate x time + products in cents, hours/
  minutes preset chips, product cost optional defaulting to $0.00, warm receipt with the
  configurable contact block (glossgenius link + reply email) and "Superkate loves you!",
  mailto composer with client email prefill, and the delete-detach invariant from calculator
  t-031's test list.
- Cross-feature tie-in: the restyler's Client field now suggests names from the client book —
  first step toward the t-013 real client-identity link.
- Follow-up (not this PR): replace localStorage with KR-model-backed persistence so Superkate's
  book syncs across devices; that is where the "1-1 it somehow" upgrade lands.

**Suggested action:** Silas — one review pass on kind_robots #138 covers both the prod
generation fix and the suite; remember to restart the home relay agent with the updated
relay_agent.py (conductor #320) or queued styling jobs will fail at the LoadImage node.
