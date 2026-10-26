# Playbook Kit: Design Brief

Started 2026-10-26 PT at Silas's request: one consistent framework for iterating
on new playbooks, in the manner of Emperor of Dust, Zuzu: Shifting Lands,
Shifting Desks, Prom of Doom, Space Couch and Ecotone, and smart about how
much complexity it allows.

## What it is

A shared frame, not a shared engine. Each playbook keeps its own rules, voice
and stage. The kit owns what a player should find in the same place in every
playbook:

- a one-screen console shell with a meter strip;
- a single settings sheet: text size, font, contrast, motion, text speed, sound,
  trailer and romance content;
- a spoiler-free title trailer;
- a scrapbook of cinematic moments with a full-screen view;
- Cast (followers, villains, figures, optional romance), Factions, Secrets
  (reveals) and Endings panes;
- per-game saved progress.

Code and the full recipe live in kind_robots: `utils/playbookKit/`,
`components/playbook-kit/`, `/admin/playbook-kit`, `docs/playbook-kit/README.md`.

## Why it exists

A survey of the six games on 2026-10-26 found nothing shared:

- **Settings:** Emperor has five reading preferences; Prom of Doom and This
  Means Warp have none.
- **Endings:** only Shifting Desks has an endings gallery.
- **Scrapbook:** no game has one.
- **Layout:** three use the fixed console layout and three do not.

Every new playbook re-solved the same problems differently.

## Being smart about complexity

Each playbook declares a tier, and the tier caps every moving part:

| Tier | Scope |
| --- | --- |
| Vignette | One sitting |
| Standard | An evening |
| Saga | A campaign |

Two composite caps limit what the player has to hold at once:

- **Attention:** the meters on screen.
- **Parallel threads:** villains, romances and factions together.

How the caps apply:

- Going over a cap fails CI unless the spec carries a written allowance
  explaining why it earns its place.
- Coming in under a minimum is just the next rung to build.
- Everything declared must be felt: a faction, follower or villain with no
  moment, reveal or ending is flagged.

New playbooks start at Vignette and grow only after a playtested tier review
(template task t-007).

## How a new playbook starts

```bash
cd /path/to/conductor
git pull
python scripts/new_playbook.py moon-laundry "Moon Laundry" --goal "One-line definition of done."
```

```bash
cd /path/to/kind_robots
git pull
npm run playbook:new -- moon-laundry "Moon Laundry"
```

The Conductor script runs `intake.py` (every registration surface), then writes
the playbook design brief and the ladder roadmap from `templates/` (`roadmap.template.yaml`, `DESIGN-BRIEF.template.md`).

## Gates

None beyond the ordinary ones. Each playbook's public `/play` release and
visual acceptance stay Silas's (template t-010).
