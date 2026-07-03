# conductor-app changelog

## 2026-06-28
- Added initial project scaffold.
- Added workspace image request queue entries.

## 2026-07-02
- Wrote app-architecture-v2.md: multi-user auth (no admin token in binary), three server
  modes (hosted / bring-your-own-server / local-only), app placement in app/ at repo root.
- Scaffolded the Flutter app in app/: server picker, login/register, projects dashboard
  (Dream-backed), project detail with waypoints, todos, Agent Ops approvals, settings.
- Audited kind_robots for multi-user safety; auth fixes shipped on the matching
  kind_robots branch (see TALKBACK security flag).
- Roadmap: t-002 in review; added t-006 (v2 approval gate), t-007 (votes/priorities to DB),
  t-008 (wishlist/intent editor), t-009 (project chat + art), t-010 (store readiness, gated).

## 2026-07-02 (round 2)
- Project intent editor (title/goal/description/pitch/flavorText/liveUrl/repoUrl).
- Feature wishlist: ordered DESIRED_FEATURE todos with move/promote/retire.
- Waypoints: long-press to reorder or remove.
- Todos: tap to edit; DESIRED_FEATURE selectable in composer.
- Offline resilience: remote projects/todos fall back to last-good cached data
  on network failure (server auth errors still surface).
- Approvals badge on the nav bar with 5-minute foreground polling (MVP
  notification strategy from t-004).
- Fixed a ThemeData.cardTheme API that breaks newer Flutter versions.
- Tests: ServerConfig, model round-trips, local repository CRUD.

## 2026-07-02 (round 3)
- Per-project AI chat (t-009): streaming assistant on the dream-<id>-assistant
  channel with history, project-context system prompt, and reply persistence.
- Project artwork: dashboard thumbnails and detail hero banners, resolved
  against the configured server URL (hidden in local mode).
- CI: app-ci.yml runs flutter analyze + test on every push touching app/.
- Toolchain now runs in the agent container too: analyze + 18 tests green
  before every push.
