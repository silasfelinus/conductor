import 'dart:convert';

import 'package:conductor_app/core/api/api_client.dart';
import 'package:conductor_app/core/config/server_config.dart';
import 'package:conductor_app/core/storage/app_storage.dart';
import 'package:conductor_app/features/auth/auth_controller.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

/// In-memory stand-in for [AppStorage] so tests never touch the real
/// secure-storage platform channel (unavailable under plain `flutter test`).
class _FakeAppStorage implements AppStorage {
  ServerConfig? _config;
  String? _jwt;
  final Map<String, String> _blobs = {};

  @override
  ServerConfig? readServerConfig() => _config;

  @override
  Future<void> writeServerConfig(ServerConfig config) async => _config = config;

  @override
  Future<void> clearServerConfig() async => _config = null;

  @override
  Future<String?> readJwt() async => _jwt;

  @override
  Future<void> writeJwt(String token) async => _jwt = token;

  @override
  Future<void> clearJwt() async => _jwt = null;

  @override
  String? readBlob(String key) => _blobs[key];

  @override
  Future<void> writeBlob(String key, String value) async => _blobs[key] = value;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  const config = ServerConfig(
      mode: ServerMode.selfHosted, baseUrl: 'https://example.test');

  ProviderContainer buildContainer(
      http.Client mockClient, _FakeAppStorage storage) {
    final container = ProviderContainer(overrides: [
      appStorageProvider.overrideWithValue(storage),
      apiClientProvider.overrideWithValue(
        ApiClient(
            baseUrl: config.baseUrl,
            tokenProvider: storage.readJwt,
            inner: mockClient),
      ),
    ]);
    addTearDown(container.dispose);
    return container;
  }

  group('AuthController.deleteAccount', () {
    test('DELETEs the signed-in user then resets server config and jwt',
        () async {
      final requests = <http.Request>[];
      final mockClient = MockClient((request) async {
        requests.add(request);
        if (request.method == 'GET' && request.url.path == '/api/users/me') {
          return http.Response(
              jsonEncode({
                'user': {'id': 42, 'username': 'silas'}
              }),
              200);
        }
        if (request.method == 'DELETE' && request.url.path == '/api/users/42') {
          return http.Response(
              jsonEncode({
                'success': true,
                'data': {'purged': {}}
              }),
              200);
        }
        return http.Response(
            'unexpected request: ${request.method} ${request.url.path}', 404);
      });

      final storage = _FakeAppStorage()
        ..writeJwt('tok')
        .._config = config;
      final container = buildContainer(mockClient, storage);

      final signedIn = await container.read(authControllerProvider.future);
      expect(signedIn, isA<SignedIn>());
      expect((signedIn as SignedIn).user.id, 42);

      await container.read(authControllerProvider.notifier).deleteAccount();

      expect(
        requests
            .any((r) => r.method == 'DELETE' && r.url.path == '/api/users/42'),
        isTrue,
        reason: 'expected a DELETE /api/users/42 call',
      );
      expect(container.read(serverConfigProvider), isNull);
      expect(await storage.readJwt(), isNull);
    });

    test('throws and makes no request when nobody is signed in', () async {
      final requests = <http.Request>[];
      final mockClient = MockClient((request) async {
        requests.add(request);
        return http.Response('', 401);
      });

      final storage = _FakeAppStorage()
        .._config = const ServerConfig(mode: ServerMode.local);
      final container = buildContainer(mockClient, storage);

      final state = await container.read(authControllerProvider.future);
      expect(state, isA<LocalUser>());

      await expectLater(
        () => container.read(authControllerProvider.notifier).deleteAccount(),
        throwsA(isA<StateError>()),
      );
      expect(requests, isEmpty);
    });
  });
}
