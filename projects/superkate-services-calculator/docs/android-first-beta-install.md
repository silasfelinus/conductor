# Android-first local beta install notes

This note is for the reversible, local-only Hair by Superkate beta path. It does **not** authorize Play Store submission, TestFlight work, public distribution, live backend sync, production customer data upload, analytics, billing, DNS, secrets, or backend email sending.

## Current beta rule

Use fake or throwaway local test data only until all of these are true:

- durable local persistence is verified on the target Android device;
- export is available and user-initiated;
- customer and appointment delete/edit flows are verified;
- app/device lock is in place for sensitive history, contact details, export, and settings;
- fake-data backend sync is tested without real customer records;
- Silas explicitly approves any step that touches live distribution, hosting, secrets, or real customer data.

The current app target is Android first. Desktop targets stay useful for development and smoke checks, but Android is the first beta install path for Superkate.

## Debug build from a development machine

From the repository root:

```sh
cd apps/superkate-services-calculator
flutter pub get
flutter analyze --fatal-infos
flutter test
flutter build apk --debug
```

The debug APK is expected at:

```txt
apps/superkate-services-calculator/build/app/outputs/flutter-apk/app-debug.apk
```

## Install on a connected Android device

Enable developer mode and USB debugging on the Android device, then connect it by USB.

Check that Flutter can see the device:

```sh
cd apps/superkate-services-calculator
flutter devices
```

Install and run the app directly:

```sh
flutter run -d <device-id>
```

Or install the debug APK after building it:

```sh
adb install -r build/app/outputs/flutter-apk/app-debug.apk
```

Use `flutter devices` to find `<device-id>`. If only one Android device is connected, `flutter run` without `-d` is usually enough.

## Local beta smoke test checklist

Use fake client names and fake email/contact details only.

1. Launch the app on the Android device.
2. Create a fake appointment with:
   - client name;
   - appointment date;
   - hourly rate;
   - time spent;
   - product cost left blank once, then set once;
   - expected total using `hourly rate × time spent + product cost`.
3. Close and reopen the app, then confirm the fake appointment is still present.
4. Search history by fake client name.
5. Search or filter history by appointment date.
6. Prepare a receipt and confirm it opens as a user-reviewed draft or copyable fallback.
7. Confirm the app does not send email by itself.
8. Confirm no real customer records, real customer email addresses, or real appointment data were entered.
9. Confirm no sync endpoint, analytics service, billing flow, or app-store workflow was used.

## Before any wider beta handoff

Before sharing even a debug build beyond Silas/Superkate testing, re-check:

- Android device install works from a clean checkout;
- the README install commands match the actual Flutter version in use;
- customer edit/delete and appointment delete flows are done;
- CSV export is done;
- app/device lock is done;
- fake backend sync remains fake-data only;
- release signing keys are not added to the repo;
- no store listing, store metadata, privacy policy submission, production backend, production database, DNS, billing, or analytics has been touched.

## Explicitly not included

This task does not create or prepare:

- a Play Store listing;
- release signing keys;
- production app bundles;
- TestFlight or iOS distribution;
- backend deployment;
- production sync;
- backend email sending;
- analytics;
- billing;
- public web pages;
- real customer data migration.
