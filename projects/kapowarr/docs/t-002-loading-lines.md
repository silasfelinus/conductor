# kapowarr/t-002 — Add rotating funny loading lines (handoff)

date: 2026-08-15
target repository: `silasfelinus/Kapowarr` (not `conductor` or `kind_robots`)
intended branch: `worker/kapowarr-t-002`
status: this conductor session cannot push to `silasfelinus/Kapowarr` — its GitHub
  access is scoped to `silasfelinus/conductor` and `silasfelinus/kind_robots` only
  (see `projects/kapowarr/DESIGN-BRIEF.md`'s architecture-boundaries section, which
  anticipated exactly this gap for every t-002+ code task). This document preserves
  the fully-specified patch so a session with `Kapowarr` in its GitHub scope — or
  Silas directly — can apply it without re-deriving the design.

## What was actually done this session

Read-only inspection of the live `silasfelinus/Kapowarr` source (currently an
undiverged fork of `Casvt/Kapowarr`, no local changes yet) to ground this patch in
the fork's real template/JS structure rather than guessing at it. No writes were
made to that repository.

## Where the loading state actually lives

Three server-rendered templates show a static `<h2>Loading...</h2>` inside a
`.loading-screen` container while their page's JS fetches data over the API and
swaps the container out for real content:

- `frontend/templates/volumes.html` (`#loading-library`, line ~106) — library list
- `frontend/templates/view_volume.html` (`#loading-screen`, line ~350) — volume detail
- `frontend/templates/library_import.html` (`#loading-window`, line ~125) — import scan

All three are wired the same way: plain vanilla JS (no framework, no bundler), page
scripts (`volumes.js`, `view_volume.js`, `library_import.js`) run top-level (loaded
with `defer`, so the DOM is ready) and toggle the `hidden` class between the loading
container and the real content once their fetch resolves. There is no existing
frontend test runner (`tests/` only covers the Python backend via pytest); the
patch below is written to be testable in isolation anyway, in case one is added
later.

## Design (matches DESIGN-BRIEF.md's m1 personality-layer rules)

One centralized data source (an array of lines) + one pure lookup function, applied
via a single new script that every loading screen opts into with a plain HTML data
attribute — not scattered per-page edits. The static `"Loading..."` text stays
baked into every template as the literal, guaranteed fallback: if the new script
fails to load, throws, or JS is disabled, the heading still reads exactly what it
does today. `applyLoadingLines()` never throws past its own try/catch, so a bug in
the rotation logic can't block a loading screen from rendering.

## Exact patch

### New file: `frontend/static/js/loading_lines.js`

```js
//
// Rotating loading-screen flavor text
//
// Personal-fork QoL touch: swaps the default "Loading..." heading for a
// playful, Radarr/Sonarr-style line, picked at random each time a loading
// screen is shown. Centralized here (one data source + one lookup function)
// so any loading screen in the app can opt in via a single data attribute
// instead of scattered per-page copy.
//
// Kept pure and dependency-free on purpose: pickLoadingLine() takes an
// explicit lines array + random function, so it's unit-testable with a
// stubbed randomFn without touching the DOM.
//

const LOADING_LINES = [
	"Uncrinkling the pages...",
	"Waking up the letterer...",
	"Checking the staples...",
	"Flipping to the next issue...",
	"Talking the inker into one more panel...",
	"Dusting off the long boxes...",
	"Reordering the back issues...",
	"Asking the colorist for five more minutes...",
	"Chasing down a missing splash page...",
	"Un-bagging and un-boarding...",
];

// Must exactly match the fallback text already baked into every template's
// <h2>Loading...</h2>, so a slow/blocked script never leaves a blank heading.
const DEFAULT_LOADING_LINE = "Loading...";

function pickLoadingLine(lines = LOADING_LINES, randomFn = Math.random) {
	if (!Array.isArray(lines) || lines.length === 0)
		return DEFAULT_LOADING_LINE;
	const index = Math.floor(randomFn() * lines.length);
	return lines[Math.max(0, Math.min(lines.length - 1, index))];
};

function applyLoadingLines() {
	try {
		document.querySelectorAll('[data-loading-line]').forEach(el => {
			el.textContent = pickLoadingLine();
		});
	} catch (e) {
		// Any failure here leaves the template's own static "Loading..."
		// text in place -- never throw past this.
	}
};

// code run on load
applyLoadingLines();
```

