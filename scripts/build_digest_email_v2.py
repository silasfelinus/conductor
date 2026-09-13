#!/usr/bin/env python3
"""Daily digest email renderer with a truthful stale-latest Dream heading.

The implementation snapshot lives in ``build_digest_email_v2_impl.py``.  The only overlay
here is presentation for a completed Dream that is older than the current cycle: it still
gets the art-rich cards, but it is labeled "Latest completed output" rather than either
"Previous" or "Just built".
"""
from pathlib import Path as _WrapperPath

_WRAPPER_NAME = __name__
_IMPL_PATH = _WrapperPath(__file__).with_name("build_digest_email_v2_impl.py")
_IMPL_SOURCE = _IMPL_PATH.read_text(encoding="utf-8")

globals()["__name__"] = "build_digest_email_v2_impl_runtime"
exec(compile(_IMPL_SOURCE, str(_IMPL_PATH), "exec"), globals(), globals())
globals()["__name__"] = _WRAPPER_NAME

_BASE_PROPOSAL_SECTION = proposal_section


def proposal_section(
    _heading: str,
    proposal: dict[str, Any] | None,
    cta: bool = False,
    images: list[dict[str, Any]] | None = None,
    page_link: str = "",
) -> str:
    if not proposal or str(proposal.get("display_mode") or "") != "latest-completed":
        return _BASE_PROPOSAL_SECTION(
            _heading,
            proposal,
            cta=cta,
            images=images,
            page_link=page_link,
        )

    art_rich = dict(proposal)
    art_rich["display_mode"] = "art-rich"
    rendered = _BASE_PROPOSAL_SECTION(
        _heading,
        art_rich,
        cta=cta,
        images=images,
        page_link=page_link,
    )
    rendered = rendered.replace(
        "🖼️ Previous completed output",
        "🖼️ Latest completed output",
        1,
    )
    rendered = rendered.replace(
        "this is the art-bearing output from the prior cycle.",
        "this is the most recent completed art-bearing output; no fresher bundle completed this cycle.",
        1,
    )
    return rendered


if _WRAPPER_NAME == "__main__":
    raise SystemExit(main())
