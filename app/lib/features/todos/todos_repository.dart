import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/storage/app_storage.dart';
import '../auth/auth_controller.dart';
import 'todo_models.dart';

abstract class TodosRepository {
  Future<List<Todo>> list({bool includeArchived = false});
  Future<Todo> create(Map<String, dynamic> fields);
  Future<Todo> update(Todo todo, Map<String, dynamic> patch);
  Future<void> delete(Todo todo);
}

class RemoteTodosRepository implements TodosRepository {
  RemoteTodosRepository(this._api, this._storage);

  static const _cacheKey = 'cache_todos';
  final ApiClient _api;
  final AppStorage _storage;

  @override
  Future<List<Todo>> list({bool includeArchived = false}) async {
    try {
      final res = await _api.get('/api/todos',
          query: includeArchived ? {'includeArchived': '1'} : null);
      final items = unwrap(res, ['todos', 'data']);
      final todos = (items as List)
          .whereType<Map<String, dynamic>>()
          .map(Todo.fromJson)
          .toList();
      if (includeArchived) {
        await _storage.writeBlob(
            _cacheKey, jsonEncode(todos.map((t) => t.toJson()).toList()));
      }
      return todos;
    } on ApiException {
      rethrow;
    } catch (_) {
      final cached = _storage.readBlob(_cacheKey);
      if (cached == null) rethrow;
      final todos = (jsonDecode(cached) as List)
          .whereType<Map<String, dynamic>>()
          .map(Todo.fromJson)
          .toList();
      return includeArchived
          ? todos
          : todos.where((t) => t.status != 'ARCHIVED').toList();
    }
  }

  @override
  Future<Todo> create(Map<String, dynamic> fields) async {
    final res = await _api.post('/api/todos', body: fields);
    return Todo.fromJson(unwrap(res, ['todo', 'data']) as Map<String, dynamic>);
  }

  @override
  Future<Todo> update(Todo todo, Map<String, dynamic> patch) async {
    final res = await _api.patch('/api/todos/${todo.id}', body: patch);
    return Todo.fromJson(unwrap(res, ['todo', 'data']) as Map<String, dynamic>);
  }

  @override
  Future<void> delete(Todo todo) => _api.delete('/api/todos/${todo.id}');
}

class LocalTodosRepository implements TodosRepository {
  LocalTodosRepository(this._storage);

  static const _key = 'local_todos';
  final AppStorage _storage;

  List<Todo> _read() {
    final raw = _storage.readBlob(_key);
    if (raw == null) return [];
    return (jsonDecode(raw) as List)
        .whereType<Map<String, dynamic>>()
        .map(Todo.fromJson)
        .toList();
  }

  Future<void> _write(List<Todo> todos) => _storage.writeBlob(
      _key, jsonEncode(todos.map((t) => t.toJson()).toList()));

  @override
  Future<List<Todo>> list({bool includeArchived = false}) async {
    final todos = _read();
    return includeArchived
        ? todos
        : todos.where((t) => t.status != 'ARCHIVED').toList();
  }

  @override
  Future<Todo> create(Map<String, dynamic> fields) async {
    final todos = _read();
    final nextId = todos.isEmpty
        ? 1
        : todos.map((t) => t.id).reduce((a, b) => a > b ? a : b) + 1;
    final todo = Todo.fromJson({'id': nextId, ...fields});
    await _write([...todos, todo]);
    return todo;
  }

  @override
  Future<Todo> update(Todo todo, Map<String, dynamic> patch) async {
    final merged = Todo.fromJson({...todo.toJson(), ...patch});
    await _write(_read().map((t) => t.id == todo.id ? merged : t).toList());
    return merged;
  }

  @override
  Future<void> delete(Todo todo) async {
    await _write(_read().where((t) => t.id != todo.id).toList());
  }
}

final todosRepositoryProvider = Provider<TodosRepository?>((ref) {
  final config = ref.watch(serverConfigProvider);
  if (config == null) return null;
  if (config.isLocal) return LocalTodosRepository(ref.watch(appStorageProvider));
  final api = ref.watch(apiClientProvider);
  return api == null
      ? null
      : RemoteTodosRepository(api, ref.watch(appStorageProvider));
});

class TodosController extends AsyncNotifier<List<Todo>> {
  @override
  Future<List<Todo>> build() async {
    final repo = ref.watch(todosRepositoryProvider);
    if (repo == null) return [];
    final todos = await repo.list(includeArchived: true);
    const priorityRank = {'HIGH': 0, 'NORMAL': 1, 'LOW': 2};
    todos.sort((a, b) => (priorityRank[a.priority] ?? 1)
        .compareTo(priorityRank[b.priority] ?? 1));
    return todos;
  }

  Future<void> create(Map<String, dynamic> fields) async {
    final repo = ref.read(todosRepositoryProvider);
    if (repo == null) return;
    await repo.create(fields);
    ref.invalidateSelf();
  }

  Future<void> setStatus(Todo todo, String status) async {
    final repo = ref.read(todosRepositoryProvider);
    if (repo == null) return;
    await repo.update(todo, {'status': status});
    ref.invalidateSelf();
  }

  @override
  Future<void> update(Todo todo, Map<String, dynamic> patch) async {
    final repo = ref.read(todosRepositoryProvider);
    if (repo == null) return;
    await repo.update(todo, patch);
    ref.invalidateSelf();
  }

  Future<void> delete(Todo todo) async {
    final repo = ref.read(todosRepositoryProvider);
    if (repo == null) return;
    await repo.delete(todo);
    ref.invalidateSelf();
  }
}

final todosControllerProvider =
    AsyncNotifierProvider<TodosController, List<Todo>>(TodosController.new);
