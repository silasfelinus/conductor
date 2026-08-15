# t-003: Make the displayed application title configurable

**Target repo:** `silasfelinus/Kapowarr` (not in this session's GitHub scope — this
session covers `silasfelinus/conductor` and `silasfelinus/kind_robots` only, same
boundary hit by t-002; see `projects/kapowarr/docs/t-002-loading-lines.md`).

**Status:** patch fully designed and verified against the live fork source (read-only
clone, deleted after inspection). Not applied/pushed/tested in Kapowarr itself.

## What this does

Adds a `app_title` public setting (default: empty string → falls back to `"Kapowarr"`).
When Silas sets it in Settings → General, it replaces "Kapowarr" in:
- the browser tab title on every page (`base.html`, `login.html`, `page_not_found.html`)
- the login screen's `<h1>`
- the PWA manifest `name`/`short_name` (what shows on a home-screen install)

**Attribution is intentionally untouched.** The System Status page
(`frontend/templates/status.html`) already shows "Kapowarr version", a link to
`github.com/Casvt/Kapowarr`, and the upstream Donate link — none of that is part of
this patch, so upstream credit stays fully visible regardless of what title is set.
This satisfies the task note's "without obscuring the Kapowarr origin, license, or
attribution" requirement by leaving the one place attribution actually lives alone,
rather than trying to inject an attribution string into the renamed title itself.

Config-over-rename, per the task note: nothing is hard-coded to a fork name anywhere;
an empty setting reproduces upstream's exact current behavior byte-for-byte, so this
stays a trivial rebase target.

## Patch

### 1. `backend/base/definitions.py` — single source of truth for the default

Add to `class Constants` (near the other string constants, e.g. next to `DB_NAME`):

```python
    DEFAULT_APP_TITLE = "Kapowarr"
    "Displayed application title when no custom app_title setting is set"
```

### 2. `backend/internals/settings.py` — new public setting

In `PublicSettingsValues` (`dataclass(frozen=True)`), add one field. Placement:
right after `url_base: str = ''` reads naturally since both are "how the app presents
itself" settings, but any position in the dataclass works — order doesn't affect the
DB-backed generic get/set/reset/validate machinery, which is entirely field-driven
(`_insert_missing_settings`, `get_public_settings`, `update`, `__format_value` all key
off `__dataclass_fields__`, so a plain `str` field needs zero other code changes):

```python
    host: str = '0.0.0.0'
    port: int = 5656
    url_base: str = ''
    app_title: str = ''
```

That's the entire backend change needed for the setting itself — no special-casing in
`__format_value`/`__validate_settings` required since `str` already has a generic
isinstance-checked path, and empty string is a legal value (meaning "use default").

### 3. `frontend/ui.py` — resolve the title and pass it to every UI template

```python
from backend.internals.server import Server
from backend.internals.settings import Settings   # new import
from backend.base.definitions import Constants     # new import
```

```python
def render(filename: str, **kwargs: Any) -> str:
    app_title = Settings().get_public_settings().app_title or Constants.DEFAULT_APP_TITLE
    return render_template(
        filename, url_base=Server.url_base, app_title=app_title, **kwargs
    )
```

This covers every route that already goes through `render()` (`ui_login`,
`ui_volumes`, `ui_settings`, etc. — i.e. `base.html` and everything that extends it,
plus `login.html`) with one change.

Also update the PWA manifest so an installed home-screen icon reflects the same title:

```python
@ui.route('/manifest.json', methods=methods)
def ui_manifest():
    app_title = Settings().get_public_settings().app_title or Constants.DEFAULT_APP_TITLE
    return send_file(
        BytesIO(dumps(
            {
                "name": app_title,
                "short_name": app_title,
                "description": "Kapowarr is a software to build and manage a comic book library, fitting in the *arr suite of software.",
                ...  # unchanged below
```

(Only the `name`/`short_name` values change from the literal `"Kapowarr"` to
`app_title`; `description` intentionally keeps naming Kapowarr explicitly since it's
prose about what the software is, not a UI label.)

### 4. `backend/internals/server.py` — the 404 page doesn't go through `ui.py`'s `render()`

`Settings` is already imported here. One-line change to the existing handler:

```python
        @app.errorhandler(404)
        def not_found(e):
            if request.path.startswith(Constants.API_PREFIX):
                return {'error': 'NotFound', 'result': {}}, 404
            return render_template(
                'page_not_found.html',
                app_title=Settings().get_public_settings().app_title or Constants.DEFAULT_APP_TITLE
            )
```

### 5. `frontend/templates/base.html` — one-line template diff

