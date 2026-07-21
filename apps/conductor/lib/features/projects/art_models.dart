/// A single generated image, as returned embedded under a project's
/// (kind_robots Dream's) `ArtCollection`/`ArtCollections` relations.
class ArtImageSummary {
  const ArtImageSummary({
    required this.id,
    this.imagePath,
    this.path,
    this.fileName,
    this.promptString,
    this.artPrompt,
  });

  final int id;
  final String? imagePath;
  final String? path;
  final String? fileName;
  final String? promptString;
  final String? artPrompt;

  /// Server-relative path to resolve against the active server's base URL.
  String? get displayPath => imagePath ?? path;

  factory ArtImageSummary.fromJson(Map<String, dynamic> json) =>
      ArtImageSummary(
        id: (json['id'] as num?)?.toInt() ?? 0,
        imagePath: json['imagePath'] as String?,
        path: json['path'] as String?,
        fileName: json['fileName'] as String?,
        promptString: json['promptString'] as String?,
        artPrompt: json['artPrompt'] as String?,
      );
}

/// A gallery of images (kind_robots ArtCollection) linked to a project,
/// used for browsing existing art as inspiration before requesting new work.
class ArtCollectionSummary {
  const ArtCollectionSummary({
    required this.id,
    this.label,
    this.description,
    this.imagePath,
    this.artPrompt,
    this.images = const [],
  });

  final int id;
  final String? label;
  final String? description;
  final String? imagePath;
  final String? artPrompt;
  final List<ArtImageSummary> images;

  String get displayLabel =>
      (label?.isNotEmpty ?? false) ? label! : 'Untitled collection';

  factory ArtCollectionSummary.fromJson(Map<String, dynamic> json) =>
      ArtCollectionSummary(
        id: (json['id'] as num?)?.toInt() ?? 0,
        label: json['label'] as String?,
        description: json['description'] as String?,
        imagePath: json['imagePath'] as String?,
        artPrompt: json['artPrompt'] as String?,
        images: ((json['ArtImages'] as List?) ?? const [])
            .whereType<Map<String, dynamic>>()
            .map(ArtImageSummary.fromJson)
            .toList(),
      );
}
