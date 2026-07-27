import 'package:flutter_test/flutter_test.dart';
import 'package:humboldt_scoop_field_client/route_models.dart';

void main() {
  test('nextStop advances after completion without changing order', () {
    const first = RouteStop(id: 'one', customerName: 'One', addressLabel: 'A', petNotes: '', yardNotes: '', latitude: 1, longitude: 1);
    const second = RouteStop(id: 'two', customerName: 'Two', addressLabel: 'B', petNotes: '', yardNotes: '', latitude: 2, longitude: 2);
    final route = CrewRoute(date: DateTime(2026, 7, 27), stops: const [first, second]);

    final updated = route.updateStop(first.copyWith(completed: true, crewNotes: 'Gate secured'));

    expect(updated.stops.map((stop) => stop.id), ['one', 'two']);
    expect(updated.stops.first.crewNotes, 'Gate secured');
    expect(updated.nextStop?.id, 'two');
  });
}
