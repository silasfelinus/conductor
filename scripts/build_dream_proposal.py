#!/usr/bin/env python3
"""Daily Dream proposal builder with stale-entropy docket recovery.

The implementation snapshot lives in ``build_dream_proposal_impl.py``.  This wrapper
keeps its public API intact while tightening docket semantics: an unbuilt proposal only
counts as runway, and only blocks another proposal for the same date, when it still
passes the CURRENT creative contract.  Older proposals remain in the backlog as history
but cannot freeze authoring after the entropy contract advances.
"""
from pathlib import Path as _WrapperPath

_WRAPPER_NAME = __name__
_IMPL_PATH = _WrapperPath(__file__).with_name("build_dream_proposal_impl.py")
_IMPL_SOURCE = _IMPL_PATH.read_text(encoding="utf-8")

globals()["__name__"] = "build_dream_proposal_impl_runtime"
exec(compile(_IMPL_SOURCE, str(_IMPL_PATH), "exec"), globals(), globals())
globals()["__name__"] = _WRAPPER_NAME


def _frontmatter_from_text(text: str) -> dict[str, Any]:
    end = text.find("\n---\n", 4)
    if not text.startswith("---\n") or end < 0:
        return {}
    value = yaml.safe_load(text[4:end])
    return value if isinstance(value, dict) else {}


def _proposal_is_current_contract(text: str) -> bool:
    proposal = _proposal_data(text)
    if not isinstance(proposal, dict):
        return False
    seeds = proposal.get("seed_facets")
    raw_version = seeds.get("creative_entropy_version") if isinstance(seeds, dict) else 0
    try:
        version = int(raw_version or 0)
    except (TypeError, ValueError):
        return False
    if version < CREATIVE_ENTROPY_VERSION:
        return False
    return not validate_proposal(proposal)


def stale_unbuilt_backlog() -> list[str]:
    """Return queued proposal dates that no longer satisfy today's contract."""
    days: list[str] = []
    for path in _files():
        if path.name.startswith("_") or path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        fm = _frontmatter_from_text(text)
        if not fm.get("proposal") or re.search(r"<!--\s*built-data", text):
            continue
        if _proposal_is_current_contract(text):
            continue
        days.append(str(fm.get("proposal_date") or fm.get("created") or path.name[:10]))
    return sorted(days)


def unbuilt_backlog() -> list[str]:
    """Current-contract proposal dates authored but not built, oldest first.

    The pre-2026-09-11 implementation counted every unbuilt markdown file toward the
    five-day buffer.  After entropy v2 intentionally invalidated the v0/v1 queue, those
    five stale files still made the docket look full, so agent sessions stopped authoring
    while the daily builder rejected every candidate.  Count only proposals that can
    actually build under today's creative policy.
    """
    days: list[str] = []
    for path in _files():
        if path.name.startswith("_") or path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        fm = _frontmatter_from_text(text)
        if not fm.get("proposal") or re.search(r"<!--\s*built-data", text):
            continue
        if not _proposal_is_current_contract(text):
            continue
        days.append(str(fm.get("proposal_date") or fm.get("created") or path.name[:10]))
    return sorted(days)


def proposal_exists_for(day: str) -> bool:
    """Treat a stale unbuilt same-day proposal as replaceable, not a duplicate.

    Built history still owns its date.  A current-contract unbuilt proposal also owns its
    date.  An obsolete steering proposal remains on disk for audit/history but must not
    prevent the current entropy policy from authoring a replacement alongside it.
    """
    for path in _files():
        text = path.read_text(encoding="utf-8")
        fm = _frontmatter_from_text(text)
        proposal_day = str(fm.get("proposal_date") or fm.get("created") or path.name[:10])
        if proposal_day != day:
            continue
        if re.search(r"<!--\s*built-data", text):
            return True
        if fm.get("proposal") and _proposal_is_current_contract(text):
            return True
    return False


def remote_proposal_for(day: str) -> str | None:
    """Remote duplicate guard with the same stale-contract semantics as local files."""
    try:
        names = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "origin/main", "--", "projects/dream-cycle/backlog"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        ).stdout
        for name in names.splitlines():
            shown = subprocess.run(
                ["git", "show", f"origin/main:{name}"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            if shown.returncode != 0:
                continue
            text = shown.stdout
            fm = _frontmatter_from_text(text)
            proposal_day = str(fm.get("proposal_date") or fm.get("created") or Path(name).name[:10])
            if proposal_day != day:
                continue
            if re.search(r"<!--\s*built-data", text):
                return Path(name).name
            if fm.get("proposal") and _proposal_is_current_contract(text):
                return Path(name).name
    except OSError:
        pass
    return None


if _WRAPPER_NAME == "__main__":
    raise SystemExit(main())
