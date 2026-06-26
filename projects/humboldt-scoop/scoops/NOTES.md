# Humboldt Scoop imported site audit

## Scope

This is an inventory note for `projects/humboldt-scoop/scoops/`. I did not change site code.

The imported app is a WordPress/PHP site. The root `index.php` is the standard WordPress front controller that loads `wp-blog-header.php`, and `wp-config.php` is the Docker-aware WordPress configuration variant that reads database settings and salts from environment variables when present.

## Files checked

- `index.php` — standard WordPress entrypoint.
- `wp-config.php` — Docker/environment based configuration.
- `.htaccess` — WordPress managed block exists, but it is currently empty between `BEGIN WordPress` and `END WordPress`.
- `wp-content/themes/index.php` and `wp-content/plugins/index.php` — placeholder guard files only.

GitHub code search timed out during this audit, and direct local clone was blocked by the runtime, so this note is based on targeted repository file reads rather than a full recursive directory listing.

## Configuration findings

`wp-config.php` expects these environment variables when run in a containerized environment:

- `WORDPRESS_DB_NAME`
- `WORDPRESS_DB_USER`
- `WORDPRESS_DB_PASSWORD`
- `WORDPRESS_DB_HOST`
- `WORDPRESS_DB_CHARSET`
- `WORDPRESS_DB_COLLATE`
- `WORDPRESS_TABLE_PREFIX`
- `WORDPRESS_DEBUG`
- `WORDPRESS_CONFIG_EXTRA`
- WordPress auth key and salt variables such as `WORDPRESS_AUTH_KEY`, `WORDPRESS_SECURE_AUTH_KEY`, and matching salt values.

The file defaults `DB_HOST` to `mysql`, which strongly suggests the expected local/dev setup is a WordPress container plus a MySQL/MariaDB container on the same Docker network.

## Build/run notes

No `Dockerfile`, `compose.yaml`, `docker-compose.yml`, `.env`, or README was found at the expected root paths during targeted checks. Because the site itself is WordPress, there may not be a build step beyond running PHP/Apache with a database.

A reasonable local smoke-test setup would be:

```bash
cd projects/humboldt-scoop/scoops

docker network create humboldt-scoop || true

docker run --name humboldt-scoop-db \
  --network humboldt-scoop \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wordpress \
  -e MYSQL_PASSWORD=wordpress \
  -e MYSQL_RANDOM_ROOT_PASSWORD=1 \
  -d mysql:8

docker run --name humboldt-scoop-wp \
  --network humboldt-scoop \
  -p 8080:80 \
  -e WORDPRESS_DB_HOST=humboldt-scoop-db:3306 \
  -e WORDPRESS_DB_NAME=wordpress \
  -e WORDPRESS_DB_USER=wordpress \
  -e WORDPRESS_DB_PASSWORD=wordpress \
  -v "$PWD":/var/www/html \
  -d wordpress:php8.2-apache
```

Then open `http://localhost:8080` and complete the WordPress installer or import a database dump if one exists outside this repo.

Cleanup:

```bash
docker rm -f humboldt-scoop-wp humboldt-scoop-db
```

## Needs attention

1. Add a checked-in `compose.yaml` and `.env.example` so the site can be started consistently without hand-built `docker run` commands.
2. Replace the hardcoded fallback auth keys/salts in `wp-config.php` before any public/staging deployment, or require all salt variables in environment configuration.
3. Confirm whether the theme, plugins, uploads, and database dump were imported. The files I could directly verify look like core WordPress scaffolding rather than the business-specific site content.
4. If pretty permalinks are required, regenerate or commit the expected `.htaccess` rewrite block through WordPress/admin tooling.

## Verification

- Read the steering/control files and roadmap.
- Confirmed GitHub access and repo permissions.
- Checked the WordPress root/config files via connected GitHub file reads.
- Could not perform a local Docker run because this automation runtime blocked local clone/network access.
