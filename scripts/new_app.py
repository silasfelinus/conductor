#!/usr/bin/env python3
"""
new_app.py — AppMaker scaffolder (appmaker/t-002).

Creates everything a new app needs, consistently, in one command:

  apps/<slug>/                    Flutter app skeleton (lib/, test/, pubspec)
  projects/<slug>/roadmap.yaml    conductor project driving agent cycles
  projects/<slug>/CHANGELOG.md
  art-prompts.yaml entries        icon / card / hero, status pending
  project-overrides.yaml          registered active/normal
  projects/priority.yaml          appended to the priority order

It also files an AGENT todo in kind_robots (if KR_API_TOKEN is set) asking the
Worker to create the matching PROJECT Dream — the third leg of the one-slug
rule (apps/<slug>/ + projects/<slug>/ + Dream <slug>).

Platform folders are NOT generated here; run this afterwards on a machine
with the SDKs:  cd apps/<slug> && flutter create . --org org.kindrobots \
  --project-name <slug_underscored> --platforms ios,android

Usage:
  python scripts/new_app.py <slug> --title "Nice Name" [--description "..."]
  python scripts/new_app.py <slug> --title "Nice Name" --dry-run
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KR_API = "https://kindrobots.org/api/todos"
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{1,40}$")

PUBSPEC = """name: {package}
description: "{title} — built with AppMaker on conductor."
publish_to: "none"
version: 0.1.0+1

environment:
  sdk: ^3.5.0

dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0

flutter:
  uses-material-design: true
"""

MAIN_DART = """import 'package:flutter/material.dart';

void main() => runApp(const {app_class}());

class {app_class} extends StatelessWidget {{
  const {app_class}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{title}',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('{title}')),
        body: const Center(child: Text('{title} — scaffolded by AppMaker')),
      ),
    );
  }}
}}
"""

SMOKE_TEST = """import 'package:flutter_test/flutter_test.dart';
import 'package:{package}/main.dart';

void main() {{
  testWidgets('app boots', (tester) async {{
    await tester.pumpWidget(const {app_class}());
    expect(find.text('{title}'), findsWidgets);
  }});
}}
"""

ANALYSIS_OPTIONS = """include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_single_quotes: true
    always_declare_return_types: true
"""

GITIGNORE = """.dart_tool/
build/
.flutter-plugins
.flutter-plugins-dependencies
*.iml
.idea/
*.env
*.keystore
key.properties
**/GoogleService-Info.plist
**/google-services.json
"""

APP_README = """# {title}

Scaffolded by AppMaker (`scripts/new_app.py`). See `apps/README.md` for the
workshop conventions and `projects/{slug}/roadmap.yaml` for the plan.

First checkout on a dev machine:

```sh
cd apps/{slug}
flutter create . --org org.kindrobots --project-name {package} --platforms ios,android
flutter pub get
flutter test
```
"""

ROADMAP = """project: {slug}
kind: software
notes_from_silas: '{title}: scaffolded by AppMaker. Define what this app is before building.

  '
milestones:
- id: m1
  title: Concept and spec
  weight: 30
  status: not-started
- id: m2
  title: MVP build
  weight: 50
  status: not-started
- id: m3
  title: Store readiness
  weight: 20
  status: not-started
tasks:
- id: t-001
  milestone: m1
  title: Write the app spec (what it is, who it serves, MVP screens)
  status: ready
  owner: null
  passes: 0
  stakes: reversible
  gate_human: true
  approved_by_human: false
  note: 'Produce projects/{slug}/SPEC.md. Ends at needs-human for Silas to approve before build.

    '
- id: t-002
  milestone: m2
  title: Build the MVP in apps/{slug}/
  status: waiting
  owner: null
  passes: 0
  stakes: reversible
  depends_on: t-001
  note: 'Implement the approved spec. CI (app-ci.yml) must stay green.

    '
- id: t-003
  milestone: m3
  title: 'Store readiness checklist (do NOT submit)'
  status: waiting
  owner: null
  passes: 0
  stakes: outward-facing
  gate_human: true
  approved_by_human: false
  depends_on: t-002
  note: 'Signing docs, privacy labels, release checklist. Submission itself is a separate
    needs-human action by Silas.

    '
"""

CHANGELOG = """# {slug} changelog

## {date}
- Scaffolded by AppMaker (scripts/new_app.py): apps/{slug}/, this project,
  art prompts, and registry entries.
"""

ART_ENTRY = """  - project: {slug}
    icon:
      image_path: projects/images/{slug}-icon.webp
      size: "256x256"
      status: pending
      prompt: >
        Premium app icon for {title}, {art_hint}, crisp app-icon polish with a strong
        silhouette, no text, no logo, no watermark, no collage, square composition
    card:
      image_path: projects/images/{slug}-card.webp
      size: "512x768"
      status: pending
      prompt: >
        Professional portrait card illustration for {title}, {art_hint}, featuring a
        diverse cast of humans, robots, and inventive companions where figures appear,
        cinematic key-art staging, tactile detail, no readable text, no logos,
        no watermark, portrait composition
    hero:
      image_path: projects/images/{slug}-hero.webp
      size: "1280x720"
      status: pending
      prompt: >
        Studio-quality widescreen hero illustration for {title}, {art_hint}, layered
        depth and cinematic lighting, rich but uncluttered, diverse figures where people
        appear, no readable text, no logos, no watermark, landscape composition
