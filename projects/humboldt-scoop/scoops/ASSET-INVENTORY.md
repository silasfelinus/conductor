# Humboldt Scoop WordPress asset inventory

## Scope

Task `humboldt-scoop/t-004` asked to confirm whether the imported WordPress theme, plugins, uploads, and database assets are present before build work continues.

This inventory used connected GitHub file reads. The automation runtime did not provide a local clone or a recursive directory listing API, and GitHub code search timed out during broad searches, so the conclusion below is conservative: files explicitly verified as present are listed as present; missing common paths are listed as not found; anything not directly readable should be treated as unconfirmed until someone runs a local recursive listing.

## Summary

The checked-in import currently appears to contain WordPress core/config scaffolding, but not the business-specific site assets needed to restore the existing Humboldt Scoop site.

| Asset area | Status | Evidence |
| --- | --- | --- |
| Business-specific theme | Missing / unconfirmed | `wp-content/themes/index.php` exists and is only the WordPress guard file. Common default theme path `wp-content/themes/twentytwentyfour/style.css` was not found. |
| Plugins | Missing / unconfirmed | `wp-content/plugins/index.php` exists and is only the WordPress guard file. No plugin directory was directly verified. |
| Uploads / media library | Missing / unconfirmed | `wp-content/uploads/index.php` was not found, and no upload subdirectory was directly verified. |
| Database import | Missing / unconfirmed | No SQL or database import file was directly verified in the checked paths. Broad code search for database terms timed out. |
| WordPress config | Present | `wp-config.php` is present and Docker-aware, using `WORDPRESS_*` environment variables with fallback values. |
| Permalink rules | Incomplete | `.htaccess` exists, but the WordPress-managed block has no rewrite rules between `BEGIN WordPress` and `END WordPress`. |

## Files directly verified

- `projects/humboldt-scoop/scoops/wp-config.php`
- `projects/humboldt-scoop/scoops/.htaccess`
- `projects/humboldt-scoop/scoops/wp-content/themes/index.php`
- `projects/humboldt-scoop/scoops/wp-content/plugins/index.php`

## Paths checked and not found

- `projects/humboldt-scoop/scoops/wp-content/uploads/index.php`
- `projects/humboldt-scoop/scoops/wp-content/themes/twentytwentyfour/style.css`
- `projects/humboldt-scoop/scoops/wp-content/themes/twentytwentythree/style.css`
- `projects/humboldt-scoop/scoops/wp-content/mu-plugins/index.php`

## Recommended next step

Before build/import work continues, collect and stage the missing assets intentionally:

1. The active production theme directory under `wp-content/themes/<theme-name>/`.
2. Required plugins under `wp-content/plugins/<plugin-name>/`, excluding generated caches and private config.
3. Media uploads under `wp-content/uploads/`, or a documented external media migration plan if uploads are too large for git.
4. A sanitized local/staging database import, or a private import path if it contains customer data.

Do not commit private configuration, live customer data, production credentials, or anything deployment-related. If the database import contains customer/contact data, keep the import gated for Silas and document only the expected filename/path in git.

## Local verification commands for Silas or a local worker

When local git access is available, run recursive checks from the repo root for:

- first-level directories under `projects/humboldt-scoop/scoops/wp-content/themes`
- first-level directories under `projects/humboldt-scoop/scoops/wp-content/plugins`
- file counts under `projects/humboldt-scoop/scoops/wp-content/uploads`
- database import files under `projects/humboldt-scoop/scoops`

Keep the output summarized in this file rather than pasting a giant media-file listing into the roadmap.
