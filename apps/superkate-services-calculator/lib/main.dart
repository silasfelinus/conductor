import 'package:flutter/material.dart';

import 'data/in_memory_persistence_service.dart';
import 'data/persistence_service.dart';
import 'domain/money.dart';
import 'ui/new_appointment_form.dart';

void main() => runApp(const SuperkateServicesCalculatorApp());

class SuperkateServicesCalculatorApp extends StatelessWidget {
  const SuperkateServicesCalculatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    const purple = Color(0xFF8B5CF6);
    const teal = Color(0xFF14B8A6);
    const surface = Color(0xFF171224);

    return MaterialApp(
      title: 'Superkate Services Calculator',
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: purple,
          brightness: Brightness.dark,
          primary: purple,
          secondary: teal,
          surface: surface,
        ),
        scaffoldBackgroundColor: const Color(0xFF0B0712),
        useMaterial3: true,
      ),
      home: const SuperkateHomePage(),
    );
  }
}

class SuperkateHomePage extends StatefulWidget {
  const SuperkateHomePage({super.key, this.service});

  /// Injectable for tests; defaults to the local-first in-memory service.
  final PersistenceService? service;

  @override
  State<SuperkateHomePage> createState() => _SuperkateHomePageState();
}

class _SuperkateHomePageState extends State<SuperkateHomePage> {
  late final PersistenceService _service =
      widget.service ?? InMemoryPersistenceService();

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Superkate Services Calculator'),
        backgroundColor: Colors.transparent,
        foregroundColor: colors.onSurface,
      ),
      body: SafeArea(
        child: NewAppointmentForm(
          service: _service,
          onSaved: (appointment) {
            ScaffoldMessenger.of(context)
              ..clearSnackBars()
              ..showSnackBar(
                SnackBar(
                  content: Text(
                    'Saved ${appointment.clientNameSnapshot} — '
                    '${formatCents(appointment.appointmentTotalCents)}',
                  ),
                ),
              );
          },
        ),
      ),
    );
  }
}
