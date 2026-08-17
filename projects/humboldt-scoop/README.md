# humboldt-scoop — FINISHED historical site project

**This project is finished.** It proved the original website/front-end path and is retained only as completion history and provenance.

All ongoing Humboldt Scoop Solutions work is coordinated by **`humboldt-scoop-cms`**, whose historical slug now represents the whole HSS product: the public website, customer portal, admin/dispatch surfaces, scooper/worker tools, shared backend, and Android/iOS apps through App Store / Play Store release.

The only canonical implementation repository is [`silasfelinus/humboldtscoopsolutions`](https://github.com/silasfelinus/humboldtscoopsolutions). Website code lives there under `site/`. **Do not develop against the copies under this Conductor directory.**

## Why this stays

Conductor is the coordination ledger, so the completed `roadmap.yaml` and historical notes remain available. The directory is not a second implementation of HSS.

## What moved

| Was here | Canonical location now |
|---|---|
| `scoops/` (custom themes, `humboldt-scoop-portal`, uploads/config import) | `humboldtscoopsolutions/site/` |
| `scoops/NOTES.md`, `scoops/ASSET-INVENTORY.md` | `humboldtscoopsolutions/site/docs/` |
| `CONTENT-BRIEF.md` | `humboldtscoopsolutions/docs/CONTENT-BRIEF.md` |
| ongoing product roadmap | `projects/humboldt-scoop-cms/roadmap.yaml` |

The legacy copies here are archaeology only. If they contain a useful implementation that the canonical repo lacks, salvage that implementation into `silasfelinus/humboldtscoopsolutions` first and record the provenance there; never revive this directory as a working codebase.
