# CONTROL.md global notes and full directive wording

Preserved byte-for-byte from CONTROL.md's global overview at 5360148 when that overview was
machine-trimmed on 2026-11-27 (Silas: CONTROL.md "should definitely be machine trimmed").
CONTROL.md governs current direction. Load this file only when a task needs a directive's full
wording or one of the standing procedures in "Global notes" (slug parity, project-truth split,
goal/milestones, continuous lifecycle, briefs-as-direction, commercial-generation licensing,
creation-a-day fallback, cross-project collision risk); those procedures remain in force unless
CONTROL.md or a newer directive supersedes them. The "Right now" and "Priority order this week"
lines below are superseded: project order lives in `projects/priority.yaml`.

Original preamble:

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

**Playtest goal (Silas, 2026-11-15 PT, supersedes 2026-11-11):** Every HIGH-priority game should enter `playtest` once its **finite agent-owned roadmap** is genuinely complete: authored art/text delivered, playable gameplay/endings, build/QA and full playthroughs verified, and a usable game URL established. **Human playtesting is the next phase, not a roadmap task or a prerequisite verdict.** The roadmap ends at verified readiness for human trials. At that transition set Conductor `playtest/normal`, prefix the single indexed GitHub roadmap issue `[FLAGGED FOR HUMAN TESTING]`, and close it as completed while preserving its URL and evidence. Optional human-test feedback lives outside the finite build roadmap. No `needs-human` subjective-acceptance task is required for handoff. Publication, sharing, deployment, wider promotion, money and creative signoff still require their separate real human approvals. Later scoped fixes use `playtest_iteration: true`; unfinished original build work cannot be relabeled to hide it. Preserve high-priority ordering until the handoff.\n\n**Standing creative direction (Silas, 2026-10-11 PT):** Across character-led Kind Robots projects, design casts with a genuine range of body types, skin tones, racial and cultural backgrounds, gender identities and expression. Diversity is not a casting checklist or a set of personality stereotypes. Write distinctive, fully realized people with motivations, flaws, friendships, humor, expertise, agency and lived-in visual design. Preserve strong existing canon and art; reconcile designs rather than mechanically replacing them to satisfy labels. Accessibility and fairness require that a person's body/identity does not imply game-balance penalties. A focused cast may only have a few people, but the *world* should feel populated by different kinds of people. Specific project cast bibles decide individual characters.\n\n**Creative development focus (Silas, 2026-10-21 PT):** Ecotone: Weird Humboldt,
Emperor of Dust, Zuzu Gamebook, Zuzu Shifting Lands, Shifting Desks,
Rainbow Space Princess, and Save the Plumber. **These seven are one focused
portfolio, not an internally ranked list.** Prioritize their story quality,
meaningful choices, gameplay, tests, and image-led presentation in ordinary
agent task selection. Preserve their previous relative queue order as a stable
tie-breaker; do not infer personal ranking from the way Silas listed them.
Other projects remain in their existing lifecycle states, but do not displace
the seven for discretionary creative work. Scheduled operational commitments,
security fixes, and review/merge work remain governed by existing policies.
This is not permission for a public launch, billing, or irreversible changes.



**Priority order this week:** rainbow-bullet-hell-space-princess → save-the-plumber →
kind-pinball → zuzu-lair → kr-arcade → zuzu-showdown → memory-dungeon →
cthulhuquarium → kind-economy → comet-city-academy → butterfly-gallery → art-archive.


The detailed project-specific directives formerly in this overview now live in the corresponding
project block below (including their supersession history). Read only the assigned block.
The pre-split original is preserved verbatim in [CONTROL history](docs/agents/control-reference-2026-11-26.md).
The current file, not the archived history, governs work.

**Daily creative commitments (separate assignment):** Daily Dream/digest, Dead Air, the five
daily approved-project improvements, and Animation Manager's daily creation remain independent.
The current production contract and its exact source directives are in
[Daily creative direction](docs/agents/daily-creative-direction.md). Load it only for that assignment;
do not revive stopped rituals or count queued assets as delivered.

**Daily creative commitments:** Daily Dream/digest delivery remains the top scheduled
creative commitment. Immediately below it, animation-manager/t-007 gets one Pacific-calendar-day
attempt to ship a genuinely new screensaver before ordinary backlog pickup. Review and broken-work
recovery still outrank it. Its other research/maintenance tasks remain continuous fallback work.

**Continuous fallback order:** animation-manager, then dream-cycle. (kr-arcade left this tier
2026-10-07: Silas made it a HIGH-priority active project, so its game factory kr-arcade/t-009 is
now lead work rather than fallback.) Outside the explicit
animation-manager/t-007 daily-commitment exception above, finite `active` work always outranks
`continuous` programs; dream-cycle remains the final idle fallback.
**Never idle (2026-09-29):** a run never ends on "nothing to do". When queues are empty, walk
docs/agents/role-assignment.md's fallback ladder — continuous tasks, dream docket, art, polish,
bug hunts, old pitches, new objects, new pitches — and ship one unit.

**Standing rules for all agents:** Respect each project's `kind`. Honor `depends_on` gates.
Never expand product-types.yaml — pitch it. When unsure, do less and escalate to
needs-human.

**Human gate clearance rule:** If Silas explicitly clears a human-gated task in the current
ChatGPT/GitHub session and the agent verifies that the roadmap standards are complete, the
agent may set `approved_by_human: true` and `status: done` with a note citing that clearance.
This does not authorize publishing, deploys, billing changes, DNS/secrets work, app-store
submission, destructive database actions, or other irreversible/outward-facing actions unless
Silas explicitly approves that concrete action too.

**Default-recommendation rule (Silas, 2026-09-30, in session):** a reversible product-decision
gate with a written agent recommendation is adopted after 7 days without an answer. This never
covers money, publishing, legal, security, irreversible, secrets, or physical-access gates. See
docs/agents/human-gates.md.

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
- Continuous lifecycle (2026-08-07; animation exception 2026-09-23): `continuous`
  is the explicit never-idle program status. Continuous projects normally run only after every
  finite `active` project has no claimable ready work. The explicit exception is
  animation-manager/t-007: when its `daily_last_checked` predates today's Pacific calendar
  date, select_role.py surfaces it as `daily-creative` ahead of ordinary backlog/audit work.
  Review and broken-work recovery still come first. Other Animation Manager work and dream-cycle
  retain normal continuous behavior, with dream-cycle always last. The AI Art Academy autonomous
  test is concluded; Academy is finite active work and must stop inventing polish/content tasks
  when its real roadmap queue empties.
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

- **Full-game playtest readiness (Silas, 2026-11-26 PT):** fully developed art-first single-screen games, original generated artwork AND icons (no SVG art or placeholder icon sets), front page/settings, global account saves, achievements (12+ main/3 small), scrapbook equivalent, appropriate endings/replay, sound/music and adversarial full-game/device QA. Apply [main-game-standard.md](docs/agents/main-game-standard.md) for relevant scopes, not a duplicated checklist. Verified readiness precedes human playtesting; subjective approval and publication stay separate.
