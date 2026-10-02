# Evolve Rebel Button — Design Brief

date: 2026-10-02
status: draft (scaffolded via intake.py — fill in before building)
author: (assign)

## What it is

After 100 clicks the Rebel Button becomes an art reviewer: random unseen, maturity-appropriate public or owned art, 1-5 star reviews (hate it/meh/neutral/like it/love it) with optional comment, each first review earning a click and karma.

## Who it serves

Kind Robots visitors who already pressed the button 100 times, and the art library, which needs honest reactions on pieces nobody has looked at yet.

## MVP scope

- At 100 clicks (logged in) the page title, copy and main area become the reviewer; the leaderboard stays.
- One random image at a time: public art or the viewer's own, never one they have already reacted to, under the shared maturity gate (CHILD never sees mature art; mature needs the opt-in).
- Five big buttons, labelled Hate it / Meh / Neutral / Like it / Love it, with an optional comment and Skip.
- Reviews are Reactions (one per user per image; rating 1-5 kept, so scores are remembered and re-ratable).
- First review of an image: +1 click on the leaderboard record and the existing REACTION_GIVEN karma; the owner earns REACTION_RECEIVED. Re-rating earns nothing.

## Out of scope / guardrails

- No schema change, no new route or channel; the Rebel Button page stays where it is.
- Not offered to guests; reviewing needs an account.
- Mature art whose only source is the owner-gated file route is skipped for other viewers.

## Open questions

- Should reviews also surface as a per-image average on gallery cards?
- Should skipped images come back in a later visit (today skips last one visit)?
