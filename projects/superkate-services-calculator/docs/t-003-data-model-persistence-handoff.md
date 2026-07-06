# Superkate Services Calculator — Appointment and Customer Persistence Handoff

Date: 2026-07-06
Task: `superkate-services-calculator/t-003`
Status: implementation handoff, not live code

## Why this handoff exists

`t-003` asks for the actual appointment/customer persistence implementation. In this connector-only Worker run, I can update the conductor repository, but I cannot run the application, inspect or write a separate target app repository, install dependencies, execute `scripts/resolve_deps.py`, or use `KR_API_TOKEN`/runtime secrets.

Because the task is software implementation and customer-data related, I am not marking it done from a documentation-only change. This file preserves the exact implementation shape that should be applied in the app repository/runtime when branch/write/test access is available.

## Target outcome

Build the first durable persistence layer for the Superkate Services Calculator:

- `Customer` records with name, optional email, and timestamps.
- `Appointment` records with customer linkage, client name snapshot, appointment date, cents-based money fields, minute-based time field, calculated total, and timestamps.
- Local-first storage as the UI source of truth.
- Sync-ready metadata without requiring sync to be fully implemented in this task.
- No customer names, emails, or appointment records written to logs.

## Data model contract

### Customer

```ts
export interface SuperkateCustomer {
  id: string
  name: string
  email: string | null
  createdAt: string
  updatedAt: string
}
```

Validation rules:

- `name` is required after trimming.
- `email` is optional and stored as `null` when blank.
- Email validation should be gentle in beta: reject obvious malformed values when supplied, but do not require an email for customer creation.
- `createdAt` and `updatedAt` are ISO strings or platform-native date values normalized at the storage boundary.

### Appointment

```ts
export interface SuperkateAppointment {
  id: string
  customerId: string | null
  clientNameSnapshot: string
  appointmentDate: string
  hourlyRateCents: number
  timeSpentMinutes: number
  productCostCents: number
  appointmentTotalCents: number
  createdAt: string
  updatedAt: string
  syncedAt: string | null
}
```

Validation rules:

- `clientNameSnapshot` is required after trimming.
- `appointmentDate` is required.
- `hourlyRateCents` must be a non-negative integer.
- `timeSpentMinutes` must be a positive integer.
- `productCostCents` must be a non-negative integer and defaults to `0`.
- `appointmentTotalCents` is always calculated, never trusted from UI input.
- `customerId` may be `null` for a one-off client, but if present it must reference a stored customer.
- `syncedAt` starts as `null` until sync implementation marks the record synced.

## Total calculation

Money is stored as cents. Time is stored as minutes.

```ts
export function calculateAppointmentTotalCents(input: {
  hourlyRateCents: number
  timeSpentMinutes: number
  productCostCents?: number | null
}) {
  const productCostCents = input.productCostCents ?? 0
  return Math.round((input.hourlyRateCents * input.timeSpentMinutes) / 60) + productCostCents
}
```

Examples:

- $100/hour × 90 minutes + $25 product = `10000 * 90 / 60 + 2500 = 17500` cents.
- $80/hour × 45 minutes + $0 product = `8000 * 45 / 60 = 6000` cents.

Use integer cents at every API/store/storage boundary. UI formatting can convert to dollars only for display.

## Recommended local persistence shape

Use the architecture selected in `projects/superkate-services-calculator/docs/customer-sync-architecture.md`:

- SQLite-backed storage for mobile/desktop app targets.
- IndexedDB only for a web-only prototype.
- Avoid `localStorage` for customer appointment history.

The first implementation should expose storage through a small repository/service layer instead of letting Vue components touch the database directly.

Suggested service surface:

