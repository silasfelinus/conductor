# Coloring Book Studio event queue

This directory is the connector-safe bridge between the Kind Robots production studio and the secret-bearing Coloring Book ArtJob runner.

A studio request creates one bounded YAML event. The `Process Coloring Book Studio events` workflow validates it, runs only the named proposal IDs through the canonical color consumer and semantic gate, commits landed renders and queue updates, and removes the event only after the request finishes or reaches human review.

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

Rules:

- `book` must be `monster-recast`, `hollywood-recast`, or `kind-robots`.
- `proposal_ids` must contain 1–18 IDs belonging to that book.
- `timeout` must be 30–900 seconds per ArtJob.
- `force: false` accepts only proposals already pending in the canonical queue.
- `force: true` requests a revision of a completed, approved, or review-blocked proposal. The current generated candidate is moved into a timestamped `revisions/` directory before the new attempt starts, and its queue metadata is retained in `studio_revision_history`.
- Event values never become shell commands; the processor constructs a fixed argument list.
- A retryable failure preserves the event for the hourly retry. Successfully landed renders remain marked `done`, preventing duplicate submission.
- A semantic rejection that exhausts its retry allowance moves the proposal to `needs_review` and consumes the event instead of retrying forever.
- Keep one event file per intentional request. Do not duplicate a preserved event after a timeout.
