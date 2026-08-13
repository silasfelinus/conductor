# RENDER-BACKLOG.md

Append-only ledger of the shared ComfyUI render-queue's health (`GET
/api/art/queue/stats` on kind_robots). At least three tasks — ai-art-academy/t-004,
coloring-book/t-022, newsfeed/t-022 — had each independently re-probed the same
single-worker backlog and hand-written their own "RECHECKED &lt;date&gt;: still
PENDING=N, oldest ~Nh old" prose paragraph, the exact pattern `EGRESS-BLOCKERS.md`
(conductor/t-052) already solved for sandbox egress. This file does the same job
for the render pipeline: one append-only ledger, one stamped entry per recheck,
greppable from any task instead of re-derived each time.

**Never edit or delete a prior entry — append only, like `TALKBACK.md`.**

## How to use this

Run `python scripts/recheck_render_queue.py [--task <project>/<task-id>]` (requires
`KR_API_TOKEN`, an admin-capable machine token) before leaving a task `ready` on a
suspected render-backlog block, or before re-blocking a task that was already
flagged. It queries `GET {KR_BASE_URL}/api/art/queue/stats` and appends one
timestamped summary — `queueDepth.PENDING`, `oldestPending` age, the window's
DONE-vs-newly-PENDING throughput, and a breakdown of `recentFailed` error
signatures — below.

A `growing`/`draining`/`healthy` classification here does **not** by itself change
any task's status — the agent that ran the recheck still applies the normal
Failure-triage rules (`AGENTS.md`) to the task it's unblocking. Per the "Blocker
discipline" convention already used in `ai-art-academy/docs/continuous-improvement-checklist.md`:
do not re-probe when this ledger already has a recent entry with the same
signature — recheck only when enough time has passed that the backlog could
plausibly have moved, or when a materially different signal (a fix landing, a
relay restart, a Silas confirmation) suggests it might have.

## Log

## 2026-07-26T16:15:00Z | conductor/t-081 | growing
queueDepth: PENDING=135, RUNNING=1, DONE=1546, FAILED=62 (all-time). oldestPending:
id=2017, age=191547s (~53.2h), engine=COMFY. windowThroughput (24h): DONE=37,
newly PENDING=133 — backlog still growing, not draining (consistent with every
prior recheck on t-004/coloring-book-t-022/newsfeed-t-022 since 2026-07-24).
recentFailed (last 25, all attempts=3/exhausted): 24/25 = generic "ComfyUI
reported a workflow error" (kind_robots-side detail unavailable — see
conductor/t-080, PR #1137, merged 2026-07-26T12:22:29Z, which added
`describe_comfy_error()` to preserve real node/exception detail for *future*
failures); 1/25 = connection-refused to `http://127.0.0.1:8188` (WinError 10061,
job 2373, updatedAt 15:33:14Z). NOTE: the most recent workflow-error failures in
this same batch (jobs 2368-2372, updatedAt 15:27-15:33Z) still carry the old
generic string, ~3 hours after PR #1137 merged — see conductor/t-082 (home relay
likely hasn't restarted to pick up the fix yet).

## 2026-07-26T20:03:36Z | ai-art-academy/t-010 | growing
queueDepth: PENDING=114, RUNNING=2, DONE=1578, FAILED=62, CANCELLED=765 (all-time). oldestPending: id=2017, age=205416s (~57.1h), engine=COMFY. windowThroughput (24h): PENDING=112, RUNNING=2, DONE=58, FAILED=43. recentFailed (last 25): 24/25 = generic workflow error (no node/exception detail forwarded); 1/25 = connection-refused to ComfyUI.

## 2026-07-26T20:09:58Z | growing
queueDepth: PENDING=115, RUNNING=2, DONE=1578, FAILED=62, CANCELLED=765 (all-time). oldestPending: id=2017, age=205798s (~57.2h), engine=COMFY. windowThroughput (24h): PENDING=113, RUNNING=2, DONE=56, FAILED=43. recentFailed (last 25): 24/25 = generic workflow error (no node/exception detail forwarded); 1/25 = connection-refused to ComfyUI.

## 2026-07-27T00:06:03Z | ai-art-academy/t-010 | growing
queueDepth: PENDING=144, RUNNING=1, DONE=1645, CANCELLED=765 (all-time). oldestPending: id=2017, age=219963s (~61.1h), engine=COMFY. windowThroughput (24h): PENDING=142, RUNNING=1, DONE=34. recentFailed: none.

## 2026-07-27T02:05:55Z | ai-art-academy/t-004 | growing
queueDepth: PENDING=112, RUNNING=1, DONE=1699, CANCELLED=765 (all-time). oldestPending: id=2017, age=227155s (~63.1h), engine=COMFY. windowThroughput (24h): PENDING=110, RUNNING=1, DONE=54. recentFailed: none.

