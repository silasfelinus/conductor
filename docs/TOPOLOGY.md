# TOPOLOGY.md — Dependency Graphs and Pipeline Patterns

This document explains how task dependencies work in Conductor and how to read the topology output.

## Task lifecycle

```
ready → claimed → review → done
         ↓              ↓
      blocked        needs-human
waiting (unmet deps)
```

- **ready** — available to be claimed by the Worker
- **waiting** — blocked on a dependency; resolver flips it to `ready` when deps are met
- **claimed** — Worker has started; branch opened
- **review** — PR open; Reviewer is evaluating
- **done** — merged and complete
- **blocked** — 3 passes exhausted without success; needs Silas
- **needs-human** — output requires Silas approval before continuing (content/proposal, or `gate_human: true`)

## Declaring dependencies

In `roadmap.yaml`:

```yaml
tasks:
  - id: t-001
    status: done
    ...

  - id: t-002
    depends_on: t-001      # single dependency
    status: waiting        # resolver will flip to ready when t-001 is done
    ...

  - id: t-003
    depends_on:            # multiple dependencies
      - t-001
      - t-002
    status: waiting
    ...
```

A task with `gate_human: true` on its upstream dependency stays `waiting` until:
1. The upstream task is `status: done`
2. AND `approved_by_human: true` is set on the upstream task by Silas

## Human gates

```yaml
tasks:
  - id: t-005
    gate_human: true
    status: needs-human    # Worker stops here; Silas must approve
    ...

  - id: t-006
    depends_on: t-005
    status: waiting        # won't unlock until t-005 is done AND approved_by_human: true
```

Silas approves by editing the roadmap:
```yaml
  - id: t-005
    status: done
    approved_by_human: true
```

Then `python scripts/resolve_deps.py` flips t-006 to `ready`.

## Running the topology viewer

```bash
# All projects, text view
python scripts/topology.py

# Single project
python scripts/topology.py --project humboldt-scoop

# Graphviz DOT (pipe to dot or paste into graphviz.online)
python scripts/topology.py --dot > conductor.dot
dot -Tsvg conductor.dot -o conductor.svg
```

## Reading the text output

```
═══════════════════════════════════
  humboldt-scoop  (software)
═══════════════════════════════════
  → t-001        ready          Confirm the loop (smoke test)
  → t-002        ready          Audit the imported site
              deps: t-001
```

Symbols: `✓` done · `→` ready · `⏳` waiting · `⚙` claimed · `👁` review · `✗` blocked · `👤` needs-human
