# humboldt-scoop-cms — code has moved

**The CMS and field client now live in [`silasfelinus/humboldtscoopsolutions`](https://github.com/silasfelinus/humboldtscoopsolutions).**

Seeded there 2026-08-15 from this directory. Do not continue editing the service
here — changes made in conductor will not reach the working copy and recreate the
split-brain problem the move was meant to end.

## What stays in conductor

`roadmap.yaml` — task status, milestones, human gates, completion history.
Per [`SOURCE_OF_TRUTH.md`](../../SOURCE_OF_TRUTH.md), Conductor is the canonical
coordination ledger. Status *about* this work stays here; the work itself lives
in the other repo.

Still open here: **t-010** (`needs-human`) — review real-address privacy, map
costs, and launch gates. That gate is unaffected by the move.

## What moved

| Was here | Now |
|---|---|
| `src/`, `ops/`, `route-cards/`, `route-planner/`, `package.json`, `tsconfig.json` | `cms/` |
| `SCHEMA.md`, `STACK.md`, `PRIVACY-LAUNCH-REVIEW.md` | `cms/` |
| `field_client/` | `field-client/` |

`apps/humboldt-scoop-cms/` (repo root) was **not** carried over — it is an
AppMaker scaffold whose `lib/main.dart` is a 22-line hello-world, under a
different package name (`humboldt_scoop_cms`) than the real client
(`humboldt_scoop_field_client`). Copying it alongside `field_client` would have
produced a broken mixed-package build. Platform directories are regenerated in
the new repo with `cd field-client && flutter create .`.

Verified at move time: `npm run build` clean, `npm test` 25/25 passing.
