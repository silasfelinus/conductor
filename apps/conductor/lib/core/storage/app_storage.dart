import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../config/server_config.dart';

/// Overridden in main() with the real instance.
final sharedPrefsProvider = Provider<SharedPreferences>(
  (ref) => throw UnimplementedError('set in main()'),
);

final appStorageProvider = Provider<AppStorage>(
  (ref) => AppStorage(ref.watch(sharedPrefsProvider)),
);

/// Non-secret app state goes in SharedPreferences; the JWT goes in the
/// platform keychain/keystore via flutter_secure_storage. No API keys or
/// admin tokens are ever stored in the app or its config.
class AppStorage {
  AppStorage(this._prefs);

  final SharedPreferences _prefs;
  final FlutterSecureStorage _secure = const FlutterSecureStorage();

  static const _kServerConfig = 'server_config';
  static const _kJwt = 'kr_jwt';

  ServerConfig? readServerConfig() =>
      ServerConfig.fromJsonString(_prefs.getString(_kServerConfig));

  Future<void> writeServerConfig(ServerConfig config) =>
      _prefs.setString(_kServerConfig, config.toJsonString());

  Future<void> clearServerConfig() async {
    await _prefs.remove(_kServerConfig);
  }

  Future<String?> readJwt() => _secure.read(key: _kJwt);

  Future<void> writeJwt(String token) => _secure.write(key: _kJwt, value: token);

  Future<void> clearJwt() => _secure.delete(key: _kJwt);

  /// Generic JSON blob storage for local-mode repositories.
  String? readBlob(String key) => _prefs.getString('blob_$key');

  Future<void> writeBlob(String key, String value) =>
      _prefs.setString('blob_$key', value);
}
