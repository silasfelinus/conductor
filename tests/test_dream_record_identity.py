import json

from scripts import audit_dream_record_identity as identity


def test_built_daily_dream_records_are_not_shared_between_bundles():
    report = identity.summary()
    assert report["collision_count"] == 0, json.dumps(report, indent=2, ensure_ascii=False)
