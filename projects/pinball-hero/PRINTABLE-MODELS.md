# Pinball Machine — 3D Printable Model Catalog

Generated: 2026-07-22
Task: pinball-hero/t-003
Depends on: DESIGN-BRIEF.md (approved 2026-07-01)

Full catalog of every part in the machine that gets 3D printed, with material,
orientation, tolerance, and file-format guidance. All parts respect the
DESIGN-BRIEF.md print constraints: Bambu A1 bed (256mm × 256mm × 256mm), no
single part over 250mm in any dimension, sliding fits +0.3mm/side, press fits
-0.1mm/side, ball-passage guides ≥28mm ID.

---

## How to read this

Each entry lists: **material**, **orientation**, **supports**, **tolerance notes**,
**file format to release**, and **heat/wear notes** where relevant. "Multi-piece"
flags parts that exceed the 250mm single-part limit and need a joint.

Recommended file formats:
- **STL** — geometry-only, fine for static/decorative parts nobody needs to modify
- **3MF** — preserves multi-part assemblies, print settings, and color if the
  slicer supports painted models (Bambu Studio does) — use for anything shipped
  as a pre-configured print profile
- **Editable CAD source (STEP/F3D)** — required for anything a builder is likely
  to need to resize, retolerance for their own printer, or remix (flipper arms,
  cabinet joinery, mounting brackets)

---

## Mechanical system (playfield-critical parts)

