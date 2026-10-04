# Pitch: Kind Spot the Difference
date: 2026-10-04
project-target: new
status: awaiting-silas

## The idea
Pairs of pre-generated Kind Robots scenes that differ in five small details, found by tapping the changed spots. Hints cost nothing, and a finished set unlocks a new scene pair with a short hand-written caption about the scene.

## Why it's worth doing
It needs no LLM at runtime, so it is free for every visitor. Art plan: 12 scenes, each with an edited twin made by inpainting in ComfyUI, with difference coordinates recorded in a JSON file.

## Rough effort
medium

## Suggested first task
2 scene pairs, the tap-hit test against recorded regions, and a found counter.
