# Mission remittance runbook and reconciliation

**Task:** `kind-economy/t-016`. Runbook and tooling only — this document does not
authorize or automate a transfer. Sending money is Silas's action, taken outside this
app, on his own schedule.

## What this covers

`t-010` (kind_robots PR #1964) built the bookkeeping: an admin-only dashboard at
`/mission-accrual` (`server/api/economy/mission-accrual.{get,post}.ts`,
`server/utils/missionAccrual.ts`, `stores/missionAccrualStore.ts`,
`components/pages/mission-accrual-page.vue`) that shows

- **Accrued** — the running platform-wide sum of `RevenueSplit.missionShareCents`
  (reversal-corrected — a corrected spend never inflates this).
- **Remitted** — the sum of every `MissionRemittance` row, a manual, append-only log
  of real money Silas has already sent to the fundraiser *outside* this app.
- **Outstanding** — `accrued − remitted`. This is the number that matters here.

`t-005` (`research/remittance-options.md`) settled the *route*: **Option A**, a
redirect to Every.org's hosted AMF donate page (`every.org/againstmalaria`), with
**Option C**, the existing `againstmalaria.com/amibot` direct-giving link, staying
live unconditionally as the zero-registration fallback. Neither is wired into
checkout yet (that's the still-open registration question in `t-005`'s note, for the
CPA/attorney conversation) — today, every remittance is Silas manually sending money
through one of those two channels and then logging it here.

This runbook is the procedure that connects "outstanding says $X" to "$X actually
left the door and the ledger says so."

## Cadence

**Recommended: quarterly**, alongside Silas's own calendar-quarter bookkeeping
(Jan 1 / Apr 1 / Jul 1 / Oct 1) — it's a natural review point and lines up with the
non-profit-restart timeline he's already targeting for January. This is a
recommendation, not an enforced gate: nothing in the code requires quarterly cadence,
and Silas can remit whenever he chooses.

Two situations call for remitting sooner than the next quarterly checkpoint, regardless
of schedule:
- **Outstanding has been sitting non-trivially positive for a while.** As a rule of
  thumb, don't let more than about $50 or one full quarter (whichever comes first) go
  by unremitted — the longer the gap, the more it looks like the "a third of what you
  pay buys nets" promise isn't being kept in practice, even though it's technically
  tracked.
- **Silas wants to close the books for some other reason** (tax filing, an audit of the
  economy system, a public accounting of where the mission share has gone).

There's no requirement to remit tiny amounts immediately — batching small accruals into
one clean quarterly transfer keeps the number of donation receipts (and reconciliation
steps) manageable.

## Who initiates

**Silas, manually, every time.** No agent creates a Stripe/Every.org/bank transaction,
touches payment credentials, or automates a transfer — this is unconditional per the
project's standing rules (`roadmap.yaml`'s `notes_from_silas`) and is not something this
task or runbook changes. An agent's role is limited to: surfacing the outstanding
balance, describing the steps, and logging the remittance record *after* Silas confirms
the money has actually moved.

## Procedure

1. **Check outstanding.** Open `/mission-accrual` (admin-only) or
   `GET /api/economy/mission-accrual`. Read `data.outstandingCents`. If it's `0`,
   there's nothing to remit — stop here.
2. **Send exactly that amount** to the Against Malaria Foundation, through whichever
   channel is live at the time:
   - Preferred once wired up: Every.org's hosted AMF page
     (`every.org/againstmalaria`) — per `t-005`'s Option A recommendation.
   - Fallback, always available: `againstmalaria.com/amibot` — Option C, the same
     link already used for the ~$840 raised directly to date.

   Round to the nearest cent; don't round the transfer up or down for convenience —
   the reconciliation check in step 4 is exact, not fuzzy.
3. **Keep the receipt.** Every.org and AMF both send an email confirmation /
   donation-ID for each gift. Save that confirmation wherever Silas keeps financial
   records (e.g. a dedicated folder outside this git repo — receipts and donor
   confirmation emails are not committed to the repo). The donation ID or confirmation
   number is what goes in the `reference` field in the next step, so the ledger entry
   can always be traced back to the actual receipt.
