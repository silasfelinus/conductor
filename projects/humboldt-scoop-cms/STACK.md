# Humboldt Scoop CMS — Stack Proposal

## Recommendation: small TypeScript HTTP app with Hono

Use a small Node.js TypeScript service built with Hono and the official `@hono/node-server` adapter.

Why this fits the first milestone:

- It is simple to self-host anywhere Node can run, including Docker later.
- It avoids pulling in a full framework before the product shape is clear.
- The route model stays close to future API needs: customers, yards, pets, service plans, visits, and draft invoices.
- It can grow into either a JSON API for a separate frontend or a tiny server-rendered/admin UI later.
- It keeps real customer/payment integrations out of scope until explicitly approved.

Current scaffold:

- `src/server.ts` starts the app.
- `GET /health` returns a JSON health check.
- `GET /` returns a tiny service descriptor.
- `npm run dev` runs locally with `tsx`.
- `npm run build` type-checks and emits JavaScript to `dist/`.
- `npm start` runs the built server.

## Alternative: Nuxt/Nitro app

Nuxt/Nitro would be a good alternative if the first usable milestone needs a polished admin UI immediately. It brings file-based API routes, server rendering, and familiar Kind Robots ergonomics. The tradeoff is more framework surface area before the data model and workflow are settled.

## Guardrails

- Dummy/seed data only until Silas approves real data entry.
- No payment processor, live billing, customer import, deployment, DNS, or secrets in automated worker tasks.
- Treat invoicing as draft-only until a human-gated task approves anything outward-facing.
