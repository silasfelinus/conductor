# Shifting Lands vs Shifting Desks — depth assessment (2026-10-18)

Silas, 2026-10-18: *"Zuzu shifting lands feels like it's lost some polish since
we've been working on Shifting Desks. … Our shifting desks game has 24 random
encounters for each level, five levels. I want an assessment of what shifting
lands has, and aim for that level of complexity or better. … While desks is
more about weirdness and oddities, the world of Zuzu should be about making
tough decisions and facing the consequences of sacrifice and doing good in a
world that doesn't always reward it."*

## Like for like

Both games are five levels × three locations, and a run draws one card per
location (15 encounters). Replay depth comes from the size of each location's
pool and from what each card lets you do.

| | Shifting Desks | Shifting Lands (before) | Shifting Lands target (V6) |
| --- | --- | --- | --- |
| Cards per level | 24 (8 per location) | Homestead 12, others 9 (3 per location) | **24 (8 per location)** |
| Cards total | 120 | 48 | **120** |
| Choices per card | 3–4 (avg ≈ 3.4) | always 2 | **3–4** |
| Rolled vs certain choices | 207 rolled / 200 certain | 96 rolled / 0 certain | ≥ half of cards carry a certain (sacrifice / refusal) choice |
| Routes locked behind earlier play | 65 gated choices (flags, clearance, forms, grades) | none on cards (trial clue routes only) | ~⅓ of cards gate a route on shared **deed flags** |
| Up-front costs | yes (composure, forms, suspicion…) | none on cards (trial parley only) | hp / provisions costs on sacrifices |
| Boss | 7–8 choices, 6–9 department outcomes | 3 approaches, one outcome per result | (t-034) more outcomes keyed to the moral ledger |
| Run-wide identity | 5 job titles, 6 secret societies, 8 mutations | fixed hero | hero-agnostic prose makes later character choice possible |
| Endings | 10 authored endings with variants | victory / fallen / retired | (t-034) endings read from the moral ledger (`marks`) |
| Check presentation | "Risky 8" chip, tap for the sum | "steel · 8" (raw target) | **"Risky 7" chip** (shipped in kind_robots#3830) |
| Voice | second person | third person "Zuzu … he" + boilerplate | **second person, hero-agnostic** (shipped in kind_robots#3830) |

## Polish problems Silas saw, and their causes

1. **Stilted writing.** 72 of 72 later-land choice intents read "Zuzu chooses to X
   while respecting the consequences of this meeting", and risk lines were mechanical
   ("steel check against 8; a poor outcome can cost health or provisions"). The
   third-person "Zuzu … he" voice also locked the quest to one hero. *Fixed in
   kind_robots#3830:* every card, trial and journal line rewritten in second person;
   saves still restore (prose is excluded from replay comparison; rules stay pinned).
2. **Cluttered, scrolling layout.** The encounter reader put 16:9 art into a tall
   column with `object-cover`, cropping most of the painting, and the text column
   overflowed so the pane scrolled. *Fixed in #3830:* the whole painting is shown
   (contained over a blurred fill) above the text; readers fit one screen.
3. **"Three cups" but no cups.** Two causes: the layout cropped the painting, *and*
   the ROUND-1 keeper `three-cups-on-the-table.webp` genuinely shows a cook, a lantern
   and an empty table, no cups. The art needs a re-render (t-033), and the other 47
   card paintings need the same title-object audit.

## The V6 plan

- **t-031** engine: certain choices (`roll: null`), gated choices
  (`requires.anyFlags`), up-front `cost`, a moral ledger (`marks`: mercy, honesty,
  courage, cunning, ruthlessness), per-card pools of 8, all five lands on one
  reducer, a V6 save key. V2–V5 saves keep their frozen 48-card / 2-choice rules.
- **t-032** content: 72 new cards and 1–2 new choices on each existing card, written
  to `DECK-SPEC` (scratch spec copied into the PR) around ten shared deed flags
  (`deed-shared-bread`, `deed-kept-promise`, `deed-told-truth`, `deed-spared-foe`,
  `deed-carries-medicine`, `deed-knows-old-roads`, `deed-marked-by-wardens`,
  `deed-owed-favor`, `deed-bloodied-hands`, `deed-left-someone`) so early mercy
  or cruelty echoes in later lands.
- **t-033** art: card paintings for the 72 new cards; re-render Three Cups; audit
  every existing card painting for the objects its title promises.
- **t-034** endings: Desks-level ending variety from the moral ledger and trial
  outcomes, so a kind run that loses and a ruthless run that wins read differently.
- **t-035** balance: seeded simulation of V6 survival, death causes and gate
  reachability per land (Desks has `shiftingDesksBalanceReport.ts`).
