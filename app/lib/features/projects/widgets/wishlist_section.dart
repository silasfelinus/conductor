import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../todos/todo_models.dart';
import '../../todos/todos_repository.dart';
import '../project_models.dart';

/// The project feature wishlist: DESIRED_FEATURE todos linked to the project
/// (dreamId), kept in an explicit order. Items can be reordered, promoted to
/// an AGENT task, or retired (archived) — mirroring the kind_robots
/// workspace behavior.
class WishlistSection extends ConsumerWidget {
  const WishlistSection({super.key, required this.project});

  final Project project;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final wishlist = (ref.watch(todosControllerProvider).valueOrNull ?? [])
        .where((t) =>
            t.dreamId == project.id &&
            t.category == 'DESIRED_FEATURE' &&
            t.status != 'ARCHIVED')
        .toList()
      ..sort((a, b) => (a.order ?? 1 << 30).compareTo(b.order ?? 1 << 30));

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Feature wishlist', style: Theme.of(context).textTheme.titleMedium),
        if (wishlist.isEmpty)
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 8),
            child: Text('Nothing on the wishlist yet.'),
          ),
        for (final (index, item) in wishlist.indexed)
          ListTile(
            dense: true,
            leading: Text('${index + 1}.',
                style: Theme.of(context).textTheme.titleSmall),
            title: Text(item.title),
            subtitle: item.description?.isNotEmpty == true
                ? Text(item.description!,
                    maxLines: 1, overflow: TextOverflow.ellipsis)
                : null,
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                IconButton(
                  icon: const Icon(Icons.arrow_upward, size: 18),
                  tooltip: 'Move up',
                  onPressed: index == 0
                      ? null
                      : () => _move(ref, wishlist, index, index - 1),
                ),
                IconButton(
                  icon: const Icon(Icons.arrow_downward, size: 18),
                  tooltip: 'Move down',
                  onPressed: index == wishlist.length - 1
                      ? null
                      : () => _move(ref, wishlist, index, index + 1),
                ),
                PopupMenuButton<String>(
                  onSelected: (action) => _onAction(context, ref, item, action),
                  itemBuilder: (ctx) => const [
                    PopupMenuItem(
                        value: 'promote',
                        child: Text('Promote to agent task')),
                    PopupMenuItem(value: 'retire', child: Text('Retire')),
                  ],
                ),
              ],
            ),
          ),
        TextButton.icon(
          icon: const Icon(Icons.add),
          label: const Text('Add to wishlist'),
          onPressed: () => _add(context, ref, wishlist.length),
        ),
      ],
    );
  }

  /// Reorders by rewriting `order` to the list position for every item whose
  /// position changed — resilient to legacy rows with null/duplicate orders.
  Future<void> _move(
      WidgetRef ref, List<Todo> wishlist, int from, int to) async {
    final reordered = [...wishlist];
    final item = reordered.removeAt(from);
    reordered.insert(to, item);
    final controller = ref.read(todosControllerProvider.notifier);
    for (final (index, todo) in reordered.indexed) {
      if (todo.order != index) {
        await controller.update(todo, {'order': index});
      }
    }
  }

  Future<void> _onAction(
      BuildContext context, WidgetRef ref, Todo item, String action) async {
    final controller = ref.read(todosControllerProvider.notifier);
    switch (action) {
      case 'promote':
        await controller
            .update(item, {'category': 'AGENT', 'priority': 'HIGH'});
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              content: Text('"${item.title}" promoted to agent task')));
        }
      case 'retire':
        await controller.update(item, {'status': 'ARCHIVED'});
    }
  }

  Future<void> _add(BuildContext context, WidgetRef ref, int position) async {
    final controller = TextEditingController();
    final title = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Add to wishlist'),
        content: TextField(
          controller: controller,
          autofocus: true,
          decoration: const InputDecoration(labelText: 'Desired feature'),
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
    if (title == null || title.trim().isEmpty) return;
    await ref.read(todosControllerProvider.notifier).create({
      'title': title.trim(),
      'category': 'DESIRED_FEATURE',
      'priority': 'LOW',
      'status': 'OPEN',
      'dreamId': project.id,
      'order': position,
    });
  }
}
