# Recipe Box — SPEC

Status: draft for Silas review
Priority: normal
Slug: `recipe-box`
Kind: software

## Goal

A cozy, personal cooking companion: a Flutter app for saving, organizing, and cooking
from your own recipes. Recipe Box is for one person's kitchen, not a public recipe site
or a social network — it should feel like a well-loved recipe box on the counter, not a
spreadsheet. Core value: get a recipe in fast, find it again fast, and use it hands-free
while actually cooking.

## Reference material

No existing external reference material (no examples/ or legacy site) — this is a
from-scratch personal app. `apps/recipe-box/` is the scaffolded Flutter skeleton
(`flutter create . --platforms ios,android` per its README); no code has been written yet.

## Install targets

`ios` and `android` only for MVP, matching the scaffold already generated. Recipe Box is
meant to be held or propped up in a kitchen — phone/tablet is the right form factor.
Desktop/web is a plausible future add for recipe entry/editing at a bigger screen, but
it's a non-goal for MVP; add it later as a straightforward Flutter platform target if
Silas wants it (no architecture changes required to add it).

## MVP users

- Silas is the only user. No accounts, no multi-user sharing, no public profiles.
- Recipes come from three places: typed in by hand, pasted/copied from somewhere else
  (a website, a text message, a cookbook photo) and cleaned up manually, or eventually
  imported via a "paste a URL" helper (stretch goal, not MVP — see Non-goals).

## Core recipe fields

- Title
- Optional photo (one hero image per recipe)
- Optional short description/note ("Grandma's, but with less salt")
- Prep time, cook time (both optional, freeform-ish but structured as minutes)
- Servings / yield
- Ingredients: an ordered list of `{ quantity, unit, name, note }` — quantity and unit
  are free-text strings (e.g. `"1 1/2"`, `"cups"`), not parsed/validated numerics, so
  "a pinch" or "to taste" work without fighting the input
- Steps: an ordered list of freeform text instructions (one entry per step)
- Tags: freeform strings the user defines as they go (e.g. `dinner`, `vegetarian`,
  `30-minutes`, `grandma`) — no fixed taxonomy to maintain
- Source (optional freeform text/URL — "where this came from," not a live link fetch)
- Favorite (boolean)
- createdAt / updatedAt

## MVP screens

1. **Recipe List**
   - Grid or list of saved recipes (photo thumbnail when present, title, tags).
   - Search by title/ingredient/tag (client-side, instant, no backend).
   - Filter by tag and by favorite.
   - Prominent "add a recipe" action.

