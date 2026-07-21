import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../auth/auth_controller.dart';
import '../art_models.dart';
import '../art_repository.dart';
import '../project_models.dart';
import 'art_request_form_sheet.dart';

/// Browse a project's linked ArtCollections for inspiration, and (admins
/// only) queue a new art request into Conductor's art-prompts.yaml queue.
/// Hidden entirely in local mode, since there is no server to browse or
/// queue against.
class ArtInspirationSection extends ConsumerWidget {
  const ArtInspirationSection({super.key, required this.project});

  final Project project;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final config = ref.watch(serverConfigProvider);
    if (config == null || config.isLocal) return const SizedBox.shrink();

    final collectionsAsync =
        ref.watch(artCollectionsForProjectProvider(project.id));
    final isAdmin = ref.watch(currentUserProvider)?.isAdmin ?? false;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('Inspiration', style: Theme.of(context).textTheme.titleMedium),
            if (isAdmin)
              TextButton.icon(
                icon: const Icon(Icons.add_photo_alternate_outlined),
                label: const Text('Request art'),
                onPressed: () => ArtRequestFormSheet.show(context, ref),
              ),
          ],
        ),
        collectionsAsync.when(
          loading: () => const Padding(
            padding: EdgeInsets.symmetric(vertical: 16),
            child: Center(child: CircularProgressIndicator()),
          ),
          error: (error, _) => Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Text('Could not load inspiration art: $error',
                style: Theme.of(context).textTheme.bodySmall),
          ),
          data: (collections) {
            final withImages =
                collections.where((c) => c.images.isNotEmpty).toList();
            if (withImages.isEmpty) {
              return const Padding(
                padding: EdgeInsets.symmetric(vertical: 8),
                child: Text('No art collected for this project yet.'),
              );
            }
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                for (final collection in withImages)
                  _CollectionRow(collection: collection),
              ],
            );
          },
        ),
      ],
    );
  }
}

class _CollectionRow extends ConsumerWidget {
  const _CollectionRow({required this.collection});

  final ArtCollectionSummary collection;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final resolveUrl = ref.watch(serverConfigProvider)?.resolveAssetUrl;

    return Padding(
      padding: const EdgeInsets.only(top: 8, bottom: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(collection.displayLabel,
              style: Theme.of(context).textTheme.labelLarge),
          const SizedBox(height: 6),
          SizedBox(
            height: 96,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: collection.images.length,
              separatorBuilder: (_, __) => const SizedBox(width: 8),
              itemBuilder: (context, index) {
                final image = collection.images[index];
                final url = resolveUrl?.call(image.displayPath);
                return ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: GestureDetector(
                    onTap: () => _showFull(context, url, image),
                    child: SizedBox(
                      width: 96,
                      height: 96,
                      child: url == null
                          ? const ColoredBox(color: Colors.black12)
                          : CachedNetworkImage(
                              imageUrl: url,
                              fit: BoxFit.cover,
                              errorWidget: (context, url, error) =>
                                  const ColoredBox(color: Colors.black12),
                            ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  void _showFull(BuildContext context, String? url, ArtImageSummary image) {
    showDialog<void>(
      context: context,
      builder: (ctx) => Dialog(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (url != null)
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: CachedNetworkImage(imageUrl: url, fit: BoxFit.contain),
                ),
              if ((image.promptString ?? image.artPrompt)?.isNotEmpty ==
                  true) ...[
                const SizedBox(height: 8),
                Text(image.promptString ?? image.artPrompt!,
                    style: Theme.of(ctx).textTheme.bodySmall),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
