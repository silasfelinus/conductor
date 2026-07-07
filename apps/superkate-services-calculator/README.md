# Superkate Services Calculator

A private appointment services calculator for Hair by Superkate.

Core formula:

```txt
hourly rate × time spent + product cost = appointment total
```

See `projects/superkate-services-calculator/SPEC.md` for the product brief and `projects/superkate-services-calculator/roadmap.yaml` for the agent plan.

First checkout on a dev machine:

```sh
cd apps/superkate-services-calculator
flutter create . --org org.kindrobots --project-name superkate_services_calculator --platforms ios,android
flutter pub get
flutter test
```

## Architecture (domain + persistence layer — roadmap t-003)

The app is organized so Flutter widgets talk to a store/service, never to a
database or API directly (SPEC.md "Storage and access"):

```
lib/
  domain/
    money.dart        cents/minutes math + the appointment-total formula + display formatting
    validation.dart   user-safe input validation (never echoes customer data)
    ids.dart          dependency-free local id generation (sync-ready)
  models/
    customer.dart     immutable Customer value object (+ toMap/fromMap)
    appointment.dart  immutable Appointment value object (+ toMap/fromMap)
  data/
    persistence_service.dart            the PersistenceService interface + input/filter types
    in_memory_persistence_service.dart  local-first implementation (source of truth today)
```

Invariants enforced here:

- **Money is cents, time is minutes** at every boundary; dollars only for display.
- The **appointment total is always recalculated** from stored fields, never
  trusted from UI input.
- **Product cost defaults to `0`**.
- `clientNameSnapshot` is preserved so historic receipts survive customer renames.
- Deleting a customer **detaches** their appointments (sets `customerId` to null)
  rather than deleting them — no destructive cascade.
- Records carry `createdAt` / `updatedAt` (+ `syncedAt` on appointments) so the
  local store does not fight the future beta sync design.

Next steps (follow-on tasks): a durable **SQLite adapter** behind the same
`PersistenceService` interface, then the calculator form (t-004) and
client/date search UI (t-005) wired to a store, not to storage directly.

Run the unit tests with `flutter test` (covers the total formula, validation,
and the in-memory service including search filters and snapshot preservation).
