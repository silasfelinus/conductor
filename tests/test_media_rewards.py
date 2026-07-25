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
        "public/images/rewards/favor/test.webp",
        "/public/images/rewards/favor/test.webp",
        "public/rewards/favor/test.webp",
        "/public/rewards/favor/test.webp",
        "rewards/favor/test.webp",
        "/rewards/favor/test.webp",
        r"public\rewards\favor\test.webp",
    ],
)
def test_relay_canonicalizes_reward_paths_under_public_images(
    monkeypatch, image_path
):
    relay_media = load_relay_media_module(monkeypatch)

    assert relay_media.normalize_kindrobots_image_path(image_path) == (
        "public/images/rewards/favor/test.webp"
    )

    media_kind, relative = relay_media.direct_media_target(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": image_path,
            }
        }
    )

    assert media_kind == "images"
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
    image_root = tmp_path / "kindrobots" / "image"
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(image_root))
    monkeypatch.setattr(
        relay_media, "encode_image_for_suffix", lambda raw, _suffix: raw
    )

    destination = relay_media.write_direct_media(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": "public/images/rewards/favor/sample.webp",
            }
        },
        {
            "data_b64": base64.b64encode(b"encoded-image").decode(),
            "file_type": "png",
            "is_video": False,
        },
    )

    assert destination == image_root / "rewards" / "favor" / "sample.webp"
    assert destination.read_bytes() == b"encoded-image"
    assert (destination.parent / "gallery.json").exists()
    assert (image_root / "collections.json").exists()


def test_relay_rejects_non_image_public_roots(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)

    with pytest.raises(ValueError, match="public/images/"):
        relay_media.direct_media_target(
            {
                "payload": {
                    "targetRepo": "silasfelinus/kind_robots",
                    "imagePath": "public/assets/test.webp",
                }
            }
        )


def test_relay_rejects_path_traversal(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)

    with pytest.raises(ValueError, match="Unsafe media imagePath"):
        relay_media.normalize_kindrobots_image_path(
            "public/images/rewards/../secret.webp"
        )


def test_relay_uses_configured_image_root_without_sibling_mapping(
    tmp_path, monkeypatch
):
    relay_media = load_relay_media_module(monkeypatch)
    image_root = tmp_path / "media-cache"
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(image_root))

    assert relay_media.media_root() == image_root.resolve()
