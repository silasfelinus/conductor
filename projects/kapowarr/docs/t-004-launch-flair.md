# kapowarr/t-004 — Add database-driven launch flair (handoff)

date: 2026-08-15
target repository: `silasfelinus/Kapowarr` (not `conductor` or `kind_robots`)
intended branch: `worker/kapowarr-t-004`
status: this conductor session cannot push to `silasfelinus/Kapowarr` — its GitHub
  access is scoped to `silasfelinus/conductor` and `silasfelinus/kind_robots` only
  (see `projects/kapowarr/DESIGN-BRIEF.md`, and t-002/t-003's handoffs, which hit the
  identical wall). This document preserves the fully-specified patch so a session
  with `Kapowarr` in its GitHub scope — or Silas directly — can apply it without
  re-deriving the design.

## What was actually done this session

Read-only inspection of the live `silasfelinus/Kapowarr` source (`backend/implementations/volumes.py`'s
`Library` class, `frontend/api.py`'s route table, `frontend/templates/base.html`'s
header markup, `frontend/static/js/{auth,general,volumes}.js`, and
`frontend/static/css/general.css`'s header rules and theme variables) to ground this
patch in the fork's real data-access and page-load structure rather than guessing.
No writes were made to that repository.

## Where "launch" actually happens

Kapowarr has no dedicated splash/loading screen at the app level (t-002 already
covers the three per-page in-content loading states). The one element present on
every authenticated page, exactly once, is the `<header>` in `frontend/templates/base.html`
— it is not overridden by any page template, so it is the natural, minimal place for
a once-per-page-load flourish. The unauthenticated `login.html` does **not** extend
`base.html` (no header at all), so this feature never needs to run before login —
`usingApiKey()` (defined in `auth.js`, loaded non-deferred ahead of every other
script) is always safe to call from a script registered in `base.html`.

## Where the title data actually lives

`backend/implementations/volumes.py`'s `Library` class already has `get_stats()`
(a `SELECT ... FROM volumes` aggregate) and `get_public_volumes()`. Volume titles
live in the `volumes.title` column, the same one used everywhere else in the file
(`Library.search()`'s `match_title` filtering, `Library.get_public_volumes()`'s
`SELECT`). No existing method returns a single random title — this patch adds one.

## Design (matches DESIGN-BRIEF.md's m1 personality-layer rules)

Same shape as t-002 (one centralized data source + one pure function + one opt-in
element), but sourced from the real library instead of a static array, per the task
note's "database-driven" requirement:

- **Backend**: `Library.get_random_title()` — one `SELECT title FROM volumes ORDER
  BY RANDOM() LIMIT 1` query, returns `None` when the library is empty. `RANDOM()`
  is native SQLite (Kapowarr's DB engine, confirmed via the existing raw-SQL style
  throughout `volumes.py`), so no new dependency.
- **API**: `GET /api/system/launchflair` — authenticated (`@auth`, matching every
  other `/system/*` route except `/public`), returns `{"title": <str or null>}`.
  Deliberately returns only the raw title, not a pre-built sentence — keeps the
  playful-copy templates on the frontend, next to `loading_lines.js`'s equivalent
  array, rather than splitting personality-layer copy across both languages.
- **Frontend**: new `launch_flair.js`, registered in `base.html` right after
  `loading_lines.js`. `buildLaunchFlair(title, ...)` is a pure function (title,
  templates, fallback lines, and a `randomFn` all passed as arguments, exactly like
  t-002's `pickLoadingLine`) so it's unit-testable without the DOM or a real fetch.
  It **sanitizes and truncates** the raw DB title (strips control characters,
  truncates to 80 chars with an ellipsis) before formatting it into a template, and
  the result is written via `textContent` (never `innerHTML`), so a maliciously or
  accidentally crafted title (e.g. containing `<script>`) can never execute — it can
  only ever render as inert text, truncated. An empty/null title (empty library) or
  a failed/errored fetch both resolve to one of the generic `DEFAULT_FLAIR_LINES` —
  never a blank half-sentence, matching the task note's explicit "deterministic
  generic fallback for empty or unavailable libraries."

## Exact patch

### `backend/implementations/volumes.py` — add `Library.get_random_title()`

Insert right after `get_stats()` (before the existing `get_volumes()` classmethod):

```diff
             FROM v;
         """).fetchonedict() or {}
         return result

+    @classmethod
+    def get_random_title(cls) -> Union[str, None]:
+        """Get the title of a random volume in the library, for display
+        purposes only (e.g. launch flair). Not suitable for anything that
+        needs a stable or weighted selection.
+
+        Returns:
+            Union[str, None]: The title of a random volume, or `None` if the
+                library is empty.
+        """
+        result = get_db().execute(
+            "SELECT title FROM volumes ORDER BY RANDOM() LIMIT 1;"
+        ).fetchonedict()
+        return result['title'] if result else None
+
     @classmethod
     def get_volumes(cls) -> List[int]:
         """Get a list of the IDs of all the volumes.
```

(`Union` is already imported at the top of the file — no new import needed.)

### `frontend/api.py` — new endpoint

Insert right after `api_volumes_stats()` (which already imports and uses `Library`):

```diff
 @api.route('/volumes/stats', methods=['GET'])
 @error_handler
 @auth
 def api_volumes_stats():
     result = Library.get_stats()
     return return_api(result)


+@api.route('/system/launchflair', methods=['GET'])
+@error_handler
+@auth
+def api_launch_flair():
+    result = {'title': Library.get_random_title()}
+    return return_api(result)
+
+
 @api.route('/volumes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
```

### New file: `frontend/static/js/launch_flair.js`

```js
//
// Database-driven launch flair
//
// Personal-fork QoL touch, sibling to loading_lines.js: on each page load,
// shows one playful line in the header built from a random comic title
// already in the local library -- e.g. "Currently rereading Saga..." -- or
// a generic fallback line when the library is empty or the title couldn't
// be fetched. Centralized here (one template array + one pure build
// function) so the personality-layer copy stays in one place next to its
// static-line sibling.
//
// Kept pure and dependency-free on purpose: buildLaunchFlair() takes the
// title, templates, fallback lines, and random function as explicit
// arguments, so it's unit-testable without the DOM or a real fetch.
//

const LAUNCH_FLAIR_TEMPLATES = [
	"Currently rereading {title}...",
	"Dusting off {title}...",
	"Fresh off the shelf: {title}.",
	"Tonight's pick: {title}.",
	"Keeping an eye on {title}...",
];

// Shown when the library is empty or the title couldn't be fetched --
// deterministic, no randomness, so an empty/failed state never looks broken.
const DEFAULT_FLAIR_LINES = [
	"Ready for your first longbox.",
	"No comics yet -- add a volume to get started.",
];

const MAX_TITLE_LENGTH = 80;

// Strips control characters and truncates. The result is always written via
// textContent (never innerHTML) by applyLaunchFlair(), so this is a display
// safeguard against garbled/oversized data, not the injection defense --
// textContent is what actually makes injection impossible.
function sanitizeTitle(title) {
	if (typeof title !== 'string')
		return '';

	// eslint-disable-next-line no-control-regex
	const cleaned = title.replace(/[\x00-\x1F\x7F]/g, '').trim();

	if (cleaned.length <= MAX_TITLE_LENGTH)
		return cleaned;

	return cleaned.slice(0, MAX_TITLE_LENGTH - 1).trimEnd() + '…';
}

function pickRandom(list, randomFn = Math.random) {
	const index = Math.floor(randomFn() * list.length);
	return list[Math.max(0, Math.min(list.length - 1, index))];
}

function buildLaunchFlair(
	title,
	templates = LAUNCH_FLAIR_TEMPLATES,
	fallbackLines = DEFAULT_FLAIR_LINES,
	randomFn = Math.random
) {
	const clean = sanitizeTitle(title);

	if (!clean)
		return pickRandom(fallbackLines, randomFn);

	return pickRandom(templates, randomFn).replace('{title}', clean);
}

async function applyLaunchFlair() {
	const el = document.querySelector('#launch-flair');
	if (!el) return;

	try {
		const api_key = await usingApiKey(false);
		if (!api_key) return;

		const response = await fetchAPI('/system/launchflair', api_key);
		el.textContent = buildLaunchFlair(response.result.title);
	} catch (e) {
		// Any failure here leaves the header exactly as it was rendered
		// (empty) -- never throw past this, never leave a half-built line.
	}
}

// code run on load
applyLaunchFlair();
```

### `frontend/templates/base.html` — header element + script registration

```diff
 	<script src="{{ url_for('static', filename='js/auth.js') }}"></script>
 	<script src="{{ url_for('static', filename='js/general.js') }}" defer></script>
 	<script src="{{ url_for('static', filename='js/loading_lines.js') }}" defer></script>
+	<script src="{{ url_for('static', filename='js/launch_flair.js') }}" defer></script>
 	{% block js %}
 	{% endblock js %}
```

```diff
 	<header>
 		<div class="menu-title-container">
 			<button id="toggle-nav" aria-label="Toggle menu" aria-hidden="true">
 				<img src="{{url_base}}/static/img/menu.svg" alt="">
 			</button>
 			<a href="{{url_base}}/" aria-label="Go to homepage">
 				<img src="{{ url_for('static', filename='img/favicon.svg') }}" alt="">
 			</a>
+			<p id="launch-flair" aria-live="polite"></p>
 		</div>
 		{% block right_side_header %}
 		{% endblock %}
 	</header>
```

(The third line of `base.html`'s diff above assumes t-002's `loading_lines.js`
`<script>` line has already been applied; if t-002 hasn't landed yet, add
`launch_flair.js`'s line directly after `general.js`'s instead — the two scripts
have no dependency on each other, only on `auth.js`/`general.js`.)

### `frontend/static/css/general.css` — style the flourish

Insert right after the existing `.menu-title-container > a` rule:

```diff
 .menu-title-container > a {
 	width: 3rem;
 }

+#launch-flair {
+	color: var(--header-color);
+	opacity: .75;
+	font-style: italic;
+	white-space: nowrap;
+	overflow: hidden;
+	text-overflow: ellipsis;
+}
+
 /*  */
 /* Nav bar */
 /*  */
```

That's the complete patch: one new backend method, one new API route, one new
frontend file, and three small template/CSS additions. No new dependencies, no new
config surface, no schema change (reads the existing `volumes.title` column).

## Why this satisfies the task note

- "Optionally derive a playful line ... from a random comic/title already in the
  local database" — `Library.get_random_title()` reads directly from `volumes`, no
  new table or synced cache.
- "Visual flourish" — a small italicized header line, styled with the existing
  theme variables (`--header-color`), so it matches both the light and dark themes
  already defined in `general.css` without new tokens.
- "Sanitize displayed data" — `sanitizeTitle()` strips control characters and
  truncates; the result is written via `textContent`, never `innerHTML`, so DB
  content can never be interpreted as markup regardless of what it contains.
- "Deterministic generic fallback for empty or unavailable libraries" —
  `buildLaunchFlair()` falls back to `DEFAULT_FLAIR_LINES` whenever the title is
  empty/null (empty library) or missing, and `applyLaunchFlair()`'s try/catch
  ensures a network/auth failure leaves the header blank rather than broken (no
  half-built sentence, no thrown error visible to the user).

## Verification possible / actually done this session

- Confirmed `backend/implementations/volumes.py`'s `Library` class already runs raw
  SQL (`get_stats()`, `get_public_volumes()`) against a `volumes` table with a
  `title` column, and that `Union` is already imported for the new method's return
  type.
- Confirmed `frontend/api.py`'s existing `/volumes/stats` route is the closest
  precedent for a simple authenticated `Library`-backed GET endpoint, and copied its
  shape (`@error_handler`, `@auth`, `return_api`).
- Confirmed `base.html`'s `<header>` is rendered on every authenticated page (not
  overridden by any page template) and that unauthenticated `login.html` does not
  extend `base.html` at all, so no unauthenticated code path is affected.
- Confirmed `auth.js` (defines `usingApiKey`) loads non-deferred, ahead of every
  deferred script including the new one, and that `general.js` (defines
  `fetchAPI`) is deferred but ordered before `launch_flair.js` in the script list —
  both are available by the time `applyLaunchFlair()` runs.
- Did not and could not run the Kapowarr app itself, `pytest`, or any linter against
  this patch (no target-repo access) — this is a design/patch handoff, not a
  verified merge.

## Verification still needed (by whichever session/human applies this)

- Apply the patch, run the app with a non-empty library, and confirm the header
  shows one of the `LAUNCH_FLAIR_TEMPLATES` lines with a real title substituted, on
  a fresh page load.
- Empty the library (or test against a fresh DB) and confirm a `DEFAULT_FLAIR_LINES`
  line shows instead — never a blank template or literal `{title}`.
- Confirm a title longer than 80 characters truncates with an ellipsis and a title
  containing HTML-special characters (e.g. `<b>Test</b>`) renders as literal inert
  text, not markup.
- Block or fail the `/api/system/launchflair` request (e.g. devtools network
  throttling/offline) and confirm the header area stays empty rather than showing a
  stale or broken line.
- Confirm the element doesn't visually collide with `right_side_header` content
  (e.g. the search bar on `volumes.html`) at narrow viewport widths — `white-space:
  nowrap` + `overflow: hidden` + `text-overflow: ellipsis` should keep it from
  wrapping or pushing the layout, but this needs an actual browser check.

## Safety boundaries respected

- No upstream (`Casvt/Kapowarr`) reads/writes beyond what public GitHub already
  serves; this session made no upstream PR/issue and modified nothing there.
- No secrets, DNS, billing, or deploy actions.
- No code was pushed anywhere — this file is documentation only, landing in
  `conductor` via a normal reversible PR.
