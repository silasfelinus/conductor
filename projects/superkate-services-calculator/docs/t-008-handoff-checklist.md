# Superkate Services Calculator — Handoff Checklist

Date: 2026-07-08  
Task: `superkate-services-calculator/t-008`  
Status: human-gated handoff draft; no store submission

## Purpose

This checklist prepares the Superkate app for local device install/testing, privacy review, and next-step planning without submitting anything to an app store, publishing anything, spending money, or touching live customer data.

The app is now useful enough to test the core appointment workflow from `main`, but it is not ready for real client records yet because durable local storage, cloud sync, CSV export, and app/device lock are not implemented.

## Current build state

Implemented in `apps/superkate-services-calculator/`:

- Flutter app scaffold with Android and iOS platform folders.
- Dark purple/teal salon UI.
- New appointment form with client name, appointment date, hourly rate, time spent, optional product cost, and live total.
- Core formula: `hourly rate × time spent + product cost = appointment total`.
- Money stored/calculated as cents and time as minutes in the domain layer.
- Appointment history tab with client-name search and date filters.
- Receipt preparation from appointment history using a local, user-reviewed email composer handoff plus a copyable fallback dialog.
- Receipt copy includes appointment facts, the formula line, and `Superkate loves you!`.
- Superkate Flutter CI workflow runs `flutter pub get`, `flutter analyze --fatal-infos`, and `flutter test` when Superkate app files or the workflow change.

Current limitations to treat as blockers before real beta/customer use:

- Appointment/customer data is backed by `InMemoryPersistenceService` today, so saved records are for testing only and should be expected to disappear when the app restarts.
- No SQLite/durable local adapter yet.
- No cloud sync, account login, sync status UI, or deletion propagation yet.
- No app/device lock onboarding or settings toggle yet.
- No customer profile UI, customer edit/delete UI, appointment delete UI, or CSV export UI yet.
- No app-store package, listing, billing, analytics, or production deploy has been prepared.

## Local checkout and automated verification

From the Windows dev machine:

```powershell
cd D:\code\Conductor
git checkout main
git pull
cd apps\superkate-services-calculator
D:\dev\flutter\bin\flutter.bat pub get
D:\dev\flutter\bin\flutter.bat analyze --fatal-infos
D:\dev\flutter\bin\flutter.bat test
```

Expected result:

- `flutter pub get` completes without dependency errors.
- `flutter analyze --fatal-infos` reports no issues.
- `flutter test` passes.

CI expectation:

- Superkate Flutter CI should also pass on PRs/pushes that touch `apps/superkate-services-calculator/**` or `.github/workflows/superkate-flutter-ci.yml`.

## Device install smoke test

Use a local debug install only.

```powershell
cd D:\code\Conductor\apps\superkate-services-calculator
D:\dev\flutter\bin\flutter.bat devices
D:\dev\flutter\bin\flutter.bat run -d <deviceId>
```

Do not submit to Google Play, the Apple App Store, TestFlight, or any public distribution channel from this checklist.

## Manual workflow test script

Use fake client data only.

### Launch and layout

- Open the app.
- Confirm the title reads `Superkate Services Calculator`.
- Confirm the app has `New` and `History` tabs.
- Confirm the visual style is dark with purple/teal accents and readable touch targets.

### Calculator formula

- In the `New` tab, enter a fake client name.
- Pick today or another appointment date.
- Enter an hourly rate.
- Select or enter time spent.
- Enter optional product cost.
- Confirm the appointment total updates live.

Known-good example:

```txt
Hourly rate: $120.00
Time spent: 1h 30m
Product cost: $25.00
Expected total: $205.00
```

### Validation behavior

- Try saving with a missing client name.
- Try invalid money input.
- Confirm errors are user-safe and do not expose raw customer data or internal details.

### Save and history

- Save a fake appointment.
- Confirm the snackbar shows the fake client name and calculated total.
- Open `History`.
- Confirm the saved appointment appears newest-first.
- Search by part of the fake client name.
- Confirm matching appointments remain and non-matching appointments disappear.
- Use date filters and confirm results stay within the selected range.
- Clear filters and confirm the full test list returns.

### Receipt composer

- In `History`, tap `Prepare receipt` on a fake appointment.
- Confirm the app opens the device mail composer when available.
- Confirm the fallback dialog appears if no composer is available.
- Confirm the draft/fallback includes:
  - fake client name;
  - appointment date;
  - hourly rate;
  - time spent;
  - product cost;
  - total price;
  - formula line;
  - `Superkate loves you!`.
- Confirm the user can review/edit before sending.
- Confirm the app does not silently send email from a backend.

### Persistence reality check

- Save one fake appointment.
- Fully close and relaunch the app.
- Expect the saved fake appointment to be gone until a durable persistence adapter lands.
- Treat this as a known blocker before real beta usage, not as a surprise regression.

## Customer data and backup expectations

For this build:

- Use fake test data only.
- Do not enter real client names, emails, appointment prices, or receipt content that must be retained.
- There is no real backup path yet.
- There is no cloud sync recovery path yet.
- There is no CSV export yet.

Before Superkate uses the app for real customer records, add and verify:

- Durable local storage behind the existing `PersistenceService` interface.
- Cloud sync with authenticated ownership checks.
- Clear synced/offline/pending/error states.
- Deletion propagation across devices.
- CSV export for customers and appointments.
- App/device lock for saved customer history.

## Privacy and security review checklist

Before any real beta, confirm:

- No analytics or telemetry is added.
- No customer names, emails, appointment totals tied to a customer, or receipt bodies are logged.
- Receipt preparation remains local and user-reviewed.
- Backend direct-send email remains out of scope.
- Cloud sync API routes require authentication and owner/business scoping before any customer data leaves the device.
- Secrets are not committed or bundled into the client.
- App/device lock protects saved customer history, export, and settings that reveal customer email.
- Privacy copy explains local storage, cloud backup/sync behavior, export, deletion, and receipt composer behavior in plain language.

## Configuration values Silas/Superkate still need to provide

- Final booking/contact link for receipt copy.
- Final preferred reply contact for receipt copy.
- Final app-lock onboarding language.
- Whether the first beta target is Android debug install, iOS local install/TestFlight later, web, or both mobile platforms.
- Which account/auth system should own cloud sync.

## App-store readiness gate

Do not submit or prepare a live listing until these are done and explicitly approved:

- Durable local persistence.
- Real customer-data privacy/security review.
- App/device lock behavior.
- Cloud sync/auth decision.
- Export/deletion behavior.
- App icon, screenshots, store copy, pricing, and privacy labels.
- Human approval for the exact store submission path.

## Handoff decision

This checklist is ready for Silas/Superkate review as a testing and release-gate document. It should end at `needs-human`, not `done`, because the task is human-gated and touches handoff/store-readiness decisions.
