#!/usr/bin/env python3
"""Watched-folder LoRA import agent for Kind Robots.

Drop a LoRA file into the import folder and this agent auto-detects it
(base model, SFW/NSFW, name, triggers, preview image), sorts it into
<LoRA root>/<Base>/<SFW|NSFW>/, and upserts it as a kind_robots Resource
with the correct `localPath` — the field the enqueue path
(`server/utils/artLoraResource.ts`) resolves to ComfyUI's `lora_name`.

It is a thin orchestrator: it reuses the proven, dependency-free tools that
already live in the kind_robots repo —
  scan_loras.py   (hash -> Civitai/CivArchive -> base model + maturity +
                   triggers + preview image; --organize move sorts on disk)
  import_catalog.py --upsert   (POST /api/resources/batch?mode=upsert)
so there is no new detection logic and no new pip dependency.

WHERE TO RUN IT: on the box that owns the LoRA files. Running it on the Linux
host (alexandria) that holds the array is preferred — file moves happen on the
local, case-sensitive filesystem, avoiding the Windows/SMB case-folding issues.
It can also run under pm2 on the Windows render box (see ecosystem.config.js);
in that case the paths are the Z: mount.

Config via env (all have sensible defaults):
  KR_BASE_URL        kind_robots base URL          (default vercel prod)
  KR_RELAY_TOKEN     kind_robots admin api-key (x-api-key)   [required]
  LORA_IMPORT_DIR    watched drop folder           (default <LORA_ROOT>/import)
  LORA_ROOT          root of the sorted LoRA tree  [required]
  CIVITAI_TOKEN      Civitai API token (optional but recommended)
  POLL_SECONDS       directory poll interval       (default 20)
  PYTHON             python executable to run the tools (default: this one)
  SCAN_SCRIPT        path to scan_loras.py         [required]
  IMPORT_SCRIPT      path to import_catalog.py     [required]
  CATALOG_OUT        scratch dir for the catalog   (default <LORA_ROOT>/.import-work)

Stdlib only. Python 3.8+.
"""

import os
import subprocess
import sys
import time

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_RELAY_TOKEN = os.environ.get("KR_RELAY_TOKEN", "").strip()
LORA_ROOT = os.environ.get("LORA_ROOT", "").strip()
LORA_IMPORT_DIR = os.environ.get(
    "LORA_IMPORT_DIR", os.path.join(LORA_ROOT, "import") if LORA_ROOT else ""
).strip()
CIVITAI_TOKEN = os.environ.get("CIVITAI_TOKEN", "").strip()
POLL_SECONDS = float(os.environ.get("POLL_SECONDS", "20"))
PYTHON = os.environ.get("PYTHON", sys.executable)
SCAN_SCRIPT = os.environ.get("SCAN_SCRIPT", "").strip()
IMPORT_SCRIPT = os.environ.get("IMPORT_SCRIPT", "").strip()
CATALOG_OUT = os.environ.get(
    "CATALOG_OUT", os.path.join(LORA_ROOT, ".import-work") if LORA_ROOT else ""
).strip()

MODEL_EXTS = (".safetensors", ".pt", ".ckpt", ".pth", ".bin")


def log(message):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[lora-import {stamp}] {message}", flush=True)


def model_files(folder):
    try:
        entries = os.listdir(folder)
    except OSError as error:
        log(f"cannot list {folder}: {error}")
        return []
    out = []
    for name in entries:
        path = os.path.join(folder, name)
        if os.path.isfile(path) and name.lower().endswith(MODEL_EXTS):
            out.append(path)
    return out


def stat_sig(path):
    try:
        st = os.stat(path)
        return (st.st_size, int(st.st_mtime))
    except OSError:
        return None


def run(cmd, timeout):
    """Run a subprocess, streaming a trimmed tail of its output to the log."""
    printable = " ".join(
        ("***" if prev in ("--civitai-token", "--api-key") else a)
        for prev, a in zip([""] + cmd, cmd)
    )
    log(f"$ {printable}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        log(f"TIMEOUT after {timeout}s")
        return False
    tail = "\n".join((result.stdout or "").strip().splitlines()[-12:])
    if tail:
        for line in tail.splitlines():
            log(f"  | {line}")
    if result.returncode != 0:
        err = "\n".join((result.stderr or "").strip().splitlines()[-6:])
        log(f"  ! exit {result.returncode}: {err}")
        return False
    return True


def process_batch():
    os.makedirs(CATALOG_OUT, exist_ok=True)
    scan_cmd = [
        PYTHON, SCAN_SCRIPT, LORA_IMPORT_DIR,
        "--organize", "move", "--dest", LORA_ROOT,
        "--out", CATALOG_OUT, "--workers", "2",
    ]
    if CIVITAI_TOKEN:
        scan_cmd += ["--civitai-token", CIVITAI_TOKEN]
    if not run(scan_cmd, timeout=1800):
        log("scan failed — leaving files in place for the next cycle")
        return
    catalog = os.path.join(CATALOG_OUT, "lora-catalog.json")
    if not os.path.isfile(catalog):
        log("no catalog produced — nothing to import")
        return
    import_cmd = [
        PYTHON, IMPORT_SCRIPT, catalog,
        "--url", KR_BASE_URL, "--api-key", KR_RELAY_TOKEN,
        "--upsert", "--batch-size", "10",
    ]
    run(import_cmd, timeout=900)


def main():
    missing = [
        n for n, v in (
            ("KR_RELAY_TOKEN", KR_RELAY_TOKEN), ("LORA_ROOT", LORA_ROOT),
            ("LORA_IMPORT_DIR", LORA_IMPORT_DIR), ("SCAN_SCRIPT", SCAN_SCRIPT),
            ("IMPORT_SCRIPT", IMPORT_SCRIPT),
        ) if not v
    ]
    if missing:
        log(f"missing required env: {', '.join(missing)} — exiting")
        sys.exit(1)
    os.makedirs(LORA_IMPORT_DIR, exist_ok=True)
    log(f"watching {LORA_IMPORT_DIR} -> {LORA_ROOT}  (poll {POLL_SECONDS}s, {KR_BASE_URL})")

    seen = {}  # path -> stat signature from the previous poll
    while True:
        try:
            files = model_files(LORA_IMPORT_DIR)
            now = {f: stat_sig(f) for f in files}
            # A file is "stable" if its size+mtime are unchanged since last poll
            # (guards against grabbing a half-copied file).
            unstable = [f for f in files if seen.get(f) != now.get(f)]
            if files and not unstable:
                log(f"{len(files)} stable file(s) ready — importing")
                process_batch()
                now = {}  # they were moved out; reset tracking
            elif unstable:
                log(f"waiting for {len(unstable)} file(s) to finish copying")
            seen = now
        except KeyboardInterrupt:
            raise
        except Exception as error:  # noqa: BLE001 - agent must survive failures
            log(f"error: {error}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
