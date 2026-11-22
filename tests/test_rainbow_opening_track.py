"""Pinned audio track retrieval for the Rainbow Space Princess opening."""

from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from scripts import export_rainbow_opening as opening


class OpeningPinnedTrackTests(unittest.TestCase):
    def lookup(self, status, response):
        requests = []

        def http_json(method, url):
            requests.append((method, url))
            return status, response

        with patch.object(
            opening,
            "_core",
            return_value=SimpleNamespace(
                KR_BASE_URL="https://kindrobots.org",
                http_json=http_json,
            ),
        ):
            result = opening.track_image_id()
        self.assertEqual(
            requests,
            [("GET", "https://kindrobots.org/api/art/queue/44644")],
        )
        return result

    def test_done_score_survives_recent_jobs_pagination(self):
        self.assertEqual(
            self.lookup(
                200,
                {"data": {"job": {
                    "id": opening.TRACK_JOB_ID,
                    "status": "DONE",
                    "artImageId": 277111,
                }}},
            ),
            ("DONE", 277111),
        )

    def test_pending_score_is_not_mistaken_for_an_exportable_track(self):
        self.assertEqual(
            self.lookup(
                200,
                {"data": {"job": {
                    "id": opening.TRACK_JOB_ID,
                    "status": "PROCESSING",
                    "artImageId": None,
                }}},
            ),
            ("PROCESSING", None),
        )

    def test_done_without_real_artimage_does_not_ship_silent_audio(self):
        for bad in (None, 0, -4, True, "277111"):
            with self.subTest(art_image_id=bad):
                self.assertEqual(
                    self.lookup(
                        200,
                        {"data": {"job": {
                            "id": opening.TRACK_JOB_ID,
                            "status": "DONE",
                            "artImageId": bad,
                        }}},
                    ),
                    ("DONE_WITHOUT_AUDIO", None),
                )

    def test_wrong_job_id_and_missing_payload_fail_closed(self):
        for response in (
            {},
            {"data": {}},
            {"data": {"job": {"id": 9999, "status": "DONE", "artImageId": 1}}},
        ):
            with self.subTest(response=response):
                with self.assertRaisesRegex(RuntimeError, "unexpected queue response"):
                    self.lookup(200, response)

    def test_http_error_reports_pinned_job_number(self):
        with self.assertRaisesRegex(RuntimeError, "queue/44644: HTTP 403"):
            self.lookup(403, {"success": False})


if __name__ == "__main__":
    unittest.main()
