library;

import 'app_lock_service.dart';

class InMemoryAppLockService implements AppLockService {
  InMemoryAppLockService({String? pin}) : _pin = pin {
    if (pin != null) ensureValidAppLockPin(pin);
  }

  String? _pin;

  @override
  Future<bool> isEnabled() async => _pin != null;

  @override
  Future<void> enable(String pin) async {
    ensureValidAppLockPin(pin);
    _pin = pin;
  }

  @override
  Future<void> disable() async {
    _pin = null;
  }

  @override
  Future<bool> verifyPin(String pin) async => _pin != null && _pin == pin;
}
