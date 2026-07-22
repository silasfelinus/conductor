import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../art_repository.dart';

/// Admin-only form to queue a new art request into Conductor's
/// art-prompts.yaml, via POST /api/conductor/art-request. Server-side
/// authorization (admin role + API key) is what actually gates the call;
/// callers must still only offer this UI to admins.
class ArtRequestFormSheet extends StatefulWidget {
  const ArtRequestFormSheet({super.key});

  /// Shows the form, submits it if confirmed, and reports the result via a
  /// snackbar. Safe to call from a button's onPressed.
  static Future<void> show(BuildContext context, WidgetRef ref) async {
    final repo = ref.read(artRepositoryProvider);
    if (repo == null) {
      ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Connect to a server to request art.')));
      return;
    }
    final fields = await showModalBottomSheet<Map<String, String>>(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => const ArtRequestFormSheet(),
    );
    if (fields == null) return;
    final imagePath = fields['imagePath'] ?? '';
    if (imagePath.isEmpty) return;

    try {
      await repo.submitArtRequest(
        imagePath: imagePath,
        label: fields['label'],
        prompt: fields['prompt'],
        variant: fields['variant'],
        pageUrl: fields['pageUrl'],
      );
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Art request queued in Conductor.')));
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text('$e')));
      }
    }
  }

  @override
  State<ArtRequestFormSheet> createState() => _ArtRequestFormSheetState();
}

class _ArtRequestFormSheetState extends State<ArtRequestFormSheet> {
  final _imagePathController = TextEditingController();
  final _labelController = TextEditingController();
  final _promptController = TextEditingController();
  final _pageUrlController = TextEditingController();
  String _variant = 'image';

  static const _variants = ['image', 'icon', 'card', 'hero'];

  @override
  void dispose() {
    _imagePathController.dispose();
    _labelController.dispose();
    _promptController.dispose();
    _pageUrlController.dispose();
    super.dispose();
  }

  void _submit() {
    final imagePath = _imagePathController.text.trim();
    if (imagePath.isEmpty) return;
    Navigator.of(context).pop({
      'imagePath': imagePath,
      'label': _labelController.text.trim(),
      'prompt': _promptController.text.trim(),
      'variant': _variant,
      'pageUrl': _pageUrlController.text.trim(),
    });
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
            Text('Request art', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 4),
            Text(
              'Queues a new entry in art-prompts.yaml for the next art-generation cycle.',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _imagePathController,
              autofocus: true,
              decoration: const InputDecoration(
                labelText: 'Image path',
                hintText: 'public/images/foo.webp',
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _labelController,
              decoration: const InputDecoration(labelText: 'Label (optional)'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _promptController,
              maxLines: 3,
              decoration: const InputDecoration(labelText: 'Prompt (optional)'),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              initialValue: _variant,
              decoration: const InputDecoration(labelText: 'Variant'),
              items: [
                for (final variant in _variants)
                  DropdownMenuItem(value: variant, child: Text(variant)),
              ],
              onChanged: (value) {
                if (value != null) setState(() => _variant = value);
              },
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _pageUrlController,
              keyboardType: TextInputType.url,
              decoration:
                  const InputDecoration(labelText: 'Page URL (optional)'),
            ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: _submit,
              child: const Text('Queue request'),
            ),
          ],
        ),
      ),
    );
  }
}