```ts
export interface SuperkatePersistenceService {
  listCustomers(): Promise<SuperkateCustomer[]>
  upsertCustomer(input: UpsertSuperkateCustomerInput): Promise<SuperkateCustomer>
  deleteCustomer(customerId: string): Promise<void>
  listAppointments(filter?: SuperkateAppointmentFilter): Promise<SuperkateAppointment[]>
  createAppointment(input: CreateSuperkateAppointmentInput): Promise<SuperkateAppointment>
  deleteAppointment(appointmentId: string): Promise<void>
}
```

Suggested input types:

```ts
export interface UpsertSuperkateCustomerInput {
  id?: string
  name: string
  email?: string | null
}

export interface CreateSuperkateAppointmentInput {
  customerId?: string | null
  clientName: string
  appointmentDate: string
  hourlyRateCents: number
  timeSpentMinutes: number
  productCostCents?: number | null
}

export interface SuperkateAppointmentFilter {
  customerId?: string
  clientNameQuery?: string
  appointmentDate?: string
  appointmentDateFrom?: string
  appointmentDateTo?: string
}
```

## Sync-ready fields

Do not overbuild sync in `t-003`, but store records in a way that does not fight future sync:

- Preserve stable UUID/string IDs generated client-side or through the storage layer.
- Keep `createdAt` and `updatedAt` on both models.
- Keep `syncedAt` on appointments as already approved in `SPEC.md`.
- If the chosen storage adapter supports it cleanly, add non-UI metadata fields such as `deletedAt` or `syncStatus` only behind the service layer. Do not expose sync internals in the calculator form.

## Pinia/store guidance

Components should not call API routes or storage directly. The app should use a Superkate-focused store, then have that store call the persistence service.

Suggested store responsibilities:

- hold customers and appointments in state;
- provide async actions for loading customers/appointments;
- create customer records when a new named client is saved;
- create appointments with calculated totals;
- surface user-safe error messages;
- avoid logging customer details.

Suggested state shape:

```ts
export interface SuperkateState {
  customers: SuperkateCustomer[]
  appointments: SuperkateAppointment[]
  isLoading: boolean
  error: string | null
}
```

## User-safe error handling

Errors shown to Superkate should be useful without leaking customer data:

- `Customer name is required.`
- `Time spent must be greater than zero.`
- `Hourly rate must be zero or more.`
- `Could not save the appointment. Please try again.`

Avoid errors like:

- full raw record payloads;
- customer names/emails in logs;
- stack traces in UI;
- receipt body text in telemetry.

## Implementation checklist for the app repo

1. Add shared model/types for `Customer` and `Appointment`.
2. Add a tested total calculation helper.
3. Add validation helpers for customer and appointment input.
4. Add the local database/storage adapter.
5. Add the repository/service layer.
6. Add Pinia store actions for create/list/delete flows.
7. Wire existing or new calculator UI to the store, not direct API calls.
8. Confirm stored money is cents and stored time is minutes.
9. Confirm appointments preserve `clientNameSnapshot` after customer edits.
10. Confirm product cost defaults to zero.
11. Confirm no client data is logged.

## Verification to run when target repo access exists

At minimum:

```bash
npm run test
npm run typecheck
npm run lint
```

Add unit coverage for:

- cents/minutes total calculation;
- product cost defaulting to zero;
- required customer/client name validation;
- appointment total recalculation from input fields;
- preserving `clientNameSnapshot`;
- list/search service filters if included in this task.

## Safety boundaries

This task should not:

- send receipt emails;
- create backend direct-send credentials;
- add payment handling;
- add analytics/telemetry around customer data;
- create public customer-data endpoints;
- implement destructive bulk delete;
- touch DNS, secrets, billing, or deploy configuration.

## Suggested next state

Because the live implementation was not applied, the roadmap should not mark `t-003` as done. The correct next action is one of:

1. Apply this implementation in the actual Superkate app repository/runtime, then set `t-003` back to `ready` or `claimed` for a patch-capable Worker; or
2. If the Superkate app is meant to live inside another known repo, update the roadmap note with that target repository path so the next Worker can branch there directly.
