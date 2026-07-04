# Superkate Services Calculator — SPEC

Status: draft for Superkate/Silas review  
Priority: high  
Slug: `superkate-services-calculator`  
Kind: software

## Goal

Build a private services calculator app for Hair by Superkate that records appointment pricing details, calculates the appointment total, supports client/date search, and prepares an appointment receipt email.

## Core formula

```txt
appointment total = hourly rate × time spent + product cost
```

## MVP users

- Superkate uses the app during or after an appointment.
- A client receives a clean appointment receipt by email.

## Required appointment fields

- Client name
- Appointment date
- Hourly rate
- Time spent
- Product cost
- Appointment total

## MVP screens

1. **Calculator / New Appointment**
   - Enter client name.
   - Pick appointment date.
   - Enter hourly rate.
   - Enter time spent.
   - Enter product cost.
   - Show live appointment total.
   - Save appointment.

2. **Appointment Search**
   - Search by client name.
   - Filter by appointment date.
   - Show saved appointment rows with total price.

3. **Appointment Detail / Receipt**
   - Display the saved appointment.
   - Show receipt math in this form: `hourly rate × time spent + product cost = total price`.
   - Open an email composer with the client name and receipt details prefilled.

## Data model

```txt
Appointment
- id
- clientName
- appointmentDate
- hourlyRateCents
- timeSpentMinutes
- productCostCents
- appointmentTotalCents
- createdAt
- updatedAt
```

Store money as cents and time as minutes. Calculate totals from stored values rather than trusting manually entered totals.

## Customer data security baseline

Client appointment data is sensitive business data and may include customer personal information. The MVP must stay local-first/private by default, and the paid-app path must treat this as customer data, not casual app state.

### Data minimization

- Store only the fields needed for the calculator, appointment history, and receipt preparation.
- Do not store client email by default unless Superkate explicitly approves it in the MVP spec review.
- Do not add free-form client notes, photos, formulas, analytics identifiers, or marketing tags in the MVP.
- Do not log client names, receipt bodies, appointment totals tied to a client, or raw appointment records to console/server logs.

### Storage and access

- Appointment history should use local persistence for MVP; no cloud sync, public pages, analytics, telemetry, or multi-device backend until explicitly approved.
- Do not store customer appointment data in browser `localStorage` for a paid release unless Superkate explicitly accepts the risk; prefer a local database/storage layer protected by the operating system.
- If the app target supports it, add an app lock or device-auth gate before showing saved client history.
- Keep all secrets out of source control and client bundles. The MVP should not require backend email credentials.

### Receipt safety

- The MVP prepares a user-reviewed email in the device mail app or email composer; it must not silently send receipts from a backend.
- Receipt text should include only appointment facts Superkate entered for that appointment.
- If client email storage is later approved, make it optional and editable per receipt.

### Data lifecycle

- Provide a path to delete an appointment record before paid release.
- Plan for export/backup only after Superkate chooses whether the MVP is one-device-only or sync-enabled.
- Do not add destructive bulk-delete behavior without a confirmation step.

### Paid-app release gates

Before release as a paid app, the project needs a privacy/security review covering:

- where appointment data is stored;
- whether device/app lock is required;
- whether client email is stored or receipt-only;
- deletion/export/backup expectations;
- whether any crash reporting or analytics exists, and whether it is configured to avoid customer data;
- privacy copy for the app listing or handoff notes.

## Privacy and safety

Client appointment data is sensitive business data. The MVP should be local-first/private by default. Do not add cloud sync, public pages, analytics, telemetry, direct email-sending credentials, payment processing, or shared backend storage without explicit human approval.

## Email receipt behavior

The MVP should prepare an email in the user's mail app rather than silently sending email from a backend. A later version can support direct sending if Superkate wants that and credentials/secrets are handled safely.

Receipt body should include:

- Client name
- Appointment date
- Hourly rate
- Time spent
- Product cost
- Total price
- The formula line: `hourly rate × time spent + product cost = total price`

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
- Cloud sync without explicit approval
- Analytics or telemetry that can capture customer data
- Storing client email before Superkate approves it

## Open questions for Superkate

- Should time spent be entered as hours with decimals, hours/minutes, or preset chips?
- Should product cost be optional per appointment?
- Does the receipt need the client's email address stored, or should email be entered only when sending?
- Should receipts include salon name/contact info and any legal/disclaimer text?
- Should appointment history stay on one device only for MVP, or sync later?
- Should the paid app require an app lock or device authentication before showing saved client history?
- Should deletion/export/backup be part of the first paid version or a post-MVP release?
