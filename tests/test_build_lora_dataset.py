"""Tests for scripts/build_lora_dataset.py (comic-creator t-016)."""

import sys
import zipfile
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_lora_dataset as lora  # noqa: E402


def _character(images=None, **extra):
    return {
        "key": "zuzu",
        "name": "Zuzu",
        "trigger": "zuzukoala",
        "class": "koala",
        "repeats": 10,
        "identity": ["anthro koala", "male"],
        "images": images if images is not None else [{"id": 1, "tags": ["front view"]}] * 10,
        **extra,
    }


def test_caption_puts_the_trigger_first_and_drops_repeats():
    assert lora.caption("zuzukoala", ["anthro koala", "male"], ["front view", "Male", " "]) == (
        "zuzukoala, anthro koala, male, front view"
    )


def test_subset_folder_follows_kohya_repeats_naming():
    assert lora.subset_dir(_character()) == "10_zuzukoala koala"


def test_validate_flags_bad_triggers_missing_class_and_thin_sets():
    spec = {"characters": [_character(trigger="zuzu koala"), _character(**{"class": ""}), _character(images=[{"id": 1}] * 3)]}
    problems = lora.validate(spec)
    assert any("trigger" in p for p in problems)
    assert any("class word" in p for p in problems)
    assert any("at least 10" in p for p in problems)
    assert lora.validate({"characters": [_character()]}) == []


def test_ledger_reference_resolves_to_the_rendered_image(tmp_path):
    (tmp_path / "L.yaml").write_text(
        yaml.safe_dump(
            {
                "subjects": [
                    {"key": "lora-zuzu-angry", "art": {"kontext-expr": {"status": "DONE", "art_image_id": 777}}},
                    {"key": "lora-zuzu-sad", "art": {"kontext-expr": {"status": "PENDING", "art_image_id": None}}},
                ]
            }
        )
    )
    assert lora.resolve_image_id({"ledger": "L.yaml", "ledger_key": "lora-zuzu-angry"}, tmp_path) == 777
    assert lora.resolve_image_id({"id": -5}, tmp_path) == -5
    with pytest.raises(ValueError, match="no art_image_id"):
        lora.resolve_image_id({"ledger": "L.yaml", "ledger_key": "lora-zuzu-sad"}, tmp_path)
    with pytest.raises(ValueError, match="not in"):
        lora.resolve_image_id({"ledger": "L.yaml", "ledger_key": "missing"}, tmp_path)


def test_dataset_toml_and_train_script_point_at_the_subset_and_model():
    character = _character()
    toml = lora.dataset_toml(character)
    assert "image_dir = 'img/10_zuzukoala koala'" in toml
    assert 'caption_extension = ".txt"' in toml and "enable_bucket = true" in toml
    ps1 = lora.train_ps1(character, "D:\\models\\base.safetensors", "D:\\Lora\\import")
    assert "sdxl_train_network.py" in ps1 and "zuzukoala_v1" in ps1
    assert "D:\\models\\base.safetensors" in ps1 and "--network_train_unet_only" in ps1


def test_build_writes_mirrored_cropped_images_captions_and_a_zip(tmp_path):
    pytest.importorskip("PIL")
    from PIL import Image

    def fetch(image_id):
        image = Image.new("RGB", (100, 200), "white")
        image.paste((255, 0, 0), (0, 0, 10, 200))  # a red strip on the left edge
        return image

    images = [{"id": 1, "tags": ["front view"]}, {"id": -1, "tags": ["profile right"]}]
    images += [{"id": 1, "crop": [0, 0, 1, 0.5], "tags": ["portrait"]}] + [{"id": 1}] * 7
    spec = {"base_model": "D:\\m.safetensors", "output_dir": "D:\\out", "characters": [_character(images=images)]}
    rows = lora.build(spec, tmp_path, tmp_path / "out", fetch=fetch)
    sub = tmp_path / "out" / "zuzukoala" / "img" / "10_zuzukoala koala"
    assert len(rows["zuzu"]) == 10 and len(list(sub.glob("*.png"))) == 10
    assert Image.open(sub / "001.png").getpixel((2, 100)) == (255, 0, 0)
    assert Image.open(sub / "002.png").getpixel((97, 100)) == (255, 0, 0), "a negative id is mirrored"
    assert Image.open(sub / "003.png").size == (100, 100), "crop is fractions of the render"
    assert (sub / "002.txt").read_text() == "zuzukoala, anthro koala, male, profile right\n"
    with zipfile.ZipFile(tmp_path / "out" / "zuzukoala.zip") as bundle:
        names = bundle.namelist()
    assert "zuzukoala/dataset.toml" in names and "zuzukoala/train.ps1" in names
    assert "zuzukoala/img/10_zuzukoala koala/010.txt" in names


def test_dry_run_fetches_nothing(tmp_path):
    def fetch(image_id):
        raise AssertionError("dry run must not fetch")

    spec = {"base_model": "m", "output_dir": "o", "characters": [_character()]}
    rows = lora.build(spec, tmp_path, tmp_path / "out", fetch=fetch, dry_run=True)
    assert len(rows["zuzu"]) == 10 and not (tmp_path / "out").exists()


def test_dry_run_reports_a_pending_ledger_render_but_a_real_build_refuses(tmp_path):
    (tmp_path / "L.yaml").write_text(yaml.safe_dump({"subjects": [{"key": "k", "art": {"lane": {"art_image_id": None}}}]}))
    images = [{"ledger": "L.yaml", "ledger_key": "k"}] + [{"id": 1}] * 9
    spec = {"base_model": "m", "output_dir": "o", "characters": [_character(images=images)]}
    rows = lora.build(spec, tmp_path, tmp_path / "out", fetch=lambda i: None, dry_run=True)
    assert rows["zuzu"][0][1] is None
    with pytest.raises(ValueError, match="no art_image_id"):
        lora.build(spec, tmp_path, tmp_path / "out", fetch=lambda i: None)


def test_train_all_runs_every_set_in_order_and_always_restarts_the_relay():
    ps1 = lora.train_all_ps1(["zuzukoala", "zkasister", "zkaabbess"])
    assert '$triggers = @("zuzukoala", "zkasister", "zkaabbess")' in ps1
    assert "venv\\Scripts\\accelerate.exe" in ps1 and "git clone https://github.com/kohya-ss/sd-scripts.git" in ps1
    assert ps1.index("pm2 stop kr-relay") < ps1.index("$Comfy/queue"), "pause the relay, then let ComfyUI drain"
    assert ps1.index("pm2 stop kr-relay") < ps1.index("} finally {") < ps1.index("pm2 start kr-relay")
    assert "if ($LASTEXITCODE)" in ps1
    assert "Python310\\python.exe" in ps1 and "& $Python -m venv venv" in ps1, "uses ComfyUI's Python 3.10, not a bare python"
    assert "$Comfy/queue" in ps1 and "$Comfy/free" in ps1
    assert "_v1.safetensors" in ps1, "a finished set is skipped on a re-run"


def test_build_writes_train_all_beside_the_zips(tmp_path):
    pytest.importorskip("PIL")
    from PIL import Image

    spec = {"base_model": "m", "output_dir": "o", "characters": [_character()]}
    lora.build(spec, tmp_path, tmp_path / "out", fetch=lambda i: Image.new("RGB", (64, 64)))
    assert '@("zuzukoala")' in (tmp_path / "out" / "train_all.ps1").read_text()
