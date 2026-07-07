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
    assert cr.is_pending({}) is True  # default
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
    # unknown repo falls back to conductor root
    assert cr.target_path({"target_repo": "who/what", "image_path": "z.webp"}) == Path("/c/z.webp")


def test_load_requests(tmp_path, monkeypatch):
    f = tmp_path / "art-prompts.yaml"
    f.write_text(SAMPLE)
    monkeypatch.setattr(cr, "ART_PROMPTS_FILE", f)
    reqs = cr.load_requests()
    assert [r["id"] for r in reqs] == [
        "conductor-davinci-card-2e72bbc9",
        "kind-robots-fox-image-abc123",
    ]


def test_set_request_status_flips_only_target():
    out, changed = cr.set_request_status(SAMPLE, "conductor-davinci-card-2e72bbc9", "done")
    assert changed is True
    # the davinci request is now done
    assert "status: done\n" in out
    # the fox request is untouched (still pending)
    fox_block = out.split('- id: "kind-robots-fox-image-abc123"')[1]
    assert "status: pending" in fox_block
    # the header comment and images: prompt survive
    assert "header comment that must survive" in out
    assert "prompt: an icon" in out


def test_set_request_status_handles_quoted_id():
    out, changed = cr.set_request_status(SAMPLE, "kind-robots-fox-image-abc123", "done")
    assert changed is True
    fox_block = out.split('- id: "kind-robots-fox-image-abc123"')[1]
    assert "status: done" in fox_block
    # davinci stays pending
    dv_block = out.split("- id: conductor-davinci-card-2e72bbc9")[1].split("- id:")[0]
    assert "status: pending" in dv_block


def test_set_request_status_missing_id_is_noop():
    out, changed = cr.set_request_status(SAMPLE, "nope-not-here", "done")
    assert changed is False
    assert out == SAMPLE


def test_mark_done_writes_file(tmp_path, monkeypatch):
    f = tmp_path / "art-prompts.yaml"
    f.write_text(SAMPLE)
    monkeypatch.setattr(cr, "ART_PROMPTS_FILE", f)
    n = cr.mark_done(["conductor-davinci-card-2e72bbc9"])
    assert n == 1
    text = f.read_text()
    dv_block = text.split("- id: conductor-davinci-card-2e72bbc9")[1].split("- id:")[0]
    assert "status: done" in dv_block


def test_entry_to_job_reused_for_a_request():
    # a request dict (no 'project') maps cleanly via the shared consumer
    job = cr.consumer.entry_to_job(
        {"image_path": "public/images/serendipity/a-fox.webp", "prompt": "a fox", "variant": "image"}
    )
    # default engine is Flux (a COMFY job carrying the workflow graph)
    assert job["engine"] == "COMFY"
    assert job["payload"]["promptString"] == "a fox"
    # no size on an image request => consumer's 1024x1024 default
    assert job["payload"]["width"] == 1024
    assert job["payload"]["height"] == 1024
