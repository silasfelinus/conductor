# Memory Dungeon · Writer's Room

> **Current, 30 October 2026. Internal spoilers.** Start here, not in `roadmap.yaml`. Four paired character acts followed by four interlocking crossover worlds, **twelve overworlds total**. The game must never advertise the internal count to players. This page is a writing/navigation surface; links distinguish authored source from pitches.

## The thirty-second pitch

A researcher is tricked into swapping lives with fey changeling Morrow. In a dangerous fairy-tale world they meet a goblin, a pair of mermaid princesses, a terrifyingly competent headsman, and Vesper, a moth-folk cartographer whose desperate rescue betrayed vulnerable strangers. Four character stories revisit their own worlds in distorted form. Then reality comes apart: forests crawl through office cubicles, mermaid palaces flood subway stations, and Japanese-folklore refuges fold into maps that won't let anyone leave. Four protagonists return to reclaim scattered fragments of the worlds and decide what home, memory and free choice can mean after everything has collided.

## Choose how deep to read

| Reading depth | Go here | What a writer gets |
|---|---|---|
| **0. Pitch (this page)** | Stay here | Hook, cast, story order, production truth |
| **1. Story beats, 5–10 min** | [Act pitches](story/ACT-PITCHES.md) | Twelve world openings, stakes, twists, exit choices and viewpoint |
| **2. Geography, 15 min** | [Map plans](story/MAP-PLANS.md) | Reused 8×8 sites, 6×6 dungeon plans, anchored photos, crossover rules and missing map fragments |
| **3. Write a quest** | [Scene room](story/SCENE-ROOM.md) | Sample encounters, decision/payoff patterns, character knowledge, save keys, formatting and test handoff |
| **4. Endings and callbacks** | [Ending matrix](story/ENDING-MATRIX.md) | Five decisive choices, 32 core families, variant epilogues and spoiler safeguards |
| **5. Deep evidence** | [Original notes archive](archive/roadmap-2026-10-30-pre-12-world-slim.yaml) | Exact full old roadmap, prior PRs, run IDs, art receipts, task discussion |

## Quick starts for different writers

**Pitching a new encounter?** Read [one act](story/ACT-PITCHES.md), find its recurring landmark in [the map atlas](story/MAP-PLANS.md), and follow the [scene packet](story/SCENE-ROOM.md). Only then open the implementation issue. You should not need the archived roadmap.

**Expanding a particular map?** Start with [geography and immutable IDs](story/MAP-PLANS.md), follow the linked site registry in Kind Robots, and use the dark-mirror briefs only after the warm map's actual choice and saved consequence have been checked.

**Writing an ending?** Start with [the five-axis ending matrix](story/ENDING-MATRIX.md) and choose one numbered family. Read **only** the scene handoffs supporting its earned facts. Different endings require a different culminating act, not just one sentence swapped in a common epilogue.

**Researching why a decision was made?** Use the [exact archived full roadmap](archive/roadmap-2026-10-30-pre-12-world-slim.yaml) and original issue/PR references. Treat dated, superseded instructions as history rather than fresh canon.

## Canonical order

| Role and act | First version | Dark/reimagined version |
|---|---|---|
| **Act I: Earth researcher** | e01 · Briar Marches | e02 · Briar Understory |
| **Act II: Morrow** | e03 · Human Earth | e04 · Magic-broken Earth, the tide-gate choice |
| **Act III: Scylla** | e05 · Days before the sisters' landward escape | e06 · A rewritten mermaid kingdom |
| **Act IV: Vesper** | e07 · Hoshimori, their childhood home | e08 · Recursive, grotesque yōkai nightmare |

After Act IV, **e09–e12 are one connected finale**, not two more original/dark pairs: revisit Briar with **playable Pip**, Earth with Morrow, the sea with **playable Char**, and Hoshimori with Vesper. Scylla and Pip remain essential characters. Char's death in e04 is **conditional**; do not erase her witnessed death by casually switching viewpoint. She can be played in a branched future or time-displaced context with an explicit, authored causal explanation.

## What's actually built?

- **Implemented:** Briar and Dark Briar 64-site content, the paired House experiences, relevant story and Chronicle code; Hoshimori e07's **64-site warm map and 21 of 36 Red Oven rooms** in Kind Robots source. Art delivery and device QA have independent status.
- **Partially written in source:** 12-world registry and branching/recovery logic are being revised; code PR and CI must verify before claiming merged.
- **Pitch only:** e03–e06 full maps, e08 full dark playable map, and e09–e12 crossover maps; some e08 first-site briefs and several original scenes exist as **documents**, not runnable stages.
- **Not complete:** 32 distinct complete endings, four full finale maps, 15 remaining warm Oven rooms, dark Oven, all new art media, adversarial end-to-end QA.

## The source-of-truth rule

For *creative intent*, read this hub → [Act pitches](story/ACT-PITCHES.md) → world plans. For *task status*, read the concise [roadmap](roadmap.yaml). For *actual playability and save schema*, Kind Robots TypeScript, Vue, tests, and verified ArtJob/media receipts win. Historic sixteen-world design files remain **reference only** after 2026-10-30, not competing canon. Never rewrite committed event/save IDs merely to make a pitch prettier.

[View the current roadmap](roadmap.yaml) · [Original roadmap, unchanged](archive/roadmap-2026-10-30-pre-12-world-slim.yaml)
