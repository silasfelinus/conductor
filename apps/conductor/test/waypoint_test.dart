import 'package:conductor_app/features/projects/project_models.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Waypoint parsing', () {
    test('parses the three status prefixes', () {
      final waypoints =
          Waypoint.parseList('✓ shipped step|~ current step|future step');
      expect(waypoints, hasLength(3));
      expect(waypoints[0].status, WaypointStatus.done);
      expect(waypoints[0].label, 'shipped step');
      expect(waypoints[1].status, WaypointStatus.inProgress);
      expect(waypoints[2].status, WaypointStatus.todo);
    });

    test('round-trips through serialize', () {
      const raw = '✓ a|~ b|c';
      expect(Waypoint.serializeList(Waypoint.parseList(raw)), raw);
    });

    test('handles null and empty input', () {
      expect(Waypoint.parseList(null), isEmpty);
      expect(Waypoint.parseList('  '), isEmpty);
    });
  });
}