## 2026-07-27T05:05:33Z | ai-art-academy/t-010 | healthy
queueDepth: DONE=1834, FAILED=2, CANCELLED=765 (all-time). oldestPending: none. windowThroughput (24h): DONE=159. recentFailed (last 2): 2/2 = generic workflow error (no node/exception detail forwarded).

## 2026-07-27T05:12:04Z | draining
queueDepth: PENDING=1, RUNNING=1, DONE=1834, FAILED=2, CANCELLED=765 (all-time). oldestPending: id=2603, age=101s (~0.0h), engine=COMFY. windowThroughput (24h): PENDING=1, RUNNING=1, DONE=157. recentFailed (last 2): 2/2 = generic workflow error (no node/exception detail forwarded).

## 2026-07-27T05:15:20Z | draining
queueDepth: PENDING=1, RUNNING=1, DONE=1834, FAILED=2, CANCELLED=765 (all-time). oldestPending: id=2603, age=298s (~0.1h), engine=COMFY. windowThroughput (24h): PENDING=1, RUNNING=1, DONE=155. recentFailed (last 2): 2/2 = generic workflow error (no node/exception detail forwarded).

## 2026-07-27T05:24:59Z | healthy
queueDepth: RUNNING=1, DONE=1835, FAILED=3, CANCELLED=765 (all-time). oldestPending: none. windowThroughput (24h): RUNNING=1, DONE=155, FAILED=1. recentFailed (last 3): 2/3 = generic workflow error (no node/exception detail forwarded); 1/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':.

## 2026-07-27T05:26:54Z | healthy
queueDepth: RUNNING=1, DONE=1835, FAILED=3, CANCELLED=765 (all-time). oldestPending: none. windowThroughput (24h): RUNNING=1, DONE=154, FAILED=1. recentFailed (last 3): 2/3 = generic workflow error (no node/exception detail forwarded); 1/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':.

## 2026-07-27T05:32:21Z | draining
queueDepth: PENDING=1, RUNNING=1, DONE=1837, FAILED=3, CANCELLED=765 (all-time). oldestPending: id=2607, age=120s (~0.0h), engine=COMFY. windowThroughput (24h): PENDING=1, RUNNING=1, DONE=155, FAILED=1. recentFailed (last 3): 2/3 = generic workflow error (no node/exception detail forwarded); 1/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':.

## 2026-07-27T05:50:31Z | healthy
queueDepth: RUNNING=1, DONE=1841, FAILED=3, CANCELLED=765 (all-time). oldestPending: none. windowThroughput (24h): RUNNING=1, DONE=159, FAILED=1. recentFailed (last 3): 2/3 = generic workflow error (no node/exception detail forwarded); 1/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':.

## 2026-07-27T06:08:52Z | draining
queueDepth: PENDING=2, RUNNING=1, DONE=1845, FAILED=3, CANCELLED=768 (all-time). oldestPending: id=2615, age=493s (~0.1h), engine=COMFY. windowThroughput (24h): PENDING=2, RUNNING=1, DONE=162, FAILED=1, CANCELLED=3. recentFailed (last 3): 2/3 = generic workflow error (no node/exception detail forwarded); 1/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':.

## 2026-07-27T06:13:48Z | draining
queueDepth: PENDING=2, RUNNING=1, DONE=1846, FAILED=3, CANCELLED=769 (all-time). oldestPending: id=2620, age=211s (~0.1h), engine=COMFY. windowThroughput (24h): PENDING=2, RUNNING=1, DONE=163, FAILED=1, CANCELLED=4. recentFailed (last 3): 2/3 = generic workflow error (no node/exception detail forwarded); 1/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':.

## 2026-07-27T09:06:42Z | healthy
queueDepth: DONE=1920, FAILED=5, CANCELLED=771 (all-time). oldestPending: none. windowThroughput (24h): DONE=214, FAILED=3, CANCELLED=6. recentFailed (last 5): 3/5 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/5 = generic workflow error (no node/exception detail forwarded).

## 2026-07-27T14:00:48Z | draining
queueDepth: PENDING=7, RUNNING=1, DONE=1921, FAILED=5, CANCELLED=771 (all-time). oldestPending: id=2699, age=2093s (~0.6h), engine=COMFY. windowThroughput (24h): PENDING=7, RUNNING=1, DONE=199, FAILED=3, CANCELLED=6. recentFailed (last 5): 3/5 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/5 = generic workflow error (no node/exception detail forwarded).

## 2026-07-27T17:07:30Z | draining
queueDepth: PENDING=12, RUNNING=1, DONE=1921, FAILED=6, CANCELLED=771 (all-time). oldestPending: id=2700, age=12795s (~3.6h), engine=COMFY. windowThroughput (24h): PENDING=12, RUNNING=1, DONE=179, FAILED=4, CANCELLED=6. recentFailed (last 6): 3/6 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/6 = generic workflow error (no node/exception detail forwarded); 1/6 = ComfyUI image job timed out after 1800.0s.

