# Pitch: Art Generator Connect — conductor-driven image generation
date: 2026-06-27
project-target: kind-robots
status: awaiting-silas

## The idea
Wire conductor Worker cycles into the existing SD / ComfyUI automated pipelines
already running in kind_robots. Workers can request image generation (character
art, scene headers, coloring-book pages, etc.) by POSTing to the kind_robots
art API; the result URL is committed back to the project or stored as an
ArtImage record. No new rendering infrastructure needed — we already have it.

## Why it's worth doing
Agents currently produce text. Adding image output unlocks coloring-book PDFs,
project card art, character portraits, and storefront products — all without
Silas having to prompt anything manually. It is the multiplier for every other
creative project in the pipeline.

## Rough effort
medium

## Key integration points
- `POST /api/art/generate` (SD) or `POST /api/art/comfy` (ComfyUI) in kind_robots
- Worker calls endpoint with `{ prompt, model, width, height, projectSlug }`
- Response ArtImage id written back to project notes or Dream.artImageId
- Conductor script `scripts/request_art.py` wraps the call + polls for completion
- Auth via KR_API_TOKEN (same token used by fetch_todos.py)

## Suggested first task
Read the existing kind_robots art generation API endpoints and document their
request/response shape in `docs/art-api.md` so Workers know exactly what to send.
