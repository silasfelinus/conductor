# Playbook Forge: design (playbook-kit t-010)

2026-10-26 PT. Silas asked for one consistent manager across every playbook, an
admin console where an idea becomes a configured project with honest
generation-time forecasts, analysis and adjustment of existing plans, and an
AAA console look rather than a web app. This document is the investigation and
the design; t-011 to t-014 build it.

Evidence: three read-only surveys of kind_robots (Playbook Studio architecture;
save/load, character creation, checks and structure in eight games), and one
read-only call to `/api/admin/art-review` for real render times (202 ArtJobs).

## 1. What every playbook shares

Eight story games were surveyed: Emperor of Dust, Zuzu: Shifting Lands, Shifting
Desks, Prom of Doom, This Means Warp, Ecotone, Terrors on Crystal Street and the
Zuzu gamebook.

The common core is the same in all of them:

- a seeded deterministic run, with the seed stored in the save;
- a localStorage autosave of one versioned run, plus a "storage blocked" warning;
- a phase loop: brief or choice → check → authored outcome with effects and
  flags → debrief → finale → ending;
- 4–6 named stats and 2–5 visible meters;
- an ending chosen from flags and meters at the finale;
- pre-rendered art keyed by id, with an initials or monogram fallback;
- six of the eight are wired to the Playbook Studio live-text overlay.

## 2. What varies (the extras the forge exposes as options)

| Module | Who uses it | Forge row |
| --- | --- | --- |
| Manual save slots | Emperor (3), Ecotone (3) | Save → Save slots |
| Undo / rewind | Ecotone (last choice), Emperor (any dawn), Gamebook (swap) | Save → Undo |
| Replay-ledger saves | Shifting Lands, Emperor | Save → Save style |
| Export / import | Ecotone | Save → Export saves |
| Share link / daily seed | Crystal Street, Shifting Desks | Save → Share a run |
| Cross-run scrapbook, endings, codex | Emperor, Desks, Ecotone, Crystal St, Gamebook | Save → Keep between runs |
| Character creator | Prom (form × element), Ecotone (archetype, name, avatar), Crystal St (avatar × clique), Desks (job), Warp (captain + crew) | Player tab |
| Player-uploaded portrait | Ecotone | Player → Upload own portrait |
| Followers / crew | Emperor, Ecotone, Crystal St, Warp, Prom | Cast → Followers, Party size |
| Factions | Emperor (15), Crystal St (4), Desks (6 Societies) | Cast → Factions |
| Villain drawn per run | Warp, Crystal St | Cast → New villain each run |
| Hidden moral ledger | Shifting Lands, Desks, Gamebook | Rules → Hidden moral ledger |
| Art-style picker | Desks, Ecotone | Pitch → Art styles |
| Mystery deck | Ecotone | Story → Reveals |

## 3. Where games genuinely differ (parameters, not modules)

- **Checks:**
  - five games roll 2d6 plus a stat against a target, with natural 2/12 overrides;
  - Emperor and Warp roll a shown percentage built from the party's stats (an identical formula);
  - Prom uses a d6 hash.
- **Outcome tiers:** Emperor, Prom and Warp ship four (triumph, success,
  partial, failure). The rest ship pass/fail. Warp's plan asks for five.
- **Failure:** every game fails forward, so a bad roll never dead-ends.
- **Identity:** in Ecotone it is cosmetic; in Prom and Desks it changes the
  odds; Shifting Lands is deliberately identity-agnostic.
- **Unreadable save:**
  - Emperor holds it untouched and says so;
  - Lands warns;
  - the other six silently reset and overwrite the player's run.

## 4. Save and load standard

