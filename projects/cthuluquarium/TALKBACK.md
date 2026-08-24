# TALKBACK.md — cthuluquarium

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

## 2026-08-24 | Reviewer → Worker | cthuluquarium/t-001 | pattern

**Subject:** Project scaffolded from KR Todo #1320; game-client repo is out of session GitHub scope.

**Detail:**
- Kind Robots Project 2112 (`cthuluquarium`, BRAINSTORM, liveUrl `/aquarium`) already exists —
  this roadmap only adds the conductor-side counterpart per PROJECT-CREATION.md Surface 2.
- `repoUrl` on the Project record is `https://github.com/silasfelinus/cthulhuquarium`, which is
  not in this session's repo scope (conductor/kind_robots/Kapowarr/humboldtscoopsolutions only).
  t-001's note asks the Worker to produce conductor-side handoff docs for game-client work until
  access is confirmed, per AGENTS.md's "Cross-repo tasks" section — not to substitute a different
  repo (e.g. kind_robots) without Silas's direction.
- Todo #1321 ("infrastructure on kind robots, access page, Play directory") was left unhandled
  this cycle — it's NORMAL priority behind #1320 and scoped as kind_robots-side follow-up work
  that fits naturally as a BUILD-milestone task once t-001's design brief lands; not created here
  to avoid guessing at implementation shape before the brief exists.

**Suggested action:** Next session handling t-001: confirm repo access before assuming a target,
and turn Todo #1321 into a scoped m2/m3 task once the design brief clarifies what "access page"
and "Play directory" integration actually require in kind_robots.

## 2026-08-24 | Reviewer → Worker | cthuluquarium/t-004 | pattern

**Subject:** Todo #1321 turned into a scoped m2 task instead of deferred further.

**Detail:**
- Researched the actual kind_robots routing/content mechanics (Play channel tabs are
  Nuxt Content frontmatter under `content/channels/play/*.md`, resolved by
  `resolveChannels()`; a project access page is `content/{slug}.md` + a manager
  component, with `components/conductor/project-front-page.vue` as a reusable shell)
  before writing t-004's note, rather than leaving the todo open indefinitely on the
  earlier "wait for the design brief" assumption from the prior entry above.
- This turned out to be pure routing/plumbing with no art or design-brief dependency —
  confirmed `/aquarium` currently 404s (no content file, no page, no
  `projectPlacements.ts` entry) — so t-004 is `ready`, not `waiting`, and can proceed
  in parallel with t-001/t-003.
- Flagged in t-004's note: `sample/new-section.md` step 6 tells implementers to add
  `liveUrl`/`channelKey`/`tabKey` to `conductor/project-overrides.yaml`, but root
  AGENTS.md's "Project identity and source of truth" section says kind_robots owns
  those fields directly (`PATCH /api/projects/{id}` or `PROJECT_PLACEMENTS`). This
  project's own `project-overrides.yaml` entry already carries `liveUrl: /aquarium`
  as an informational mirror, consistent with how other projects' override entries
  are commented ("synced ... by sync_projects.py").

**Suggested action:** Worth a small doc fix in `sample/new-section.md` step 6 to stop
pointing implementers at the stale `project-overrides.yaml` instruction — left as a
future kind-robots docs task rather than done here (out of scope for this cycle).
