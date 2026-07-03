import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../auth/auth_controller.dart';

/// The AppMaker fleet, mirroring GET /api/appmaker/apps:
/// [scaffolded] apps have a workspace folder in the conductor repo;
/// [pending] requests are filed but waiting for the next Worker cycle.
class AppsInventory {
  const AppsInventory({this.scaffolded = const [], this.pending = const []});

  final List<String> scaffolded;
  final List<PendingScaffold> pending;

  factory AppsInventory.fromJson(Map<String, dynamic> json) {
    final data = Map<String, dynamic>.from(unwrap(json) as Map);
    return AppsInventory(
      scaffolded: ((data['scaffolded'] as List?) ?? const [])
          .whereType<String>()
          .toList(),
      pending: ((data['pending'] as List?) ?? const [])
          .whereType<Map<String, dynamic>>()
          .map(PendingScaffold.fromJson)
          .toList(),
    );
  }
}

class PendingScaffold {
  const PendingScaffold({required this.slug, this.requestedAt});

  final String slug;
  final DateTime? requestedAt;

  factory PendingScaffold.fromJson(Map<String, dynamic> json) =>
      PendingScaffold(
        slug: (json['slug'] as String?) ?? '',
        requestedAt: json['requestedAt'] != null
            ? DateTime.tryParse(json['requestedAt'] as String)
            : null,
      );
}

String slugify(String value) {
  final slug = value
      .toLowerCase()
      .trim()
      .replaceAll(RegExp(r'[^a-z0-9]+'), '-')
      .replaceAll(RegExp(r'^-+|-+$'), '');
  return slug.length > 40 ? slug.substring(0, 40) : slug;
}

class AppmakerRepository {
  AppmakerRepository(this._api);

  final ApiClient _api;

  Future<AppsInventory> fetchApps() async {
    final res = await _api.get('/api/appmaker/apps');
    return AppsInventory.fromJson(res as Map<String, dynamic>);
  }

  /// Files a scaffold request. The server creates the Dream (slug parity)
  /// and queues the AGENT todo; the app appears after the next Worker cycle.
  Future<String> requestScaffold({
    required String title,
    String? slug,
    String? description,
  }) async {
    final res = await _api.post('/api/appmaker/scaffold-request', body: {
      'title': title,
      if (slug != null && slug.isNotEmpty) 'slug': slug,
      if (description != null && description.isNotEmpty)
        'description': description,
    });
    final data = unwrap(res) as Map<String, dynamic>;
    return (data['slug'] as String?) ?? slug ?? slugify(title);
  }
}

final appmakerRepositoryProvider = Provider<AppmakerRepository?>((ref) {
  final api = ref.watch(apiClientProvider);
  return api == null ? null : AppmakerRepository(api);
});

final appsInventoryProvider = FutureProvider<AppsInventory?>((ref) async {
  final repo = ref.watch(appmakerRepositoryProvider);
  if (repo == null) return null;
  return repo.fetchApps();
});