### `frontend/templates/base.html` — register the script

Add right after the existing `general.js` include (before `{% block js %}`), so it
loads on every page, deferred like its siblings:

```diff
 	<script src="{{ url_for('static', filename='js/auth.js') }}"></script>
 	<script src="{{ url_for('static', filename='js/general.js') }}" defer></script>
+	<script src="{{ url_for('static', filename='js/loading_lines.js') }}" defer></script>
 	{% block js %}
 	{% endblock js %}
```

### `frontend/templates/volumes.html` — opt the library-loading heading in

```diff
 	<div id="loading-library" class="loading-screen">
-		<h2>Loading...</h2>
+		<h2 data-loading-line>Loading...</h2>
 		<p id="massedit-progress"></p>
```

### `frontend/templates/view_volume.html` — opt the volume-detail heading in

```diff
 <div class="loading-container">
 	<div id="loading-screen" class="loading-screen">
-		<h2>Loading...</h2>
+		<h2 data-loading-line>Loading...</h2>
 	</div>
```

### `frontend/templates/library_import.html` — opt the import-scan heading in

```diff
 	<div id="loading-window" class="hidden">
-		<h2>Loading...</h2>
+		<h2 data-loading-line>Loading...</h2>
 	</div>
```

That's the complete patch: one new file, four one-line template diffs. No backend
changes, no new dependencies, no config surface.

## Why this satisfies the task note

- "Radarr/Sonarr-style playful loading copy" — ten comic-flavored lines, easy to
  extend by appending to `LOADING_LINES`.
- "centralized mechanism" — one array, one pure lookup function
  (`pickLoadingLine`), one apply function (`applyLoadingLines`), one script include.
- "easy to extend and test" — `pickLoadingLine(lines, randomFn)` takes its
  dependencies as arguments, so a future test (e.g. Vitest/Jest if one is ever
  added) can assert `pickLoadingLine(["a"], () => 0) === "a"` without touching the
  DOM or wiring up a browser.
- "Keep ordinary loading behavior functional when JavaScript or data lookup
  fails" — the template's literal `Loading...` text is the fallback (unset
  `data-loading-line` targets nothing if the script never runs; `pickLoadingLine`
  itself falls back to `DEFAULT_LOADING_LINE` on an empty/invalid array; the whole
  apply step is wrapped in try/catch).

## Verification possible / actually done this session

- Confirmed all three `<h2>Loading...</h2>` locations, their surrounding
  `.loading-screen` markup, and the `defer` + top-level-script-execution pattern
  used by every other page script, by reading the live fork source directly.
- Confirmed there is no existing frontend build step (no `package.json`, no
  bundler) — a plain `<script defer>` is the correct integration point, matching
  every other `frontend/static/js/*.js` file already wired into `base.html`.
- Did not and could not run the Kapowarr app itself, `pytest`, or any linter
  against this patch (no target-repo access) — this is a design/patch handoff, not
  a verified merge.

## Verification still needed (by whichever session/human applies this)

- Apply the patch, run the app locally, and confirm each of the three loading
  screens shows a random line from `LOADING_LINES` and that the text is fully
  replaced (not appended) before the real content swaps in.
- Confirm `defer` execution order still resolves `document.querySelectorAll` after
  the DOM contains the `[data-loading-line]` elements (it does — templates are
  server-rendered before any script runs), and that `loading_lines.js` loading
  after `general.js` doesn't introduce an ordering issue (it has no dependency on
  `general.js`, so order between the two doesn't matter beyond both preceding
  `{% block js %}`'s page-specific scripts, which is already true in the diff
  above).
- Disable JavaScript (or block the script) in a browser and confirm all three
  screens still read the plain `"Loading..."` text, per the task's explicit
  fallback requirement.

## Safety boundaries respected

- No upstream (`Casvt/Kapowarr`) reads/writes beyond what public GitHub already
  serves; this session made no upstream PR/issue and modified nothing there.
- No secrets, DNS, billing, or deploy actions.
- No code was pushed anywhere — this file is documentation only, landing in
  `conductor` via a normal reversible PR.
