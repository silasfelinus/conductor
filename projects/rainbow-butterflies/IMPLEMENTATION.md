# Rainbow Butterflies implementation home

**Repository:** https://github.com/silasfelinus/rainbowbutterflies

Silas created the dedicated repository on 2026-08-28. Treat it as the default implementation home for Rainbow Butterflies work produced from this Conductor project.

## Ownership boundary

Conductor remains the canonical source for roadmap state, priorities, claims, research direction, and task coordination.

The `rainbowbutterflies` repository owns implementation artifacts specific to the mission site and agent commons. It should not become a fork or reduced copy of Kind Robots.

Kind Robots remains the preferred owner for shared identity, generation, reusable creative objects, and other mature platform primitives. Kind Economy remains the owner of paid-resource accounting and any future creator/platform/mission revenue split.

## Current implementation posture

The repository is intentionally documentation-first until `t-003` specifies the agent commons and contribution protocol. Do not scaffold a standalone application merely to make progress visible. `t-003` should decide whether the resulting product is:

- a standalone deployed application using Kind Robots services;
- a separately branded frontend over Kind Robots APIs;
- a Kind Robots-hosted mission surface with protocol/adaptor code owned in the dedicated repository; or
- another architecture justified by the spec.

For `t-004` and later implementation tasks, inspect `silasfelinus/rainbowbutterflies/AGENTS.md` before writing code and open implementation PRs in that repository unless the task specifically belongs in Kind Robots, Kind Economy, or Conductor.
