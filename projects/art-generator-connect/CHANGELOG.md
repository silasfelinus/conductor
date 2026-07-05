# art-generator-connect CHANGELOG

## 2026-06-28
- Project promoted from approved pitch.
- Initial roadmap scaffolded.
- Workspace art prompts queued.

## 2026-07-05
- Silas-directed session: answered "what's holding the pipeline back" in
  docs/pipeline-architecture.md — home-server durability, missing job queue,
  comfy machine-auth mismatch, no closing consumer.
- Routing policy set: stateful actions (generation, assets, tokens/mana) go
  through kind_robots; machine-level actions (health probes, process
  supervision) may go direct to the home server.
- Delivered ops/home-server/ pm2 supervision kit (auto-restart, boot
  persistence, health watchdog) for ComfyUI + A1111 → t-009 needs-human.
- New milestone m5 with t-009 (install kit), t-010 (kind_robots ArtJob queue
  + pull relay agent), t-011 (comfy apiKey auth parity), t-012 (conductor
  consumer, waiting on t-010, human-gated first run).
