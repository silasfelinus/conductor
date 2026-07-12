import 'package:conductor_app/features/chat/chat_models.dart';
import 'package:conductor_app/features/chat/chat_repository.dart';
import 'package:conductor_app/features/projects/project_models.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('ProjectChatRepository', () {
    test('buildMessages interleaves history and appends the new prompt', () {
      final history = [
        const ChatMessage(id: 1, content: 'hi', botResponse: 'hello!'),
        const ChatMessage(id: 2, content: 'status?'), // reply never generated
      ];
      final messages =
          ProjectChatRepository.buildMessages(history, 'what next?');
      expect(messages, [
        {'role': 'user', 'content': 'hi'},
        {'role': 'assistant', 'content': 'hello!'},
        {'role': 'user', 'content': 'status?'},
        {'role': 'user', 'content': 'what next?'},
      ]);
    });

    test('systemPromptFor embeds project context', () {
      final project = Project.fromJson({
        'id': 1,
        'slug': 'x',
        'title': 'X',
        'goal': 'ship',
      });
      final prompt = ProjectChatRepository.systemPromptFor(project);
      expect(prompt, contains('project assistant for "X"'));
      expect(prompt, contains('Goal: ship'));
    });

    test('channel name matches the kind_robots workspace convention', () {
      expect(ProjectChatRepository.channelFor(42), 'dream-42-assistant');
    });
  });
}
