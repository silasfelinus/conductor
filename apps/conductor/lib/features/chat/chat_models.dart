/// One exchange in a project chat: the user's message and (once generated)
/// the assistant's reply, matching the kind_robots Chat row shape.
class ChatMessage {
  const ChatMessage({
    required this.id,
    required this.content,
    this.botResponse,
    this.createdAt,
  });

  final int id;
  final String content;
  final String? botResponse;
  final DateTime? createdAt;

  factory ChatMessage.fromJson(Map<String, dynamic> json) => ChatMessage(
        id: (json['id'] as num).toInt(),
        content: (json['content'] as String?) ?? '',
        botResponse: json['botResponse'] as String?,
        createdAt: json['createdAt'] != null
            ? DateTime.tryParse(json['createdAt'] as String)
            : null,
      );

  ChatMessage copyWith({String? botResponse}) => ChatMessage(
        id: id,
        content: content,
        botResponse: botResponse ?? this.botResponse,
        createdAt: createdAt,
      );
}
