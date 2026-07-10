import 'package:flutter/material.dart';

import '../data/app_lock_service.dart';
import 'superkate_style.dart';

/// Shown at startup when the app lock is on. The client book stays closed
/// until the saved PIN is entered.
class SuperkateAppLockScreen extends StatefulWidget {
  const SuperkateAppLockScreen({
    super.key,
    required this.lockService,
    required this.onUnlocked,
  });

  final AppLockService lockService;
  final VoidCallback onUnlocked;

  @override
  State<SuperkateAppLockScreen> createState() => _SuperkateAppLockScreenState();
}

class _SuperkateAppLockScreenState extends State<SuperkateAppLockScreen> {
  final TextEditingController _pinController = TextEditingController();
  String? _error;
  bool _checking = false;

  @override
  void dispose() {
    _pinController.dispose();
    super.dispose();
  }

  Future<void> _tryUnlock() async {
    setState(() {
      _checking = true;
      _error = null;
    });
    final ok = await widget.lockService.verifyPin(_pinController.text.trim());
    if (!mounted) return;
    if (ok) {
      widget.onUnlocked();
      return;
    }
    setState(() {
      _checking = false;
      _error = "That PIN doesn't match — take a breath and try again.";
    });
  }

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(gradient: palette.nightGradient),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 460),
                child: Card(
                  color: palette.card,
                  shape: SuperkateStyle.cardShape(border: palette.cardBorder),
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        const Align(
                          alignment: Alignment.centerLeft,
                          child: RainbowBadge(icon: Icons.lock_outline),
                        ),
                        const SizedBox(height: 18),
                        Text(
                          'Welcome back',
                          style: TextStyle(
                            color: palette.soft,
                            fontSize: 28,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Your client book is locked. Enter your PIN to open your chair.',
                          style: TextStyle(
                            color: palette.muted,
                            fontSize: 15,
                            height: 1.35,
                          ),
                        ),
                        const SizedBox(height: 20),
                        TextField(
                          key: const ValueKey('app-lock-pin-field'),
                          controller: _pinController,
                          keyboardType: TextInputType.number,
                          obscureText: true,
                          maxLength: 8,
                          onSubmitted: (_) => _tryUnlock(),
                          decoration: InputDecoration(
                            labelText: 'PIN',
                            counterText: '',
                            errorText: _error,
                          ),
                        ),
                        const SizedBox(height: 16),
                        FilledButton.icon(
                          key: const ValueKey('app-lock-unlock-button'),
                          onPressed: _checking ? null : _tryUnlock,
                          icon: _checking
                              ? const SizedBox.square(
                                  dimension: 18,
                                  child:
                                      CircularProgressIndicator(strokeWidth: 2),
                                )
                              : const Icon(Icons.lock_open),
                          label: Text(_checking ? 'Checking...' : 'Unlock'),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          'The PIN never leaves this device.',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: palette.quiet,
                            fontSize: 12,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ],
                    ),
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
