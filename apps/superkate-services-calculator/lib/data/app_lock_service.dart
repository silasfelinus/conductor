library;

/// Optional PIN lock protecting the saved client book (customer history,
/// contact details, and sensitive settings). Local-first: the PIN never
/// leaves the device and is stored only as a salted hash.
abstract class AppLockService {
  Future<bool> isEnabled();

  /// Turns the lock on with [pin]. Throws [ArgumentError] if the PIN is
  /// not 4-8 digits.
  Future<void> enable(String pin);

  /// Turns the lock off. Callers are responsible for verifying the current
  /// PIN first (see [verifyPin]).
  Future<void> disable();

  /// Whether [pin] matches the stored PIN. Always false while disabled.
  Future<bool> verifyPin(String pin);
}

/// PINs are short numeric codes: 4-8 digits.
final RegExp _pinPattern = RegExp(r'^\d{4,8}$');

bool isValidAppLockPin(String pin) => _pinPattern.hasMatch(pin);

void ensureValidAppLockPin(String pin) {
  if (!isValidAppLockPin(pin)) {
    throw ArgumentError.value(pin, 'pin', 'PIN must be 4-8 digits');
  }
}
