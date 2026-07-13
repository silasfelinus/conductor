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
