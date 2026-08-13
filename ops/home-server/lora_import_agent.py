#!/usr/bin/env python3
"""Watched-folder LoRA import agent for Kind Robots.

Drop a LoRA file into the import folder and this agent auto-detects it
(base model, SFW/NSFW, name, triggers, preview image), sorts it into
<LoRA root>/<Base>/<SFW|NSFW>/, and upserts it as a kind_robots Resource
with the correct `localPath` — the field the enqueue path
(`server/utils/artLoraResource.ts`) resolves to ComfyUI's `lora_name`.

It also drains the front-end download queue (Phase 3): each cycle it claims one
PENDING DownloadRequest from kind_robots, fetches the file (Civitai by-version
URL with CIVITAI_TOKEN, or a direct URL) into the same import folder, and marks
it complete — so a "Download" click in the Discover browser flows through the
exact same detect/sort/upsert pipeline as a manual drop.

It is a thin orchestrator: it reuses the proven, dependency-free tools that
already live in the kind_robots repo —
  scan_loras.py   (hash -> Civitai/CivArchive -> base model + maturity +
                   triggers + preview image; --organize move sorts on disk)
  import_catalog.py --upsert   (POST /api/resources/batch?mode=upsert)
so there is no new detection logic and no new pip dependency.

WHERE TO RUN IT: on the box that owns (or mounts) the LoRA files. The permanent
home is the pm2 render box that already runs kr-relay — this watcher is embedded
there as a background thread inside the kr-relay process (see
relay_media_agent.py + ecosystem.config.js), so it's one process, one token, one
log. The array host (alexandria) is a locked-down NAS and does not run ad-hoc
daemons. Because the tree is reached over SMB (Z:) and SMB is case-insensitive,
new base-model folders always resolve to the existing canonical casing — so once
the tree has single-case folders (already merged via case_merge.py), running the
moves from Windows is safe and actually prevents fresh case-duplicate folders.

This module also runs standalone (`python lora_import_agent.py`) for debugging or
one-off use; the loop is the same either way.

Config via env (all have sensible defaults):
  KR_BASE_URL        kind_robots base URL          (default vercel prod)
  KR_RELAY_TOKEN     kind_robots admin api-key (x-api-key)   [required]
  LORA_IMPORT_DIR    watched drop folder           (default <LORA_ROOT>/import)
  LORA_ROOT          root of the sorted LoRA tree  [required]
  CIVITAI_TOKEN      Civitai API token (optional but recommended)
  LORA_POLL_SECONDS  directory poll interval       (default 20)
  PYTHON             python executable to run the tools (default: this one)
  SCAN_SCRIPT        path to scan_loras.py    (default: vendored ./lora-catalog/)
  IMPORT_SCRIPT      path to import_catalog.py(default: vendored ./lora-catalog/)
  CATALOG_OUT        scratch dir for the catalog   (default <LORA_ROOT>/.import-work)
  CACHE_DB           scanner sqlite cache path     (default: scanner picks <out>/;
                     set to LOCAL disk when the tree is an SMB mount)

Embedding: import this module and, after checking missing_config() is empty,
run watch_loop() on a daemon thread. Stdlib only. Python 3.8+.
"""

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

