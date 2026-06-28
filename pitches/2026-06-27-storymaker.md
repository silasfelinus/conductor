# Pitch: Storymaker — collaborative storytelling phase 3
date: 2026-06-27
project-target: kind-robots
status: approved

## The idea
Phase 3 of Kind Robots: a full collaborative storytelling engine built on top
of Bots, Characters, Dreams, Rewards, Scenarios, and Chats already in the DB.

Two play modes:
- **Exquisite Corpse** — players take turns adding or mutating elements of a
  shared story, character, or world model. Asynchronous-first.
- **Guided Adventure** — pick a Scenario, choose an LLM narrator Bot, set
  variables, then play through a multi-stage journey with branching choices.
  Can be solo or group (async or live via chat).

At every branch point, players see preset options + a custom-input field +
the option to spend Character stats or Rewards for unusual outcomes. Along the
way they collect new Characters, Locations, and Items added to their profile
for use in future sessions. Genre remixes and rare Rewards unlock from the
existing model DB.

## Why it's worth doing
All the data models are already there. This is the experience layer that turns
Kind Robots from an admin sandbox into something players actually interact with.
It is the flagship feature that justifies the whole stack.

## Rough effort
large

## Suggested first task
Design the Storymaker session data model: what persists between turns
(participants, current narrative state, inventory changes, branch history).
Draft as `docs/storymaker-session-model.md` for Silas to review.
