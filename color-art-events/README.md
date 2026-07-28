# Coloring Book Studio event queue

This directory is the connector-safe bridge between the Kind Robots production studio and the secret-bearing Coloring Book ArtJob runner.

A studio action creates one bounded YAML event. The `Process Coloring Book Studio events` workflow validates it, applies only the named interior proposal or book cover, commits resulting images and ledger state, and removes the event after success or a terminal human-review result.

```yaml
version: 1
operation: generate-color-proposals
book: monster-recast
proposal_ids:
  - mr-009
timeout: 600
force: false
requested_by: kind-robots-coloring-studio
task: coloring-book/t-028
note: Optional context.
```

An existing interior set asset can be adopted without pretending it came from a current ArtJob:

```yaml
version: 1
operation: accept-color
book: monster-recast
proposal_ids:
  - mr-020
source_path: approved/fly-beach-color.webp
timeout: 600
force: false
requested_by: kind-robots-coloring-studio
task: coloring-book/t-028
```

Cover operations target the book directly and omit `proposal_ids`:

```yaml
version: 1
operation: generate-cover
book: kind-robots
timeout: 600
force: false
requested_by: kind-robots-coloring-studio
task: coloring-book/t-028
note: Generate the first canonical Kind Robots front-cover source candidate.
```

Supported interior operations:

- `generate-color-proposals` — render or revise exact color proposals through the existing semantic-gated color pipeline.
- `accept-color` — write the reviewed color candidate into `accepted.color`, mark the queue entry approved, and lock the exact render seed when one exists. With `source_path`, adopt that exact existing set asset instead.
- `generate-bw` — derive a faithful Kontext line-art candidate from `accepted.color`, then run the mechanical line-art gate and color/BW pair-fidelity gate.
- `accept-bw` — write the reviewed line-art candidate into `accepted.bw`. With `source_path`, mechanically inspect that existing set asset and run pair-fidelity review against the accepted color master before promotion.
- `finalize-pair` — revalidate the accepted pair and write both paths into `final`.

Supported cover operations:

- `generate-cover` — generate or force-revise the named book’s portrait front-cover source art from `projects/coloring-book/cover-art-jobs.yaml`.
- `accept-cover` — semantically and mechanically review the current candidate, or adopt an exact set-local `source_path`, then write the accepted path into the book ledger’s `cover.accepted.color` field.
- `finalize-cover` — revalidate the accepted source art and write it into `cover.final.color`.

Cover source art is not the complete print wraparound. Generated words are forbidden; typography, spine, back cover, barcode area, bleed, and printer-template layout remain a separate packaging step.

Rules:

- `book` must be `monster-recast`, `hollywood-recast`, or `kind-robots`.
- Interior operations require `proposal_ids` containing 1–18 IDs belonging to that book.
- Cover operations reject `proposal_ids`; the book slug identifies the single cover.
- `timeout` must be 30–900 seconds per ArtJob.
- `force` is valid only for `generate-color-proposals`, `generate-bw`, and `generate-cover`.
- `source_path` is valid only for `accept-color`, `accept-bw`, or `accept-cover` and must name an existing image inside the selected Conductor set.
- Existing-asset adoption preserves the original file in place and does not invent an ArtImage ID, render seed, engine, or other missing provenance.
- Forced color, B&W, and cover revisions archive the current candidate and preserve revision metadata.
- B&W generation requires an explicitly accepted color master. It never chooses an inspiration or merely existing file on its own.
- Generated candidates remain candidates until the studio sends the corresponding acceptance action.
- `accepted` remains a human decision. Automated semantic gates may reject or flag candidates, but they do not silently promote them.
- Terminal mechanical or semantic review failures are recorded as `needs_review` and consumed; retryable network, queue, credential, or unavailable-gate failures preserve the event.
- `finalize-pair` and `finalize-cover` revalidate accepted assets before writing final ledger paths.
- Event values never become shell commands; the processor constructs a fixed argument list.
- Keep one event file per intentional action. Do not duplicate a preserved event after a timeout.
