# Pinball Machine — Bill of Materials by Tier

Generated: 2026-07-22
Task: pinball-hero/t-002
Depends on: DESIGN-BRIEF.md (approved 2026-07-01)

Three build tiers, matching DESIGN-BRIEF.md's variant table. Every tier shares the
same cabinet and printed mechanical parts (see PRINTABLE-MODELS.md for those);
this document covers purchased/commodity parts and where each tier diverges.
Prices are 2026 US street-price estimates for a single build, not bulk/kit pricing.

---

## How to read this

- **Common to all tiers** parts are listed once, then each tier's table only lists
  what's added or swapped.
- **"Salvage-friendly"** flags a part where a used/pulled part from a donor machine
  or parts-bin source is normally better value and comparable quality to new.
- Part numbers are examples of a known-good class of part, not an endorsement of one
  seller — home builders should price-check against whatever hobby/electronics
  supplier is cheapest in their region (Amazon, AliExpress, McMaster-Carr, Marco
  Specialties/PinballLife for pinball-specific hardware, Pinbits for EU builders).

---

## Common to all tiers

### Cabinet and playfield structure
| Part | Spec | Est. cost | Source |
|---|---|---|---|
| Cabinet plywood | 3/4" Baltic birch, 1 sheet (4'×8', cut down) | $65–90 | Home center / hardwood supplier |
| Playfield panel | 1/2" MDF, 18"×36" cut | $15–25 (from the same or a second sheet) | Home center |
| Leg levelers | 4×, M8 threaded, load-rated ≥25 lb each | $8–12 | Hardware store / Amazon |
| Piano hinge | 18" length, steel | $6–10 | Hardware store |
| Prop rod | 1× steel rod + eye screws (DIY) or purchased playfield support | $3–5 | Hardware store |
| Lock hasp | Small cabinet hasp + padlock (optional) | $5–8 | Hardware store |
| Wood screws, glue, corner brackets | Assorted | $10–15 | Hardware store |
| **Subtotal** | | **≈ $112–165** | |

### Playfield hardware
| Part | Spec | Est. cost | Source |
|---|---|---|---|
| Steel pinball(s) | 1-1/16" (27mm), 1–3× | $3–8 | PinballLife / Marco Specialties / Amazon |
| Rubber ring/band service kit | Standard pinball rubber kit (various sizes) | $12–18 | PinballLife / Marco Specialties |
| Microswitches | Omron D2F or equivalent, 4–8× (targets, trough, slings) | $10–20 (bulk pack) | Amazon / AliExpress |
| Coil spring, plunger | Standard pinball plunger spring | $4–6 | PinballLife / Marco Specialties |
| Plunger rod + tip | Steel rod + rubber/plastic tip | $6–10 | PinballLife (salvage-friendly: a donor plunger assembly is often cheaper) |
| Transparent playfield overlay (optional) | Polycarbonate sheet, 1/16"–1/8" | $15–25 | TAP Plastics / Amazon |
| **Subtotal** | | **≈ $50–87** | |

### Electronics core
| Part | Spec | Est. cost | Source |
|---|---|---|---|
| Microcontroller | Raspberry Pi Pico (or Pico W for wireless scoring/telemetry) | $5–8 | Adafruit / Amazon |
| Power supply | ATX PC power supply (repurposed) or 5V/12V dual-rail bench supply | $0 (salvage-friendly, old PC PSU) – $25 (new) | Salvage bin / Amazon |
| Fuses | 5V logic rail 2A, plus per-tier solenoid fusing (below) | $5–8 (assorted fuse kit) | Amazon |
| Wiring | 22 AWG hookup wire, connectors, heat-shrink | $15–20 | Amazon |
| **Subtotal** | | **≈ $25–61** | |

