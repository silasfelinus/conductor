# Pinball Machine Design Brief

Generated: 2026-06-30
Task: pinball-hero/t-001

---

## What We're Building

A compact, partly 3D-printed pinball machine designed for home builders. The target is a real, working machine — not a toy — that someone with a Bambu Lab A1-class printer and basic woodworking skills can build over several weekends. The plans will be released as a free or low-cost package (Printables / GitHub) and optionally a premium tier with premium extras.

---

## Cabinet / Playfield Size

**Target:** "Mini cabinet" — roughly 18" wide × 36" deep playfield, total cabinet height ~50"

**Rationale:**
- Fits through a standard interior door without disassembly
- Shorter playfield = lower part count and cost at first build
- 18" width is compatible with ~16" printable playfield elements (Bambu A1 bed: 256mm × 256mm × 256mm)
- Full-size (21" × 42") is a stretch goal for version 2

**Playfield inclination:** ~6.5° (standard pinball; adjustable feet)

---

## Mechanical Scope (MVP)

### Included in first build
- Spring-loaded plunger lane (print the housing; use a commodity coil spring)
- 2 × flippers (left + right) — printed arms + purchased coil assemblies or solenoids
- 2–4 fixed bumpers (passive, no solenoids) — printed caps + purchased rubber rings
- 1 × active pop bumper (optional, solenoid-driven, if electronics budget allows)
- Inlanes and outlanes (printed guide rails + purchased 1/4" rubber lip)
- Printed ball trough (3–5 ball capacity)
- Slingshots: printed brackets; rubber band driven at MVP, solenoid optional
- 1 basic ramp (printed PLA/PETG, if geometry fits — defer to t-003)
- LED under-playfield lighting (WS2812B strip)
- Score display: 7-segment or small LCD panel on the backglass

### Not included at MVP
- Multiball lock mechanism (v2)
- Motorized spinner (v2)
- Shaker motor (v2)
- Live DMD / video display (scope creep — v2 only)
- Genuine coil solenoid flippers (optional premium tier only; beginners use rubber-band or spring-assisted flippers first)

---

## What Should Be Printed vs. Purchased

### 3D Printed (Bambu A1 friendly)
- Playfield rail guides and lane dividers
- Pop bumper cap and housing
- Fixed bumper caps
- Flipper arms and pivot brackets
- Ball trough
- Plunger housing
- Backglass frame mounts
- Wire guides and cable clips
- Post inserts (decorative, lane markers)
- Ramp section mounts (if ramp included)
- LED strip diffuser channels

### Purchased (commodity off-the-shelf)
- Plywood or MDF sheet for cabinet body and playfield surface (≥ 3/4" for cabinet, ≥ 1/2" for playfield)
- Leg levelers (4×)
- Rubber rings and bands (standard pinball service kit)
- Steel ball (1–3 × standard 1-1/16" pinball balls)
- Coil spring for plunger
- Microswitches (Omron D2F series or similar) for target/bumper contacts
- Solenoid coils (only for flipper drive and pop bumper; cheapest option: salvage from a $20 eBay parts machine)
- 12V/5V power supply (computer ATX PSU works well; fan is a bonus)
- WS2812B LED strip, ~2m
- Microcontroller: Raspberry Pi Pico or similar (see electronics section)
- Transparent polycarbonate sheet for playfield overlay (optional)
- Piano hinge for playfield lift
- Lock hasp for cabinet
- Audio: small 3W speaker + PAM8403 amp module

### Judgment call: coils vs. rubber-band flippers
Full solenoid flippers are authentic but add ~$30–60 parts cost, require higher-voltage (24–48V) solenoid driver boards, and add fire risk if wired incorrectly. **Recommendation for beginner tier**: spring-assisted printed flipper with a DC motor actuator or servo — simpler, safer, 5V-compatible. Solenoid flipper kit as optional upgrade instructions.

---

## Bambu A1 Print Constraints

**Bed size:** 256mm × 256mm × 256mm  
**Recommended materials:**
- PLA+ for decorative, non-stress parts (bumper caps, cosmetics)
- PETG for mechanical parts that see heat, flex, or friction (flipper arms, trough, rail guides)
- ASA/ABS: skip unless the machine will live in a hot garage; PETG is more beginner-friendly

**Part size rule:** No single printed part may exceed 250mm in any dimension. Multi-piece assemblies need alignment pins or snap-fit joints.

**Tolerances:**
- Sliding fits: +0.3mm per side
- Press fits: -0.1mm per side
- Ball passage guides: min 28mm ID (1-1/16" ball is 27mm OD)

**Print orientation notes:**
- Flipper arms: print perpendicular to pivot axis for layer-line strength
- Rail guides: flat on bed, no supports needed if designed with ≤45° overhangs
- Pop bumper caps: print upside-down with minimal supports (aesthetic surface faces down = clean result)

---

## Safety Constraints

- **Voltage:** Keep logic at 5V. Solenoids (if included) run on 24V via a separate supply with a dedicated fuse per coil. 24V and 5V rails must be isolated; never mix.
- **Fusing:** 1A fuse per solenoid; 3A total solenoid bus fuse; 2A on the 5V logic rail.
- **Heat:** PETG parts can soften above ~80°C. Coil solenoids can reach 60–70°C under heavy use — add a thermal fuse (SF Series, 75°C) inline per coil if using solenoids.
- **Ball retention:** The cabinet must physically prevent the ball from leaving the play area without player intent. Trough must be fully enclosed.
- **Playfield lift safety:** Piano hinge + prop rod (never leave playfield propped without locking it).

---

## Build Variants

| Tier | Flippers | Pop bumper | Ramp | Audio | Est. cost |
|---|---|---|---|---|---|
| Starter | Spring-assist (printed) | No | No | Basic buzzer | $60–90 |
| Solid | DC motor actuator | Yes (solenoid) | Printed ramp | Speaker + amp | $120–180 |
| Deluxe | Salvage solenoid coils | Yes + slingshots | Printed + acrylic | Amplified stereo | $200–300 |

All tiers use the same cabinet and printed mechanical parts. Differences are in the electronics and solenoid options.

---

## Open Questions for Silas

1. **Flipper drive preference:** Spring-assist / DC motor (simpler, safer) or solenoid from the start? This determines the electronics BOM significantly.
2. **Target theme:** Generic "pinball machine" open-source release, or a specific theme (Kind Robots, arcade retro, Humboldt nature)? Theme drives the playfield art and bumper sculpts.
3. **Ramp in MVP?** A ramp requires polycarbonate bending or a multi-piece printed structure. In or out for first version?
4. **Score display:** 7-segment digits (retro, easy) or small LCD/OLED (modern, requires more code). Both fit the budget.
5. **Cabinet material:** Plywood (heavier, easier to route) or MDF (smoother finish, heavier, doesn't hold screws as well). Recommendation: 3/4" Baltic birch plywood for cabinet, 1/2" MDF for playfield surface.
6. **Release format:** Free on Printables + GitHub, or paid PDF manual on Gumroad (see brainstorm pitch 2026-06-30-pinball-parts-pack.md)?

---

## Downstream Task Dependencies

This design brief feeds:
- pinball-hero/t-002: BOM tiers and common-source parts
- pinball-hero/t-003: 3D printable model set specification
- pinball-hero/t-004: Electronics and control plan (requires t-001 + t-002 input on flipper drive)
- pinball-hero/t-005: Final build package outline
