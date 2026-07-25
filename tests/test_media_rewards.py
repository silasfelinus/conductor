import base64
import importlib.util
import sys
from pathlib import Path

import pytest


def load_relay_media_module(monkeypatch):
    home_server = Path(__file__).parents[1] / "ops" / "home-server"
    monkeypatch.syspath_prepend(str(home_server))
    sys.modules.pop("relay_media_agent", None)
    sys.modules.pop("relay_agent", None)
    spec = importlib.util.spec_from_file_location(
        "relay_media_agent", home_server / "relay_media_agent.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "image_path",
    [
        "public/rewards/favor/test.webp",
        "/public/rewards/favor/test.webp",
        "rewards/favor/test.webp",
        "/rewards/favor/test.webp",
        r"public\rewards\favor\test.webp",
    ],
)
def test_relay_maps_reward_paths_under_images(monkeypatch, image_path):
    relay_media = load_relay_media_module(monkeypatch)

    media_kind, relative = relay_media.direct_media_target(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": image_path,
            }
        }
    )

    assert media_kind == "rewards"
    assert relative == Path("rewards/favor/test.webp")
    assert relay_media.direct_media_relative(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": image_path,
            }
        }
    ) == Path("rewards/favor/test.webp")


def test_relay_writes_rewards_inside_image_root(tmp_path, monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    images_root = tmp_path / "kindrobots" / "images"
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(images_root))
    monkeypatch.setattr(
        relay_media, "encode_image_for_suffix", lambda raw, _suffix: raw
    )

    destination = relay_media.write_direct_media(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": "public/rewards/favor/sample.webp",
            }
        },
        {
            "data_b64": base64.b64encode(b"encoded-image").decode(),
            "file_type": "png",
            "is_video": False,
        },
    )

    assert destination == images_root / "rewards" / "favor" / "sample.webp"
    assert destination.read_bytes() == b"encoded-image"
    assert not (destination.parent / "gallery.json").exists()
    assert not (images_root / "collections.json").exists()


def test_relay_uses_configured_image_root_without_sibling_mapping(
    tmp_path, monkeypatch
):
    relay_media = load_relay_media_module(monkeypatch)
    images_root = tmp_path / "media-cache"
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(images_root))

    assert relay_media.media_root() == images_root.resolve()
