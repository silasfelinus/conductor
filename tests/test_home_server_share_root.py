"""The render box's model paths must all derive from one share root.

2026-08-25: renders failed for ~15 hours because the `Z:` SMB mapping to
alexandria was rebuilt and the box's three views of it diverged -- ComfyUI held
a dead connection object (WinError 1117), `folder_paths` later re-enumerated a
half-readable share into a short list (registered models reported as "no
matching file"), and an interactive `dir Z:\\ai\\models\\unet` in the same hour
said the path did not exist. A mapped drive letter is per-logon-session; a UNC
path is not. Switching away from the letter has to be one edit, so these paths
cannot drift back to eight hardcoded `Z:/ai/models/...` literals.
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

CONFIG = Path(__file__).resolve().parents[1] / "ops" / "home-server" / "ecosystem.config.js"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None, reason="node is not available"
)


def load(env=None):
    """The resolved pm2 config, as node sees it."""
    script = (
        "const c = require(process.argv[1]);"
        "console.log(JSON.stringify(c.apps.map("
        "a => ({name: a.name, args: a.args || '', env: a.env || {}}))));"
    )
    result = subprocess.run(
        ["node", "-e", script, str(CONFIG)],
        capture_output=True,
        text=True,
        check=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin", **(env or {})},
    )
    return {app["name"]: app for app in json.loads(result.stdout)}


def model_paths(apps):
    """Every configured path under the model root, from args and env alike."""
    blob = "\n".join(
        app["args"] + "\n" + "\n".join(str(v) for v in app["env"].values())
        for app in apps.values()
    )
    return set(re.findall(r"\S*/ai/models/\S*|\S*/kindrobots/images\S*", blob))


def test_engine_paths_default_to_local_disk():
    # 2026-09-21: the models moved off the share (LoRAs 2026-09-20, checkpoints
    # and diffusion_models 2026-09-21), so everything that WRITES or SCANS has
    # to follow them. An import inbox left on the share sorts and catalogs a
    # model into a directory ComfyUI no longer reads -- a LoRA dropped there has
    # been invisible to renders since the `loras:` declaration was removed, with
    # a correct Resource row and no error anywhere.
    apps = load()
    assert apps["kr-relay"]["env"]["LORA_ROOT"] == "D:/comfy/comfy-fast/models/Lora"
    assert apps["kr-relay"]["env"]["LORA_IMPORT_DIR"] == (
        "D:/comfy/comfy-fast/models/Lora/import"
    )
    assert apps["kr-relay"]["env"]["CHECKPOINT_IMPORT_DIR"] == (
        "D:/comfy/comfy-fast/models/checkpoints/import"
    )
    # 2026-09-19: the default moved from the WebUI-era `Stable-diffusion` folder to
    # `checkpoints` when the watched-import lane was generalized from LoRAs to
    # checkpoints (lora-ingestion/t-009). ecosystem.config.js is the source of truth;
    # this assertion follows it rather than pinning the retired path.
    assert apps["kr-download"]["env"]["KR_CHECKPOINT_DIR"] == (
        "D:/comfy/comfy-fast/models/checkpoints"
    )


def test_share_probe_stays_on_the_share():
    # The probe answers "is the SHARE alive?", which is a different question
    # from "where do models live?". Pointing it at local disk makes it pass
    # unconditionally and silently disarms the gate that stops the relay
    # claiming jobs against a dead share -- ~2700 jobs burned that way on
    # 2026-08-28 when a weaker (scandir-only) gate stayed green.
    apps = load()
    assert apps["kr-relay"]["env"]["KR_SHARE_PROBE_PATH"] == "Z:/ai/models"


def test_share_probe_does_not_follow_the_engine_root():
    # Moving the engine's models must not drag the probe along with them.
    apps = load({"KR_ENGINE_MODEL_ROOT": "E:/elsewhere/models"})
    assert apps["kr-relay"]["env"]["LORA_ROOT"] == "E:/elsewhere/models/Lora"
    assert apps["kr-relay"]["env"]["KR_SHARE_PROBE_PATH"] == "Z:/ai/models"


def test_one_env_var_moves_every_model_path_off_the_drive_letter():
    apps = load({"KR_SHARE_ROOT": "//alexandria/array"})
    paths = model_paths(apps)
    assert paths, "expected to find configured model paths"
    stragglers = sorted(p for p in paths if p.startswith("Z:"))
    assert not stragglers, f"still pinned to the drive letter: {stragglers}"
    assert all(p.startswith("//alexandria/array/") for p in paths), sorted(paths)


def test_media_dir_follows_the_same_share_root():
    apps = load({"KR_SHARE_ROOT": "//alexandria/array"})
    assert apps["kr-relay"]["env"]["KR_MEDIA_IMAGES_DIR"] == (
        "//alexandria/array/kindrobots/images"
    )


def test_model_root_can_be_overridden_independently_of_the_share():
    # The models and the media share do not have to move together. Since
    # 2026-09-21 KR_MODEL_ROOT steers the SHARE-side paths (the probe above);
    # the engine's own directories are KR_ENGINE_MODEL_ROOT's job.
    apps = load({"KR_MODEL_ROOT": "//alexandria/models"})
    assert apps["kr-relay"]["env"]["KR_SHARE_PROBE_PATH"] == "//alexandria/models"
    assert apps["kr-relay"]["env"]["KR_MEDIA_IMAGES_DIR"].startswith("Z:")
