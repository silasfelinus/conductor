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
