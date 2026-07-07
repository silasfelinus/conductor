import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/domain/validation.dart';

void main() {
  group('validateClientName', () {
    test('trims and returns a valid name', () {
      expect(validateClientName('  Kate  '), 'Kate');
    });

    test('rejects blank / null', () {
      expect(() => validateClientName(''), throwsA(isA<ValidationException>()));
      expect(() => validateClientName('   '),
          throwsA(isA<ValidationException>()));
      expect(
          () => validateClientName(null), throwsA(isA<ValidationException>()));
    });

    test('error message is user-safe', () {
      try {
        validateClientName('');
        fail('expected throw');
      } on ValidationException catch (e) {
        expect(e.message, 'Customer name is required.');
      }
    });
  });

  group('validateOptionalEmail', () {
    test('blank becomes null', () {
      expect(validateOptionalEmail(''), isNull);
      expect(validateOptionalEmail('   '), isNull);
      expect(validateOptionalEmail(null), isNull);
    });

    test('accepts a reasonable address', () {
      expect(validateOptionalEmail(' kate@example.com '), 'kate@example.com');
    });

    test('rejects obviously malformed values', () {
      expect(() => validateOptionalEmail('kate@'),
          throwsA(isA<ValidationException>()));
      expect(() => validateOptionalEmail('nope'),
          throwsA(isA<ValidationException>()));
    });
  });

  group('cents validation', () {
    test('hourly rate must be non-negative', () {
      expect(validateHourlyRateCents(0), 0);
      expect(validateHourlyRateCents(8000), 8000);
      expect(() => validateHourlyRateCents(-1),
          throwsA(isA<ValidationException>()));
    });

    test('product cost defaults to zero and must be non-negative', () {
      expect(validateProductCostCents(null), 0);
      expect(validateProductCostCents(2500), 2500);
      expect(() => validateProductCostCents(-1),
          throwsA(isA<ValidationException>()));
    });
  });

  group('validateTimeSpentMinutes', () {
    test('must be strictly positive', () {
      expect(validateTimeSpentMinutes(1), 1);
      expect(validateTimeSpentMinutes(90), 90);
      expect(() => validateTimeSpentMinutes(0),
          throwsA(isA<ValidationException>()));
      expect(() => validateTimeSpentMinutes(-5),
          throwsA(isA<ValidationException>()));
    });
  });
}
