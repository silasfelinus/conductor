# kind-oracle — task history archive

Full `note:` prose for completed kind-oracle tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-004 — Reading engine and tests (kind_robots utils/)

<!-- note:begin t-004 -->
Pure seedable draw, orientation and reading assembly from a static content table; DB-free tsx tests proving every spread yields complete text.
Reading engine merged in kind_robots#3207: utils/oracle/{types,rng,spreads,reading,validate}.ts plus npm run test:oracle-engine (8 DB-free tests, wired into contract-tests.yml). Repo gates hit on the way: noUncheckedIndexedAccess and the Prettier ratchet (repo-pinned prettier 3.9.6).
<!-- note:end t-004 -->

## t-005 — Author the content: 78 card meanings, position texts and pair texts (majors first)

<!-- note:begin t-005 -->
Write every card meaning plus position and pair texts as static JSON. Read each reading style through; warm, kind, never fatalistic. All-ages.
2026-11-28 PT: authored for the live Kind Tarot reader. 78 card meanings, energy pairs and openings/closings shipped earlier (kind_robots#6003); kind_robots#6062 adds 396 bespoke position passages for all 22 majors (9 positions x upright/reversed) and brings special pairs to 20. Minors keep the position frame by the spec's design. Done once #6062 merges.
2026-11-28 09:40 UTC: kind_robots#6062 merged with all checks green (validateOracle over the full content reports 0 problems; test:tarot-reader asserts every major has both passages in every position). Done.
<!-- note:end t-005 -->
