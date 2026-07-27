# Humboldt Scoop field client

Android-first Flutter client for crew route work. The same Dart code remains compatible with Linux and iOS because API access, navigation handoff, and route persistence are injected behind small interfaces.

## Included slice

- Today's ordered route and next-stop summary
- Route cards with pet and yard notes
- Visit completion with crew notes
- Safe handoff to an installed navigation app
- Dummy-data mode for development
- HTTP API adapter for `/routes/today` and `/visits/:id/complete`
- No background location collection or real customer data

## Run

```bash
flutter pub get
flutter test
flutter run
```

`main.dart` uses `DummyRouteApi` by default. A deployed build should inject `HttpRouteApi(Uri.parse(...))` from environment-specific bootstrap code rather than hard-coding a production URL.

## Platform boundaries

The client requests no background-location permission. Navigation is an explicit button press that opens the platform's installed handler. Route storage currently defaults to memory; a durable implementation can replace `RouteStorage` without changing widgets or API behavior.
