# Comic Creator — Design Brief

date: 2026-10-02
status: draft (Silas-directed pitch; scope confirmation t-002 is a soft checkpoint and blocks nothing)
author: claude

## What it is

A browser comic maker for Kind Robots. Pick a page layout, drop images into panels, add Kind Robots
characters as cut-out stickers, place speech bubbles, thought bubbles and caption boxes, choose a
lettering font, and export the finished comic as PNG pages or a single PDF. Nothing in the maker calls
an LLM, so it works for every visitor, signed in or not.

Silas's pitch, 2026-10-02, verbatim: *"a comic book creator."*

## Why this one

It is the biggest open slot in the product family: the site is full of characters, scenarios and art,
and there is nowhere to *make* something with them without spending tokens. A comic is the natural
container: panels hold existing gallery art, characters supply the cast, and the Daily Dream scenarios
supply plots.

## Who it serves

Kids and families first (Silas has an 11 and a 14 year old; the first test audience is at his own
table), then anyone browsing Kind Robots who wants to make something rather than read something.

## The flow

1. **Layout.** Choose from 12 to 20 page templates (single splash, 2x2, 3-row, manga-diagonal, a
   4-koma strip, and so on). A comic is a list of pages; add, duplicate, reorder, delete.
2. **Panels.** Tap a panel to fill it: from the Kind Robots gallery (public ArtImages), from a shipped
   *Comic Pack* of backgrounds, or from an upload. Pan and zoom the image inside the panel.
3. **Cast.** Drop characters on a panel as stickers. Each character ships a small set of
   transparent-background poses (neutral, happy, surprised, sad, running), pre-generated.
4. **Words.** Speech bubble, thought bubble, shout burst, whisper, caption box and sound-effect text,
   each with a tail you drag to the speaker. Typed by the user; no generation.
5. **Export.** PNG per page, or one PDF, rendered in the browser. A "Remix from a scenario" starter
   pre-fills a 4-page outline (title, setup, twist, ending) from a Scenario's own text, authored
   statically, so there is a place to begin without a blank page.

## What exists and what does not (to be verified by t-003)

Gallery images, characters and scenarios exist in kind_robots. A canvas-based editor, a bubble set, a
sticker pack and a PDF writer do not. The editor is the work.

## Architecture

- Home is kind_robots: `/play/comics`, a Nuxt page with a Pinia `comicStore` that owns all persistence
  and no network calls beyond fetching public gallery images. Components never call APIs.
- The document is plain JSON (pages, panels, placements, bubbles) saved to IndexedDB, with a JSON
  download/upload for backup. Cloud save is a later optional task.
- Rendering is a single canvas renderer shared by the live editor, thumbnails and export, so what you
  see is what exports.
- Sticker and background packs are static files under `public/` produced by sessions with Comfy and
  committed with provenance metadata; nothing is generated at runtime.
- PDF export is client-side (a small library or a hand-rolled single-image-per-page writer).

## MVP scope

One layout family, panel image fill with pan/zoom, speech and caption bubbles, text typing, 20
character stickers, PNG export. Then: more layouts, thought/shout bubbles, PDF, scenario starters.

## Out of scope / guardrails

- No LLM or generation call in the player path.
- No publishing or public sharing in v1; export is a download.
- No user-upload moderation surface until sharing exists (uploads stay on the device).
- Fonts must be freely licensed; record each in the pack manifest.
- Additive migrations only, and only if cloud save is ever approved.

## Open questions (none block development)

1. Cloud save: wanted at all, or is device-local plus JSON backup enough?
2. Which characters get sticker packs first (the roster is large; pick the 20 with the best art)?
3. Should comics be shareable to a public gallery (a sharing/moderation decision for Silas)?
