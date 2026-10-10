# Oversight dispatcher import failure

The 2026-10-10 Conductor Oversight run failed with `ModuleNotFoundError: No module named 'scripts'` when invoking `python scripts/ensure_semantic_intent_review.py`.

The safe repair is to run `python -m scripts.ensure_semantic_intent_review` from the repository root, or make the script support direct execution. The semantic review itself was current, and project parity was clean.

This is a deterministic entrypoint defect, not an external service outage.

**Status (2026-10-10 review):** resolved on main — `scripts/ensure_semantic_intent_review.py` now inserts the repo root on `sys.path`, so direct execution works.