| Setting | Recommendation | Reason |
| --- | --- | --- |
| Autosave | Always on | Every playbook does it. |
| Save style | Snapshot by default; ledger when every ending needs a replayable proof trace | A ledger means a rules change needs a pinned rules version. |
| Unreadable save | **Hold** | Keep the unreadable save untouched, explain it, and offer a new run beside it. The kit store already does this, and the forge flags *Start over* as a defect. |
| Versioning | A `version` field and a migration function per bump | Emperor (v3 → v4), Lands (v3 → v8), Desks (v1 → v5) and Ecotone (v4) all show the pattern. |
| Meta-progress | A separate key from the run | The scrapbook, endings and secrets survive a new run (the kit's `kr-playbook-kit-<id>-v1`). |

## 5. Character and avatar

The opening comes in three shapes, each with different art math:

| Opening | Example | Images |
| --- | --- | --- |
| Fixed hero | Zuzu, the Emperor | `1 + poses` |
| Pick a hero from a roster | Warp captains, Ecotone archetypes | `roster × (1 + poses)` |
| Build a hero from factors | Prom, Crystal St | depends on the portrait strategy below |

Portrait strategies for a built hero:

| Strategy | Images |
| --- | --- |
| Per option | `factors × options` tiles |
| Per combination | `options ^ factors × poses` |
| On demand | 0 up front; painted when the player finishes the creator |
| Drawn in code | 0 |

Per combination explodes quickly: Prom's 6 forms × 8 elements are 48 identities
before any pose. The forge warns above 60.

Name and pronouns, player upload (a private ArtImage, as in Ecotone) and
"identity changes the odds" are independent toggles.

## 6. Forecast model

Render seconds per image are medians of DONE jobs, measured from claim to image
saved (via `/api/admin/art-review`, 2026-10-26):

| Checkpoint | Seconds per image | Measured? |
| --- | --- | --- |
| Illustrious (Arthemy, Nova) | 23 | 118 jobs |
| SDXL | 37 | yes |
| Krea 2 | 82 | yes |
| Z-Image | 67 | yes |
| Flux 2 | 760 | 8 jobs only |
| Distilled | 8 | Inferred, not yet measured |

Images are the sum of these terms:

- 2 (key art and title);
- hero portraits (section 5);
- followers × (1 + poses);
- villains × 2;
- figures;
- faction emblems;
- encounters;
- encounters × choices × outcome pictures (0, 1 or 2);
- quests;
- endings × finale beats;
- moments.

The trailer reuses moments. The total is then multiplied by art styles and by
1.3 for rerolls. Ledgers run 1.2–3 times shipped art.

Render time is images × seconds per image, plus one cold start per lane. Queue
wait is a separate input.

Words come from per-unit rates (encounter 160, outcome 55 per tier per choice,
ending 260, reveal 120, bio 180, quest step 110, caption 30). Fail-forward
outcomes cost 35% more text. Ending families cost 60% more per family.

- **Agent sessions** = words ÷ 6,000, plus one session per system beyond the
  core loop (checks, builder, upload, ledger saves, rewind, villain per run…).
- **QA** = 2 seeded playthroughs per ending, one per drawn villain, plus 5 for
  seeds.
- **Tier fit** reuses the kit's `TIER_BUDGETS`. Visible stats count as meters.

The word rates are uncalibrated estimates and stay editable in the forge's
Assumptions screen.

## 7. One manager for every playbook (t-013)

The Playbook Studio registry is a fixed tuple. At runtime, though, it is a
plain array check, and the database keys on a free-text slug. So:

- **Widen the registry.** Build `PLAYBOOK_GAMES` as legacy adapters plus
  `KIT_PLAYBOOKS.map(kitToPlaybook)`.
- **Add a kit adapter** `utils/playbook/kitAdapter.ts`:
  - acts become routes;
  - moments, reveals and endings become nodes;
  - cast becomes people, and factions become variations;
  - art briefs feed the existing art-request lanes.
- **Report one shape.** Every adapter also reports the forge `Blueprint` counts
  (`utils/playbookForge/existing.ts` already counts from adapters), so Studio
  and Forge show the same numbers.
- **Add the missing games.** Prom and Warp are not in Studio yet; their forge
  counts read their rules modules directly until an adapter exists.

## 8. The Forge (t-012, t-014)

`/admin/playbook-forge` is a console, not a form.

1. **Title screen.**
   - Menu: *New playbook*, *Continue draft*, *Analyze a game*, *Assumptions*.
   - Visuals: full-bleed key art, the logo, and a pulsing "press A" prompt.
2. **Idea.** A title, an idea in plain words, and a genre chosen from art tiles.
   - Each genre is a starting loadout from its pioneer game.
3. **Loadout.** Seven bumper tabs: Pitch · Player · Cast · Story · Rules ·
   Endings · Save.
   - Each tab is a short list of console option rows (`label ◀ value ▶`).
   - The focused row's explanation sits under the list.
   - A persistent **forecast HUD** shows:
     - tier, images, render time, words, sessions and QA;
     - for the focused row, a **preview of ◀ and ▶**, the way an RPG compares
       equipment before you equip it.
4. **Launch.**
   - A summary card of the forecast, plus where the game lives (Admin preview,
     Play or Projects).
   - Forging creates the Kind Robots Project. Its scaffold Todo carries the
     blueprint to Conductor, and `new_playbook.py --blueprint` reads it.
5. **Analyze a game.**
   - Pick a game cover. Each row shows **Built** (counted live from code) next
     to **Plan** (the Conductor goal), plus the remaining images, render time
     and words.
   - Adjust the plan with the same rows, then *Send plan to agents*. That
     creates a high-priority agent Todo with the diff and the blueprint, and
     Todos outrank every roadmap.

The factor rows are data (`utils/playbookForge/factors.ts`). A new option is one
row plus one estimator term.

## 9. AAA console visual system (t-011)

The first kit shell read as a web app: a light page, small type, pill buttons
and form rows. The console system replaces that:

- **Stage.**
  - Dark scoped theme `forge` (`data-theme`): ink black-blue ground, one hot
    accent and one cool accent.
  - Full-bleed key art behind everything: blurred and darkened, with slow
    parallax drift and a vignette and scanline grain.
- **Safe area.** A TV-safe inset of `clamp(16px, 4vw, 64px)` on every side;
  nothing interactive sits outside it.
- **Type.**
  - Display: a condensed uppercase stack (Bahnschrift, DIN Alternate, Arial
    Narrow) with wide tracking.
  - Body: at least 18 px at 1080p via `clamp()`.
  - Numbers: tabular.
- **Focus, not hover.**
  - Exactly one focused element at a time: an accent bar, a glow and a 1.02
    scale.
  - D-pad or arrow keys move focus, ◀ ▶ change the value, A / Enter confirms,
    B / Esc goes back.
  - LB / RB (Q / E) switch tabs; Start / Enter launches.
  - The mouse sets focus on hover; touch taps.
  - Gamepad input reuses `utils/arcade/input.ts`.
- **Prompt bar.** A fixed bottom bar of button prompts that follows the last
  input device: Xbox-style glyphs for a pad, keycaps for a keyboard, hidden for
  touch.
- **Motion.** 160 ms ease-out on focus, a 260 ms slide on tab change, count-up
  numbers in the HUD. All of it drops under reduced motion.
- **Layout.**
  - Desktop: header (logo · bumper tabs · fullscreen), then the option list
    (about 60%) beside the HUD (about 40%), then the prompt bar.
  - Phone: the list takes the full width and the HUD collapses into a
    three-number strip that expands.
  - One screen at every width: the option list scrolls inside its own bounded
    pane.
- **Fullscreen** is on the header and on ☰ / F, as the arcade cabinets do.

The kit shell (playbook-kit-shell) moves onto the same system in t-011.

## 10. Production ledger (t-016)

Silas, 2026-10-26: *"any of our games can be loaded and it will enumerate all of its
computations and how much they will and have taken. If all is complete, will be stared and
shiny, all all will be super shiny, but showing where are discrepancies. Will submit sections
for processing, to be read by relay or next agent."*

**Load a game** in the Forge opens its ledger (`/admin/playbook-forge?ledger=<slug>`).

- **Units.** Every beat the game's Playbook Studio adapter knows, grouped by node kind into
  sections. A beat's art moves through four states: missing → queued → rendered → delivered.
  It can also be failed, when every job for it failed. Rendered is not delivered until the
  game shows the picture: a DONE job on a beat with no `artUrl` is a discrepancy, "not wired".
  A beat's words are its scene text plus success and failure text for each checked choice.
  Checks that branch to other beats (the Zuzu Gamebook) expect no outcome text.
- **Spent.** Spend comes from the real relay time of the ArtJobs linked to the beat by
  Studio `art-request` notes, measured from the relay claiming the job to its image being
  saved. Project totals come from every ArtJob tagged to the game's `artProject`.
- **Left.** Render time left is the missing and failed beats × the calibrated lane median ×
  (1 + reroll rate). Words left use the Forge word rates.
- **Shine.** A section earns ★ when every beat in it is delivered and written. The game is
  **super shiny** when every section is starred and no measured plan factor is short.
- **Discrepancies.** The ledger lists:
  - unwired renders;
  - beats that only ever failed;
  - beats with no art and no job;
  - missing text;
  - plan gaps;
  - Studio edits not yet folded into the authored source;
  - games with no Studio adapter (Warp and Prom until t-013).
- **Submit.**
  - *Submit art* sends a section's missing and failed beats to kr-relay as Studio art
    requests: the same prompt, shape and project tag Studio uses. It sends at most 60 per
    press and never re-sends queued or rendered art.
  - *Send writing* creates a HIGH-priority AGENT Todo listing the missing text beat by beat,
    which the next agent takes before any roadmap work.
- **Server.** `GET /api/admin/playbook-ledger/[slug]` is admin-only and read-only, and reads
  at most 5000 jobs.

Ledger read from code alone on 2026-10-26, with no relay data:

| Game | Art delivered | Starred sections |
|---|---|---|
| Ecotone | 42/301 | 4 of 7 |
| Emperor of Dust | 248/253 (5 follower portraits) | 4 of 5 |
| Shifting Lands | 140/140 | all |
| Shifting Desks | 155/155 | all |
| Zuzu Gamebook | 380/380 | all |
| Crystal Street | 436/436 | all |
