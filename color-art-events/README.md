# Coloring-art event queue

This directory is the connector-safe bridge to the secret-bearing coloring-book ArtJob runner.
A Worker creates one bounded YAML request. The `Process coloring art events` workflow validates
it, invokes the fixed coloring-book consumer with `KR_API_TOKEN`, commits any landed renders and
queue updates, and deletes the event only after the consumer succeeds.

```yaml
version: 1
operation: generate-color-proposals
book: monster-recast
limit: 18
timeout: 300
requested_by: worker
task: coloring-book/t-022
note: Optional context.
```

Rules:

- `book` must be `monster-recast`, `hollywood-recast`, or `kind-robots`.
- `limit` is constrained to 1–18, matching the production model's half-book batch maximum.
- `timeout` is constrained to 30–900 seconds per ArtJob.
- Event data never becomes a shell command; the processor builds a fixed argument list.
- A failed or partially successful consumer run preserves the event for the next scheduled retry.
  Successfully landed renders remain committed and their queue entries are marked `done`, so a
  retry does not regenerate them.
- Keep one request file per intended batch. Do not duplicate a queued event after a failure.
