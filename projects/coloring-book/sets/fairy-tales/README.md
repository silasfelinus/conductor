# Fractured Fairy Tales

slug: `fairy-tales`
status: independent (Silas works it by hand; no agent queue)
book-format: physical + digital coloring book
content-rating: provisional teen and adult, approximately PG-13 (Silas to confirm)
production-state: two seed pages exist; no roadmap task, generation queue, or schedule

## Why this set is independent

The `coloring-book` project is **paused** (Silas, 2026-09-27), and this set does not unpause it.
Silas asked on 2026-10-06 for the set to be supported "but keep the coloring book paused ... I
might want to work on it independently". That means:

- **No agent work.** No roadmap task, no `color-art-jobs.yaml` entry, no art-modeler request, no
  publishing or POD step. Agents treat this folder the way they treat `hollywood-recast-2/`: preserve
  it, and do not schedule it.
- **Not in `../catalog.yaml`.** The catalog is the paused project's production line, and every
  entry there must carry a full 36-slot ledger checked by `scripts/coloring_proposal_status.py`.
  Promote the set into the catalog only when Silas decides it becomes a production book.
- **Silas's ledger.** `concept-seeds.yaml` is the working list. Add pages, record files, and change
  status by hand.

## The concept

Classic fairy tales, fractured. Each page takes a tale everyone recognizes and flips who holds the
power, the glamour, or the menace. The recognisable beats stay: the candy house, the three bears,
the glass slipper. The casting, genre, or point of view turns sideways. The witch becomes the most
beloved showwoman in town. The bears get a police procedural. The humour comes from committing to the
new version completely, not from winking at it.

The source tales here are mostly public-domain folk tales (Grimm, Perrault, Andersen, English folk
tales), which gives this set more freedom than the Hollywood sets. Studio-specific designs are not
public domain, though. Avoid any one studio's character designs, costumes, colour keys or signature
staging, and never use a studio's logo or title lettering.

## Visual language

Follow the production pair already used by Monster Recast (`../monster-recast/STYLE-GUIDE.md`):

- a colored graphic master first
- then a faithful black-and-white coloring-page conversion
- thick, confident black contours; high, organized detail with many colorable regions
- one independent image per file, never a collage or panel grid
- no generated text inside the artwork

The two seed pages already set the house style. Both have dense storybook-gothic environments, a
huge supporting cast of small colorable characters, and one central figure who owns the frame.

## Seed pages

| id | working title | tale | files on Ferngrotto |
|---|---|---|---|
| `ft-001` | Bear Patrol | to name (Silas) | black-and-white page |
| `ft-002` | The Candy Hostess | Hansel and Gretel | colored master |

Full descriptions and file slots are in `concept-seeds.yaml`.

## Adding pages and art

1. Add an entry to `concept-seeds.yaml` with the next `ft-NNN` id.
2. Put art under `generated/color/` and `generated/bw/`, named
   `ft-NNN-<slug>.webp` (for example `generated/bw/ft-001-bear-patrol.webp`), and record each path
   in the page's `files` block.
3. Commit through a PR like any other change.

The art that existed before this README lived untracked in the Ferngrotto checkout at
`projects/coloring-book/sets/fairy-tales/`. File it under `generated/` as above when you are ready
to commit it.

## Files

- `README.md`: this set's concept, rules, and workflow
- `concept-seeds.yaml`: the hand-maintained page list, with file slots
