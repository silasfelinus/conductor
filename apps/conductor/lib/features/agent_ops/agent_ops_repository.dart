import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../auth/auth_controller.dart';

/// Agent Ops is the conductor-repo layer: roadmap tasks, pitches, approvals,
/// and the inbox. It is single-tenant by nature (one conductor repo per
/// server), so it is only surfaced for admins on a server that has the
/// conductor integration configured. General users never see this layer.
///
/// All writes go through the user's JWT; the server enforces the admin role.
class AgentOpsRepository {
  AgentOpsRepository(this._api);

  final ApiClient _api;

  Future<ConductorData> fetch() async {
    final res = await _api.get('/api/conductor/projects');
    return ConductorData.fromJson(res as Map<String, dynamic>);
  }

  Future<void> votePitch(String slug, String vote) =>
      _api.post('/api/conductor/pitch-vote', body: {'slug': slug, 'vote': vote});

  Future<void> sendInboxMessage(String message) =>
      _api.post('/api/conductor/message', body: {'message': message});
}

class ConductorData {
  const ConductorData({this.projects = const [], this.pitches = const []});

  final List<RoadmapProject> projects;
  final List<Pitch> pitches;

  factory ConductorData.fromJson(Map<String, dynamic> json) {
    final data = unwrap(json) as Map<String, dynamic>;
    return ConductorData(
      projects: ((data['projects'] as List?) ?? const [])
          .whereType<Map<String, dynamic>>()
          .map(RoadmapProject.fromJson)
          .toList(),
      pitches: ((data['pitches'] as List?) ?? const [])
          .whereType<Map<String, dynamic>>()
          .map(Pitch.fromJson)
          .toList(),
    );
  }

  /// Tasks across all projects waiting on a human decision.
  List<(RoadmapProject, RoadmapTask)> get approvals => [
        for (final p in projects)
          for (final t in p.tasks)
            if (t.status == 'needs-human' ||
                (t.gateHuman && !t.approvedByHuman && t.status != 'done'))
              (p, t),
      ];
}

class RoadmapProject {
  const RoadmapProject({
    required this.slug,
    required this.title,
    this.kind = 'software',
    this.progress = 0,
    this.tasks = const [],
    this.notesFromSilas,
  });

  final String slug;
  final String title;
  final String kind;
  final num progress;
  final List<RoadmapTask> tasks;
  final String? notesFromSilas;

  factory RoadmapProject.fromJson(Map<String, dynamic> json) => RoadmapProject(
        slug: (json['slug'] as String?) ?? (json['project'] as String?) ?? '',
        title: (json['title'] as String?) ??
            (json['slug'] as String?) ??
            'Untitled',
        kind: (json['kind'] as String?) ?? 'software',
        progress: (json['progress'] as num?) ?? 0,
        tasks: ((json['tasks'] as List?) ?? const [])
            .whereType<Map<String, dynamic>>()
            .map(RoadmapTask.fromJson)
            .toList(),
        notesFromSilas: json['notes_from_silas'] as String? ??
            json['notesFromSilas'] as String?,
      );
}

class RoadmapTask {
  const RoadmapTask({
    required this.id,
    required this.title,
    this.status = 'ready',
    this.note,
    this.stakes,
    this.gateHuman = false,
    this.approvedByHuman = false,
  });

  final String id;
  final String title;
  final String status;
  final String? note;
  final String? stakes;
  final bool gateHuman;
  final bool approvedByHuman;

  factory RoadmapTask.fromJson(Map<String, dynamic> json) => RoadmapTask(
        id: (json['id'] as String?) ?? '',
        title: (json['title'] as String?) ?? '',
        status: (json['status'] as String?) ?? 'ready',
        note: json['note'] as String?,
        stakes: json['stakes'] as String?,
        gateHuman:
            (json['gate_human'] as bool?) ?? (json['gateHuman'] as bool?) ?? false,
        approvedByHuman: (json['approved_by_human'] as bool?) ??
            (json['approvedByHuman'] as bool?) ??
            false,
      );
}

class Pitch {
  const Pitch({required this.slug, required this.title, this.status = ''});

  final String slug;
  final String title;
  final String status; // awaiting-silas | approved | passed | proposed

  factory Pitch.fromJson(Map<String, dynamic> json) => Pitch(
        slug: (json['slug'] as String?) ?? (json['file'] as String?) ?? '',
        title: (json['title'] as String?) ?? 'Untitled pitch',
        status: (json['status'] as String?) ?? '',
      );
}

final agentOpsRepositoryProvider = Provider<AgentOpsRepository?>((ref) {
  final api = ref.watch(apiClientProvider);
  final user = ref.watch(currentUserProvider);
  if (api == null || user == null || !user.isAdmin) return null;
  return AgentOpsRepository(api);
});

final agentOpsDataProvider = FutureProvider<ConductorData?>((ref) async {
  final repo = ref.watch(agentOpsRepositoryProvider);
  if (repo == null) return null;
  return repo.fetch();
});
