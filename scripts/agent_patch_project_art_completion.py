from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Missing patch anchor: {label}")
    return text.replace(old, new, 1)


root = Path(__file__).resolve().parents[1]

queue_path = root / "scripts/consume_art_queue.py"
queue = queue_path.read_text()
queue = replace_once(
    queue,
    '    if status != 201 or not resp or not resp.get("success"):\n',
    '    if status not in (200, 201) or not resp or not resp.get("success"):\n',
    "accept deduplicated ArtJob response",
)
queue_path.write_text(queue)

requests_path = root / "scripts/consume_art_requests.py"
requests = requests_path.read_text()
requests = replace_once(
    requests,
    'GENERIC_IMAGE_ID = re.compile(r"\\b(?:art\\s*)?image\\s*#?\\s*\\d+\\b", re.IGNORECASE)\n',
    '''GENERIC_IMAGE_ID = re.compile(r"\\b(?:art\\s*)?image\\s*#?\\s*\\d+\\b", re.IGNORECASE)
PROJECT_ASSET_NAME = re.compile(
    r"^(?P<slug>.+)-(?P<variant>icon|card|hero)\\.[a-z0-9]+$",
    re.IGNORECASE,
)
PROJECT_FIELD_BY_VARIANT = {
    "icon": "imagePath",
    "card": "cardPath",
    "hero": "heroPath",
}
''',
    "project asset metadata constants",
)

sync_helpers = '''def project_art_sync_payload(entry, art_image_id):
    """Build the Kind Robots Project cover synchronization payload when applicable.

    New missing-image reports carry explicit project metadata. Older Conductor
    project-art requests are recoverable from `{slug}-{variant}.webp`, allowing
    the existing backlog to self-heal without rewriting every historical entry.
    """
    image_path = str(entry.get("image_path") or "").strip().replace("\\\\", "/")
    source_url = str(entry.get("source_url") or "").strip()
    target_repo = str(entry.get("target_repo") or "").strip()
    explicit_slug = str(entry.get("project_slug") or "").strip()
    explicit_field = str(entry.get("project_field") or "").strip()
    basename = Path(image_path).name
    match = PROJECT_ASSET_NAME.match(basename)
    variant = str(
        entry.get("variant") or (match.group("variant") if match else "")
    ).lower()
    project_field = (
        explicit_field
        if explicit_field in PROJECT_FIELD_BY_VARIANT.values()
        else PROJECT_FIELD_BY_VARIANT.get(variant)
    )
    project_slug = explicit_slug or (match.group("slug") if match else "")

    if not project_slug or not project_field:
        return None

    project_id = entry.get("project_id")
    try:
        project_id = int(project_id) if project_id is not None else None
    except (TypeError, ValueError):
        project_id = None

    return {
        "projectId": project_id,
        "projectSlug": project_slug,
        "projectField": project_field,
        "variant": variant,
        "targetRepo": target_repo,
        "imagePath": image_path,
        "sourceUrl": source_url,
        "artImageId": int(art_image_id),
    }


def sync_project_art(entry, art_image_id):
    payload = project_art_sync_payload(entry, art_image_id)
    if not payload:
        return False

    status, response = consumer.http_json(
        "POST",
        f"{consumer.KR_BASE_URL}/api/conductor/project-art-complete",
        payload,
    )
    if status != 200 or not response or not response.get("success"):
        detail = response.get("message") if isinstance(response, dict) else response
        raise RuntimeError(f"project art sync failed: HTTP {status} {detail}")
    return True


'''
requests = replace_once(
    requests,
    "def main():\n",
    sync_helpers + "def main():\n",
    "project art completion helpers",
)
requests = replace_once(
    requests,
    '''            if warning:
                print(f"    WARNING: {warning}")
            if request.get("id"):
''',
    '''            if warning:
                print(f"    WARNING: {warning}")
            if sync_project_art(request, job["artImageId"]):
                print("    synchronized Project cover path + ArtImage relation")
            if request.get("id"):
''',
    "completion synchronization call",
)
requests_path.write_text(requests)

media_path = root / "scripts/media_direct_consumer.py"
media = media_path.read_text()
media = replace_once(
    media,
    '''        payload["targetRepo"] = _target_repo(entry, default_target_repo)
        payload["imagePath"] = _image_path(entry, default_target_repo)
        return job
''',
    '''        payload["targetRepo"] = _target_repo(entry, default_target_repo)
        payload["imagePath"] = _image_path(entry, default_target_repo)
        if entry.get("id"):
            job["idempotencyKey"] = str(entry["id"])
        if entry.get("project_slug"):
            job["projectSlug"] = str(entry["project_slug"])
        return job
''',
    "direct-media idempotency and project metadata",
)
media_path.write_text(media)

request_tests_path = root / "tests/test_consume_art_requests.py"
request_tests = request_tests_path.read_text()
request_tests += '''


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
'''
request_tests_path.write_text(request_tests)

media_tests_path = root / "tests/test_media_direct.py"
media_tests = media_tests_path.read_text()
media_tests = replace_once(
    media_tests,
    '''    entry = {
        "prompt": "a friendly robot",
        "image_path": image_path,
    }
''',
    '''    entry = {
        "id": "kind-robots-project-card-retry-2",
        "project_slug": "project-card",
        "prompt": "a friendly robot",
        "image_path": image_path,
    }
''',
    "direct-media metadata test fixture",
)
media_tests = replace_once(
    media_tests,
    '''    assert job["payload"]["targetRepo"] == "silasfelinus/kind_robots"
    assert job["payload"]["imagePath"] == canonical

    output, warning = consumer.save_result(entry, base64.b64encode(b"bytes").decode())
''',
    '''    assert job["payload"]["targetRepo"] == "silasfelinus/kind_robots"
    assert job["payload"]["imagePath"] == canonical
    assert job["idempotencyKey"] == "kind-robots-project-card-retry-2"
    assert job["projectSlug"] == "project-card"

    output, warning = consumer.save_result(entry, base64.b64encode(b"bytes").decode())
''',
    "direct-media metadata assertions",
)
media_tests_path.write_text(media_tests)

print("Applied project art retry and completion synchronization patch.")
