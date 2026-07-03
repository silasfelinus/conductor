import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiException implements Exception {
  ApiException(this.statusCode, this.message);

  final int statusCode;
  final String message;

  bool get isUnauthorized => statusCode == 401;

  @override
  String toString() => 'ApiException($statusCode): $message';
}

/// Thin JSON HTTP client. All authenticated calls send the current user's
/// JWT as a Bearer token — there is deliberately no admin-token path here;
/// privileged actions are authorized server-side by the user's role.
class ApiClient {
  ApiClient({required this.baseUrl, required this.tokenProvider, http.Client? inner})
      : _inner = inner ?? http.Client();

  final String baseUrl;
  final Future<String?> Function() tokenProvider;
  final http.Client _inner;

  Future<dynamic> get(String path, {Map<String, String>? query}) =>
      _send('GET', path, query: query);

  Future<dynamic> post(String path, {Object? body}) =>
      _send('POST', path, body: body);

  Future<dynamic> patch(String path, {Object? body}) =>
      _send('PATCH', path, body: body);

  Future<dynamic> delete(String path) => _send('DELETE', path);

  /// POSTs and yields the raw lines of a server-sent-event response.
  /// Callers parse the `data:` payloads themselves.
  Stream<String> postEventStream(String path, {Object? body}) async* {
    final request = http.Request('POST', Uri.parse('$baseUrl$path'));
    request.headers['Accept'] = 'text/event-stream';
    final token = await tokenProvider();
    if (token != null && token.isNotEmpty) {
      request.headers['Authorization'] = 'Bearer $token';
    }
    if (body != null) {
      request.headers['Content-Type'] = 'application/json';
      request.body = jsonEncode(body);
    }
    final response = await _inner.send(request);
    if (response.statusCode >= 400) {
      final text = await response.stream.bytesToString();
      throw ApiException(
          response.statusCode, text.isEmpty ? 'Stream request failed' : text);
    }
    yield* response.stream
        .transform(utf8.decoder)
        .transform(const LineSplitter());
  }

  Future<dynamic> _send(
    String method,
    String path, {
    Map<String, String>? query,
    Object? body,
  }) async {
    final uri = Uri.parse('$baseUrl$path').replace(queryParameters: query);
    final request = http.Request(method, uri);
    request.headers['Accept'] = 'application/json';
    final token = await tokenProvider();
    if (token != null && token.isNotEmpty) {
      request.headers['Authorization'] = 'Bearer $token';
    }
    if (body != null) {
      request.headers['Content-Type'] = 'application/json';
      request.body = jsonEncode(body);
    }
    final streamed = await _inner.send(request);
    final response = await http.Response.fromStream(streamed);
    if (response.statusCode >= 400) {
      String message = response.reasonPhrase ?? 'Request failed';
      try {
        final decoded = jsonDecode(response.body);
        if (decoded is Map && decoded['message'] is String) {
          message = decoded['message'] as String;
        }
      } catch (_) {}
      throw ApiException(response.statusCode, message);
    }
    if (response.body.isEmpty) return null;
    return jsonDecode(response.body);
  }
}

/// kind_robots wraps most payloads as { success, data | <entity> }.
/// Unwrap defensively so the client survives shape drift between servers.
dynamic unwrap(dynamic json, [List<String> keys = const ['data']]) {
  if (json is! Map<String, dynamic>) return json;
  for (final key in keys) {
    if (json[key] != null) return json[key];
  }
  return json;
}
