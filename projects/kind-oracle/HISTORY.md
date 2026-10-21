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
