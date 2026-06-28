# Humboldt Scoop CMS — Customer and Property Schema

This schema is a TypeScript definition-first model for the early CMS. It does not create database migrations, touch a real database, import real customers, or wire payments. The companion file is `src/schema.ts`, with dummy seed data for local development.

## Model map

- `Customer` is the account-level contact record. It stores basic contact details, lifecycle status, and internal notes.
- `Property` belongs to one customer and represents a yard or service location. A customer can have multiple properties, but one can be marked primary.
- `Pet` belongs to both a customer and a property so service notes can stay tied to the actual yard where the pet is encountered.
- `ServicePlan` belongs to a customer and property. It captures schedule frequency, preferred weekday, pricing, and whether the plan is draft, active, paused, or cancelled.
- `Visit` belongs to a service plan, customer, and property. It records scheduled and completed work without assuming routing or crew assignment yet.
- `DraftInvoice` and `DraftInvoiceLineItem` are intentionally draft-only. They model invoice previews from visits without live payment collection.

## Design choices

IDs are stable string identifiers in the schema so seed data can be readable and easy to diff. A future persistence layer can map these to database IDs or keep them as external-safe slugs/UUIDs.

Money is stored in cents as integers. That avoids floating-point math weirdness when future invoice drafts start adding recurring visits, one-time cleanups, and adjustments.

Scheduling is deliberately simple: `ServicePlan.frequency` plus `preferredWeekday` is enough for the next milestone to generate recurring visits without committing to a complex calendar engine too early.

Access and pet temperament are enums because they are operationally important during service. Free-form notes remain available for edge cases, because yards are chaos goblins with fences.

Invoices are present but draft-only. This keeps milestone five visible in the data model while respecting the rule that no live billing or payment integration should happen without human approval.

## Guardrails

- Dummy data only.
- No migrations against a real database.
- No real customer import.
- No live billing, payment processor, emails, SMS, or outward-facing notifications.
- Any future task that handles real customer data or payment collection should be marked `needs-human` before implementation.

## Likely next schema extensions

- Crew or operator assignment for visits.
- Service area and route grouping.
- Photo attachments for visit proof, if explicitly approved.
- Quote/estimate records for leads before conversion to an active service plan.
- Customer communication preferences, gated before any sending integration.