2. **Recipe Detail / Cook Mode**
   - Full recipe: photo, description, prep/cook time, servings, ingredients, steps.
   - Ingredients render as a checklist (tap to check off while gathering/cooking) —
     checked state resets each time the recipe is reopened, it's a per-session aid,
     not a persisted shopping-list state.
   - Steps render large and readable, one focus-friendly view, screen-stays-awake while
     this screen is open (so the phone doesn't lock mid-recipe with messy hands nearby).
   - Favorite toggle, edit, delete (delete asks for confirmation — it's destroying a
     recipe someone may have hand-typed in from memory).

3. **Add / Edit Recipe**
   - Form covering every field in "Core recipe fields" above.
   - Ingredients and steps are reorderable, freeform-add lists (add row, reorder,
     remove row) — no minimum count enforced, but title is required to save.
   - Optional photo picker (device gallery/camera).

4. **Settings**
   - Export all recipes to a single JSON file (share sheet) — the backup/portability
     story for MVP.
   - Import recipes from a previously exported JSON file.
   - About/version info.

## Data model

```txt
Recipe
- id
- title
- description
- photoPath          // local file path/URI, not a remote URL
- prepMinutes        // nullable int
- cookMinutes        // nullable int
- servings           // nullable string ("4", "6-8", "a dozen cookies")
- source             // nullable freeform string
- favorite           // bool, default false
- tags               // list<string>
- createdAt
- updatedAt

Ingredient (ordered, belongs to a Recipe)
- id
- recipeId
- position            // sort order
- quantity            // freeform string, nullable
- unit                // freeform string, nullable
- name
- note                // nullable ("softened", "or to taste")

Step (ordered, belongs to a Recipe)
- id
- recipeId
- position
- text
```

Store data locally on-device (e.g. `drift`/SQLite or an equivalent embedded DB — pick
whatever the implementer finds most maintainable in Flutter; no preference expressed
here beyond "not raw `SharedPreferences` for structured recipe data"). Photos live in
app-local storage, referenced by path, not embedded as blobs in the database.

## Storage, privacy, and sync

This is a personal single-user app with no sensitive third-party data (unlike
superkate-services-calculator's client records) — the security bar is correspondingly
lower, but still real:

- **MVP is local-only.** No accounts, no backend, no network calls required to use the
  app. Everything lives on-device.
- **Backup is export/import, not cloud sync**, for MVP. A JSON export via the OS share
  sheet is "good enough" backup/transfer between devices for a personal app; there is
  no server component to build, secure, or pay for.
- **Cloud sync across devices is a real, plausible v2**, not a beta requirement like the
  Superkate app — flag it as a future task once MVP is live and Silas has used it enough
  to know whether he actually wants it (e.g. "I want this on my phone AND my tablet").
  If/when it's built, it should follow the same auth/authorization/HTTPS baseline as
  every other kind_robots-adjacent app (see superkate-services-calculator/SPEC.md's
  "Beta sync expectation" for the baseline to reuse, not reinvent).
- No analytics, no telemetry, no crash reporting that phones home by default.
- No secrets, credentials, or API keys required for MVP — nothing to keep out of source
  control yet because there's nothing to leak.

## Visual direction

Cozy and warm — a well-worn recipe box, not enterprise software. Rounded corners, warm
neutral/cream backgrounds, a food-forward accent color (terracotta/warm orange or sage
green reads "kitchen" without being a cliché red-and-white checkered tablecloth).
Photography-first recipe cards when a photo exists; a pleasant placeholder (icon or
soft pattern, not a broken-image glyph) when it doesn't. Large, legible type in Cook
Mode specifically — it may be read from across a counter with flour-dusted hands.

## Non-goals for MVP

- Accounts, multi-user sharing, or any social/public feature (comments, discovery feed,
  following other cooks)
- Cloud sync/backend of any kind
- "Paste a URL and auto-import a recipe" scraping/parsing — genuinely useful later, but
  it's a distinct, fiddly feature (parsing arbitrary recipe sites) that shouldn't gate
  MVP; track it as a stretch/v2 task
- Meal planning / weekly calendar view
- Shopping list generation across multiple recipes (the per-recipe ingredient checklist
  in Cook Mode covers "gathering for one recipe"; a cross-recipe shopping list is a
  reasonable v2 but adds real scope — aggregating/deduping freeform ingredient strings
  across recipes is not trivial)
- Nutrition info, unit conversion/scaling math, or serving-size recalculation
- Recipe rating/review, version history, or "recipe forking"
- Any store submission or public release — that's its own future needs-human gate per
  `apps/README.md` ("Store submission for any app is a needs-human gate. No exceptions.")

## Decided product choices

- Silas is the only user; no accounts or sharing in MVP.
- Ingredients and quantities are freeform strings, not parsed/validated numerics —
  optimizes for fast entry over structured math.
- Tags are freeform, user-defined, no fixed taxonomy.
- Backup is JSON export/import via share sheet, not cloud sync, for MVP.
- Cook Mode keeps the screen awake and uses large, glance-friendly type.
- Delete requires confirmation; nothing else in MVP is destructive enough to need it.
- Install targets are `ios` and `android` only for MVP, matching the existing scaffold.

## Implementation configuration values to collect

- Preferred embedded DB package (`drift` is a reasonable default; no strong opinion
  expressed here — implementer's call unless Silas has a preference).
- Confirm accent color direction (terracotta vs. sage vs. something else) before
  finalizing the palette — this doc proposes options, doesn't lock one in.