## 2026-07-27T17:12:20Z | ai-art-academy/t-035 | draining
queueDepth: PENDING=12, RUNNING=1, DONE=1921, FAILED=6, CANCELLED=771 (all-time). oldestPending: id=2700, age=13086s (~3.6h), engine=COMFY. windowThroughput (24h): PENDING=12, RUNNING=1, DONE=179, FAILED=4, CANCELLED=6. recentFailed (last 6): 3/6 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/6 = generic workflow error (no node/exception detail forwarded); 1/6 = ComfyUI image job timed out after 1800.0s.

## 2026-07-28T03:08:17Z | healthy
queueDepth: DONE=1956, FAILED=5, CANCELLED=771 (all-time). oldestPending: none. windowThroughput (24h): DONE=145, FAILED=3, CANCELLED=6. recentFailed (last 5): 3/5 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/5 = generic workflow error (no node/exception detail forwarded).

## 2026-07-28T06:06:53Z | healthy
queueDepth: DONE=1957, FAILED=5, CANCELLED=771 (all-time). oldestPending: none. windowThroughput (24h): DONE=111, FAILED=1, CANCELLED=2. recentFailed (last 5): 3/5 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/5 = generic workflow error (no node/exception detail forwarded).

## 2026-07-28T15:11:56Z | healthy
queueDepth: DONE=1991, FAILED=9, CANCELLED=773 (all-time). oldestPending: none. windowThroughput (24h): DONE=56, FAILED=4, CANCELLED=2. recentFailed (last 9): 5/9 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/9 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'318'; 2/9 = generic workflow error (no node/exception detail forwarded).

## 2026-07-29T06:05:43Z | healthy
queueDepth: DONE=2042, FAILED=7, CANCELLED=774 (all-time). oldestPending: none. windowThroughput (24h): DONE=83, FAILED=5, CANCELLED=2. recentFailed (last 7): 5/7 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/7 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'318'.

## 2026-07-29T16:05:30Z | healthy
queueDepth: DONE=2061, FAILED=7, CANCELLED=774 (all-time). oldestPending: none. windowThroughput (24h): DONE=67, FAILED=1. recentFailed (last 7): 5/7 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/7 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'318'.

## 2026-07-29T16:08:45Z | healthy
queueDepth: RUNNING=1, DONE=2062, FAILED=7, CANCELLED=774 (all-time). oldestPending: none. windowThroughput (24h): RUNNING=1, DONE=68, FAILED=1. recentFailed (last 7): 5/7 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 2/7 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'318'.

## 2026-07-29T21:04:48Z | draining
queueDepth: PENDING=6, RUNNING=1, DONE=2073, CANCELLED=774 (all-time). oldestPending: id=2621, age=226356s (~62.9h), engine=COMFY. windowThroughput (24h): PENDING=1, DONE=61. recentFailed: none.

## 2026-08-05T04:07:24Z | growing
queueDepth: PENDING=3130, RUNNING=1, DONE=3651, FAILED=51, CANCELLED=789 (all-time). oldestPending: id=4492, age=280071s (~77.8h), engine=COMFY. windowThroughput (24h): PENDING=2744, DONE=1. recentFailed (last 25): 16/25 = connection-refused to ComfyUI; 3/25 = ComfyUI image job timed out after 1800.0s; 1/25 = complete(4329) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4328) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4327) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4304) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4270) failed: HTTP 500 Database operation failed: 
Invalid `prisma.facetArtImage.deleteMany()` invocation:


Tr; 1/25 = complete(4265) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction.

## 2026-08-05T04:27:06Z | growing
queueDepth: PENDING=3127, RUNNING=1, DONE=3654, FAILED=51, CANCELLED=789 (all-time). oldestPending: id=4495, age=281247s (~78.1h), engine=COMFY. windowThroughput (24h): PENDING=2744, DONE=1. recentFailed (last 25): 16/25 = connection-refused to ComfyUI; 3/25 = ComfyUI image job timed out after 1800.0s; 1/25 = complete(4329) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4328) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4327) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4304) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4270) failed: HTTP 500 Database operation failed: 
Invalid `prisma.facetArtImage.deleteMany()` invocation:


Tr; 1/25 = complete(4265) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction.

## 2026-08-05T05:28:47Z | growing
queueDepth: PENDING=3120, RUNNING=1, DONE=3660, FAILED=52, CANCELLED=789 (all-time). oldestPending: id=4502, age=284932s (~79.1h), engine=COMFY. windowThroughput (24h): PENDING=2744, DONE=1. recentFailed (last 25): 15/25 = connection-refused to ComfyUI; 3/25 = ComfyUI image job timed out after 1800.0s; 1/25 = complete(4497) failed: HTTP 500 Database operation failed: 
Invalid `prisma.facetArtImage.deleteMany()` invocation:


