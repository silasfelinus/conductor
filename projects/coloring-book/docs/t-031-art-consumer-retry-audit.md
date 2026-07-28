# t-031 — Generic Art Consumer Retry Audit

## Scope

Audited the two consumers named by the task:

- `scripts/consume_art_queue.py`
- `scripts/consume_art_requests.py`

Both eventually call the same `entry_to_job()` and `wait_for_job()` implementation. The request consumer imports the queue consumer as its shared transport boundary.

## Finding

The duplicate-submission bug applies to both consumers.

For Comfy workflow engines, an entry without a pinned seed previously received a new random seed every time `entry_to_job()` ran. When `wait_for_job()` timed out while the server-side ArtJob remained queued or running, the YAML entry stayed pending. A later run rebuilt the request with a different seed and therefore a different payload. The server could not identify it as the same attempt, so the retry could enqueue a second ArtJob while the first was still active or had completed after the local timeout.

The existing filesystem check in `consume_art_requests.py` only protects requests whose target file has already landed in the checkout. It does not protect a render that completed remotely after the local timeout but has not yet been downloaded and committed.

## Fix

The public `consume_art_queue.py` boundary now assigns a deterministic seed to generic Comfy entries that omit a seed. The seed is derived from stable request identity:

- request id
- image path
- project slug
- normalized prompt
- normalized engine

Re-running the same pending entry therefore rebuilds the same seed and workflow payload. Changing the actual request identity still produces a different seed.

The prior implementation is preserved byte-for-byte in `consume_art_queue_core.py`; the public entrypoint wraps it and patches the shared `entry_to_job()` reference used by both command-line execution and `consume_art_requests.py`.

## Specialized coloring exception

`consume_coloring_book_color_art.py` intentionally explores a fresh seed for each semantic attempt and already implements `recover_timed_out_job()` using the prior ArtJob id recorded in its semantic gate error. Entries carrying its `set`, `concept_id`, and `semantic_attempts` fields therefore retain randomized attempt seeds. This avoids flattening deliberate exploration while making the two generic consumers retry-stable.

## Regression coverage

`tests/test_art_queue_retry_seed.py` verifies:

1. identical generic retries rebuild the same seed and workflow;
2. a changed request identity changes the derived seed;
3. an explicit seed remains authoritative;
4. specialized coloring attempts retain fresh-seed behavior; and
5. the art-request consumer uses the retry-stable shared boundary.

No ArtJobs were submitted, retried, mutated, or deleted during this audit.
