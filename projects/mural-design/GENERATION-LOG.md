# Mural Design — Generation Log

Provenance record for the fence-mural artwork in this project folder, per AGENTS.md's
"Generated art is pre-approved" rule (keep prompt/model/source metadata needed to
recreate or delete the image). Newest entries at the bottom.

## Silas-uploaded references (not agent-generated)

- `current.jpg` — actual photograph of the real fence today (red/terracotta paint,
  hedge on the left, house behind, the original small Catbus panel already on the
  right). This is the "actual photo of the fence" base layer referenced throughout
  this log and in Silas's Todo #1145 instructions.
- `firstdraft.jpg` — Silas's own first-draft composition/color reference (brick-red
  background), uploaded as the design-direction target per DESIGN-BRIEF.md.
- `swatches.jpg` — photographed PPG Voice of Color paint-swatch cards, palette
  reference only.

## Agent-generated candidates found already in the project folder (pre-existing, undocumented)

These two files were present in the project working tree before this session but
carry **no prior TALKBACK/roadmap provenance note** — the repo's shallow git history
only shows them entering at the truncation boundary commit, with no earlier session
record of the job that produced them. Flagged here as a process gap (see TALKBACK
entry, conductor session 2026-08-04); treat their exact prompt/seed as unrecoverable,
but their content is directly inspectable and, on visual review, matches the
DESIGN-BRIEF composition closely enough to be genuinely useful reference candidates:

- `colored_revision2.png` — maximalist colored mural mockup. Composition (hedge/ivy
  left edge, continuous mural across the fence span, Catbus right, house roofline and
  yard details behind matching `current.jpg`'s real layout) is consistent with an
  img2img/Kontext pass using `current.jpg` as the base layer, refined from
  `firstdraft.jpg` (background pushed from brick-red to a wine/magenta-purple, per
  Silas's 2026-07-07 palette note in roadmap.yaml). Contains: Totoro-like spirit in an
  ivy portal (left), hidden soot sprites among the foliage, a small Kind-Robots-style
  robot, rainbow butterflies, stylized alien-leaning monstera/foliage, refreshed
  Catbus (right) — thick black outlines, flat single-color sections throughout.
- `5f3d5014-a6aa-464a-8cee-b58b49cf51ad.png` — coloring-book remix of
  `colored_revision2.png`. Sky, house, sidewalk, curb, hedge/ivy outside the fence,
  and off-fence flowers remain in full color; only the fence surface and everything
  painted on it (leaves, Catbus, Totoro, robot, butterflies, sprites) is converted to
  thick black line art on white. This matches WONDERLAB-COLORING-SPEC.md's fence-only
  rule exactly. One known imperfection: the soot sprites were left as solid black
  filled shapes rather than white-interior line art (soot sprites are canonically
  black, so this may be an intentional/acceptable rendering rather than a linework
  miss — worth Silas's eye).

## This session's fresh, fully-documented iteration (2026-08-04)

**Stage 1 — maximalist color mockup, ArtJob 4878 (already in flight when this session
started, completed mid-session):**
- Engine: COMFY (Kontext/Flux workflow), queued via `/api/art/enqueue`,
  `projectSlug: mural-design`.
- Source: `current.jpg` (real fence photo) as the img2img base layer.
- Prompt (verbatim, matches DESIGN-BRIEF.md's "next generator pass" variation prompt
  plus a maximalist-emphasis clause): "Create a wide realistic mockup painted onto
  the actual fence, using the uploaded photo as the physical baseline. Keep the
  Catbus freshly painted on the right, an ivy portal with hidden Totoro-like spirit
  on the left, normal-sized hidden soot sprites, several small Kind Robots-style
  robots, rainbow butterflies, and a slightly alien plant landscape. Restore
  simplicity: fewer leaf types, large readable shapes, flat single-color fills only,
  no shading, no gradients, thick black outlines, clear negative space, and a
  practical grid-friendly mural layout. Design around a practical PPG Voice of Color
  exterior-paint palette: three greens for leaves, black outlines, off-white beings
  and Totoro belly, yellow Catbus eyes, dark purple-red/magenta background, orange
  Catbus body, brown Catbus secondary color, robin-blue/teal windows, purple/violet
  butterfly accents, and gray robot/Totoro body parts. Favor slightly blue-tinted
  color choices to offset outdoor sun fading. Avoid the giant soot sprite. Make the
  composition feel magical, personal, and achievable to repaint by hand. Maximalist
  but still clean: clear thick black lines and solid color divisions throughout."
- Result: ArtImage id 15428, saved as `mural-mockup-4878-15428.png`. Completed
  (`status: DONE`) at 2026-08-04T04:44:14Z after 2 attempts (the job had timed out
  once earlier per the same-day TALKBACK pattern entry on ComfyUI backend load, then
  succeeded on retry — the job record itself, not a fresh submission, resolved DONE).
  Composition diverges further from the base photo than `colored_revision2.png` does
  (different house roofline/creature designs, no clear Totoro-ivy-portal callback) —
  kept as a genuine third candidate for comparison, not a replacement for
  `colored_revision2.png`, which stays the strongest maximalist candidate.

**Stage 2 — coloring-page remix, ArtJob 4879 (queued this session):**
- Engine: `kontext` via `/api/art/enqueue`, `projectSlug: mural-design`.
- Source: `colored_revision2.png` (the strongest maximalist candidate) as the img2img
  base layer for the remix — not a fresh photo base, since this stage's job is to
  convert an already-approved-looking color design into line art, per Silas's "then
  remix it into a coloring book page" instruction.
- Prompt (verbatim, WONDERLAB-COLORING-SPEC.md's Kontext prompt direction, used
  as-is): "From the uploaded mural image, create a clean coloring-page source for the
  painted fence only. Preserve the sky, house, sidewalk, curb, street, real plants,
  and other off-fence environment in full color as locked context. Convert the mural
  painted on the fence into crisp black outlines with closed, flat fillable regions.
  Include the fence background itself as fillable regions. Keep the Catbus on the
  right, the hidden spirit/ivy area on the left, foliage, robots, soot sprites,
  butterflies, mushrooms, pods, sparkles, and small spirits. No shading, no
  gradients, no painterly texture. Keep the linework thick, simple, and
  hand-paintable."
- Params: width 1536, height 512, steps 20, guidance 2.5, denoise 1.
- Result: **did not finish within this session's window.** Queued 2026-08-04T07:43:54Z,
  claimed by the render box (`Silas-PC`) at 07:46:35Z, still `status: RUNNING` with no
  error as of the last check this session (07:49Z+, ~5 min into the run — well inside
  the render box's normal range; ArtJob 4878 earlier the same day took ~68 minutes
  across 2 attempts before landing `DONE`). Not treated as failed or stalled — just
  not waited out, per the session's time budget. **Follow-up:** poll
  `GET /api/art/queue/4879` (same pattern as this log's stage 1); if `DONE`, fetch
  `artImageId` via `GET /api/art/image/{id}?includeImageData=true` and save as
  `mural-coloring-4879-<artImageId>.png` alongside this log. This does not block the
  needs-human review below — the pre-existing `5f3d5014-a6aa-464a-8cee-b58b49cf51ad.png`
  already satisfies the coloring-page deliverable; job 4879 is a second, fully-documented
  candidate for comparison once it lands, not a prerequisite.
