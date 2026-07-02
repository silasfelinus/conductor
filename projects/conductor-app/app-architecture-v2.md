# Conductor App — Architecture v2 (Multi-User, Multi-Server)

Date: 2026-07-02
Supersedes: app-architecture.md (v1, approved with t-001). v1's screen list and
API mapping still apply; v2 revises the auth model, adds server modes, and
records the multi-user audit of kind_robots. Directed by Silas in-session.

---

## What changed since v1 and why

v1 designed a **Silas-only** app: the admin `KR_API_TOKEN` was to be compiled
into the binary via `--dart-define`. That is disqualifying for a public App
Store / Play Store app — anyone can extract a token from a shipped binary and
would gain admin write access to kindrobots.org and the conductor repo.

v2's goals (from Silas, 2026-07-02):
1. Multi-user correctness — the app must be safe with many users.
2. Bring-your-own-server or use our hosted server (paid tier later).
3. Local-only mode — full functionality without our DB.
4. Cover the kind_robots conductor-manager feature set with an app-like UI.
5. Path to iOS + Android app stores (submission itself stays `needs-human`).

## Where the code lives

`app/` at the conductor repo root. A Flutter project needs its own package
root (pubspec.yaml, platform folders), so it cannot merge into the repo base
folder; a subfolder keeps app + roadmaps + agent ops in one repo and CI can
path-filter. `projects/conductor-app/` remains the roadmap/design home; code
lives in `app/`.

## The two data layers (key architectural insight)

The kind_robots "conductor manager" is really two backends stitched together:

| Layer | Storage | Multi-user? | App treatment |
|---|---|---|---|
| **Core**: projects (Dream rows, dreamType PROJECT), todos, waypoints, priorities, statuses, users | Prisma/MySQL, JWT-scoped | Yes (already userId-aware) | The app's main surface, for every user |
| **Agent Ops**: roadmap YAML, pitches, inbox, approvals, art-request queue | GitHub passthrough to the single `silasfelinus/conductor` repo | No — single-tenant by nature | Opt-in layer, admin-role only, hidden from general users |

A general user's "project" is their own Dream + linked Todos. The GitHub
roadmap layer only makes sense for the server operator (Silas on hosted; a
self-hoster who wires their own conductor repo). This is how we get
multi-user correctness without pretending the shared repo can be multi-tenant.

## Server modes

Chosen at first launch, switchable in Settings:

1. **Hosted** — kindrobots.org. Free account now; membership/paid tier later
   (existing `isMember`/`memberUntil` fields support this).
2. **Self-hosted** — user enters a base URL of their own kind_robots instance.
   Identical API contract; their server, their data, their admin role.
3. **Local** — no network. Repositories have local implementations backed by
   on-device storage (SharedPreferences JSON now; migrate to drift/SQLite when
   data outgrows it). Same models, so a later "attach to server" migration is
   straightforward.

## Auth model

- Username/password → JWT (`POST /api/auth/login`), stored in
  keychain/keystore via flutter_secure_storage. Google OAuth later (WebView).
- **No admin token anywhere in the app.** All privileged calls ride the
  user's JWT; the server checks `Role === 'ADMIN'`.
- The app decides what UI to *show* from `/api/users/me` role, but the server
  is the enforcement point.
- On 401: clear stored JWT, return to login.

## Multi-user audit of kind_robots (2026-07-02)

Fixes shipped on branch `claude/conductor-app-dev-wd4rcc` (kind_robots) are
marked ✅; the rest are follow-up tasks in the roadmap.

**Critical — unauthenticated writes to the conductor repo.** These endpoints
had no auth at all; any anonymous caller could write to the repo:
- `POST /api/conductor/pitch` ✅ now admin-gated
- `POST /api/conductor/pitch-vote` ✅ now admin-gated
- `POST /api/conductor/inbox` ✅ now admin-gated
- `POST /api/conductor/message` ✅ now admin-gated
- `POST /api/conductor/overrides` ✅ now admin-gated
(`art-request.post` was already admin-gated; reads stay public for now.)

**Cross-user data leak:** `GET /api/todos/dream/[dreamId]` returned every
user's todos for a dream (not userId-scoped) ✅ now scoped to the caller.

**Remaining single-user assumptions (follow-up tasks, not blockers):**
- Pitch votes and project priorities live in browser localStorage
  (`conductorStore`), not per-user DB state → move to DB or accept as
  operator-only quirk.
- `syncMissingProjects()` hardcodes `userId: 1`; `userIsAdmin` treats
  `id === 1` as admin; guest fallback `userId 10`.
- `PATCH /api/dreams/[id]/priority` has no owner check (admin-only today, so
  acceptable; must add owner check before opening to members).
- No push notification infrastructure (polling for MVP, as v1 planned).
- `FREE_PROJECT_LIMIT = 2` for non-member users is the existing hook for the
  paid tier.

## Feature parity map (conductor-manager → app)

| conductor-page.vue capability | App location | Status |
|---|---|---|
| Project gallery + priority sort | Dashboard | scaffolded |
| New project (Dream) + project cap | Dashboard FAB | scaffolded |
| Project status/priority/intent editing | Project detail | scaffolded (status, priority, full intent editor) |
| Waypoints (add/cycle/reorder/remove) | Project detail | scaffolded |
| Todos: create, edit, filter, done/archive, categories | Todos tab | scaffolded |
| Feature wishlist (DESIRED_FEATURE + order, promote/retire) | Project detail | scaffolded |
| Brainstorm / pitch voting | Approvals tab (Agent Ops) | scaffolded |
| Needs-human approvals queue | Approvals tab (Agent Ops) | scaffolded |
| Conductor inbox messages | Approvals tab reply action | scaffolded |
| Per-project AI chat | — | follow-up task (m3) |
| Art gallery / art requests | — | follow-up task (m3) |
| Sync GitHub slugs → Dreams | operator tool, not app MVP | deferred |

## Store readiness (all gated needs-human before submission)

- Bundle ids `org.kindrobots.conductor_app`; signing assets never committed.
- Privacy: local mode = zero data collection — a genuine store-listing asset.
- Account deletion path required by Apple (kind_robots has user delete).
- Nothing in this plan auto-submits; store submission is a `needs-human` task.
