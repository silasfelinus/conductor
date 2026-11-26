# CLAUDE.md

Use [AGENTS.md](AGENTS.md) as the shared agent contract. Read it once; do not duplicate it here.

For a direct task, proceed with that task and its role-specific context. Otherwise use the SessionStart hook's current signals and `scripts/select_role.py`; load only the named playbook. Use `scripts/session_sweep.py --max-lines 3` when diagnosing maintenance signals, not as a mandatory full sweep before every assignment. Scheduled deterministic checks own routine detection; inspect failures and stale results as needed.

Daily Dream, Dead Air, five daily upgrades and other recurring creative commitments retain their current CONTROL.md requirements. Load [daily rituals](docs/agents/daily-rituals.md) only for that assignment. Never revive stopped rituals.

Open PRs, verify completed green checks, merge safe work and reconcile the actual task state per AGENTS.md. Genuine gates remain gated. Do not ask Silas to select routine work. Report the result concisely.

Full prior startup/closeout details are preserved in [the reference](docs/agents/claude-reference-2026-11-26.md); read only the relevant section if needed.
