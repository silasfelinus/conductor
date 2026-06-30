# Yard Route Calendar Card Spec

This document defines a dummy-data route-card export for Humboldt Scoop CMS. It is a draft specification only: no real customer data, live dispatching, billing, publishing, deployment, SMS, email, or payment workflow is included.

## Purpose

Route cards should give a crew member or owner-operator a compact daily reference for scheduled yard visits. The first version can be exported from dummy CMS data as a manual PDF/template, then later evolve into generated route sheets when scheduling and customer-data handling are approved.

## Card fields

Each card should fit on a printable half-page or mobile-friendly panel.

| Field | Required | Notes |
| --- | --- | --- |
| `visitDate` | yes | Local service date, displayed as a friendly calendar label. |
| `routeSlot` | yes | Suggested order for the day, such as `Morning 01`. |
| `customerName` | yes | Display name only; use dummy data until real data is explicitly approved. |
| `neighborhood` | yes | General service area, not a full address in the first template. |
| `propertyLabel` | yes | Human-readable yard label, such as `Home yard`. |
| `serviceFrequency` | yes | Weekly, twice-weekly, biweekly, monthly, or one-time. |
| `pets` | yes | Pet names, species, temperament, and notes needed for a safe visit. |
| `yardNotes` | yes | Operational notes: side yard, bin location, hazards, cleanup preferences. |
| `gateDetailsPlaceholder` | yes | Placeholder only. Never commit real gate codes or lockbox details. |
| `visitChecklist` | yes | A short checklist for work completion and proof notes. |
| `crewNotes` | optional | Internal notes captured during or after the visit. |
| `billingMode` | optional | Draft-only label for future invoicing context; no payment collection. |

## Suggested checklist

- Confirm correct property/yard label.
- Check pet status before entering.
- Scoop main yard.
- Scoop side yard or marked secondary area.
- Bag and dispose according to service notes.
- Close and latch gates.
- Record bags used.
- Add crew notes if anything needs follow-up.

## Sample cards

### Card 1 — Morning 01

| Field | Value |
| --- | --- |
| Visit date | Tuesday, July 7, 2026 |
| Customer name | Maya Rivera |
| Neighborhood | Cutten / dummy sample area |
| Property label | Home yard |
| Service frequency | Weekly |
| Pets | Poppy — dog, Labrador mix, friendly. Dummy pet for local development only. |
| Yard notes | Check side yard behind garage. Watch for loose garden edging near the back fence. |
| Gate details placeholder | `[GATE DETAILS REDACTED / ENTERED BY APPROVED HUMAN WORKFLOW]` |
| Visit checklist | Confirm yard, greet/secure pet if present, scoop main yard, scoop side yard, bag waste, latch gate, record bags used. |
| Crew notes | If side-yard access is blocked, mark for owner follow-up. |
| Billing mode | Draft monthly invoice line only. |

### Card 2 — Morning 02

| Field | Value |
| --- | --- |
| Visit date | Tuesday, July 7, 2026 |
| Customer name | Theo Chen |
| Neighborhood | Henderson Center / dummy sample area |
| Property label | Back patio run |
| Service frequency | Biweekly |
| Pets | Mochi — dog, corgi, shy. Keep movements slow near patio gate. |
| Yard notes | Small fenced run plus gravel strip along shed. Skip raised garden beds. |
| Gate details placeholder | `[GATE DETAILS REDACTED / ENTERED BY APPROVED HUMAN WORKFLOW]` |
| Visit checklist | Confirm pet is inside, scoop patio run, inspect gravel strip, avoid garden beds, bag waste, latch gate, record bags used. |
| Crew notes | Ask human reviewer whether gravel-strip cleanup needs a separate checklist item. |
| Billing mode | Draft service-plan preview only. |

### Card 3 — Afternoon 01

| Field | Value |
| --- | --- |
| Visit date | Thursday, July 9, 2026 |
| Customer name | Jordan Park |
| Neighborhood | Myrtletown / dummy sample area |
| Property label | Duplex yard B |
| Service frequency | One-time cleanup |
| Pets | Juniper — dog, unknown breed, protective. Appointment-only entry in this dummy card. |
| Yard notes | Large shared yard. Work only the right-side fenced section marked Yard B. Look for waste under the cedar tree. |
| Gate details placeholder | `[APPOINTMENT-ONLY ACCESS / HUMAN-CONFIRMED BEFORE SERVICE]` |
| Visit checklist | Confirm appointment window, confirm Yard B boundary, scoop right-side fenced section, check cedar tree area, bag waste, record bags used, note hazards. |
| Crew notes | Protective pet means this should remain human-reviewed before any automated scheduling. |
| Billing mode | Draft one-time cleanup estimate only. |

## PDF/manual template path

A low-risk first product could be a manually reviewed PDF packet:

1. Select a service date and dummy/sample visits.
2. Render one card per visit with the fields above.
3. Group cards by route slot and neighborhood.
4. Add a cover page with the date, crew name placeholder, and guardrails.
5. Export to PDF for internal review only.

This could later become a paid template/manual product for small service businesses: printable route cards, daily route cover sheet, visit checklist, and customer follow-up notes. That product path should stay human-gated because templates may imply operational, safety, privacy, or customer-data handling decisions.

## Guardrails

- Dummy data only until real customer data handling is approved.
- No real addresses, gate codes, lockbox details, phone numbers, emails, or payment data in committed examples.
- No live dispatch, customer messaging, billing, or publishing from this spec.
- Any future generated PDF/export feature should keep secrets out of source control and require human approval before handling real customer records.
