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
    this.waypoints = const [],
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
  final List<Waypoint> waypoints;
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
        waypoints: Waypoint.parseList(json['waypoints'] as String?),
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
        'waypoints': Waypoint.serializeList(waypoints),
        'isPublic': isPublic,
      };
}

enum WaypointStatus { todo, inProgress, done }

/// Waypoints are stored server-side as one pipe-delimited string on the
/// Dream: "✓ done step|~ in-progress step|future step".
class Waypoint {
  const Waypoint(this.label, this.status);

  final String label;
  final WaypointStatus status;

  static List<Waypoint> parseList(String? raw) {
    if (raw == null || raw.trim().isEmpty) return const [];
    return raw.split('|').where((s) => s.trim().isNotEmpty).map((s) {
      final t = s.trim();
      if (t.startsWith('✓ ')) return Waypoint(t.substring(2), WaypointStatus.done);
      if (t.startsWith('~ ')) {
        return Waypoint(t.substring(2), WaypointStatus.inProgress);
      }
      return Waypoint(t, WaypointStatus.todo);
    }).toList();
  }

  static String serializeList(List<Waypoint> waypoints) => waypoints
      .map((w) => switch (w.status) {
            WaypointStatus.done => '✓ ${w.label}',
            WaypointStatus.inProgress => '~ ${w.label}',
            WaypointStatus.todo => w.label,
          })
      .join('|');
}
