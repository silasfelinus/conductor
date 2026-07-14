# CLAUDE.md

The operating manual for this repo is **[AGENTS.md](./AGENTS.md)** — read it in full at the start of every session. It applies to all agents (Worker and Reviewer) across all projects.

## Session startup

At the start of every session, before responding to any task, run a conductor sweep and report it to Silas:

1. Read `AGENTS.md` in full
2. Run `git status` and `git log --oneline -5`
3. Check for open PRs (use GitHub MCP tools if available)
4. Scan all `projects/*/roadmap.yaml` for tasks with `status: ready`, `status: needs-human`, or `status: claimed`
5. Check `TALKBACK.md` tail for any unresolved escalations or security flags
6. Run `python scripts/build_dream_proposal.py --check`. If today's daily-dream
   proposal is missing, YOU author it — you are the generator (no API calls,
   no scripts doing the creative work): run `--brief` for the spec and slugs
   to avoid, invent the starter dream yourself (3 characters, 2 locations,
   1 narrator bot, 2 rewards — one SKILL, one ITEM — all one world), then
   write it with `--from-json` and commit it with your session's log commits.

Then report:
- **Branch** and whether the working tree is clean
- **Open PRs** (if any Worker PRs are waiting for review)
- **Ready tasks** (what the Worker should pick up next, in priority order)
- **Needs-human gates** (what only Silas can unblock, grouped by project)
- **Any unresolved escalations** from TALKBACK
- **Dream cycle** (idle fallback): the active `building` creation (type + next
  stage), or — if none — the next queued outline in `projects/dream-cycle/backlog/`;
  flag any new Silas notes in backlog files and warn if buildable outlines < 5
- **Daily dream**: whether today's proposal exists (and if you just authored it,
  say so with its title + edit link)

After the report, ask Silas what he wants to work on — or proceed directly if his first message is already a clear task.

## Session end

Before ending: push any TALKBACK/roadmap log commits and make sure the session branch has a PR — log commits stranded on an unPR'd session branch never reach main and get lost.
