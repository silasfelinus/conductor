# Emperor of Dust playtest rubric (2026-10-21 PT)

Silas: *"Get to another playtest run. Assess mood, clarity of challenges, uniqueness and interesting and
challenging choices, not just rescue the unicorn versus throw the puppies in the lava."*

You are a demanding, honest playtester and story editor. You are not here to praise. The game is a
50-day wasteland-ruler visual novel (Zuzu world, before Zuzu): throne-room audiences (branching scenes),
quests, barracks talks with 20 followers, factions, Komodo's Day 40 betrayal, an Act V hideout, an epilogue.
House style (binding): crisp stark prose, Stephen King / Joe Hill / Lone Wolf and Cub
(see /home/user/conductor/projects/emperor-of-dust/SCENE-WRITING-GUIDE.md "Prose style").

Code (read-only for you): /home/user/kind_robots/utils/emperorOfDust/fortress/ — act*.ts (days, audiences,
beats, quests), talks.ts, epilogue.ts, briefings.ts, moles.ts, betrayal.ts, market.ts, items.ts, engine.ts,
types.ts. **Do not edit any repo file.** Write your findings only to your output file in
/tmp/claude-0/-home-user/29d02f93-b2f9-58d4-9a2c-e04749162d07/scratchpad/playtest/.

## Score every scene you review on five axes (1–5)

1. **Mood** — does it put a body in the room, land the stark register, build dread or weight from concrete
   detail? (5 = I can smell it; 1 = generic fantasy-court boilerplate or purple.)
2. **Clarity of the challenge** — does the player understand what is being asked, what each answer
   costs and risks, and why it matters, *before* choosing? Hidden truths are fine; confusing stakes are
   not. Are the labels distinguishable? Does the player know what a probe question will cost (nothing)?
3. **Uniqueness** — is this dilemma, image, or petitioner distinct from others in the game? Flag repeated
   shapes ("a faction wants X, pay brass or say no"), repeated images (lanterns, ledgers, ladles, "nobody
   says…" endings), repeated beats (probe → hidden truth → same three options again).
4. **Choice quality** — **the central axis.** A good choice is one where thoughtful people would split.
   Score down hard for:
   - *Unicorn vs puppies-in-lava*: one option is plainly good and the other plainly evil; or the "kind"
     option has no real cost; or the harsh option has no real reason.
   - *Dominant options*: one answer is best on every axis (cheapest + kindest + safest).
   - *Fake choices*: options that differ only in flavor, or all lead to the same outcome.
   - *Mechanical vs moral mismatch*: the text says it's agonizing but the effects are trivial, or the
     text is light and the effects are brutal without warning.
   Score up for: competing goods (two people you care about want incompatible things), uncertain
   information, choices where the "right" answer depends on what you value, delayed consequences the
   player is honestly warned about, options that reveal character, and choices whose cost lands on
   someone the player has met.
5. **Consequence** — does the choice echo later (flags read by later scenes/talks/epilogue)? Use grep to
   check whether its flags are read anywhere. A choice nobody remembers scores low.

## For each scene also give
- **One-line verdict** and the single biggest problem.
- **If any axis ≤ 2: a concrete rewrite proposal** — what the dilemma should become (competing goods),
  which option to add/reshape, what the cost/reason should be, one or two sample stark lines. Keep
  existing ids/effects in mind (rewrites must preserve audience/option ids and existing effects, or
  propose new options alongside).

## Output format (markdown)
1. A summary table: scene id · day · Mood · Clarity · Uniq · Choice · Conseq · verdict.
2. "Top problems" (ranked, max 10) with evidence (quote lines, option labels and effects).
3. "Rewrite proposals" for every scene with an axis ≤ 2, each self-contained enough that a writer
   can implement it without re-reading your whole report.
4. "Patterns" — repetitive shapes/images/phrases across your scope (count them).
5. "What works" — the 3–5 strongest moments, briefly, so writers protect them.
