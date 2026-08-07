from pathlib import Path
import re

# The priority queue should represent selectable work, not retain inactive historical slugs.
priority = Path('projects/priority.yaml')
priority.write_text('''# Which project leads when multiple have ready tasks. Top of list wins.
# Finite active projects always outrank continuous projects. Paused, finished, and
# retired projects are historical records and do not belong in the selectable queue.
# Continuous programs are fallback work; dream-cycle stays last by design.
order:
  - interface-vision
  - ai-art-academy
  - coloring-book
  - humboldt-scoop-cms
  - digital-storefront
  - mermaids-of-venice
  - kind-robots
  - kindrobots-unraid
  - model-builder
  - lora-ingestion
  - conductor
  - taskmaster
  - storybook
  - davinci
  - mural-design
  - coat-dance
  - alexa-integration
  - conductor-app
  - appmaker
  - media-watchlist
  - brainstorm
  - wishmaster
  - ruler-hooked
  - music-mentor
  - animation-manager
  - dream-cycle
''', encoding='utf-8')

# Keep the finite priority band parseable as a band; continuous semantics get their own paragraph.
control = Path('CONTROL.md')
text = control.read_text(encoding='utf-8')
pattern = re.compile(r'\*\*Priority order this week:\*\*.*?(?=\n\n)', re.S)
replacement = '''**Priority order this week:** interface-vision → ai-art-academy → coloring-book →
humboldt-scoop-cms → digital-storefront → mermaids-of-venice → kind-robots →
kindrobots-unraid.

**Continuous fallback order:** animation-manager, then dream-cycle. Finite `active` work
always outranks `continuous` programs; dream-cycle remains the final idle fallback.'''
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'CONTROL priority band replacement expected 1 match, got {count}')
control.write_text(text, encoding='utf-8')

# Teach the structural audit that continuous is workable but not finite-active.
audit = Path('scripts/audit_roadmaps.py')
text = audit.read_text(encoding='utf-8')
text = text.replace('ACTIVE_STATES = {"active"}\n', 'ACTIVE_STATES = {"active"}\nWORKABLE_STATES = {"active", "continuous"}\n', 1)
text = text.replace(
    '    active = {slug for slug, entry in overrides.items() if entry.get("status") in ACTIVE_STATES}\n',
    '    active = {slug for slug, entry in overrides.items() if entry.get("status") in ACTIVE_STATES}\n'
    '    continuous = {slug for slug, entry in overrides.items() if entry.get("status") == "continuous"}\n'
    '    workable = active | continuous\n',
    1,
)
text = text.replace('    for slug in sorted(active - set(priority)):\n', '    for slug in sorted(workable - set(priority)):\n', 1)
text = text.replace(
    '        if slug not in priority and override_status == "active":\n            findings.append(issue("error", "ACTIVE_ROADMAP_MISSING_PRIORITY", slug, "Active roadmap is not selectable because it is absent from priority.yaml."))\n',
    '        if slug not in priority and override_status in WORKABLE_STATES:\n'
    '            findings.append(issue("error", "WORKABLE_ROADMAP_MISSING_PRIORITY", slug, "Active/continuous roadmap is not selectable because it is absent from priority.yaml."))\n',
    1,
)
text = text.replace(
    '        if override_status != "active" and counts.get("ready", 0):\n',
    '        if override_status not in WORKABLE_STATES and counts.get("ready", 0):\n',
    1,
)
text = text.replace(
    '            "active_projects": len(active),\n',
    '            "active_projects": len(active),\n            "continuous_projects": len(continuous),\n',
    1,
)
text = text.replace(
    '        f"- **{summary[\'roadmaps\']}** roadmaps, **{summary[\'active_projects\']}** active projects, **{summary[\'tasks\']}** tasks",\n',
    '        f"- **{summary[\'roadmaps\']}** roadmaps, **{summary[\'active_projects\']}** active + **{summary[\'continuous_projects\']}** continuous projects, **{summary[\'tasks\']}** tasks",\n',
    1,
)
audit.write_text(text, encoding='utf-8')

# Existing full pytest CI now executes the repository-level lifecycle validator even without
# permission to edit .github/workflows/ci.yml.
Path('tests/test_current_project_lifecycle.py').write_text('''from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_current_repository_roadmaps_pass_lifecycle_validation() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_roadmaps.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
''', encoding='utf-8')
