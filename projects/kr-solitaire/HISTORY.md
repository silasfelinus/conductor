# kr-solitaire — task history archive

Full `note:` prose for completed kr-solitaire tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Confirm scope with Silas

<!-- note:begin t-002 -->
FOR SILAS: soft checkpoint, nothing is blocked on it. Read projects/kr-solitaire/DESIGN-BRIEF.md and confirm or redirect the agent picks listed in notes_from_silas. If there is no answer within 7 days the next gate-triage session adopts them as written under the 2026-09-30 default-recommendation rule.

Silas approved all proposals in session on 2026-10-02 ("I like all proposals"); agent picks in notes_from_silas stand as written.
<!-- note:end t-002 -->

## t-003 — Survey existing card art and component patterns, pick the card-back set

<!-- note:begin t-003 -->
Read-only survey, write projects/kr-solitaire/docs/survey.md: which existing card art (components/navigation/flip-card.vue, card-picker.vue, character and reward cards) can serve as card backs, aspect ratios, where /play pages live, and the pattern for lazy static assets. Recommend 3 to 6 backs. No code changes.
Survey landed at projects/kr-solitaire/docs/survey.md: recommend all five existing card backs.
<!-- note:end t-003 -->

## t-004 — Seedable Klondike engine with tests (kind_robots utils/)

<!-- note:begin t-004 -->
Pure TypeScript engine: seeded shuffle, deal, legal move generation, move application, undo log, win and auto-complete detection, draw-1 and draw-3. DB-free tsx tests, a contract-tests step, and a solvability sampler over 200 seeds. No UI.
Landed kind_robots#3175: utils/solitaireEngine.ts (seeded shuffle, deal, legal moves, undo, win/auto-complete, draw-1/3, bounded solver) + test:solitaire-engine (13 checks; 115/200 seeds solved within a 6000-node budget), wired into Contract Tests.
<!-- note:end t-004 -->

## t-006 — Deck design bible: suits, pips, court cards and the 52-card prompt table

<!-- note:begin t-006 -->
Write projects/kr-solitaire/docs/deck-bible.md: the four suits (names, colours, pips, personality), the 12 court characters mapped to existing characters, the style bible and seed policy, and a 52-row prompt table following the Krea 2 contract in ART-PROMPTS.md. Silas may rename suits; keep them one-line edits.
2026-10-06: merged conductor#5658. docs/deck-bible.md: suits, court cast, style bible, seed policy, 52-row prompt table. t-007 should swap generic court costumes for each character's established look.
<!-- note:end t-006 -->
