import 'package:flutter/material.dart';

import 'data/in_memory_persistence_service.dart';
import 'data/persistence_service.dart';
import 'data/sqlite_persistence_service.dart';
import 'domain/money.dart';
import 'ui/appointment_history.dart';
import 'ui/new_appointment_form.dart';
import 'ui/receipt_email_launcher.dart';
import 'ui/superkate_style.dart';

void main() => runApp(const SuperkateServicesCalculatorApp());

class SuperkateServicesCalculatorApp extends StatefulWidget {
  const SuperkateServicesCalculatorApp({super.key, this.service});

  final Future<PersistenceService>? service;

  @override
  State<SuperkateServicesCalculatorApp> createState() =>
      _SuperkateServicesCalculatorAppState();
}

class _SuperkateServicesCalculatorAppState
    extends State<SuperkateServicesCalculatorApp> {
  SuperkatePalette _selectedPalette = SuperkatePalettes.rainbowConnection;
  late final Future<PersistenceService> _service =
      widget.service ?? SqlitePersistenceService.open();

  @override
  Widget build(BuildContext context) {
    final palette = _selectedPalette;

    return SuperkateTheme(
      palette: palette,
      child: MaterialApp(
        title: 'Superkate Services Calculator',
        debugShowCheckedModeBanner: false,
        theme: _buildTheme(palette),
        home: FutureBuilder<PersistenceService>(
          future: _service,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return SuperkateHomePage(
                service: snapshot.requireData,
                selectedPalette: palette,
                onThemeChanged: (next) =>
                    setState(() => _selectedPalette = next),
              );
            }
            if (snapshot.hasError) {
              return _StartupErrorPage(selectedPalette: palette);
            }
            return _StartupLoadingPage(selectedPalette: palette);
          },
        ),
      ),
    );
  }

  ThemeData _buildTheme(SuperkatePalette palette) {
    return ThemeData(
      brightness: Brightness.dark,
      colorScheme: ColorScheme.fromSeed(
        seedColor: palette.primary,
        brightness: Brightness.dark,
        primary: palette.primary,
        secondary: palette.secondary,
        tertiary: palette.tertiary,
        surface: palette.cardStrong,
        error: palette.error,
      ),
      scaffoldBackgroundColor: palette.ink,
      useMaterial3: true,
      textTheme: ThemeData.dark().textTheme.apply(
            bodyColor: palette.soft,
            displayColor: palette.soft,
          ),
      appBarTheme: AppBarTheme(
        centerTitle: false,
        elevation: 0,
        scrolledUnderElevation: 0,
        backgroundColor: Colors.transparent,
        foregroundColor: palette.soft,
        titleTextStyle: TextStyle(
          color: palette.soft,
          fontSize: 20,
          fontWeight: FontWeight.w900,
          letterSpacing: 0.2,
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: palette.cardStrong,
        labelStyle: TextStyle(color: palette.muted),
        hintStyle: TextStyle(color: palette.quiet),
        prefixIconColor: palette.secondary,
        suffixIconColor: palette.primary,
        prefixStyle: TextStyle(color: palette.soft),
        border: const OutlineInputBorder(
          borderRadius: BorderRadius.all(Radius.circular(22)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: const BorderRadius.all(Radius.circular(22)),
          borderSide: BorderSide(color: palette.cardBorder),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: const BorderRadius.all(Radius.circular(22)),
          borderSide: BorderSide(color: palette.secondary, width: 1.8),
        ),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: palette.plum,
        selectedColor: palette.selectedChip,
        labelStyle: TextStyle(
          color: palette.soft,
          fontWeight: FontWeight.w700,
        ),
        side: BorderSide(color: palette.cardBorder),
        shape: const StadiumBorder(),
      ),
      snackBarTheme: SnackBarThemeData(
        behavior: SnackBarBehavior.floating,
        backgroundColor: palette.plum,
        contentTextStyle: TextStyle(color: palette.soft),
      ),
      popupMenuTheme: PopupMenuThemeData(
        color: palette.cardStrong,
        textStyle: TextStyle(color: palette.soft),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          minimumSize: const Size.fromHeight(56),
          foregroundColor: palette.ink,
          backgroundColor: palette.secondary,
          textStyle: const TextStyle(
            fontWeight: FontWeight.w900,
            letterSpacing: 0.2,
          ),
          shape: const RoundedRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(22)),
          ),
        ),
      ),
    );
  }
}

class SuperkateHomePage extends StatefulWidget {
  const SuperkateHomePage({
    super.key,
    this.service,
    this.launchReceiptEmail,
    this.selectedPalette = SuperkatePalettes.rainbowConnection,
    this.onThemeChanged,
  });

  final PersistenceService? service;
  final ReceiptEmailLauncher? launchReceiptEmail;
  final SuperkatePalette selectedPalette;
  final ValueChanged<SuperkatePalette>? onThemeChanged;

  @override
  State<SuperkateHomePage> createState() => _SuperkateHomePageState();
}

