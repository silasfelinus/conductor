import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/app_lock_service.dart';
import 'package:superkate_services_calculator/data/file_app_lock_service.dart';
import 'package:superkate_services_calculator/data/in_memory_app_lock_service.dart';

void main() {
  group('PIN validation', () {
    test('accepts 4-8 digit PINs', () {
      expect(isValidAppLockPin('1234'), isTrue);
      expect(isValidAppLockPin('12345678'), isTrue);
    });

    test('rejects short, long, and non-numeric PINs', () {
      expect(isValidAppLockPin('123'), isFalse);
      expect(isValidAppLockPin('123456789'), isFalse);
      expect(isValidAppLockPin('12a4'), isFalse);
      expect(isValidAppLockPin(''), isFalse);
      expect(isValidAppLockPin('12 34'), isFalse);
    });
  });

  group('InMemoryAppLockService', () {
    test('starts disabled and enables with a valid PIN', () async {
      final lock = InMemoryAppLockService();
      expect(await lock.isEnabled(), isFalse);
      expect(await lock.verifyPin('1234'), isFalse);

      await lock.enable('1234');
      expect(await lock.isEnabled(), isTrue);
      expect(await lock.verifyPin('1234'), isTrue);
      expect(await lock.verifyPin('9999'), isFalse);
    });

    test('rejects an invalid PIN on enable', () async {
      final lock = InMemoryAppLockService();
      expect(() => lock.enable('12'), throwsArgumentError);
      expect(await lock.isEnabled(), isFalse);
    });

    test('disable clears the PIN', () async {
      final lock = InMemoryAppLockService(pin: '1234');
      await lock.disable();
      expect(await lock.isEnabled(), isFalse);
      expect(await lock.verifyPin('1234'), isFalse);
    });
  });

  group('FileAppLockService', () {
    late Directory tempDir;

    setUp(() async {
      tempDir = await Directory.systemTemp.createTemp('superkate_lock_test');
    });

    tearDown(() async {
      await tempDir.delete(recursive: true);
    });

    File lockFile() => File('${tempDir.path}/app_lock.json');

    test('missing file means disabled', () async {
      final lock = FileAppLockService.forFile(lockFile());
      expect(await lock.isEnabled(), isFalse);
      expect(await lock.verifyPin('1234'), isFalse);
    });

    test('enable persists a salted hash, not the PIN', () async {
      final lock = FileAppLockService.forFile(lockFile());
      await lock.enable('4321');

      final raw = await lockFile().readAsString();
      expect(raw, isNot(contains('4321')));
      expect(raw, contains('salt'));
      expect(raw, contains('hash'));

      // A fresh instance over the same file verifies the PIN.
      final reopened = FileAppLockService.forFile(lockFile());
      expect(await reopened.isEnabled(), isTrue);
      expect(await reopened.verifyPin('4321'), isTrue);
      expect(await reopened.verifyPin('1234'), isFalse);
    });

    test('re-enabling with a new PIN replaces the old one', () async {
      final lock = FileAppLockService.forFile(lockFile());
      await lock.enable('1234');
      await lock.enable('5678');
      expect(await lock.verifyPin('1234'), isFalse);
      expect(await lock.verifyPin('5678'), isTrue);
    });

    test('disable removes the file', () async {
      final lock = FileAppLockService.forFile(lockFile());
      await lock.enable('1234');
      await lock.disable();
      expect(await lockFile().exists(), isFalse);
      expect(await lock.isEnabled(), isFalse);
    });

    test('a corrupt file fails closed to disabled without throwing', () async {
      await lockFile().writeAsString('not json at all');
      final lock = FileAppLockService.forFile(lockFile());
      expect(await lock.isEnabled(), isFalse);
      expect(await lock.verifyPin('1234'), isFalse);
    });

    test('rejects an invalid PIN on enable', () async {
      final lock = FileAppLockService.forFile(lockFile());
      expect(() => lock.enable('abc'), throwsArgumentError);
      expect(await lock.isEnabled(), isFalse);
    });
  });
}
