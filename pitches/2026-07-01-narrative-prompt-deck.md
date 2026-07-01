# Pitch: Narrative Prompt Deck
date: 2026-07-01
project-target: new
status: awaiting-silas

## The idea
A digital product: a printable (and optionally web-interactive) deck of 60 narrative prompt cards designed for writers, GMs, and collaborative fiction lovers. Each card contains a scenario seed, a character tension, a world detail, and a "twist" — structured so cards stack together to build scenes. Cards are formatted for standard playing-card print-at-home dimensions (2.5" x 3.5"). The deck ships as a PDF + a simple browser page where you can shuffle and draw digitally.

## Why it's worth doing
Silas already has domain expertise in collaborative fiction and games, and the kind_robots brand fits a "creative tools" niche well. Prompt decks are perennial sellers on Gumroad/Etsy with low support overhead — a PDF product requires no inventory and no ongoing fulfillment. The dual delivery (print PDF + web draw) makes it feel premium without heavy engineering. A second deck (sci-fi edition, horror edition) is a natural upsell with zero new infrastructure.

## Rough effort
medium

## Suggested first task
Design the card schema (JSON: seed, tension, world-detail, twist fields), write a first batch of 20 prompt entries for a "general fiction" deck, and generate a single sample card layout as a printable PDF proof using a Node script or browser-side canvas renderer.
