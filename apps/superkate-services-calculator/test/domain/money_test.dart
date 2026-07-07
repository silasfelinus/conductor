import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/domain/money.dart';

void main() {
  group('calculateAppointmentTotalCents', () {
    test(r'rate x time + product (SPEC example: $100 x 90m + $25 = $175)', () {
      expect(
        calculateAppointmentTotalCents(
          hourlyRateCents: 10000,
          timeSpentMinutes: 90,
          productCostCents: 2500,
        ),
        17500,
      );
    });

    test(r'product cost defaults to zero when omitted (SPEC: $80 x 45m)', () {
      expect(
        calculateAppointmentTotalCents(
          hourlyRateCents: 8000,
          timeSpentMinutes: 45,
        ),
        6000,
      );
    });

    test('product cost defaults to zero when null', () {
      expect(
        calculateAppointmentTotalCents(
          hourlyRateCents: 8000,
          timeSpentMinutes: 45,
          productCostCents: null,
        ),
        6000,
      );
    });

    test(r'rounds the labour term once (half a minute at $60/hr)', () {
      // 6000 * 1 / 60 = 100 exactly; 6000 * 25 / 60 = 2500 exactly.
      expect(
        calculateAppointmentTotalCents(
            hourlyRateCents: 6000, timeSpentMinutes: 1),
        100,
      );
      // A rate that does not divide evenly: 3333c/hr * 10m = 555.5 -> 556.
      expect(
        calculateAppointmentTotalCents(
            hourlyRateCents: 3333, timeSpentMinutes: 10),
        556,
      );
    });

    test('zero hourly rate still adds product cost', () {
      expect(
        calculateAppointmentTotalCents(
          hourlyRateCents: 0,
          timeSpentMinutes: 60,
          productCostCents: 2500,
        ),
        2500,
      );
    });
  });

  group('formatCents', () {
    test('formats whole and fractional dollars', () {
      expect(formatCents(17500), r'$175.00');
      expect(formatCents(6000), r'$60.00');
      expect(formatCents(5), r'$0.05');
      expect(formatCents(0), r'$0.00');
    });

    test('formats negatives', () {
      expect(formatCents(-2500), r'-$25.00');
    });
  });

  group('toMinutes', () {
    test('combines hours and minutes', () {
      expect(toMinutes(hours: 1, minutes: 30), 90);
      expect(toMinutes(minutes: 45), 45);
      expect(toMinutes(hours: 2), 120);
    });
  });

  group('parseDollarsToCents', () {
    test('blank / null defaults to zero cents', () {
      expect(parseDollarsToCents(''), 0);
      expect(parseDollarsToCents('   '), 0);
      expect(parseDollarsToCents(null), 0);
    });

    test('parses plain and decorated dollar strings', () {
      expect(parseDollarsToCents('80'), 8000);
      expect(parseDollarsToCents('80.5'), 8050);
      expect(parseDollarsToCents(r'$1,234.50'), 123450);
      expect(parseDollarsToCents('0.05'), 5);
    });

    test('returns null for non-money text so callers can flag it', () {
      expect(parseDollarsToCents('abc'), isNull);
      expect(parseDollarsToCents('12.34.56'), isNull);
    });
  });
}
