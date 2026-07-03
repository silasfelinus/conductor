import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/config/server_config.dart';
import '../auth/auth_controller.dart';

class ServerPickerScreen extends ConsumerStatefulWidget {
  const ServerPickerScreen({super.key});

  @override
  ConsumerState<ServerPickerScreen> createState() => _ServerPickerScreenState();
}

class _ServerPickerScreenState extends ConsumerState<ServerPickerScreen> {
  final _urlController = TextEditingController();
  bool _showCustomUrl = false;

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  Future<void> _select(ServerConfig config) =>
      ref.read(serverConfigProvider.notifier).select(config);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            const SizedBox(height: 32),
            Icon(Icons.hub, size: 64, color: theme.colorScheme.primary),
            const SizedBox(height: 16),
            Text('Conductor',
                textAlign: TextAlign.center,
                style: theme.textTheme.headlineMedium),
            Text('Projects for humans and their AI agents',
                textAlign: TextAlign.center, style: theme.textTheme.bodyMedium),
            const SizedBox(height: 32),
            _ModeCard(
              icon: Icons.cloud,
              title: 'Kind Robots Cloud',
              subtitle:
                  'Sync across devices with a free kindrobots.org account.',
              onTap: () =>
                  _select(const ServerConfig(mode: ServerMode.hosted)),
            ),
            _ModeCard(
              icon: Icons.dns,
              title: 'Your own server',
              subtitle: 'Connect to a kind_robots instance you host.',
              onTap: () => setState(() => _showCustomUrl = !_showCustomUrl),
            ),
            if (_showCustomUrl)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Column(
                  children: [
                    TextField(
                      controller: _urlController,
                      keyboardType: TextInputType.url,
                      decoration: const InputDecoration(
                        labelText: 'Server URL',
                        hintText: 'https://kr.example.com',
                      ),
                    ),
                    const SizedBox(height: 8),
                    FilledButton(
                      onPressed: () {
                        final url = _urlController.text
                            .trim()
                            .replaceAll(RegExp(r'/+$'), '');
                        if (Uri.tryParse(url)?.hasScheme != true) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                                content: Text(
                                    'Enter a full URL, e.g. https://kr.example.com')),
                          );
                          return;
                        }
                        _select(ServerConfig(
                            mode: ServerMode.selfHosted, baseUrl: url));
                      },
                      child: const Text('Connect'),
                    ),
                  ],
                ),
              ),
            _ModeCard(
              icon: Icons.phone_iphone,
              title: 'Just this device',
              subtitle:
                  'No account, no server. Everything stays on this device.',
              onTap: () => _select(const ServerConfig(mode: ServerMode.local)),
            ),
          ],
        ),
      ),
    );
  }
}

class _ModeCard extends StatelessWidget {
  const _ModeCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: Icon(icon, size: 36),
        title: Text(title),
        subtitle: Text(subtitle),
        onTap: onTap,
      ),
    );
  }
}