AGENT_ID = os.environ.get("LORA_AGENT_ID", "").strip() or f"{socket.gethostname()}-lora"
KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_RELAY_TOKEN = os.environ.get("KR_RELAY_TOKEN", "").strip()
LORA_ROOT = os.environ.get("LORA_ROOT", "").strip()
LORA_IMPORT_DIR = os.environ.get(
    "LORA_IMPORT_DIR", os.path.join(LORA_ROOT, "import") if LORA_ROOT else ""
).strip()
CIVITAI_TOKEN = os.environ.get("CIVITAI_TOKEN", "").strip()
# Own poll var (not POLL_SECONDS): when embedded as a thread inside kr-relay the
# relay owns POLL_SECONDS for the render loop; the watcher paces itself.
LORA_POLL_SECONDS = float(os.environ.get("LORA_POLL_SECONDS", "20"))
PYTHON = os.environ.get("PYTHON", sys.executable)
# The scan/import tools are vendored LOCALLY next to this agent (lora-catalog/)
# so they run from the conductor checkout on the render box, never over the Z:
# network mount. Only the LoRA files are remote; the code is local. Override
# only to point at a different local checkout.
_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_SCAN = os.path.join(_HERE, "lora-catalog", "scan_loras.py")
_DEFAULT_IMPORT = os.path.join(_HERE, "lora-catalog", "import_catalog.py")
SCAN_SCRIPT = (os.environ.get("SCAN_SCRIPT") or _DEFAULT_SCAN).strip()
IMPORT_SCRIPT = (os.environ.get("IMPORT_SCRIPT") or _DEFAULT_IMPORT).strip()
CATALOG_OUT = os.environ.get(
    "CATALOG_OUT", os.path.join(LORA_ROOT, ".import-work") if LORA_ROOT else ""
).strip()
# Keep the scanner's sqlite hash cache on LOCAL disk. When the LoRA tree is an
# SMB/network mount (the pm2 Windows box reaching alexandria over Z:), a cache
# on the share invites sqlite locking failures; a local path avoids them. Empty
# = let scan_loras.py default it to <out>/.lora-cache.sqlite.
CACHE_DB = os.environ.get("CACHE_DB", "").strip()

MODEL_EXTS = (".safetensors", ".pt", ".ckpt", ".pth", ".bin")


