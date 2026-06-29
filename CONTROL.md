# CONTROL.md — Silas's Steering Sheet

**This is the one file Silas edits to steer everything. Agents read it FIRST, before any
project roadmap.** It holds *intent and direction*; the per-project `roadmap.yaml` files
hold the detailed task lists. When this file and a roadmap disagree on direction, THIS
file wins — agents should adjust the roadmap to match, not ignore this.

STATUS.md (next to this file) is auto-generated and read-only — read it to see what's
happened. Don't edit it; edit here.

---

## Global overview  ← agents read this before everything

**Right now:** Proving the autonomous loop works end-to-end. Keep changes small and
reversible until the first clean cycle is done. Nothing publishes, deploys, or spends
money without my explicit approval (set `approved_by_human: true` on the gated task).

**Priority order this week:** humboldt-scoop → humboldt-scoop-cms → approval-portal
→ digital-storefront → kind-robots → global-ui. (Mirror changes into projects/priority.yaml.)

**Standing rules for all agents:** Respect each project's `kind`. Honor `depends_on` gates.
Never expand product-types.yaml — pitch it. When unsure, do less and escalate to
needs-human.

**Global notes (free-form, agents read these):**
- (add notes here anytime — e.g. "deprioritize SEO for now", "I like the comic pitch, run with it")

---

## Per-project direction  ← agents read the block for the project they're working on

### humboldt-scoop  (software)
**Direction:** Import the existing site, get it building cleanly, then refresh content.
Don't redesign — modernize and fix.
**Notes:**
- (your notes)

### humboldt-scoop-cms  (software)
**Direction:** Build the customer-management tool for the poop-scoop business. Simple,
self-hostable. Dummy data only until I say otherwise.
**Notes:**
- (your notes)

### approval-portal  (software)
**Direction:** The console I want to live in — read projects/pitches, approve/reject,
confirm updates, roll back. A face over the repo; git stays the source of truth. Build
incrementally, each milestone usable alone.
**Notes:**
- (your notes)

### digital-storefront  (content)
**Direction:** Research stores → brainstorm content (only within approved product types) →
I pick → create drafts → market → advertise on budgeted channels. Every outward step is
gated on me.
**Notes:**
- (your notes)

### kind-robots  (software)
**Direction:** STUB until I write the full roadmap. App owns its own logic; the shared KR
backend is read-only/external. Backend changes become pitches, never direct edits.
**Notes:**
- (your notes)

### global-ui  (software)
**Direction:** Define and build the shared user-facing interface for projects, tasks,
front-end TODOs, honeydos, kaizens, approvals, and completion history. Honeydos are global
LLM-assigned user tasks; kaizens are project-specific prompts shown while viewing a project.
Keep task creation visible on the front end without creating a second source of truth.
**Notes:**
- Start by approving the vocabulary and presentation model before implementation.

### brainstorm  (proposal)
**Direction:** Generate a few strong, specific, buildable pitches each cycle for me to vote
on — new products (within approved types), content series, revenue streams, and AI_Networker
upgrades. Quality over quantity. Don't repeat existing pitches.
**Genre / content guidance (agents follow this for content pitches):**
- (e.g. "comics: queer-positive, hopeful sci-fi, all-ages"; "RPG: rules-light, GM-friendly";
  "coloring books: nature + whimsy". Add/replace anytime — this steers content pitches.)
**Notes:**
- (your notes)

### conductor  (software)
**Direction:** Improvements to the conductor / AI_Networker system itself — CI, scripts,
ops tooling. Keep changes small and reversible. Nothing outward-facing without needs-human.
**Notes:**
- (your notes)

### alexa-integration  (software)
**Direction:** Custom Alexa skill + Unraid relay server. Draft and prototype only — do NOT
publish the skill to the Alexa store or expose a live endpoint without needs-human.
Auth via KR_API_TOKEN (same token as fetch_todos.py).
**Notes:**
- (your notes)

### conductor-app  (software)
**Direction:** Flutter app (iOS/Android/macOS/web) over the kind_robots REST API.
Build incrementally; each milestone should run standalone. Do NOT submit to any app
store without needs-human. Auth secrets stay out of source control.
**Notes:**
- (your notes)

### art-generator-connect  (software)
**Direction:** Wire conductor Workers into the existing kind_robots art API (SD/ComfyUI).
Treat the shared backend as read-only/external — consume endpoints, don't modify them.
Backend changes become pitches, not direct code edits.
**Notes:**
- (your notes)

### media-watchlist  (software)
**Direction:** Parse + import Silas's personal media log, then surface it with browse,
stats, and integrations (Letterboxd, Comic Vine, Tautulli). HARD GATE: no affiliate
links and no public-facing pages without needs-human. Dummy/sample data only until
the real log is shared.
**Notes:**
- (your notes)

### storymaker  (software)
**Direction:** Collaborative storytelling engine built on top of existing Kind Robots
data models. App-owned logic only; shared backend is read-only/external.
Start with the session data model (needs-human gate) before any play-mode code.
**Notes:**
- (your notes)

---

## How my edits take effect
- **Direction / notes:** agents read them next cycle. No script needed.
- **Priority:** also update projects/priority.yaml (or tell an agent to sync it).
- **Approve a gated task / pitch:** edit the task in its roadmap (`approved_by_human: true`,
  `status: done`) or set a pitch's `status:` to approved/rejected. The resolver unblocks
  dependents next cycle.
