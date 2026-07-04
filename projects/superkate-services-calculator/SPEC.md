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

## Privacy and safety

Client appointment data is sensitive business data. The MVP should be local-first/private by default. Do not add cloud sync, public pages, analytics, or direct email-sending credentials without explicit human approval.

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

## Open questions for Superkate

- Should time spent be entered as hours with decimals, hours/minutes, or preset chips?
- Should product cost be optional per appointment?
- Does the receipt need the client's email address stored, or should email be entered only when sending?
- Should receipts include salon name/contact info and any legal/disclaimer text?
- Should appointment history stay on one device only for MVP, or sync later?
