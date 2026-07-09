# Hair by Superkate dedicated backend — Unraid Postgres setup

Date recorded: 2026-07-08

Silas created the initial dedicated Postgres database container on Unraid for the future Hair by Superkate backend.

## Non-secret connection facts

```txt
Database engine: Postgres
Container intent/name: hairbysuperkate-postgres
Database name: hairbysuperkate
App user: hbs_app
Port: 5433
Network exposure: no public access; internal/private only
Data path target: /mnt/user/appdata/hairbysuperkate-postgres
Timezone: UTC
Tailscale: reachable on Silas's Tailscale network from approved workers/agents that have explicit access
```

Do not store the database password in this repository, GitHub, roadmap notes, PR bodies, issue comments, or chat logs.

## Intended architecture

- The future Hair by Superkate backend service connects to this database over Silas's private Unraid/Docker/Tailscale network.
- The Android app must never connect directly to Postgres.
- The phone app should talk only to the dedicated backend API after sync is explicitly enabled.
- Local Android beta remains local-only until durable local persistence, export, app/device lock, and fake-data backend sync are verified.
- GitHub workers or LLM agents may use the Tailscale database route only for explicitly approved fake-data migrations, schema checks, connectivity checks, and non-destructive verification.

## First backend environment shape

Use environment variables like these in the backend runtime, but keep actual secret values outside GitHub:

```bash
HBS_DATABASE_URL=postgres://hbs_app:<secret>@hairbysuperkate-postgres:5433/hairbysuperkate
HBS_BUSINESS_SLUG=hair-by-superkate
HBS_ENV=local
```

If the backend container shares a Docker network with the database container, prefer the internal container name as host. If the backend or an approved worker runs from Tailscale instead, use the Tailscale/private host and keep the port private to the tailnet/LAN only.

## Minimum schema direction

The first fake-data schema should include:

```txt
businesses
users
customers
appointments
sync_state or sync_events
```

Every synced business-data row should include:

```txt
id
owner_id
business_slug
created_at
updated_at
deleted_at
sync_version
```

Use `business_slug = hair-by-superkate` even if the backend starts single-tenant.

## Safety gates

Workers may document, scaffold local/fake-data backend code, and write tests. Workers must not touch DNS, secrets, production deploy settings, public exposure, billing, analytics, direct-send email, or real customer-data sync without Silas explicitly approving that concrete action in-session.

Even with Tailscale access, agents must not run destructive database commands such as `DROP DATABASE`, `DROP TABLE`, `TRUNCATE`, production data rewrites, bulk deletes, or reset-style migration commands. Schema work should start with fake data and additive, reversible migrations.