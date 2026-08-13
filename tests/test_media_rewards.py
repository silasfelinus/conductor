"""Reward art lives UNDER the images root, in a ``rewards`` folder inside it.

There is one media root. This file previously asserted the opposite -- that
``public/rewards/...`` was a sibling root with its own KR_MEDIA_REWARDS_DIR --
on the strength of `public/rewards/` existing in the kind_robots checkout. That
directory is 13 legacy committed files, and nothing serves from it.

Measured on 2026-08-13, against production:

    227 of 261 live Rewards store an imagePath under /images/rewards/...
      0 store one under /rewards/...
    https://media.acrocatranch.com/images/rewards/skill/adhd-spark.webp
      -> 200 image/webp

kind_robots settled this rule first and independently: its
server/utils/artJobNormalization.ts:normalizeKindRobotsImagePath rewrites
`rewards/` -> `images/rewards/` and "has since art-job ingestion was written",
and utils/scripts/repairRewardImagePaths.ts calls `/rewards/` the LEGACY_PREFIX
and `/images/rewards/` the CORRECT_PREFIX, having repaired 195 rows on
2026-08-04. The relay was the last place holding a second, contradictory
definition -- and because KR_MEDIA_REWARDS_DIR was never configured on the box,
every reward job routed through it would have failed with "KR_MEDIA_REWARDS_DIR
is required". The startup line reporting that missing root is what surfaced it
(Silas, 2026-08-13: "there is no public/rewards and shouldnt be, all images
live inside images/").
"""

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
        "/images/rewards/favor/test.webp",
        "images/rewards/favor/test.webp",
        "public/rewards/favor/test.webp",
        "/public/rewards/favor/test.webp",
        "rewards/favor/test.webp",
        "/rewards/favor/test.webp",
        r"public\rewards\favor\test.webp",
        "https://media.acrocatranch.com/images/rewards/favor/test.webp",
    ],
)
def test_every_reward_spelling_folds_under_the_images_root(monkeypatch, image_path):
    relay_media = load_relay_media_module(monkeypatch)

    assert relay_media.normalize_kindrobots_image_path(image_path) == (
        "public/images/rewards/favor/test.webp"
    )

    job = {
        "payload": {
            "targetRepo": "silasfelinus/kind_robots",
            "imagePath": image_path,
        }
    }
    assert relay_media.direct_media_target(job) == Path("rewards/favor/test.webp")
    assert relay_media.direct_media_relative(job) == Path("rewards/favor/test.webp")


def test_reward_art_is_written_inside_the_images_root(tmp_path, monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    image_root = tmp_path / "kindrobots" / "images"
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(image_root))
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

    # The path the media origin actually serves: <images root>/rewards/...
    assert destination == image_root.resolve() / "rewards" / "favor" / "sample.webp"
    assert destination.read_bytes() == b"encoded-image"
    # Rewards are part of the browsable images tree now, so they get the same
    # manifest treatment as everything else under it.
    assert (image_root / "collections.json").exists()
    assert (destination.parent / "gallery.json").exists()


def test_a_missing_images_root_fails_loudly(monkeypatch):
    """No silent guess at a physical path, and no half-configured second root
    to forget: one root, named in the error."""
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", "")

    with pytest.raises(RuntimeError, match="KR_MEDIA_IMAGES_DIR"):
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


def test_there_is_no_second_media_root(monkeypatch):
    """A rewards-specific root must not come back. It is unreachable config
    that silently fails every reward job when unset."""
    relay_media = load_relay_media_module(monkeypatch)
    assert not hasattr(relay_media, "REWARDS_ROOT_VALUE")
    source = (
        Path(__file__).parents[1] / "ops" / "home-server" / "relay_media_agent.py"
    ).read_text(encoding="utf-8")
    assert "KR_MEDIA_REWARDS_DIR" not in source
    assert "KR_LOCAL_REWARDS_DIR" not in source


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


def test_media_root_resolves_the_single_configured_root(tmp_path, monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    image_root = tmp_path / "media-cache" / "images"
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(image_root))
    assert relay_media.media_root() == image_root.resolve()
