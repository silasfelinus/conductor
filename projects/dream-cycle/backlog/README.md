# Dream Cycle backlog

One file per creation idea. This folder is the shared steering surface between
Silas and the agents — outlines wait here until idle capacity builds them.

## File format

Copy the template for the creation type (`_template.md` for dreams,
`_template-coloring-book.md` for books). Frontmatter drives the queue:

| field      | values                                                     | who sets it |
|------------|------------------------------------------------------------|-------------|
| `type`     | `dream` / `coloring-book` / (any type with a `specs/<type>.md` playbook) | either |
| `status`   | `outline` → `approved` → `building` → `built` (+ `parked`, `vetoed`) | Silas may flip anything; agents move `outline/approved → building → built` only |
| `priority` | `low` / `normal` / `high`                                  | Silas (agents default `normal`) |
| `narrator` | `yes` / `no` (dream type only)                             | either — Silas's word wins |

Queue order (across all types): `approved` before `outline`, then `priority`,
then oldest `created`. An outline whose `type` has no playbook in `specs/` yet is
not buildable — it waits, it doesn't block the queue. `parked` and `vetoed`
files are never built (vetoed files stay as a record of what NOT to make).
Only ONE creation may be `building` at a time.

## Home-project delegation

Types whose output belongs to another project (e.g. `coloring-book` → set files
in `projects/coloring-book/sets/<slug>/`) keep their content THERE — the backlog
file here is the scheduler card and steering surface only. Never duplicate a
home project's content into this folder; link to it.

## Rules for agents

- **Read `## Notes from Silas` before every stage.** Fold notes in, then note in
  the Build log how you applied them. NEVER edit or delete Silas's notes.
- Append stage completions to `## Build log` (date, stage, what was created
  where, PR link).
- Keep at least 5 buildable outlines (`outline`/`approved`, playbook-backed type)
  in this folder — replenish at ship time.
- New outlines must not duplicate existing kind_robots Dreams, home-project sets,
  or backlog entries; check all before writing one.

## For Silas

Leave notes in any file's `## Notes from Silas` section, flip `status`/
`priority`/`narrator` in the frontmatter, or drop a bare-bones idea file with
just a `type`, a title, and a sentence — agents will grow it into a full
outline. Veto by setting `status: vetoed` (leave the file in place).
