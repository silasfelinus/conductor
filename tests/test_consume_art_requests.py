import textwrap
from pathlib import Path

import scripts.consume_art_requests as cr


SAMPLE = textwrap.dedent(
    """\
    # header comment that must survive
    images:
      - project: packmaker
        icon:
          image_path: projects/images/packmaker-icon.webp
          status: pending
          prompt: an icon
    requests:
    - id: conductor-davinci-card-2e72bbc9
      source: kind-robots-missing-image
      status: pending
      target_repo: silasfelinus/conductor
      image_path: projects/images/davinci-card.webp
      variant: card
      prompt: a portrait of davinci
    - id: "kind-robots-fox-image-abc123"
      source: kind-robots-missing-image
      status: pending
      target_repo: silasfelinus/kind_robots
      image_path: public/images/serendipity/a-fox.webp
      variant: image
      prompt: a fox
    """
)


def test_is_pending():
    assert cr.is_pending({"status": "pending"}) is True
    assert cr.is_pending({}) is True
    assert cr.is_pending({"status": "done"}) is False
    assert cr.is_pending({"status": "DONE"}) is False


def test_target_path_maps_repo_root(tmp_path, monkeypatch):
    monkeypatch.setattr(cr, "ROOT", Path("/c"))
    monkeypatch.setattr(cr, "KIND_ROBOTS_ROOT", Path("/kr"))
    monkeypatch.setattr(
        cr,
        "REPO_ROOTS",
        {"silasfelinus/conductor": Path("/c"), "silasfelinus/kind_robots": Path("/kr")},
    )
    assert cr.target_path(
        {"target_repo": "silasfelinus/conductor", "image_path": "projects/images/x.webp"}
    ) == Path("/c/projects/images/x.webp")
    assert cr.target_path(
        {"target_repo": "silasfelinus/kind_robots", "image_path": "public/y.webp"}
    ) == Path("/kr/public/y.webp")
    assert cr.target_path({"target_repo": "who/what", "image_path": "z.webp"}) == Path("/c/z.webp")


def test_load_requests(tmp_path, monkeypatch):
    file = tmp_path / "art-prompts.yaml"
    file.write_text(SAMPLE)
    monkeypatch.setattr(cr, "ART_PROMPTS_FILE", file)
    requests = cr.load_requests()
    assert [request["id"] for request in requests] == [
        "conductor-davinci-card-2e72bbc9",
        "kind-robots-fox-image-abc123",
    ]


def test_set_request_status_flips_only_target():
    output, changed = cr.set_request_status(SAMPLE, "conductor-davinci-card-2e72bbc9", "done")
    assert changed is True
    assert "status: done\n" in output
    fox_block = output.split('- id: "kind-robots-fox-image-abc123"')[1]
    assert "status: pending" in fox_block
    assert "header comment that must survive" in output
    assert "prompt: an icon" in output


def test_set_request_status_handles_quoted_id():
    output, changed = cr.set_request_status(SAMPLE, "kind-robots-fox-image-abc123", "done")
    assert changed is True
    fox_block = output.split('- id: "kind-robots-fox-image-abc123"')[1]
    assert "status: done" in fox_block
    davinci_block = output.split("- id: conductor-davinci-card-2e72bbc9")[1].split("- id:")[0]
    assert "status: pending" in davinci_block


def test_set_request_status_missing_id_is_noop():
    output, changed = cr.set_request_status(SAMPLE, "nope-not-here", "done")
    assert changed is False
    assert output == SAMPLE


def test_mark_done_writes_file(tmp_path, monkeypatch):
    file = tmp_path / "art-prompts.yaml"
    file.write_text(SAMPLE)
    monkeypatch.setattr(cr, "ART_PROMPTS_FILE", file)
    count = cr.mark_done(["conductor-davinci-card-2e72bbc9"])
    assert count == 1
    text = file.read_text()
    davinci_block = text.split("- id: conductor-davinci-card-2e72bbc9")[1].split("- id:")[0]
    assert "status: done" in davinci_block


def test_filter_by_id_prefix():
    entries = [
        {"id": "kind-robots-academy-style-preview-cubism"},
        {"id": "conductor-davinci-card-2e72bbc9"},
    ]
    assert cr.filter_by_id_prefix(entries, "kind-robots-academy-style-preview-") == [entries[0]]
    assert cr.filter_by_id_prefix(entries, None) == entries
    assert cr.filter_by_id_prefix(entries, "") == entries


def test_entry_to_job_reused_for_a_request():
    job = cr.consumer.entry_to_job(
        {"image_path": "public/images/serendipity/a-fox.webp", "prompt": "a fox", "variant": "image"}
    )
    assert job["engine"] == "COMFY"
    assert job["payload"]["promptString"] == "a fox"
    assert job["payload"]["width"] == 1024
    assert job["payload"]["height"] == 1024


def test_filler_steps_default_is_lower_than_project_lane():
    assert cr.FILLER_STEPS < cr.consumer.DEFAULT_STEPS
    assert cr.FILLER_STEPS < cr.consumer.FLUX_MODELS["dev"]["steps"]


def test_apply_default_steps_fills_only_unset():
    entries = [
        {"image_path": "a.webp"},
        {"image_path": "b.webp", "steps": 40},
        {"image_path": "c.webp", "steps": 0},
    ]
    cr.apply_default_steps(entries, 20)
    assert entries[0]["steps"] == 20
    assert entries[1]["steps"] == 40
    assert entries[2]["steps"] == 20


def test_filler_steps_reach_the_flux_workflow():
    entry = {
        "image_path": "public/images/x.webp",
        "prompt": "x",
        "variant": "image",
        "engine": "flux",
    }
    cr.apply_default_steps([entry], cr.FILLER_STEPS)
    job = cr.consumer.entry_to_job(entry)
    assert job["payload"]["steps"] == cr.FILLER_STEPS
    sampler = job["payload"]["workflow"]["52"]["inputs"]
    assert sampler["steps"] == cr.FILLER_STEPS


def test_weak_prompt_reason_blocks_legacy_image_id_fallback():
    entry = {
        "prompt": "polished web illustration for Image 529, clear subject, cohesive Kind Robots visual style, no text"
    }
    assert cr.weak_prompt_reason(entry) == "legacy generic missing-image fallback"


def test_weak_prompt_reason_blocks_named_legacy_fallback_too():
    entry = {
        "prompt": "polished web illustration for Music Mentor, clear subject, cohesive Kind Robots visual style, no text"
    }
    assert cr.weak_prompt_reason(entry) == "legacy generic missing-image fallback"


def test_weak_prompt_reason_allows_concrete_prompt():
    entry = {
        "prompt": "A singer at a warm studio microphone while a friendly companion robot traces pitch ribbons through amber light, crisp modern animation, no readable text"
    }
    assert cr.weak_prompt_reason(entry) is None
