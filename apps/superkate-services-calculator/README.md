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
flutter create . --org org.kindrobots --project-name superkate_services_calculator --platforms ios,android,windows,linux
flutter pub get
flutter test
```

Default Flutter app scaffolding should include `ios`, `android`, `windows`, and `linux` targets unless a project explicitly narrows its install targets.

## Reference material

Project-specific visual/reference material lives in the conductor project folder:

- `projects/superkate-services-calculator/examples/` — Superkate hair-work examples for visual inspiration.
- `projects/superkate-services-calculator/hairpress/` — current Hair by Superkate WordPress front end, for reference only. It may be updated or replaced later.

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
  ui/
    new_appointment_form.dart           New Appointment screen with a live total (t-004)
  main.dart                             app shell + theme; hosts the form
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
`PersistenceService` interface, and the client/date search UI (t-005). The
calculator form (t-004) is done and hosted in `main.dart`. Before layering more
UI on top, the app needs `flutter create` run once to add its platform folders
and a real `flutter test` pass (roadmap **t-014**) — this workspace has no
Flutter toolchain, so t-003/t-004 were verified by inspection only.

Run the unit tests with `flutter test` (covers the total formula, validation,
and the in-memory service including search filters and snapshot preservation).
