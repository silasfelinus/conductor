# Maintaining the Zuzu world registry

Scope: shared discovery, identity, provenanced asset references, canon and cross-project
relationships. Not scope: project task queues, copies of binary art, lore invented by an
unreviewed game branch, a second Resource table, or secret plot details.

1. Read [README.md](README.md) and the ordered `canon_sources` in
   [catalog.json](catalog.json). Follow Book One / Cast Picks / Video Guardrails,
   not the old script or seed Dream when they disagree.
2. Update the **owning file or Kind Robots runtime row first**. Only then add or
   revise a pointer in `catalog.json`. Existing paths and `ArtImage` IDs are
   identity references, not duplicated content.
3. Give each resource or production a stable, lowercase, hyphenated key.
   Populate a live model ID only after checking its actual Kind Robots record.
   Empty `stable_ids` means unverified; do not fill it with a plausible guess.
4. Distinguish `source-defined`, `not-audited`, `legacy-inspiration` and
   verified live resources. A LoRA dataset definition is not a trained or
   imported LoRA. Keep provenance and rights with the asset.
5. Treat comic Book One as canonical chronology; games may have alternate
   routes and a lighter rating without rewriting that chronology.
6. Use normal Conductor PR, review, test and publication gates. For a new
   project, keep its roadmap under `projects/<slug>/` and its Kind Robots
   `Project.conductorSlug` as the identity join; do **not** create a new
   Conductor project for a world folder.
7. Run `python -m unittest tests/test_zuzu_world_catalog.py` when editing the
   catalog or relocating paths. Update consumers to point to this index,
   not hardcoded copies of conflicting lore.

The catalog intentionally does not reproduce the secret guardrail terms.
Read the latest Video Guardrails source at generation time.
