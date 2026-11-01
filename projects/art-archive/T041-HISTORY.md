# art-archive/t-041 — full note history archive

This file is the archaeology index for art-archive/t-041 ("Run the first real production import of the private archive and record the result"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-041 -->
The step the whole project was for, and the one nobody filed. t-019's title reads like this task but its implementation built the --dry-run mode and the privacy audit instead; its own note says running against the real /app/private mount needed shell access the agent did not have, and it was closed anyway. t-020 then confirmed from the live site that production held 0 ArchiveEntry rows, and kind_robots#2885 recorded explicitly that no production import had been run. Nothing since has changed that, so 36 of 38 tasks are done and none of the files under /mnt/user/pc/kindrobots/private have entered the database.
FOR SILAS: with t-040 merged, this needs no shell. On kindrobots.org go to /admin/art-archive and press Dry Run. Read the report: filesScanned, the new/changed/moved/copied/unchanged/missing plan, scan issues, how many files carry Resource match evidence, and the unresolved-model count. Unresolved checkpoints and LoRAs are expected and do not block -- they are preserved as evidence and collected by t-021's backlog. If the counts look right, press Import and confirm. Every row is written isPublic=false and isMature=true; the import is idempotent, so a second run after adding missing Resources is safe.
TO CLOSE: paste the dry-run and import numbers into this note and set approved_by_human: true and status: done. Then re-open t-020's visual acceptance against the populated grid at 390/768/1280px -- its own note flags that it could only exercise the empty state. t-033 (archive preset ArtJobs hardcoding engine 'A1111' against the COMFY-only direction) is a real bug but does not block this: scanning, importing, rating, collecting, moving, and Resource matching are all independent of regeneration.

Silas explicitly directed this session to fix the private archive import rather than merely report on it. Human gate cleared for the reversible private production import; proceed through the authenticated Kind Robots admin API and record aggregate dry-run/import results without exposing private filenames or secrets.

Added an agent-safe production import runner plus GitHub Actions workflow using Conductor's existing KR_API_TOKEN secret. The first-import request marker will trigger the workflow on merge; it runs dry-run first, refuses zero-file or scanner-issue imports, performs the idempotent production import, verifies every listed ArchiveEntry remains private+mature, and logs only aggregate counts.

ROUTE UPDATE 2026-09-20: the page now lives at /art-archive, not /admin/art-archive.
kind_robots#2926 moved pages/admin/art-archive.vue to pages/art-archive.vue and
registered content/channels/admin/art-archive.md, so the Art Archive is a real Admin-
channel nav link (sort 73, between Curation Studio and LoRA Triage) instead of a URL you
had to already know. Silas, 2026-09-20: 'If the path exists, it should be a nav link in
admin channel. If I can't reach it via /art-archive if admin, you aren't fully
connected.' Every step above reads the same -- just start from the Admin channel's Art
Archive tab rather than typing a URL. Note also that merge is not deploy: production is
Alexandria/Unraid, so the controls appear once the Unraid User Script (scripts/unraid-
user-script.sh -> scripts/deploy-unraid.sh) pulls the new image. Nothing here touches
prisma/, so there is no migration in this deploy.

Session investigation 2026-09-20 (soft, no status change -- still a hard human gate
pending Alexandria deploy): both production runs that failed (workflow runs 35507938021,
35508317136, both before this investigation) hit HTTP 400 'Maximum call stack size
exceeded' from scanArchiveRoot()'s walk(). Root-caused to TWO independent stack-overflow
classes in server/utils/artArchiveScanner.ts: (1) kind_robots#2933 (already merged same
day, ~5h before the failures were diagnosed) fixed files.push(...(await walk(...)))
spreading a whole subtree's file list as call arguments -- overflows V8's argument-
spread limit on a large subtree. (2) kind_robots#2936 (opened this session) fixes the
separate, still-present issue that walk() itself is recursive per subdirectory with no
depth/cycle guard -- resolveConfined() only rejects paths that resolve OUTSIDE the root,
so an in-bounds symlink loop or a sufficiently deep tree would still overflow the call
stack even after #2933. #2936 rewrites walk() as an iterative explicit-stack traversal
and adds a regression test for the symlink-cycle case; vue-tsc/eslint/prettier-ratchet
all clean, all 14 scanner self-test assertions pass locally. NEITHER PR is deployed to
production yet -- kind_robots merge != Unraid deploy (needs a Force Update on Alexandria
per AGENTS.md). FOR SILAS: once both PRs are merged AND a Force Update has run, re-
trigger the Art Archive Production Import workflow (push a new ops/art-archive-import-
requests/*.json marker, or workflow_dispatch with mode=dry-run first) to see if the scan
now completes. If it still 400s after that, the failure is something else and needs
fresh logs.

Session 2026-09-21 (scheduled Conductor Agent run): re-triggered the Art Archive
Production Import workflow in dry-run mode (workflow_dispatch, mode=dry-run) to test
whether kind_robots#2933/#2936 (both merged 2026-09-20, scanner stack-overflow fixes)
resolved the two prior production failures. Result: the dry-run's single POST
/api/admin/art-archive/dry-run request (client-side read timeout 300s) did not return
within ~40 minutes -- far past both the client timeout and the workflow's own 30-minute
job timeout, which did not auto-cancel it; cancelled it manually via the Actions API.
General site health is fine in the same window (kindrobots.org/ and /api/health/database
both 200 in under 1.1s), so this is specific to the archive scan route, not a general
outage. Most likely explanation: the merged fixes have not reached production yet --
merge != deploy, and this task's own note already flagged that both PRs need a Force
Update on Alexandria before they take effect. If the live route is still running the
pre-#2933/#2936 code, a hang this long (rather than the earlier fast 400 stack-overflow
crash) is a plausible symptom of hitting a much larger or more deeply-nested/cyclic
subtree than the two previous failures did, without the guard that would have made it
fail fast or the iterative rewrite that would have made it finish. Not re-attempting
further live dry-runs this session -- repeated long-hanging requests against the
production archive scanner are not obviously safe to keep firing blind. FOR SILAS:
please confirm whether a Force Update has actually been run on Alexandria since
2026-09-20T23:15Z (when #2936 merged); if not, that is the next step before any further
dry-run/import attempt. If a Force Update HAS run and the hang persists, the scanner may
have a further, still-undiagnosed issue beyond #2933/#2936 and needs fresh server-side
investigation (Alexandria logs during a dry-run request) rather than another blind
client-side retry.
GATE HYGIENE 2026-09-29: the earlier approved_by_human=true referred to Silas's
explicit authorization for the reversible private import. The task later acquired a
different blocker: the scanner fixes must reach production through an Alexandria Force
Update before another live dry-run is safe. That deployment is a new outward-facing
human gate, so the CURRENT approval flag is reset to false while the prior import
authorization remains preserved above. Do not deploy or retry the production scan
until Silas clears that concrete deployment/action.

GATE TRIAGE 2026-09-30 (session 20260930T0600Z-gate-triage, requested by Silas in
session): Production now runs a build containing #2933/#2936 (kind_robots 431f499,
2026-09-29), so the Force Update blocker is cleared. Dry-run re-triggered today: run
36672365799. The single POST /api/admin/art-archive/dry-run still hit the runner's 300s
read timeout. The workflow reported green anyway because the fail step was import-only,
fixed in this PR. The blocker is now engineering: a synchronous full scan cannot finish
inside one HTTP request. Filed art-archive/t-044 (ready) to make the scan
resumable/batched. Moved this task to waiting behind it. Silas's import authorization,
preserved above, still stands for when t-044 lands.
<!-- note:end t-041 -->
