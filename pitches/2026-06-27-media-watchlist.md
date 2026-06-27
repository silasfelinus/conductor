# Pitch: Media Watchlist — 10+ years of consumption data, made useful
date: 2026-06-27
project-target: kind-robots
status: awaiting-silas

## The idea
Silas has kept a running text log of every book, game, movie, TV series, comic,
and podcast consumed since ~2014 (one or two years missing). Parse and import
this into a structured DB, then surface it with:
- Browse/filter views by medium, year, rating, genre
- Stats dashboards (books per year, genre breakdown, completion rate)
- Letterboxd sync for films (import/export)
- Comic Vine integration for series data (issues read, publisher, character tags)
- Tautulli pull for Plex watch history to fill gaps
- Amazon affiliate links auto-attached to purchasable items
- Optional review editor: Silas writes a short take, publishes to site

## Why it's worth doing
This is a personal knowledge base with real SEO value if the reviews go public.
Affiliate links make it passive income. The Tautulli + Letterboxd integrations
bring in richer metadata than the raw text log has, potentially surfacing
patterns Silas hasn't noticed across a decade of consumption.

## Rough effort
medium (import + UI) + ongoing (integrations)

## Suggested first task
Share the raw text log file. Worker parses a sample (first 100 entries),
identifies the format patterns, and proposes a DB schema + import script plan.
