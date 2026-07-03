import 'package:flutter/material.dart';

import '../project_models.dart';

/// Edits the project "intent" fields the kind_robots workspace exposes:
/// goal, description, pitch, flavor text, live URL, repo URL.
/// Returns a patch map of only the fields that changed, or null on cancel.
class IntentEditorSheet extends StatefulWidget {
  const IntentEditorSheet({super.key, required this.project});

  final Project project;

  static Future<Map<String, dynamic>?> show(
      BuildContext context, Project project) {
    return showModalBottomSheet<Map<String, dynamic>>(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => IntentEditorSheet(project: project),
    );
  }

  @override
  State<IntentEditorSheet> createState() => _IntentEditorSheetState();
}

class _IntentEditorSheetState extends State<IntentEditorSheet> {
  late final Map<String, TextEditingController> _fields;

  static const _labels = {
    'title': 'Title',
    'goal': 'Goal',
    'description': 'Description',
    'pitch': 'Pitch',
    'flavorText': 'Flavor text',
    'liveUrl': 'Live URL',
    'repoUrl': 'Repo URL',
  };

  @override
  void initState() {
    super.initState();
    final p = widget.project;
    _fields = {
      'title': TextEditingController(text: p.title),
      'goal': TextEditingController(text: p.goal ?? ''),
      'description': TextEditingController(text: p.description ?? ''),
      'pitch': TextEditingController(text: p.pitch ?? ''),
      'flavorText': TextEditingController(text: p.flavorText ?? ''),
      'liveUrl': TextEditingController(text: p.liveUrl ?? ''),
      'repoUrl': TextEditingController(text: p.repoUrl ?? ''),
    };
  }

  @override
  void dispose() {
    for (final controller in _fields.values) {
      controller.dispose();
    }
    super.dispose();
  }

  Map<String, dynamic> _buildPatch() {
    final original = widget.project.toJson();
    final patch = <String, dynamic>{};
    for (final entry in _fields.entries) {
      final value = entry.value.text.trim();
      final before = (original[entry.key] as String?) ?? '';
      if (value != before.trim()) {
        patch[entry.key] = value.isEmpty ? null : value;
      }
    }
    // A project always needs a title; ignore attempts to blank it.
    if (patch.containsKey('title') && patch['title'] == null) {
      patch.remove('title');
    }
    return patch;
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
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('Project details',
                style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 16),
            for (final entry in _fields.entries) ...[
              TextField(
                controller: entry.value,
                maxLines: switch (entry.key) {
                  'description' || 'pitch' => 3,
                  'goal' || 'flavorText' => 2,
                  _ => 1,
                },
                keyboardType: entry.key.endsWith('Url')
                    ? TextInputType.url
                    : TextInputType.text,
                decoration: InputDecoration(labelText: _labels[entry.key]),
              ),
              const SizedBox(height: 12),
            ],
            FilledButton(
              onPressed: () => Navigator.of(context).pop(_buildPatch()),
              child: const Text('Save'),
            ),
          ],
        ),
      ),
    );
  }
}
