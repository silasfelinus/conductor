# humboldt-scoop — code has moved

**The website code now lives in [`silasfelinus/humboldtscoopsolutions`](https://github.com/silasfelinus/humboldtscoopsolutions), under `site/`.**

Seeded there 2026-08-15 from this directory's `scoops/` import. Do not continue
editing the site here — changes made in conductor will not reach the working
copy and recreate the split-brain problem the move was meant to end.

## What stays in conductor

`roadmap.yaml` — task status, milestones, human gates, completion history.
Per [`SOURCE_OF_TRUTH.md`](../../SOURCE_OF_TRUTH.md), Conductor is the canonical
coordination ledger. Status *about* this work stays here; the work itself lives
in the other repo.

## What moved

| Was here | Now |
|---|---|
| `scoops/` (custom themes, `humboldt-scoop-portal` plugin, uploads, `compose.yaml`, config) | `site/` |
| `scoops/NOTES.md`, `scoops/ASSET-INVENTORY.md` | `site/docs/` |
| `CONTENT-BRIEF.md` | `docs/CONTENT-BRIEF.md` |

`scoops/wp-admin/` and `scoops/wp-includes/` (79MB of vendored WordPress 7.0)
were not carried over — the `wordpress:php8.2-apache` image supplies core.

The copy under `scoops/` here is retained for now as the import of record. It can
be deleted once the new repo is reconciled against the Alexandria PC — see
`docs/INVENTORY.md` in the new repo for what that reconciliation still needs
(a database dump, above all).
