# deepheart — task history archive

Full `note:` prose for completed deepheart tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-011 — Art ledger: queue every brief auto_submit

<!-- note:begin t-011 -->
projects/deepheart/art/WRITTEN-BACKLOG-2026-11-16-KIT-DEEPHEART.yaml queues the 139
unpainted kit pictures (key art, 57 portraits, 41 romance plates, 9 ending plates, 31
scene/support plates) auto_submit at priority 1, from scripts/scan_written_art.py.
Still to queue: 3 faction emblems, 6 room plates (utils/deepheart/art.ts ROOM_ART) and
the 20 achievement badges (kind_robots scripts/generate_achievement_art.ts after the
catalog rows are seeded). Queued is not rendered: t-012 verifies delivery.

Deepheart foundation merged as Kind Robots #5257. The 139-item written art backlog exists, but t-011 remains unfinished: 3 faction emblems, 6 room plates and 20 achievement badges still need submission; queue completion cannot be inferred from prompt files.

Authored 29 remaining Deepheart asset prompts in worker/deepheart-t-011-missing-art-6b4278fa: 3 factions, 6 room plates and 20 achievements, sourced from the live Kind Robots catalog and art spec. The idempotent auto_submit queue will run after a green merge; review status pending verification of accepted ArtJob IDs.

Merged Conductor #7505 as fae31db; Auto Art Generate 43983771297 successfully submitted and checkpointed 29 unique Deepheart ArtJobs 69628-69656 in projects/deepheart/art/MISSING-ASSETS-2026-11-16.yaml (3 emblems, 6 rooms, 20 achievements). Previously queued original 139 jobs 69460-69598 are all DONE with ArtImage IDs. No duplicates. Submission is complete; t-012 now owns rendered media URL verification and wiring, including association of the badge ArtImages with live Achievement records.
<!-- note:end t-011 -->
