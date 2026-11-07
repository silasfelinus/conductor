# Memory Dungeon t-020: twelve-world compatibility acceptance matrix

**Scope:** Save and narrative compatibility for the modern-Earth opening and the retired sixteen-realm plan. This is an implementation contract, not a claim that migration or artwork is complete.

**Authority:** `CONTROL.md` (2026-10-30 twelve-world production cap; 2026-11-05 Rowan correction), then `TWELVE-REALITY-COLLISION-FINALE.md`. `SIXTEEN-REALM-PRODUCTION.md` is historical where it conflicts. Preserve the existing /play/memory and Classic Match.

## Current canon and save identity

| Play order | Location/POV contract | Migration rule |
| --- | --- | --- |
| e01–e02 | Briar original/twisted, researcher Rowan; Pip is a goblin courier NPC | Preserve authored 8×8 coordinates, previously earned Briar flags, dungeon outcomes and existing save identifiers. Do not silently rename Pip-labeled persisted keys. |
| e03–e04 | Earth original/twisted, Morrow; Earth contacts call Morrow “Rowan” | Preserve the body-exchange premise, photograph chronology and existing response choices. Earth-side “Rowan” is not evidence that Morrow and the displaced protagonist share a save identity. |
| e05–e06 | Scylla's original/twisted mermaid worlds | Char's possible loss and later altered younger Char are separate causal states. No unconditional resurrection on load. |
| e07–e08 | Vesper's Hoshimori original/twisted childhood | Keep e08 in Vesper POV; Pip's Oven storyline remains a supporting subplot. |
| e09 | Briar collision, Rowan leads; Pip accompanies | Reuse Briar geography without treating collision discoveries as fresh original-world rewards. |
| e10 | Earth collision, Morrow leads | Preserve earlier Earth photograph and consent outcomes. |
| e11 | Mermaid collision, Char leads if alive, otherwise Scylla | Restore lead selection from persisted consequential state, not a new random draw. |
| e12 | Hoshimori collision, Vesper leads | Preserve four pair-hinge axes and the final choice for ending selection. |
| e13–e16 | **Retired** from new campaign routing | Existing save history must remain readable/archived; never reinterpret these keys as e09–e12 or delete them during a migration. |

## Executable acceptance cases for follow-up implementation

1. **Classic isolation:** Create a Classic Match save, enter and leave the RPG, then reload. Compare original Classic deck selection, scores and completion state byte-for-byte except explicitly documented timestamps.
2. **Legacy Briar:** Load a pre-twelve-world save with `BRIAR_START`, old Pip/Index narrative flags and `vault-1`/`vault-2` outcomes. Verify the map and House retain their rewards and resolved rooms; text may update to Rowan without rewriting old identifiers.
3. **Old-world archive:** Load a synthetic legacy save with e13–e16 discovery and Chronicle records. New routing must stop at e12, but a subsequent save/restore must preserve the old records without silently converting them to collision-world progress.
4. **Photo spoiler gate:** Restore photographs in nonchronological discovery order. Display them in canonical Earth order, hide future undiscovered photographs, and never reveal children unambiguously before the final disclosure.
5. **Char causality:** Restore one save where Char survived and one where she was lost. e11 lead and epilogue must differ accordingly; no restoration path may invent an unearned Char rescue.
6. **Cross-world replay:** Resolve the same collision encounter twice, including after JSON round-trip. No duplicate rewards, memory fragments, hinge choices or ending achievements.
7. **Prologue interruption:** Reload before and after the first choice, including skipping the cinematic. Neither path may lose character/expedition state, and the first actionable choice should remain reachable within the ninety-second design target.
8. **Corrupt or future saves:** Reject unsupported schema versions and malformed nested arrays without consuming rewards or mutating the input. Preserve a recoverable Classic entry rather than silently resetting an RPG run.
9. **Viewport:** At 390, 768 and 1440 CSS pixels, the prologue's primary art and one-tap choice hand remain visible in the console shell; help text stays in the tutorial surface, not over the art.

## Integration guardrails

Keep separate versioned World, Character, Expedition and Chronicle records. Migration must be idempotent: migrating an already migrated save changes nothing. Record explicit version transitions and test them against frozen fixtures. Avoid a blanket `worldIndex <= 12` filter on storage because that would discard archived e13–e16 discoveries. Distinguish **new-route eligibility** from **historical data retention**.

The recently merged `kind_robots#4894` deterministic three-floor simulator is a separate unintegrated subsystem. Its six rooms per floor are not replacements for any authored 8×8 overworld or 6×6 dungeon, and its room IDs must not collide with House or existing dungeon save keys.

## Still outstanding

This matrix does not implement migrations, verify browser rendering, submit ArtJobs or establish final narrative acceptance. Implement fixture-backed save migration tests and the live Pinia adapter next; then perform adversarial interruption and cross-world branch runs. Keep t-020 active until the opening, compatibility tests and artwork contract are actually integrated.
