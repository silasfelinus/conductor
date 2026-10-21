# evolve-rebel-button — task history archive

Full `note:` prose for completed evolve-rebel-button tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Ship the 100-click art reviewer (kind_robots)

<!-- note:begin t-002 -->
kind_robots: rebel-button.vue swaps to rebel-art-reviewer.vue at 100 clicks (logged-in). GET /api/art/review/next serves a random unreacted public-or-own still image under the shared maturity gate (buildArtImageWhere). POST /api/art/review writes one Reaction per user per image (1-5 maps to HATED/BOOED/NEUTRAL/CLAPPED/LOVED, rating stored), awards the existing REACTION_GIVEN karma, credits the owner REACTION_RECEIVED, and increments clickRecord by 1 on the first review of an image only. No schema change.
<!-- note:end t-002 -->

## t-003 — Silas visual and feel check of the reviewer on main

<!-- note:begin t-003 -->
FOR SILAS: open the Rebel Button on kindrobots.org after the next deploy, with an account at 100+ clicks. Check phone, tablet and desktop widths and whether the stars, labels and comment box feel right. TO APPROVE: set approved_by_human: true and status: done here, or leave a note with changes. Nothing is blocked on this.
Silas 2026-10-10 in session: the stars overlap each other on small/mobile screens. Fixed in silasfelinus/kind_robots#3429 (narrower button padding and smaller, wrapping stars below sm; verified at 320/375/640/1024 px). Re-check on a phone after that deploys; stays a soft gate until then.

ACCEPTED COMPLETE by silasfelinus via Kind Robots For You. Confirmed.
<!-- note:end t-003 -->
