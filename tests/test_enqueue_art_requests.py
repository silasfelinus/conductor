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
