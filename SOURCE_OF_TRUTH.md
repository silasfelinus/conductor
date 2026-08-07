# Conductor and Kind Robots source-of-truth contract

This contract applies to every agent, model, workflow, and human-facing surface that crosses the Conductor and Kind Robots repositories.

## The rule

**Conductor is the canonical coordination ledger. Kind Robots stores a materialized read projection of that ledger and owns live application state.**

There is one authority for each field. Synchronization is deliberately one-way for coordination data:

```text
Conductor repository
  project-overrides.yaml
  projects/*/roadmap.yaml
  pitches/*
          |
          | authenticated commit-stamped snapshot
          v
Kind Robots ConductorProjection table
          |
          | read-only normalized view
          v
Kind Robots For You / project planning UI
```

Human actions in Kind Robots do not mutate the projection table directly. They create Conductor task events or pitch updates. Conductor processes those writes, commits the canonical result, and the next projection sync returns that committed state to Kind Robots.

## Field ownership

### Conductor owns

- project lifecycle: `active | continuous | paused | retired | finished`;
- project coordination priority;
- roadmap milestones and tasks;
- task status, dependencies, claims, ownership, notes, and passes;
- human gates and approval bookkeeping;
- pitches and pitch status;
- coordination history and completion provenance.

`continuous` is a Conductor scheduling lifecycle: it means intentionally ongoing fallback work and does not require a distinct Kind Robots database lifecycle enum. The materialized Kind Robots `Project` remains runtime `ACTIVE` while the projection preserves the exact Conductor lifecycle.

### Kind Robots owns

- `Project.title` and user-facing description;
- channel, dashboard tab, and route placement;
- live URL and repository URL shown by the application;
- project icon, card, hero, and other artwork;
- user preferences, read/unread state, comments, and conversations;
- runtime queues, ArtJobs, deployments, payments, grants, and entitlements;
- all other application and user data.

`Project.conductorSlug` is the join key. Do not add a second cross-repository identity key.

## Presentation metadata transition

`project-overrides.yaml` historically contains `liveUrl`, `channelKey`, `tabKey`, and `repoUrl` for some projects. Those keys are deprecated as authorities.

- Do not add new presentation metadata to `project-overrides.yaml`.
- Existing values may remain temporarily as bootstrap data for a missing Kind Robots `Project` row.
- Once a Kind Robots Project record exists, its presentation fields win.
- The projection sync updates only coordination fields on an existing Project: lifecycle status, priority, `conductorSlug`, and `lastSyncedAt`.
- Moving or restyling a project in the Kind Robots UI must be implemented in Kind Robots, not copied back into Conductor.

## Projection invariants

Every accepted projection must include:

- source repository and ref;
- exact source commit SHA;
- generation timestamp;
- complete lifecycle registry;
- roadmap text keyed by project slug;
- pitch text keyed by filename;
- image content versions.

Kind Robots stores only a successfully validated snapshot. A failed sync must not replace the last known good projection.

The projection is a cache, not a peer database:

- never resolve conflicts by choosing the newest timestamp from either side;
- never write projected task state directly in Kind Robots;
- never import Kind Robots presentation fields into Conductor;
- never treat an optimistic browser update as canonical completion;
- always reconcile against the committed Conductor roadmap.

## Agent checklist

Before changing cross-repository project data, identify the owner above.

- Coordination change: update Conductor, then verify the projection sync.
- Presentation or runtime change: update Kind Robots only.
- Human decision from Kind Robots: emit a Conductor event, verify it is processed, then verify the new snapshot arrives.
- Apparent disagreement: Conductor wins for coordination fields; Kind Robots wins for presentation and application fields. Repair the projection or event path rather than editing both sides.