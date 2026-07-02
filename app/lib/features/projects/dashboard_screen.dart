import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../agent_ops/agent_ops_repository.dart';
import 'project_models.dart';
import 'projects_repository.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final projects = ref.watch(projectsProvider);
    final ops = ref.watch(agentOpsDataProvider).valueOrNull;
    final approvalsCount = ops?.approvals.length ?? 0;

    return Scaffold(
      appBar: AppBar(title: const Text('Projects')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _createProject(context, ref),
        icon: const Icon(Icons.add),
        label: const Text('New project'),
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(projectsProvider);
          ref.invalidate(agentOpsDataProvider);
        },
        child: projects.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e, _) => _ErrorRetry(
              message: '$e', onRetry: () => ref.invalidate(projectsProvider)),
          data: (items) => ListView(
            padding: const EdgeInsets.all(16),
            children: [
              if (approvalsCount > 0)
                Card(
                  color: Theme.of(context).colorScheme.tertiaryContainer,
                  child: ListTile(
                    leading: const Icon(Icons.notifications_active),
                    title: Text('$approvalsCount task(s) need your decision'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => context.go('/approvals'),
                  ),
                ),
              if (items.isEmpty)
                const Padding(
                  padding: EdgeInsets.only(top: 64),
                  child: Center(
                      child: Text(
                          'No projects yet.\nCreate one to get started.',
                          textAlign: TextAlign.center)),
                ),
              for (final project in items) _ProjectCard(project: project),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _createProject(BuildContext context, WidgetRef ref) async {
    final controller = TextEditingController();
    final title = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('New project'),
        content: TextField(
          controller: controller,
          autofocus: true,
          decoration: const InputDecoration(labelText: 'Project title'),
          onSubmitted: (v) => Navigator.of(ctx).pop(v),
        ),
        actions: [
          TextButton(
              onPressed: () => Navigator.of(ctx).pop(),
              child: const Text('Cancel')),
          FilledButton(
              onPressed: () => Navigator.of(ctx).pop(controller.text),
              child: const Text('Create')),
        ],
      ),
    );
    if (title == null || title.trim().isEmpty) return;
    final repo = ref.read(projectsRepositoryProvider);
    if (repo == null) return;
    await repo.create(title: title.trim());
    ref.invalidate(projectsProvider);
  }
}

class _ProjectCard extends ConsumerWidget {
  const _ProjectCard({required this.project});

  final Project project;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final done =
        project.waypoints.where((w) => w.status == WaypointStatus.done).length;
    final total = project.waypoints.length;
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        title: Row(
          children: [
            Expanded(
                child: Text(project.title,
                    style: Theme.of(context).textTheme.titleMedium)),
            _StatusChip(status: project.projectStatus),
          ],
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (project.description?.isNotEmpty == true)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(project.description!,
                    maxLines: 2, overflow: TextOverflow.ellipsis),
              ),
            if (total > 0)
              Padding(
                padding: const EdgeInsets.only(top: 12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    LinearProgressIndicator(value: done / total),
                    const SizedBox(height: 4),
                    Text('$done of $total waypoints'),
                  ],
                ),
              ),
          ],
        ),
        onTap: () => context.go('/projects/${project.id}'),
      ),
    );
  }
}

class _StatusChip extends StatelessWidget {
  const _StatusChip({required this.status});

  final String status;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final color = switch (status) {
      'ACTIVE' => scheme.primaryContainer,
      'PAUSED' => scheme.surfaceContainerHighest,
      'BRAINSTORM' => scheme.tertiaryContainer,
      'DONE' => scheme.secondaryContainer,
      _ => scheme.surfaceContainerHighest,
    };
    return Chip(
      label: Text(status, style: const TextStyle(fontSize: 11)),
      backgroundColor: color,
      visualDensity: VisualDensity.compact,
    );
  }
}

class _ErrorRetry extends StatelessWidget {
  const _ErrorRetry({required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 12),
            FilledButton(onPressed: onRetry, child: const Text('Retry')),
          ],
        ),
      ),
    );
  }
}
