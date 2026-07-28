# Coloring Book Studio event queue

This directory is the connector-safe bridge between the Kind Robots production studio and the secret-bearing Coloring Book ArtJob runner.

A studio action creates one bounded YAML event. The `Process Coloring Book Studio events` workflow validates it, applies only the named proposal IDs, commits resulting images and ledger state, and removes the event after success or a terminal human-review result.

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

An existing set asset can be adopted without pretending it came from a current ArtJob:

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

Supported operations:

- `generate-color-proposals` — render or revise exact color proposals through the existing semantic-gated color pipeline.
- `accept-color` — write the reviewed color candidate into `accepted.color`, mark the queue entry approved, and lock the exact render seed when one exists. With `source_path`, adopt that exact existing set asset instead.
- `generate-bw` — derive a faithful Kontext line-art candidate from `accepted.color`, then run the mechanical line-art gate and color/BW pair-fidelity gate.
- `accept-bw` — write the reviewed line-art candidate into `accepted.bw`. With `source_path`, mechanically inspect that existing set asset and run pair-fidelity review against the accepted color master before promotion.
- `finalize-pair` — revalidate the accepted pair and write both paths into `final`.

Rules:

- `book` must be `monster-recast`, `hollywood-recast`, or `kind-robots`.
- `proposal_ids` must contain 1–18 IDs belonging to that book.
- `timeout` must be 30–900 seconds per ArtJob.
- `force` is valid only for `generate-color-proposals` and `generate-bw`.
- `source_path` is valid only for `accept-color` or `accept-bw`, requires exactly one proposal ID, and must name an existing image inside the selected Conductor set.
- Existing-asset adoption preserves the original file in place and does not invent an ArtImage ID, render seed, engine, or other missing provenance.
- A forced color revision archives the current generated color candidate and preserves its metadata in `studio_revision_history`.
- A forced B&W revision archives the current line-art candidate and preserves its metadata in `bw_revision_history`.
- B&W generation requires an explicitly accepted color master. It never chooses an inspiration or merely existing file on its own.
- Generated B&W candidates remain candidates until the studio sends `accept-bw`.
- `accepted` remains a human decision. Automated semantic gates may reject or flag candidates, but they do not silently promote them.
- An adopted B&W file that fails pair-fidelity review is recorded as `needs_review` and is not accepted; the event is terminal so it does not retry the same unsuitable pair forever.
- `finalize-pair` requires accepted color and B&W files and reruns mechanical and pair-fidelity validation before writing `final`.
- Event values never become shell commands; the processor constructs a fixed argument list.
- Retryable network, queue, or credential failures preserve the event. Terminal mechanical or semantic rejections record review evidence and consume the event instead of retrying forever.
- Keep one event file per intentional action. Do not duplicate a preserved event after a timeout.
