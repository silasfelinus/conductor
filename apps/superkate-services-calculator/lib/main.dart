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
    const background = Color(0xFF0B0712);
    const mutedText = Color(0xFFCAC2DF);

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
        scaffoldBackgroundColor: background,
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: false,
          elevation: 0,
          scrolledUnderElevation: 0,
          backgroundColor: Colors.transparent,
          foregroundColor: Color(0xFFF7F1FF),
          titleTextStyle: TextStyle(
            color: Color(0xFFF7F1FF),
            fontSize: 20,
            fontWeight: FontWeight.w800,
            letterSpacing: 0.2,
          ),
        ),
        inputDecorationTheme: const InputDecorationTheme(
          filled: true,
          fillColor: Color(0xFF1E1830),
          labelStyle: TextStyle(color: mutedText),
          hintStyle: TextStyle(color: Color(0xFF9C92B8)),
          prefixIconColor: mutedText,
          suffixIconColor: mutedText,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(18)),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(18)),
            borderSide: BorderSide(color: Color(0xFF3B2A5B)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(18)),
            borderSide: BorderSide(color: teal, width: 1.6),
          ),
        ),
        snackBarTheme: const SnackBarThemeData(
          behavior: SnackBarBehavior.floating,
          backgroundColor: Color(0xFF24183A),
          contentTextStyle: TextStyle(color: Color(0xFFF7F1FF)),
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.all(Radius.circular(18)),
            ),
          ),
        ),
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
          bottom: TabBar(
            indicatorColor: colors.secondary,
            indicatorWeight: 3,
            labelColor: colors.secondary,
            unselectedLabelColor: const Color(0xFFBDB2D6),
            tabs: const [
              Tab(text: 'New'),
              Tab(text: 'History'),
            ],
          ),
        ),
        body: Container(
          decoration: const BoxDecoration(
            gradient: RadialGradient(
              center: Alignment.topLeft,
              radius: 1.25,
              colors: [
                Color(0xFF24123E),
                Color(0xFF120A20),
                Color(0xFF0B0712),
              ],
              stops: [0, 0.48, 1],
            ),
          ),
          child: SafeArea(
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
      ),
    );
  }
}
