import 'dart:convert';

/// How the app talks to the outside world.
///
/// - [hosted]: our server (kindrobots.org). Account required; paid tier later.
/// - [selfHosted]: any kind_robots instance the user runs. Same API contract.
/// - [local]: no server at all. Data lives on-device only.
enum ServerMode { hosted, selfHosted, local }

class ServerConfig {
  const ServerConfig({required this.mode, this.baseUrl = ''});

  final ServerMode mode;

  /// Only meaningful for [ServerMode.selfHosted].
  final String baseUrl;

  static const String hostedUrl = 'https://kindrobots.org';

  static const ServerConfig unset = ServerConfig(mode: ServerMode.local);

  bool get isLocal => mode == ServerMode.local;

  String get effectiveBaseUrl => switch (mode) {
        ServerMode.hosted => hostedUrl,
        ServerMode.selfHosted => baseUrl,
        ServerMode.local => '',
      };

  /// Turns a server-relative asset path (e.g. /images/foo.webp) into a
  /// fetchable URL. Returns null in local mode or for empty paths.
  String? resolveAssetUrl(String? path) {
    if (path == null || path.isEmpty || isLocal) return null;
    if (path.startsWith('http')) return path;
    final base = effectiveBaseUrl;
    return path.startsWith('/') ? '$base$path' : '$base/$path';
  }

  String toJsonString() =>
      jsonEncode({'mode': mode.name, 'baseUrl': baseUrl});

  static ServerConfig? fromJsonString(String? raw) {
    if (raw == null || raw.isEmpty) return null;
    try {
      final map = jsonDecode(raw) as Map<String, dynamic>;
      return ServerConfig(
        mode: ServerMode.values.byName(map['mode'] as String),
        baseUrl: (map['baseUrl'] as String?) ?? '',
      );
    } catch (_) {
      return null;
    }
  }
}