class _SuperkateHomePageState extends State<SuperkateHomePage> {
  late final PersistenceService _service =
      widget.service ?? InMemoryPersistenceService();
  int _historyRefreshToken = 0;

  @override
  Widget build(BuildContext context) {
    final palette = widget.selectedPalette;

    return SuperkateTheme(
      palette: palette,
      child: DefaultTabController(
        length: 2,
        child: Scaffold(
          extendBodyBehindAppBar: true,
          appBar: AppBar(
            title: const Text('Superkate Services Calculator'),
            actions: [
              _ThemePickerButton(
                selectedPalette: palette,
                onThemeChanged: widget.onThemeChanged,
              ),
            ],
            bottom: PreferredSize(
              preferredSize: const Size.fromHeight(56),
              child: Column(
                children: [
                  const Padding(
                    padding: EdgeInsets.symmetric(horizontal: 16),
                    child: RainbowRail(height: 4),
                  ),
                  const SizedBox(height: 8),
                  TabBar(
                    indicatorWeight: 3,
                    indicatorColor: palette.secondary,
                    labelColor: palette.secondary,
                    unselectedLabelColor: palette.muted,
                    labelStyle: const TextStyle(fontWeight: FontWeight.w800),
                    tabs: const [
                      Tab(text: 'New'),
                      Tab(text: 'History'),
                    ],
                  ),
                ],
              ),
            ),
          ),
          body: Container(
            decoration: BoxDecoration(gradient: palette.nightGradient),
            child: Stack(
              children: [
                Positioned(
                  top: -80,
                  right: -70,
                  child: _GlowOrb(
                    size: 210,
                    fillColor: palette.orbFillPrimary,
                    shadowColor: palette.orbShadowPrimary,
                  ),
                ),
                Positioned(
                  bottom: 80,
                  left: -90,
                  child: _GlowOrb(
                    size: 240,
                    fillColor: palette.orbFillSecondary,
                    shadowColor: palette.orbShadowSecondary,
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
      ),
    );
  }
}

class _StartupLoadingPage extends StatelessWidget {
  const _StartupLoadingPage({required this.selectedPalette});

  final SuperkatePalette selectedPalette;

  @override
  Widget build(BuildContext context) {
    return SuperkateTheme(
      palette: selectedPalette,
      child: Scaffold(
        body: Container(
          decoration: BoxDecoration(gradient: selectedPalette.nightGradient),
          child: const Center(
            child: CircularProgressIndicator(),
          ),
        ),
      ),
    );
  }
}

class _StartupErrorPage extends StatelessWidget {
  const _StartupErrorPage({required this.selectedPalette});

  final SuperkatePalette selectedPalette;

  @override
  Widget build(BuildContext context) {
    return SuperkateTheme(
      palette: selectedPalette,
      child: Scaffold(
        body: Container(
          decoration: BoxDecoration(gradient: selectedPalette.nightGradient),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 520),
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        Icons.lock_clock,
                        color: selectedPalette.secondary,
                        size: 40,
                      ),
                      const SizedBox(height: 16),
                      const Text(
                        'Superkate needs a second',
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'The local appointment database could not open. Restart the app and try again.',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: selectedPalette.muted),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _ThemePickerButton extends StatelessWidget {
  const _ThemePickerButton({
    required this.selectedPalette,
    required this.onThemeChanged,
  });

  final SuperkatePalette selectedPalette;
  final ValueChanged<SuperkatePalette>? onThemeChanged;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return PopupMenuButton<SuperkatePalette>(
      tooltip: 'Choose theme',
      onSelected: onThemeChanged,
      icon: const Icon(Icons.auto_awesome),
      itemBuilder: (context) => [
        for (final option in SuperkatePalettes.all)
          PopupMenuItem<SuperkatePalette>(
            value: option,
            child: Row(
              children: [
                _ThemeSwatch(palette: option),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        option.name,
                        style: TextStyle(
                          color: palette.soft,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        option.description,
                        style: TextStyle(color: palette.muted, fontSize: 12),
                      ),
                    ],
                  ),
                ),
                if (option == selectedPalette)
                  Icon(Icons.check, color: palette.secondary, size: 18),
              ],
            ),
          ),
      ],
    );
  }
}

class _ThemeSwatch extends StatelessWidget {
  const _ThemeSwatch({required this.palette});

  final SuperkatePalette palette;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: palette.spectrumGradient,
        border: Border.all(color: palette.cardBorder),
      ),
    );
  }
}

class _GlowOrb extends StatelessWidget {
  const _GlowOrb({
    required this.size,
    required this.fillColor,
    required this.shadowColor,
  });

  final double size;
  final Color fillColor;
  final Color shadowColor;

  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: fillColor,
          boxShadow: [
            BoxShadow(
              color: shadowColor,
              blurRadius: 90,
              spreadRadius: 18,
            ),
          ],
        ),
      ),
    );
  }
}
