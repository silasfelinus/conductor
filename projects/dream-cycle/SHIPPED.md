# Daily Dream creation evidence

This file is a pointer, not a second ledger.

Successful Daily Dream bundles are recorded atomically inside their dated proposal files as `built-data`. That block contains the actual kind_robots model IDs, build timestamp, art-request IDs, attachment targets, and source slug used by the digest and later repair passes.

To inspect shipped output:

1. open a dated `proposal: true` file in `backlog/`;
2. confirm `status: built`;
3. inspect its `built-data` block;
4. use the daily digest for the readable proposal/build/Facet/art presentation.

Failed attempts remain visible as `build-attempt-data` retry evidence until the same canonical builder succeeds. Delegated non-dream creations keep their authoritative completion evidence in their home project.

A hand-maintained list here would drift from those machine-written records, so new Daily Dream bundles are not appended manually.
