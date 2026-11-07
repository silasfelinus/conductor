import scripts.check_roadmap_note_mismatch as lint

LONG = "Author the full cocaine meth and mdma opening lens journeys across every companion route end to end, including seeded junctions, signature endings, fate convergence and the verification pass."


def test_flags_note_copied_from_sibling():
    tasks = [
        {"id": "t-1", "title": "A", "note": LONG + " first"},
        {"id": "t-2", "title": "B", "note": LONG + " second"},
    ]
    assert lint.find_mismatches(tasks) == ["t-2: note opens with the same text as t-1's note"]


def test_flags_note_that_matches_only_sibling_title():
    tasks = [
        {"id": "t-1", "title": "Four ideological tensions", "note": "Journeys for cocaine and meth and mdma lens openings with careful detail here, covering every companion route and each signature ending in turn."},
        {"id": "t-2", "title": "Cocaine meth mdma journeys", "note": "x"},
    ]
    assert lint.find_mismatches(tasks) == ["t-1: note shares no word with its title but 4 with t-2's title"]


def test_clean_roadmap_passes():
    tasks = [{"id": "t-1", "title": "Build the gallery grid", "note": "Gallery grid built with responsive columns and keyboard navigation support."}]
    assert lint.find_mismatches(tasks) == []


def test_main_exit_codes(tmp_path):
    d = tmp_path / "projects" / "demo"
    d.mkdir(parents=True)
    (d / "roadmap.yaml").write_text("project: demo\ntasks:\n- id: t-1\n  title: Gallery\n  note: short\n")
    assert lint.main(tmp_path) == 0
