/// Input validation for customers and appointments.
///
/// Errors are user-safe (SPEC.md "Customer data security baseline"): they never
/// echo raw payloads, customer names, emails, or receipt bodies. Throw
/// [ValidationException] with a short message suitable for direct UI display.
library;

class ValidationException implements Exception {
  const ValidationException(this.message);

  /// User-safe, display-ready message (e.g. "Customer name is required.").
  final String message;

  @override
  String toString() => 'ValidationException: $message';
}

/// Trims a name and asserts it is non-empty. Returns the trimmed value.
String validateClientName(String? raw) {
  final name = (raw ?? '').trim();
  if (name.isEmpty) {
    throw const ValidationException('Customer name is required.');
  }
  return name;
}

/// Normalizes an optional email: blank -> `null`; otherwise a gentle format
/// check (beta: reject only obviously malformed values when supplied).
String? validateOptionalEmail(String? raw) {
  final email = (raw ?? '').trim();
  if (email.isEmpty) return null;
  final looksValid = RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(email);
  if (!looksValid) {
    throw const ValidationException('That email address looks incomplete.');
  }
  return email;
}

/// Asserts a non-negative integer cents amount.
int validateNonNegativeCents(int cents, {required String label}) {
  if (cents < 0) {
    throw ValidationException('$label must be zero or more.');
  }
  return cents;
}

/// Asserts hourly rate is a valid (non-negative) cents amount.
int validateHourlyRateCents(int cents) =>
    validateNonNegativeCents(cents, label: 'Hourly rate');

/// Asserts product cost is a valid (non-negative) cents amount; `null` -> 0.
int validateProductCostCents(int? cents) =>
    validateNonNegativeCents(cents ?? 0, label: 'Product cost');

/// Asserts time spent is a positive integer minute count.
int validateTimeSpentMinutes(int minutes) {
  if (minutes <= 0) {
    throw const ValidationException('Time spent must be greater than zero.');
  }
  return minutes;
}
