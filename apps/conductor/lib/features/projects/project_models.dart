/// A project is a kind_robots Dream row with dreamType PROJECT.
/// In local mode the same model is stored on-device.
class Project {
  const Project({
    required this.id,
    required this.slug,
    required this.title,
    this.description,
    this.goal,
    this.pitch,
    this.flavorText,
    this.liveUrl,
    this.repoUrl,
    this.projectStatus = 'ACTIVE',
    this.priority = 'NORMAL',
    this.imagePath,
    this.cardPath,
    this.heroPath,
    this.isPublic = false,
  });

  final int id;
  final String slug;
  final String title;
  final String? description;
  final String? goal;
  final String? pitch;
  final String? flavorText;
  final String? liveUrl;
  final String? repoUrl;
  final String projectStatus; // ACTIVE | PAUSED | BRAINSTORM | DONE | ARCHIVED
  final String priority; // LOW | NORMAL | HIGH
  final String? imagePath;
  final String? cardPath;
  final String? heroPath;
  final bool isPublic;

  factory Project.fromJson(Map<String, dynamic> json) => Project(
        id: (json['id'] as num?)?.toInt() ?? 0,
        slug: (json['slug'] as String?) ?? '',
        title: (json['title'] as String?) ?? 'Untitled',
        description: json['description'] as String?,
        goal: json['goal'] as String?,
        pitch: json['pitch'] as String?,
        flavorText: json['flavorText'] as String?,
        liveUrl: json['liveUrl'] as String?,
        repoUrl: json['repoUrl'] as String?,
        projectStatus: (json['projectStatus'] as String?) ?? 'ACTIVE',
        priority: (json['priority'] as String?) ?? 'NORMAL',
        imagePath: json['imagePath'] as String?,
        cardPath: json['cardPath'] as String?,
        heroPath: json['heroPath'] as String?,
        isPublic: (json['isPublic'] as bool?) ?? false,
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'slug': slug,
        'title': title,
        'description': description,
        'goal': goal,
        'pitch': pitch,
        'flavorText': flavorText,
        'liveUrl': liveUrl,
        'repoUrl': repoUrl,
        'projectStatus': projectStatus,
        'priority': priority,
        'imagePath': imagePath,
        'cardPath': cardPath,
        'heroPath': heroPath,
        'isPublic': isPublic,
      };
}