Tr; 1/25 = complete(4329) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4328) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4327) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4304) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4270) failed: HTTP 500 Database operation failed: 
Invalid `prisma.facetArtImage.deleteMany()` invocation:


Tr; 1/25 = complete(4265) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction.

## 2026-08-05T08:28:50Z | growing
queueDepth: PENDING=3102, RUNNING=2, DONE=3677, FAILED=52, CANCELLED=789 (all-time). oldestPending: id=4520, age=295688s (~82.1h), engine=COMFY. windowThroughput (24h): PENDING=2744. recentFailed (last 25): 15/25 = connection-refused to ComfyUI; 3/25 = ComfyUI image job timed out after 1800.0s; 1/25 = complete(4497) failed: HTTP 500 Database operation failed: 
Invalid `prisma.facetArtImage.deleteMany()` invocation:


Tr; 1/25 = complete(4329) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4328) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4327) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4304) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4270) failed: HTTP 500 Database operation failed: 
Invalid `prisma.facetArtImage.deleteMany()` invocation:


Tr; 1/25 = complete(4265) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction.

## 2026-08-05T08:28:57Z | growing
queueDepth: PENDING=3102, RUNNING=2, DONE=3677, FAILED=52, CANCELLED=789 (all-time). oldestPending: id=4520, age=295695s (~82.1h), engine=COMFY. windowThroughput (24h): PENDING=2744. recentFailed (last 25): 15/25 = connection-refused to ComfyUI; 3/25 = ComfyUI image job timed out after 1800.0s; 1/25 = complete(4497) failed: HTTP 500 Database operation failed: 
Invalid `prisma.facetArtImage.deleteMany()` invocation:


Tr; 1/25 = complete(4329) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4328) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4327) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction; 1/25 = complete(4304) failed: HTTP 500 Database operation failed: 
Invalid `prisma.character.update()` invocation:


Transactio; 1/25 = complete(4270) failed: HTTP 500 Database operation failed: 
Invalid `prisma.facetArtImage.deleteMany()` invocation:


Tr; 1/25 = complete(4265) failed: HTTP 500 Database operation failed: 
Invalid `prisma.artImage.update()` invocation:


Transaction.
## 2026-08-05T09:27:17Z | growing
queueDepth: PENDING=3109, RUNNING=1, DONE=3681, CANCELLED=789 (all-time). oldestPending: id=4327, age=299778s (~83.3h), engine=COMFY. windowThroughput (24h): PENDING=2744. recentFailed: none.

## 2026-08-05T14:30:40Z | growing
queueDepth: PENDING=3094, RUNNING=1, DONE=3707, CANCELLED=789 (all-time). oldestPending: id=4539, age=317314s (~88.1h), engine=COMFY. windowThroughput (24h): PENDING=2755. recentFailed: none.

## 2026-08-05T16:31:13Z | growing
queueDepth: PENDING=3081, RUNNING=1, DONE=3722, CANCELLED=789 (all-time). oldestPending: id=4554, age=324510s (~90.1h), engine=COMFY. windowThroughput (24h): PENDING=2757. recentFailed: none.

## 2026-08-05T17:38:22Z | growing
queueDepth: PENDING=3072, RUNNING=1, DONE=3731, CANCELLED=789 (all-time). oldestPending: id=4563, age=328518s (~91.3h), engine=COMFY. windowThroughput (24h): PENDING=2757. recentFailed: none.

## 2026-08-05T18:34:38Z | growing
queueDepth: PENDING=3065, RUNNING=1, DONE=3738, CANCELLED=789 (all-time). oldestPending: id=4570, age=331878s (~92.2h), engine=COMFY. windowThroughput (24h): PENDING=2757. recentFailed: none.

## 2026-08-05T20:38:50Z | growing
queueDepth: PENDING=3089, DONE=3750, FAILED=25, CANCELLED=789 (all-time). oldestPending: id=4581, age=339304s (~94.3h), engine=COMFY. windowThroughput (24h): PENDING=2792, FAILED=25. recentFailed (last 25): 25/25 = connection-refused to ComfyUI.

## 2026-08-05T22:37:25Z | coloring-book/t-022 | growing
queueDepth: PENDING=3099, RUNNING=1, DONE=3764, CANCELLED=789 (all-time). oldestPending: id=4581, age=346419s (~96.2h), engine=COMFY. windowThroughput (24h): PENDING=2802, RUNNING=1, DONE=14. recentFailed: none.

## 2026-08-05T23:26:52Z | growing
queueDepth: PENDING=3080, RUNNING=1, DONE=3783, CANCELLED=789 (all-time). oldestPending: id=4581, age=349387s (~97.1h), engine=COMFY. windowThroughput (24h): PENDING=2783, RUNNING=1, DONE=33. recentFailed: none.