def _use_utf8_stdout():
    """See relay_agent._use_utf8_stdout -- same cp1252 trap, same fix.

    Duplicated rather than imported because this module runs standalone too
    (`python lora_import_agent.py`), where relay_agent is not loaded.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


_use_utf8_stdout()


def human_time(moment):
    """`Aug 13 3:47PM` -- the scannable half of the timestamp.

    Built by hand rather than with strftime because the no-pad directives that
    would express it are platform-specific: %-I/%-d are glibc, Windows wants
    %#I/%#d, and this relay runs on Windows. %b is portable, the rest is
    arithmetic.
    """
    hour = (moment.hour % 12) or 12
    meridiem = "AM" if moment.hour < 12 else "PM"
    return (
        f"{moment:%b} {moment.day} "
        f"{hour}:{moment.minute:02d}:{moment.second:02d}{meridiem}"
    )


def log(message):
    # Same shape as relay_agent.log -- these two streams interleave in one pm2
    # log, so they have to line up with each other.
    line = f"{human_time(datetime.now().astimezone())} lora-import {message}"
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


# ---------------------------------------------------------------------------
# Download queue (Phase 3): claim a LoRA download request from kind_robots,
# fetch the file into the import folder, and let the watch loop catalog it.
# ---------------------------------------------------------------------------

def http_json(method, path, body=None):
    """Call a kind_robots JSON endpoint with the admin api-key. Returns the
    parsed 'data' object (or {}); raises on transport/HTTP error."""
    url = KR_BASE_URL + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("x-api-key", KR_RELAY_TOKEN)
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        parsed = json.loads(resp.read().decode("utf-8"))
    return parsed.get("data") or {}


def resolve_download_url(request):
    url = str(request.get("downloadUrl") or "").strip()
    version_id = request.get("civitaiModelVersionId")
    if not url and version_id:
        url = f"https://civitai.com/api/download/models/{version_id}"
    if not url:
        return None
    # Attach the Civitai token as a query param for Civitai download links.
    if CIVITAI_TOKEN and "civitai.com" in url and "token=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}token={CIVITAI_TOKEN}"
    return url


def _redact_url(url):
    return re.sub(r"token=[^&]+", "token=***", url or "")


def safe_filename(name):
    name = os.path.basename(str(name or "")).strip()
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    if not name or name in (".", ".."):
        return ""
    if not name.lower().endswith(MODEL_EXTS):
        name += ".safetensors"
    return name


def filename_from_headers(headers):
    disposition = headers.get("Content-Disposition", "") or ""
    match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', disposition)
    return safe_filename(match.group(1)) if match else ""


def download_request_file(request):
    """Fetch the request's file into LORA_IMPORT_DIR (atomically via a .part
    temp) so the watch loop picks it up once stable. Returns the final path."""
    url = resolve_download_url(request)
    if not url:
        raise RuntimeError("no download url or civitaiModelVersionId")
    log(f"  downloading {_redact_url(url)}")
    req = urllib.request.Request(url, headers={"User-Agent": "kr-lora-import"})
    with urllib.request.urlopen(req, timeout=1800) as resp:
        name = (
            safe_filename(request.get("fileName"))
            or filename_from_headers(resp.headers)
            or safe_filename(f"civitai_{request.get('civitaiModelVersionId') or 'download'}")
        )
        dest = os.path.join(LORA_IMPORT_DIR, name)
        tmp = dest + ".part"
        with open(tmp, "wb") as handle:
            shutil.copyfileobj(resp, handle, length=1024 * 1024)
    os.replace(tmp, dest)
    return dest


def claim_and_download():
    """Claim one pending download and fetch it. The subsequent watch cycle
    catalogs + upserts it as a Resource. Best-effort: any failure is reported
    back so the request can be retried or marked FAILED."""
    try:
        data = http_json("POST", "/api/lora/download/claim", {"agentId": AGENT_ID})
    except (urllib.error.URLError, OSError, ValueError) as error:
        log(f"claim failed: {error}")
        return
    request = data.get("request")
    if not request:
        return
    request_id = request.get("id")
    label = (
        request.get("label")
        or request.get("fileName")
        or f"version {request.get('civitaiModelVersionId')}"
    )
    log(f"claimed download #{request_id}: {label}")
    try:
        dest = download_request_file(request)
        log(f"  saved {os.path.basename(dest)} -> import will catalog it")
        http_json("POST", f"/api/lora/download/{request_id}/complete", {"success": True})
    except Exception as error:  # noqa: BLE001 - report and move on
        log(f"download #{request_id} failed: {error}")
        try:
            http_json(
                "POST",
                f"/api/lora/download/{request_id}/complete",
                {"success": False, "error": str(error)[:500]},
            )
        except Exception as report_error:  # noqa: BLE001
            log(f"  could not report failure: {report_error}")


def process_batch():
    os.makedirs(CATALOG_OUT, exist_ok=True)
    scan_cmd = [
        PYTHON, SCAN_SCRIPT, LORA_IMPORT_DIR,
        "--organize", "move", "--dest", LORA_ROOT,
        "--out", CATALOG_OUT, "--workers", "2",
    ]
    if CIVITAI_TOKEN:
        scan_cmd += ["--civitai-token", CIVITAI_TOKEN]
    if CACHE_DB:
        scan_cmd += ["--cache", CACHE_DB]
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


def missing_config():
    """Return the names of any required env vars that are unset. SCAN_SCRIPT /
    IMPORT_SCRIPT are omitted — they default to the vendored local copies."""
    return [
        n for n, v in (
            ("KR_RELAY_TOKEN", KR_RELAY_TOKEN), ("LORA_ROOT", LORA_ROOT),
            ("LORA_IMPORT_DIR", LORA_IMPORT_DIR),
        ) if not v
    ]


def watch_loop():
    """The poll loop. Runs forever. Safe to call on its own thread (e.g. embedded
    in kr-relay) or as the standalone process entrypoint. Assumes config is
    present — callers should check missing_config() first."""
    os.makedirs(LORA_IMPORT_DIR, exist_ok=True)
    log(f"watching {LORA_IMPORT_DIR} -> {LORA_ROOT}  (poll {LORA_POLL_SECONDS}s, {KR_BASE_URL})")

    seen = {}  # path -> stat signature from the previous poll
    while True:
        try:
            # Pull one queued front-end download (if any) into the import folder;
            # the stability check below catalogs it on a later cycle.
            claim_and_download()

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
        time.sleep(LORA_POLL_SECONDS)


def main():
    missing = missing_config()
    if missing:
        log(f"missing required env: {', '.join(missing)} — exiting")
        sys.exit(1)
    watch_loop()


if __name__ == "__main__":
    main()
