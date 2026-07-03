import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../auth/auth_controller.dart';
import '../todos/todos_repository.dart';
import 'project_models.dart';
import 'projects_repository.dart';
import 'widgets/intent_editor_sheet.dart';
import 'widgets/wishlist_section.dart';

class ProjectDetailScreen extends ConsumerWidget {
  const ProjectDetailScreen({super.key, required this.projectId});

  final int projectId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final projects = ref.watch(projectsProvider).valueOrNull ?? [];
    final project = projects.where((p) => p.id == projectId).firstOrNull;
    if (project == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    final todos = (ref.watch(todosControllerProvider).valueOrNull ?? [])
        .where((t) => t.dreamId == project.id && t.category != 'DESIRED_FEATURE')
        .toList();

    return Scaffold(
      appBar: AppBar(
        title: Text(project.title),
        actions: [
          if (ref.watch(serverConfigProvider)?.isLocal == false)
            IconButton(
              icon: const Icon(Icons.chat_bubble_outline),
              tooltip: 'Project assistant',
              onPressed: () => context.go('/projects/${project.id}/chat'),
            ),
          IconButton(
            icon: const Icon(Icons.edit),
            tooltip: 'Edit details',
            onPressed: () async {
              final patch = await IntentEditorSheet.show(context, project);
              if (patch != null && patch.isNotEmpty) {
                await _patch(ref, project, patch);
              }
            },
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _addTask(context, ref, project),
        child: const Icon(Icons.add_task),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (ref
                  .watch(serverConfigProvider)
                  ?.resolveAssetUrl(project.heroPath ?? project.imagePath)
              case final heroUrl?)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: AspectRatio(
                  aspectRatio: 16 / 9,
                  child: CachedNetworkImage(
                    imageUrl: heroUrl,
                    fit: BoxFit.cover,
                    errorWidget: (context, url, error) =>
                        const SizedBox.shrink(),
                  ),
                ),
              ),
            ),
          if (project.goal?.isNotEmpty == true) ...[
            Text('Goal', style: Theme.of(context).textTheme.titleSmall),
            Text(project.goal!),
            const SizedBox(height: 16),
          ],
          if (project.description?.isNotEmpty == true) ...[
            Text(project.description!),
            const SizedBox(height: 16),
          ],
          Row(
            children: [
              Expanded(
                child: _EnumPicker(
                  label: 'Status',
                  value: project.projectStatus,
                  options: const [
                    'ACTIVE',
                    'PAUSED',
                    'BRAINSTORM',
                    'DONE',
                    'ARCHIVED'
                  ],
                  onChanged: (v) =>
                      _patch(ref, project, {'projectStatus': v}),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _EnumPicker(
                  label: 'Priority',
                  value: project.priority,
                  options: const ['HIGH', 'NORMAL', 'LOW'],
                  onChanged: (v) => _patch(ref, project, {'priority': v}),
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          Text('Waypoints', style: Theme.of(context).textTheme.titleMedium),
          if (project.waypoints.isEmpty)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 8),
              child: Text('No waypoints yet.'),
            ),
          for (final (i, waypoint) in project.waypoints.indexed)
            ListTile(
              dense: true,
              leading: Icon(switch (waypoint.status) {
                WaypointStatus.done => Icons.check_circle,
                WaypointStatus.inProgress => Icons.timelapse,
                WaypointStatus.todo => Icons.radio_button_unchecked,
              }),
              title: Text(waypoint.label),
              onTap: () => _cycleWaypoint(ref, project, i),
              onLongPress: () => _waypointActions(context, ref, project, i),
            ),
          TextButton.icon(
            icon: const Icon(Icons.add),
            label: const Text('Add waypoint'),
            onPressed: () => _addWaypoint(context, ref, project),
          ),
          const SizedBox(height: 24),
          Text('Tasks', style: Theme.of(context).textTheme.titleMedium),
          if (todos.isEmpty)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 8),
              child: Text('No tasks for this project yet.'),
            ),
          for (final todo in todos)
            CheckboxListTile(
              dense: true,
              value: todo.isDone,
              title: Text(todo.title,
                  style: todo.isDone
                      ? const TextStyle(
                          decoration: TextDecoration.lineThrough)
                      : null),
              onChanged: (checked) => ref
                  .read(todosControllerProvider.notifier)
                  .setStatus(todo, checked == true ? 'DONE' : 'OPEN'),
            ),
          const SizedBox(height: 24),
          WishlistSection(project: project),
          const SizedBox(height: 48),
        ],
      ),
    );
  }