### Lighting and score display
| Part | Spec | Est. cost | Source |
|---|---|---|---|
| LED strip | WS2812B, ~2m, 60 LED/m | $12–18 | Amazon / Adafruit |
| Score display | 4-digit 7-segment (TM1637 driver) — starter/solid; upgrade path to OLED — see Open Questions | $6–10 | Amazon |
| **Subtotal** | | **≈ $18–28** | |

**Common-to-all running total: ≈ $205–341** (before tier-specific flipper/pop-bumper/audio additions below)

---

## Starter tier — target $60–90 *tier-specific add-on cost*

Flippers are spring-assisted (printed arm, no solenoid), no pop bumper, no ramp,
basic buzzer for audio. This is the cheapest path to "actually playable."

| Part | Spec | Est. cost | Notes |
|---|---|---|---|
| Flipper return | 2× extension/torsion spring sized to printed flipper arm | $4–8 | Hardware store spring assortment |
| Flipper actuation | Manual button → printed linkage (no motor) OR small hobby servo (SG90-class) ×2 if button-triggered assist wanted | $0 (pure mechanical) – $10 (2× servo) | Amazon |
| Audio | Piezo buzzer or single small speaker, no amp | $2–4 | Amazon |
| Fixed bumpers | 2–4×, passive, printed cap + rubber ring only (no coil) | $0 extra (rubber rings already in common kit) | — |
| **Tier add-on subtotal** | | **≈ $6–22** | |

**Starter tier total (common + add-on): ≈ $211–363.** Runs above the DESIGN-BRIEF.md's
original $60–90 estimate once cabinet material and full electronics core are priced
individually rather than assumed already on hand — see "Reconciling with the design
brief's estimate" below.

---

## Solid tier — target $120–180 *tier-specific add-on cost*

Adds a DC-motor-actuated flipper (safer and simpler than a true coil), one solenoid
pop bumper, a printed ramp, and a small amplified speaker.

| Part | Spec | Est. cost | Notes |
|---|---|---|---|
| Flipper actuation | 2× DC gear motor (12V, ~100:1 gearbox) + motor driver board (e.g. L298N dual H-bridge) | $18–28 | Amazon |
| Pop bumper solenoid | 1× 12V pinball-style solenoid coil (salvage-friendly: pulled coil from a parts machine) | $8–15 new / $5–10 salvage | PinballLife or eBay parts-machine listing |
| Solenoid driver | 1× MOSFET driver module rated ≥3A, flyback diode | $4–8 | Amazon |
| Thermal fuse (per coil) | SF series, 75°C inline fuse | $2–3 | Amazon / Mouser |
| Ramp material | Clear or translucent 1/16" polycarbonate strip, formed/heat-bent, or multi-piece PETG print | $10–15 | TAP Plastics (if bent) or filament only (if printed) |
| Audio | Small 3W speaker + PAM8403 class-D amp module | $6–10 | Amazon |
| **Tier add-on subtotal** | | **≈ $48–79** | |

**Solid tier total (common + add-on): ≈ $253–420.**

---

## Deluxe tier — target $200–300 *tier-specific add-on cost*

Adds salvaged genuine solenoid flipper coils (authentic feel), pop bumper +
slingshots (both solenoid-driven), printed-and-acrylic ramp, amplified stereo audio.
This tier is the one place DESIGN-BRIEF.md's "judgment call" (spring/DC vs. true
solenoid flippers) is spent — see Safety below before building this tier.

