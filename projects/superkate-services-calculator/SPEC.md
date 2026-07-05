# Superkate Services Calculator — SPEC

Status: draft for Superkate/Silas review  
Priority: high  
Slug: `superkate-services-calculator`  
Kind: software

## Goal

Build a polished services calculator app for Hair by Superkate that records customer and appointment pricing details, calculates the appointment total, supports customer/date search, syncs customer data safely across devices for the initial beta path, and prepares a warm appointment receipt email.

## Core formula

```txt
appointment total = hourly rate × time spent + product cost
```

## MVP users

- Superkate uses the app during or after an appointment.
- A repeat customer can be selected from a customer database instead of re-entered every time.
- A client receives a clean, warm appointment receipt by email.

## Required appointment fields

- Customer/client name
- Appointment date
- Hourly rate
- Time spent, entered as hours/minutes with preset chips
- Product cost, optional and defaulting to `$0.00`
- Appointment total

## Customer database

A customer database is part of the beta expectation, not a distant someday feature. Hair by Superkate has repeat clientele, so the app should treat customer profiles as a normal local-business workflow.

Customer records should include:

- Customer name
- Optional email address for receipt prefill
- Created/updated timestamps

Customer email storage is approved as a reasonable feature when implemented with the app's security baseline. Email should remain editable per receipt, and storing email should never imply automated backend sending.

## MVP screens

1. **Calculator / New Appointment**
   - Select an existing customer or enter a new customer name.
   - Pick appointment date.
   - Enter hourly rate.
   - Enter time spent with preset chips and manual hours/minutes controls.
   - Enter optional product cost, defaulting to `$0.00`.
   - Show live appointment total.
   - Save appointment.

2. **Customer / Appointment Search**
   - Search by customer name.
   - Filter appointments by date.
   - Show saved appointment rows with customer, date, and appointment total.
   - Open a customer profile to review repeat-client history.

3. **Appointment Detail / Receipt**
   - Display the saved appointment.
   - Show receipt math in this form: `hourly rate × time spent + product cost = total price`.
   - Open an email composer with the customer email prefilled when known.
   - Include warm receipt copy and the slogan: `Superkate loves you!`

4. **Sync / Account Status**
   - Show whether the app is synced, offline, or has pending changes.
   - Surface sync errors clearly without exposing customer data in logs or UI internals.

## Data model

```txt
Customer
- id
- name
- email
- createdAt
- updatedAt

Appointment
- id
- customerId
- clientNameSnapshot
- appointmentDate
- hourlyRateCents
- timeSpentMinutes
- productCostCents
- appointmentTotalCents
- createdAt
- updatedAt
- syncedAt
```

Store money as cents and time as minutes. Calculate totals from stored values rather than trusting manually entered totals. Keep a `clientNameSnapshot` on appointments so historic receipts remain readable even if the customer profile name changes later.

## Beta sync expectation

Cloud sync is part of the initial beta expectation. The app should still be local-first/offline-capable, but the planned beta architecture should include secure account-backed sync for customer and appointment data.

The sync design must cover:

- authenticated access before customer history can sync;
- per-user or per-business ownership checks on every API route;
- HTTPS-only API communication;
- server-side validation of customer and appointment payloads;
- no secrets in client bundles;
- a predictable conflict strategy for edits across devices;
- clear sync status in the UI;
- deletion propagation across synced devices;
- export/backup expectations before paid release.

Cloud sync can later be gated to paid customers, but the beta should be designed as if cloud sync is a real product requirement, not a bolt-on afterthought.

## Customer data security baseline

Client appointment data is sensitive business data and may include customer personal information. The app must treat this as customer data, not casual app state.

### Data minimization

- Store the fields needed for the customer database, calculator, appointment history, receipt preparation, and sync.
- Customer email may be stored when provided so repeat-client receipts can be prefilled.
- Do not add free-form client notes, photos, formulas, analytics identifiers, or marketing tags in the MVP.
- Do not log client names, emails, receipt bodies, appointment totals tied to a client, or raw appointment records to console/server logs.

### Storage and access

- Appointment and customer history should use a real local database/storage layer for app state, not browser `localStorage`, for any paid or customer-data beta release.
- Cloud sync must go through authenticated API routes with authorization checks; never expose a public customer-data endpoint.
- If the app target supports it, add optional app lock or device-auth before showing saved customer history.
- Keep all secrets out of source control and client bundles. The MVP should not require backend email credentials for receipt preparation.

### Receipt safety

- The MVP prepares a user-reviewed email in the device mail app or email composer; it must not silently send receipts from a backend.
- Receipt text should include only appointment facts Superkate entered for that appointment, salon contact details, and warm receipt copy.
- Customer email may prefill the composer when known, but the user should be able to edit it before sending.

### Data lifecycle

- Provide a path to delete an appointment record before paid release.
- Provide a path to delete or update a customer record before paid release.
- Decide export/backup expectations during the sync architecture note.
- Do not add destructive bulk-delete behavior without a confirmation step.

### Paid-app release gates

Before release as a paid app, the project needs a privacy/security review covering:

- where appointment and customer data is stored locally;
- how cloud sync authenticates users and scopes customer data;
- whether optional device/app lock is enabled by default;
- how customer email is stored and edited;
- deletion/export/backup expectations;
- whether any crash reporting or analytics exists, and whether it is configured to avoid customer data;
- privacy copy for the app listing or handoff notes.

## Privacy and safety

Client appointment data is sensitive business data. The app should be local-first/offline-capable, cloud-sync-ready for beta, and private by default. Do not add public pages, customer-data analytics, telemetry that can capture customer data, direct email-sending credentials, payment processing, or shared backend storage without explicit architecture review.

## Email receipt behavior

The MVP should prepare an email in the user's mail app rather than silently sending email from a backend. A later version can support direct sending if Superkate wants that and credentials/secrets are handled safely.

Receipt body should include:

- Hair by Superkate / Superkate salon contact details
- Client name
- Appointment date
- Hourly rate
- Time spent
- Product cost
- Total price
- The formula line: `hourly rate × time spent + product cost = total price`
- Warm signoff including: `Superkate loves you!`

## Visual direction

Dark theme with purple and teal accents. It should feel polished, salon-friendly, calm, and professional — not enterprise beige spreadsheet purgatory.

## Non-goals for MVP

- Payment processing
- Online booking
- Client portal
- Staff accounts
- Public website changes
- GlossGenius import/export
- Automated email sending without user review
- Analytics or telemetry that can capture customer data
- Legal/disclaimer-heavy receipt language

## Decided product choices

- Time spent is entered as hours/minutes with preset chips.
- Product cost is optional and defaults to `$0.00`.
- A customer database with optional stored email is expected for repeat clientele.
- Receipt copy should be warm and include `Superkate loves you!`.
- Cloud sync is part of the initial beta expectation and may later be gated to paying customers.
- App/device lock should be optional where supported.

## Remaining open questions for Superkate

- What exact salon contact details should appear on receipts?
- Should optional app/device lock be enabled by default or simply available in settings?
- What deletion/export/backup behavior is required for the first paid version?
- Should backend direct-send receipts ever be part of the roadmap, or should user-reviewed composer remain the product stance?
