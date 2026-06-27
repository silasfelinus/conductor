# Pitch: Alexa Integration — voice commands to Conductor via Unraid
date: 2026-06-27
project-target: conductor
status: awaiting-silas

## The idea
A custom Alexa skill with a unique wake phrase routes voice commands through
a lightweight relay service running on Unraid. Commands fan out to:
- Conductor task creation / status queries
- kind_robots art generation requests
- Direct LLM conversation (proxied through kind_robots)
- Quick website actions (create todo, check project status)

Relay service = a small Node/Python HTTP server on Unraid that accepts the
Alexa intent payload and calls the appropriate kind_robots or conductor API.
Auth handled by KR_API_TOKEN stored as an Unraid environment variable.

## Why it's worth doing
Silas already has the hardware (Unraid + Alexa). This turns the home assistant
into a natural-language front-end for the whole conductor system — hands-free
task logging while working, quick art requests, status checks without opening
a browser.

## Rough effort
medium

## Key pieces
1. Alexa Developer Console custom skill + invocation name
2. Unraid relay server (Node or Python, runs as a Docker container)
3. Intent handlers: create-todo, request-art, ask-llm, check-status
4. HTTPS endpoint (Unraid behind reverse proxy or ngrok for dev)

## Suggested first task
Draft the Alexa skill intent schema (5-8 intents, sample utterances) in
`docs/alexa-intent-schema.json` and the Unraid relay server skeleton.
