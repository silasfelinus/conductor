import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_WORKER = ROOT / "scripts" / "run_worker.py"


# run_worker.py was rewritten (conductor #254) from a task-claiming worker into a
# deterministic, read-only healthcheck: real task execution is now session-driven
# from ChatGPT/Claude via their GitHub connectors, and the script only verifies the
# queue plumbing. These tests pin that contract so the script can never quietly grow
# back the ability to mutate task status or rewrite roadmap files.


def test_worker_script_does_not_mutate_task_status():
    text = RUN_WORKER.read_text()

    # None of the old lifecycle-mutation surface should exist any more.
    for forbidden in (
        "def claim_task",
        "def set_task_status",
        "def write_roadmap",
        "_run_worker_task_status",
    ):
        assert forbidden not in text, f"{forbidden!r} reintroduced into read-only healthcheck"


def test_worker_script_only_loads_roadmaps_never_writes_them():
    text = RUN_WORKER.read_text()

    # It reads roadmaps to build the queue summary...
    assert "def load_roadmaps" in text
    # ...but must never serialize YAML back out (that would mean rewriting a roadmap).
    for serializer in ("yaml.dump", "yaml.safe_dump", ".dump("):
        assert serializer not in text, f"unexpected YAML write via {serializer!r}"
    # The only file the healthcheck writes is the transient digest, never a roadmap.
    assert text.count("write_text") == 1
    assert "digest_path.write_text" in text


def test_worker_script_exposes_the_healthcheck_surface():
    text = RUN_WORKER.read_text()

    for expected in (
        "def build_queue_summary",
        "def find_ready_task",
        "def check_dependency_resolution",
    ):
        assert expected in text, f"missing healthcheck function {expected!r}"


def test_worker_script_compiles():
    # Real smoke test: catches syntax breakage the text scrapes above would miss.
    py_compile.compile(str(RUN_WORKER), doraise=True)
