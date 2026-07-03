# appmaker changelog

## 2026-07-02
- Project created from Silas's in-session direction.
- BRIEF.md: app factory on conductor — apps/<slug>/ workspace convention,
  three surfaces (kind_robots page, mobile app, conductor repo), two-phase
  permission-based GitHub model.
- Roadmap: t-001 approval gate, scaffolder, GitHub permission design,
  kind_robots page, mobile surface, Dream sync.
- apps/README.md documents the workshop convention.
- Icon/card/hero art queued in art-prompts.yaml.

## 2026-07-03
- GITHUB-APP-DESIGN.md (t-003): app manifest and least-privilege permissions,
  server-only credential handling, GithubInstallation/AppRepo data model
  (slug->repo mapping), connect/create/graduate flows, agent-role mapping for
  external repos, security invariants, and implementation tasks t-007..t-010.

## 2026-07-03 (t-004)
- AppMaker workspace page in kind_robots: fleet browser (roadmap progress,
  needs-you badges), self-serve create-an-app form, pending-scaffold chips.
- New endpoints: GET /api/appmaker/apps, POST /api/appmaker/scaffold-request
  (Dream + worker-queued AGENT todo, project cap enforced).
- Reachable from the workspace gallery via the new 'appmaker' card.
