import 'package:flutter/material.dart';

import 'data/in_memory_persistence_service.dart';
import 'data/persistence_service.dart';
import 'domain/money.dart';
import 'ui/appointment_history.dart';
import 'ui/new_appointment_form.dart';
import 'ui/receipt_email_launcher.dart';

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
  const SuperkateHomePage({
    super.key,
    this.service,
    this.launchReceiptEmail,
  });

  /// Injectable for tests; defaults to the local-first in-memory service.
  final PersistenceService? service;
  final ReceiptEmailLauncher? launchReceiptEmail;

  @override
  State<SuperkateHomePage> createState() => _SuperkateHomePageState();
}

class _SuperkateHomePageState extends State<SuperkateHomePage> {
  late final PersistenceService _service =
      widget.service ?? InMemoryPersistenceService();
  int _historyRefreshToken = 0;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;

    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Superkate Services Calculator'),
          backgroundColor: Colors.transparent,
          foregroundColor: colors.onSurface,
          bottom: const TabBar(
            tabs: [
              Tab(text: 'New'),
              Tab(text: 'History'),
            ],
          ),
        ),
        body: SafeArea(
          child: TabBarView(
            children: [
              NewAppointmentForm(
                service: _service,
                onSaved: (appointment) {
                  setState(() => _historyRefreshToken++);
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
              AppointmentHistory(
                service: _service,
                refreshToken: _historyRefreshToken,
                launchReceiptEmail: widget.launchReceiptEmail,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
