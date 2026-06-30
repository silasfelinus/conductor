# TALKBACK.md — humboldt-scoop

Cross-agent critique log for this project. Append-only.

---

## 2026-06-29 | Reviewer → Worker | humboldt-scoop/t-002 + t-004 | pattern

**Subject:** Tasks marked `review` since June 26 with no corresponding open PR — roadmap and reality are out of sync.

**Detail:**
- t-002 ("Audit the imported site") and t-004 ("Confirm theme/plugin/upload assets") both
  show `status: review` in roadmap.yaml but no open PRs exist in the conductor repo.
- The most likely cause is that the Worker's PRs were merged (or closed) without the
  roadmap being updated to `done`.
- This makes the STATUS.md count of "in-progress" tasks unreliable.

**Suggested action:** Worker should verify whether t-002 and t-004 PRs landed and update
the roadmap to `done` (if merged) or `ready` (if they need to be redone). Reviewer to
validate next cycle and flag if still unresolved.

---

## 2026-06-30 | Reviewer → Worker | humboldt-scoop/t-002 + t-004 | response

**Decision:** merged (retroactive — PRs #14 and #19 were already merged; statuses now set to `done`)

**What was good:**
- NOTES.md (t-002) correctly limited to read-only audit with no site code changes.
- ASSET-INVENTORY.md (t-004) used a clear summary table and honestly stated what could vs. could not be verified given runtime limits (no local clone, GitHub search timeouts).
- Both deliverables flagged actionable follow-ups (missing auth keys, missing theme/plugins/DB dump) without inventing scope or creating unnecessary tasks.
- Worker self-noted runtime limitations rather than overstating confidence.

**What to improve:**
- t-002 and t-004 PRs were merged without a Reviewer session updating statuses — this left the roadmap showing "in review" work for 4+ days. The Worker should verify that Reviewer status updates occurred before closing out a cycle; if the Reviewer hasn't confirmed, the status remains a known open item.
- t-004 discovered that the business-specific site assets (theme, plugins, uploads, DB) are absent from the import. A follow-up `ready` task to collect and stage those assets would close the loop on m2, but that gate belongs to Silas since it involves real site content.

**Pattern note:** (continuation of 2026-06-29 entry above) Status sync lag between merged PRs and roadmap updates has now been confirmed as the root cause. Resolved by Reviewer directly in this cycle. Worker should not re-do this work.

---

## 2026-06-30 | Reviewer → Worker | humboldt-scoop/t-005 | response

**Decision:** merged (PR #48 — already merged and status set to `done` in roadmap)

**What was good:**
- `getenv_docker_required()` pattern is clean: accepts both plain env vars and `*_FILE` Docker secrets mounts, fails fast with a clear error message if a var is missing. This is the right approach for secret injection in Docker-based WordPress.
- Correctly removed all eight committed fallback auth key/salt strings from wp-config.php.
- Worker honestly declared the verification limitation ("static only — no local script execution") rather than overstating confidence.
- Staying in scope (wp-config.php only) when the compose.yaml write was blocked by the tool safety layer was the correct call. Scope discipline, not workaround.

**What to improve:**
- compose.yaml still passes `${WORDPRESS_AUTH_KEY:-dev-auth-key-change-me}` (and the other seven auth key/salt vars) with hardcoded fallback values. This means Docker Compose *provides* those env vars to the container, so `getenv_docker_required()` sees a value and proceeds — it cannot distinguish a real secret from a dev placeholder. Net result: `docker compose up` without real secrets starts WordPress with known-weak credentials, defeating the wp-config.php hardening. Worker should have flagged this residual gap explicitly in "Flags for Reviewer." A follow-up task (t-006) has been added to remove those fallback defaults from compose.yaml.

**Pattern note:** Worker correctly bounded scope when a write was blocked — good discipline. The missing flag is about understanding the *end-to-end* security invariant, not just the immediate file change. When hardening one layer (wp-config.php), the Worker should check whether another layer (compose.yaml) re-introduces the gap it was meant to close.

---

## 2026-06-30 | Reviewer → Worker | humboldt-scoop/t-006 | response

**Decision:** merged (PR #50 — squash-merged; status already updated to `done` in roadmap)

**What was good:**
- Correctly removed all eight `:-dev-*` fallback defaults from compose.yaml, making `${WORDPRESS_AUTH_KEY}` (and the other seven vars) reference the env var directly with no fallback. This is exactly what the task specified.
- `.env.example` improvement: added a `# Required:` comment block with a link to the WordPress secret key generator API (`https://api.wordpress.org/secret-key/1.1/salt/`). This wasn't strictly required by t-006 but genuinely helps local developers and closes a usability gap.
- Scope discipline: only touched compose.yaml and .env.example. Did not drift into wp-config.php or other files.
- Limitations honestly disclosed: KR_API_TOKEN and resolve_deps.py unavailable; Worker verified t-005 dependency manually rather than either skipping the check or pretending to run the script.

**What to improve:**
- Minor nuance worth knowing: `${VAR}` without a fallback in Docker Compose still passes an empty string to the container if the host has the variable unset (Compose logs a warning but does not fail the `docker compose up`). This means fail-fast enforcement still comes from `getenv_docker_required()` in wp-config.php detecting the empty string — not from Compose itself. The two-layer defense works correctly, but the Worker's flags did not mention this subtlety. Noting it in the "Flags for Reviewer" section would have given the Reviewer confidence that the end-to-end invariant was understood.
- No TALKBACK entry from the Worker side for this task — expected (t-006 had no challenge or disagreement), but good practice is for the Worker to at least verify the Reviewer's prior critique was addressed before closing.

**Pattern note:** Two tasks in this milestone (t-005, t-006) form a complete end-to-end hardening chain: php layer first, then compose layer. Worker correctly followed the dependency chain and addressed the exact residual gap identified in the t-005 critique. This is the intended cross-session learning flow working as designed.

---
