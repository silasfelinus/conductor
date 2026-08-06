# AI Art Academy roadmap audit: LoRA verification handoff

Date: 2026-08-06
Task: `ai-art-academy/t-010`, lane 2 (roadmap accuracy)

## Finding

The live roadmap is internally consistent and should not enqueue another LoRA test yet.

- `t-044` correctly remains `ready`, `gate_human: true`, and `soft_gate: true`.
- ArtJobs `7622` and `7623` are already the durable verification probes for the Kontext-native and FLUX-dev LoRA paths.
- The last verified state left both jobs pending behind the relay/ComfyUI backlog. Re-submitting would spend mana and create duplicate evidence without resolving the infrastructure dependency.
- `t-045` correctly remains `waiting` on `t-044`; its A/B promotion work cannot begin until one Kontext-native and one FLUX-dev LoRA complete through the real queue.
- Milestone `m2` therefore correctly remains `in-progress`. Milestone `m6` remains `in-progress` by design because `t-010` is recurring.

## Resume rule

The next session with live queue access should inspect ArtJobs `7622` and `7623` directly before creating anything new.

- If both complete and save images without `value_not_in_list`, close `t-044` and resolve `t-045`.
- If either reaches ComfyUI and fails with `value_not_in_list`, keep `t-044` open and use the captured error as the current path-mismatch evidence.
- If both remain pending because the relay is still unhealthy, leave task state unchanged and rotate to unrelated eligible work.

## Roadmap hygiene

No task status, dependency, milestone, human gate, or curriculum-candidate status needed correction in this pass. The useful change is this concise handoff, which replaces repeated queue submissions with a single explicit evidence-reuse rule.
