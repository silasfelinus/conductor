import 'package:flutter/material.dart';

import 'data/app_lock_service.dart';
import 'data/file_app_lock_service.dart';
import 'data/file_onboarding_service.dart';
import 'data/in_memory_persistence_service.dart';
import 'data/onboarding_service.dart';
import 'data/persistence_service.dart';
import 'data/sqlite_persistence_service.dart';
import 'domain/money.dart';
import 'ui/app_lock_screen.dart';
import 'ui/app_lock_settings.dart';
import 'ui/appointment_history.dart';
import 'ui/customer_profiles.dart';
import 'ui/new_appointment_form.dart';
import 'ui/receipt_email_launcher.dart';
import 'ui/superkate_onboarding.dart';
import 'ui/superkate_style.dart';

void main() => runApp(const SuperkateServicesCalculatorApp());

enum SuperkateBackgroundPattern {
  circles('Circles', 'Soft salon glow orbs'),
  hearts('Hearts', 'Queer-alt love notes'),
  grid('Grid', 'Clean calculator structure'),
  none('None', 'Plain gradient only');

  const SuperkateBackgroundPattern(this.label, this.description);

  final String label;
  final String description;
}

class SuperkateServicesCalculatorApp extends StatefulWidget {
  const SuperkateServicesCalculatorApp({
    super.key,
    this.service,
    this.onboardingService,
    this.appLockService,
  });

  final Future<PersistenceService>? service;
  final Future<OnboardingService>? onboardingService;
  final Future<AppLockService>? appLockService;

  @override
  State<SuperkateServicesCalculatorApp> createState() =>
      _SuperkateServicesCalculatorAppState();
}

