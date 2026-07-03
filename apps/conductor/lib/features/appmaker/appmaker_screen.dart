import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../agent_ops/agent_ops_repository.dart';
import 'appmaker_repository.dart';

class AppmakerScreen extends ConsumerWidget {
  const AppmakerScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final inventory = ref.watch(appsInventoryProvider);
    final opsProjects =
        ref.watch(agentOpsDataProvider).valueOrNull?.projects ?? const [];

    return Scaffold(
      appBar: AppBar(title: const Text('AppMaker')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _createApp(context, ref),
        icon: const Icon(Icons.add),
        label: const Text('New app'),
      ),
      body: RefreshIndicator(
        onRefresh: () async => ref.invalidate(appsInventoryProvider),
        child: inventory.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Text('$e', textAlign: TextAlign.center),
            ),
          ),
          data: (data) {
            if (data == null) {
              return const Center(
                  child: Text('AppMaker needs a server connection.'));
            }
            return ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (data.pending.isNotEmpty) ...[
                  Text('Being built',
                      style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      for (final item in data.pending)
                        Chip(
                          avatar: const SizedBox(
                            width: 14,
                            height: 14,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          ),
                          label: Text(item.slug),
                        ),
                    ],
                  ),
                  const SizedBox(height: 16),
                ],
                Text('Apps (${data.scaffolded.length})',
                    style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 8),
                if (data.scaffolded.isEmpty)
                  const Padding(
                    padding: EdgeInsets.symmetric(vertical: 24),
                    child: Center(
                        child:
                            Text('No apps yet — create the first one below.')),
                  ),
                for (final slug in data.scaffolded)
                  _AppCard(
                    slug: slug,
                    project: opsProjects
                        .where((p) => p.slug == slug)
                        .firstOrNull,
                  ),
                const SizedBox(height: 72),
              ],
            );
          },
        ),
      ),
    );
  }

  Future<void> _createApp(BuildContext context, WidgetRef ref) async {
    final repo = ref.read(appmakerRepositoryProvider);
    if (repo == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text('Connect to a server to create apps.')));
      return;
    }
    final result = await showModalBottomSheet<Map<String, String>>(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => const _NewAppSheet(),
    );
    if (result == null) return;
    try {
      final slug = await repo.requestScaffold(
        title: result['title']!,
        slug: result['slug'],
        description: result['description'],
      );
      ref.invalidate(appsInventoryProvider);
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text(
                "Request filed — '$slug' will be scaffolded on the next agent cycle.")));
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text('$e')));
      }
    }
  }
}

class _AppCard extends StatelessWidget {
  const _AppCard({required this.slug, this.project});

  final String slug;
  final RoadmapProject? project;

  @override
  Widget build(BuildContext context) {
    final tasks = project?.tasks ?? const [];
    final done = tasks.where((t) => t.status == 'done').length;
    final needsHuman = tasks.where((t) => t.status == 'needs-human').length;
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: const Icon(Icons.apps, size: 32),
        title: Text(project?.title ?? _titleize(slug)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(slug, style: Theme.of(context).textTheme.bodySmall),
            if (tasks.isNotEmpty) ...[
              const SizedBox(height: 8),
              LinearProgressIndicator(
                  value: tasks.isEmpty ? 0 : done / tasks.length),
              const SizedBox(height: 4),
              Text([
                '$done of ${tasks.length} tasks done',
                if (needsHuman > 0) '$needsHuman need you',
              ].join(' · ')),
            ],
          ],
        ),
      ),
    );
  }

  String _titleize(String slug) => slug
      .split('-')
      .map((part) =>
          part.isEmpty ? part : part[0].toUpperCase() + part.substring(1))
      .join(' ');
}

class _NewAppSheet extends StatefulWidget {
  const _NewAppSheet();

  @override
  State<_NewAppSheet> createState() => _NewAppSheetState();
}

class _NewAppSheetState extends State<_NewAppSheet> {
  final _title = TextEditingController();
  final _slug = TextEditingController();
  final _description = TextEditingController();

  @override
  void dispose() {
    _title.dispose();
    _slug.dispose();
    _description.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 16,
        right: 16,
        top: 16,
        bottom: MediaQuery.of(context).viewInsets.bottom + 16,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text('New app', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 4),
          Text(
            'Files a scaffold request: the agents create the workspace, '
            'roadmap, and art prompts on the next cycle.',
            style: Theme.of(context).textTheme.bodySmall,
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _title,
            autofocus: true,
            decoration: const InputDecoration(labelText: 'Name'),
            onChanged: (_) => setState(() {}),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _slug,
            decoration: InputDecoration(
              labelText: 'Slug',
              hintText: slugify(_title.text).isEmpty
                  ? 'my-app'
                  : slugify(_title.text),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _description,
            decoration: const InputDecoration(
                labelText: 'What is it? (one line, steers its art)'),
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () {
              if (_title.text.trim().isEmpty) return;
              Navigator.of(context).pop({
                'title': _title.text.trim(),
                'slug': _slug.text.trim(),
                'description': _description.text.trim(),
              });
            },
            child: const Text('Create app'),
          ),
        ],
      ),
    );
  }
}
