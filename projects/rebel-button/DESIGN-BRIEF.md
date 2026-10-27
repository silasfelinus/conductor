# Rebel Button — Design Brief

date: 2026-10-27
status: draft
author: Claude (from Silas's Todo #1324, 2026-10-26)

## What it is

Turn the Rebel Button into a playful 100-press journey: after ten presses the button moves, shrinks, hides behind walls, triggers surprise minigames (aim a cannon to break a wall, spot the real button among decoys), and at 100 offers keep pressing for a high score, rate art, share a malaria-net fundraiser post, or donate.

## Who it serves

Visitors to kindrobots.org who find the Rebel Button. It is a small, funny toy that rewards persistence, and it
ends by pointing that goodwill at the malaria-net fundraiser.

## MVP scope

1. Presses 1-10 behave as today. From 11 the button moves around its stage, shrinks in steps, and gains walls.
2. Two surprise minigames at seeded press counts:
   - a cannon you aim at an arch to destroy a wall;
   - a field of fake buttons, each with one obvious difference from the real one.
3. Press 100 opens a finale with four choices:
   - keep pressing for a high score;
   - rate art;
   - share a fundraiser post (the visitor sends it themselves);
   - donate.
4. Built on the existing `components/pages/rebel-button.vue` and `content/button.md`. Press state lives in a Pinia
   store.

## Out of scope / guardrails

- The site never posts to social media and never moves money. Share and donate open the visitor's own flows.
- No new top-level channel.
- A failed minigame never costs earned presses.

## Open questions

- Exact press counts for each minigame. The default is seeded between 11 and 99.
