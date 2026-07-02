import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/storage/app_storage.dart';
import '../auth/auth_controller.dart';
import 'project_models.dart';

abstract class ProjectsRepository {
  Future<List<Project>> list();
  Future<Project> create({required String title, String? description});
  Future<Project> update(Project project, Map<String, dynamic> patch);
}

class RemoteProjectsRepository implements ProjectsRepository {
  RemoteProjectsRepository(this._api);

  final ApiClient _api;

  @override
  Future<List<Project>> list() async {
    final res = await _api.get('/api/dreams', query: {
      'dreamType': 'PROJECT',
      'mine': '1',
      'take': '100',
    });
    final items = unwrap(res, ['dreams', 'data']);
    return (items as List)
        .whereType<Map<String, dynamic>>()
        .map(Project.fromJson)
        .toList();
  }

  @override
  Future<Project> create({required String title, String? description}) async {
    final res = await _api.post('/api/dreams', body: {
      'title': title,
      'description': description,
      'dreamType': 'PROJECT',
      'projectStatus': 'ACTIVE',
    });
    return Project.fromJson(
        unwrap(res, ['dream', 'data']) as Map<String, dynamic>);
  }

  @override
  Future<Project> update(Project project, Map<String, dynamic> patch) async {
    final res = await _api.patch('/api/dreams/${project.id}', body: patch);
    return Project.fromJson(
        unwrap(res, ['dream', 'data']) as Map<String, dynamic>);
  }
}

/// On-device projects for ServerMode.local — same model, no account needed.
class LocalProjectsRepository implements ProjectsRepository {
  LocalProjectsRepository(this._storage);

  static const _key = 'local_projects';
  final AppStorage _storage;

  List<Project> _read() {
    final raw = _storage.readBlob(_key);
    if (raw == null) return [];
    return (jsonDecode(raw) as List)
        .whereType<Map<String, dynamic>>()
        .map(Project.fromJson)
        .toList();
  }

  Future<void> _write(List<Project> projects) => _storage.writeBlob(
      _key, jsonEncode(projects.map((p) => p.toJson()).toList()));

  @override
  Future<List<Project>> list() async => _read();

  @override
  Future<Project> create({required String title, String? description}) async {
    final projects = _read();
    final nextId = projects.isEmpty
        ? 1
        : projects.map((p) => p.id).reduce((a, b) => a > b ? a : b) + 1;
    final slug = title
        .toLowerCase()
        .replaceAll(RegExp(r'[^a-z0-9]+'), '-')
        .replaceAll(RegExp(r'^-+|-+$'), '');
    final project = Project(
      id: nextId,
      slug: slug.isEmpty ? 'project-$nextId' : slug,
      title: title,
      description: description,
    );
    await _write([...projects, project]);
    return project;
  }

  @override
  Future<Project> update(Project project, Map<String, dynamic> patch) async {
    final merged = Project.fromJson({...project.toJson(), ...patch});
    final projects =
        _read().map((p) => p.id == project.id ? merged : p).toList();
    await _write(projects);
    return merged;
  }
}

final projectsRepositoryProvider = Provider<ProjectsRepository?>((ref) {
  final config = ref.watch(serverConfigProvider);
  if (config == null) return null;
  if (config.isLocal) {
    return LocalProjectsRepository(ref.watch(appStorageProvider));
  }
  final api = ref.watch(apiClientProvider);
  return api == null ? null : RemoteProjectsRepository(api);
});

final projectsProvider = FutureProvider<List<Project>>((ref) async {
  final repo = ref.watch(projectsRepositoryProvider);
  if (repo == null) return [];
  final projects = await repo.list();
  const priorityRank = {'HIGH': 0, 'NORMAL': 1, 'LOW': 2};
  projects.sort((a, b) => (priorityRank[a.priority] ?? 1)
      .compareTo(priorityRank[b.priority] ?? 1));
  return projects;
});