### Flipper arms (×2, left + right mirrored)
- **Material:** PETG (sees repeated flex/impact stress; PLA is too brittle here)
- **Orientation:** Print perpendicular to the pivot axis — i.e., pivot bore vertical
  on the bed, arm extending horizontally — for layer-line strength across the
  impact face (per DESIGN-BRIEF.md's own orientation note)
- **Supports:** Minimal — only under the ball-strike tip overhang if >45°
- **Tolerance:** Pivot bore uses the sliding-fit spec (+0.3mm over the pivot pin/
  shaft OD); if a DC-motor actuator is used (Solid tier), the motor-shaft coupling
  bore uses the press-fit spec (-0.1mm) for a friction-lock, no-glue connection
- **File format:** STEP/F3D (mirrored left/right variant is a parametric flip —
  ship the source so builders can adjust arm length for a non-stock playfield)
- **Heat/wear note:** Highest-wear part in the machine; design for tool-free
  swap (no glued-in inserts) so a worn arm is a 2-minute reprint-and-replace

### Flipper pivot brackets (×2)
- **Material:** PETG
- **Orientation:** Flat on bed, mounting face down
- **Supports:** None if bracket is a simple L/plate profile
- **Tolerance:** Press-fit for any embedded pivot bushing/bearing; standard
  clearance holes for wood screws into the playfield
- **File format:** STL (fixed geometry, no builder resizing expected)

### Pop bumper cap and housing
- **Material:** PLA+ (cosmetic-facing, low mechanical stress on the cap; PETG for
  the housing if a solenoid strikes it directly — see Solid/Deluxe electrics)
- **Orientation:** Print upside-down (dome face down on bed) with minimal supports
  — per DESIGN-BRIEF.md, this gives the cleanest visible surface since the domed
  top is what the player sees
- **Supports:** Light tree supports only under the skirt overhang
- **Tolerance:** Skirt ID uses sliding fit over the housing OD so the cap can be
  lifted for switch access without tools
- **File format:** 3MF (ship as a pre-painted/color-split model — cap and housing
  are visually distinct components worth a multi-color profile)

### Fixed bumper caps (×2–4)
- **Material:** PLA+
- **Orientation:** Flat, dome up, no supports needed (simple hemisphere-on-post
  geometry)
- **Tolerance:** Standard — these are passive, no moving fit
- **File format:** STL

### Inlane / outlane guide rails
- **Material:** PETG (ball-contact wear surface)
- **Orientation:** Flat on bed, guide channel facing up — avoids supports inside
  the channel where they'd be hard to clean out and would mar the ball-contact
  surface
- **Tolerance:** Channel ID ≥28mm minimum ball-passage clearance (DESIGN-BRIEF.md
  hard constraint — ball OD is 27mm); rubber-lip groove sized to commodity 1/4"
  rubber lip stock with a light press fit
- **File format:** STEP/F3D — rail length is playfield-layout-dependent, so ship
  source for builders adapting to a different cabinet width
- **Multi-piece:** Full-length rails on the 36"-deep playfield exceed 250mm —
  split into 2–3 segments with alignment-pin joints (2mm dowel pins, +0.1mm
  clearance holes) rather than one oversized piece

### Ball trough (3–5 ball capacity)
- **Material:** PETG (constant ball contact, needs impact/wear resistance)
- **Orientation:** Print on its side (long axis parallel to bed) to avoid
  supporting the full internal channel length
- **Supports:** Yes, tree supports for the channel roof; design with a removable
  access panel to clean supports out post-print rather than relying on
  supports-optional geometry
- **Tolerance:** Channel ID ≥28mm; ball-stop/switch-actuator cutouts sized to the
  specific microswitch footprint (Omron D2F series — see BOM-TIERS.md)
- **File format:** STEP/F3D (switch-mount cutouts are a common point builders
  will need to adjust for whatever switch they actually sourced)
- **Multi-piece:** At full 5-ball capacity this may approach the 250mm limit
  depending on final ball spacing — validate against final layout before
  finalizing as single-piece; design the split joint preemptively either way

### Plunger housing
- **Material:** PETG (spring compression + repeated impact)
- **Orientation:** Print with the bore axis vertical (bore printed as a hole, not
  bridged) for round, true bore geometry without elephant-foot distortion
- **Supports:** None if bore is vertical
- **Tolerance:** Bore ID uses sliding fit over the commodity plunger rod OD;
  spring-seat recess dimensioned to the sourced coil spring's OD with light
  clearance
- **File format:** STEP/F3D (rod/spring dimensions vary by source, so builders
  substituting a different spring need to edit the seat)

### Slingshot brackets (×2, Solid/Deluxe tiers)
- **Material:** PETG
- **Orientation:** Flat on bed
- **Tolerance:** Standard; rubber-band anchor posts sized to commodity pinball
  rubber band ID with a light press fit
- **File format:** STL

---

## Ramp system (Solid/Deluxe tiers, optional)

### Ramp section mounts
- **Material:** PETG (structural, holds ramp panel under ball rolling load)
- **Orientation:** Flat on bed where geometry allows; ramp entry/exit lips may
  need a 30–45° print angle with light supports to keep the ball-contact face
  clean
- **Tolerance:** Mounting-post holes sized for wood screws into playfield;
  ramp-panel slot uses sliding fit over the acrylic/polycarbonate sheet thickness
  sourced (nominal 1/16"–1/8", confirm actual stock before finalizing slot width)
- **File format:** STEP/F3D
- **Multi-piece:** A full 36"-deep ramp run will exceed 250mm — design as 3–4
  mount segments supporting a continuous acrylic/printed panel rather than one
  printed ramp surface

### Ramp panel (printed variant, if no acrylic sourced)
- **Material:** PETG (translucent PETG if a lit/backlit ramp effect is wanted —
  pairs with the WS2812B under-lighting)
- **Orientation:** Flat, widest face down, to keep the ball-rolling surface
  print-line-smooth (may need light sanding/acetone-vapor smoothing for PETG-adjacent
  ball roll quality — note for the build instructions, not this spec)
- **Multi-piece:** Same segmenting as the mounts above; align via dowel pins

---

## Backglass and cabinet fixtures

### Backglass frame mounts
- **Material:** PLA+ (low mechanical load, cosmetic)
- **Orientation:** Flat on bed
- **Tolerance:** Standard; sized to whatever backglass panel material is sourced
  (acrylic/printed graphic panel — not specified in DESIGN-BRIEF.md, flag as an
  open item alongside the theme question)
- **File format:** STL

### Wire guides and cable clips
- **Material:** PLA+ (no mechanical load beyond holding wire bundles)
- **Orientation:** Flat, whichever face minimizes supports (simple clip geometry)
- **Tolerance:** Snap-fit clip opening sized -0.2mm under 22 AWG bundle OD for
  positive retention without tools
- **File format:** STL

### Post inserts (decorative, lane markers)
- **Material:** PLA+ (cosmetic only)
- **Orientation:** Vertical, base down
- **Tolerance:** Press-fit into playfield-drilled holes (-0.1mm per DESIGN-BRIEF.md
  spec)
- **File format:** 3MF (color-variant markers benefit from a multi-color profile)

### LED strip diffuser channels
- **Material:** PLA+ (or translucent/natural PLA for light diffusion — natural
  PLA lets more light through than colored PLA without needing a dedicated
  diffuser material)
- **Orientation:** Print channel-side up, no supports needed for a simple
  U-channel profile
- **Tolerance:** Channel width matched to WS2812B strip PCB width (+0.3mm sliding
  fit per side) plus adhesive-backing clearance
- **File format:** STEP/F3D — channel length is cabinet-size-dependent

---

## Print settings summary (Bambu A1, all parts unless noted)

| Setting | PLA+ (cosmetic) | PETG (mechanical) |
|---|---|---|
| Nozzle temp | 210–220°C | 230–240°C |
| Bed temp | 55–60°C | 70–80°C |
| Layer height | 0.2mm | 0.2mm (0.16mm for flipper arms — impact face quality) |
| Infill | 15% (cosmetic) | 40–60% (flipper arms, trough, rail guides — load-bearing) |
| Perimeters | 2–3 | 4 (flipper arms — impact durability) |

---

## Assembly hardware convention

Where two printed parts join and aren't press-fit or snap-fit, standardize on
M3 heat-set inserts (Bambu-compatible, common brass insert size) rather than
self-tapping into raw plastic — reduces stripped-thread failures on repeated
disassembly during troubleshooting. Call this out explicitly in the eventual
t-005 build instructions package.

---

## Open items this catalog inherits from DESIGN-BRIEF.md

- **Ramp in MVP?** — this catalog specs the ramp system as Solid/Deluxe-tier
  content (per DESIGN-BRIEF.md's MVP scope, which lists the ramp as "if geometry
  fits — defer to t-003"). No ramp print files are needed for the Starter tier.
- **Theme** — post inserts, backglass frame, and pop bumper cap cosmetics are all
  themeable once Silas picks a direction (generic/Kind Robots/arcade retro/
  Humboldt nature); this catalog specs the neutral/undecorated geometry only.
- **Part size validation on the ball trough** — flagged above; needs a final
  layout pass once cabinet dimensions are locked to confirm single-piece vs.
  split-piece is required.

---

## Next steps

This catalog feeds pinball-hero/t-005 (final build package outline) directly and
t-004 (electronics plan) for the solenoid/motor mounting interfaces referenced
above. No CAD files exist yet — this document is the spec those files will be
built against, not the models themselves. No code or live service changes.
