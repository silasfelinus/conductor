import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/config/server_config.dart';
import '../auth/auth_controller.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final config = ref.watch(serverConfigProvider);
    final user = ref.watch(currentUserProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: [
          if (user != null)
            ListTile(
              leading: const CircleAvatar(child: Icon(Icons.person)),
              title: Text(user.username),
              subtitle: Text([
                user.email,
                if (user.isAdmin) 'Admin',
                'karma ${user.karma} · mana ${user.mana}',
              ].whereType<String>().join(' · ')),
            ),
          ListTile(
            leading: const Icon(Icons.dns),
            title: const Text('Server'),
            subtitle: Text(switch (config?.mode) {
              ServerMode.hosted =>
                'Kind Robots Cloud (${ServerConfig.hostedUrl})',
              ServerMode.selfHosted => config!.baseUrl,
              ServerMode.local => 'This device only — no server',
              null => 'Not configured',
            }),
          ),
          const Divider(),
          if (user != null)
            ListTile(
              leading: const Icon(Icons.logout),
              title: const Text('Sign out'),
              onTap: () => ref.read(authControllerProvider.notifier).logout(),
            ),
          if (user != null)
            ListTile(
              leading: Icon(Icons.delete_forever,
                  color: Theme.of(context).colorScheme.error),
              title: Text('Delete account',
                  style: TextStyle(color: Theme.of(context).colorScheme.error)),
              subtitle: const Text(
                  'Permanently removes your account and everything you own. Cannot be undone.'),
              onTap: () => _confirmDeleteAccount(context, ref),
            ),
          ListTile(
            leading: const Icon(Icons.swap_horiz),
            title: const Text('Switch server mode'),
            subtitle: const Text(
                'Local data stays on this device; server data stays on the server.'),
            onTap: () async {
              final confirmed = await showDialog<bool>(
                context: context,
                builder: (ctx) => AlertDialog(
                  title: const Text('Switch server mode?'),
                  content: const Text(
                      'You will return to the welcome screen. Nothing is deleted.'),
                  actions: [
                    TextButton(
                        onPressed: () => Navigator.of(ctx).pop(false),
                        child: const Text('Cancel')),
                    FilledButton(
                        onPressed: () => Navigator.of(ctx).pop(true),
                        child: const Text('Switch')),
                  ],
                ),
              );
              if (confirmed == true) {
                await ref.read(serverConfigProvider.notifier).reset();
              }
            },
          ),
          const Divider(),
          const AboutListTile(
            icon: Icon(Icons.info_outline),
            applicationName: 'Conductor',
            applicationVersion: '0.1.0',
            aboutBoxChildren: [
              Text('Deluxe task manager for humans and their AI agents.'),
            ],
          ),
        ],
      ),
    );
  }

  Future<void> _confirmDeleteAccount(
      BuildContext context, WidgetRef ref) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Delete account?'),
        content: const Text(
            'This permanently deletes your account, projects, dreams, characters, '
            'chats, and everything else tied to it on the server. This cannot be undone.'),
        actions: [
          TextButton(
              onPressed: () => Navigator.of(ctx).pop(false),
              child: const Text('Cancel')),
          FilledButton(
            onPressed: () => Navigator.of(ctx).pop(true),
            style: FilledButton.styleFrom(
                backgroundColor: Theme.of(ctx).colorScheme.error),
            child: const Text('Delete permanently'),
          ),
        ],
      ),
    );
    if (confirmed != true) return;
    try {
      await ref.read(authControllerProvider.notifier).deleteAccount();
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Could not delete account: $e')),
      );
    }
  }
}
