import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../auth/auth_controller.dart';
import 'art_models.dart';

/// Browses a project's linked ArtCollections for inspiration, and lets an
/// admin queue a new art request into Conductor's `art-prompts.yaml`.
/// Local mode has no server and no admin concept, so this repository is only
/// ever provided when a remote server is configured (see
/// [artRepositoryProvider]).
abstract class ArtRepository {
  Future<List<ArtCollectionSummary>> collectionsForProject(int projectId);

  Future<void> submitArtRequest({
    required String imagePath,
    String? label,
    String? prompt,
    String? variant,
    String? pageUrl,
  });
}

class RemoteArtRepository implements ArtRepository {
  RemoteArtRepository(this._api);

  final ApiClient _api;

  @override
  Future<List<ArtCollectionSummary>> collectionsForProject(
      int projectId) async {
    final res = await _api.get('/api/dreams/$projectId');
    final dream = unwrap(res, ['dream', 'data']);
    if (dream is! Map<String, dynamic>) return const [];

    final collections = <ArtCollectionSummary>[];

    final primary = dream['ArtCollection'];
    if (primary is Map<String, dynamic>) {
      collections.add(ArtCollectionSummary.fromJson(primary));
    }

    final linked = dream['ArtCollections'];
    if (linked is List) {
      for (final item in linked.whereType<Map<String, dynamic>>()) {
        final summary = ArtCollectionSummary.fromJson(item);
        if (collections.every((c) => c.id != summary.id)) {
          collections.add(summary);
        }
      }
    }

    return collections;
  }

  @override
  Future<void> submitArtRequest({
    required String imagePath,
    String? label,
    String? prompt,
    String? variant,
    String? pageUrl,
  }) {
    return _api.post('/api/conductor/art-request', body: {
      'imagePath': imagePath,
      if (label != null && label.trim().isNotEmpty) 'label': label.trim(),
      if (prompt != null && prompt.trim().isNotEmpty) 'prompt': prompt.trim(),
      if (variant != null && variant.trim().isNotEmpty)
        'variant': variant.trim(),
      if (pageUrl != null && pageUrl.trim().isNotEmpty)
        'pageUrl': pageUrl.trim(),
    });
  }
}

final artRepositoryProvider = Provider<ArtRepository?>((ref) {
  final api = ref.watch(apiClientProvider);
  return api == null ? null : RemoteArtRepository(api);
});

final artCollectionsForProjectProvider = FutureProvider.family
    .autoDispose<List<ArtCollectionSummary>, int>((ref, projectId) async {
  final repo = ref.watch(artRepositoryProvider);
  if (repo == null) return const [];
  return repo.collectionsForProject(projectId);
});
