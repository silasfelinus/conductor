# Hair by Superkate Backend

Local/fake-data backend scaffold for the Superkate Services Calculator sync runway.

This is intentionally **not** a production deployment. It provides a small Python service layer, in-memory test store, validation helpers, and unit tests matching the backend API/schema contract in:

```txt
projects/superkate-services-calculator/docs/backend-api-schema-contract.md
```

## Safety boundaries

This scaffold does not:

- connect to production Postgres;
- store secrets;
- touch DNS, deploy settings, billing, analytics, or public admin surfaces;
- send receipt email;
- upload or sync real customer data.

The future production database details are documented separately in:

```txt
projects/superkate-services-calculator/docs/unraid-postgres-setup.md
```

## Local test run

From this directory:

```bash
python -m unittest discover -s tests
```

The tests use only the Python standard library and an in-memory fake store.

## Optional local health server

```bash
python -m hbs_backend.app
```

Then visit:

```txt
http://127.0.0.1:8787/api/superkate/health
```

## Fake auth

Sync endpoints require a local test auth header:

```txt
Authorization: Bearer local-test-token
```

That maps to the fake owner:

```txt
test-owner-superkate
```

## Environment shape for later

Do not commit real secrets. A future runtime should use environment variables such as:

```bash
HBS_ENV=local
HBS_BUSINESS_SLUG=hair-by-superkate
HBS_DATABASE_URL=postgres://hbs_app:<secret>@hairbysuperkate-postgres:5433/hairbysuperkate
```

For now, `HBS_DATABASE_URL` is read only as configuration shape. This scaffold never opens it.