  Future<void> _waypointActions(
      BuildContext context, WidgetRef ref, Project project, int index) async {
    final waypoints = project.waypoints;
    final action = await showModalBottomSheet<String>(
      context: context,
      builder: (ctx) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              title: Text(waypoints[index].label,
                  style: Theme.of(ctx).textTheme.titleSmall),
            ),
            if (index > 0)
              ListTile(
                leading: const Icon(Icons.arrow_upward),
                title: const Text('Move up'),
                onTap: () => Navigator.of(ctx).pop('up'),
              ),
            if (index < waypoints.length - 1)
              ListTile(
                leading: const Icon(Icons.arrow_downward),
                title: const Text('Move down'),
                onTap: () => Navigator.of(ctx).pop('down'),
              ),
            ListTile(
              leading: const Icon(Icons.delete_outline),
              title: const Text('Remove'),
              onTap: () => Navigator.of(ctx).pop('remove'),
            ),
          ],
        ),
      ),
    );
    if (action == null) return;
    final updated = [...waypoints];
    switch (action) {
      case 'up':
        updated.insert(index - 1, updated.removeAt(index));
      case 'down':
        updated.insert(index + 1, updated.removeAt(index));
      case 'remove':
        updated.removeAt(index);
    }
    await _patch(
        ref, project, {'waypoints': Waypoint.serializeList(updated)});
  }

  Future<void> _patch(
      WidgetRef ref, Project project, Map<String, dynamic> patch) async {
    final repo = ref.read(projectsRepositoryProvider);
    if (repo == null) return;
    await repo.update(project, patch);
    ref.invalidate(projectsProvider);
  }

  Future<void> _cycleWaypoint(WidgetRef ref, Project project, int index) async {
    final waypoints = [...project.waypoints];
    final current = waypoints[index];
    final next = switch (current.status) {
      WaypointStatus.todo => WaypointStatus.inProgress,
      WaypointStatus.inProgress => WaypointStatus.done,
      WaypointStatus.done => WaypointStatus.todo,
    };
    waypoints[index] = Waypoint(current.label, next);
    await _patch(ref, project, {'waypoints': Waypoint.serializeList(waypoints)});
  }

  Future<void> _addWaypoint(
      BuildContext context, WidgetRef ref, Project project) async {
    final label = await _promptText(context, 'Add waypoint', 'Waypoint');
    if (label == null || label.trim().isEmpty) return;
    final waypoints = [
      ...project.waypoints,
      Waypoint(label.trim(), WaypointStatus.todo)
    ];
    await _patch(ref, project, {'waypoints': Waypoint.serializeList(waypoints)});
  }

  Future<void> _addTask(
      BuildContext context, WidgetRef ref, Project project) async {
    final title = await _promptText(context, 'Add task', 'Task title');
    if (title == null || title.trim().isEmpty) return;
    await ref.read(todosControllerProvider.notifier).create({
      'title': title.trim(),
      'category': 'HONEYDO',
      'priority': 'NORMAL',
      'status': 'OPEN',
      'dreamId': project.id,
    });
  }

  Future<String?> _promptText(
      BuildContext context, String title, String label) {
    final controller = TextEditingController();
    return showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(title),
        content: TextField(
          controller: controller,
          autofocus: true,
          decoration: InputDecoration(labelText: label),
          onSubmitted: (v) => Navigator.of(ctx).pop(v),
        ),
        actions: [
          TextButton(
              onPressed: () => Navigator.of(ctx).pop(),
              child: const Text('Cancel')),
          FilledButton(
              onPressed: () => Navigator.of(ctx).pop(controller.text),
              child: const Text('Add')),
        ],
      ),
    );
  }
}

class _EnumPicker extends StatelessWidget {
  const _EnumPicker({
    required this.label,
    required this.value,
    required this.options,
    required this.onChanged,
  });

  final String label;
  final String value;
  final List<String> options;
  final ValueChanged<String> onChanged;

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      decoration: InputDecoration(labelText: label),
      initialValue: options.contains(value) ? value : options.first,
      items: [
        for (final option in options)
          DropdownMenuItem(value: option, child: Text(option)),
      ],
      onChanged: (v) {
        if (v != null) onChanged(v);
      },
    );
  }
}
