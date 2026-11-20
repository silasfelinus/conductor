# Continuous production pipeline

**Silas direction, 2026-11-20 PT.** Pending CI is not a reason to stop creating independent playable content. Applies especially to paired `comet-city-academy` (Prom of Doom) and `every-villain-tactics` (Every Villain Tactics) work, and other active software projects with ready tasks.

## Production loop

1. Read Conductor priorities, human gates, task claims, and open review PRs. Handle completed red CI by fixing the existing PR; merge only completed green, reversible, non-gated changes.
2. Claim exactly **one** highest-priority independent ready task, atomically and with a collision-resistant session. Verify the roadmap claim before editing. Never take a waiting task, duplicate an owned claim, or silently override new mainline work.
3. Produce one focused *real* content/gameplay/art increment plus its regression tests. Push, set `status: review`, verify the handoff, and **open the PR immediately**. Do not end with just a branch.
4. If the PR's checks are queued/running, subscribe for completion when possible, then **immediately claim a different independent ready task**. This is safe because the previous task has been handed off in `review`; there is still only one actively claimed task. Keep gameplay, narrative, and private art requests moving, with independent branches and as little file overlap as possible.
5. Upon completed-PR activity, repair failed checks on the original branch; merge only after *every* relevant latest-head check completed green. If branches conflict, reconcile against current main without force-pushing. Then resume independent content production.
6. After merge, reconcile Conductor task state: `done` only when all its original scope has shipped and passed tests; partial nonrecurring work returns to `ready` for another iteration. Never mark a queued art request rendered or delivered.

## Guards

- **One active claim per Worker.** Review PRs can be in flight while another task is claimed; they must be tracked, revisited, and closed out. Other workers' claims and review PRs remain off-limits without ownership or explicit review assignment.
- **No passive CI-monitoring runs.** Use completion subscriptions or check latest-head CI at the next scheduled run. A queue is not a failure and `mergeable: true` is not green. A red check deserves action before expanding work on that same branch.
- **Respect dependencies and collision risk.** If the next task depends on an unmerged change or touches the same contested files, take another independent task. Do not stack changes on the old PR or manufacture fake tasks.
- **Preserve human gates.** Public publishing, deploys, billing, DNS, secrets, irreversible changes and subjective approval stay gated and unmerged, regardless of CI outcome.
- **Art and content have distinct states.** Ledger prepared, ArtJob submitted, image rendered, asset attached and user-visible final image verified are different. Likewise design concepts, playable content and tested complete routes.
- **Maintain project-specific canon.** Prom Story remains a consequential 30-day choice-driven campaign without upfront morality selection. Tactics is the separate HERO/VILLAIN grid game; both use the same 48 permanent identities and keep existing routes and save compatibility.

## Example

Ship Captain Valcourt's Tactics origin battle as a scoped PR and mark it `review`. While TypeScript, Tactics and contract checks run, claim an unclaimed Prom relationship/patrol task or a different origin/art task with no overlapping files, and implement it. On a completed CI event, fix/merge Valcourt's PR and return the still-incomplete 48-origin task to `ready`. Never claim Valcourt's same task twice or describe the pending art render as delivered.

## Report

Every run states the new code/content actually authored, PR URLs, completed versus pending checks, merge/deploy status, live task ownership and remaining counts. If eligible independent work exists, "checks pending" is not the entire output.
