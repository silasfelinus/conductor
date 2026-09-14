# animation-studio — task history archive

Full `note:` prose for completed animation-studio tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Research modern passive screensavers and browser animation patterns

<!-- note:begin t-001 -->
Maintain RESEARCH.md with sources, techniques, performance notes, reduced-motion behavior, passive-first interaction patterns, and ideas worth adapting rather than cloning. Include Canvas 2D, CSS, SVG, WebGL/WebGPU where justified, audio-free defaults, and mobile limits. CLAIM RETRACTED 2026-07-21T23:07:28Z (conductor scheduled burst, claude-conductor-burst-20260721T230725Z-anim-t001): claimed this in error -- project-overrides.yaml marks animation-studio status: retired (2026-07-19, conductor/t-039), superseded by animation-manager, which already mirrors this exact task (its own t-001/t-002 are done). The claiming session's ready-task scan built the active-project set from project-overrides.yaml but never actually filtered by it before walking priority.yaml, so a retired project's ready task surfaced as pickable. Caught before any PR was opened -- no animation-studio code/doc change was merged. Left at status: ready/owner: null since this project is off-limits for claims per AGENTS.md's active-only rule; a future session should not re-claim it either, and ideally the retired project's remaining ready tasks (t-001, t-002, t-004) get formally closed as superseded rather than surfacing as pickable again.

CONSISTENCY CLOSE 2026-08-29: this retired project was superseded by animation-manager; closing the leftover ready task prevents retired work from resurfacing as claimable.
<!-- note:end t-001 -->

## t-002 — Maintain a ranked animation pitch queue

<!-- note:begin t-002 -->
Add 5-10 concise pitches per research pass to pitches/. Each pitch defines the passive loop, optional surprise interaction, visual novelty, implementation approach, performance risk, reduced-motion fallback, and why it belongs in the opening rotation. Rank novelty, serenity, surprise, reliability, and effort.

CONSISTENCY CLOSE 2026-08-29: this retired project was superseded by animation-manager; closing the leftover ready task prevents retired work from resurfacing as claimable.
<!-- note:end t-002 -->

## t-004 — Design reaction-backed animation attempts and revision lineage

<!-- note:begin t-004 -->
Define the smallest durable contract linking an animation concept, implementation attempt, revision/build, screenshots or clips, provenance, performance notes, status, and Reactions. Reuse the existing Reaction model/API where possible. Do not invent a parallel voting system. Aggregate reactions by attempt and preserve lineage so polish work can compare versions.

CONSISTENCY CLOSE 2026-08-29: this retired project was superseded by animation-manager; closing the leftover ready task prevents retired work from resurfacing as claimable.
<!-- note:end t-004 -->
