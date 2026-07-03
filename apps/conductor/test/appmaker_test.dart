import 'package:conductor_app/features/appmaker/appmaker_repository.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('AppsInventory', () {
    test('parses the /api/appmaker/apps response shape', () {
      final inventory = AppsInventory.fromJson({
        'success': true,
        'data': {
          'scaffolded': ['conductor', 'recipe-box'],
          'pending': [
            {
              'slug': 'dream-journal',
              'dreamId': 42,
              'requestedAt': '2026-07-03T00:00:00.000Z',
            },
          ],
        },
      });
      expect(inventory.scaffolded, ['conductor', 'recipe-box']);
      expect(inventory.pending.single.slug, 'dream-journal');
      expect(inventory.pending.single.requestedAt, isNotNull);
    });

    test('tolerates empty and missing fields', () {
      final inventory = AppsInventory.fromJson({'data': {}});
      expect(inventory.scaffolded, isEmpty);
      expect(inventory.pending, isEmpty);
    });
  });

  group('slugify', () {
    test('matches the server convention', () {
      expect(slugify('Recipe Box!'), 'recipe-box');
      expect(slugify('  --Weird   Name--  '), 'weird-name');
      expect(slugify('A' * 60).length, 40);
    });
  });
}