## 2026-08-06T00:41:45Z | growing
queueDepth: PENDING=3069, RUNNING=1, DONE=3794, CANCELLED=789 (all-time). oldestPending: id=4581, age=353880s (~98.3h), engine=COMFY. windowThroughput (24h): PENDING=2768, RUNNING=1, DONE=44. recentFailed: none.

## 2026-08-06T04:28:03Z | draining
queueDepth: PENDING=3039, RUNNING=1, DONE=3824, CANCELLED=789 (all-time). oldestPending: id=4596, age=367422s (~102.1h), engine=COMFY. windowThroughput (24h): PENDING=13, DONE=60. recentFailed: none.

## 2026-08-06T05:31:38Z | draining
queueDepth: PENDING=3032, RUNNING=1, DONE=3833, CANCELLED=789 (all-time). oldestPending: id=4605, age=371215s (~103.1h), engine=COMFY. windowThroughput (24h): PENDING=15, DONE=60. recentFailed: none.

## 2026-08-06T07:30:00Z | draining
queueDepth: PENDING=3018, RUNNING=1, DONE=3847, CANCELLED=789 (all-time). oldestPending: id=4619, age=378283s (~105.1h), engine=COMFY. windowThroughput (24h): PENDING=15, DONE=60. recentFailed: none.

## 2026-08-06T10:30:48Z | draining
queueDepth: PENDING=2995, RUNNING=1, DONE=3078, CANCELLED=789 (all-time). oldestPending: id=4642, age=389076s (~108.1h), engine=COMFY. windowThroughput (24h): PENDING=15, DONE=57. recentFailed: none.

## 2026-08-06T18:27:43Z | growing
queueDepth: PENDING=3102, RUNNING=1, DONE=3140, CANCELLED=816 (all-time). oldestPending: id=4658, age=417616s (~116.0h), engine=COMFY. windowThroughput (24h): PENDING=125, RUNNING=1, DONE=102, CANCELLED=27. recentFailed: none.

## 2026-08-07T02:31:30Z | draining
queueDepth: PENDING=3046, RUNNING=1, DONE=3198, CANCELLED=816 (all-time). oldestPending: id=4658, age=446643s (~124.1h), engine=COMFY. windowThroughput (24h): PENDING=69, RUNNING=1, DONE=103, CANCELLED=27. recentFailed: none.

## 2026-08-07T05:27:30Z | draining
queueDepth: PENDING=3025, RUNNING=1, DONE=3219, CANCELLED=816 (all-time). oldestPending: id=4658, age=457203s (~127.0h), engine=COMFY. windowThroughput (24h): PENDING=46, RUNNING=1, DONE=124, CANCELLED=27. recentFailed: none.

## 2026-08-07T08:28:52Z | draining
queueDepth: PENDING=3002, RUNNING=1, DONE=3242, CANCELLED=816 (all-time). oldestPending: id=4658, age=468084s (~130.0h), engine=COMFY. windowThroughput (24h): PENDING=23, RUNNING=1, DONE=147, CANCELLED=27. recentFailed: none.

## 2026-08-07T08:43:53Z | draining
queueDepth: PENDING=3006, DONE=3244, CANCELLED=816 (all-time). oldestPending: id=4658, age=468986s (~130.3h), engine=COMFY. windowThroughput (24h): PENDING=27, DONE=149, CANCELLED=27. recentFailed: none.

## 2026-08-07T09:33:10Z | coloring-book/t-022 | draining
queueDepth: PENDING=3000, RUNNING=1, DONE=3249, CANCELLED=816 (all-time). oldestPending: id=4658, age=471943s (~131.1h), engine=COMFY. windowThroughput (24h): PENDING=21, RUNNING=1, DONE=154, CANCELLED=27. recentFailed: none.

## 2026-08-07T22:47:48Z | growing
queueDepth: PENDING=2908, DONE=3342, FAILED=1, CANCELLED=816 (all-time). oldestPending: id=4741, age=515791s (~143.3h), engine=COMFY. windowThroughput (24h): PENDING=8. recentFailed (last 1): 1/1 = complete(4659) failed: HTTP 500 Database operation failed: 
Invalid `prisma.user.findFirst()` invocation:


Database err.

## 2026-08-08T01:30:41Z | growing
queueDepth: PENDING=2882, RUNNING=1, DONE=3413, FAILED=4, CANCELLED=816 (all-time). oldestPending: id=4790, age=525453s (~146.0h), engine=COMFY. windowThroughput (24h): PENDING=51, DONE=1, FAILED=3. recentFailed (last 4): 3/4 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'1': ; 1/4 = complete(4659) failed: HTTP 500 Database operation failed: 
Invalid `prisma.user.findFirst()` invocation:


Database err.

