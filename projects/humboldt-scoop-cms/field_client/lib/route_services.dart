import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

import 'route_models.dart';

abstract interface class RouteApi {
  Future<CrewRoute> fetchToday();
  Future<void> completeStop(RouteStop stop);
}

class HttpRouteApi implements RouteApi {
  HttpRouteApi(this.baseUrl, {http.Client? client}) : _client = client ?? http.Client();

  final Uri baseUrl;
  final http.Client _client;

  @override
  Future<CrewRoute> fetchToday() async {
    final response = await _client.get(baseUrl.resolve('/routes/today'));
    if (response.statusCode != 200) throw StateError('Route request failed (${response.statusCode})');
    final payload = jsonDecode(response.body) as Map<String, dynamic>;
    final stops = (payload['stops'] as List<dynamic>? ?? const [])
        .map((value) => RouteStop.fromJson(value as Map<String, dynamic>))
        .toList();
    return CrewRoute(date: DateTime.now(), stops: stops);
  }

  @override
  Future<void> completeStop(RouteStop stop) async {
    final response = await _client.post(
      baseUrl.resolve('/visits/${stop.id}/complete'),
      headers: {'content-type': 'application/json'},
      body: jsonEncode({'notes': stop.crewNotes}),
    );
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw StateError('Completion failed (${response.statusCode})');
    }
  }
}

class DummyRouteApi implements RouteApi {
  @override
  Future<CrewRoute> fetchToday() async => CrewRoute(date: DateTime.now(), stops: const [
        RouteStop(id: 'visit-1', customerName: 'Maya Chen', addressLabel: 'Arcata sample stop', petNotes: 'Juniper is friendly; close the side gate.', yardNotes: 'Start behind the shed.', latitude: 40.8665, longitude: -124.0828),
        RouteStop(id: 'visit-2', customerName: 'Theo Alvarez', addressLabel: 'Eureka sample stop', petNotes: 'Pepper may bark from the window.', yardNotes: 'Avoid the vegetable beds.', latitude: 40.8021, longitude: -124.1637),
      ]);

  @override
  Future<void> completeStop(RouteStop stop) async {}
}

abstract interface class NavigationService {
  Future<bool> open(RouteStop stop);
}

class InstalledNavigationService implements NavigationService {
  @override
  Future<bool> open(RouteStop stop) => launchUrl(
        Uri.parse('https://www.google.com/maps/dir/?api=1&destination=${stop.latitude},${stop.longitude}'),
        mode: LaunchMode.externalApplication,
      );
}

abstract interface class RouteStorage {
  Future<void> save(CrewRoute route);
}

class MemoryRouteStorage implements RouteStorage {
  CrewRoute? latest;

  @override
  Future<void> save(CrewRoute route) async => latest = route;
}
