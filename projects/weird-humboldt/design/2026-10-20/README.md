# Ecotone and Playbook Studio mockups (Silas, 2026-10-20)

Silas: *"here's our new mockups for playbook manager and an ecotone layout
structure. Ecotone should definitely support multiple styles, same as we do
with shifting desks. I'll have to review the checkpoints still to figure out
the sweet spots"*

## Shared look

- **Background:** deep navy (about `#09141c`).
- **Panels:** a shade lighter, with a thin gold rule (about `#c9a96e`). Dialogue
  panels add a heavier gold bar on the left.
- **Titles:** heavy uppercase serif in cream (about `#f3e6c8`).
- **Labels:** small caps with wide letter-spacing, in gold or soft teal.
- **Pills:** dark, outlined, with letter-spaced caps.
- **Primary action:** a solid gold button.
- **Scene art:** the drawn, flat-vector style that Ecotone's code-drawn scenes
  already use.
- **Layout rule** (printed on the studio phone mockup): *one viewport; inner
  scroll only for long content.*

## Ecotone

### `ecotone-story-beat-desktop.webp` and `ecotone-companion-encounter-desktop.webp`

- **Top bar:**
  - A compass-star mark with ECOTONE and WEIRD HUMBOLDT beside it.
  - In the middle: a chapter or day line ("DAY 01 / THE IMPOSSIBLE WEEKEND") and
    a place-and-time line ("ARCATA · DUSK").
  - On the right: Clarity and Endings pills.
- **Scene art** runs full-bleed behind everything.
- **Left column, top to bottom:**
  - A kind pill ("STORY BEAT 01", "COMPANION ENCOUNTER").
  - A huge serif title.
  - A serif subtitle under a gold rule.
  - Narration.
- **Companion encounter:** the left column adds the companion's name, their role
  in teal caps and their quoted line. Their portrait stands on the right half of
  the screen.
- **Bottom left:** a dialogue panel with a gold kicker (the speaker) and serif
  body text. It can carry a footer line ("THE OTHERS WILL STILL BE OUT THERE.")
  and a "Tap to continue" cue.
- **Bottom right:** a choices panel ("HOW DO YOU ANSWER?"). Each choice is a
  title over a subline (the roll and what it leads to) with a chevron; the
  focused choice has a gold border.

### `ecotone-story-beat-phone.webp`

The same parts, stacked:

1. Art band with the headline over it.
2. Dialogue panel.
3. Choices.
4. A bottom nav: JOURNEY / MAP / JOURNAL / ENDINGS.

The stat names in the mockups (WITS, RIZZ, "Endings 03/32") are illustrative.
The build shows the game's real skills and ending count.

## Playbook Studio

### Story Atlas (sent inline; not saved as a file)

- **Header:** KIND ROBOTS / PLAYBOOK STUDIO.
- **Left rail:**
  - **Your stories:** each game with a count of its beats.
  - **Collection:** groupings such as festival weekend, the crossings, threads
    and quests, the convergence, all endings.
  - **Live story health:** the number of open art requests.
- **Main area:** STORY ATLAS in large serif, with the tagline "Every beat. Every
  branch. Every beautiful, strange possibility." Filter pills (game, routes,
  status) and a gold "+ New beat" button sit beside it.
- **Cards:** a grid. Each card shows its art inset, a numbered kind pill ("02 /
  CROSSROADS"), an uppercase serif title, a place-and-route line, a status dot
  (READY / SELECTED / DRAFT EDIT / NEEDS ART / ENDING) and an open arrow.

### `playbook-studio-scene-desktop.png` and `playbook-studio-scene-phone.png`

The scene editor:

- A "‹ All scenes" back link, a big serif title and a breadcrumb ("ECOTONE /
  CHAPTER 02 / KIT'S THREAD").
- **Art card:** a gold-framed card with scene and variant pills, a quoted line
  over the art, the selected visual and how many art candidates exist, and a
  "View art options" button.
- **Edit panel:**
  - Header: EDIT SCENE with an "Unsaved draft" pill.
  - Underlined tabs: Story / Choices / Variants / Art / Notes.
  - Title and story-text fields.
  - Player choices, each with its roll badge.
  - Footer: a summary ("3 choices · 4 variants · 1 art request") and a gold
    SAVE DRAFT button.
- **Phone:** the same parts stacked.

## Art styles

Ecotone takes the player-selectable style system Shifting Desks uses:

- **Styles change only what the player sees.** Runs and saves are unaffected.
- **Each style keeps its renders under its own path.** A beat a style hasn't
  drawn yet falls back to the base art, and then to the code-drawn scene.
- **The choice is saved per player.**

Which checkpoints become styles is Silas's call once he has reviewed the
bake-off (`art/CHECKPOINT-BAKEOFF.yaml`).
