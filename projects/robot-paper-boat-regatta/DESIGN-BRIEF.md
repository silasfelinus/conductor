# Robot Paper Boat Regatta — Design Brief

date: 2026-10-09
status: draft v1 (written by agent; scope confirmation is the soft gate t-002)
author: Conductor agent

## What it is

A calm puzzle toy: fold a paper boat from sail, hull and cargo choices, then race it
down a pre-painted stream against simple rival boats. The race is fully deterministic
(current rules, no randomness, no model at runtime), so every outcome is explainable
and replayable. Free to play.

## Who it serves

Kids and relaxed-puzzle players on Kind Robots who like tinkering with a small number
of parts and seeing the cause and effect immediately. Sessions are 2-5 minutes.

## Creative direction

Cut-paper, watercolor stream, gentle robot mascots as rivals. Tone is cozy and
low-stakes: no timers that punish, no losing screen, a ribbon for first place.

## MVP scope (first slice)

- One stream backdrop with named current lanes (fast, slow, eddy).
- Three sail choices x three hull choices x (optional) one cargo slot.
  Each part has fixed numeric traits (speed, steadiness, load).
- Deterministic race: each lane segment applies a rule (e.g. eddy cancels speed
  below a steadiness threshold). Two scripted rivals with fixed builds.
- Replay of the race as a tick-by-tick animation from the same simulation log.
- Ribbon on first place; "try another build" loop.

## Art plan (pre-generated)

6 stream backdrops, 18 boat parts (sails/hulls/cargo), 8 rival boats. MVP needs
1 backdrop, 9 parts, 2 rivals.

## Out of scope / guardrails

- No runtime LLM, no accounts, no multiplayer, no purchases.
- Publishing the page to production kindrobots.com follows normal PR + deploy gates.

## Build plan

1. Pure simulation module + unit tests (traits, lane rules, rival builds).
2. Boat builder UI and race animation page.
3. Art wiring from the pre-generated queue.
4. Polish: sound optional, ribbon, replay link.

## Open questions

- Confirm the three-lane stream rules feel readable (soft, resolvable in play-testing).