4. **Log the remittance.** On `/mission-accrual`, use the "Log a remittance" form
   (or `POST /api/economy/mission-accrual` directly with
   `{ amountCents, note, reference }`):
   - `amountCents` — the exact amount sent in step 2, in cents.
   - `note` — what it was for, e.g. `"Q1 2027 mission-share remittance via Every.org"`.
   - `reference` — the Every.org/AMF donation ID or confirmation number from step 3.
     This is the field that lets a future audit walk from the ledger row back to the
     real-world receipt.

   This never edits or deletes an existing `MissionRemittance` row — correcting a
   mistake means logging a new, clearly-noted row, not touching the old one
   (`t-010`'s append-only design; same discipline as `RevenueSplit`).
5. **Confirm reconciliation.** The dashboard reloads after a successful submit and
   shows a reconciliation banner (`kind-economy/t-016`,
   `checkMissionRemittanceReconciliation` in `server/utils/missionAccrual.ts`). It
   should read **"✅ Reconciled — outstanding is $0.00."** If it doesn't, see below —
   don't walk away from a non-reconciled state without understanding why.

## Reconciliation check — the two failure modes that matter

Because every remittance is meant to bring the running outstanding balance back to
exactly zero (there's no per-period bucketing on `MissionRemittance` — see "Why no
per-period tracking" below), both failure modes the task asks for collapse onto the
sign of `outstandingCents` immediately after logging a remittance:

| `outstandingCents` after logging | Status | Meaning |
|---|---|---|
| `== 0` | ✅ **Reconciled** | The remittance covered exactly what had accrued. Nothing owed. |
| `> 0` | ⚠️ **Under-remitted** | *Remitting less than accrued — the promise is broken.* Less went out than had accrued. The fundraiser is still owed the shortfall shown. |
| `< 0` | ⚠️ **Over-remitted** | *Double-remitting the same period — the money is gone twice.* More was logged as remitted than had accrued. Most likely cause: the same real-world donation was logged twice, or the amount was mistyped too high. |

This is computed by `checkMissionRemittanceReconciliation()` in
`server/utils/missionAccrual.ts`, returned as `data.reconciliation` from
`GET /api/economy/mission-accrual`, and rendered as a banner on `/mission-accrual`.
Covered by `utils/scripts/verifyMissionAccrual.test.ts` (`npm run
test:mission-accrual`).

**If under-remitted:** send the shortfall shown and log a second remittance row for
it (don't edit the first row). Confirm the banner returns to reconciled afterward.

**If over-remitted:** before assuming anything is wrong with the ledger, check the
remittance log for a duplicate entry (same amount, note, or `reference` appearing
twice close together in time) — that's the far more likely cause than a real
double-payment to AMF. If it is a duplicate log entry, don't delete it (append-only);
instead log a correcting note (e.g. a `note` explaining the duplicate) so a human
reading the log later understands the ledger is honest about what was *recorded*,
even though the true dollar amount sent was less. If the real-world payment actually
was sent twice, that's a genuine problem outside this app (contact AMF/Every.org
about a refund or credit toward the next period) — not something this tooling can fix.

## Why no per-period tracking

`MissionRemittance` rows don't carry a "for period X" field. The alternative design —
bucketing remittances by calendar quarter and checking each bucket's remitted total
against that bucket's accrued total — was considered and rejected for this task: it
adds a schema field and matching logic for no real benefit, because the running
`outstanding = accrued − remitted` total already answers the only question that
matters ("is the ledger currently honest?") without needing to know which period a
given remittance was "for." A remittance that's late, early, or a batch covering more
than one quarter's accrual all reconcile identically as long as the running total
returns to zero. If Silas later wants period-by-period reporting (e.g. for a annual
filing), that's a reporting view on top of the existing `createdAt` timestamps, not a
correctness requirement for this reconciliation check.

## What this explicitly does not do

- Does not create a Stripe, Every.org, bank, or payment-processor transaction.
- Does not touch DNS, secrets, or billing.
- Does not decide the entity question (`t-002`/`t-003`, still open).
- Does not resolve the registration question flagged in `t-005` (redirect-vs-embedded
  donate flow, commercial-co-venture/charitable-solicitation state law) — that's still
  a CPA/attorney conversation before anything is wired into checkout.
