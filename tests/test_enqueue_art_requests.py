import yaml

import scripts.enqueue_art_requests as enq

LEDGER = {
    "project_slug": "comic-creator",
    "designer": "Comic Studio",
    "is_public": True,
    "lanes": [
        {"key": "zimage-turbo", "engine": "zimage", "prompt": "prose"},
        {
            "key": "il",
            "engine": "comfy",
            "checkpoint": "Illustrious/x.safetensors",
            "prompt": "tags",
            "prefix": "masterpiece",
            "suffix": "gritty",
        },
    ],
    "subjects": [
        {
            "key": "s1",
            "size": "1344x768",
            "prompt_prose": "a koala ronin on a dune",
            "prompt_tags": "anthro, koala",
            "negative": "nsfw, lowres",
            "jobs": {"zimage-turbo": None, "il": None},
        }
    ],
}


def _ledger(tmp_path):
    path = tmp_path / "ledger.yaml"
    path.write_text("# header line\n" + yaml.safe_dump(LEDGER, sort_keys=False))
    return path


def test_prose_lane_request_has_no_checkpoint_or_negative():
    body = enq.build_request(LEDGER, LEDGER["lanes"][0], LEDGER["subjects"][0])
    assert body["engine"] == "zimage"
    assert body["promptString"] == "a koala ronin on a dune"
    assert (body["width"], body["height"]) == (1344, 768)
    assert "checkpoint" not in body and "negativePrompt" not in body
    assert body["projectSlug"] == "comic-creator" and body["isPublic"] is True


def test_tag_lane_request_wraps_tags_and_carries_negative():
    body = enq.build_request(LEDGER, LEDGER["lanes"][1], LEDGER["subjects"][0])
    assert body["promptString"] == "masterpiece, anthro, koala, gritty"
    assert body["checkpoint"] == "Illustrious/x.safetensors"
    assert body["negativePrompt"] == "nsfw, lowres"
    assert not {"steps", "cfg", "sampler", "scheduler"} & body.keys()


def test_comfy_lane_carries_author_settings_only_when_set():
    lane = dict(LEDGER["lanes"][1], sampler="euler_ancestral", scheduler="normal", cfg=5)
    body = enq.build_request(LEDGER, lane, LEDGER["subjects"][0])
    assert (body["sampler"], body["cfg"]) == ("euler_ancestral", 5)
    assert "steps" not in body and "scheduler" not in body
    prose = dict(LEDGER["lanes"][0], sampler="euler")
    assert "sampler" not in enq.build_request(LEDGER, prose, LEDGER["subjects"][0])


def test_round4_ledger_is_a_fair_bakeoff():
    from pathlib import Path

    ledger = yaml.safe_load(
        Path("projects/comic-creator/issues/zuzu-koala-assassin-01/ART-ROUND-4.yaml").read_text()
    )
    cells = list(enq.iter_cells(ledger))
    assert len(cells) == 42
    assert ledger["is_public"] is False
    assert all(lane["checkpoint"].startswith("Illustrious/") for lane in ledger["lanes"])
    assert len({(lane["prefix"], lane["suffix"], lane["prompt"]) for lane in ledger["lanes"]}) == 1
    assert not any(k in lane for lane in ledger["lanes"] for k in ("steps", "cfg", "sampler", "scheduler"))


def test_submit_writes_job_ids_back_and_skips_existing(tmp_path):
    path = _ledger(tmp_path)
    header, ledger = enq.load_ledger(path)
    calls = []

    def post(body):
        calls.append(body)
        return 200, {"success": True, "data": {"jobId": 100 + len(calls)}}

    cells = list(enq.iter_cells(ledger))
    assert enq.submit(path, header, ledger, cells, post=post) == (2, 0)
    text = path.read_text()
    assert text.startswith("# header line\n")
    saved = yaml.safe_load(text)
    assert saved["subjects"][0]["jobs"] == {"zimage-turbo": 101, "il": 102}

    header, ledger = enq.load_ledger(path)
    assert enq.submit(path, header, ledger, list(enq.iter_cells(ledger)), post=post) == (0, 0)
    assert len(calls) == 2


def test_failed_submit_leaves_cell_empty(tmp_path):
    path = _ledger(tmp_path)
    header, ledger = enq.load_ledger(path)
    result = enq.submit(path, header, ledger, list(enq.iter_cells(ledger, ["il"])), post=lambda b: (402, {"message": "no mana"}))
    assert result == (0, 1)
    assert yaml.safe_load(path.read_text())["subjects"][0]["jobs"]["il"] is None


def test_refresh_status_records_art_image(tmp_path):
    path = _ledger(tmp_path)
    header, ledger = enq.load_ledger(path)
    ledger["subjects"][0]["jobs"] = {"zimage-turbo": 7, "il": None}
    counts = enq.refresh_status(path, header, ledger, get=lambda job_id: (200, {"data": {"job": {"status": "DONE", "artImageId": 9}}}))
    assert counts == {"DONE": 1}
    saved = yaml.safe_load(path.read_text())
    assert saved["subjects"][0]["art"] == {"zimage-turbo": {"status": "DONE", "art_image_id": 9}}


KONTEXT_LEDGER = {
    "lanes": [{"key": "angles", "engine": "kontext", "prompt": "prose", "steps": 20, "guidance": 2.5}],
    "subjects": [
        {"key": "front", "size": "832x1216", "prompt_prose": "turn him around", "source_image_id": 7, "jobs": {}},
        {"key": "back", "size": "832x1216", "prompt_prose": "show his back", "source_image_id": 7, "jobs": {}},
    ],
}


