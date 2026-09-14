# mona-salai — task history archive

Full `note:` prose for completed mona-salai tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Write the research design and evidence-standard brief

<!-- note:begin t-001 -->
Define the claim carefully: distinguish "Lisa del Giocondo was the sitter," "Salaì supplied reusable facial features," "the portrait became an idealized composite," and "Salaì was the principal model." Establish an evidence ladder and falsification rules. The documented Lisa del Giocondo identification must be treated as the mainstream historical baseline, not hand-waved away. Explain why facial-recognition confidence on artworks cannot establish identity by itself.


Research design brief implemented on worker/mona-salai-t-001-research-design-31a9.

Merged PR #1198 as squash 4c43ae9d14dc212c114ae26c344588329bf634d2. Added the research design and evidence-standard brief with separate hypotheses, evidence tiers, preregistration, controls, falsification rules, uncertainty limits, and reproducibility requirements.
<!-- note:end t-001 -->
