#!/usr/bin/env bash
# checkpoint_art_state.sh "<commit message>" -- push recorded ArtJob ids to main NOW.
#
# Every Conductor art submitter writes job ids into files (ledger cells, art-prompts.yaml
# last_art_job_id, RECOVERED ledgers, ops/unrecorded-art.yaml). They only become durable on main.
# Auto Art Generate runs routinely hit their 150-minute timeout, which cancels the job before
# "Commit conductor results", so anything submitted earlier in the run was lost and rendered
# again next run (2026-11-11 PT: Ruler Hooked's 211 requests rendered ~414 times, none recorded).
# Call this right after any step that submits, before any step that waits on renders.
#
# Stages only art state, never the whole tree. Exits 1 if the push cannot land after 5 rebases.
set -uo pipefail

message="${1:-chore: checkpoint ArtJob IDs [skip ci]}"
git config user.name >/dev/null || git config user.name "conductor-bot"
git config user.email >/dev/null || git config user.email "conductor-bot@users.noreply.github.com"

paths=(projects/art-prompts.yaml projects/art-generate.yaml ops/unrecorded-art.yaml ops/art-candidates-sync.yaml)
shopt -s nullglob globstar
paths+=(projects/*/art/*.yaml projects/*/art/**/*.yaml)
existing=()
for path in "${paths[@]}"; do [ -e "$path" ] && existing+=("$path"); done
[ "${#existing[@]}" -gt 0 ] && git add -- "${existing[@]}"

if git diff --staged --quiet; then
  echo "Art state already matches main."
  exit 0
fi
git commit -q -m "$message"
for attempt in 1 2 3 4 5; do
  if git push -q origin HEAD:main; then
    echo "Checkpointed art state (attempt $attempt)."
    exit 0
  fi
  echo "Checkpoint push race (attempt $attempt), integrating newer main."
  git pull -q --rebase --autostash origin main || exit 1
  sleep $((attempt * 2))
done
echo "::error::Could not persist ArtJob ids to main."
exit 1
