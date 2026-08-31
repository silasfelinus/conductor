#!/usr/bin/env bash
# Make sure today's daily digest actually ran, and start it if it did not.
#
# This is deliberately shared by two callers with very different reliability:
#
#   * daily-digest-retry.yml  -- dedicated crons at 16:30 and 18:30 UTC
#   * hourly-conductor.yml    -- an hourly cron that also carries this check
#
# The dedicated watchdog is the right tool but it has a fatal shared-mode
# failure: it is itself a `schedule:` workflow, so when GitHub stops delivering
# scheduled events to this repo it stops running for exactly the same reason the
# digest did. That is not hypothetical. On 2026-08-31 the digest (15:30 UTC) and
# both watchdog passes (16:30, 18:30) were all undelivered, and the digest had to
# be dispatched by hand. Over 08-26..08-31 the hourly conductor cron itself fired
# only 3-5 times a day instead of 24 -- so no single schedule can be trusted, but
# a cron that fires several times a day is a far better carrier than one with two
# chances. Hourly-conductor is a second carrier, not a replacement.
#
# Safe to run repeatedly: it treats any run today (scheduled OR dispatched) as
# proof the digest fired, so a second caller minutes later is a no-op rather than
# a duplicate email.
#
# Env:
#   GH_TOKEN        required, needs actions:write on this repo
#   GITHUB_REPOSITORY  required, owner/name
#   WORKFLOW_FILE   defaults to daily-digest.yml
#   MAX_ATTEMPTS    defaults to 3
#   MIN_UTC_HOUR    defaults to 16; below this the digest is not yet overdue and
#                   the script exits quietly. The digest cron is 15:30 UTC, so
#                   an hourly carrier must not dispatch at 02:00 for a run that
#                   is not due for another thirteen hours.
set -euo pipefail

WORKFLOW_FILE="${WORKFLOW_FILE:-daily-digest.yml}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-3}"
MIN_UTC_HOUR="${MIN_UTC_HOUR:-16}"

hour="$(date -u +%-H)"
if (( hour < MIN_UTC_HOUR )); then
  echo "::notice::${hour}:00 UTC is before the ${MIN_UTC_HOUR}:00 overdue mark; digest is not late yet."
  exit 0
fi

today="$(date -u +%F)"
runs="$(
  gh api --method GET \
    "repos/${GITHUB_REPOSITORY}/actions/workflows/${WORKFLOW_FILE}/runs" \
    -f branch=main \
    -f per_page=20
)"

# Include both the primary scheduled run and any replacement dispatched by an
# earlier pass. Otherwise a later pass sees "no schedule" again and can dispatch
# a duplicate email run outside the retry cap.
run="$(
  jq -c --arg today "${today}" '
    [.workflow_runs[]
      | select(.event == "schedule" or .event == "workflow_dispatch")
      | select(.created_at | startswith($today))]
    | sort_by(.created_at)
    | last // empty
  ' <<<"${runs}"
)"

if [[ -z "${run}" ]]; then
  echo "::warning::No daily-digest run exists for ${today}; dispatching one."
  gh api --method POST \
    "repos/${GITHUB_REPOSITORY}/actions/workflows/${WORKFLOW_FILE}/dispatches" \
    -f ref=main \
    -F 'inputs[send_email]=true' \
    --silent
  exit 0
fi

run_id="$(jq -r '.id' <<<"${run}")"
status="$(jq -r '.status' <<<"${run}")"
conclusion="$(jq -r '.conclusion // ""' <<<"${run}")"
attempt="$(jq -r '.run_attempt // 1' <<<"${run}")"
run_url="$(jq -r '.html_url' <<<"${run}")"

echo "Latest digest: status=${status} conclusion=${conclusion:-pending} attempt=${attempt} ${run_url}"

if [[ "${status}" != "completed" ]]; then
  echo "::notice::The digest is still ${status}; leaving it alone."
  exit 0
fi

if [[ "${conclusion}" == "success" ]]; then
  echo "::notice::Today's digest already succeeded; no retry needed."
  exit 0
fi

# Ordinary failures and timeouts are application signals, not delivery failures.
# Retrying those only multiplies alerts and can replay committed cycle evidence.
case "${conclusion}" in
  action_required|cancelled|startup_failure|stale)
    ;;
  failure|timed_out)
    echo "::warning::Digest concluded ${conclusion} after workflow execution; leaving the application failure for investigation instead of multiplying alerts: ${run_url}"
    exit 0
    ;;
  *)
    echo "::warning::Digest conclusion '${conclusion}' is not retryable; leaving it for investigation."
    exit 0
    ;;
esac

if (( attempt >= MAX_ATTEMPTS )); then
  echo "::error::Daily digest exhausted ${MAX_ATTEMPTS} attempts: ${run_url}"
  exit 1
fi

echo "::warning::Re-running daily digest ${run_id} after ${conclusion} (attempt ${attempt}/${MAX_ATTEMPTS})."
gh api --method POST \
  "repos/${GITHUB_REPOSITORY}/actions/runs/${run_id}/rerun" \
  --silent
