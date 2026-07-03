import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'agent_ops_repository.dart';

/// Approvals come from the conductor repo roadmaps: tasks that are
/// needs-human or gate_human-and-unapproved. Approval itself is a YAML edit
/// in the repo, so the in-app action is "send a note to the conductor inbox"
/// — the agents (or Silas at a keyboard) apply the actual roadmap change.
class ApprovalsScreen extends ConsumerWidget {
  const ApprovalsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final ops = ref.watch(agentOpsDataProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Needs your decision')),
      body: ops.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('$e')),
        data: (data) {
          if (data == null) {
            return const Center(
              child: Padding(
                padding: EdgeInsets.all(24),
                child: Text(
                  'Agent Ops is available for admins on servers with the '
                  'conductor integration.',
                  textAlign: TextAlign.center,
                ),
              ),
            );
          }
          final approvals = data.approvals;
          final pitches = data.pitches
              .where((p) => p.status == 'awaiting-silas' || p.status == 'proposed')
              .toList();
          if (approvals.isEmpty && pitches.isEmpty) {
            return const Center(child: Text('Nothing needs you right now. 🎉'));
          }
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              if (approvals.isNotEmpty)
                Text('Gated tasks',
                    style: Theme.of(context).textTheme.titleMedium),
              for (final (project, task) in approvals)
                Card(
                  child: ListTile(
                    title: Text(task.title),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('${project.slug} / ${task.id} — ${task.status}'),
                        if (task.note?.isNotEmpty == true)
                          Padding(
                            padding: const EdgeInsets.only(top: 4),
                            child: Text(task.note!,
                                maxLines: 4, overflow: TextOverflow.ellipsis),
                          ),
                      ],
                    ),
                    isThreeLine: task.note?.isNotEmpty == true,
                    trailing: IconButton(
                      icon: const Icon(Icons.reply),
                      tooltip: 'Reply to conductor inbox',
                      onPressed: () =>
                          _composeReply(context, ref, project.slug, task.id),
                    ),
                  ),
                ),
              if (pitches.isNotEmpty) ...[
                const SizedBox(height: 16),
                Text('Pitches awaiting a vote',
                    style: Theme.of(context).textTheme.titleMedium),
                for (final pitch in pitches)
                  Card(
                    child: ListTile(
                      title: Text(pitch.title),
                      subtitle: Text(pitch.slug),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          IconButton(
                            icon: const Icon(Icons.thumb_up),
                            tooltip: 'Approve',
                            onPressed: () =>
                                _vote(context, ref, pitch.slug, 'approved'),
                          ),
                          IconButton(
                            icon: const Icon(Icons.thumb_down),
                            tooltip: 'Pass',
                            onPressed: () =>
                                _vote(context, ref, pitch.slug, 'passed'),
                          ),
                        ],
                      ),
                    ),
                  ),
              ],
            ],
          );
        },
      ),
    );
  }

  Future<void> _vote(
      BuildContext context, WidgetRef ref, String slug, String vote) async {
    final repo = ref.read(agentOpsRepositoryProvider);
    if (repo == null) return;
    await repo.votePitch(slug, vote);
    ref.invalidate(agentOpsDataProvider);
    if (context.mounted) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Voted $vote on $slug')));
    }
  }

  Future<void> _composeReply(BuildContext context, WidgetRef ref,
      String projectSlug, String taskId) async {
    final controller = TextEditingController();
    final message = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Note about $projectSlug/$taskId'),
        content: TextField(
          controller: controller,
          autofocus: true,
          maxLines: 4,
          decoration: const InputDecoration(
              hintText: 'e.g. Approved — set approved_by_human on this task.'),
        ),
        actions: [
          TextButton(
              onPressed: () => Navigator.of(ctx).pop(),
              child: const Text('Cancel')),
          FilledButton(
              onPressed: () => Navigator.of(ctx).pop(controller.text),
              child: const Text('Send')),
        ],
      ),
    );
    if (message == null || message.trim().isEmpty) return;
    final repo = ref.read(agentOpsRepositoryProvider);
    if (repo == null) return;
    await repo.sendInboxMessage('[$projectSlug/$taskId] ${message.trim()}');
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Sent to conductor inbox')));
    }
  }
}
