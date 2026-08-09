from __future__ import annotations
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'audit_roadmaps.py'

def load_auditor():
    spec = importlib.util.spec_from_file_location('audit_roadmaps_policy_test', SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def findings_for(tmp_path: Path, task_yaml: str):
    root = tmp_path
    projects = root / 'projects'
    (projects / 'example').mkdir(parents=True)
    (projects / 'dream-cycle').mkdir(parents=True)
    (root / 'CONTROL.md').write_text('# Test control\n')
    (root / 'project-overrides.yaml').write_text('overrides:\n  - slug: example\n    status: active\n    kind: software\n  - slug: dream-cycle\n    status: active\n    kind: software\n')
    (projects / 'priority.yaml').write_text('order:\n  - example\n  - dream-cycle\n')
    (projects / 'example' / 'roadmap.yaml').write_text('project: example\nkind: software\ngoal: Test audit policy.\nmilestones:\n  - id: m1\n    title: Test\n    weight: 100\n    status: not-started\ntasks:\n' + task_yaml)
    (projects / 'dream-cycle' / 'roadmap.yaml').write_text('project: dream-cycle\nkind: software\ngoal: Fallback.\nmilestones:\n  - id: m1\n    title: Loop\n    weight: 100\n    status: not-started\ntasks:\n  - id: t-001\n    milestone: m1\n    title: Recurring fallback\n    status: ready\n    stakes: reversible\n')
    auditor = load_auditor()
    auditor.ROOT = root
    auditor.PROJECTS = projects
    return auditor.audit()['findings']

def codes(items):
    return {item['code'] for item in items}

def test_completed_approved_gate_is_history(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: Approved history\n    status: done\n    stakes: reversible\n    gate_human: true\n    approved_by_human: true\n    note: Internal review record.\n')
    assert 'POSSIBLY_UNNECESSARY_GATE' not in codes(result)

def test_explicit_soft_gate_is_intentional(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: Parallel scope check\n    status: needs-human\n    stakes: reversible\n    soft_gate: true\n    note: "FOR SILAS: Optional feedback; development continues."\n')
    assert 'SOFT_NEEDS_HUMAN' not in codes(result)

def test_needs_human_stakes_is_hard_marker(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: Production decision\n    status: needs-human\n    stakes: needs-human\n    note: "FOR SILAS: Choose hosting policy."\n')
    assert 'SOFT_NEEDS_HUMAN' not in codes(result)

def test_open_unexplained_gate_still_warns(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: Suspicious gate\n    status: ready\n    stakes: reversible\n    gate_human: true\n    approved_by_human: false\n    note: Ordinary internal task.\n')
    assert 'POSSIBLY_UNNECESSARY_GATE' in codes(result)

def test_duplicate_task_key_is_flagged(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: Stale trailing owner\n    status: claimed\n    stakes: reversible\n    owner: reviewer\n    note: Some note text.\n    owner: worker\n')
    assert 'DUPLICATE_YAML_KEY' in codes(result)

def test_no_duplicate_keys_is_clean(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: Clean task\n    status: ready\n    stakes: reversible\n    note: Some note text.\n')
    assert 'DUPLICATE_YAML_KEY' not in codes(result)

def test_invalid_stakes_value_is_flagged(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: Priority bled into stakes\n    status: ready\n    stakes: high\n    note: Ordinary internal task.\n')
    assert 'INVALID_STAKES_VALUE' in codes(result)

def test_invalid_stakes_value_flagged_even_when_done(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: Legacy done history\n    status: done\n    stakes: needs-human\n    gate_human: true\n    approved_by_human: true\n    note: Internal review record.\n')
    assert 'INVALID_STAKES_VALUE' in codes(result)

def test_valid_stakes_values_are_clean(tmp_path):
    for index, value in enumerate(('reversible', 'outward-facing', 'irreversible')):
        result = findings_for(tmp_path / str(index), f'  - id: t-001\n    milestone: m1\n    title: Valid stakes\n    status: ready\n    stakes: {value}\n    note: Ordinary internal task.\n')
        assert 'INVALID_STAKES_VALUE' not in codes(result)

def test_missing_stakes_is_not_an_invalid_value(tmp_path):
    result = findings_for(tmp_path, '  - id: t-001\n    milestone: m1\n    title: No stakes yet\n    status: ready\n    note: Ordinary internal task.\n')
    assert 'INVALID_STAKES_VALUE' not in codes(result)
    assert 'OPEN_TASK_MISSING_STAKES' in codes(result)

def test_continuous_improvement_note_drift_is_flagged(tmp_path):
    result = findings_for(
        tmp_path,
        '  - id: t-001\n'
        '    milestone: m1\n'
        '    title: Recurring improvement pass\n'
        '    status: ready\n'
        '    stakes: reversible\n'
        "    updated: '2026-07-28T01:53:00Z'\n"
        '    note: |-\n'
        '      RAN 2026-07-28T01:53:00Z: option (a), front-end polish. Next preferred lane: roadmap accuracy (lane 2).\n'
        '    continuous_improvement:\n'
        '      last_lane: 4\n'
        '      next_lane: 1\n'
        "      last_run: '2026-07-28T01:30:00Z'\n"
        '      last_pr: some-pr-reference\n',
    )
    assert 'CONTINUOUS_IMPROVEMENT_NOTE_DRIFT' in codes(result)

def test_continuous_improvement_in_sync_is_clean(tmp_path):
    result = findings_for(
        tmp_path,
        '  - id: t-001\n'
        '    milestone: m1\n'
        '    title: Recurring improvement pass\n'
        '    status: ready\n'
        '    stakes: reversible\n'
        "    updated: '2026-07-28T01:30:00Z'\n"
        '    note: |-\n'
        '      RAN 2026-07-28T01:30:00Z: option (d), curriculum depth. Next preferred lane: front-end polish (lane 1).\n'
        '    continuous_improvement:\n'
        '      last_lane: 4\n'
        '      next_lane: 1\n'
        "      last_run: '2026-07-28T01:30:00Z'\n"
        '      last_pr: some-pr-reference\n',
    )
    assert 'CONTINUOUS_IMPROVEMENT_NOTE_DRIFT' not in codes(result)
