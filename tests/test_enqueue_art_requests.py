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


def test_subject_that_names_a_lane_renders_only_there():
    ledger = dict(LEDGER, subjects=[dict(LEDGER["subjects"][0], key="a", lane="il"), dict(LEDGER["subjects"][0], key="b")])
    cells = [(s["key"], lane["key"]) for s, lane in enq.iter_cells(ledger)]
    assert cells == [("a", "il"), ("b", "zimage-turbo"), ("b", "il")]


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


def test_contract_violating_prompt_is_never_posted(tmp_path):
    # Kind Robots only checks the contract at claim time, so a ", no text." prompt got
    # a job id, failed, and was never resubmitted (zuzu-showdown T008, 2026-10-10).
    path = _ledger(tmp_path)
    header, ledger = enq.load_ledger(path)
    ledger["subjects"][0]["prompt_prose"] = "a koala ronin on a dune, no text."
    calls = []
    cells = list(enq.iter_cells(ledger, ["zimage-turbo"]))
    result = enq.submit(path, header, ledger, cells, post=lambda b: calls.append(b) or (200, {"data": {"jobId": 1}}))
    assert result == (0, 1) and calls == []
    assert not (ledger["subjects"][0].get("jobs") or {}).get("zimage-turbo")


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

    assert "seed" not in body


def test_seed_comes_from_the_subject_then_the_lane():
    lane = {**KONTEXT_LEDGER["lanes"][0], "seed": 11}
    subject = KONTEXT_LEDGER["subjects"][0]
    body = enq.build_request(KONTEXT_LEDGER, lane, subject, "data:image/png;base64,AAAA")
    assert body["seed"] == 11
    body = enq.build_request(KONTEXT_LEDGER, lane, {**subject, "seed": 0}, "data:image/png;base64,AAAA")
    assert body["seed"] == 0


def test_kontext_lane_without_source_image_is_refused():
    lane, subject = KONTEXT_LEDGER["lanes"][0], KONTEXT_LEDGER["subjects"][0]
    try:
        enq.build_request(KONTEXT_LEDGER, lane, subject)
    except ValueError as exc:
        assert "source_image_id" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")


IMG2IMG_LEDGER = {
    "cast_loras": False,
    "lanes": [
        {
            "key": "house-i2i",
            "engine": "sdxl-img2img",
            "prompt": "tags",
            "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors",
            "steps": 30,
            "cfg": 5,
            "sampler": "euler_ancestral",
            "denoise": 0.6,
        }
    ],
    "subjects": [
        {
            "key": "mole-success",
            "size": "1344x768",
            "prompt_tags": "solo, anthro mole, relieved smile",
            "negative": "fox, wolf",
            "source_image_id": 245600,
            "seed": 3,
            "jobs": {},
        }
    ],
}


def test_sdxl_img2img_lane_sends_source_denoise_and_house_settings():
    lane, subject = IMG2IMG_LEDGER["lanes"][0], IMG2IMG_LEDGER["subjects"][0]
    body = enq.build_request(IMG2IMG_LEDGER, lane, subject, "data:image/png;base64,AAAA")
    assert body["engine"] == "sdxl-img2img"
    assert body["sourceImageBase64"] == "data:image/png;base64,AAAA"
    assert body["checkpoint"] == "Illustrious/arthemyWesternArt_v30.safetensors"
    assert (body["steps"], body["cfg"], body["sampler"]) == (30, 5, "euler_ancestral")
    assert body["denoise"] == 0.6 and body["negativePrompt"] == "fox, wolf" and body["seed"] == 3
    body = enq.build_request(IMG2IMG_LEDGER, lane, {**subject, "denoise": 0.75}, "data:image/png;base64,AAAA")
    assert body["denoise"] == 0.75


def test_sdxl_img2img_lane_without_source_image_is_refused():
    lane, subject = IMG2IMG_LEDGER["lanes"][0], IMG2IMG_LEDGER["subjects"][0]
    try:
        enq.build_request(IMG2IMG_LEDGER, lane, subject)
    except ValueError as exc:
        assert "source_image_id" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")


def test_submit_fetches_the_img2img_source(tmp_path):
    path = tmp_path / "img2img.yaml"
    path.write_text(yaml.safe_dump(IMG2IMG_LEDGER, sort_keys=False))
    header, ledger = enq.load_ledger(path)
    fetched, sent = [], []
    enq.submit(
        path,
        header,
        ledger,
        list(enq.iter_cells(ledger)),
        post=lambda body: (sent.append(body), (200, {"data": {"jobId": 5}}))[1],
        fetch_source=lambda image_id: (fetched.append(image_id), "data:image/png;base64,BBBB")[1],
    )
    assert fetched == [245600]
    assert sent[0]["sourceImageBase64"] == "data:image/png;base64,BBBB"


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


