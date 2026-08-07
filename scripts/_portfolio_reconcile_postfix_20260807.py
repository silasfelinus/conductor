from pathlib import Path

for rel in ('scripts/build_status.py', 'scripts/validate_roadmaps.py'):
    path = Path(rel)
    text = path.read_text(encoding='utf-8')
    if rel.endswith('build_status.py'):
        old = 'from project_lifecycle import PROJECT_LIFECYCLE_STATUSES, lifecycle_status, load_project_overrides\n'
        new = '''try:\n    from project_lifecycle import PROJECT_LIFECYCLE_STATUSES, lifecycle_status, load_project_overrides\nexcept ModuleNotFoundError:  # imported as scripts.build_status in pytest\n    from scripts.project_lifecycle import PROJECT_LIFECYCLE_STATUSES, lifecycle_status, load_project_overrides\n'''
    else:
        old = 'from scripts.project_lifecycle import PROJECT_LIFECYCLE_STATUSES, load_project_overrides\n'
        new = '''try:\n    from project_lifecycle import PROJECT_LIFECYCLE_STATUSES, load_project_overrides\nexcept ModuleNotFoundError:  # imported as scripts.validate_roadmaps in pytest\n    from scripts.project_lifecycle import PROJECT_LIFECYCLE_STATUSES, load_project_overrides\n'''
    if old not in text and new not in text:
        raise SystemExit(f'{rel}: expected generated lifecycle import not found')
    if old in text:
        path.write_text(text.replace(old, new, 1), encoding='utf-8')
