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

### First push of a session fails with HTTP 413

If `git push -u origin <your-branch>` fails with an HTTP 413 from the git-smart-HTTP
proxy on the *first* push of a session, and the branch has never had a PR opened from
it, the branch likely doesn't exist on the actual GitHub remote yet — even if your local
checkout's remote-tracking ref shows a SHA for it (that's stale/local-only knowledge).
`GIT_TRACE_CURL` will show the proxy attempting to send a full-history pack (matching
the whole `.git` size) instead of a small delta, apparently because a brand-new ref
needs a full pack rather than one computed relative to objects already reachable via
other refs (e.g. `main`).

Workaround: call the GitHub MCP `create_branch` tool (`owner`/`repo`/`branch`/
`from_branch: main`) first — this creates the ref instantly via the API with zero data
transfer, since it just points at a commit the remote already has. Then the normal
`git push` of your session's actual commits goes through as a small, fast delta.
