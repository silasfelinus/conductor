# approval-portal — task history archive

Full `note:` prose for completed approval-portal tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Build read-only dashboard from repo data

<!-- note:begin t-002 -->
Delivered via PR #58: Nuxt 3 app with /api/projects and /api/project/[slug] endpoints reading real roadmap/override/priority files; app.vue dashboard listing all active projects with progress %, task counts by status, and per-project detail (milestones, tasks grouped by status, control direction, gates, dependencies). Read-only, runs locally, no deploy. Merged to main. Worker connector failed at PR-open step but content was complete and merged by Silas. Reviewed and marked done by Reviewer 2026-06-30.
<!-- note:end t-002 -->
