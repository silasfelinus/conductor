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
        if "status=PENDING" in url:
            return 200, {"data": {"jobs": [job, other], "pagination": {"hasNextPage": False}}}
        return 200, {"data": {"jobs": [], "pagination": {"hasNextPage": False}}}

    monkeypatch.setattr(rra, "http_json", fake)
    assert rra.already_queued() == {("reward", 235)}


def test_the_queue_walk_pages_by_page_not_skip(monkeypatch):
    """`/api/art/queue` reads `page`, and ignores `skip` entirely.

    A skip-driven walk therefore re-reads page one forever: the row count never
    drops below the page size, so the loop never ends, and because it never
    repeats a job *id* within a page it reads as a slow endpoint rather than as
    a loop. Two runs hung on this before it was spotted in the handler source.
    """
    urls = []

    def fake(method, url, body=None, timeout=180):
        urls.append(url)
        if "status=PENDING" not in url:
            return 200, {"data": {"jobs": [], "pagination": {"hasNextPage": False}}}
        page = int(url.split("page=")[1].split("&")[0])
        if page > 2:
            return 200, {"data": {"jobs": [], "pagination": {"hasNextPage": False}}}
        return 200, {
            "data": {
                "jobs": [
                    {
                        "payload": {
                            "save": {"designer": "negation-repair"},
                            "entityArt": {"entityType": "facet", "entityId": page * 100 + n},
                        }
                    }
                    for n in range(3)
                ],
                "pagination": {"hasNextPage": page < 2},
            }
        }

    monkeypatch.setattr(rra, "http_json", fake)
    seen = rra.already_queued()
    assert not any("skip=" in url for url in urls)
    assert [u for u in urls if "status=PENDING" in u] == [
        f"{rra.KR_BASE_URL}/api/art/queue?pageSize={rra.QUEUE_PAGE}&page=1&status=PENDING",
        f"{rra.KR_BASE_URL}/api/art/queue?pageSize={rra.QUEUE_PAGE}&page=2&status=PENDING",
    ]
    assert ("facet", 100) in seen and ("facet", 202) in seen


def test_the_done_walk_stops_below_the_manifest_date(monkeypatch):
    """14,979 DONE jobs is 75 large reads for rows that cannot match.

    Only DONE is ordered by date (`updatedAt desc`); PENDING is ordered
    `priority desc, id asc`, so the cutoff must not be applied there or it
    would truncate the walk at the first low-priority page.
    """
    cutoff = rra.queue_cutoff({"generated": "2026-09-20"})
    assert cutoff == "2026-09-17"
    assert rra.DATE_ORDERED_STATUSES == {"DONE"}

    fresh = {"updatedAt": "2026-09-19T23:00:00.000Z", "payload": {}}
    stale = {"updatedAt": "2026-08-01T00:00:00.000Z", "payload": {}}
    pages = {1: [fresh, stale], 2: [stale, stale], 3: [stale, stale]}
    read = []

    def fake(method, url, body=None, timeout=180):
        if "status=DONE" not in url:
            return 200, {"data": {"jobs": [], "pagination": {"hasNextPage": False}}}
        page = int(url.split("page=")[1].split("&")[0])
        read.append(page)
        return 200, {"data": {"jobs": pages.get(page, []), "pagination": {"hasNextPage": True}}}

    monkeypatch.setattr(rra, "http_json", fake)
    rra.already_queued(cutoff)
    # Page 1 is mixed so the walk continues; page 2 is wholly stale and ends it.
    assert read == [1, 2]


def test_a_mixed_page_does_not_end_the_done_walk(monkeypatch):
    """One stale row in an otherwise current page must not truncate the read."""
    cutoff = rra.queue_cutoff({"generated": "2026-09-20"})
    read = []

    def fake(method, url, body=None, timeout=180):
        if "status=DONE" not in url:
            return 200, {"data": {"jobs": [], "pagination": {"hasNextPage": False}}}
        page = int(url.split("page=")[1].split("&")[0])
        read.append(page)
        rows = [
            {"updatedAt": "2026-08-01T00:00:00.000Z", "payload": {}},
            {"updatedAt": "2026-09-19T00:00:00.000Z", "payload": {}},
        ]
        return 200, {"data": {"jobs": rows, "pagination": {"hasNextPage": page < 3}}}

    monkeypatch.setattr(rra, "http_json", fake)
    rra.already_queued(cutoff)
    assert read == [1, 2, 3]


def test_an_unreadable_manifest_date_falls_back_to_the_full_walk():
    assert rra.queue_cutoff({}) == ""
    assert rra.queue_cutoff({"generated": "not a date"}) == ""
