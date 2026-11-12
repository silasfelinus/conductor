# Shifting Desks art acceptance audit — November 12, 2026

**Status: NOT ready for verified Playtest transition.** Evidence inventory, not a
creative sign-off. The result is independent of whether an existing runtime
asset happens to return HTTP 200: the latest forced rerender needs its own
media provenance and a separate human/agent editorial *keep* decision.
Existing published art must not be deleted or replaced on speculation.

## Latest effective art ledger entry per destination

Compared all available `art/ROUND-*.yaml` files; later round number wins
when a destination is repainted. This prevents a previous KEEP from silently
approving a newer requested or rendered image.

| Accepted KEEP + delivered evidence | Delivered, verdict absent | New/latest delivery not verified | Distinct destinations |
|---:|---:|---:|---:|
| 175 | 196 | 20 | 391 |

The **196 delivered-but-unreviewed** are all round-18 subject-first Western
Cartoon images. Every one already carries an ArtJob, ArtImage and HEAD 200
provenance. Do **not** generate those 196 again: the missing work is visual
curation, especially the roach illustrations that were previously withdrawn.
Review the actual rendered subject and gag before recording keep/redo; some
rendered media may need a new composition, but do not bulk-approve a style.

The **20 not-delivered-latest** entries are:

- Round 13 (1): `ending-the-kind-rewrite`.
- Round 14 (9): `wellness`, `nutrition-studies`,
  `cognitive-testing-chamber`, `mutation-suite`, `sub-level-zero`,
  `boardroom-antechamber`, `founders-office`, `server-room-zero`,
  `the-board`.
- Round 15 (9): `the-curious-robot`, `kevin-from-tank-nine`,
  `dale-in-the-mustache`, `the-taste-panel`,
  `the-suppression-drill`, `the-jam-in-tube-14`,
  `mutation-four-second-precognition`, `mutation-empathic-static`,
  `mutation-eyes-in-the-back-of-your-head`.
- Round 17 (1): `ending-permanent-adjournment`.

**Important:** Requested status means the *newest specified rerender* lacks
recorded delivery evidence. It does not establish that the image path is empty.
The main-game standard audit on this date reported all eleven base ending
images returning 200. Do not queue duplicate jobs or erase working ending
plates merely to satisfy this ledger. Reconcile production ArtJob IDs, request
IDs, timestamps and media first via `art/reconcile_delivery.py --live --write`.

## Verification workflow

The script `scripts/shifting_desks_art_readiness.py` is the one-command
inventory. The Auto Art Generate workflow attaches a human-readable report on
each run, and the script can emit every individual blocker in JSON:

```bash
python scripts/shifting_desks_art_readiness.py --markdown
python scripts/shifting_desks_art_readiness.py --json
python scripts/shifting_desks_art_readiness.py --strict
```

The strict command must fail while any ledger destination remains missing,
unreviewed, rejected or unsupported by delivery evidence. It is an **art gate
only**, not a replacement for independent gameplay, editorial, 390/768/1440
layout, screen-reader and user-facing verification.

Next agent-owned actions:
1. Reconcile the 20 requested rerenders against actual DONE ArtJobs and newer
   media. If an old painting is good enough, explicitly withdraw the *new*
   request with documented evidence, rather than inventing a delivery.
2. Review the 196 verified round-18 images against subject-first prompts;
   record actual KEEP/REDO, prioritize the roach cards and obvious gag misses.
3. Link accepted Classic imagery with
   `projects/shifting-desks/encounters/link_art.py --write --probe`.
4. Re-run the readiness audit and the actual game/art/device tests, then hand
   the **final fun verdict** to Conductor `shifting-desks/t-020` with
   `status: needs-human`. Never grant this approval on the agent's behalf.

**References:** `projects/shifting-desks/art/ROUND-13.yaml` through
`ROUND-18.yaml` (round 16 was not present); `projects/shifting-desks/roadmap.yaml`,
`ART-DIRECTION.md`, and
`projects/shifting-desks/STANDARD-AUDIT-2026-11-12.md`.
