# Shifting Desks Classic Art Recovery / 2026-11-12 PT

## Authenticated production evidence (read-only)

GitHub Actions [Shifting Desks art visual review run 43335325581](https://github.com/silasfelinus/conductor/actions/runs/43335325581) executed `art/audit_live_artjobs.py` with the existing Conductor CI `KR_API_TOKEN`, never displaying credentials.

- Production ArtJobs inspected: **1,076**.
- Latest unmet Classic/recovery destinations: **20**.
- Exact request-ID + destination + target repository + created-after-request matches: **0**.
- Alternate-ID ArtJobs at the same destination newer than the request: **0**.
- Verified latest-round replacements delivered: **0**.
- All 20 live URLs contained older artwork, per the earlier Last-Modified audit. Existing media was not deleted or silently accepted.

The 20 legitimate missing requests were restored to `projects/art-prompts.yaml` with the **original prompt, engine, image path, size, seed and request ID**, and `status: pending`, `force: true`. Nineteen records had been absent; the existing round-17 Permanent Adjournment record was incorrectly `done` despite no newer ArtJob and was reset to pending. Unique IDs and image paths remain intact. No ArtJob was submitted by the audit itself.

### Sources and progress

- Round 13: **1** (Kind Rewrite ending).
- Round 14: **9** (Wellness/Sub-Level Zero location and department tone-ladder imagery).
- Round 15: **9** (robot, Kevin, Dale, suppression/tube gags, three mutation images).
- Round 17: **1** (Permanent Adjournment ending).

The **only acceptable completion** is a new matching ArtJob ID, DONE status, real ArtImage ID, newer final media, and an independently reviewed KEEP. Use:

```bash
python projects/shifting-desks/art/reconcile_delivery.py --live --write
python scripts/shifting_desks_art_readiness.py --strict
python projects/shifting-desks/encounters/link_art.py --write --probe
```

Run after jobs have completed; do not fabricate provenance. Keep the Western Cartoon runtime edition **suspended** while the six-cell private comparative fidelity pilot in `SUBJECT-FIDELITY-PILOT-V1.yaml` is generated and inspected against its six exact scene requirements. Do not link these isolated pilot ArtImages as production artwork until their individual reviews pass.

The project remains **active**, not `playtest`, and the final human fun verdict remains gated.
