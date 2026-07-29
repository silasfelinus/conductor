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


def test_relay_keeps_literal_images_rewards_subfolder_under_images_root(
    monkeypatch,
):
    """``public/images/rewards/...`` is a literal image path (a folder named
    ``rewards`` under the images root) and is unrelated to the real
    ``public/rewards/...`` reward-asset root -- it must stay under the images
    root unchanged, not be confused with the sibling root below."""
    relay_media = load_relay_media_module(monkeypatch)
    image_path = "public/images/rewards/favor/test.webp"

    assert (
        relay_media.normalize_kindrobots_image_path(image_path) == image_path
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
def test_relay_canonicalizes_reward_paths_under_their_own_sibling_root(
    monkeypatch, image_path
):
    """``public/rewards/...`` is a real top-level directory in the
    kind_robots repo, a sibling of ``public/images/...`` -- not nested under
    it (confirmed against the live checkout: ``public/rewards/favor/...``
    exists, ``public/images/rewards/...`` does not). It must resolve to its
    own ``rewards`` media root, not be folded into the images root."""
    relay_media = load_relay_media_module(monkeypatch)

    assert relay_media.normalize_kindrobots_image_path(image_path) == (
        "public/rewards/favor/test.webp"
    )

    media_kind, relative = relay_media.direct_media_target(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": image_path,
            }
        }
    )

    assert media_kind == "rewards"
    assert relative == Path("favor/test.webp")
    assert relay_media.direct_media_relative(
        {
            "payload": {
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": image_path,
            }
        }
    ) == Path("favor/test.webp")


def test_relay_writes_rewards_under_their_own_root_not_inside_images(
    tmp_path, monkeypatch
):
    relay_media = load_relay_media_module(monkeypatch)
    image_root = tmp_path / "kindrobots" / "image"
    rewards_root = tmp_path / "kindrobots" / "rewards"
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(image_root))
    monkeypatch.setattr(relay_media, "REWARDS_ROOT_VALUE", str(rewards_root))
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

    assert destination == rewards_root / "favor" / "sample.webp"
    assert destination.read_bytes() == b"encoded-image"
    # Reward jobs don't get the images-gallery manifest treatment -- that's
    # specific to the browsable images gallery, not the reward-asset root.
    assert not (image_root / "collections.json").exists()


def test_relay_reward_job_fails_loudly_without_rewards_root_configured(
    monkeypatch,
):
    """A missing KR_MEDIA_REWARDS_DIR must fail loudly (retryable FAILED job)
    rather than silently guessing a physical path or falling back to the
    images root -- that silent-wrong-location failure is exactly the bug
    this fix replaces."""
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "REWARDS_ROOT_VALUE", "")

    with pytest.raises(RuntimeError, match="KR_MEDIA_REWARDS_DIR"):
        relay_media.write_direct_media(
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


def test_relay_uses_configured_image_and_rewards_roots_independently(
    tmp_path, monkeypatch
):
    relay_media = load_relay_media_module(monkeypatch)
    image_root = tmp_path / "media-cache" / "images"
    rewards_root = tmp_path / "media-cache" / "rewards"
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(image_root))
    monkeypatch.setattr(relay_media, "REWARDS_ROOT_VALUE", str(rewards_root))

    assert relay_media.media_root("images") == image_root.resolve()
    assert relay_media.media_root("rewards") == rewards_root.resolve()
