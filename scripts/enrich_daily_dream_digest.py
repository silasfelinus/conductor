#!/usr/bin/env python3
"""Daily Dream digest enrichment with completed-output freshness awareness.

The implementation snapshot lives in ``enrich_daily_dream_digest_impl.py``.  This wrapper
preserves that behavior for a normal daily cycle, but stops pretending an older completed
bundle was "just built" when the builder has produced nothing new.  Stale latest output
gets its art probed and is labeled as the latest completed bundle instead.
"""
from pathlib import Path as _WrapperPath

_WRAPPER_NAME = __name__
_IMPL_PATH = _WrapperPath(__file__).with_name("enrich_daily_dream_digest_impl.py")
_IMPL_SOURCE = _IMPL_PATH.read_text(encoding="utf-8")

globals()["__name__"] = "enrich_daily_dream_digest_impl_runtime"
exec(compile(_IMPL_SOURCE, str(_IMPL_PATH), "exec"), globals(), globals())
globals()["__name__"] = _WRAPPER_NAME

_BASE_ENRICH_DIGEST = enrich_digest


def enrich_digest(
    digest: dict[str, Any],
    proposals: list[dict[str, Any]],
    *,
    today: date,
    probe_images: bool = True,
) -> dict[str, Any]:
    output = _BASE_ENRICH_DIGEST(
        digest,
        proposals,
        today=today,
        probe_images=probe_images,
    )

    completed = [proposal for proposal in proposals if proposal.get("built")]
    completed.sort(key=_completed_sort_key)
    current = completed[-1] if completed else None
    if not current:
        return output

    built_on = _built_date(current)
    # One calendar day of grace protects timezone/late-run edges and preserves the
    # existing normal-cycle contract.  Two or more days old is unambiguously not
    # "just built this cycle" and should not have its finished art hidden.
    age_days = (today - built_on).days if built_on is not None else 999
    if age_days <= 1:
        return output

    payload = proposal_payload(current, probe_images=probe_images)
    built_label = built_on.isoformat() if built_on else "an unknown date"
    payload["display_mode"] = "latest-completed"
    payload["calendar_label"] = (
        f"Latest completed bundle; built {built_label} from the "
        f"{current['proposal_date']} proposal. No newer completed bundle exists "
        f"for the {today.isoformat()} digest."
    )
    output["current_dream_output"] = payload
    output["daily_dream_output_status"] = (
        f"No new Daily Dream bundle completed for {today.isoformat()}; "
        f"latest completed output was built {built_label}."
    )
    return output


if _WRAPPER_NAME == "__main__":
    raise SystemExit(main())
