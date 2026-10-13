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
    if not proposal:
        # Preserve the long-standing frontmatter-only/lightweight-fixture docket
        # semantics. Real authored steering proposals contain a non-empty
        # proposal-data block, which is where entropy-version recovery applies.
        return True
    seeds = proposal.get("seed_facets")
    raw_version = seeds.get("creative_entropy_version") if isinstance(seeds, dict) else 0
    try:
        version = int(raw_version or 0)
    except (TypeError, ValueError):
        return False
    if version < CREATIVE_ENTROPY_VERSION:
        return False
    fm = _frontmatter_from_text(text)
    day = str(fm.get("proposal_date") or fm.get("created") or "")
    if _v3_day(day) and proposal.get("bundle_version") != 3:
        # Preserve earlier buffered six-asset manuscripts AS FILES, but don't
        # count them as a post-cutover complete daily authoring slot. A fresh
        # 14-asset proposal for that date is allowed; neither is overwritten.
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
    five-day buffer. After entropy v2 intentionally invalidated the v0/v1 queue, those
    stale files still made the docket look full, so agent sessions stopped authoring
    while the daily builder rejected every candidate. Count only authored proposals that
    can actually build under today's creative policy.
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

    Built history still owns its date. A current-contract unbuilt proposal also owns its
    date. An obsolete steering proposal remains on disk for audit/history but must not
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


# The old six-slot Facet planner is retained verbatim for historical proposals.
# Newly authored Pacific dates get eight INDEPENDENT project Facet assignments.
try:
    from daily_dream_v3_authoring import (
        extend_brief as _extend_zuzu_brief,
        is_v3_day as _v3_day,
    )
    from daily_dream_v3_contract import validate_v3 as _validate_v3_bundle
except ModuleNotFoundError:
    from scripts.daily_dream_v3_authoring import (
        extend_brief as _extend_zuzu_brief,
        is_v3_day as _v3_day,
    )
    from scripts.daily_dream_v3_contract import validate_v3 as _validate_v3_bundle

_six_asset_build_brief = build_brief
_six_asset_validate_proposal = validate_proposal


def build_brief(day: str | None = None, catalog=None) -> dict[str, Any]:
    brief = _six_asset_build_brief(day, catalog)
    if not _v3_day(str(brief["proposal_date"])):
        return brief
    # Reuse the supplied catalog when available, otherwise fetch the same
    # registered taxonomy data the original planner already consults.
    zuzu_catalog = catalog if catalog is not None else fetch_facet_catalog()[0]
    return _extend_zuzu_brief(brief, zuzu_catalog)


def validate_proposal(proposal: Any) -> list[str]:
    errors = _six_asset_validate_proposal(proposal)
    if isinstance(proposal, dict):
        if proposal.get("bundle_version") == 3:
            errors.extend(_validate_v3_bundle(proposal))
        elif proposal.get("zuzu_assets"):
            errors.append("zuzu_assets require bundle_version 3")
    return errors


_original_render_markdown = render_markdown


def render_markdown(p: dict[str, Any], day: str) -> str:
    base = _original_render_markdown(p, day)
    if p.get("bundle_version") != 3:
        return base
    extras = p["zuzu_assets"]
    lines = [
        "## Eight additional Zuzu-world creations (independent of this Dream)",
        "",
        "These creations belong to Zuzu Gamebook or Emperor of Dust. They do NOT",
        "inherit today's original Dream vibe, location, links, or visual style.",
        "",
    ]
    for kind, titlekey in (
        ("locations", "title"), ("characters", "name"),
        ("rewards", "name"), ("scenarios", "title"),
    ):
        lines.append(f"### Zuzu {kind.title()} (2)")
        for row in extras[kind]:
            label = str(row[titlekey])
            project = str(row["project_target"])
            checkpoint = str(row["checkpoint_family"])
            lines.append(f"- **{label}** [{project} / {checkpoint}]")
            for key, val in row.items():
                if key in (titlekey, "project_target", "checkpoint_family", "choices"):
                    continue
                lines.append(f"  - {key.replace('_', ' ').title()}: {val}")
            for choice in row.get("choices") or []:
                lines.append(
                    f"  - **Choice {choice['label']}**: {choice['tradeoff']} "
                    f"Immediate: {choice['immediate_consequence']} "
                    f"Later: {choice['later_consequence']}"
                )
        lines.append("")
    anchor = "## Notes from Silas"
    if anchor not in base:
        raise ValueError("proposal template missing Notes from Silas")
    return base.replace(anchor, "\n".join(lines) + anchor, 1)


if _WRAPPER_NAME == "__main__":
    raise SystemExit(main())
