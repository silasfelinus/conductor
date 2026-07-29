# Vendored LoRA catalog tools

`scan_loras.py` and `import_catalog.py` are **vendored copies** of the tools that
live canonically in the **kind_robots** repo at `scripts/lora-catalog/`.

They are copied here so the home render box (which runs `kr-relay` and the
embedded LoRA import watcher, see `../lora_import_agent.py`) executes them from
**local disk in this conductor checkout** — never over the `Z:` network mount to
alexandria. Only the LoRA *files* are remote (`LORA_ROOT=Z:/ai/models/Lora`);
the code that moves and catalogs them runs locally.

Both scripts are pure Python stdlib (no pip deps, no kind_robots imports), so a
straight file copy is all that's needed.

## Re-sync when the kind_robots tools change

These are copies, so they can drift. Whenever `scripts/lora-catalog/scan_loras.py`
or `import_catalog.py` change in kind_robots (e.g. new catalog fields), refresh
them here:

```
cp <kind_robots>/scripts/lora-catalog/scan_loras.py     ops/home-server/lora-catalog/
cp <kind_robots>/scripts/lora-catalog/import_catalog.py ops/home-server/lora-catalog/
```

Last synced from kind_robots branch `claude/lora-organization-catalog-coyhav`
(includes the `civitaiModelId`/`civitaiModelVersionId` emission from t-004).
The batch import endpoint ignores unknown fields, so a newer scanner is safe to
run against an older API — the extra ids are simply dropped until the API + DB
support them.
