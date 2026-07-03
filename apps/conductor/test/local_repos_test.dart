import 'package:conductor_app/core/storage/app_storage.dart';
import 'package:conductor_app/features/projects/projects_repository.dart';
import 'package:conductor_app/features/todos/todos_repository.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

Future<AppStorage> freshStorage() async {
  SharedPreferences.setMockInitialValues({});
  return AppStorage(await SharedPreferences.getInstance());
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('LocalProjectsRepository', () {
    test('creates projects with slugs and incrementing ids', () async {
      final repo = LocalProjectsRepository(await freshStorage());
      final a = await repo.create(title: 'My Great App!');
      final b = await repo.create(title: 'Second');
      expect(a.slug, 'my-great-app');
      expect(b.id, a.id + 1);
      expect(await repo.list(), hasLength(2));
    });

    test('update merges a patch and persists it', () async {
      final repo = LocalProjectsRepository(await freshStorage());
      final project = await repo.create(title: 'P');
      await repo.update(project, {'goal': 'win', 'priority': 'HIGH'});
      final reloaded = (await repo.list()).single;
      expect(reloaded.goal, 'win');
      expect(reloaded.priority, 'HIGH');
      expect(reloaded.title, 'P');
    });
  });

  group('LocalTodosRepository', () {
    test('full CRUD cycle', () async {
      final repo = LocalTodosRepository(await freshStorage());
      final todo = await repo
          .create({'title': 'task', 'status': 'OPEN', 'priority': 'NORMAL'});
      expect((await repo.list()).single.title, 'task');

      await repo.update(todo, {'status': 'DONE'});
      expect((await repo.list()).single.status, 'DONE');

      await repo.update(todo, {'status': 'ARCHIVED'});
      expect(await repo.list(), isEmpty);
      expect(await repo.list(includeArchived: true), hasLength(1));

      await repo.delete(todo);
      expect(await repo.list(includeArchived: true), isEmpty);
    });
  });
}