def test_source_pad_centres_a_portrait_in_a_widescreen_canvas():
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    images = {1: _png("red", (832, 1216))}
    out = enq._decode_data_url(enq.compose_source({"source_image_id": 1, "source_pad": "16:9"}, images.get))
    assert out.size == (2162, 1216)
    left = (2162 - 832) // 2
    assert out.getpixel((left + 10, 600)) == (255, 0, 0)
    assert out.getpixel((10, 600)) == (255, 255, 255)
    assert out.getpixel((2150, 600)) == (255, 255, 255)


def test_source_pad_leaves_a_matching_image_alone_and_refuses_nonsense():
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    images = {1: _png("blue", (1600, 900))}
    out = enq._decode_data_url(enq.compose_source({"source_image_id": 1, "source_pad": "16:9"}, images.get))
    assert out.size == (1600, 900)
    with pytest.raises(ValueError):
        enq.compose_source({"source_image_id": 1, "source_pad": "wide"}, images.get)


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


def test_source_image_fetch_sends_the_token(monkeypatch):
    # Private files need an authorized viewer (kind_robots#3235); an anonymous fetch 404s.
    monkeypatch.setattr(enq.core, "KR_API_TOKEN", "tok")
    monkeypatch.setattr(
        enq.core, "http_json", lambda *a, **k: (200, {"data": {"imagePath": "/images/generated/a.webp"}})
    )
    seen = {}

    class Response:
        headers = type("H", (), {"get_content_type": staticmethod(lambda: "image/webp")})()

        def read(self):
            return b"img"

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def fake_urlopen(request, timeout=None):
        seen["url"] = request.full_url
        seen["auth"] = request.get_header("Authorization")
        return Response()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert enq.fetch_source_image(1) == "data:image/webp;base64,aW1n"
    assert seen["url"].endswith("/images/generated/a.webp")
    assert seen["auth"] == "Bearer tok"


def test_loras_ride_on_comfy_requests_subject_first():
    ledger = {"is_public": False}
    lane = {"key": "a", "engine": "comfy", "prompt": "tags", "loras": [{"resource_id": 7}]}
    subject = {"key": "s", "size": "832x1216", "prompt_tags": "zuzukoala, front view"}
    assert enq.build_request(ledger, lane, subject)["loras"] == [{"resourceId": 7, "strength": 0.8}]
    subject["loras"] = [{"resource_id": "4593", "strength": 0.6}]
    assert enq.build_request(ledger, lane, subject)["loras"] == [{"resourceId": 4593, "strength": 0.6}]
    assert "loras" not in enq.build_request(ledger, {**lane, "loras": None}, {**subject, "loras": []})


def test_series_cast_loras_ride_only_on_subjects_that_name_the_character():
    ledger = {"series": "zuzu-koala-assassin"}
    lane = {"key": "a", "engine": "comfy", "prompt": "tags", "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors"}
    zuzu = {"key": "z", "size": "832x1216", "prompt_tags": "anthro koala, straw hat"}
    assert enq.build_request(ledger, lane, zuzu)["loras"] == [{"resourceId": 4593, "strength": 0.8}]
    siblings = {**zuzu, "prompt_tags": "the older sister carries the toddler"}
    assert enq.build_request(ledger, lane, siblings)["loras"] == [
        {"resourceId": 4583, "strength": 0.6},
        {"resourceId": 4588, "strength": 0.6},
    ]
    # Zuzu and the abbess fuse with any second LoRA (stacks: false), so a shared frame gets none.
    assert "loras" not in enq.build_request(ledger, lane, {**zuzu, "prompt_tags": "the koala bandages the coyote"})
    assert "loras" not in enq.build_request(ledger, lane, {**zuzu, "prompt_tags": "the abbess grips the sister"})
    assert enq.build_request(ledger, lane, {**zuzu, "prompt_tags": "the abbess at the gate"})["loras"] == [
        {"resourceId": 4595, "strength": 0.8}
    ]
    assert "loras" not in enq.build_request(ledger, lane, {**zuzu, "prompt_tags": "empty desert, coyotes"})
    assert "loras" not in enq.build_request(ledger, lane, {**zuzu, "prompt_tags": "a crowd of otter nuns"})


