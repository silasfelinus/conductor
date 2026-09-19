#!/usr/bin/env python3
"""Watched-folder model import agent for Kind Robots.

Two filesystem inboxes are supported:

* <LORA_ROOT>/import: scan_loras.py detects/enriches LoRAs, sorts them into
  <Base>/<SFW|NSFW>/, then import_catalog.py upserts canonical Resources.
* <MODEL_ROOT>/checkpoints/import: scan_models.py classifies checkpoints and
  related file-backed components, moves them into ComfyUI's canonical model
  directories, then imports the resulting Resources.

Queued Discover downloads are deliberately NOT claimed here. kr-download is
the single DownloadRequest consumer; keeping network downloads and watched
filesystem imports in separate workers prevents the two agents racing for the
same queue row.

The scanner/importer tools are vendored beside this file under lora-catalog/
so executable code stays on local disk even when MODEL_ROOT is an SMB mount.

Config:
  KR_BASE_URL              Kind Robots base URL (default https://kindrobots.org)
  KR_RELAY_TOKEN           API key used by import_catalog.py [required]
  MODEL_ROOT               Comfy model root (derived from LORA_ROOT when unset)
  LORA_ROOT                sorted LoRA root [required]
  LORA_IMPORT_DIR          LoRA inbox (default <LORA_ROOT>/import)
  CHECKPOINT_IMPORT_DIR    generic model inbox
                           (default <MODEL_ROOT>/checkpoints/import)
  CIVITAI_TOKEN            optional Civitai token for metadata enrichment
  LORA_POLL_SECONDS        poll interval for both inboxes (default 20)
  SCAN_SCRIPT              scan_loras.py override
  MODEL_SCAN_SCRIPT        scan_models.py override
  IMPORT_SCRIPT            import_catalog.py override
  CATALOG_OUT              LoRA scratch output
  MODEL_CATALOG_OUT        generic-model scratch output
  CACHE_DB                 LoRA scanner sqlite cache (prefer local disk)
  MODEL_CACHE_DB           generic scanner sqlite cache (prefer local disk)
"""

import os
import subprocess
import sys
import time
from datetime import datetime

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_RELAY_TOKEN = os.environ.get("KR_RELAY_TOKEN", "").strip()
LORA_ROOT = os.environ.get("LORA_ROOT", "").strip()
MODEL_ROOT = os.environ.get(
    "MODEL_ROOT",
    os.environ.get("KR_MODEL_ROOT", "").strip()
    or (os.path.dirname(LORA_ROOT.rstrip("/\\")) if LORA_ROOT else ""),
).strip()
LORA_IMPORT_DIR = os.environ.get(
    "LORA_IMPORT_DIR", os.path.join(LORA_ROOT, "import") if LORA_ROOT else ""
).strip()
CHECKPOINT_IMPORT_DIR = os.environ.get(
    "CHECKPOINT_IMPORT_DIR",
    os.path.join(MODEL_ROOT, "checkpoints", "import") if MODEL_ROOT else "",
).strip()
CIVITAI_TOKEN = os.environ.get("CIVITAI_TOKEN", "").strip()
LORA_POLL_SECONDS = float(os.environ.get("LORA_POLL_SECONDS", "20"))
PYTHON = os.environ.get("PYTHON", sys.executable)

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_SCAN = os.path.join(_HERE, "lora-catalog", "scan_loras.py")
_DEFAULT_MODEL_SCAN = os.path.join(_HERE, "lora-catalog", "scan_models.py")
_DEFAULT_IMPORT = os.path.join(_HERE, "lora-catalog", "import_catalog.py")
SCAN_SCRIPT = (os.environ.get("SCAN_SCRIPT") or _DEFAULT_SCAN).strip()
MODEL_SCAN_SCRIPT = (
    os.environ.get("MODEL_SCAN_SCRIPT") or _DEFAULT_MODEL_SCAN
).strip()
IMPORT_SCRIPT = (os.environ.get("IMPORT_SCRIPT") or _DEFAULT_IMPORT).strip()

CATALOG_OUT = os.environ.get(
    "CATALOG_OUT", os.path.join(LORA_ROOT, ".import-work") if LORA_ROOT else ""
).strip()
MODEL_CATALOG_OUT = os.environ.get(
    "MODEL_CATALOG_OUT",
    os.path.join(MODEL_ROOT, ".model-import-work") if MODEL_ROOT else "",
).strip()
CACHE_DB = os.environ.get("CACHE_DB", "").strip()
MODEL_CACHE_DB = os.environ.get("MODEL_CACHE_DB", "").strip()

# Keep this aligned with the scanners. GGUF matters for modern diffusion-model
# / checkpoint imports and was previously invisible to the watcher.
MODEL_EXTS = (".safetensors", ".pt", ".ckpt", ".pth", ".bin", ".gguf")


def _use_utf8_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


_use_utf8_stdout()


def human_time(moment):
    hour = (moment.hour % 12) or 12
    meridiem = "AM" if moment.hour < 12 else "PM"
    return (
        f"{moment:%b} {moment.day} "
        f"{hour}:{moment.minute:02d}:{moment.second:02d}{meridiem}"
    )