## 2026-08-08T03:37:23Z | ai-art-academy/t-044 | growing
queueDepth: PENDING=2871, RUNNING=1, DONE=3428, FAILED=4, CANCELLED=816 (all-time). oldestPending: id=4790, age=533055s (~148.1h), engine=COMFY. windowThroughput (24h): PENDING=45, RUNNING=1, DONE=10, FAILED=3. recentFailed (last 4): 3/4 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'1': ; 1/4 = complete(4659) failed: HTTP 500 Database operation failed: 
Invalid `prisma.user.findFirst()` invocation:


Database err.

## 2026-08-08T06:34:55Z | draining
queueDepth: PENDING=2858, RUNNING=1, DONE=3452, FAILED=4, CANCELLED=816 (all-time). oldestPending: id=4790, age=543707s (~151.0h), engine=COMFY. windowThroughput (24h): PENDING=32, RUNNING=1, DONE=34, FAILED=3. recentFailed (last 4): 3/4 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'1': ; 1/4 = complete(4659) failed: HTTP 500 Database operation failed: 
Invalid `prisma.user.findFirst()` invocation:


Database err.

## 2026-08-08T08:57:58Z | growing
queueDepth: PENDING=2918, RUNNING=1, DONE=3470, FAILED=4, CANCELLED=816 (all-time). oldestPending: id=4790, age=552290s (~153.4h), engine=COMFY. windowThroughput (24h): PENDING=87, RUNNING=1, DONE=52, FAILED=3. recentFailed (last 4): 3/4 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'1': ; 1/4 = complete(4659) failed: HTTP 500 Database operation failed: 
Invalid `prisma.user.findFirst()` invocation:


Database err.

## 2026-08-08T11:30:12Z | growing
queueDepth: PENDING=2905, RUNNING=1, DONE=3488, CANCELLED=819 (all-time). oldestPending: id=4790, age=561424s (~156.0h), engine=COMFY. windowThroughput (24h): PENDING=73, RUNNING=1, DONE=70, CANCELLED=2. recentFailed: none.

## 2026-08-08T14:29:53Z | draining
queueDepth: PENDING=2899, RUNNING=1, DONE=3512, CANCELLED=819 (all-time). oldestPending: id=4790, age=572204s (~158.9h), engine=COMFY. windowThroughput (24h): PENDING=67, RUNNING=1, DONE=94, CANCELLED=2. recentFailed: none.

## 2026-08-08T21:31:13Z | coloring-book/t-022 | draining
queueDepth: PENDING=2868, RUNNING=1, DONE=3565, FAILED=1, CANCELLED=819 (all-time). oldestPending: id=4796, age=597471s (~166.0h), engine=COMFY. windowThroughput (24h): PENDING=42, DONE=142, FAILED=1, CANCELLED=2. recentFailed (last 1): 1/1 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'1': .

## 2026-08-08T23:28:55Z | draining
queueDepth: PENDING=2876, RUNNING=1, DONE=3579, CANCELLED=820 (all-time). oldestPending: id=4808, age=604506s (~167.9h), engine=COMFY. windowThroughput (24h): PENDING=62, RUNNING=1, DONE=143, CANCELLED=3. recentFailed: none.

## 2026-08-09T03:30:24Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=2848, RUNNING=1, DONE=3611, FAILED=1, CANCELLED=820 (all-time). oldestPending: id=4838, age=618927s (~171.9h), engine=COMFY. windowThroughput (24h): PENDING=64, DONE=97, FAILED=1. recentFailed (last 1): 1/1 = connection-refused to ComfyUI.

