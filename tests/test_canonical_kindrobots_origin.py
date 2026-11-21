from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ORIGIN = "https://kindrobots.org"
RETIRED_ORIGIN = "https://kind-robots.vercel.app"

# These are executable production callers/configuration, not historical notes.
OPERATIONAL_PATHS = (
    ".github/workflows/auto-art-generate.yml",
    ".github/workflows/daily-digest.yml",
    ".github/workflows/sync-kind-robots-projection.yml",
    ".github/workflows/repair-failed-artjobs.yml",
    "scripts/fetch_todos.py",
    "scripts/complete_todo.py",
    "scripts/sync_kind_robots_projection.py",
    "scripts/request_art.py",
    "scripts/consume_art_queue_core.py",
    "scripts/recheck_render_queue.py",
    "scripts/retire_shadow_dreams.py",
    "scripts/challenge_submit.py",
    "scripts/repair_queued_cast_prompts.py",
    "scripts/ci_janitor.py",
    "scripts/build_digest.py",
    "scripts/enrich_daily_dream_digest.py",
    "scripts/reconcile_expressions.py",
    "scripts/dream_slug_image_cleanup.py",
    "scripts/repair_dream_art.py",
    "scripts/build_conductor_summary.py",
    "scripts/apply_daily_dream_facets.py",
    "scripts/build_dream_records.py",
    "scripts/build_dream_proposal.py",
    "scripts/new_app.py",
    "ops/home-server/relay_agent.py",
    "ops/home-server/ecosystem.config.js",
    "ops/home-server/parity_migrate.py",
    "ops/home-server/lora_import_agent.py",
)


def test_operational_kindrobots_callers_do_not_use_retired_origin():
    for relative_path in OPERATIONAL_PATHS:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        assert RETIRED_ORIGIN not in text, f"retired Vercel origin remains in {relative_path}"


def test_canonical_origin_is_defined_by_shared_callers():
    shared_callers = (
        ".github/workflows/auto-art-generate.yml",
        ".github/workflows/daily-digest.yml",
        "scripts/fetch_todos.py",
        "scripts/complete_todo.py",
        "scripts/sync_kind_robots_projection.py",
        "scripts/request_art.py",
        "scripts/consume_art_queue_core.py",
        "ops/home-server/relay_agent.py",
        "ops/home-server/ecosystem.config.js",
    )
    for relative_path in shared_callers:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        assert CANONICAL_ORIGIN in text, f"canonical Kind Robots origin missing from {relative_path}"


def test_no_workflow_or_script_reintroduces_retired_origin():
    """Glob guard: a NEW workflow or script must not reach the retired host either.

    The fixed list above missed new files; worker branches re-added
    kind-robots.vercel.app three times on 2026-11-20/21 (#7722 and
    worker/prom-tactics-art-api-base-20261121-0220). The host answers
    DEPLOYMENT_PAUSED, so any caller using it silently loses art submissions.
    """
    patterns = (".github/workflows/*.yml", ".github/workflows/*.yaml", "scripts/*.py", "ops/**/*.py")
    offenders = []
    for pattern in patterns:
        for path in sorted(ROOT.glob(pattern)):
            if RETIRED_ORIGIN in path.read_text(encoding="utf-8", errors="ignore"):
                offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, f"retired Vercel origin found in: {offenders}"
