import 'package:conductor_app/features/projects/project_models.dart';
import 'package:conductor_app/features/todos/todo_models.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Todo', () {
    test('round-trips through JSON', () {
      final todo = Todo.fromJson({
        'id': 7,
        'title': 'Ship it',
        'status': 'OPEN',
        'priority': 'HIGH',
        'category': 'DESIRED_FEATURE',
        'dreamId': 3,
        'order': 2,
        'dueDate': '2026-07-04T00:00:00.000Z',
      });
      final restored = Todo.fromJson(todo.toJson());
      expect(restored.id, 7);
      expect(restored.dreamId, 3);
      expect(restored.order, 2);
      expect(restored.category, 'DESIRED_FEATURE');
      expect(restored.dueDate, isNotNull);
    });

    test('applies safe defaults for missing fields', () {
      final todo = Todo.fromJson({'id': 1, 'title': 'x'});
      expect(todo.status, 'OPEN');
      expect(todo.priority, 'NORMAL');
      expect(todo.dreamId, isNull);
    });
  });

  group('Project', () {
    test('round-trips intent fields', () {
      final project = Project.fromJson({
        'id': 5,
        'slug': 'conductor-app',
        'title': 'Conductor App',
        'goal': 'Ship to stores',
        'flavorText': 'beep boop',
        'liveUrl': 'https://kindrobots.org',
        'repoUrl': 'https://github.com/silasfelinus/conductor',
      });
      final restored = Project.fromJson(project.toJson());
      expect(restored.goal, 'Ship to stores');
      expect(restored.flavorText, 'beep boop');
      expect(restored.liveUrl, 'https://kindrobots.org');
    });

    test('tolerates a server payload with extra/missing fields', () {
      final project = Project.fromJson({
        'id': 1,
        'slug': 's',
        'title': 't',
        'unknownField': {'nested': true},
      });
      expect(project.projectStatus, 'ACTIVE');
    });
  });
}
