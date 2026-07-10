# Coloring Book — Design Brief

date: 2026-07-10
status: active
author: Claude (Silas-directed session)

## What it is

A front-end coloring book app of AI-generated coloring pages inside kind_robots.
Users treat it like a normal coloring book app — pick a page, fill regions with
colors, save/share their work — plus the AI twist: the Kind Robots Kontext network
and/or a coloring-book LoRA can generate **new** pages from prompts or from existing
images (including the user's own art and the KR gallery).

This grew out of two earlier threads Silas started under different names:

- **mural-design** — its WonderLab color studio (kind_robots `/mural`, PR #135)
  already built the core interaction: clickable SVG sections, saved color swatches,
  group fills, per-section overrides, Pinia/localStorage persistence. That engine
  is the seed of this app's coloring surface; mural stays its own project, but the
  coloring tech should be shared, not duplicated.
- **digital-storefront** — the approved "Acts of Kindness coloring book" concept
  (`concepts/acts-of-kindness-coloring-book.md`) anticipated sellable coloring
  books. This project is the production line for that idea.

## Product shape (v1)

1. **Coloring surface** — open a page, tap/click regions to fill, palette
   management, undo/reset, save progress locally (account-synced later), export
   as image. Generalize the mural color-studio engine into a reusable component.
2. **Book library** — coloring pages organized into **sets** (books). Launch sets,
   per Silas: **"Kind Robots"** (generated from existing KR art assets) and
   **"Spooktacular Monster Drag Party"**. More sets follow continuously.
3. **Page generator** — users generate their own pages via Kontext
   ("convert to coloring book line art": clean black outlines, white fill regions,
   no shading) and/or a coloring-book LoRA. Free tier includes a small number of
   generations; beyond that, tokens — aligned with the KR mana/token economy,
   never a second economy. Purchasable **coloring book sets** and generator
   **tokens** are storefront items (hard-gated at the go-live step as always).
4. **Art channel tab** — the app gets a tab in the kind_robots art channel
   (`dashboardConfigs.art` in stores/helpers/dashboardHelper.ts).

## Generation pipeline (the hard part, spec'd in t-004)

Two distinct outputs matter:

- **Printable/colorable raster page** — Kontext or a FLUX coloring-book/line-art
  LoRA converts a source image (or generates from prompt) into clean line art.
  This alone is enough for print (POD) and for flood-fill raster coloring.
- **Region-fillable page** — the interactive app wants closed regions. Options,
  in evaluation order: raster flood fill on the line art directly (cheapest,
  proven by every casual coloring app), vectorize (potrace-style) to SVG regions
  to reuse the mural SVG engine, or generate region maps at creation time.
  t-004 picks the v1 approach; bias toward the cheapest thing that ships.

Every page keeps prompt/model/source metadata (generated-art rule) and each set
ships with a manifest (title, cover, page list, source attributions).

## Storefront / print-on-demand bridge

Whatever pages this app creates are digital-storefront inventory:

- **Digital**: coloring book sets sold as in-app unlocks and/or PDF downloads.
- **Physical**: print-on-demand paper coloring books assembled from the same
  sets (storefront m4 owns the POD provider relationship; this project owns
  producing print-ready pages: 300dpi-equivalent, 8.5x11, clean margins).

The **Humboldt Impropriety Society** coloring book + calendar ideas remain
archived inspiration (CONTROL.md: humboldt-impropriety-calendar was not
approved). This app is the machinery that would make an HIS book cheap to
produce if Silas ever revives it — but no HIS set gets built until he
explicitly re-approves that content. Launch sets are the two he named.

## Content rating

Launch sets are all-ages. "Spooktacular Monster Drag Party" is playful-spooky
and celebratory — glamorous monster performers, big hair, bigger boas —
kept all-ages in v1. Any mature set (HIS territory) is a separate,
Silas-approved decision with proper gating.

## Background asset generation (pre-authorized)

Silas authorized generating art assets in the background for this project:
multiple coloring book sets, app/front-end assets, icon/card/hero. Generated
art rule applies (traceable, reversible, metadata kept). Reuse kind_robots art
assets freely as source images for the Kind Robots set.
