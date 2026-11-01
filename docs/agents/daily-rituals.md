# Daily rituals and the session report — full text

> Moved verbatim from `CLAUDE.md` on 2026-11-01 PT (token-essentialization pass 2). CLAUDE.md is
> injected into every session's context, so it now keeps a one-line pointer per ritual and this
> file holds Silas's full directions. Open the section for a ritual only when that ritual is due.
> Numbering matches CLAUDE.md's startup sweep.

## Startup sweep steps 7–9 (dream docket, daily upgrades, playbook challenge)

7. Dream docket: `session_sweep.py` runs `build_dream_proposal.py --check --fetch`. **Sessions own the
   docket** (the API author step is opt-in via `daily-digest.yml`'s `spend_api_credits`). If it reports
   fewer than 5 (`TARGET_BUFFER_DAYS`) unbuilt proposals, author exactly ONE this session with the
   `--brief` → `--from-json` recipe — never more than one per session; a full docket means leave it alone,
   and a day with no proposal dated today is normal. Exit 1 means the docket is **empty**: author one now.
   The authoring contract (six linked originals plus eight extra Zuzu assets from 2026-10-13 PT, preserve `seed_facets`, Scenario last, complete-sentence card copy
   per `scripts/dream_prose_quality.py`) and the history behind it are in `docs/sweep-checks.md` (Step 7)
   — read that section before authoring.

8. Daily upgrades, effective 2026-10-13 PT (Silas's superseding direction):
   **Build first, review afterward.** The five extra digest entries are NOT
   speculative pitches or roadmaps. Choose existing approved ACTIVE projects
   and ship five small, reversible, CI-tested improvements where possible:
   Arcade stages/enemies, fighter moves, gamebook branches, Shifting Lands
   cards, Emperor of Dust encounters, and similar additions.
   Claim scoped source tasks, implement, open PRs, inspect completed CI, merge
   safe green work, link playable previews and actual rendered art or ArtJobs.
   If unfinished, report real implementation PR and next step as in-progress;
   neither ideas nor queued art count as finished.
   Run python scripts/daily_project_deliveries.py --brief, author five
   evidenced entries at projects/dream-cycle/daily-deliveries/<Pacific-date>.yaml,
   then --materialize and --check before the morning digest.
   The signed inbox handles Keep / Modify / Reject AFTER implementation.
   --feedback is the agent queue for modifications and scoped tested rollback
   PRs. Reject does not destructively remove live data. Existing hard gates
   for secrets, billing, DNS, publishing and irreversible operations remain.
   The original six-linked Daily Dream and eight additional Zuzu assets
   remain separate from these five project improvements.
   Never rewrite historical pitch votes. For old intake only,
   python scripts/daily_pitches.py --approved preserves legacy behavior.
   dream-cycle/t-035 is the recurring build-and-report commitment.
   **Audience-first window, 2026-10-26 → 2026-11-25 PT** (Silas, 2026-10-26, after a
   fresh-visitor audit found ~15 polished games but almost no outside players): at
   least three of the five daily upgrades must help a first-time visitor find,
   understand, share or support the site (front door, link previews, share/give
   prompts, review flow, drop-offs seen in `/admin/site-stats` or playtest notes).
   New content counts only when it fixes something real players hit. Backlog:
   interface-vision t-150, t-151. The `--brief` prints this until the window ends.

> **STOPPED 2026-10-29 PT** by Silas (CONTROL.md "2026-10-29 PT daily creative correction"):
> do not author new playbook-challenge dockets. The text below is kept as the historical direction.

9. **New-playbook challenge, separate from the five shipped daily upgrades:**
   Every Pacific day, review the current authored Kind Robots Playbook Studio
   registry (`kind_robots/utils/playbook/games.ts`) plus current active game
   DESIGN-BRIEFs (including **Prom of Doom** and **This Means Warp** even before
   they enter the Studio). Run `python scripts/daily_playbook_challenge.py --brief`
   and author **exactly three evolving pitches** at
   `pitches/playbook-challenges/<Pacific-date>.yaml` with production costs.
   **Persistent concept memory (Silas, 2026-10-26 PT):** Every day build on
   yesterday AND the entire history, rather than inventing three disconnected
   ideas. Use `python scripts/daily_playbook_challenge.py --memory` and
   the `--brief` full-history curator shelf, plus
   `pitches/playbook-challenges/MEMORY.yaml` for human/editorial decisions,
   strengths, objections and next moves. Silas's notes from the Playbook Forge's
   Gestation screen (`pitches/playbook-challenges/SILAS-NOTES.yaml`) are listed
   first by `--brief`; answer open notes before anything else and mark each one
   `addressed` with `addressed_in: <date>/<slug>`. Choose each slot freely from
   `new` (unoccupied genre), `expand` (a meaningful revision of one
   older concept, same permanent ID), or `meld` (a justified fusion of
   at least two DIFFERENT older concept families, new permanent ID).
   Do not force a fusion or a novelty-only idea; once a prior concept exists
   at least one of the daily three must advance a previous lineage.
   Each entry records stable concept_id, mode, dated parent version refs,
   substantial design evolution, what to preserve, what to question and
   two+ next-day creative questions. Historical date files are snapshots,
   not things to rewrite; editorial memory is the separate living index.
   Never imply a rejected pitch is active without a conscious editorial
   status change. Run `--check --date YYYY-MM-DD` before digest handoff.
   **Genre-first calibration (Silas, 2026-10-26 PT):** Do not select a narrow
   unusual mechanic and call it a complete new game. Map the broad genres
   already occupied (Weird West, post-apocalypse, superheroes, slice of life,
   theatre of place, dark comedy, psychedelia) and prioritize missing
   long-form genre pillars. The first three requested gaps are an original,
   family-friendly children's literary wonderland (playful nonsense,
   friendship and adventure, no romance), **cyberpunk with deeply mechanical
   body evolution and human selfhood**, and **Heaven/Hell final-soul judgment
   simulation** with evidence, eternal consequences and appeal.
   Explicitly state genre, gap, audience, multi-act world scope, emotional
   promise and at least three substantial genre-defining systems. Re-reading
   and copying earlier fantasy pitches is not enough; do not imitate named
   writers or copyrighted characters. Specify playable opening choices;
   disjoint NPC/follower cast; emotional/injury/evolved portraits; maps;
   encounter, friendship, optional romance, villain, transformation and
   finale art; prose beats and processing-pass assumptions; at least three
   explicit seeded-state × authored/optional LLM prose × selected/generated
   art collisions and their actual gameplay consequences.
   Validate exactly three each day; reuse is allowed only via explicit,
   substantial expansion or fusion with discoverable lineage, never as an
   unmarked fresh proposal. Do not call missing/invalid entries authored.
   Sessions write the dated creative docket,
   **not** the scheduled workflow (paid authoring remains opt-in).
   A pitch is a proposal for Silas, not approval to create projects, start
   ArtJobs, pay for models, publish, or replace the five shipped upgrades.

## Full session-report checklist

Then report:
- **Branch** and whether the working tree is clean
- **Open PRs** (if any Worker PRs are waiting for review)
- **Ready tasks** (what the Worker should pick up next, in priority order)
- **Priority-queue depth** (only when `check_priority_queue_starvation.py` exits non-zero): how many
  projects the queue walked past before landing on real work, and why each was skipped
- **Needs-human gates** from active projects only (what only Silas can unblock, grouped by project)
- **State reconciliation** findings (merged-PR drift, stale-gate signals, or milestone/task mismatches)
- **Projection headroom**: the `check_roadmap_note_size.py` payload line (bytes used against the
  4,000,000 limit, and headroom). Report it every session — it is the repo's only hard ceiling, and
  when it broke on 2026-09-11 nothing had warned that it was close
- **Art queue health**: the `art_queue_health` sweep line — failed art the last Auto Art Generate run
  could not render (its green check hides them). Non-zero means `art-medic` work; name the counts by kind
- **Container log triage** (Alexandria): new/spiking/newly-quiet log signatures, or a stale
  digest meaning the daily User Script stopped running — omit entirely when not configured yet
- **Any unresolved escalations** from TALKBACK
- **Creation fallback**: any delegated non-dream scheduler card currently
  `building`, its authoritative home-project stage, and any new Notes from Silas
- **Daily dream**: whether today's dated proposal exists; its steering/build/retry,
  Facet, art, and digest state; legacy Dream outlines are idea inventory rather
  than queued object builds (warn when useful idea inventory falls below five)
- **Daily upgrades**: report five PR-backed shipped/in-progress additions, actual CI runs and merge SHA, playable and art evidence, plus the modifications/rollback feedback queue (daily_project_deliveries.py --check / --feedback). Historical decisions remain in daily_pitches.py --approved.
- **New playbook challenge**: dated 1–3 new-game proposals or honest missing/invalid status; explain the unoccupied GENRE pillar and three+ genre-scale systems before novelty mechanics; quantify unique render targets and authored scenes separately from LLM tokens, and do not imply approval.
- **Daily Tzaddik**: from the sweep's `tzaddik_review` section (`python scripts/tzaddik_review.py --check`
  for the full list), report the
  approved/rejected/deferred/pending counts across every discovery docket. List
  any pending suggestions so Silas can act with `--decide "Name"
  approved|rejected|deferred` (or by hand-editing
  `projects/tzaddik-gallery/discovery-decisions.yaml`, the same pattern as any
  other roadmap-adjacent field Silas edits directly) — a rejected/deferred name
  never boomerangs back into a future docket once decided