"""


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def plan_files(slug: str, title: str, description: str, existing_project: bool) -> dict:
    package = slug.replace("-", "_")
    app_class = "".join(part.capitalize() for part in slug.split("-")) + "App"
    from datetime import date

    fmt = dict(
        slug=slug,
        title=title,
        package=package,
        app_class=app_class,
        date=date.today().isoformat(),
        art_hint=description or f"an evocative scene expressing what {title} does",
    )
    app_dir = f"apps/{slug}"
    files = {
        f"{app_dir}/pubspec.yaml": PUBSPEC.format(**fmt),
        f"{app_dir}/analysis_options.yaml": ANALYSIS_OPTIONS,
        f"{app_dir}/.gitignore": GITIGNORE,
        f"{app_dir}/README.md": APP_README.format(**fmt),
        # Named widget_test.dart deliberately: flutter create skips existing
        # files, so this blocks its MyApp boilerplate test from appearing.
        f"{app_dir}/lib/main.dart": MAIN_DART.format(**fmt),
        f"{app_dir}/test/widget_test.dart": SMOKE_TEST.format(**fmt),
    }
    # --existing-project: the roadmap/changelog already exist and stay
    # authoritative; only the app workspace is new.
    if not existing_project:
        files[f"projects/{slug}/roadmap.yaml"] = ROADMAP.format(**fmt)
        files[f"projects/{slug}/CHANGELOG.md"] = CHANGELOG.format(**fmt)
    return files, fmt


def append_registries(slug: str, fmt: dict, dry: bool) -> None:
    art = ROOT / "projects/art-prompts.yaml"
    text = art.read_text()
    marker = "\nrequests:"
    has_art_files = any(
        (ROOT / "projects/images" / f"{slug}-{variant}.webp").exists()
        for variant in ("icon", "card", "hero")
    )
    if has_art_files:
        print(f"  ~ art-prompts.yaml: skipped ({slug} images already exist)")
    elif f"- project: {slug}\n" not in text and marker in text:
        entry = ART_ENTRY.format(**fmt)
        text = text.replace(marker, f"\n{entry}{marker}", 1)
        if not dry:
            art.write_text(text)
        print(f"  + art-prompts.yaml: {slug} icon/card/hero")

    overrides = ROOT / "project-overrides.yaml"
    if f"- slug: {slug}\n" not in overrides.read_text():
        if not dry:
            with overrides.open("a") as f:
                f.write(f"\n  - slug: {slug}\n    status: active\n    priority: normal\n    kind: software\n")
        print(f"  + project-overrides.yaml: {slug} active/normal")

    priority = ROOT / "projects/priority.yaml"
    ptext = priority.read_text()
    if f"  - {slug}\n" not in ptext:
        if not dry:
            priority.write_text(ptext.rstrip("\n") + f"\n  - {slug}\n")
        print(f"  + priority.yaml: {slug} appended")


def file_dream_todo(slug: str, title: str, dry: bool) -> None:
    token = os.environ.get("KR_API_TOKEN", "").strip()
    todo = {
        "title": f"Create kind_robots Project '{slug}' (slug parity for new app)",
        "description": (
            f"AppMaker scaffolded apps/{slug}/ and projects/{slug}/. Run "
            f"scripts/sync_projects.py (or POST /api/projects) so kind_robots has a "
            f"Project with conductorSlug '{slug}' titled '{title}'."
        ),
        "priority": "NORMAL",
        "category": "AGENT",
    }
    if dry or not token:
        reason = "dry run" if dry else "KR_API_TOKEN not set"
        print(f"  ~ Dream-sync todo NOT filed ({reason}); do it manually:\n    {todo['title']}")
        return
    req = urllib.request.Request(
        KR_API,
        data=json.dumps(todo).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            print("  + kind_robots AGENT todo filed for Dream sync")
    except (urllib.error.URLError, OSError) as e:
        print(f"  ~ could not file Dream-sync todo ({e}); do it manually", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="kebab-case app slug, e.g. recipe-box")
    parser.add_argument("--title", required=True, help="Human name, e.g. 'Recipe Box'")
    parser.add_argument("--description", default="", help="One line used in art prompts")
    parser.add_argument(
        "--existing-project",
        action="store_true",
        help="Add an app workspace to a project that already has projects/<slug>/",
    )
    parser.add_argument("--dry-run", action="store_true", help="print the plan, write nothing")
    args = parser.parse_args()

    slug = args.slug.strip().lower()
    if not SLUG_RE.match(slug):
        fail(f"slug must match {SLUG_RE.pattern}")
    if (ROOT / "apps" / slug).exists():
        fail(f"apps/{slug}/ already exists")
    project_exists = (ROOT / "projects" / slug).exists()
    if args.existing_project and not project_exists:
        fail(f"--existing-project given but projects/{slug}/ does not exist")
    if not args.existing_project and project_exists:
        fail(f"projects/{slug}/ already exists (use --existing-project to add an app to it)")

    files, fmt = plan_files(slug, args.title, args.description, args.existing_project)
    print(f"{'DRY RUN — ' if args.dry_run else ''}scaffolding '{slug}' ({args.title})")
    for rel, content in files.items():
        path = ROOT / rel
        if not args.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        print(f"  + {rel}")
    append_registries(slug, fmt, args.dry_run)
    if args.existing_project:
        print("  ~ Dream-sync todo skipped (existing project; parity assumed)")
    else:
        file_dream_todo(slug, args.title, args.dry_run)
    print(
        f"\nNext steps:\n"
        f"  1. cd apps/{slug} && flutter create . --org org.kindrobots "
        f"--project-name {fmt['package']} --platforms ios,android\n"
        f"  2. flutter test\n"
        f"  3. Commit, push, open a PR — app-ci runs automatically.\n"
        f"  4. Generate the three images from art-prompts.yaml when convenient."
    )


if __name__ == "__main__":
    main()
