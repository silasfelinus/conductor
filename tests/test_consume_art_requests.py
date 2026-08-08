import sys
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
    """The filler default applies to engines with no native step count.

    Entries that name no engine default to krea2 (DEFAULT_ENGINE), a distilled
    8-step model — stamping the 20-step filler budget on those is what
    over-cooked the daily-dream cards on 2026-08-08. They are left unset so
    entry_to_job resolves the engine's own cadence.
    """
    entries = [
        {"image_path": "a.webp", "engine": "flux"},
        {"image_path": "b.webp", "engine": "flux", "steps": 40},
        {"image_path": "c.webp", "engine": "flux", "steps": 0},
    ]
    cr.apply_default_steps(entries, 20)
    assert entries[0]["steps"] == 20
    assert entries[1]["steps"] == 40
    assert entries[2]["steps"] == 20


def test_apply_default_steps_leaves_distilled_engines_on_their_native_cadence():
    entries = [
        {"image_path": "a.webp"},                      # no engine -> krea2
        {"image_path": "b.webp", "engine": "krea2"},
        {"image_path": "c.webp", "engine": "sdxl"},    # aliased to krea2
        {"image_path": "d.webp", "engine": "krea2", "steps": 12},
    ]
    cr.apply_default_steps(entries, 20)
    assert "steps" not in entries[0]
    assert "steps" not in entries[1]
    assert "steps" not in entries[2], "engine aliases resolve before the guard"
    assert entries[3]["steps"] == 12, "an explicit per-entry override still wins"


def test_distilled_engines_get_cfg_one_not_the_generic_default():
    """Krea 2 Turbo is trained at cfg 1; entry_to_job used a flat cfg 7 for every
    engine while resolving steps per-engine (2026-08-08)."""
    assert cr.consumer.engine_default_cfg("krea2") == 1
    assert cr.consumer.engine_default_cfg("flux2-klein") == 1
    assert cr.consumer.engine_default_cfg("sdxl") == cr.consumer.DEFAULT_CFG


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



def test_project_art_sync_payload_prefers_explicit_metadata():
    payload = cr.project_art_sync_payload(
        {
            "project_id": 42,
            "project_slug": "music-mentor",
            "project_field": "cardPath",
            "variant": "card",
            "target_repo": "silasfelinus/kind_robots",
            "image_path": "public/images/projects/music-mentor-card.webp",
            "source_url": "/images/projects/music-mentor-card.webp",
        },
        777,
    )
    assert payload == {
        "projectId": 42,
        "projectSlug": "music-mentor",
        "projectField": "cardPath",
        "variant": "card",
        "targetRepo": "silasfelinus/kind_robots",
        "imagePath": "public/images/projects/music-mentor-card.webp",
        "sourceUrl": "/images/projects/music-mentor-card.webp",
        "artImageId": 777,
    }


def test_project_art_sync_payload_infers_legacy_conductor_cover():
    payload = cr.project_art_sync_payload(
        {
            "variant": "hero",
            "target_repo": "silasfelinus/conductor",
            "image_path": "projects/images/newsfeed-hero.webp",
            "source_url": "https://raw.githubusercontent.com/silasfelinus/conductor/main/projects/images/newsfeed-hero.webp",
        },
        778,
    )
    assert payload["projectSlug"] == "newsfeed"
    assert payload["projectField"] == "heroPath"
    assert payload["artImageId"] == 778


def test_project_art_sync_payload_ignores_non_project_art():
    assert (
        cr.project_art_sync_payload(
            {
                "variant": "image",
                "image_path": "public/images/bots/ami.webp",
            },
            779,
        )
        is None
    )


def test_sync_project_art_posts_completion(monkeypatch):
    calls = []

    def fake_http_json(method, url, body=None, timeout=60):
        calls.append((method, url, body, timeout))
        return 200, {"success": True, "data": {"field": "cardPath"}}

    monkeypatch.setattr(cr.consumer, "http_json", fake_http_json)
    assert cr.sync_project_art(
        {
            "project_slug": "packmaker",
            "project_field": "cardPath",
            "variant": "card",
            "target_repo": "silasfelinus/conductor",
            "image_path": "projects/images/packmaker-card.webp",
        },
        780,
    )
    assert calls[0][0] == "POST"
    assert calls[0][1].endswith("/api/conductor/project-art-complete")
    assert calls[0][2]["artImageId"] == 780


