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
