# Pinball Hero — Open-Source Software Stack Survey

Generated: 2026-06-30
Task: pinball-hero/t-006

---

## Summary

The dominant recommendation for a homebrew pinball build in 2025 is **Mission Pinball Framework (MPF)**. It is the only fully open-source, hardware-agnostic, actively maintained option with a large community and complete feature set. All other options are either hardware-locked, simulation-only, or low-activity.

---

## Comparison Table

| Project | Language | Hardware support | Beginner-friendly | Community | License | Verdict |
|---|---|---|---|---|---|---|
| **Mission Pinball Framework** | Python | Hardware-agnostic (FAST, P-ROC, OPP, Arduino, Raspberry Pi, virtual) | Good (docs are thorough; learning curve is real) | Large, active (Discord, forums, YouTube series) | MIT | **Recommended** |
| FAST Pinball (software) | Python/config | FAST hardware only | Moderate (tied to FAST ecosystem) | Medium (FAST-focused forums) | Proprietary | Skip unless buying FAST hardware |
| Multimorphic P-ROC/P3-ROC | Python | P-ROC/P3-ROC hardware only | Moderate | Small-medium | Commercial | Skip — expensive hardware lock-in |
| Visual Pinball X (VPX) | C++/VBScript | PC simulation only | Easy for play; hard for authoring | Very large (simulation community) | GPL | Wrong tool — simulation, not control |
| pypinball | Python | Experimental/Arduino sketch | Low (minimal docs, limited scope) | Very small, low activity | MIT | Prototype only |
| MiSTer FPGA pinball cores | FPGA HDL | FPGA emulation | Low (FPGA development required) | Niche (emulation community) | Mixed | Wrong use case — emulation of classic hardware |

---

## Mission Pinball Framework (MPF) — Detail

**Website:** `missionpinball.org`  
**Repo:** `github.com/missionpinball/mpf`  
**Language:** Python 3  
**Latest stable:** MPF 0.57.x (active development)  
**License:** MIT

### What it does

MPF is a game engine for real pinball machines. It handles:
- Coil/solenoid firing (flipper physics, bumpers, kickers)
- Switch/sensor matrix (ball detection, rollover lanes)
- LED/lamp control (RGB lighting effects, shows)
- Audio/video (pygame-based display engine, music, callouts)
- Scoring logic (modes, bonus, multipliers)
- Ball management (ball trough, VUK, multi-ball)
- Hardware communication over USB/serial/Ethernet

### Hardware support

MPF is hardware-agnostic through platform plugins:
- **FAST Pinball** — commercial, full-featured, most tested with MPF
- **Open Pinball Project (OPP)** — open-source hardware, low cost, active
- **Multimorphic P-ROC/P3-ROC** — mature, commercial
- **Arduino** — via `mpf-arduino-bridge` (experimental; best for prototyping individual nodes)
- **Raspberry Pi** — can run MPF; GPIO direct-drive is possible but requires care on power domains
- **Virtual** — built-in platform for testing without hardware; good for development

For pinball-hero, **OPP or Arduino bridge** are the most cost-effective starting points for a scratch build.

### Beginner friendliness

- The MPF docs are genuinely good (missionpinball.org/docs) and cover basic machine setup through advanced mode logic
- Configuration is YAML-based (machines are defined in config files, not raw code) — no Python required for basic builds
- Python is used for advanced custom logic when YAML isn't enough
- Learning curve is real but manageable; the "getting started" tutorial is a 1–2 day investment
- Large Discord community with active developers who answer beginner questions

### Constraints / notes

- MPF requires a host computer (Raspberry Pi 4 or small PC) running during play — there's no firmware-only mode
- The visual display engine (mpf-mc) requires more hardware (separate display controller or Pi with HDMI)
- Coil/solenoid power safety (high voltage, inrush current, flyback protection) is NOT handled by software — this is an electrical design concern independent of MPF
- The flipper latency on Raspberry Pi GPIO is acceptable for casual play but tighter hardware (OPP, FAST) gives better response time

---

## Visual Pinball X (VPX) — why it's excluded

VPX is the gold standard for PC-based pinball simulation. It's excellent for designing and playing virtual machines, and builders sometimes use it to prototype playfield physics before committing to physical construction. However, it does not control real hardware — it's a simulator, not a machine controller. Excluded from this survey as out-of-scope, but worth knowing about for prototyping layout/physics before cutting wood.

---

## Recommendation for pinball-hero

**Start with Mission Pinball Framework + Open Pinball Project hardware.**

Rationale:
- OPP boards are open-source, available as kits, and well-documented
- MPF + OPP is the most popular DIY stack with the most homebrew build documentation online
- Raspberry Pi 4 as host is affordable and runs MPF well
- MIT license allows the final build-plan package to reference, modify, and redistribute MPF config examples freely
- If the build scales up, migrating to FAST hardware is straightforward since MPF supports both

**First software milestone for Silas to consider:** Install MPF + OPP simulator, run the tutorial machine, and confirm the development workflow before committing to hardware choices. This costs zero dollars and one evening.
