"""The three ways the resume pass reported failures that were its own.

Each test here is a bug the 2026-09-20 run produced on live data, where the
symptom named the wrong thing: a 404 that read as missing data, a 400 that
never reached the contract, and a dedupe check that silently matched nothing.
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "render_repaired_art", ROOT / "scripts" / "render_repaired_art.py"
)
rra = importlib.util.module_from_spec(spec)
sys.modules["render_repaired_art"] = rra
spec.loader.exec_module(rra)


def test_a_facet_is_resolved_from_the_list_not_the_detail_route(monkeypatch):
    """/api/facets/:id takes a SLUG. A numeric id answers 404 for every row.

    The manifest stores numeric ids, so the detail route refused all 575
    facets and each one was logged as "no artPrompt on the live record" --
    which reads like the record is empty, not like the URL is wrong.
    """
    calls = []

    def fake(method, url, body=None, timeout=180):
        calls.append(url)
        if "/api/facets?take=250&skip=0" in url:
            return 200, {"data": [{"id": 1193, "artPrompt": "a bare lantern"}]}
        if "/api/facets?take=250" in url:
            return 200, {"data": []}
        return 404, {"message": "Facet not found."}

    monkeypatch.setattr(rra, "http_json", fake)
    monkeypatch.setattr(rra, "_FACET_ROWS", None)

    row = rra.fetch_prompt("facet", 1193)
    assert row and row["artPrompt"] == "a bare lantern"
    assert not any("/api/facets/1193" in url for url in calls)


def test_the_facet_read_stops_when_a_page_adds_nothing(monkeypatch):
    """An endpoint that ignored `skip` would otherwise page forever."""
    monkeypatch.setattr(
        rra, "http_json",
        lambda *a, **k: (200, {"data": [{"id": 7, "artPrompt": "same row every time"}]}),
    )
    monkeypatch.setattr(rra, "_FACET_ROWS", None)
    assert set(rra.facet_rows()) == {7}


def test_a_bot_writes_its_avatar_slot_not_image_path():
    """`imagePath` is refused with 400 "Invalid bot image field."

    The first repair pass died before it reached a single bot, so all 64 of
    them met this for the first time in the resume run -- and a 400 never
    reaches the prompt contract, so it looked nothing like the 422s beside it.
    """
    assert rra.PRIMARY_FIELD.get("bot") == "avatarImage"
    for kind in rra.ORDER:
        if kind != "bot":
            assert rra.PRIMARY_FIELD.get(kind, rra.DEFAULT_PRIMARY_FIELD) == "imagePath"


def test_the_dedupe_check_reads_the_designer_where_enqueue_files_it(monkeypatch):
    """`designer` lives under payload.save, not at the top of payload.

    Reading `payload["designer"]` returned None for every job, so the skip set
    came back empty and every run looked like a clean first run.
    """
    job = {
        "payload": {
            "save": {"designer": "negation-repair"},
            "entityArt": {"entityType": "reward", "entityId": 235},
        }
    }
    other = {
        "payload": {
            "save": {"designer": "daily-dream"},
            "entityArt": {"entityType": "reward", "entityId": 999},
        }
    }

    def fake(method, url, body=None, timeout=180):
        if "status=PENDING&" in url or url.endswith("status=PENDING"):
            return 200, {"data": {"jobs": [job, other]}}
        return 200, {"data": {"jobs": []}}

    monkeypatch.setattr(rra, "http_json", fake)
    assert rra.already_queued() == {("reward", 235)}


def test_the_queue_read_pages_past_the_two_hundred_row_cap(monkeypatch):
    """`limit` is capped at 200 server-side; limit=1000 answers "200 of 1132"."""
    pages = {}
    for page in range(2):
        pages[page * rra.QUEUE_PAGE] = [
            {
                "payload": {
                    "save": {"designer": "negation-repair"},
                    "entityArt": {"entityType": "facet", "entityId": page * 1000 + n},
                }
            }
            for n in range(rra.QUEUE_PAGE)
        ]

    def fake(method, url, body=None, timeout=180):
        if "status=PENDING" not in url:
            return 200, {"data": {"jobs": []}}
        skip = int(url.split("skip=")[1].split("&")[0])
        return 200, {"data": {"jobs": pages.get(skip, [])}}

    monkeypatch.setattr(rra, "http_json", fake)
    seen = rra.already_queued()
    assert len(seen) == 2 * rra.QUEUE_PAGE
    assert ("facet", 1000) in seen
