import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../auth/auth_controller.dart';
import '../projects/project_models.dart';
import 'chat_models.dart';

/// Per-project assistant chat, mirroring the kind_robots workspace flow:
/// 1. persist the user message as a Chat row on channel dream-<id>-assistant
/// 2. stream the reply from /api/chats/anthropic/stream (JWT + mana gated)
/// 3. persist the finished reply back onto the Chat row
class ProjectChatRepository {
  ProjectChatRepository(this._api);

  final ApiClient _api;

  static String channelFor(int dreamId) => 'dream-$dreamId-assistant';

  Future<List<ChatMessage>> history(int dreamId) async {
    final res = await _api.get('/api/chats', query: {
      'channel': channelFor(dreamId),
      'mine': '1',
      'take': '50',
    });
    final items = unwrap(res, ['chats', 'data']);
    final messages = (items as List)
        .whereType<Map<String, dynamic>>()
        .map(ChatMessage.fromJson)
        .toList();
    messages.sort((a, b) => a.id.compareTo(b.id));
    return messages;
  }

  Future<ChatMessage> createUserMessage(int dreamId, String content) async {
    final res = await _api.post('/api/chats', body: {
      'content': content,
      'channel': channelFor(dreamId),
      'type': 'ToBot',
      'dreamId': dreamId,
    });
    return ChatMessage.fromJson(
        unwrap(res, ['chat', 'data']) as Map<String, dynamic>);
  }

  /// Yields text tokens as they arrive. The payload is Anthropic's SSE
  /// format proxied by the server; anything unrecognized is skipped.
  Stream<String> streamReply({
    required List<Map<String, String>> messages,
    required String system,
    int? chatId,
  }) async* {
    final lines = _api.postEventStream('/api/chats/anthropic/stream', body: {
      'messages': messages,
      'system': system,
      if (chatId != null) 'chatId': chatId,
    });
    await for (final line in lines) {
      if (!line.startsWith('data:')) continue;
      final data = line.substring(5).trim();
      if (data.isEmpty || data == '[DONE]') continue;
      try {
        final event = jsonDecode(data) as Map<String, dynamic>;
        if (event['type'] == 'content_block_delta') {
          final delta = event['delta'];
          if (delta is Map && delta['type'] == 'text_delta') {
            final text = delta['text'] as String?;
            if (text != null && text.isNotEmpty) yield text;
          }
        }
      } catch (_) {
        // Non-JSON keepalives and metering events are expected; skip them.
      }
    }
  }

  Future<void> saveBotResponse(int chatId, String text) =>
      _api.patch('/api/chats/$chatId', body: {'botResponse': text});

  /// The same project context the kind_robots workspace assistant gets.
  static String systemPromptFor(Project project) {
    return [
      'You are the project assistant for "${project.title}".',
      if (project.goal?.isNotEmpty == true) 'Goal: ${project.goal}',
      if (project.pitch?.isNotEmpty == true) 'Pitch: ${project.pitch}',
      if (project.description?.isNotEmpty == true)
        'Description: ${project.description}',
      'Help the user plan, unblock, and advance this project. Be concise '
          'and concrete; suggest next actions they can take in this app.',
    ].join('\n');
  }

  /// Builds the Anthropic message list from stored history plus a new prompt.
  static List<Map<String, String>> buildMessages(
      List<ChatMessage> history, String newPrompt) {
    final messages = <Map<String, String>>[];
    for (final message in history) {
      if (message.content.isNotEmpty) {
        messages.add({'role': 'user', 'content': message.content});
      }
      if (message.botResponse?.isNotEmpty == true) {
        messages.add({'role': 'assistant', 'content': message.botResponse!});
      }
    }
    messages.add({'role': 'user', 'content': newPrompt});
    return messages;
  }
}

final projectChatRepositoryProvider = Provider<ProjectChatRepository?>((ref) {
  final api = ref.watch(apiClientProvider);
  return api == null ? null : ProjectChatRepository(api);
});