## 2026-08-09T06:35:22Z | conductor/t-109 | draining
queueDepth: PENDING=2813, RUNNING=1, DONE=3631, FAILED=9, CANCELLED=827 (all-time). oldestPending: id=4887, age=363905s (~101.1h), engine=COMFY. windowThroughput (24h): PENDING=46, DONE=96, FAILED=1, CANCELLED=7. recentFailed (last 9): 8/9 = ArtJob validation failed before claim: Art prompt rejected by the prompt contract (1 violation):
  [engine-step-mismatch; 1/9 = connection-refused to ComfyUI.

### 2026-08-09 | conductor/t-109 | the eight `engine-step-mismatch` failures, diagnosed

The `recentFailed` line above ("8/9 = ArtJob validation failed before claim ...
[engine-step-mismatch") is not a new incident, and it is not a relay problem. Full
finding, so no later session re-derives it:

- **What.** ArtJobs 4843, 4844, 4845, 4858, 4859, 4860, 4867, 4877 — enqueued
  2026-08-02..04, failed at claim 2026-08-09T04:13Z as the relay reached them.
  Error, all eight identical: `krea2 runs at roughly 12 steps or fewer; got 20`.
  Their cfg was already correct at 1 and their prompt text passes every other
  contract rule. Only the step count was stale.
- **Why.** kind_robots' prompt contract shipped 2026-08-08 and is re-applied at
  claim time to catch pre-gate backlog rows. These rows are exactly that: written
  before the fix, rejected after it. This is the "prompts made before a fixed
  problem" case, not a regression.
- **How much more.** A scan of all 2815 PENDING rows found **27** more with the
  same single defect — 7633, 7635, 7636, 7697-7701, 7895-7902, 7955-7965 — and no
  other contract violation anywhere in the backlog. Bounded, not systemic.
- **The 9th failure** (8116, A1111, resource-previews) is a refused ComfyUI
  connection: relay down at that moment, unrelated, requeue-and-forget.

Fixed by kind_robots PR #1645 (claim clamps out-of-band sampler settings to the
engine ceiling instead of failing the row; enqueue still rejects outright) and the
companion Conductor PR (`entry_to_job` holds an explicit `steps:`/`cfg:` to the same
ceilings). The 27 pending rows self-heal as they drain; the 8 failed ones were
requeued after #1645 reached production.

**Use `python scripts/scan_art_queue_sampler.py` for this class of question.**
`recheck_render_queue.py` reports the last N failures — what just broke. The scanner
pages the whole queue and answers how much more is coming, which is the number that
decided this fix (27, not 2000). Its scope is the mechanical rules only: steps and
cfg against the engine ceilings. The prompt-text rules live in kind_robots and are
deliberately not reimplemented there, so a clean run means "nothing will die on its
sampler settings", not "everything will render".

## 2026-08-09T07:06:10Z | conductor/t-109 | draining
queueDepth: PENDING=2816, RUNNING=1, DONE=3635, FAILED=1, CANCELLED=828 (all-time). oldestPending: id=4845, age=554508s (~154.0h), engine=COMFY. windowThroughput (24h): PENDING=45, DONE=96, FAILED=1, CANCELLED=8. recentFailed (last 1): 1/1 = connection-refused to ComfyUI.

### 2026-08-09 | conductor/t-109 | confirmed: the fix renders

Closing the loop on the entry above, because "requeued" is not the same as "works".

**ArtJob 4843 — one of the eight that died at claim this morning — is `DONE`,
`artImageId: 17052`, one attempt, no error.** Same row, same prompt, same graph;
the only difference is `steps: 20 → 12` and `cfg: 7 → 1`, applied by the claim
path instead of being grounds for killing it. 4844 went RUNNING right behind it.

The repair is recorded on each payload, so any of these is self-explaining later:

    samplerRepair: {repairedAt: 2026-08-09T06:54:03Z, engine: krea2, repairs: [
      payload.steps 20→12, payload.cfg 7→1, workflow.7.inputs.steps 20→12]}

One row was lost in the gap: **7633 was claimed at 06:48:00Z and killed by the old
code**, ~3 minutes before the production build finished at 06:50:49Z. Requeued with
the rest and repaired. Nothing else was in flight during that window.

`engine-step-mismatch` no longer appears anywhere in `recentFailed`. The one
remaining FAILED row is ArtJob 8116, a *different* failure — connection refused to
a hardcoded A1111 backend that nothing on the relay is serving. That is
conductor/t-110, not this.

## 2026-08-10T01:31:16Z | draining
queueDepth: PENDING=2367, RUNNING=1, DONE=3771, FAILED=3, CANCELLED=1204 (all-time). oldestPending: id=4893, age=432059s (~120.0h), engine=COMFY. windowThroughput (24h): DONE=64, FAILED=1, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-10T09:29:17Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=1574, RUNNING=1, DONE=3828, FAILED=3, CANCELLED=1948 (all-time). oldestPending: id=4893, age=460740s (~128.0h), engine=COMFY. windowThroughput (24h): DONE=67, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-10T22:28:47Z | draining
queueDepth: PENDING=1248, RUNNING=1, DONE=3917, FAILED=3, CANCELLED=2227 (all-time). oldestPending: id=4893, age=507510s (~141.0h), engine=COMFY. windowThroughput (24h): DONE=50. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-11T04:44:38Z | draining
queueDepth: PENDING=1077, RUNNING=1, DONE=3962, FAILED=3, CANCELLED=2360 (all-time). oldestPending: id=4893, age=530061s (~147.2h), engine=COMFY. windowThroughput (24h): PENDING=4, RUNNING=1, DONE=44. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-11T14:40:01Z | draining
queueDepth: PENDING=845, RUNNING=1, DONE=4035, FAILED=3, CANCELLED=2531 (all-time). oldestPending: id=4893, age=565784s (~157.2h), engine=COMFY. windowThroughput (24h): DONE=43. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-11T17:28:54Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=826, RUNNING=1, DONE=4055, FAILED=3, CANCELLED=2554 (all-time). oldestPending: id=4893, age=575918s (~160.0h), engine=COMFY. windowThroughput (24h): PENDING=9, RUNNING=1, DONE=45, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-11T20:29:19Z | draining
queueDepth: PENDING=765, RUNNING=1, DONE=4077, FAILED=3, CANCELLED=2593 (all-time). oldestPending: id=4893, age=586742s (~163.0h), engine=COMFY. windowThroughput (24h): DONE=42, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-11T23:29:01Z | draining
queueDepth: PENDING=681, RUNNING=1, DONE=4098, FAILED=3, CANCELLED=2656 (all-time). oldestPending: id=4893, age=597524s (~166.0h), engine=COMFY. windowThroughput (24h): DONE=42, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-12T00:45:09Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=642, DONE=4108, FAILED=3, CANCELLED=2686 (all-time). oldestPending: id=4893, age=602092s (~167.2h), engine=COMFY. windowThroughput (24h): DONE=42, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-12T02:31:54Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=586, RUNNING=1, DONE=4121, FAILED=3, CANCELLED=2728 (all-time). oldestPending: id=4893, age=608497s (~169.0h), engine=COMFY. windowThroughput (24h): DONE=40, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-12T03:38:58Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=554, RUNNING=1, DONE=4129, FAILED=3, CANCELLED=2752 (all-time). oldestPending: id=4893, age=612521s (~170.1h), engine=COMFY. windowThroughput (24h): DONE=40, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-12T04:28:53Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=530, DONE=4136, FAILED=3, CANCELLED=2770 (all-time). oldestPending: id=4893, age=615516s (~171.0h), engine=COMFY. windowThroughput (24h): DONE=40, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-12T06:30:18Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=470, RUNNING=1, DONE=4150, FAILED=3, CANCELLED=2815 (all-time). oldestPending: id=4893, age=622802s (~173.0h), engine=COMFY. windowThroughput (24h): DONE=25, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-12T07:29:13Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=442, RUNNING=1, DONE=4157, FAILED=3, CANCELLED=2836 (all-time). oldestPending: id=4893, age=626336s (~174.0h), engine=COMFY. windowThroughput (24h): DONE=25, CANCELLED=1. recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-12T22:28:47Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=422, RUNNING=1, DONE=4162, FAILED=3, CANCELLED=2851 (all-time). oldestPending: id=4893, age=680310s (~189.0h), engine=COMFY. windowThroughput (24h): . recentFailed (last 3): 2/3 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':; 1/3 = connection-refused to ComfyUI.

## 2026-08-13T06:32:41Z | ai-art-academy/t-044 | growing
queueDepth: PENDING=425, RUNNING=1, DONE=4162, CANCELLED=2856 (all-time). oldestPending: id=4893, age=709344s (~197.0h), engine=COMFY. windowThroughput (24h): PENDING=3, CANCELLED=2. recentFailed: none.

## 2026-08-13T08:29:51Z | ai-art-academy/t-044 | growing
queueDepth: PENDING=425, RUNNING=1, DONE=4162, CANCELLED=2856 (all-time). oldestPending: id=4893, age=716374s (~199.0h), engine=COMFY. windowThroughput (24h): PENDING=3, CANCELLED=2. recentFailed: none.

## 2026-08-13T09:28:05Z | growing
queueDepth: PENDING=425, RUNNING=1, DONE=4162, CANCELLED=2856 (all-time). oldestPending: id=4893, age=719868s (~200.0h), engine=COMFY. windowThroughput (24h): PENDING=3, CANCELLED=2. recentFailed: none.

## 2026-08-13T10:36:04Z | growing
queueDepth: PENDING=425, RUNNING=1, DONE=4162, CANCELLED=2856 (all-time). oldestPending: id=4893, age=723947s (~201.1h), engine=COMFY. windowThroughput (24h): PENDING=3, CANCELLED=2. recentFailed: none.

## 2026-08-13T16:05:34Z | ai-art-academy/t-044 | growing
queueDepth: PENDING=425, RUNNING=1, DONE=4162, CANCELLED=2856 (all-time). oldestPending: id=4893, age=743717s (~206.6h), engine=COMFY. windowThroughput (24h): PENDING=3, CANCELLED=2. recentFailed: none.

## 2026-08-13T18:35:07Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=103, RUNNING=1, DONE=4173, FAILED=2, CANCELLED=3172 (all-time). oldestPending: id=4894, age=752690s (~209.1h), engine=COMFY. windowThroughput (24h): PENDING=1, DONE=7, FAILED=2, CANCELLED=2. recentFailed (last 2): 2/2 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':.

## 2026-08-13T20:31:36Z | ai-art-academy/t-044 | draining
queueDepth: PENDING=89, RUNNING=1, DONE=4187, FAILED=2, CANCELLED=3172 (all-time). oldestPending: id=4894, age=759679s (~211.0h), engine=COMFY. windowThroughput (24h): PENDING=1, DONE=7, FAILED=2, CANCELLED=2. recentFailed (last 2): 2/2 = ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt returned HTTP 400 at http://127.0.0.1:8188: {'61':.
