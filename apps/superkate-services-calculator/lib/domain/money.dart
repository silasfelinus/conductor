/// Money and time math for the Superkate Services Calculator.
///
/// Money is always stored and passed as integer **cents**; time is always
/// stored and passed as integer **minutes**. Totals are calculated from these
/// stored values and never trusted from UI input (SPEC.md "Data model").
///
/// Core formula (SPEC.md):
///   appointment total = hourly rate × time spent + product cost
/// expressed in cents:
///   totalCents = round(hourlyRateCents × timeSpentMinutes / 60) + productCostCents
library;

/// Calculates the appointment total in cents from stored values.
///
/// - [hourlyRateCents] must be a non-negative integer.
/// - [timeSpentMinutes] must be a positive integer.
/// - [productCostCents] is optional and defaults to `0`.
///
/// Rounding happens once, on the rate×time term, using banker's-free
/// round-half-away-from-zero so a 30-minute half-hour bills cleanly.
int calculateAppointmentTotalCents({
  required int hourlyRateCents,
  required int timeSpentMinutes,
  int? productCostCents,
}) {
  final product = productCostCents ?? 0;
  final labour = (hourlyRateCents * timeSpentMinutes) / 60;
  return labour.round() + product;
}

/// Formats an integer cents value as a US-dollar display string, e.g.
/// `17500 -> "$175.00"`. Display only — never store the formatted value.
String formatCents(int cents) {
  final negative = cents < 0;
  final abs = cents.abs();
  final dollars = abs ~/ 100;
  final remainder = (abs % 100).toString().padLeft(2, '0');
  return '${negative ? '-' : ''}\$$dollars.$remainder';
}

/// Converts whole hours and minutes into a total minute count.
/// Used by the calculator's hours/minutes chips (SPEC.md).
int toMinutes({int hours = 0, int minutes = 0}) => hours * 60 + minutes;

/// Parses a user-typed dollar string (e.g. "80", "80.5", "$1,234.50") into
/// integer cents. Blank/`null` returns `0` (product cost defaults to zero).
///
/// Returns `null` when the text is present but not a valid money amount, so the
/// caller can show a user-safe validation message rather than guessing a value.
int? parseDollarsToCents(String? raw) {
  final text = (raw ?? '').trim().replaceAll(RegExp(r'[\$,\s]'), '');
  if (text.isEmpty) return 0;
  final dollars = double.tryParse(text);
  if (dollars == null || dollars.isNaN || dollars.isInfinite) return null;
  return (dollars * 100).round();
}
