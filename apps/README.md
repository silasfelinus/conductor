# apps/ — the AppMaker workshop

Each subfolder is one self-contained app project (Flutter unless noted),
created and managed by AppMaker (`projects/appmaker/`).

## The one-slug rule

An app named `<slug>` always has three artifacts sharing that slug:

| Artifact | Where | Role |
|---|---|---|
| `apps/<slug>/` | this folder | the code workspace |
| `projects/<slug>/roadmap.yaml` | conductor projects | drives Worker/Reviewer cycles |
| Dream (`dreamType: PROJECT`, same slug) | kind_robots DB | identity + display |

Use `scripts/new_app.py` (appmaker/t-002) to create all three consistently —
don't hand-roll the trio.

## Conventions

- Every app folder is a complete project root: own `pubspec.yaml`, own
  platform folders, own tests. Nothing in here imports across app folders.
- CI: `flutter analyze --fatal-infos` + `flutter test` must pass (see
  `.github/workflows/app-ci.yml`; it generalizes to `apps/**` with t-002).
- Secrets/keystores never live in this tree — see each app's `.gitignore`.
- Store submission for any app is a `needs-human` gate. No exceptions.
- An app can "graduate" to its own repository (permission-based git,
  appmaker/t-003); AppMaker keeps the slug → repo mapping when it does.

Note: the Conductor companion app predates this convention and lives at
`app/` in the repo root. Whether it migrates to `apps/conductor/` is an open
question on appmaker/t-001.
