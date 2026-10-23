"""relay_fingerprint.py -- a version string that changes whenever the relay's code does.

kr-relay used to report agentVersion "conductor-relay-completion-proof-v1",
a constant nobody bumped. On 2026-10-23 Coat Dance ArtJob 42356 failed in
ComfyUI's LoadVideo/PyAV with the exact defect conductor#6444 had fixed two
days earlier: Silas-PC was still running the pre-#6444 worker, and relay-status
could not say so. The only tell was the old wording of the error message.

So the version is now derived from the code itself: a hash of every module the
kr-relay pm2 process (relay_media_agent.py) loads from this folder, read once
at startup. A relay that was pulled but never restarted keeps reporting the old
hash, which is the case that matters. scripts/check_relay_version_drift.py
computes the same hash from main and flags any relay whose hash differs.

Line endings are normalised so a Windows checkout with core.autocrlf hashes
the same as CI. Standard library only: relay_agent.py imports this first.
"""

import hashlib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = "conductor-relay-"

# Every module the kr-relay process imports from ops/home-server. Add a file
# here when relay_media_agent.py (or anything it imports) starts loading it.
RELAY_CODE_FILES = (
    "relay_fingerprint.py",
    "relay_agent.py",
    "relay_media_agent.py",
    "lora_import_agent.py",
    "vace_relay.py",
    "coat_dance_vace_worker.py",
)

_VERSION_RE = re.compile(re.escape(PREFIX) + r"([0-9a-f]{12})\b")


def code_fingerprint(root=HERE, files=RELAY_CODE_FILES):
    """First 12 hex digits of a sha256 over the relay modules under root."""
    digest = hashlib.sha256()
    for name in files:
        try:
            raw = (Path(root) / name).read_bytes().replace(b"\r\n", b"\n")
        except OSError:
            raw = b"<missing>"
        digest.update(name.encode("utf-8") + b"\0" + raw + b"\0")
    return digest.hexdigest()[:12]


def relay_version(commit="", root=HERE):
    """agentVersion for claims: conductor-relay-<fingerprint>[@<commit>]."""
    version = PREFIX + code_fingerprint(root)
    return f"{version}@{commit}" if commit else version


def parse_fingerprint(agent_version):
    """The fingerprint inside an agentVersion, or None for a pre-fingerprint relay."""
    match = _VERSION_RE.search(str(agent_version or ""))
    return match.group(1) if match else None