def test_set_request_field_inserts_when_absent():
    output, changed = cr.set_request_field(
        SAMPLE, "conductor-davinci-card-2e72bbc9", "last_art_job_id", 2775
    )
    assert changed is True
    davinci_block = output.split("- id: conductor-davinci-card-2e72bbc9")[1].split("- id:")[0]
    assert "last_art_job_id: 2775" in davinci_block
    fox_block = output.split('- id: "kind-robots-fox-image-abc123"')[1]
    assert "last_art_job_id" not in fox_block
    assert "header comment that must survive" in output


def test_set_request_field_updates_existing_value():
    once, _ = cr.set_request_field(SAMPLE, "conductor-davinci-card-2e72bbc9", "last_art_job_id", 2775)
    twice, changed = cr.set_request_field(once, "conductor-davinci-card-2e72bbc9", "last_art_job_id", 2999)
    assert changed is True
    davinci_block = twice.split("- id: conductor-davinci-card-2e72bbc9")[1].split("- id:")[0]
    assert davinci_block.count("last_art_job_id:") == 1
    assert "last_art_job_id: 2999" in davinci_block


def test_set_request_field_missing_id_is_noop():
    output, changed = cr.set_request_field(SAMPLE, "nope-not-here", "last_art_job_id", 2775)
    assert changed is False
    assert output == SAMPLE


def test_record_submitted_job_writes_durable_field(tmp_path, monkeypatch):
    file = tmp_path / "art-prompts.yaml"
    file.write_text(SAMPLE)
    monkeypatch.setattr(cr, "ART_PROMPTS_FILE", file)
    assert cr.record_submitted_job("conductor-davinci-card-2e72bbc9", 2775) is True
    text = file.read_text()
    davinci_block = text.split("- id: conductor-davinci-card-2e72bbc9")[1].split("- id:")[0]
    assert "last_art_job_id: 2775" in davinci_block
    assert "status: pending" in davinci_block  # untouched by the durable-record write


def test_record_submitted_job_missing_req_id_is_noop(tmp_path, monkeypatch):
    file = tmp_path / "art-prompts.yaml"
    file.write_text(SAMPLE)
    monkeypatch.setattr(cr, "ART_PROMPTS_FILE", file)
    assert cr.record_submitted_job(None, 2775) is False
    assert file.read_text() == SAMPLE


def test_live_run_records_job_id_before_wait_and_survives_timeout(tmp_path, monkeypatch):
    """The exact conductor/t-095 gap: enqueue succeeds, wait_for_job then times
    out (or the process crashes) before the request is marked done. The ArtJob
    id must already be durably recorded on the request entry, and main() must
    exit non-zero so the calling session actually notices the failure."""
    file = tmp_path / "art-prompts.yaml"
    file.write_text(SAMPLE)
    monkeypatch.setattr(cr, "ART_PROMPTS_FILE", file)
    monkeypatch.setattr(cr, "already_satisfied", lambda entry: False)
    monkeypatch.setattr(cr.consumer, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(cr.consumer, "enqueue", lambda job_body: 2775)

    def fake_wait_for_job(job_id, timeout):
        raise RuntimeError(f"job {job_id} timed out after {timeout}s (still queued/running)")

    monkeypatch.setattr(cr.consumer, "wait_for_job", fake_wait_for_job)
    monkeypatch.setattr(sys, "argv", ["consume_art_requests.py", "--live", "--id-prefix", "conductor-davinci"])

    exit_code = cr.main()

    assert exit_code == 1
    text = file.read_text()
    davinci_block = text.split("- id: conductor-davinci-card-2e72bbc9")[1].split("- id:")[0]
    assert "last_art_job_id: 2775" in davinci_block
    assert "status: pending" in davinci_block


def test_enqueue_accepts_deduplicated_done_job(monkeypatch):
    monkeypatch.setattr(
        cr.consumer,
        "http_json",
        lambda *_args, **_kwargs: (
            200,
            {
                "success": True,
                "data": {"job": {"id": 881, "status": "DONE"}},
            },
        ),
    )
    assert cr.consumer.enqueue({"engine": "COMFY", "payload": {}}) == 881
