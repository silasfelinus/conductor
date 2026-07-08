import 'package:flutter/material.dart';

import 'data/in_memory_persistence_service.dart';
import 'data/persistence_service.dart';
import 'domain/money.dart';
import 'ui/appointment_history.dart';
import 'ui/new_appointment_form.dart';
import 'ui/receipt_email_launcher.dart';
import 'ui/superkate_style.dart';

void main() => runApp(const SuperkateServicesCalculatorApp());

class SuperkateServicesCalculatorApp extends StatelessWidget {
  const SuperkateServicesCalculatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Superkate Services Calculator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: SuperkateStyle.hotPink,
          brightness: Brightness.dark,
          primary: SuperkateStyle.hotPink,
          secondary: SuperkateStyle.teal,
          tertiary: SuperkateStyle.violet,
          surface: SuperkateStyle.cardStrong,
          error: const Color(0xFFFF8FA3),
        ),
        scaffoldBackgroundColor: SuperkateStyle.ink,
        useMaterial3: true,
        textTheme: ThemeData.dark().textTheme.apply(
              bodyColor: SuperkateStyle.soft,
              displayColor: SuperkateStyle.soft,
            ),
        appBarTheme: const AppBarTheme(
          centerTitle: false,
          elevation: 0,
          scrolledUnderElevation: 0,
          backgroundColor: Colors.transparent,
          foregroundColor: SuperkateStyle.soft,
          titleTextStyle: TextStyle(
            color: SuperkateStyle.soft,
            fontSize: 20,
            fontWeight: FontWeight.w900,
            letterSpacing: 0.2,
          ),
        ),
        tabBarTheme: const TabBarThemeData(
          dividerColor: Colors.transparent,
          indicatorColor: SuperkateStyle.teal,
          labelColor: SuperkateStyle.teal,
          unselectedLabelColor: SuperkateStyle.muted,
          labelStyle: TextStyle(fontWeight: FontWeight.w800),
        ),
        inputDecorationTheme: const InputDecorationTheme(
          filled: true,
          fillColor: Color(0xCC211633),
          labelStyle: TextStyle(color: SuperkateStyle.muted),
          hintStyle: TextStyle(color: SuperkateStyle.quiet),
          prefixIconColor: SuperkateStyle.teal,
          suffixIconColor: SuperkateStyle.hotPink,
          prefixStyle: TextStyle(color: SuperkateStyle.soft),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(22)),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(22)),
            borderSide: BorderSide(color: SuperkateStyle.cardBorder),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(22)),
            borderSide: BorderSide(color: SuperkateStyle.teal, width: 1.8),
          ),
        ),
        chipTheme: ChipThemeData(
          backgroundColor: SuperkateStyle.plum,
          selectedColor: SuperkateStyle.hotPink.withValues(alpha: 0.22),
          labelStyle: const TextStyle(
            color: SuperkateStyle.soft,
            fontWeight: FontWeight.w700,
          ),
          side: const BorderSide(color: SuperkateStyle.cardBorder),
          shape: const StadiumBorder(),
        ),
        snackBarTheme: const SnackBarThemeData(
          behavior: SnackBarBehavior.floating,
          backgroundColor: SuperkateStyle.plum,
          contentTextStyle: TextStyle(color: SuperkateStyle.soft),
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            minimumSize: const Size.fromHeight(56),
            foregroundColor: SuperkateStyle.ink,
            backgroundColor: SuperkateStyle.teal,
            textStyle: const TextStyle(
              fontWeight: FontWeight.w900,
              letterSpacing: 0.2,
            ),
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.all(Radius.circular(22)),
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
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          title: const Text('Superkate Services Calculator'),
          bottom: const PreferredSize(
            preferredSize: Size.fromHeight(56),
            child: Column(
              children: [
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: 16),
                  child: RainbowRail(height: 4),
                ),
                SizedBox(height: 8),
                TabBar(
                  indicatorWeight: 3,
                  tabs: [
                    Tab(text: 'New'),
                    Tab(text: 'History'),
                  ],
                ),
              ],
            ),
          ),
        ),
        body: Container(
          decoration: const BoxDecoration(gradient: SuperkateStyle.nightGradient),
          child: Stack(
            children: [
              const Positioned(
                top: -80,
                right: -70,
                child: _GlowOrb(
                  size: 210,
                  color: SuperkateStyle.hotPink,
                ),
              ),
              const Positioned(
                bottom: 80,
                left: -90,
                child: _GlowOrb(
                  size: 240,
                  color: SuperkateStyle.teal,
                ),
              ),
              SafeArea(
                child: Padding(
                  padding: const EdgeInsets.only(top: 58),
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
            ],
          ),
        ),
      ),
    );
  }
}

class _GlowOrb extends StatelessWidget {
  const _GlowOrb({required this.size, required this.color});

  final double size;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: color.withValues(alpha: 0.16),
          boxShadow: [
            BoxShadow(
              color: color.withValues(alpha: 0.34),
              blurRadius: 90,
              spreadRadius: 18,
            ),
          ],
        ),
      ),
    );
  }
}
