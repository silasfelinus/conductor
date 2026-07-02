class AppUser {
  const AppUser({
    required this.id,
    required this.username,
    this.email,
    this.role = 'USER',
    this.karma = 0,
    this.mana = 0,
    this.avatarImage,
  });

  final int id;
  final String username;
  final String? email;
  final String role;
  final int karma;
  final int mana;
  final String? avatarImage;

  /// Server-side authorization is what actually gates privileged calls;
  /// this flag only controls which UI surfaces are shown.
  bool get isAdmin => role == 'ADMIN';

  factory AppUser.fromJson(Map<String, dynamic> json) => AppUser(
        id: (json['id'] as num).toInt(),
        username: (json['username'] as String?) ?? 'user',
        email: json['email'] as String?,
        role: (json['Role'] as String?) ?? (json['role'] as String?) ?? 'USER',
        karma: (json['karma'] as num?)?.toInt() ?? 0,
        mana: (json['mana'] as num?)?.toInt() ?? 0,
        avatarImage: json['avatarImage'] as String?,
      );
}
