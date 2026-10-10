# Oversight dispatcher import failure

The 2026-10-10 Conductor Oversight run failed with `ModuleNotFoundError: No module named 'scripts'` when invoking `python scripts/ensure_semantic_intent_review.py`.

Fixed: the script now adds the repo root to sys.path, so `python scripts/ensure_semantic_intent_review.py` works directly.

This is a deterministic entrypoint defect, not an external service outage.
