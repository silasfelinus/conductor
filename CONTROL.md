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

**Priority order this week:** superkate-services-calculator → challenge-center →
ai-art-academy → coloring-book → humboldt-scoop → humboldt-scoop-cms →
digital-storefront → packmaker → mermaids-of-venice → kind-robots → global-ui.
(Mirror changes into projects/priority.yaml. Updated 2026-07-10: ai-art-academy and
coloring-book created per Silas's session direction — ai-art-academy is the autonomous
initiative test run and should get Worker attention early while it's being proven.)

**Standing rules for all agents:** Respect each project's `kind`. Honor `depends_on` gates.
Never expand product-types.yaml — pitch it. When unsure, do less and escalate to
needs-human.

**Human gate clearance rule:** If Silas explicitly clears a human-gated task in the current
ChatGPT/GitHub session and the agent verifies that the roadmap standards are complete, the
agent may set `approved_by_human: true` and `status: done` with a note citing that clearance.
This does not authorize publishing, deploys, billing changes, DNS/secrets work, app-store
submission, destructive database actions, or other irreversible/outward-facing actions unless
Silas explicitly approves that concrete action too.

**Global notes (free-form, agents read these):**
- Slug parity is a standing rule: every conductor project must have a matching
  kind_robots Dream of dreamType PROJECT sharing the same slug. The slug is the
  universal key across conductor file system, kind_robots database, front-end UI,
  and LLM. When creating a project from any surface (conductor roadmap, front-end
  form, LLM), produce a Dream with the matching slug and update conductor accordingly.
  The sync_projects_to_dreams.py script (conductor/t-009) is the canonical
  conductor → Dream bridge. Do not add redundant FK fields — enforce via slug match.
- Do not invent a second source of project truth. Conductor roadmap.yaml is the
  authoritative task record; kind_robots Dream is the authoritative display/identity
  record. Slug is the join key.
- Project Dreams now expose `goal` and `waypoints`. Treat `goal` as the friendly
  definition of done and `waypoints` as the lightweight user-facing step list.
  Conductor roadmap.yaml remains the authoritative agent task queue; Dream waypoints
  are the UI/voice layer and should not replace roadmap tasks.
- Autonomous project initiative (2026-07-10): roadmaps may declare `autonomous: true`.
  Those projects keep running without my input under the "never idle" rule in AGENTS.md
  (style pass / roadmap upgrade / more inspirations / content expansion when nothing is
  ready). ai-art-academy is the test run. Escalate only actual human gates.

---

## Per-project direction  ← agents read the block for the project they're working on

### superkate-services-calculator  (software)
**Direction:** High-priority app for Superkate / Hair by Superkate. Build a private,
polished services calculator for salon appointments: client name, appointment date,
hourly rate, time spent, product cost, appointment total, search by client/date, and
receipt email preparation using `hourly rate × time spent + product cost = total price`.
Dark theme with purple and teal accents.
**Notes:**
- Treat client appointment data as sensitive. Build the customer database, beta cloud sync,
  receipt prep, and app/device lock according to the approved SPEC.md security baseline.
- No analytics, public pages, direct backend email sending, app-store submission, or store
  billing without explicit approval for that concrete action.
- Make the MVP useful before making it fancy. The fancy should be tasteful, not spreadsheet cosplay.

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
**Direction:** This IS `conductor-page.vue` in kind_robots — not a separate app.
The workspace already has project gallery (cards/heroes/icons/list), pitch voting,
todo management, Dream linking, priority controls, and project status editing.
Do NOT build a standalone Nuxt app in conductor. Future tasks for this project
belong in the kind_robots roadmap as improvements to conductor-page.vue.
**Notes:**
- t-001 (SPEC.md) approved. t-002 (dashboard) built in kind_robots — done.
- t-003 (pitch voting) already live in kind_robots — done.
- t-004/t-005 redirected: future rollback and deploy work goes in kind_robots roadmap.
- Standalone approval-portal app in projects/approval-portal/ is a redundant artifact; ignore it.

### digital-storefront  (software)
**Direction (rewritten 2026-07-05 from Silas's session direction):** ACTIVE again, and
now a build project, not a research loop. This is the digital giftshop that replaces or
expands the current kind_robots gift shop, backed by Stripe (deps already in kind_robots;
cart/mana/subscription components already exist). The v1 catalog is FIXED — Silas chose
it directly, no concept-picking cycle needed:
1. **Mermaids of Venice PDF** — Silas's novel, sold as a digital download ("third
   printing": minor word-choice/pacing edits in the first two chapters). First item to
   go live, as soon as Silas supplies the file and price.
2. **Kind Robots logo swag via print-on-demand** — the KR logo on whatever item is
   easiest to make orderable first (mug/tee/sticker). Longer waypoints: coordinate with
   the site's art gallery, and automate a POD pipeline so people can order swag printed
   with art created on the site (plus curated pieces later).
3. **Monthly supporter subscription** — recurring donation package.
4. **One-time mana top-ups** at a few reasonable levels.
5. **Against Malaria giving page** — must urge users to give DIRECTLY at
   https://againstmalaria.com/amibot rather than routing money through us.
6. **Example digital website unlock: two DLC packs** of generated website content
   (locations, genres, characters, rewards), built by the new `packmaker` project.
   Working names: **Uncanny Valor** (super-powers) and **Arcane Whimsy** (magic-powers)
   — Silas may rename.
**Notes:**
- Every outward step is still hard-gated: creating live Stripe products/prices/webhooks
  in production, creating POD accounts, publishing listings, or any spend = needs-human.
- product-types.yaml expanded 2026-07-05 to match the catalog above, recorded by the
  Reviewer from Silas's explicit direction in-session (Silas still owns the list).
- DLC unlocks depend on private-but-shared content infrastructure (see kind-robots
  roadmap t-008) — treat that DLC slice as a deliberate low-stakes security proving
  ground.
- `custom-calendar` is NOT approved. The Humboldt Impropriety Calendar pitch was passed
  (2026-07-02) — I have enough active projects. Pitch and scaffold are archived as
  brainstorm/inspiration; do not build calendar product types on their strength.

### mermaids-of-venice  (content)
**Direction (2026-07-05, Silas session):** ACTIVE. Scrap all prior AI-in-the-front-end
ideas — no AI features on the reader-facing surfaces, and no selective ordering of
parts. What this project actually needs:
1. **A simple kind_robots landing page** that offers the book. It carries (a) a
   personal note that Silas will write himself (placeholder until then), and (b) a
   note stating that no AI was used to write the book other than the words of that
   paragraph itself, ending on a punchline about reality/existence/originality.
2. **Editorial review pipeline**: Silas will drop the manuscript PDF into
   projects/mermaids-of-venice/manuscript/. From it, produce separate outputs:
   general impressions, editorial notes, cultural-awareness notes (gaps in gaze or
   privilege), and a VERY-IMPORTANT.md listing actual typos and grammar errors.
3. **Later:** build/expand the full site at mermaidsofvenice.com (currently a parked
   WordPress address). Parked until Silas is comfortable selling the book as-is.
**Notes:**
- The book's prose is Silas's craftsmanship alone. Agents advise as editors; they never
  draft prose intended for the book itself. Editorial insight is welcome; replacement
  words are not.
- docs/revision-questions.md captures the revision concerns Silas wants to dialogue
  about as the project evolves (third-act changes, character-origin question, tone).
  Handle that material with care — it is context for conversation with Silas, not a
  task list to "fix" the book.
- The PDF edition doubles as the digital-storefront's first product.

### packmaker  (software)
**Direction (2026-07-05, new project):** A repeatable, pipeline-aware generator for
"packs" of website content — locations, genres, characters, rewards — serving both
store DLC packs and general builder items. It should be a handle tool / front end that
knows the generation pipeline: different views for admin and user, packs tied to Silas
but private until released. First deliverable: the two digital-storefront launch packs
(working names Uncanny Valor and Arcane Whimsy — two words each, no alliteration, per
Silas; he may rename).
**Notes:**
- Private-but-shared packs are a deliberate low-stakes test of content security —
  coordinate with kind-robots sharing/ACL design (kind-robots t-008) rather than
  inventing a parallel permission system.
- Slug parity: create the matching PROJECT Dream via the sync script, slug `packmaker`.

### ai-art-academy  (software, autonomous: true)
**Direction (2026-07-10, new project):** Teach the history of art — movements, styles,
and creators — using ONLY public-domain art and dead artists; we don't rip off living
creators. Users pick a starter image or upload their own and remix it in a learned
style via the kontext network. kind_robots `components/art/art-styler.vue` is the
groundwork and becomes this project's front end at much bigger scope; the plain
art-styling tool stays available inside the Academy. One task hunts publicly available
LoRAs; agents may recommend a different engine if kontext loses on LoRA availability
vs model knowledge (current recommendation: Kontext-first — see DESIGN-BRIEF.md).
**This is the test run of the autonomous project initiative.** Claude has full reign
over this project and art-styler.vue. Art generation on our backend is fully supported
and pre-approved. Surface only actual human gates; keep running without my input
(never-idle rule). I'll check in occasionally to clarify.
**Notes:**
- Adjacent to sketchy (drawing instruction); shared KR token economy, separate projects.
- Living-artist/brand styles (Disney, Gorillaz, DB4RZ…) may stay in the free-play
  Style Lab but are excluded from the taught curriculum.

### coloring-book  (software)
**Direction (2026-07-10, new project):** Front-end coloring book app of AI-generated
coloring pages in kind_robots. Normal coloring-book uses plus AI: users generate their
own pages via kontext and/or a coloring-book LoRA. Include coloring book sets and
tokens for generator use beyond a free tier (aligned with the KR economy). Deserves a
tab in the art channel. Background art-asset generation is authorized: multiple
coloring book sets and whatever the app/front end needs. First two digital books:
**"Kind Robots"** (reuse kind_robots art assets as sources) and **"Monster Recast"**
(renamed from the working title "Spooktacular Monster Drag Party" in Silas's
2026-07-10 Worker session: an original gallery of gender-swapped, drag-reimagined
Hollywood monster archetypes — cast bible and 28-page plan live in
projects/coloring-book/sets/monster-recast/). Every page we create is
digital-storefront inventory — set up toward a print-on-demand service selling
physical coloring books (POD accounts, listings, and spend remain hard-gated).
**Notes:**
- Tech seed: the mural-design WonderLab color studio (kind_robots /mural, PR #135) —
  generalize/share the engine, don't fork it; mural-design keeps working.
- Humboldt Impropriety Society coloring book/calendar stay archived inspiration; no
  HIS set unless I explicitly re-approve. Launch sets are all-ages.

### humboldt-impropriety-calendar  (brainstorm — archived)
**Direction:** Not approved (2026-07-02). Retired in project-overrides.yaml; kept in
projects/ and pitches/ purely as inspiration. No task claims, no research, no outreach.
If I ever revive this, I will re-approve the pitch and answer its open questions myself.

### kind-robots  (software)
**Direction:** BOUNDARY.md approved (2026-06-30). App owns its own logic; the shared KR
backend is read-only/external. Backend changes become pitches, never direct edits.
Full roadmap is now active — see projects/kind-robots/roadmap.yaml.
**Notes:**
- Slug parity: Dream.slug is the universal key. Conductor project directory names must
  match Dream.slug values for PROJECT-type Dreams. No redundant FK fields — enforce
  via slug matching. The sync script (conductor/t-009) is the canonical
  conductor → kind_robots bridge; it upserts Dreams by slug and writes projectStatus.
- Project creation from front-end or LLM should produce a Todo for the Worker to
  scaffold the matching roadmap.yaml in conductor. Same slug, three surfaces.
- Treat the shared kind_robots backend as read-only/external. Propose backend
  changes as pitches in pitches/ — never edit the shared backend directly.

### global-ui  (software)
**Direction:** Define and build the shared user-facing interface for projects, tasks,
front-end TODOs, desired feature lists, honeydos, kaizens, approvals, and completion
history. Honeydos are global LLM-assigned user tasks; kaizens are project-specific prompts
shown while viewing a project. Desired features are orderable project wishlists that humans
or AI can add/adjust/reorder/promote without rewriting the project spec. Keep task creation
visible on the front end without creating a second source of truth.
**Notes:**
- Start by approving the vocabulary and presentation model before implementation.
- t-001 gate removed 2026-06-30: Silas pre-approves the spec direction — no additional
  human approval needed after the Worker writes the task surface spec.

### pinball-hero  (content)
**Direction:** Create practical build plans for a high-quality, efficient, partly 3D-printed
pinball machine. The final package should include parts lists, printable model specs/files,
and instructions at multiple price points. Optimize for a Bambu Lab A1-class printer and
comfortable/common off-the-shelf parts; flag safety, durability, and cost tradeoffs instead
of pretending every part should be printed.
**Notes:**
- Keep the first cycle focused on architecture and constraints before sourcing or CAD work.
- No purchasing, publishing, or safety-critical electrical recommendations without human review.

### brainstorm  (proposal)
**Direction:** Generate a few strong, specific, buildable pitches each cycle for me to vote
on — new products (within approved types), content series, revenue streams, and AI_Networker
upgrades. Quality over quantity. Don't repeat existing pitches.
**Genre / content guidance (agents follow this for content pitches):**
- (e.g. "comics: queer-positive, hopeful sci-fi, all-ages"; "RPG: rules-light, GM-friendly";
  "coloring books: nature + whimsy". Add/replace anytime — this steers content pitches.)
**Notes:**
- (your notes)

### career-transition  (content)
**Direction:** Help me land a better-paying tech job that pays me for the AI and dev skills I
already use as a hobby. Produce research, resume drafts, cover letter templates, and prep
materials. HARD GATE: nothing goes out, nothing gets posted, no applications are sent without
my explicit approval. Every task that produces outward-facing material ends at needs-human.
**Notes:**
- I've been coding since 1989 (TRS-80) and working with AI since 2001. Lead with that.
- The casino dealer background is 11 years of financial reliability and high-stakes composure — frame it, don't bury it.
- Remote-first roles, base >= $70k, AI-adjacent strongly preferred.
- kind_robots (Nuxt 3 / Vue / Prisma / TypeScript) and conductor (multi-agent orchestration) are the portfolio anchors.

### conductor  (software)
**Direction:** Improvements to the conductor / AI_Networker system itself — CI, scripts,
ops tooling. Keep changes small and reversible. Nothing outward-facing without needs-human.
**Notes:**
- (your notes)

### alexa-integration  (software)
**Direction:** Custom Alexa skill + local relay server for the Serendipity voice surface.
The stable product contract is `Serendipity: <request>` from local Echo devices. Support
custom LLM chat, Character roleplay, Dream story sessions, approved local music playback,
and safe project work. Use Dream.goal and Dream.waypoints for friendly project state;
use Conductor roadmaps for authoritative agent tasks. Draft/prototype locally first — do NOT
publish the skill, expose a live endpoint, touch DNS/secrets/billing, or bypass human gates
without needs-human approval. Auth via KR_API_TOKEN where appropriate, with user/JWT or
machine-auth questions handled explicitly before write actions.
**Notes:**
- This project should now build toward `projects/alexa-integration/docs/serendipity-voice-surface.md`.
- Voice can read goals/waypoints and draft Todos, but cannot approve, merge, deploy, publish, spend, or silently edit roadmap YAML.

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

### coat-dance  (content)
**Direction:** Revived as an active creative content project. Use Silas's original circa-2006
Humboldt State experimental coat dance video as the choreographic spine for an AI-assisted
hybrid music video. The source piece is a weird avant-garde physical-theater duet between
Silas and a black Goodwill trench coat, with object manipulation, juggling-adjacent movement,
spins, pantomime, and theatrical strangeness. Plan it in small, reversible steps: source
video ingest, beat/section mapping, style treatment, ComfyUI/LAX/Wan pipeline tests, section
remixes, restitching, music alignment, and final review.
**Notes:**
- Preserve the human/coat duet as the soul of the project; AI should expand and remix it, not erase it.
- First useful deliverable is a production brief and asset checklist so Silas can provide the source video and confirm music/style direction.
- Research practical beat transcription and slicing tools before rendering. Likely candidates include ffmpeg scene detection, manual beat sheets, pose/action analysis, and video-to-video workflow notes.
- No public release, paid tool spend, or final export decision without explicit Silas approval.

### media-watchlist  (software)
**Direction:** Parse + import Silas's personal media log, then surface it with browse,
stats, and integrations (Letterboxd, Comic Vine, Tautulli). HARD GATE: no affiliate
links and no public-facing pages without needs-human. Dummy/sample data only until
the real log is shared.
**Notes:**
- (your notes)

### serendipity  (software)
**Direction:** Story-weaving experience inside kind_robots, directed by Silas (2026-07-02).
The Serendipity bot uses dream vibes, LOCATION and GENRE dreams to spin a
second-person story with the user as protagonist; the story's questions advance the
real honey-dos and human-gated tasks of a chosen project. Build on existing
infrastructure (chat streams, Bots, Dreams, Todos). This project has write access to
develop the Serendipity component in kind_robots. Design brief first (t-001,
needs-human gate) before any code; task write-back (t-006) is also human-gated.
**Notes:**
- Coordinate with alexa-integration for the voice surface. Alexa owns the Echo/relay
  interface; Serendipity owns the story/chat/task-weaving experience.

### storymaker  (software)
**Direction:** Collaborative storytelling engine built on top of existing Kind Robots
data models. App-owned logic only; shared backend is read-only/external.
Start with the session data model (needs-human gate) before any play-mode code.
**Notes:**
- (your notes)

### davinci  (software)
**Direction:** Life simulator app/game/webgame built around branching life narrative,
pass/fail victory conditions, 1024 achievements/endpoints, milestone unlocks, ending
icons/heroes, and generated story art collections. Integrate with Kind Robots Characters,
Dreams, Chat, Art, and Milestones. Focus development on the achievement/milestone/ending
engine first so narrative generation has concrete targets.
**Notes:**
- Da Vinci may later share primitives with Storymaker, but do not merge them yet.
  Storymaker is the broader collaborative storytelling engine; Da Vinci is the playable
  life-sim ruleset with deterministic endpoints.
- Reuse the existing milestone system where possible. Each ending should link to a
  milestone icon/image path before proposing schema changes.
- The AI narrator can generate prose, choices, and art prompts; the app must own durable
  state, pass/fail outcome math, achievement rules, and unlock records.