def test_series_cast_loras_respect_opt_outs_and_lane_family():
    ledger = {"series": "zuzu-koala-assassin"}
    lane = {"key": "a", "engine": "comfy", "prompt": "tags", "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors"}
    zuzu = {"key": "z", "size": "832x1216", "prompt_tags": "anthro koala"}
    assert "loras" not in enq.build_request({**ledger, "cast_loras": False}, lane, zuzu)
    assert "loras" not in enq.build_request(ledger, {**lane, "checkpoint": "SDXL/other.safetensors"}, zuzu)
    assert "loras" not in enq.build_request({"series": "another-series"}, lane, zuzu)
    assert "loras" not in enq.build_request(ledger, lane, {**zuzu, "loras": []}), "an explicit empty list wins"
    assert enq.build_request(ledger, lane, {**zuzu, "loras": [{"resource_id": 9}]})["loras"] == [
        {"resourceId": 9, "strength": 0.8}
    ]


VIDEO_LEDGER = {
    "project_slug": "zuzu-pinball",
    "lanes": [
        {"key": "wan-clips", "engine": "wan", "prompt": "prose", "fps": 16},
        {"key": "ltx-clips", "engine": "ltx", "prompt": "prose", "output_format": "webm"},
    ],
    "subjects": [
        {
            "key": "snap",
            "size": "640x640",
            "source_image_id": 7,
            "last_image_id": 8,
            "duration": 1.5,
            "prompt_prose": "the crocodile snaps his jaws shut",
            "negative": "blurry,\n  morphing",
            "lane": "wan-clips",
        },
        {
            "key": "idle",
            "size": "640x640",
            "source_image_id": 7,
            "duration": 2,
            "loop": True,
            "prompt_prose": "the crocodile breathes",
            "lane": "ltx-clips",
        },
    ],
}


def test_video_lane_animates_between_first_and_last_frames():
    lane, subject = VIDEO_LEDGER["lanes"][0], VIDEO_LEDGER["subjects"][0]
    body = enq.build_request(VIDEO_LEDGER, lane, subject, "data:image/png;base64,FIRST", "data:image/png;base64,LAST")
    assert body["engine"] == "wan"
    assert body["firstImageBase64"] == "data:image/png;base64,FIRST"
    assert body["secondImageBase64"] == "data:image/png;base64,LAST"
    assert body["fps"] == 16 and body["durationSeconds"] == 1.5
    assert body["loop"] is False and body["outputFormat"] == "webp"
    assert body["negativePrompt"] == "blurry, morphing"
    assert "renderScale" not in body and "sourceImageBase64" not in body


def test_ltx_lane_states_its_render_scale_and_an_empty_negative():
    lane, subject = VIDEO_LEDGER["lanes"][1], VIDEO_LEDGER["subjects"][1]
    body = enq.build_request(VIDEO_LEDGER, lane, subject, "data:image/png;base64,FIRST")
    assert body["renderScale"] == 1.0 and body["outputFormat"] == "webm"
    assert body["loop"] is True and body["negativePrompt"] == ""
    assert "secondImageBase64" not in body


def test_video_cell_needs_a_first_frame_and_a_duration():
    lane, subject = VIDEO_LEDGER["lanes"][0], VIDEO_LEDGER["subjects"][0]
    for args in ((subject, None), ({**subject, "duration": None}, "data:image/png;base64,A")):
        try:
            enq.build_request(VIDEO_LEDGER, lane, *args)
        except ValueError:
            pass
        else:  # pragma: no cover
            raise AssertionError("expected ValueError")


def test_submit_fetches_both_frames_of_a_video_cell(tmp_path):
    path = tmp_path / "clips.yaml"
    path.write_text(yaml.safe_dump(VIDEO_LEDGER, sort_keys=False))
    header, ledger = enq.load_ledger(path)
    sent = []

    def post(body):
        sent.append(body)
        return 200, {"data": {"jobId": 500 + len(sent)}}

    cells = list(enq.iter_cells(ledger))
    assert enq.submit(path, header, ledger, cells, post=post, fetch_source=lambda i: f"data:image/png;base64,{i}") == (
        2,
        0,
    )
    assert sent[0]["firstImageBase64"].endswith(",7") and sent[0]["secondImageBase64"].endswith(",8")
    assert sent[1]["firstImageBase64"].endswith(",7") and "secondImageBase64" not in sent[1]
