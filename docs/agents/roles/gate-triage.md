# Playbook: gate-triage

Read AGENTS.md (core) first, especially "A gate must say why it needs a human, or agents take it
back". This playbook adds only what this role needs.

`select_role.py` recommended `gate-triage`: `scripts/check_gate_legitimacy.py` found `needs-human`
gates that are really agent work. Run it with `--live` to include the deploy check, then clear
**every** finding before re-running `select_role.py`.

| Finding | Clear it by |
|---|---|
| NO_GATE_BASIS | Return the task to `ready` with a note on what an agent does next. If there really is a human-only reason, set `gate_reason`. |
| APPROVED_PARKED | Execute the approved decision. If the only remaining step needs Silas's hands, set `gate_reason: physical-access` or `secrets` and name that step. |
| SHOULD_BE_WAITING | `status: waiting`, so `resolve_deps.py` releases it when the dependency lands. If the `depends_on` is wrong or backwards, fix it. |
| DEPLOY_PREREQ_MET | Re-run the step that was waiting on the deploy, now. |
| UNREVIEWED | Re-triage for real, then take one of the actions below. |

Actions for UNREVIEWED:

- The blocker cleared, or a standing directive or CONTROL.md note already answers it: return the
  task to `ready`.
- It is waiting on access, such as a DB, a shell, or Alexandria: ask whether an admin HTTPS
  endpoint plus a conductor workflow using `KR_API_TOKEN` would remove the need. If so, return it
  to `ready` scoped as building that path (the art-archive/t-040 pattern).
- It is a reversible product decision with a written recommendation, and no answer from Silas in
  7 days: adopt the recommendation under the 2026-09-30 default-recommendation rule and return the
  task to `ready`. Leave `approved_by_human` unset.
- It still genuinely needs Silas: set `gate_reason` and stamp `gate_rechecked: YYYY-MM-DD`, with a
  one-line note on what you re-checked.

Apply field changes with `scripts/set_task_field.py` (`gate_reason` and `gate_rechecked` are
allowed fields) and append notes with `close_task.py --append-note`. Land everything through one
small PR, and merge it when green. Stamping `gate_rechecked` without a real re-check is the exact
failure this role exists to stop.
