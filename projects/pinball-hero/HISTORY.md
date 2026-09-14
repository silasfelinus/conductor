# pinball-hero — task history archive

Full `note:` prose for completed pinball-hero tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Define the pinball machine architecture and constraints

<!-- note:begin t-001 -->
FOR SILAS: projects/pinball-hero/DESIGN-BRIEF.md is the design brief. It defines the target cabinet/playfield size, mechanical scope, what to 3D print vs buy (with Bambu A1 print constraints), safety flags, and outlines budget and premium build variants. Includes open questions for your direction before BOM/model work begins. TO APPROVE: Read projects/pinball-hero/DESIGN-BRIEF.md and add any direction changes as a note here. Set approved_by_human: true and status: done. Unblocks: pinball-hero/t-002 (BOM tiers research), t-003 (3D printable model spec).
<!-- note:end t-001 -->

## t-006 — Survey open-source pinball software stacks for project fit

<!-- note:begin t-006 -->
Wrote projects/pinball-hero/SOFTWARE-SURVEY.md. Compared Mission Pinball Framework (MPF), FAST Pinball software, Multimorphic P-ROC, pypinball, Visual Pinball X, and MiSTer FPGA pinball cores. Recommendation: MPF + Open Pinball Project (OPP) hardware. MPF is the only free, hardware-agnostic, actively maintained option with a large community and YAML-config-based machine definition. OPP boards are open-source and cost-effective. First step for Silas: install MPF virtual simulator for zero-cost development testing before hardware commitment.
<!-- note:end t-006 -->
