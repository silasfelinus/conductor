# Vendored LoRA catalog tools

`scan_loras.py`, `scan_models.py`, and `import_catalog.py` are **vendored copies** of the tools that
live canonically in the **kind_robots** repo at `scripts/lora-catalog/`.

They are copied here so the home render box (which runs `kr-relay` and the
embedded model import watcher, see `../lora_import_agent.py`) executes them from
**local disk in this conductor checkout** — never over the `Z:` network mount to
alexandria. Only the model *files* are remote (beneath `KR_MODEL_ROOT`); the
code that moves and catalogs them runs locally.

Both scripts are pure Python stdlib (no pip deps, no kind_robots imports), so a
straight file copy is all that's needed.

## Re-sync when the kind_robots tools change

These are copies, so they can drift. Whenever `scripts/lora-catalog/scan_loras.py`,
`scan_models.py`, or `import_catalog.py` change in kind_robots (e.g. new catalog
fields), refresh them here:

```
cp <kind_robots>/scripts/lora-catalog/scan_loras.py      ops/home-server/lora-catalog/
cp <kind_robots>/scripts/lora-catalog/scan_models.py      ops/home-server/lora-catalog/
cp <kind_robots>/scripts/lora-catalog/import_catalog.py   ops/home-server/lora-catalog/
```

Last synced from kind_robots branch `claude/lora-organization-catalog-coyhav`
(includes the `civitaiModelId`/`civitaiModelVersionId` emission from t-004).
The batch import endpoint ignores unknown fields, so a newer scanner is safe to
run against an older API — the extra ids are simply dropped until the API + DB
support them.

Re-synced 2026-07-29 (`scan_loras.py` only) for `.gguf` recognition — GGUF
checkpoints/unets were being silently dropped at the directory-walk step
because `LORA_EXTENSIONS` didn't include `.gguf`, so they never reached
hashing or the `/api/resources/batch` POST regardless of resourceType or
folder placement. See kind_robots PR #1168.


Re-synced 2026-09-19 for lora-ingestion/t-009. Added `scan_models.py` so the
home watcher can process `checkpoints/import` with the same catalog/sort/upsert
pipeline as `Lora/import`. This copy includes Resource emission for checkpoints,
diffusion models, text encoders, VAEs, ControlNets, hypernetworks, embeddings,
pixel upscalers, and latent upscalers.
