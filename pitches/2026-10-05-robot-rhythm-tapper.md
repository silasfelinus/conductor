# Pitch: Robot Rhythm Tapper
date: 2026-10-05
project-target: new
status: rejected

## The idea
A simple tap-along rhythm game where a robot drummer plays pre-composed patterns and you echo them on four big pads, with patterns lengthening as you succeed. Everything is bundled loops and sprites, so it plays offline and never touches a language model.

## Why it's worth doing
It needs no LLM at runtime, so it is free for every visitor. Art plan: 1 drummer robot sprite sheet and 4 pad skins generated ahead of time; loops authored by a session.

## Rough effort
medium

## Suggested first task
Four pads, ten echo patterns, the Web Audio scheduler, and a best-streak record.
