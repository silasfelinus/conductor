import 'package:flutter/material.dart';

import '../data/app_lock_service.dart';
import 'superkate_style.dart';

/// Settings sheet for the optional app lock. Turning the lock on takes a new
/// 4-8 digit PIN; turning it off or changing the PIN requires the current one.
class AppLockSettingsSheet extends StatefulWidget {
  const AppLockSettingsSheet({
    super.key,
    required this.lockService,
    this.onChanged,
  });

  final AppLockService lockService;
  final VoidCallback? onChanged;

  @override
  State<AppLockSettingsSheet> createState() => _AppLockSettingsSheetState();
}

class _AppLockSettingsSheetState extends State<AppLockSettingsSheet> {
  final TextEditingController _currentPin = TextEditingController();
  final TextEditingController _newPin = TextEditingController();
  final TextEditingController _repeatPin = TextEditingController();

  bool? _enabled;
  String? _message;
  bool _messageIsError = false;

  @override
  void initState() {
    super.initState();
    _loadEnabled();
  }

  @override
  void dispose() {
    _currentPin.dispose();
    _newPin.dispose();
    _repeatPin.dispose();
    super.dispose();
  }

  Future<void> _loadEnabled() async {
    final enabled = await widget.lockService.isEnabled();
    if (mounted) setState(() => _enabled = enabled);
  }

  void _showMessage(String message, {bool isError = false}) {
    setState(() {
      _message = message;
      _messageIsError = isError;
    });
  }

  String? _validateNewPin() {
    if (!isValidAppLockPin(_newPin.text.trim())) {
      return 'PINs are 4-8 digits.';
    }
    if (_newPin.text.trim() != _repeatPin.text.trim()) {
      return "Those PINs don't match each other.";
    }
    return null;
  }

  Future<void> _turnOn() async {
    final problem = _validateNewPin();
    if (problem != null) {
      _showMessage(problem, isError: true);
      return;
    }
    await widget.lockService.enable(_newPin.text.trim());
    widget.onChanged?.call();
    if (!mounted) return;
    setState(() {
      _enabled = true;
      _newPin.clear();
      _repeatPin.clear();
    });
    _showMessage('App lock is on. Your client book opens with your PIN.');
  }

  Future<void> _turnOff() async {
    if (!await widget.lockService.verifyPin(_currentPin.text.trim())) {
      _showMessage("That PIN doesn't match — the lock stays on.",
          isError: true);
      return;
    }
    await widget.lockService.disable();
    widget.onChanged?.call();
    if (!mounted) return;
    setState(() {
      _enabled = false;
      _currentPin.clear();
    });
    _showMessage('App lock is off. Anyone with this device can open the app.');
  }

  Future<void> _changePin() async {
    if (!await widget.lockService.verifyPin(_currentPin.text.trim())) {
      _showMessage("That current PIN doesn't match.", isError: true);
      return;
    }
    final problem = _validateNewPin();
    if (problem != null) {
      _showMessage(problem, isError: true);
      return;
    }
    await widget.lockService.enable(_newPin.text.trim());
    widget.onChanged?.call();
    if (!mounted) return;
    setState(() {
      _currentPin.clear();
      _newPin.clear();
      _repeatPin.clear();
    });
    _showMessage('PIN updated. Same lock, fresh combination.');
  }

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);
    final enabled = _enabled;

    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                const RainbowBadge(icon: Icons.lock_outline),
                const SizedBox(width: 14),
                Expanded(
                  child: Text(
                    'App lock',
                    style: TextStyle(
                      color: palette.soft,
                      fontSize: 24,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              'An optional PIN that keeps saved clients, appointment history, '
              'and receipt details just for you. It protects this app on this '
              'device — nothing is sent anywhere.',
              style: TextStyle(color: palette.muted, fontSize: 14, height: 1.4),
            ),
            const SizedBox(height: 18),
            if (enabled == null)
              const Center(child: CircularProgressIndicator())
            else if (!enabled) ...[
              TextField(
                key: const ValueKey('app-lock-new-pin'),
                controller: _newPin,
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 8,
                decoration: const InputDecoration(
                  labelText: 'Choose a PIN (4-8 digits)',
                  counterText: '',
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                key: const ValueKey('app-lock-repeat-pin'),
                controller: _repeatPin,
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 8,
                decoration: const InputDecoration(
                  labelText: 'Repeat the PIN',
                  counterText: '',
                ),
              ),
              const SizedBox(height: 16),
              FilledButton.icon(
                key: const ValueKey('app-lock-turn-on-button'),
                onPressed: _turnOn,
                icon: const Icon(Icons.lock),
                label: const Text('Turn on app lock'),
              ),
            ] else ...[
              TextField(
                key: const ValueKey('app-lock-current-pin'),
                controller: _currentPin,
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 8,
                decoration: const InputDecoration(
                  labelText: 'Current PIN',
                  counterText: '',
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                key: const ValueKey('app-lock-new-pin'),
                controller: _newPin,
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 8,
                decoration: const InputDecoration(
                  labelText: 'New PIN (only to change it)',
                  counterText: '',
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                key: const ValueKey('app-lock-repeat-pin'),
                controller: _repeatPin,
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 8,
                decoration: const InputDecoration(
                  labelText: 'Repeat the new PIN',
                  counterText: '',
                ),
              ),
              const SizedBox(height: 16),
              FilledButton.icon(
                key: const ValueKey('app-lock-change-pin-button'),
                onPressed: _changePin,
                icon: const Icon(Icons.password),
                label: const Text('Change PIN'),
              ),
              const SizedBox(height: 10),
              OutlinedButton.icon(
                key: const ValueKey('app-lock-turn-off-button'),
                onPressed: _turnOff,
                icon: const Icon(Icons.lock_open),
                label: const Text('Turn off app lock'),
              ),
            ],
            if (_message != null) ...[
              const SizedBox(height: 14),
              Text(
                _message!,
                key: const ValueKey('app-lock-message'),
                style: TextStyle(
                  color: _messageIsError ? palette.error : palette.secondary,
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
            const SizedBox(height: 6),
            Text(
              'New lock settings take effect the next time the app opens.',
              style: TextStyle(
                color: palette.quiet,
                fontSize: 12,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
