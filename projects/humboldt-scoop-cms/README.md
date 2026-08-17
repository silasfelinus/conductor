# humboldt-scoop-cms — canonical Humboldt Scoop Solutions project

The slug is historical. **This is now the one continuing Conductor project for the entire Humboldt Scoop Solutions product.**

It owns coordination from the already-working public website forward through:

- public website and quote/signup flow
- customer web portal
- admin/business-management portal
- dispatcher and route planning
- scooper/worker portal and field workflow
- shared customer/property/pet/visit/billing data
- notifications, proof-of-service, and operational tooling
- Android and iOS apps for clients and staff
- production hardening, beta distribution, and App Store / Play Store release

The original `humboldt-scoop` project is **finished** and historical. Do not create a third HSS project for mobile, portal, worker, or admin work; extend this roadmap instead.

## Canonical code

All implementation work lives in [`silasfelinus/humboldtscoopsolutions`](https://github.com/silasfelinus/humboldtscoopsolutions):

| Area | Canonical path |
|---|---|
| Public WordPress site + customer portal/admin plugin | `site/` |
| CMS, route planner, dispatcher, shared API | `cms/` |
| Flutter mobile client | `field-client/` |
| Architecture, integration, backlog, provenance | `docs/` |

The code copies still present under this Conductor directory are historical imports only. **Never implement against them.** If archaeology here reveals something better, port it into the canonical repo and record that salvage there.

## Identity model

Do not model staff as a single mutually-exclusive role enum. **Admin/business-management capability and scooper/worker capability are independent grants. A person may have either or both.**

That matters immediately: a business owner/manager may also work routes. Authentication and every web/mobile surface should derive available actions from capabilities, not force a user into one persona.

Customers remain a separate portal audience, while authorized representatives are customer-account delegates with their own limited permissions.

## History

Tasks `t-001` through `t-012` built the original CMS/routing/field-client foundation. Their detailed implementation notes remain in Git history and are summarized in `HISTORY.md`. The current roadmap preserves those task IDs as completed foundation work and continues from there.
