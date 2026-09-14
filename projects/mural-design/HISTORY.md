# mural-design — task history archive

Full `note:` prose for completed mural-design tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Create the fence-only coloring-page source assets from firstdraft

<!-- note:begin t-002 -->
FOR SILAS: FOR SILAS (Todo #1145): the maximalist-then-coloring-book fence mural pair you asked for is ready to review in projects/mural-design/. Read projects/mural-design/GENERATION-LOG.md for full prompt/model/source provenance on every file below.
What's in it: (1) projects/mural-design/colored_revision2.png — the strongest maximalist candidate: thick black outlines, flat single-color sections, Totoro-like spirit in an ivy portal on the left, hidden soot sprites, a small Kind-Robots-style robot, rainbow butterflies, stylized alien-leaning foliage, and the refreshed Catbus on the right, generated img2img from your actual current.jpg fence photo with a wine/magenta background per your 2026-07-07 palette note. (2) A second maximalist candidate, projects/mural-design/mural-mockup-4878-15428.png (this session's ArtJob 4878, fully documented) — same brief, a looser/more-divergent interpretation, kept for comparison rather than as the lead choice. (3) The coloring-book remix, projects/mural-design/5f3d5014-a6aa-464a-8cee-b58b49cf51ad.png — thick black linework on white for the fence and everything painted on it, while the sky, house, sidewalk, curb, street, hedge/ivy, and off-fence flowers stay in full color, per WONDERLAB-COLORING-SPEC.md's fence-only rule. One known imperfection: the soot sprites render as solid black filled shapes rather than white-interior line art (soot sprites are canonically black, so this may already be the right call — your eye needed either way).
Provenance gap disclosed: colored_revision2.png and the 5f3d5014 coloring page were already sitting in the project folder with no prior TALKBACK/roadmap record of the job that made them (shallow git history only shows a truncation-boundary commit) — their content was visually verified against the design brief this session, but their exact prompt/seed could not be recovered. A second, fully-documented coloring-page remix (ArtJob 4879, same source image, WONDERLAB-COLORING-SPEC's exact prompt) was queued this session but had not finished rendering by the end of the session — see GENERATION-LOG.md's follow-up note to fetch it later (projects/mural-design/mural-coloring-4879-<artImageId>.png once done) as an additional comparison candidate; it is not required to review what's already here.
TO APPROVE: pick a maximalist direction (colored_revision2.png recommended) and confirm the coloring-book remix's black/white split matches what you want to color-test, or note what to change (e.g. the soot-sprite fill). Set approved_by_human: true and status: done, or leave a correction note here. This unblocks t-003 (reviewing the section map / color-workflow adjustments) once the coloring-page direction is confirmed.


Decision accepted under Silas's 2026-09-07 default-recommendation policy: use colored_revision2.png as the lead maximalist mural direction and accept the fence-only coloring-page split as the working baseline. Keep soot sprites as small solid-black forms rather than forcing white-interior coloring regions, consistent with the established character direction. Proceed to section-map/palette iteration; all of this remains reversible internal design work until physical painting.
<!-- note:end t-002 -->

## t-006 — Confirm the design brief matches Silas's intent

<!-- note:begin t-006 -->
FOR SILAS: soft checkpoint per the new-project scope rule — nothing is blocked on this, t-002 (coloring-page asset generation) proceeds in parallel. Read projects/mural-design/DESIGN-BRIEF.md and projects/mural-design/WONDERLAB-COLORING-SPEC.md and confirm they faithfully capture your fence mural direction, uploaded current/first-draft image references, Catbus right, Totoro-ivy portal left, normal-sized hidden soot sprites, small Kind Robots-style robots, rainbow butterflies, alien-garden foliage, flat-color/thick-outline/grid-paintable style, the updated PPG Voice of Color exterior-paint palette requirements, and the WonderLab coloring-page direction where the off-fence environment remains colored while only actual fence sections are recolored by color id. TO APPROVE: set approved_by_human: true and status: done, or leave a correction note here.
CONFIRMED 2026-07-25: Silas — "confirmed."
<!-- note:end t-006 -->

## t-007 — Build the WonderLab mural coloring page in kind_robots

<!-- note:begin t-007 -->
Implemented and merged the first frontend color-studio pass in kind_robots PR #135. The shipped /mural page includes a Pinia/localStorage mural store, saved colors, add/remove swatches, clickable SVG sections, group fill controls, individual section overrides, reset-to-default behavior, WonderLab card bridge wiring, tutorial wiring, and required mural asset paths. This was intentionally a starter/manual UI scaffold rather than the final generated fence-only asset workflow. Follow-up work should replace placeholder WebP payloads with real artwork, promote mural into the canonical dashboardConfigs.wonder.tabs registry, remove the temporary labCards bridge, add palette/assignment JSON import-export, and add named paint schemes.
<!-- note:end t-007 -->
