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

**Priority order this week:** interface-vision → ai-art-academy → coloring-book →
humboldt-scoop-cms → digital-storefront → mermaids-of-venice → kind-robots →
kindrobots-unraid.

**Continuous fallback order:** animation-manager, then dream-cycle. Finite `active` work
always outranks `continuous` programs; dream-cycle remains the final idle fallback.

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
  kind_robots **Project** record (the Dream model split into Dream / Project /
  Facet in July 2026 — Dreams no longer carry project state). `conductorSlug`
  on the kind_robots Project is the universal join key across the conductor
  file system, kind_robots database, front-end UI, and LLM. When creating a
  project from any surface (conductor roadmap, front-end form, LLM), produce a
  kind_robots Project with matching conductorSlug and update conductor
  accordingly. The sync_projects.py script is the canonical conductor →
  kind_robots bridge (upserts via GET/POST/PATCH /api/projects). Do not add
  redundant FK fields — enforce via slug match.
- Do not invent a second source of project truth. Conductor roadmap.yaml is the
  authoritative task record; the kind_robots Project is the authoritative
  display/identity record. conductorSlug is the join key.
- kind_robots Projects expose `goal`. Treat `goal` as the friendly definition of
  done. Roadmap `milestones` are the structured progress buckets that flow into
  the kind_robots front end (read-only). Conductor roadmap.yaml remains the
  authoritative agent task queue; milestones are the UI/voice progress layer and
  should not replace roadmap tasks.
- Continuous lifecycle (2026-08-07): `continuous` is the explicit never-idle program
  status. Continuous projects run only after every finite `active` project has no claimable
  ready work. Initial continuous programs: animation-manager and dream-cycle, with dream-cycle
  always last. The AI Art Academy autonomous test is concluded; Academy is finite active work
  and must stop inventing polish/content tasks when its real roadmap queue empties.
- Briefs are direction, not contracts (Silas, 2026-07-10): projects evolve. When
  Silas's later commits or direction supersede a design-brief detail (e.g. Monster
  Recast's 32-38 page homage pool replacing its original 28-page plan), run with
  the newer reality and refresh the brief opportunistically — don't stall on or
  re-litigate the older document.
- Commercial-generation licensing rule (Silas, 2026-07-10, refined same day from
  ai-art-academy t-011): STANDING DEFAULT, no per-case debate needed — anything
  generated for commercial use (paid generation tiers, storefront/POD inventory,
  DLC packs) runs on either a license-unencumbered backend we host (e.g. FLUX.1
  schnell, Apache 2.0) or OpenAI/ChatGPT image generation otherwise (its terms
  allow commercial use of outputs; it's already the art-prompts.yaml pipeline).
  Officially supported licensed endpoints (BFL Kontext pro/max API, fal/Replicate)
  remain an approved variant of "otherwise" where OpenAI doesn't fit. FLUX.1 dev,
  Kontext dev, and dev-trained LoRAs never touch commercial output. Free-tier,
  educational, and internal generation continue unchanged on the current stack.
- Creation-a-day idle fallback (2026-07-10): dream-cycle sits LAST in priority.yaml.
  When no other active project has ready work, its recurring task builds the site's
  next creation (~one per day, art included) from the human-steerable backlog in
  projects/dream-cycle/backlog/. Creation types are pluggable playbooks: dreams
  (location + vibe, characters, rewards, scenarios, optional narrator with
  expressions/topics/threads) and coloring-book production days, more later. Silas
  steers by leaving notes in those files; agents fold notes in before every stage
  and never edit them.
- Cross-project same-task collision risk (2026-07-17, kind-robots/t-012 +
  digital-storefront/t-012): the same real piece of work is sometimes tracked by two
  different project roadmaps (a task note saying "blocks X in another project" or
  "cross-repo, tracked in both roadmaps"), with no `depends_on` link between them
  since that field only resolves within one project. Before implementing a task whose
  note references another project's task, skim that other project's roadmap/recent
  PRs too, not just `claim_task.py`'s own-project check — two sessions converged on
  near-identical implementations the same hour here, caught only by the routine
  fetch-before-push step.

---

## Per-project direction  ← agents read the block for the project they're working on

### superkate-services-calculator  (software)
**Direction:** Private app for Superkate / Hair by Superkate. Build a private,
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

### ai-art-academy  (software)
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

### mona-salai  (software, autonomous: true)
**Direction (2026-07-26, new project):** Build a heavily sourced Kind Robots research page
investigating the theory that Leonardo's Mona Lisa used Salaì as a model or incorporated
his facial features. The project must be allowed to support, weaken, contradict, or leave
the theory unresolved. Start with the historical record and existing scholarship, then
run reproducible computer-vision experiments on public-domain artwork—especially Saint
John the Baptist—using facial embeddings, manually reviewed landmarks, craniofacial
proportions, and cautiously framed 3D-aware analysis.
**Notes:**
- The documented Lisa del Giocondo identification is the mainstream historical baseline.
  Computational resemblance cannot erase documentary evidence.
- Paintings are not biometric photographs. Test models on painted-portrait controls and
  measure same-artist/style leakage before interpreting similarity scores.
- Prefer "facial geometry" or "craniofacial proportion analysis" over "bone analysis"
  unless a method genuinely recovers defensible 3D structure.
- Pre-register comparisons and publish controls, negative results, model versions,
  transforms, annotations, score distributions, and uncertainty. No magic AI percentage.
- The reader-facing page should feel like an open research notebook, not a conspiracy kiosk.
- Public-domain museum scans only for the core dataset. Expert outreach and public release
  remain human-gated outward actions.

### dream-cycle  (software, autonomous: true)
**Direction (2026-07-10, new project; generalized same day):** The creation-a-day
idle fallback — testing a new option for conductor sweeps. When there isn't
anything better to do, agents make something for the site, ONE creation at a time,
~a day each including all art generation. Creation types are pluggable playbooks
in `projects/dream-cycle/specs/`; v1 types:
- **dream** — a location and a vibe, each with characters, rewards, and scenarios;
  optionally a bot narrator with expressions, topics, and threads.
- **coloring-book** — "spend today drafting and making a coloring book": advance a
  book set through the coloring-book project's production sequence. First book:
  Monster Recast (gender-bending Hollywood movie monsters, already design-ready in
  projects/coloring-book/sets/monster-recast/).
The backlog of outlines lives in `projects/dream-cycle/backlog/` — accessible files
where I leave notes and flip status/priority to steer, park, or veto ideas.
**Notes:**
- Infrastructure first: API audit (t-003), CREATION-SPEC + dream playbook (t-004),
  coloring-book playbook (t-009). The recurring build task (t-006) waits on t-004.
- Only ONE creation may be `building` at a time. Backlog stays ≥5 buildable outlines.
- Delegation rule: types owned by a home project (coloring-book) keep content in
  that project; the backlog file is only the scheduler card + my steering surface.
  Never double-claim a home task the Worker already holds.
- All kind_robots data models already exist — no schema work. API gaps become
  kind_robots tasks/pitches, never direct backend edits.
- My backlog-file notes are agent-read-only: fold them in, never edit or delete them.

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
Hollywood monster archetypes — now a 34-concept homage pool targeting 32–38
interior pages, produced colored-master-first per sets/monster-recast/STYLE-GUIDE.md).
A third book, **"Hollywood Recast 2"** (classic movie-scene grammar recast through
gender/body/age/presentation; first seed Highland Heatwave), is scaffolded but
PARKED in sets/hollywood-recast-2/ — no claims, generation, or scheduling until
Silas activates it. Every page we create is digital-storefront inventory — set up
toward a print-on-demand service selling physical coloring books (POD accounts,
listings, and spend remain hard-gated).
**Notes:**
- Approved designs are locked: sets/monster-recast/approved/manifest.yaml is the
  source of truth for Silas's confirmed masters. Run
  `python scripts/coloring_approved_status.py --check` before set work; never
  regenerate an approved design for production (exploratory queue stays active).
