import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'todo_models.dart';
import 'todos_repository.dart';

class TodosScreen extends ConsumerStatefulWidget {
  const TodosScreen({super.key});

  @override
  ConsumerState<TodosScreen> createState() => _TodosScreenState();
}

class _TodosScreenState extends ConsumerState<TodosScreen> {
  String _filter = 'OPEN';

  @override
  Widget build(BuildContext context) {
    final todos = ref.watch(todosControllerProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Todos')),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _createTodo(context),
        child: const Icon(Icons.add),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'OPEN', label: Text('Open')),
                ButtonSegment(value: 'DONE', label: Text('Done')),
                ButtonSegment(value: 'ARCHIVED', label: Text('Archived')),
              ],
              selected: {_filter},
              onSelectionChanged: (s) => setState(() => _filter = s.first),
            ),
          ),
          Expanded(
            child: todos.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(child: Text('$e')),
              data: (items) {
                final filtered =
                    items.where((t) => t.status == _filter).toList();
                if (filtered.isEmpty) {
                  return const Center(child: Text('Nothing here.'));
                }
                return ListView.builder(
                  itemCount: filtered.length,
                  itemBuilder: (context, i) => _TodoTile(todo: filtered[i]),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _createTodo(BuildContext context) async {
    final result = await showModalBottomSheet<Map<String, dynamic>>(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => const _TodoComposer(),
    );
    if (result == null) return;
    await ref.read(todosControllerProvider.notifier).create(result);
  }
}

Future<void> editTodo(BuildContext context, WidgetRef ref, Todo todo) async {
  final result = await showModalBottomSheet<Map<String, dynamic>>(
    context: context,
    isScrollControlled: true,
    builder: (ctx) => _TodoComposer(initial: todo),
  );
  if (result == null) return;
  await ref.read(todosControllerProvider.notifier).update(todo, result);
}

class _TodoTile extends ConsumerWidget {
  const _TodoTile({required this.todo});

  final Todo todo;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = ref.read(todosControllerProvider.notifier);
    return Dismissible(
      key: ValueKey(todo.id),
      background: Container(
        color: Theme.of(context).colorScheme.primaryContainer,
        alignment: Alignment.centerLeft,
        padding: const EdgeInsets.only(left: 24),
        child: const Icon(Icons.check),
      ),
      secondaryBackground: Container(
        color: Theme.of(context).colorScheme.errorContainer,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 24),
        child: const Icon(Icons.archive),
      ),
      confirmDismiss: (direction) async {
        if (direction == DismissDirection.startToEnd) {
          await controller.setStatus(todo, todo.isDone ? 'OPEN' : 'DONE');
        } else {
          await controller.setStatus(todo, 'ARCHIVED');
        }
        return false; // list refreshes via provider invalidation
      },
      child: ListTile(
        leading: Icon(switch (todo.priority) {
          'HIGH' => Icons.priority_high,
          'LOW' => Icons.low_priority,
          _ => Icons.drag_handle,
        }),
        title: Text(todo.title,
            style: todo.isDone
                ? const TextStyle(decoration: TextDecoration.lineThrough)
                : null),
        subtitle: todo.description?.isNotEmpty == true
            ? Text(todo.description!,
                maxLines: 1, overflow: TextOverflow.ellipsis)
            : null,
        trailing: Chip(
          label: Text(todo.category, style: const TextStyle(fontSize: 10)),
          visualDensity: VisualDensity.compact,
        ),
        onTap: () => editTodo(context, ref, todo),
      ),
    );
  }
}

class _TodoComposer extends StatefulWidget {
  const _TodoComposer({this.initial});

  /// When set, the sheet edits this todo instead of composing a new one.
  final Todo? initial;

  @override
  State<_TodoComposer> createState() => _TodoComposerState();
}

class _TodoComposerState extends State<_TodoComposer> {
  late final _title = TextEditingController(text: widget.initial?.title ?? '');
  late final _description =
      TextEditingController(text: widget.initial?.description ?? '');
  late String _priority = widget.initial?.priority ?? 'NORMAL';
  late String _category = widget.initial?.category ?? 'HONEYDO';

  @override
  void dispose() {
    _title.dispose();
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
          Text(widget.initial == null ? 'New todo' : 'Edit todo',
              style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 16),
          TextField(
            controller: _title,
            autofocus: true,
            decoration: const InputDecoration(labelText: 'Title'),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _description,
            decoration:
                const InputDecoration(labelText: 'Description (optional)'),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: DropdownButtonFormField<String>(
                  decoration: const InputDecoration(labelText: 'Priority'),
                  value: _priority,
                  items: const [
                    DropdownMenuItem(value: 'HIGH', child: Text('High')),
                    DropdownMenuItem(value: 'NORMAL', child: Text('Normal')),
                    DropdownMenuItem(value: 'LOW', child: Text('Low')),
                  ],
                  onChanged: (v) => setState(() => _priority = v ?? 'NORMAL'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: DropdownButtonFormField<String>(
                  decoration: const InputDecoration(labelText: 'Category'),
                  value: _category,
                  items: const [
                    DropdownMenuItem(value: 'HONEYDO', child: Text('Honey-do')),
                    DropdownMenuItem(value: 'AGENT', child: Text('Agent')),
                    DropdownMenuItem(value: 'KAIZEN', child: Text('Kaizen')),
                    DropdownMenuItem(
                        value: 'DESIRED_FEATURE', child: Text('Wishlist')),
                  ],
                  onChanged: (v) => setState(() => _category = v ?? 'HONEYDO'),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () {
              if (_title.text.trim().isEmpty) return;
              Navigator.of(context).pop({
                'title': _title.text.trim(),
                'description': _description.text.trim().isEmpty
                    ? null
                    : _description.text.trim(),
                'priority': _priority,
                'category': _category,
                // New todos start OPEN; edits keep their current status.
                if (widget.initial == null) 'status': 'OPEN',
              });
            },
            child: Text(widget.initial == null ? 'Add' : 'Save'),
          ),
        ],
      ),
    );
  }
}