def test_kontext_lane_sends_source_image_and_settings():
    lane, subject = KONTEXT_LEDGER["lanes"][0], KONTEXT_LEDGER["subjects"][0]
    body = enq.build_request(KONTEXT_LEDGER, lane, subject, "data:image/png;base64,AAAA")
    assert body["engine"] == "kontext"
    assert body["sourceImageBase64"] == "data:image/png;base64,AAAA"
    assert body["steps"] == 20 and body["guidance"] == 2.5
    assert "negativePrompt" not in body and "checkpoint" not in body


def test_kontext_lane_without_source_image_is_refused():
    lane, subject = KONTEXT_LEDGER["lanes"][0], KONTEXT_LEDGER["subjects"][0]
    try:
        enq.build_request(KONTEXT_LEDGER, lane, subject)
    except ValueError as exc:
        assert "source_image_id" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")


def test_submit_fetches_each_source_image_once(tmp_path):
    path = tmp_path / "kontext.yaml"
    path.write_text(yaml.safe_dump(KONTEXT_LEDGER, sort_keys=False))
    header, ledger = enq.load_ledger(path)
    fetched, sent = [], []

    def fetch(image_id):
        fetched.append(image_id)
        return "data:image/webp;base64,BBBB"

    def post(body):
        sent.append(body)
        return 200, {"data": {"jobId": 100 + len(sent)}}

    cells = list(enq.iter_cells(ledger))
    assert enq.submit(path, header, ledger, cells, post=post, fetch_source=fetch) == (2, 0)
    assert fetched == [7]
    assert all(b["sourceImageBase64"] == "data:image/webp;base64,BBBB" for b in sent)
    assert yaml.safe_load(path.read_text())["subjects"][1]["jobs"]["angles"] == 102


def test_plain_source_passes_through_without_pil():
    subject = {"source_image_id": 7}
    assert enq.compose_source(subject, lambda image_id: f"data:image/png;base64,{image_id}") == "data:image/png;base64,7"


def _png(color, size):
    import base64
    import io

    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", size, color).save(buffer, "PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()


def test_source_crop_and_reference_stitch_geometry():
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    images = {1: _png("red", (300, 200)), 2: _png("blue", (100, 400))}
    fetched = []

    def fetch(image_id):
        fetched.append(image_id)
        return images[image_id]

    subject = {"source_image_id": 1, "source_crop": [0, 0, 1 / 3, 1], "reference_image_id": 2}
    out = enq._decode_data_url(enq.compose_source(subject, fetch))
    # Source cropped to its left third (100x200); reference 100x400 scaled to height 200 (50 wide), on the left.
    assert out.size == (150, 200)
    assert out.getpixel((10, 100)) == (0, 0, 255)
    assert out.getpixel((140, 100)) == (255, 0, 0)
    assert sorted(fetched) == [1, 2]


def test_bad_crop_is_refused():
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    subject = {"source_image_id": 1, "source_crop": [0.6, 0, 0.4, 1]}
    with pytest.raises(ValueError):
        enq.compose_source(subject, lambda image_id: _png("red", (10, 10)))


def test_source_flip_mirrors_the_source_only():
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    import base64
    import io

    from PIL import Image

    image = Image.new("RGB", (20, 10), "red")
    image.paste(Image.new("RGB", (10, 10), "blue"), (0, 0))  # blue on the left half
    buffer = io.BytesIO()
    image.save(buffer, "PNG")
    source = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
    out = enq._decode_data_url(enq.compose_source({"source_image_id": 1, "source_flip": True}, lambda _: source))
    assert out.getpixel((2, 5)) == (255, 0, 0) and out.getpixel((17, 5)) == (0, 0, 255)


def test_masked_subject_goes_to_the_kontext_route_with_a_mask(tmp_path):
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    ledger = {
        "designer": "Comic Studio",
        "lanes": [{"key": "angles", "engine": "kontext", "prompt": "prose", "steps": 20, "guidance": 2.5}],
        "subjects": [
            {"key": "stump", "size": "40x20", "prompt_prose": "a stump", "source_image_id": 7,
             "mask_box": [0, 0, 0.5, 1], "jobs": {}},
            {"key": "plain", "size": "40x20", "prompt_prose": "turn", "source_image_id": 7, "jobs": {}},
        ],
    }
    path = tmp_path / "masked.yaml"
    path.write_text(yaml.safe_dump(ledger, sort_keys=False))
    header, loaded = enq.load_ledger(path)
    sent = []

    def post(body):
        sent.append(body)
        return 200, {"data": {"jobId": len(sent)}}

    cells = list(enq.iter_cells(loaded))
    assert enq.submit(path, header, loaded, cells, post=post, fetch_source=lambda _: _png("red", (40, 20))) == (2, 0)
    masked, plain = sent
    assert set(masked) >= {"prompt", "imageData", "maskData", "width", "height", "steps", "guidance", "designer"}
    assert "promptString" not in masked and enq.request_url(masked).endswith("/api/comfy/kontext/enqueue")
    assert enq.request_url(plain).endswith("/api/art/enqueue") and "maskData" not in plain
    mask = enq._decode_data_url(masked["maskData"])
    assert mask.size == (40, 20)
    assert mask.getpixel((5, 10)) == (255, 255, 255) and mask.getpixel((35, 10)) == (0, 0, 0)


def test_bad_mask_box_is_refused():
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    with pytest.raises(ValueError):
        enq.make_mask(_png("red", (10, 10)), [0.8, 0, 0.2, 1])


def test_mask_box_accepts_several_boxes():
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    mask = enq._decode_data_url(enq.make_mask(_png("red", (40, 20)), [[0, 0, 0.25, 1], [0.75, 0, 1, 1]]))
    assert mask.getpixel((2, 10)) == (255, 255, 255)
    assert mask.getpixel((20, 10)) == (0, 0, 0)
    assert mask.getpixel((38, 10)) == (255, 255, 255)
