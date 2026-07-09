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
