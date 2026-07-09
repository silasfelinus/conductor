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
