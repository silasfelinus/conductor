# Cthulhuquarium economy suite (t-094)

2026-11-21. Two halves: a strategy simulation over the real 151-species roster,
and adversarial API checks against a local kind_robots server (MariaDB, never
production). Both are re-runnable:

    python3 projects/cthulhuquarium/data/simulate_descent.py --suite --days 120
    node projects/cthulhuquarium/data/api_exploit_suite.mjs        # local server on :3000
    node projects/cthulhuquarium/data/api_floor_keys_playthrough.mjs

## 1. Strategies (canon rarity, keys 150 / 3,000 / 30,000 / 400,000)

```
151 species; rarity by canon rarity; floor keys {2: 150, 3: 3000, 4: 30000, 5: 400000}
  active      II day 1, 0h03 | III day 1, 0h32 | IV day 2, 0h51 | V day 6, 0h51 | book day 7, 0h48  (known 151)
              tank 32/36, peak coins 399,991, lowest after feeding 40, longest wait for a new species 3d 0h45
  casual      II day 1, 0h03 | III day 2, 0h05 | IV day 5, 0h07 | V day 14, 12h00 | book day 16, 12h08  (known 151)
              tank 36/36, peak coins 400,104, lowest after feeding 40, longest wait for a new species 8d 12h00
  idle        II day 1, 12h01 | III day 4, 0h01 | IV day 11, 12h00 | V day 37, 0h00 | book day 43, 12h00  (known 151)
              tank 36/36, peak coins 405,933, lowest after feeding 40, longest wait for a new species 23d 11h59
  tapper      II day 1, 0h03 | III day 1, 0h26 | IV day 2, 0h29 | V day 6, 0h13 | book day 7, 0h02  (known 151)
              tank 32/36, peak coins 863,070, lowest after feeding 40, longest wait for a new species 3d 23h29
  binge       II day 1, 0h03 | III day 1, 0h32 | IV day 1, 1h54 | V day 2, 0h43 | book day 2, 1h47  (known 151)
              tank 32/36, peak coins 2,720,850, lowest after feeding 40, longest wait for a new species 0d 22h30
  twice-a-day II day 1, 0h03 | III day 2, 12h02 | IV day 6, 12h04 | V day 21, 0h01 | book day 24, 12h04  (known 151)
              tank 36/36, peak coins 399,983, lowest after feeding 40, longest wait for a new species 13d 11h57
  daily       II day 1, 0h03 | III day 3, 0h06 | IV day 9, 0h07 | V day 28, 0h00 | book day 32, 0h08  (known 151)
              tank 36/36, peak coins 400,104, lowest after feeding 40, longest wait for a new species 17d 0h00
  weekly      II day 1, 0h03 | III day 8, 0h00 | IV day 22, 0h14 | V day 78, 0h00 | book day 85, 0h28  (known 151)
              tank 36/36, peak coins 401,473, lowest after feeding 40, longest wait for a new species 48d 23h59
  afk         II day 3, 0h00 | III day 10, 0h00 | IV day 30, 0h00 | V day 95, 0h00 | book day 112, 0h00  (known 151)
              tank 36/36, peak coins 402,249, lowest after feeding 40, longest wait for a new species 59d 23h59
```

Profiles: **active** 60 min/day; **casual** two 10-min visits; **idle** two
3-min check-ins at 30% clicks; **tapper** every coin at up to 8 clicks/s;
**binge** one 6-hour session a day; **twice-a-day**, **daily**, **weekly**
short visits with 12 h / 24 h / 7 d gaps; **afk** opens the tank once a day
and never clicks.

### Findings

1. **No runaway strategy.** Rapid tapping (tapper) finishes the book 1 hour
   earlier than active play: clicks are capped by the drop rate, not tap speed.
   The binge player finishes on day 2, which is the honest cost of six hours a
   day; nothing about it is an exploit.
2. **Absence is capped, not farmed.** Hunger ends passive income about 70
   minutes into an absence, so a 12 h, 24 h or 7 d gap all pay about the same
   (twice-a-day 24.5 d, daily 32 d, weekly 85 d to the book). Coming back after a
   week never pays out a windfall.
3. **Nobody goes broke.** Feeding never takes any strategy below the 40
   starting coins, and even afk (never clicks) completes the book from passive
   income alone (day 112), so no tank can soft-lock.
4. **The floor V key leaves a long wait with nothing new to buy (main
   finding).** Floors I–IV hold 134 species. A player has usually bought all of
   them before the 400,000-coin key is affordable. The longest gap without a new
   species is 8.5 days for casual, 17 days for daily and 3 days for active. This
   sits inside Silas's targets (casual reaches floor V on day 14.5 and the book on
   day 16), but it is the pacing risk most worth watching in the playtest. The
   price sweep:

   | V key | casual V / book | casual longest wait | daily longest wait |
   |---|---|---|---|
   | 400,000 (shipped) | day 14.5 / day 16 | 8.5 d | 17 d |
   | 250,000 | day 11 / day 13.5 | 5 d | 10 d |
   | 150,000 | day 9 / day 11.5 | 3 d | 6 d |

   Recommendation: keep 400,000 for the first playtest, which is what was
   decided. Ask playtesters about the stretch between the Conservatory and the
   Bottom. If it drags, 250,000 is a one-constant change
   (`FLOOR_KEY_COSTS`, plus `economy.yaml` `floor_keys`). The decor, sets and
   upgrades shelves also give the saving player something to spend on, which
   this simulator does not model, so the real wait is gentler than shown.

## 2. Adversarial API checks: 26/26 pass

Run on a fresh local account each time (`api_exploit_suite.mjs`):

| Attack | Result |
|---|---|
| Positive control: an honest 3-coin claim after 10 s | paid 3 |
| Forged 500,000-coin collect | credited only the accrued allowance (6) |
| Claim above the per-request cap / negative / fractional | 400 |
| 20 parallel claims racing the same allowance | together credited 6 (compare-and-set anchor) |
| Forged reply id; unknown scene; 40-scene list | 400 |
| Marking an ending scene seen five times | no coins, no achievement |
| Buying a floor IV species on floor I | 403 |
| Buying key II below its threshold; junk floor value | 403 / 400 |
| Signed-out collect | 401 |
| Public tank JSON | no email, password, userId or token keys; email absent |
| Private tank by URL | 404 |
| Selling another tank's fish | refused |
| Ten parallel ticks over one hour of absence (two tabs, a script) | settled once (row lock, stale snapshot settles nothing) |
| Six parallel species buys with coins for one | one bought, coins never negative |
| Six parallel species buys with room for one | the tank stops at its cap |
| Three parallel finale buys | charged once |
| A new tank that knows 30 species asks for grandfathered keys | none: only tanks the key system met already past a threshold keep their floors |

The last five rows cover the races the release-candidate technical review
traced in the code (see [RC-DOSSIER.md](RC-DOSSIER.md)); they pass against the
RC-fixes build.

The floor-key play-through (`api_floor_keys_playthrough.mjs`, 15/15) covers
canon-rarity pricing, keys in order, the double-tap race (charged once under a
row lock), and grandfathered veterans (keys granted once).

Cosmetic only: a player can mark an ending scene seen without earning it, which
shows the card on their own Memory Book shelf. It pays nothing, grants no
achievement and is visible only to them, so it is left as is.

## 3. Found while running the suite

**t-084 must ship in two steps.** Prisma selects every declared scalar column, so
a build whose client still declares `bestStat*` fails on purchase once the
column is gone. That would have broken purchases between `migrate deploy` and
the container swap. Split into kind_robots #5499 (client only) and a follow-up
migration, merged only after production runs #5499.
