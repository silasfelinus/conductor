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

Use `scripts/new_app.py` to create all three consistently — don't hand-roll
the trio:

```sh
python scripts/new_app.py recipe-box --title "Recipe Box" --description "a cozy cooking companion"
```

It scaffolds the app skeleton, the roadmap, art prompts, and registry entries,
and files the Dream-sync todo when `KR_API_TOKEN` is set. Platform folders are
generated afterwards with `flutter create` (the script prints the command).

## Conventions

- Every app folder is a complete project root: own `pubspec.yaml`, own
  platform folders, own tests. Nothing in here imports across app folders.
- CI: `flutter analyze --fatal-infos` + `flutter test` must pass (see
  `.github/workflows/app-ci.yml`; it generalizes to `apps/**` with t-002).
- Secrets/keystores never live in this tree — see each app's `.gitignore`.
- Store submission for any app is a `needs-human` gate. No exceptions.
- An app can "graduate" to its own repository (permission-based git,
  appmaker/t-003); AppMaker keeps the slug → repo mapping when it does.

The Conductor companion app lives at `apps/conductor/` (migrated from the
repo-root `app/` on 2026-07-02 per Silas's t-001 decision — consistency wins).
