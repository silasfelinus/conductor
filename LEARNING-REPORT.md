# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-19T03:00:25Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **685**
- Outcomes: blocked: 15, cancelled: 1, done: 669
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 8 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 15 | 93% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 76 | 100% |
| conductor-app | 4 | 100% |
| davinci | 4 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 32 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 70 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 13 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 669 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-19 `kapowarr/t-054` — Bound remote metadata resolution as a whole and pair every loading state with success and rejection exits; source health data should be visible before acquisition.
- 2026-08-19 `model-builder/t-029` — Twelfth cycle of this recurring bug-hunt task. The suggested accessibility lead from cycle 11 was genuinely exhausted (both target components already covered or not applicable), and the fallback -- read a genuinely fresh file (the store) rather than re-walking already-audited components -- surfaced a real sibling instance of a bug class an existing guard already covered for other functions (verifyModelBuilderAutoBuildFailedSummaryGuard's TARGET_FUNCTIONS list). When a guard is written against an explicit function allowlist, a later cycle should periodically check whether new or overlooked functions with the same shape are missing from that list, rather than assuming a fixed guard covers a whole bug class permanently.

- 2026-08-19 `kapowarr/t-036` — check_pr_merged_drift.py's gh-search fallback 403'd in this sandbox, but the GitHub MCP pull_request_read "get" method (as opposed to list_pull_requests, which reported merged:false for the same closed PR) confirmed silasfelinus/Kapowarr#56 was in fact merged directly by Silas. When the drift script can't verify a candidate via its own HTTP path, cross-check the single-PR MCP get method before treating it as unresolved -- the list endpoint's merged field is not reliable evidence on its own. Concurrent race note: by the time this reconciliation PR reached CI, origin/main had already picked up the same task's real close-out (with the full implementation note and squash SHA) from another session -- resolved by keeping origin/main's roadmap content and both LEARNING.yaml entries side by side rather than picking one.

- 2026-08-19 `kapowarr/t-036` — When matching release issue numbers, verify the exported helper name rather than trusting its stale docstring example; the dependency-backed import matrix catches this immediately.
- 2026-08-18 `kapowarr/t-047` — Scheduled tasks must record failure outcomes before leaving the queue, and scraped sources require live markup verification.
- 2026-08-18 `brainstorm/t-018` — A persona-recovery task with an open-ended "add flavor" instruction doesn't require inventing anything -- audit the live database first. The real, already-generated Brainbot Bot record (art, tagline, voice) sitting unused was a stronger fit than restoring a legacy gitignored asset or a stale seed-script record that never populated production. When multiple candidate sources of truth exist (a seed file, a content .md, a live DB record), the live DB record wins if it actually satisfies the ask -- verify what's live via the site's own API rather than trusting the most convenient-looking file in the repo.

- 2026-08-18 `brainstorm/t-015` — A "run prettier --write across the whole file" reflex on a large existing file can silently launder unrelated pre-existing debt into a scoped PR -- confirmed here via git stash that the file already failed prettier --check on main before any edits, and the full-file reformat broke an unrelated test's fragile literal-text regex match by reflowing a paragraph never touched by this task. Fix: after --write, check git diff --stat -- if it's far larger than the authored content, revert to HEAD and reapply only the substantive edits by hand. When adding a field orthogonal to an existing config axis (e.g. output "domain" vs. style "mode"), keep it a separate field rather than overloading the existing one's value space -- easier to reason about and compose.

- 2026-08-18 `brainstorm/t-014` — When a task's own scope comment lives in the code ("X is wired today, Y is <task-id>'s scope -- add a resolver here"), that comment is the actual spec, more precise than the roadmap note. For a "wire an additional lightweight adapter" ask that has two halves (a picker adapter and a context-grounding resolver), wire both for the new entity rather than just the minimum picker half -- a picker-only addition reproduces the exact "shows up but doesn't ground generation" gap the task exists to close for the first entity. Also worth checking whether a script you're substantially extending was ever actually wired into CI (verifyBrainstormSourceContext.ts, added in t-013, had never been) -- fixing that gap costs little once you're already touching the file.

- 2026-08-18 `appmaker/t-013` — Kaizen audit tasks ("check whether the same gap exists elsewhere") are cheap to close honestly when the answer is no -- read the one other conductorStore-driven list on the page (pending scaffolds), confirmed it renders no description field at all so the stale-literal gap t-012 fixed can't recur there, and swept the wider tree for any other appmaker-owned list before concluding "verified no-op." Closed via close_task.py with the audit trail in the note rather than forcing an unnecessary diff.

- 2026-08-18 `alexa-integration/t-015` — This project's recurring self-audit of serendipityVoiceStore.ts has now found three distinct bug shapes across four cycles: false acknowledgements from action/target mismatches (t-015/t-020), missing error-reporting regression coverage (t-021), and this cycle's missing acknowledgement on an otherwise-correct success path (applyArtCommand() never called postAck() at all, so a fully successful voice-driven art draft got no spoken confirmation back through the relay -- the mirror image of the false-success bugs, not a repeat of them). Comparing each dispatch function against its siblings for a missing behavior, not just a wrong one, is what surfaced it. Also reconfirmed the appmaker/t-012 lesson from 2026-08-16: a single CI job failing with a live 502 to kindrobots.org (this time in the Comment Migration Contract workflow, hitting /api/bots on rerun after /api/characters on the first try) is a transient, diff-unrelated production flake -- confirmed directly via curl against the live host before merging past it, rather than assuming or guessing.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-19T03:00:25Z_
