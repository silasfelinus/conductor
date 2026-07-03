# Conductor App

Flutter client for Conductor — the deluxe task manager for humans and their AI
agents. Targets iOS and Android app stores; web and desktop later.

## Three ways to run it

| Mode | What it means | Account |
|---|---|---|
| **Kind Robots Cloud** | Our hosted server (kindrobots.org). Sync across devices. Paid tier planned. | Yes |
| **Your own server** | Any self-hosted [kind_robots](https://github.com/silasfelinus/kind_robots) instance. Same API. | Yes (on your server) |
| **Just this device** | No server, no account. Data stays local. | No |

The mode is chosen at first launch and can be switched in Settings.

## Auth model (multi-user)

- Users sign in with username/password → JWT, stored in the platform
  keychain/keystore (`flutter_secure_storage`).
- **No admin API token ships in the binary.** Privileged features (Agent Ops:
  roadmap approvals, pitch voting, conductor inbox) are authorized
  *server-side* by the signed-in user's role. Non-admin users simply never see
  that layer.
- Core features (projects, tasks/todos, waypoints) are per-user via the
  JWT-scoped kind_robots endpoints (`/api/dreams`, `/api/todos`).

## Repo layout

```
lib/
  core/         config (server modes), api client, storage, theme
  features/
    onboarding/ server picker (hosted / self-hosted / local)
    auth/       login, register, auth state
    projects/   Dream-backed projects, waypoints, dashboard, detail
    todos/      todo list + composer (dreamId links todos to projects)
    agent_ops/  conductor-repo layer: roadmaps, approvals, pitches (admin only)
    settings/
```

Repositories are interfaces with **remote** (HTTP) and **local** (on-device)
implementations, so local mode is a first-class citizen rather than a cache.

## Getting started

```sh
cd apps/conductor
flutter pub get
flutter test
flutter run
```

Platform folders (`android/`, `ios/`) are committed; run `flutter create .`
again only when adding a new platform target. Never commit keystores,
provisioning profiles, or `key.properties` (see `.gitignore`).

## Store release (gated)

App-store submission is `needs-human` in the conductor roadmap — nothing here
auto-publishes. Release checklists will live in `docs/` as they develop.
