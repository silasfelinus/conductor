import 'package:conductor_app/core/config/server_config.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('ServerConfig', () {
    test('round-trips through JSON', () {
      const config =
          ServerConfig(mode: ServerMode.selfHosted, baseUrl: 'https://kr.me');
      final restored = ServerConfig.fromJsonString(config.toJsonString());
      expect(restored!.mode, ServerMode.selfHosted);
      expect(restored.baseUrl, 'https://kr.me');
    });

    test('effectiveBaseUrl per mode', () {
      expect(const ServerConfig(mode: ServerMode.hosted).effectiveBaseUrl,
          ServerConfig.hostedUrl);
      expect(
          const ServerConfig(mode: ServerMode.selfHosted, baseUrl: 'https://x.y')
              .effectiveBaseUrl,
          'https://x.y');
      expect(const ServerConfig(mode: ServerMode.local).effectiveBaseUrl, '');
    });

    test('rejects garbage input gracefully', () {
      expect(ServerConfig.fromJsonString(null), isNull);
      expect(ServerConfig.fromJsonString(''), isNull);
      expect(ServerConfig.fromJsonString('not json'), isNull);
      expect(ServerConfig.fromJsonString('{"mode":"bogus"}'), isNull);
    });
  });
}