class _SuperkateServicesCalculatorAppState
    extends State<SuperkateServicesCalculatorApp> {
  SuperkatePalette _selectedPalette = SuperkatePalettes.rainbowConnection;
  SuperkateBackgroundPattern _selectedBackground =
      SuperkateBackgroundPattern.circles;
  bool _isCompletingOnboarding = false;
  bool? _onboardingCompletedOverride;
  bool _unlockedThisSession = false;
  bool? _lockEnabledOverride;

  late final Future<_StartupBundle> _startup = _openStartup();

  Future<_StartupBundle> _openStartup() async {
    final service = await (widget.service ?? SqlitePersistenceService.open());
    final onboardingFuture =
        widget.onboardingService ?? FileOnboardingService.open();
    final onboardingService = await onboardingFuture;
    final onboardingCompleted =
        await onboardingService.hasCompletedOnboarding();
    final appLockService =
        await (widget.appLockService ?? FileAppLockService.open());
    final lockEnabled = await appLockService.isEnabled();

    return _StartupBundle(
      service: service,
      onboardingService: onboardingService,
      onboardingCompleted: onboardingCompleted,
      appLockService: appLockService,
      lockEnabled: lockEnabled,
    );
  }

  Future<void> _completeOnboarding(
    OnboardingService onboardingService,
    AppLockService appLockService, {
    String? pin,
  }) async {
    setState(() => _isCompletingOnboarding = true);
    try {
      if (pin != null) {
        await appLockService.enable(pin);
      }
      await onboardingService.completeOnboarding();
      if (!mounted) return;
      setState(() {
        _onboardingCompletedOverride = true;
        // She just set the PIN herself — don't lock her out immediately.
        _lockEnabledOverride = pin != null;
        _unlockedThisSession = true;
        _isCompletingOnboarding = false;
      });
    } catch (_) {
      if (mounted) setState(() => _isCompletingOnboarding = false);
      rethrow;
    }
  }

  @override
  Widget build(BuildContext context) {
    final palette = _selectedPalette;

    return SuperkateTheme(
      palette: palette,
      child: MaterialApp(
        title: 'Superkate Services Calculator',
        debugShowCheckedModeBanner: false,
        theme: _buildTheme(palette),
        home: FutureBuilder<_StartupBundle>(
          future: _startup,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              final startup = snapshot.requireData;
              final onboardingCompleted =
                  _onboardingCompletedOverride ?? startup.onboardingCompleted;

              if (!onboardingCompleted) {
                return SuperkateOnboardingScreen(
                  isWorking: _isCompletingOnboarding,
                  onStart: ({String? pin}) => _completeOnboarding(
                    startup.onboardingService,
                    startup.appLockService,
                    pin: pin,
                  ),
                );
              }

              final lockEnabled =
                  _lockEnabledOverride ?? startup.lockEnabled;
              if (lockEnabled && !_unlockedThisSession) {
                return SuperkateAppLockScreen(
                  lockService: startup.appLockService,
                  onUnlocked: () =>
                      setState(() => _unlockedThisSession = true),
                );
              }

              return SuperkateHomePage(
                service: startup.service,
                appLockService: startup.appLockService,
                onAppLockChanged: () async {
                  final enabled = await startup.appLockService.isEnabled();
                  if (mounted) {
                    setState(() => _lockEnabledOverride = enabled);
                  }
                },
                selectedPalette: palette,
                selectedBackground: _selectedBackground,
                onThemeChanged: (next) =>
                    setState(() => _selectedPalette = next),
                onBackgroundChanged: (next) =>
                    setState(() => _selectedBackground = next),
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

class _StartupBundle {
  const _StartupBundle({
    required this.service,
    required this.onboardingService,
    required this.onboardingCompleted,
    required this.appLockService,
    required this.lockEnabled,
  });

  final PersistenceService service;
  final OnboardingService onboardingService;
  final bool onboardingCompleted;
  final AppLockService appLockService;
  final bool lockEnabled;
}

class SuperkateHomePage extends StatefulWidget {
  const SuperkateHomePage({
    super.key,
    this.service,
    this.appLockService,
    this.onAppLockChanged,
    this.launchReceiptEmail,
    this.selectedPalette = SuperkatePalettes.rainbowConnection,
    this.selectedBackground = SuperkateBackgroundPattern.circles,
    this.onThemeChanged,
    this.onBackgroundChanged,
  });

  final PersistenceService? service;
  final AppLockService? appLockService;
  final VoidCallback? onAppLockChanged;
  final ReceiptEmailLauncher? launchReceiptEmail;
  final SuperkatePalette selectedPalette;
  final SuperkateBackgroundPattern selectedBackground;
  final ValueChanged<SuperkatePalette>? onThemeChanged;
  final ValueChanged<SuperkateBackgroundPattern>? onBackgroundChanged;

  @override
  State<SuperkateHomePage> createState() => _SuperkateHomePageState();
}

class _SuperkateHomePageState extends State<SuperkateHomePage> {
  late final PersistenceService _service =
      widget.service ?? InMemoryPersistenceService();
  int _historyRefreshToken = 0;

  void _refreshHistory() => setState(() => _historyRefreshToken++);

  void _openAppLockSettings() {
    final lockService = widget.appLockService;
    if (lockService == null) return;
    final palette = widget.selectedPalette;
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => SuperkateTheme(
        palette: palette,
        child: ClipRRect(
          borderRadius: const BorderRadius.vertical(top: Radius.circular(32)),
          child: Material(
            color: palette.ink,
            child: AppLockSettingsSheet(
              lockService: lockService,
              onChanged: widget.onAppLockChanged,
            ),
          ),
        ),
      ),
    );
  }

  void _openCustomerProfiles() {
    final palette = widget.selectedPalette;
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => FractionallySizedBox(
        heightFactor: 0.92,
        child: SuperkateTheme(
          palette: palette,
          child: ClipRRect(
            borderRadius: const BorderRadius.vertical(top: Radius.circular(32)),
            child: Material(
              color: palette.ink,
              child: CustomerProfiles(
                service: _service,
                onChanged: _refreshHistory,
              ),
            ),
          ),
        ),
      ),
    );
  }

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
              IconButton(
                tooltip: 'Manage customers',
                onPressed: _openCustomerProfiles,
                icon: const Icon(Icons.people_alt_outlined),
              ),
              if (widget.appLockService != null)
                IconButton(
                  key: const ValueKey('app-lock-settings-button'),
                  tooltip: 'App lock',
                  onPressed: _openAppLockSettings,
                  icon: const Icon(Icons.lock_outline),
                ),
              _BackgroundPickerButton(
                selectedBackground: widget.selectedBackground,
                onBackgroundChanged: widget.onBackgroundChanged,
              ),
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
                _BackgroundPatternLayer(
                  pattern: widget.selectedBackground,
                  palette: palette,
                ),
                SafeArea(
                  child: Padding(
                    padding: const EdgeInsets.only(top: 58),
                    child: TabBarView(
                      children: [
                        NewAppointmentForm(
                          service: _service,
                          onSaved: (appointment) {
                            _refreshHistory();
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
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 360),
              child: Card(
                color: selectedPalette.card,
                shape: SuperkateStyle.cardShape(
                  border: selectedPalette.cardBorder,
                ),
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const RainbowBadge(icon: Icons.content_cut),
                      const SizedBox(height: 18),
                      Text(
                        'Hair by Superkate',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: selectedPalette.soft,
                          fontSize: 28,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 10),
                      const RainbowRail(height: 5),
                      const SizedBox(height: 18),
                      CircularProgressIndicator(
                        color: selectedPalette.secondary,
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
                color: selectedPalette.card,
                shape: SuperkateStyle.cardShape(
                  border: selectedPalette.cardBorder,
                ),
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

class _BackgroundPickerButton extends StatelessWidget {
  const _BackgroundPickerButton({
    required this.selectedBackground,
    required this.onBackgroundChanged,
  });

  final SuperkateBackgroundPattern selectedBackground;
  final ValueChanged<SuperkateBackgroundPattern>? onBackgroundChanged;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return PopupMenuButton<SuperkateBackgroundPattern>(
      tooltip: 'Choose background',
      onSelected: onBackgroundChanged,
      icon: const Icon(Icons.wallpaper),
      itemBuilder: (context) => [
        for (final option in SuperkateBackgroundPattern.values)
          PopupMenuItem<SuperkateBackgroundPattern>(
            value: option,
            child: Row(
              children: [
                _BackgroundPatternSwatch(pattern: option),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        option.label,
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
                if (option == selectedBackground)
                  Icon(Icons.check, color: palette.secondary, size: 18),
              ],
            ),
          ),
      ],
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

class _BackgroundPatternSwatch extends StatelessWidget {
  const _BackgroundPatternSwatch({required this.pattern});

  final SuperkateBackgroundPattern pattern;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return Container(
      width: 36,
      height: 36,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: palette.plum,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: palette.cardBorder),
      ),
      child: Icon(
        switch (pattern) {
          SuperkateBackgroundPattern.circles => Icons.bubble_chart,
          SuperkateBackgroundPattern.hearts => Icons.favorite,
          SuperkateBackgroundPattern.grid => Icons.grid_4x4,
          SuperkateBackgroundPattern.none => Icons.block,
        },
        color: palette.secondary,
        size: 18,
      ),
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

class _BackgroundPatternLayer extends StatelessWidget {
  const _BackgroundPatternLayer({
    required this.pattern,
    required this.palette,
  });

  final SuperkateBackgroundPattern pattern;
  final SuperkatePalette palette;

  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      child: Stack(
        key: ValueKey('background-${pattern.name}'),
        children: switch (pattern) {
          SuperkateBackgroundPattern.circles => [
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
            ],
          SuperkateBackgroundPattern.hearts => [
              _FloatingMark(
                mark: '♥',
                top: 118,
                left: 28,
                size: 76,
                color: palette.primary.withAlpha(34),
              ),
              _FloatingMark(
                mark: '✦',
                top: 220,
                right: 42,
                size: 64,
                color: palette.secondary.withAlpha(38),
              ),
              _FloatingMark(
                mark: '♥',
                bottom: 108,
                right: 34,
                size: 92,
                color: palette.tertiary.withAlpha(31),
              ),
            ],
          SuperkateBackgroundPattern.grid => [
              Positioned.fill(
                child: CustomPaint(
                  painter: _GridPatternPainter(
                    lineColor: palette.secondary.withAlpha(24),
                    accentColor: palette.primary.withAlpha(18),
                  ),
                ),
              ),
            ],
          SuperkateBackgroundPattern.none => [const SizedBox.expand()],
        },
      ),
    );
  }
}

class _FloatingMark extends StatelessWidget {
  const _FloatingMark({
    required this.mark,
    required this.size,
    required this.color,
    this.top,
    this.right,
    this.bottom,
    this.left,
  });

  final String mark;
  final double size;
  final Color color;
  final double? top;
  final double? right;
  final double? bottom;
  final double? left;

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: top,
      right: right,
      bottom: bottom,
      left: left,
      child: Text(
        mark,
        style: TextStyle(
          color: color,
          fontSize: size,
          fontWeight: FontWeight.w900,
        ),
      ),
    );
  }
}

class _GridPatternPainter extends CustomPainter {
  const _GridPatternPainter({
    required this.lineColor,
    required this.accentColor,
  });

  final Color lineColor;
  final Color accentColor;

  @override
  void paint(Canvas canvas, Size size) {
    final linePaint = Paint()
      ..color = lineColor
      ..strokeWidth = 1;
    final accentPaint = Paint()
      ..color = accentColor
      ..strokeWidth = 1.4;

    for (var x = 0.0; x < size.width; x += 36) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), linePaint);
    }
    for (var y = 0.0; y < size.height; y += 36) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), linePaint);
    }
    for (var x = 18.0; x < size.width; x += 144) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), accentPaint);
    }
  }

  @override
  bool shouldRepaint(covariant _GridPatternPainter oldDelegate) {
    return oldDelegate.lineColor != lineColor ||
        oldDelegate.accentColor != accentColor;
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