def log(message):
    line = f"{human_time(datetime.now().astimezone())} model-import {message}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "ascii"
        print(
            line.encode(encoding, "backslashreplace").decode(encoding, "replace"),
            flush=True,
        )
    except OSError:
        pass


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
    """Run a subprocess, logging a short tail while redacting credentials."""
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


def import_catalog(catalog):
    if not os.path.isfile(catalog):
        log(f"no catalog produced at {catalog} — nothing to import")
        return False
    cmd = [
        PYTHON,
        IMPORT_SCRIPT,
        catalog,
        "--url",
        KR_BASE_URL,
        "--api-key",
        KR_RELAY_TOKEN,
        "--upsert",
        "--batch-size",
        "10",
    ]
    return run(cmd, timeout=900)


def process_lora_batch():
    os.makedirs(CATALOG_OUT, exist_ok=True)
    cmd = [
        PYTHON,
        SCAN_SCRIPT,
        LORA_IMPORT_DIR,
        "--organize",
        "move",
        "--dest",
        LORA_ROOT,
        "--out",
        CATALOG_OUT,
        "--workers",
        "2",
    ]
    if CIVITAI_TOKEN:
        cmd += ["--civitai-token", CIVITAI_TOKEN]
    if CACHE_DB:
        cmd += ["--cache", CACHE_DB]
    if not run(cmd, timeout=1800):
        log("LoRA scan failed — leaving files for the next cycle")
        return False
    return import_catalog(os.path.join(CATALOG_OUT, "lora-catalog.json"))


def process_model_batch():
    os.makedirs(MODEL_CATALOG_OUT, exist_ok=True)
    cmd = [
        PYTHON,
        MODEL_SCAN_SCRIPT,
        CHECKPOINT_IMPORT_DIR,
        "--organize",
        "move",
        "--dest",
        MODEL_ROOT,
        "--out",
        MODEL_CATALOG_OUT,
        "--workers",
        "2",
        "--hash-workers",
        "2",
    ]
    if CIVITAI_TOKEN:
        cmd += ["--civitai-token", CIVITAI_TOKEN]
    if MODEL_CACHE_DB:
        cmd += ["--cache", MODEL_CACHE_DB]
    if not run(cmd, timeout=3600):
        log("checkpoint/model scan failed — leaving files for the next cycle")
        return False
    return import_catalog(os.path.join(MODEL_CATALOG_OUT, "models-catalog.json"))


def missing_config():
    """Return required configuration missing from the embedded watcher."""
    return [
        name
        for name, value in (
            ("KR_RELAY_TOKEN", KR_RELAY_TOKEN),
            ("LORA_ROOT", LORA_ROOT),
            ("LORA_IMPORT_DIR", LORA_IMPORT_DIR),
            ("MODEL_ROOT", MODEL_ROOT),
            ("CHECKPOINT_IMPORT_DIR", CHECKPOINT_IMPORT_DIR),
        )
        if not value
    ]


def _poll_inbox(label, folder, seen, processor):
    """Poll one inbox; return the signatures to compare on the next cycle."""
    os.makedirs(folder, exist_ok=True)
    files = model_files(folder)
    now = {path: stat_sig(path) for path in files}
    unstable = [path for path in files if seen.get(path) != now.get(path)]
    if files and not unstable:
        log(f"{label}: {len(files)} stable file(s) ready — importing")
        if processor():
            return {}
    elif unstable:
        log(f"{label}: waiting for {len(unstable)} file(s) to finish copying")
    return now


def watch_loop():
    """Watch LoRA and checkpoint/model inboxes forever on one daemon thread."""
    log(
        f"watching LoRAs {LORA_IMPORT_DIR} -> {LORA_ROOT}; "
        f"models {CHECKPOINT_IMPORT_DIR} -> {MODEL_ROOT} "
        f"(poll {LORA_POLL_SECONDS}s, {KR_BASE_URL})"
    )
    seen = {"lora": {}, "model": {}}
    while True:
        try:
            # Both directories may live on an SMB share that disappears during
            # NAS reboots. mkdir/list stay inside the guarded loop so a transient
            # outage cannot permanently kill the embedded watcher thread.
            seen["lora"] = _poll_inbox(
                "LoRA", LORA_IMPORT_DIR, seen["lora"], process_lora_batch
            )
            seen["model"] = _poll_inbox(
                "checkpoint/model",
                CHECKPOINT_IMPORT_DIR,
                seen["model"],
                process_model_batch,
            )
        except KeyboardInterrupt:
            raise
        except Exception as error:  # noqa: BLE001 - watcher must survive SMB/API failures
            log(f"error: {error}")
        time.sleep(LORA_POLL_SECONDS)


def main():
    missing = missing_config()
    if missing:
        log(f"missing required env: {', '.join(missing)} — exiting")
        sys.exit(1)
    watch_loop()


if __name__ == "__main__":
    main()
