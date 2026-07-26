# Design note: the `portos` dashboard tab as a second execution-runtime view

Written 2026-07-26 per `conductor/t-034` ("Pitch: kind_robots dashboard as
shared front-end for Conductor + PortOS CoS"), approved by Silas 2026-07-25.
This is a design note only — no code, no nav change, no runtime decision. It
settles the *shape* of convergence so a later runtime pitch (`conductor/t-033`,
worktree-parallel Workers, still `needs-human`) has something concrete to
target if/when it's approved. Nothing here authorizes building or deploying a
CoS-style runtime.

This session has direct read access to both sides — the `portos` tab's
current implementation in `silasfelinus/kind_robots`, and the actual
PortOS Chief-of-Staff runtime in `silasfelinus/PortOS` (`server/services/cos*.js`,
`worktreeManager.js`, `taskLearning.js`) — so the shapes below are grounded in
real code on both ends, not the docs-only comparison the 2026-07-19 pitch had
to work from.

## 1. What the `portos` tab shows today vs. what a second runtime needs

**Today** (`stores/helpers/conductorTabs.ts`, `key: 'portos'`): a stub.
Narrative text says "Add a Porto server address, validate it, and save the
user/server relationship through the proper server-entry flow once that
persistence contract is built." No live data, no runtime awareness — it's a
server-address/pairing form stub, unrelated to task execution.

**What a real second-runtime view needs**, mapped directly to PortOS CoS
primitives that already exist in `atomantic/PortOS` and this session's
`silasfelinus/PortOS` checkout:

| Dashboard need | CoS primitive it reads |
|---|---|
| Task queue depth / next-to-run | `cosJobScheduler.js` (`registerSingleJobSchedule`, `getScheduledActionReservations`, `executeScheduledJob`) — CoS's PM2-driven `dequeueNextTask` equivalent |
| Active worktrees/agents | `worktreeManager.js` `listWorktrees()`, `cosAgents.js` `getAgents()` / `getAgentsByDate()` — one row per live agent, with its worktree path and branch |
| Claim/lease state (who owns what, staleness) | `cosTaskClaim.js` (`isLeaseLive`, `getClaimOwner`, `isHeldByOther`) — the direct analog of Conductor's own `claimed_by`/`claimed_at`/`CLAIM_TTL_MINUTES`, so the same roadmap-claim UI affordance Conductor already has could render CoS claims too |
| Recent completions / outcomes | `cosAgents.js` `completeAgent()` results + `cosReports.js` |
| Model-routing / success-rate stats (CoS's `taskLearning` analog to Conductor's `LEARNING.yaml`) | `taskLearning.js` — success rates by task type feeding model choice |
| Agent feedback / health | `cosAgents.js` `getFeedbackStats()`, `cosHealthMonitor.js` |

The upgrade path is additive to the tab's existing copy: keep the
server-address/pairing flow as-is (it's a separate, already-scoped concern —
identifying *which* PortOS install to talk to), and add a second section below
it, gated on a server actually being paired, that renders the table above.
Nothing here proposes touching the pairing flow itself.

## 2. One new read-only API shape

Mirror the existing `server/api/conductor/projects.get.ts` / `prs.get.ts`
pattern exactly: a GitHub/HTTP-backed read that parses remote state into a
typed shape the tab consumes. The difference is the source — Conductor's
endpoints read *this* repo's `roadmap.yaml`/TALKBACK via the GitHub Contents
API; a PortOS-status endpoint would instead call the paired PortOS install's
own HTTP API directly (PortOS is a private-network app reachable via
Tailscale — see `PortOS/CLAUDE.md`'s trust model — not a GitHub-hosted state
file), using whatever server address the existing pairing flow already saved.

Proposed shape, `server/api/conductor/portos-status.get.ts`:

```ts
export interface PortosAgentSummary {
  agentId: string
  taskId: string | null
  taskType: string | null      // cosAgents.js extractTaskType()
  status: string                // running | completed | failed | paused
  worktreePath: string | null
  branch: string | null
  startedAt: string
  updatedAt: string
}

export interface PortosClaimSummary {
  taskId: string
  owner: string                 // getClaimOwner()
  leaseLiveUntil: string | null // isLeaseLive() expiry
  isStale: boolean
}

export interface PortosLearningSummary {
  taskType: string
  successRate: number
  sampleSize: number
  preferredModel: string | null
}

export interface PortosStatus {
  paired: boolean
  serverLabel: string | null    // from the existing pairing record
  queueDepth: number
  agents: PortosAgentSummary[]
  claims: PortosClaimSummary[]
  learning: PortosLearningSummary[]
  fetchedAt: string
}
```

Same defensive shape as `projects.get.ts`: a failed fetch (install offline,
not paired, network error) returns `{ paired: false, ... empty arrays }`
rather than a 502 that breaks the whole conductor dashboard — this tab must
degrade gracefully since PortOS is often not reachable (private network,
Tailscale-only, may not even be running).

## 3. Explicit non-goals

- Does **not** authorize building or deploying any CoS-style runtime, in this
  repo or PortOS.
- Does **not** touch the `portos` tab's existing server-address/pairing flow
  or its persistence contract — that stays exactly as scoped in the tab's
  current narrative text.
- Does **not** imply conductor's own claim protocol changes — `conductor/t-033`
  (worktree-parallel Workers) is a separate, still-`needs-human` pitch. This
  note only describes what a dashboard *would* render if that runtime (or any
  CoS-style equivalent) existed; it takes no position on whether it should.
- Stays inert: no new nav entry, no live data wiring, no route added. This is
  a reference document for whoever picks up the runtime work next, not a
  changelog of shipped behavior.

## Dependency note

Informative context for whoever picks up `conductor/t-033` — not a blocker on
it. Either can proceed independently: a runtime could be adopted without ever
building this dashboard view, and this view's shape doesn't presuppose any
particular runtime beyond "something that produces agent/queue/claim/learning
state a REST endpoint can read."