- The dream-cycle idler may spend idle days advancing this project's set-production
  tasks (Monster Recast first) under its delegation rule: content stays here, the
  idler updates both records, and never double-claims a task the Worker holds.
- Tech seed: the mural-design WonderLab color studio (kind_robots /mural, PR #135) —
  generalize/share the engine, don't fork it; mural-design keeps working.
- Humboldt Impropriety Society coloring book/calendar stay archived inspiration; no
  HIS set unless I explicitly re-approve.
- Content ratings are per-set (updated 2026-07-10 from Silas's direct commits,
  superseding the earlier "launch sets are all-ages" note): "Kind Robots" stays
  all-ages; Monster Recast is progressive teen horror (~PG-13) per its README;
  Hollywood Recast 2 is teen/adult (~PG-13). New sets default all-ages unless
  Silas's set README says otherwise.

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

### brainstorm  (software)
**Direction (rewritten 2026-08-10 from Silas's session direction):** Restore Brainstorm as
a first-class Kind Robots creative ideation tool at `/brainstorm`, with `/plan/brainstorm`
resolving to the same product. The essential interaction is pitch → ask for X ideas → curate
individual results → edit/keep/reject/regenerate/branch → save/reuse. Text quality comes first;
object-aware variations and optional Krea2-backed art generation follow once the ideation loop
is genuinely useful.
**Notes:**
- Recover the historical interaction, persona, useful data flow, and product identity. Do NOT
  use the old LLM generations as a quality standard. Silas hated those outputs; they are the
  floor to beat, not examples to imitate.
- Historical prompts/system text/output may be preserved as archaeological evidence and
  negative fixtures, but never as positive few-shot examples or a reason to preserve obsolete
  prompting. Reevaluate prompting against current model/provider capabilities.
- Judge creative quality on relevance, semantic diversity, specificity, surprise, constraint
  following, editability, and actual comic/creative premise. Random weird nouns, noun-swapped
  paraphrases, corporate-list sludge, and repetitive LLM templates are failures.
- The product supports practical ideation and playful absurd/dark-comedy improv. Do not sand
  allowed material into a generic cheerful-assistant voice.
- The internal Conductor pitch generator is no longer this project's definition. If retained,
  it becomes an explicit downstream consumer of the user-facing Brainstorm engine and never
  silently turns normal Brainstorm sessions into Conductor coordination data.
