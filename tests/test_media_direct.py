import base64
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import media_direct_consumer


def fake_consumer(tmp_path):
    def entry_to_job(entry):
        return {"engine": "COMFY", "payload": {"promptString": entry["prompt"]}}

    def save_result(entry, image_b64):
        output = tmp_path / "process" / Path(entry["image_path"]).name
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(base64.b64decode(image_b64))
        return output, None

    return SimpleNamespace(
        ROOT=tmp_path,
        entry_to_job=entry_to_job,
        save_result=save_result,
    )


def test_consumer_adds_exact_destination(tmp_path, monkeypatch):
    consumer = fake_consumer(tmp_path)
    monkeypatch.setattr(media_direct_consumer, "_media_exists", lambda _path: True)
    media_direct_consumer.patch_consumer(
        consumer, media_direct_consumer.KIND_ROBOTS_REPO
    )

    entry = {
        "prompt": "a friendly robot",
        "image_path": "public/images/bots/test/test.webp",
    }
    job = consumer.entry_to_job(entry)

    assert job["payload"]["targetRepo"] == "silasfelinus/kind_robots"
    assert job["payload"]["imagePath"] == entry["image_path"]

    output, warning = consumer.save_result(entry, base64.b64encode(b"bytes").decode())
    assert output == tmp_path / ".media-direct" / "bots" / "test" / "test.webp"
    assert "directly" in warning
    assert not (tmp_path / "process" / "test.webp").exists()


def test_consumer_keeps_fallback_when_public_media_does_not_verify(
    tmp_path, monkeypatch
):
    consumer = fake_consumer(tmp_path)
    monkeypatch.setattr(media_direct_consumer, "_media_exists", lambda _path: False)
    media_direct_consumer.patch_consumer(
        consumer, media_direct_consumer.KIND_ROBOTS_REPO
    )

    entry = {
        "prompt": "a friendly robot",
        "image_path": "public/images/bots/test/test.webp",
    }
    output, warning = consumer.save_result(entry, base64.b64encode(b"bytes").decode())

    assert output.read_bytes() == b"bytes"
    assert "fallback" in warning


def load_relay_media_module(monkeypatch):
    home_server = Path(__file__).parents[1] / "ops" / "home-server"
    monkeypatch.syspath_prepend(str(home_server))
    sys.modules.pop("relay_media_agent", None)
    spec = importlib.util.spec_from_file_location(
        "relay_media_agent", home_server / "relay_media_agent.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_relay_maps_exact_kindrobots_path(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)

    relative = relay_media.direct_media_relative(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": "public/images/bots/avatars/test.webp",
            }
        }
    )

    assert relative == Path("bots/avatars/test.webp")


@pytest.mark.parametrize(
    "image_path",
    [
        "images/test.webp",
        "public/images/../secret.webp",
        "public/images/../../secret.webp",
    ],
)
def test_relay_rejects_unsafe_kindrobots_paths(monkeypatch, image_path):
    relay_media = load_relay_media_module(monkeypatch)

    with pytest.raises(ValueError):
        relay_media.direct_media_relative(
            {
                "payload": {
                    "targetRepo": "silasfelinus/kind_robots",
                    "imagePath": image_path,
                }
            }
        )


def test_relay_writes_file_and_refreshes_manifests(tmp_path, monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(tmp_path))

    destination = relay_media.write_direct_media(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": "public/images/test/sample.svg",
            }
        },
        {
            "data_b64": base64.b64encode(b"<svg></svg>").decode(),
            "file_type": "svg",
            "is_video": False,
        },
    )

    assert destination == tmp_path / "test" / "sample.svg"
    assert destination.read_bytes() == b"<svg></svg>"
    assert (tmp_path / "test" / "gallery.json").read_text().strip() == '[\n  "sample.svg"\n]'
    assert '"test": "test"' in (tmp_path / "collections.json").read_text()
