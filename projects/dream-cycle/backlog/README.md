# Dream Cycle backlog

One file per dream idea. This folder is the shared steering surface between
Silas and the agents — outlines wait here until idle capacity builds them.

## File format

Copy `_template.md`. Frontmatter drives the queue:

| field      | values                                                     | who sets it |
|------------|------------------------------------------------------------|-------------|
| `status`   | `outline` → `approved` → `building` → `built` (+ `parked`, `vetoed`) | Silas may flip anything; agents move `outline/approved → building → built` only |
| `priority` | `low` / `normal` / `high`                                  | Silas (agents default `normal`) |
| `narrator` | `yes` / `no`                                               | either — Silas's word wins |

Queue order: `approved` before `outline`, then `priority`, then oldest `created`.
`parked` and `vetoed` files are never built (vetoed files stay as a record of
what NOT to make). Only ONE dream may be `building` at a time.

## Rules for agents

- **Read `## Notes from Silas` before every stage.** Fold notes in, then note in
  the Build log how you applied them. NEVER edit or delete Silas's notes.
- Append stage completions to `## Build log` (date, stage, what was created
  where, PR link).
- Keep at least 5 buildable outlines (`outline`/`approved`) in this folder —
  replenish at ship time (see DREAM-SPEC.md once it exists, else DESIGN-BRIEF.md).
- New outlines must not duplicate existing kind_robots Dreams or backlog entries;
  check both before writing one.

## For Silas

Leave notes in any file's `## Notes from Silas` section, flip `status`/
`priority`/`narrator` in the frontmatter, or drop a bare-bones idea file with
just a title and a sentence — agents will grow it into a full outline. Veto by
setting `status: vetoed` (leave the file in place).