```diff
-	<title>{% block title %}{% endblock %} - Kapowarr</title>
+	<title>{% block title %}{% endblock %} - {{ app_title }}</title>
```

### 6. `frontend/templates/login.html` — two-line template diff

```diff
-	<title>Login - Kapowarr</title>
+	<title>Login - {{ app_title }}</title>
 </head>
 <body>
 	<div id="text-container">
-		<h1>Kapowarr</h1>
+		<h1>{{ app_title }}</h1>
```

### 7. `frontend/templates/page_not_found.html` — one-line template diff

```diff
-	<title>Not found - Kapowarr</title>
+	<title>Not found - {{ app_title }}</title>
```

### 8. `frontend/templates/settings_general.html` — new field in the existing "Host" section

Add a row to the `fold-table` in the `Host` section, right after the Base URL row:

```diff
 				<tr>
 					<th><label for="url-base-input">Base URL</label></th>
 					<td>
 						<input type="text" id="url-base-input" spellcheck="false">
 						<p>For reverse proxy support (default is empty).</p>
 					</td>
 				</tr>
+				<tr>
+					<th><label for="app-title-input">Application Title</label></th>
+					<td>
+						<input type="text" id="app-title-input" spellcheck="false">
+						<p>
+							Custom title shown in the browser tab and on the login screen
+							(default is 'Kapowarr'). Leave empty to use the default. This does
+							not remove Kapowarr credit — the original project name, version,
+							and links stay visible on the System Status page.
+						</p>
+					</td>
+				</tr>
```

This field is not in the "Changing hosting settings will immediately restart
Kapowarr" `<p>` at the top of the Host section — it's a display-only string, not a
`host`/`port`/`url_base` value, so it correctly does **not** trigger
`hosting_changes`/a server restart in `frontend/api.py`'s `PUT /settings` handler
(that check is `s in ('host', 'port', 'url_base')` — `app_title` isn't in that tuple,
no change needed there).

### 9. `frontend/static/js/settings_general.js` — wire the field into load/save

In `fillSettings()`, alongside the other Host-section fields:

```diff
 		document.querySelector('#url-base-input').value = json.result.url_base;
+		document.querySelector('#app-title-input').value = json.result.app_title;
 		document.querySelector('#username-input').value = json.result.auth_username;
```

In `saveSettings()`, alongside the other Host-section fields in the `data` object:

```diff
 		'url_base': document.querySelector('#url-base-input').value,
+		'app_title': document.querySelector('#app-title-input').value,
 		'auth_username': '',
```

No new error-handling branch needed — `app_title` has no server-side validation
beyond the generic `str` type check, so `InvalidKeyValue` can't be raised for it in
practice (any string value is accepted, including empty).

## Verification performed (this session)

- Read the live `settings.py` dataclass/generic-settings machinery
  (`_insert_missing_settings`, `get_public_settings`, `update`, `__format_value`,
  `__validate_settings`) end to end and confirmed a plain `str` field needs no
  special-case code anywhere in that pipeline.
- Confirmed `frontend/api.py`'s `PUT /settings` `hosting_changes`/`proxy_changes`
  restart-trigger tuples explicitly enumerate their trigger keys, so adding
  `app_title` cannot accidentally cause a hosting-settings restart.
- Confirmed `page_not_found.html` is rendered directly via `render_template()` in
  `server.py`'s `404` errorhandler (not through `ui.py`'s `render()` helper), which is
  why it needs its own one-line change to receive `app_title` — every other page
  extends `base.html` and goes through `ui.py`'s `render()`, so one change there
  covers all of them.
- Confirmed the only other places the literal string `"Kapowarr"` appears as
  user-visible chrome (as opposed to prose about the project, e.g. help text in
  `settings_download_clients.html`, or `status.html`'s intentionally-untouched
  attribution) are exactly the three covered here: page `<title>`, the login `<h1>`,
  and the PWA manifest `name`/`short_name`. The header/nav (`base.html`) shows only
  the favicon image, no "Kapowarr" text, so nothing there needs changing.

**Not verified** (no Kapowarr-repo write access from this session): the patch has not
been applied, and the app has not actually been run/tested with a custom title set.

## TO APPROVE (Silas)

Apply this patch in a Kapowarr-scoped session/PR (or paste it in yourself), confirm
the settings form round-trips (`GET /settings` reflects a saved `app_title`, tab title
and login heading update, manifest name updates on a fresh install), then set
`status: done` on `kapowarr/t-003` in `projects/kapowarr/roadmap.yaml`. Soft gate —
other kapowarr tasks are unaffected and remain pickable in the meantime.
