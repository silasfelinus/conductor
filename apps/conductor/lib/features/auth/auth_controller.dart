import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/config/server_config.dart';
import '../../core/storage/app_storage.dart';
import 'auth_models.dart';

/// The chosen server mode, persisted across launches. Null until onboarding
/// picks one.
class ServerConfigController extends Notifier<ServerConfig?> {
  @override
  ServerConfig? build() => ref.watch(appStorageProvider).readServerConfig();

  Future<void> select(ServerConfig config) async {
    await ref.read(appStorageProvider).writeServerConfig(config);
    state = config;
  }

  Future<void> reset() async {
    final storage = ref.read(appStorageProvider);
    await storage.clearServerConfig();
    await storage.clearJwt();
    state = null;
  }
}

final serverConfigProvider =
    NotifierProvider<ServerConfigController, ServerConfig?>(
        ServerConfigController.new);

final apiClientProvider = Provider<ApiClient?>((ref) {
  final config = ref.watch(serverConfigProvider);
  if (config == null || config.isLocal) return null;
  final storage = ref.watch(appStorageProvider);
  return ApiClient(
    baseUrl: config.effectiveBaseUrl,
    tokenProvider: storage.readJwt,
  );
});

sealed class AuthState {
  const AuthState();
}

class SignedOut extends AuthState {
  const SignedOut();
}

class SignedIn extends AuthState {
  const SignedIn(this.user);
  final AppUser user;
}

/// Local mode has no accounts; the whole device is one workspace.
class LocalUser extends AuthState {
  const LocalUser();
}

class AuthController extends AsyncNotifier<AuthState> {
  @override
  Future<AuthState> build() async {
    final config = ref.watch(serverConfigProvider);
    if (config == null) return const SignedOut();
    if (config.isLocal) return const LocalUser();
    final api = ref.watch(apiClientProvider);
    final storage = ref.read(appStorageProvider);
    final jwt = await storage.readJwt();
    if (api == null || jwt == null || jwt.isEmpty) return const SignedOut();
    try {
      final me = unwrap(await api.get('/api/users/me'), ['user', 'data']);
      return SignedIn(AppUser.fromJson(me as Map<String, dynamic>));
    } on ApiException catch (e) {
      if (e.isUnauthorized) {
        await storage.clearJwt();
        return const SignedOut();
      }
      rethrow;
    }
  }

  Future<void> login(String username, String password) async {
    final api = ref.read(apiClientProvider);
    if (api == null) throw StateError('No server configured');
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final res = await api.post('/api/auth/login',
          body: {'username': username, 'password': password});
      final map = res as Map<String, dynamic>;
      final token = (map['token'] ??
              (map['data'] is Map ? (map['data'] as Map)['token'] : null))
          as String?;
      if (token == null || token.isEmpty) {
        throw ApiException(500, 'Login response contained no token');
      }
      await ref.read(appStorageProvider).writeJwt(token);
      final me = unwrap(await api.get('/api/users/me'), ['user', 'data']);
      return SignedIn(AppUser.fromJson(me as Map<String, dynamic>));
    });
  }

  Future<void> register(String username, String email, String password) async {
    final api = ref.read(apiClientProvider);
    if (api == null) throw StateError('No server configured');
    await api.post('/api/users/register',
        body: {'username': username, 'email': email, 'password': password});
    await login(username, password);
  }

  Future<void> logout() async {
    await ref.read(appStorageProvider).clearJwt();
    ref.invalidateSelf();
  }

  /// Permanently deletes the signed-in user's account and everything they
  /// own (server-side cascade — see kind_robots' `deleteUserWithOwnedData`).
  /// Irreversible; the caller is responsible for confirming with the user
  /// before calling this. On success the app is returned to the welcome
  /// screen, same as "Switch server mode".
  Future<void> deleteAccount() async {
    final api = ref.read(apiClientProvider);
    final current = state.valueOrNull;
    if (api == null || current is! SignedIn) {
      throw StateError('No signed-in account to delete');
    }
    await api.delete('/api/users/${current.user.id}');
    await ref.read(serverConfigProvider.notifier).reset();
  }
}

final authControllerProvider =
    AsyncNotifierProvider<AuthController, AuthState>(AuthController.new);

final currentUserProvider = Provider<AppUser?>((ref) {
  final auth = ref.watch(authControllerProvider).valueOrNull;
  return auth is SignedIn ? auth.user : null;
});
