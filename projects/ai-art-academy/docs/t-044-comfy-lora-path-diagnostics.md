# t-044 ComfyUI LoRA path diagnostics

The remaining blocker is one authoritative data capture from the home relay. Four guessed path conventions have already failed; adding more guesses would only create a more elaborate wrong answer.

## Capture two JSON files

From a Tailscale-connected machine that can reach the configured ComfyUI server, save the full `/object_info` response as `object-info.json`.

Save the Kind Robots `/api/resources` response as `resources.json`. The comparator accepts either the raw array or the normal `{ "data": [...] }` response shape.

Do not commit either capture. They may reveal private model inventory and local folder names.

## Run the comparison

```bash
python scripts/compare_comfy_lora_paths.py \
  --object-info object-info.json \
  --resources resources.json \
  --output lora-path-report.json
```

The report classifies each Resource `localPath` as:

- `normalized-exact`: same path after slash and case normalization;
- `unique-basename`: folder prefixes differ, but exactly one ComfyUI entry has that filename;
- `ambiguous`: multiple ComfyUI entries share the filename, so the tool refuses to guess;
- `missing`: no matching ComfyUI entry exists.

## Apply the result

If the catalog mostly produces unique mappings, update the affected Resource records to the exact `comfyPath` strings. If stable directory-prefix rules emerge, implement one shared resolver used by both `buildKontextWorkflow` and `simpleCheckpointWorkflow.ts`, with tests covering slash normalization, unique basename matching, ambiguity refusal, and missing files.

Then rerun one Kontext-native and one FLUX-dev LoRA through the real queue before closing t-044. Do not mark the task done from a clean static comparison alone: ComfyUI must accept the workflow and produce a saved image.

## Safety boundary

This task does not authorize exposing `/object_info` publicly, committing private inventory, editing production database rows blindly, deploying, or changing the relay configuration. The comparator is deliberately offline and default-deny for ambiguous matches.
