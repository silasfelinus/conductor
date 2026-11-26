# tarot-studio — task history archive

Full `note:` prose for completed tarot-studio tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Write architecture and printing design brief, reusing Kind Oracle

<!-- note:begin t-001 -->
Document restored engine, canonical 78-card identities, project-specific art, print provider choices, data ownership and release gates.

Architecture and supplier-neutral printing plan is implemented in worker/tarot-studio-t-001-20261120-6c4d; artwork and commerce gates remain explicit.

2026-11-20 PT Reviewer: design brief merged via #7670 (squash 9aec836); reversible docs,
CI green. Kaizen -> t-010.
<!-- note:end t-001 -->

## t-003 — Ship private admin Tarot Studio with durable multi-deck/card editing and filters

<!-- note:begin t-003 -->
Kind Robots /admin/tarot plus ADMIN nav, persistent additive data model and 78-card seed per deck, prompt/checkpoint/LoRA editing, safe admin auth and tests. Keep all private.

Kind Robots worker/tarot-studio-t-003-20261120-6c4d includes persistent 78-card multi-deck admin studio, additive migration, protected APIs and catalog tests; real ArtJob submission is next task t-004.

pr-medic 2026-11-20: fixed red CI (Prettier-split inline handler broke template
compile/build, missing prisma generate output, duplicate admin tab icon) and
kind_robots#5433 merged green. Additive-only migration audited (CREATE TABLE x2, ADD
CONSTRAINT); production deploy follows the normal migration process.
<!-- note:end t-003 -->

## t-010 — Add a contract test that every Kind Robots tarot card oracleId resolves to a canonical Kind Oracle spec identity

<!-- note:begin t-010 -->
Reviewer kaizen from t-001 (#7670): enforce the DESIGN-BRIEF data-ownership boundary so all 78 seeded cards keep canonical Kind Oracle ids (Wands->Sparks, Cups->Currents, Swords->Breezes, Pentacles->Cogs, court ranks mapped) and art records never fork reading identity.
2026-11-25 PT: verifyTarotStudio now asserts all 78 catalog oracleIds equal the canonical Kind Oracle set from projects/kind-oracle/docs/spec.md (majors by ordinal; Wands/Cups/Swords/Pentacles -> Sparks/Currents/Breezes/Cogs; Page/Knight/Queen/King -> Apprentice/Wanderer/Keeper/Elder) and every seeded deck keeps each card's id; wired into contract-tests.yml (it never ran in CI before). Merged kind_robots#5879 green.
<!-- note:end t-010 -->