| Part | Spec | Est. cost | Notes |
|---|---|---|---|
| Flipper coils | 2× genuine EOS-switched flipper coil assembly, salvaged from a donor machine | $20–40/pair salvage (new coil-only kits run $60+/pair) | eBay parts-machine listing / PinballLife rebuild kit |
| Flipper coil driver | 24–48V-rated dual driver board sized to coil spec, opto-isolated inputs | $15–25 | PinballLife / Marco Specialties driver board, or a DIY MOSFET+opto board |
| Dedicated 24–48V supply | Separate supply for the coil bus — **must stay physically isolated from the 5V logic rail** (DESIGN-BRIEF.md safety constraint) | $20–30 | Amazon (meanwell-class supply) |
| Slingshot solenoids | 2×, 12V, plus kickback rubber | $16–30 salvage/new mix | PinballLife |
| Pop bumper + slingshot drivers | Shared MOSFET driver bank sized for 3 coils total | $10–18 | Amazon / Mouser |
| Ramp material | Printed structural ramp + acrylic surface panel | $20–30 | TAP Plastics + filament |
| Audio | Small stereo amp (e.g. PAM8403 dual-channel) + 2× 3W speakers | $12–18 | Amazon |
| Per-coil thermal fuses | SF series ×3 (2 flippers + 1 pop/sling shared or separate) | $6–9 | Mouser |
| **Tier add-on subtotal** | | **≈ $119–200** | |

**Deluxe tier total (common + add-on): ≈ $324–541.**

---

## Safety notes carried from DESIGN-BRIEF.md (apply per tier)

- Starter tier has no solenoids, so the 5V/24V isolation rule doesn't apply — it's
  the simplest tier to wire safely and the right starting point for a first-time
  builder.
- Solid and Deluxe tiers introduce solenoids: keep the 24V (or 48V, Deluxe coil-only)
  bus **physically separate** from the 5V logic rail — no shared ground bus bar
  without a fuse between them, no shared connector housings between rails.
- Fuse every coil individually (1A per solenoid) plus a 3A bus fuse upstream of all
  coils combined, and a 2A fuse on the 5V logic rail — per DESIGN-BRIEF.md.
- Add a 75°C inline thermal fuse per coil on Solid/Deluxe — coils can reach 60–70°C
  under sustained play.
- Deluxe-tier genuine solenoid flippers are the one part of this BOM DESIGN-BRIEF.md
  flags as elevated fire/shock risk if mis-wired; that tier's driver board and 24–48V
  supply should only be attempted by a builder comfortable reading a solenoid driver
  schematic, not as a first electronics project.

---

## Reconciling with the design brief's estimate

DESIGN-BRIEF.md's variant table quotes $60–90 / $120–180 / $200–300 for
Starter/Solid/Deluxe. Those figures read as **tier-specific incremental cost**
(flippers + pop bumper + ramp + audio only) and match this document's "tier
add-on subtotal" rows closely once salvage options are chosen. This document adds
the shared cabinet + core electronics + playfield hardware baseline (≈$205–341)
that DESIGN-BRIEF.md's table didn't itemize, since it's identical across all three
tiers and a first-time builder needs to know the full out-of-pocket total, not just
the delta between tiers. No change to DESIGN-BRIEF.md's own numbers — this is an
itemization, not a correction.

---

## Open questions this BOM inherits from DESIGN-BRIEF.md (unresolved, Silas's call)

These affect BOM line items directly and are repeated here rather than re-litigated:

1. **Flipper drive preference** (spring-assist/DC motor vs. true solenoid from the
   start) — this document priced spring-assist as Starter's default and true
   solenoids as Deluxe-only, per DESIGN-BRIEF.md's own recommendation. If Silas
   wants solenoid flippers available at the Solid tier too, that tier's add-on
   subtotal moves up by roughly the Deluxe flipper-coil delta (~$35–65).
2. **Score display** (7-segment vs. small LCD/OLED) — this BOM prices the 7-segment
   TM1637 option (cheaper, simpler firmware) as the default across all tiers. An
   OLED swap is a low-cost change (~$5–8 more) if Silas prefers it — noted here
   rather than assumed silently.
3. **Cabinet material** — DESIGN-BRIEF.md's own recommendation (3/4" Baltic birch
   plywood cabinet, 1/2" MDF playfield) is used as-is in the common BOM above.

---

## Next steps

This BOM feeds pinball-hero/t-004 (electronics and control plan, once flipper drive
preference is confirmed) and t-005 (final build package outline). No code or live
service changes — this is a planning document only.
