import pytest
import yaml

import scripts.ensure_ledger_facets as ens

ROW = {"key": "tiger", "slug": "tiger", "title": "Tiger", "taxonomy": "animal",
       "description": "A big striped cat.", "art_prompt": "Tiger. A tiger on a rock.", "facet_id": None}


def _ledger(tmp_path, rows):
    path = tmp_path / "facets.yaml"
    data = {"project_slug": "hybridizer", "designer": "hybridizer-starter-catalog", "facets": rows}
    path.write_text("# header\n" + yaml.safe_dump(data, sort_keys=False))
    header, ledger = ens.load_ledger(path)
    return path, header, ledger


def test_creates_a_missing_facet_and_writes_its_id_back(tmp_path):
    path, header, ledger = _ledger(tmp_path, [dict(ROW)])
    posted = []
    created, adopted, failed = ens.ensure(
        path, header, ledger, live=True,
        get=lambda url: (200, {"data": [{"id": 1, "slug": "tiger-shark"}]}),
        post=lambda body: posted.append(body) or (201, {"data": {"id": 2981}}),
    )
    assert (created, adopted, failed) == (1, 0, 0)
    assert posted[0]["taxonomy"] == "ANIMAL" and posted[0]["designer"] == "hybridizer-starter-catalog"
    assert yaml.safe_load(path.read_text())["facets"][0]["facet_id"] == 2981
    assert path.read_text().startswith("# header")


def test_adopts_an_existing_slug_and_never_posts(tmp_path):
    path, header, ledger = _ledger(tmp_path, [dict(ROW)])
    created, adopted, failed = ens.ensure(
        path, header, ledger, live=True,
        get=lambda url: (200, {"data": [{"id": 77, "slug": "tiger"}]}),
        post=lambda body: pytest.fail("must not create a slug the catalog holds"),
    )
    assert (created, adopted, failed) == (0, 1, 0)
    assert ledger["facets"][0]["facet_id"] == 77


def test_an_unreachable_catalog_is_a_failure_not_an_absence(tmp_path):
    path, header, ledger = _ledger(tmp_path, [dict(ROW)])
    created, adopted, failed = ens.ensure(
        path, header, ledger, live=True,
        get=lambda url: (502, None),
        post=lambda body: pytest.fail("must not create when existence is unknown"),
    )
    assert (created, adopted, failed) == (0, 0, 1)


def test_hybridizer_starter_ledgers_agree():
    facets = yaml.safe_load(open("projects/hybridizer/facets/STARTER-FACETS-ROUND-1.yaml"))["facets"]
    art = yaml.safe_load(open("projects/hybridizer/art/STARTER-INGREDIENTS-ROUND-1.yaml"))
    ids = {row["key"]: row["facet_id"] for row in facets}
    assert len(ids) == 90 and all(isinstance(v, int) for v in ids.values())
    assert len(frozenset(ids.values())) == 90
    assert {s["starter_key"]: s["entity_art"]["id"] for s in art["subjects"]} == ids
    for subject in art["subjects"]:
        prompt = subject["prompt_prose"].lower()
        assert not any(word in prompt for word in ("jar", "test tube", "capsule", "specimen"))
