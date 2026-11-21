# Cthulhuquarium: human playtest checklist

For Silas, at `/play/aquarium` on kindrobots.org once the next Force Update has
deployed kind_robots #5472 and #5479. This is a handoff sheet, not a gate. It
lists what to look at and what each thing should feel like, so a verdict can
be specific. Allow 20–30 minutes on a phone and 10 on a desktop. Use a **fresh
account** for parts 1–3 and your own tank for part 4.

## 1. The first five minutes (fresh account)

- [ ] The intro plays full-screen. The text types out, a tap finishes the line,
      and a second tap moves on. Charlotte's and Wilbur's hero portraits appear.
- [ ] The tutorial beats (buy a free fish, Feed) drop to the small sheet so the
      buttons stay reachable. The intro's last line from Charlotte promises "floors below
      this one".
- [ ] The HUD shows a **"I · The Shop Floor"** capsule.
- [ ] The Market has today's commons, plus three **black silhouettes** reading
      "Something further down — Below Stairs opens when you know 10 species".
      *Question: does the tease make you want to get there?*

## 2. The first floor down (around 10 species)

- [ ] At 5 species the **Kelp Stair** scene plays full-screen, over its own
      painted plate once that render is harvested, and the room's art until then.
- [ ] At 10 species, **Below Stairs** plays:
  - the pantry is the backdrop;
  - Charlotte hands over the key;
  - Wilbur takes the lamp;
  - the two characters swap lit and dimmed as they talk.
- [ ] One beat offers **three reply cards** (Lead the way / Less like fish how?
      / Is it safe down there?). Each card shows who answers. Picking one plays the
      answer, and then the scene carries on. *Question: do the replies feel like
      yours?*
- [ ] Charlotte's last beat offers the Sunken Pantry with **Hang it**.
- [ ] The Market now stocks floor II creatures, and the silhouettes are floor III.
- [ ] Buying your **first floor II creature** plays "Up from Below Stairs".
- [ ] **Skip scene / Esc** works on every cinematic scene.

## 3. Weirder further down

- [ ] Look at the creatures you can buy at floor I versus floor II and, if you
      push on, floor III (25). *Question: does each floor read as stranger
      than the last?* This is the core promise. Note any species that feels
      misplaced.
- [ ] Prices: some floor II creatures cost far more than others (formerly
      evolution-only species cost their rarity's default). *Question: does the
      price spread feel like a choice or like noise?*

## 4. Your own tank (veteran path)

- [ ] Your floors are already open. No fish you own or have owned is locked.
- [ ] **World & story → Memory Book** lists every scene you've seen as an
      illustrated card. Tapping one replays it as "A memory", and Esc closes it.
- [ ] If you ever widened the tank, the **Hatchery** background is now yours,
      with a short Wilbur and Charlotte scene.
- [ ] If you bought The Last Aquarium, "After the Last Aquarium" plays once.
      *Question: does it land as a soft ending without breaking the mystery?*

## 5. Pacing (the open question)

The simulator `projects/cthulhuquarium/data/simulate_descent.py` (a very active
collector clicking 80% of coins) opens the floors at **2 / 6 / 17 minutes** and
fills the book in **about 1h20m**. The server pays and prices each fish by the
highest of its six stat rarities, a leftover of the removed hidden-stats
system. Pricing by each fish's canon rarity instead gives **2 / 6 / 21 / 46
minutes** and about 2 hours.

*Question: should the descent take days rather than an afternoon?* If so, the
levers are:
- price and pay by canon rarity;
- raise the floor thresholds;
- give each floor an entry cost.

That's a balance decision for you; it's recorded on t-094.

## 6. Art to judge as it arrives

These renders were submitted directly through the canon pipeline on 2026-11-21
(30 jobs in canon `art/jobs.yaml`) and reach the game with the next `deliver.sh`
run plus a kind_robots sync:

- [ ] Wilbur's 20 per-floor portraits. He should look a little worse on each floor, and
      nobody should mention it. *Question: is the escalation funny-dark or too much?*
- [ ] Five scene plates: the first creature from each floor, and the post-finale.
- [ ] Five plates first rendered 2026-11-02 and never delivered (first purchase,
      bestiary complete, Kelp Stair, Portsmouth, Hatchery). Those images are gone
      from the server (404), so they were re-rendered in the same batch.
