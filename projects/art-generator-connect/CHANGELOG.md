# art-generator-connect CHANGELOG

## 2026-07-06 (later)
- Closed the second art lane (t-021): added scripts/consume_art_requests.py to
  drain the requests: block of art-prompts.yaml through the same kind_robots
  ArtJob queue as the project-art batch, mark each request done
  (comment-preserving, idempotent skip-if-exists), and hand results to
  distribute_images.py. Wired into auto-art-generate.yml. Now every art request
  — project assets, missing-image reports, and Serendipity voice — funnels
  through one queue with a consumer. 8 new unit tests (22 total green).

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

## 2026-07-05 (overnight session, continued)
- URL-MAPPING.md revised per Silas: canonical placement is
  public/images/{schema_or_project}/{slug}/{slug}-{utility}-{n}; artcollections/
  demoted to unsorted fallback. New t-013 aligns tooling.
- t-010 + t-011 implemented in kind_robots PR #90: ArtJob queue (additive
  migration, enqueue/claim/complete/list/poll endpoints, atomic claiming) and
  requireMachineUser auth parity for comfy routes. Both -> status: review.
- Relay agent shipped: ops/home-server/relay_agent.py (pull-based, stdlib-only,
  pm2-managed; opt-in kr-relay block added to ecosystem.config.js).
- Silas merged kind_robots PR #90 overnight: ArtJob queue + comfy machine-auth
  live. t-010/t-011 done; t-012 (consumer) now ready; kaizen t-014 added.
- t-009 done: Silas installed and live-verified the pm2 stack (reboot
  survival, health endpoints, relay polling prod). Last human gate in m5
  cleared; first live queue job submitted end-to-end this session.
- kind_robots PR #96 merged (Silas-directed): save-generated joins
  requireMachineUser; relay's admin token now works end-to-end. Kaizen t-015
  filed (auth sweep). Relay gained local fast path (PR #220): finished images
  also land in local public/images/{collection}/ folder collections.

## 2026-07-06
- FIRST FULLY AUTONOMOUS GENERATION: ArtJob 2 -> claim -> forge render ->
  save-generated (ArtImage 4032) -> DONE -> local copy at
  kind_robots public/images/comfy/comfy-4032.png. Verified live by Silas.
  The m5 loop (supervision + queue + machine auth + relay) is operational
  end-to-end. Remaining m5 work is enrichment: t-012 (consumer feeds queue
  from art-generate.yaml), t-013 (placement/webp/gallery.json), t-014
  (contract tests), t-015 (auth sweep).

## 2026-07-06 (night session, continued)
- t-015 done (kind_robots PR #97): machine-auth sweep - art/generate,
  openai images, textGate onto requireMachineUser; three comfy routes'
  redundant inline checks removed.
- t-014 done (kind_robots PR #97): server/api/art/queue/queue.http contract
  tests (lifecycle + negatives).
- t-013 done: distribute_images.py nested folders + {utility}-{n} numbering
  + collections.json master index (5 tests); kind_robots folder endpoint
  resolves nested -> flat -> artcollections (PR #98).
- t-012 built: scripts/consume_art_queue.py (dry-run default, 6 tests,
  Pillow webp conversion w/ png fallback) -> needs-human for the first
  live cycle.
- Filed conductor/t-024: pre-existing test_run_worker_status_integration
  failures found on clean main.
