import 'package:flutter/material.dart';

import 'route_models.dart';
import 'route_services.dart';

void main() => runApp(const FieldClientApp());

class FieldClientApp extends StatelessWidget {
  const FieldClientApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'Humboldt Scoop Route',
        theme: ThemeData(colorSchemeSeed: Colors.teal, useMaterial3: true),
        home: RouteScreen(api: DummyRouteApi(), navigation: InstalledNavigationService(), storage: MemoryRouteStorage()),
      );
}

class RouteScreen extends StatefulWidget {
  const RouteScreen({required this.api, required this.navigation, required this.storage, super.key});

  final RouteApi api;
  final NavigationService navigation;
  final RouteStorage storage;

  @override
  State<RouteScreen> createState() => _RouteScreenState();
}

class _RouteScreenState extends State<RouteScreen> {
  CrewRoute? route;
  String? error;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    try {
      final value = await widget.api.fetchToday();
      if (mounted) setState(() => route = value);
    } catch (exception) {
      if (mounted) setState(() => error = exception.toString());
    }
  }

  Future<void> complete(RouteStop stop, String notes) async {
    final updated = stop.copyWith(completed: true, crewNotes: notes);
    await widget.api.completeStop(updated);
    final next = route!.updateStop(updated);
    await widget.storage.save(next);
    if (mounted) setState(() => route = next);
  }

  @override
  Widget build(BuildContext context) {
    if (error != null) return Scaffold(body: Center(child: Text(error!)));
    if (route == null) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    final next = route!.nextStop;
    return Scaffold(
      appBar: AppBar(title: const Text("Today's route")),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(next == null ? 'Route complete 🎉' : 'Next: ${next.customerName}', style: Theme.of(context).textTheme.headlineSmall),
                if (next != null) ...[
                  const SizedBox(height: 8),
                  Text(next.addressLabel),
                  const SizedBox(height: 12),
                  FilledButton.icon(onPressed: () => widget.navigation.open(next), icon: const Icon(Icons.navigation), label: const Text('Open navigation')),
                ],
              ]),
            ),
          ),
          const SizedBox(height: 12),
          ...route!.stops.map((stop) => StopCard(stop: stop, onComplete: complete)),
        ],
      ),
    );
  }
}

class StopCard extends StatefulWidget {
  const StopCard({required this.stop, required this.onComplete, super.key});

  final RouteStop stop;
  final Future<void> Function(RouteStop, String) onComplete;

  @override
  State<StopCard> createState() => _StopCardState();
}

class _StopCardState extends State<StopCard> {
  final notes = TextEditingController();

  @override
  void dispose() {
    notes.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              Icon(widget.stop.completed ? Icons.check_circle : Icons.pets),
              const SizedBox(width: 8),
              Expanded(child: Text(widget.stop.customerName, style: Theme.of(context).textTheme.titleLarge)),
            ]),
            const SizedBox(height: 8),
            Text(widget.stop.petNotes),
            Text(widget.stop.yardNotes),
            const SizedBox(height: 12),
            TextField(controller: notes, enabled: !widget.stop.completed, decoration: const InputDecoration(labelText: 'Crew notes', border: OutlineInputBorder()), minLines: 2, maxLines: 4),
            const SizedBox(height: 12),
            FilledButton(onPressed: widget.stop.completed ? null : () => widget.onComplete(widget.stop, notes.text.trim()), child: Text(widget.stop.completed ? 'Completed' : 'Complete visit')),
          ]),
        ),
      );
}
