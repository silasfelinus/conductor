import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../projects/project_models.dart';
import '../projects/projects_repository.dart';
import 'chat_models.dart';
import 'chat_repository.dart';

class ProjectChatScreen extends ConsumerStatefulWidget {
  const ProjectChatScreen({super.key, required this.projectId});

  final int projectId;

  @override
  ConsumerState<ProjectChatScreen> createState() => _ProjectChatScreenState();
}

class _ProjectChatScreenState extends ConsumerState<ProjectChatScreen> {
  final _input = TextEditingController();
  final _scroll = ScrollController();
  List<ChatMessage> _messages = [];
  bool _loading = true;
  bool _streaming = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  @override
  void dispose() {
    _input.dispose();
    _scroll.dispose();
    super.dispose();
  }

  Project? get _project => (ref
          .read(projectsProvider)
          .valueOrNull ??
      [])
      .where((p) => p.id == widget.projectId)
      .firstOrNull;

  Future<void> _loadHistory() async {
    final repo = ref.read(projectChatRepositoryProvider);
    if (repo == null) {
      setState(() => _loading = false);
      return;
    }
    try {
      final history = await repo.history(widget.projectId);
      if (mounted) setState(() => _messages = history);
    } catch (e) {
      if (mounted) setState(() => _error = '$e');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _send() async {
    final text = _input.text.trim();
    final repo = ref.read(projectChatRepositoryProvider);
    final project = _project;
    if (text.isEmpty || _streaming || repo == null || project == null) return;

    _input.clear();
    setState(() {
      _error = null;
      _streaming = true;
    });

    try {
      final priorHistory = [..._messages];
      final row = await repo.createUserMessage(widget.projectId, text);
      setState(() => _messages = [..._messages, row]);
      _scrollToEnd();

      final buffer = StringBuffer();
      await for (final token in repo.streamReply(
        messages: ProjectChatRepository.buildMessages(priorHistory, text),
        system: ProjectChatRepository.systemPromptFor(project),
        chatId: row.id,
      )) {
        buffer.write(token);
        if (!mounted) return;
        setState(() {
          _messages = [
            ..._messages.sublist(0, _messages.length - 1),
            row.copyWith(botResponse: buffer.toString()),
          ];
        });
        _scrollToEnd();
      }
      await repo.saveBotResponse(row.id, buffer.toString());
    } catch (e) {
      if (mounted) setState(() => _error = '$e');
    } finally {
      if (mounted) setState(() => _streaming = false);
    }
  }

  void _scrollToEnd() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scroll.hasClients) {
        _scroll.jumpTo(_scroll.position.maxScrollExtent);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final project = _project;
    return Scaffold(
      appBar: AppBar(title: Text(project?.title ?? 'Project chat')),
      body: Column(
        children: [
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : ListView(
                    controller: _scroll,
                    padding: const EdgeInsets.all(16),
                    children: [
                      if (_messages.isEmpty)
                        const Padding(
                          padding: EdgeInsets.only(top: 48),
                          child: Center(
                              child: Text(
                                  'Ask the assistant anything about this project.')),
                        ),
                      for (final message in _messages) ...[
                        if (message.content.isNotEmpty)
                          _Bubble(text: message.content, fromUser: true),
                        if (message.botResponse?.isNotEmpty == true)
                          _Bubble(text: message.botResponse!, fromUser: false),
                      ],
                      if (_streaming &&
                          (_messages.isEmpty ||
                              _messages.last.botResponse?.isNotEmpty != true))
                        const Padding(
                          padding: EdgeInsets.all(8),
                          child: Align(
                            alignment: Alignment.centerLeft,
                            child: SizedBox(
                                width: 20,
                                height: 20,
                                child:
                                    CircularProgressIndicator(strokeWidth: 2)),
                          ),
                        ),
                    ],
                  ),
          ),
          if (_error != null)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Text(_error!,
                  style: TextStyle(color: Theme.of(context).colorScheme.error)),
            ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _input,
                      decoration: const InputDecoration(
                          hintText: 'Message the project assistant'),
                      onSubmitted: (_) => _send(),
                      enabled: !_streaming,
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton.filled(
                    onPressed: _streaming ? null : _send,
                    icon: const Icon(Icons.send),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _Bubble extends StatelessWidget {
  const _Bubble({required this.text, required this.fromUser});

  final String text;
  final bool fromUser;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Align(
      alignment: fromUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.8),
        decoration: BoxDecoration(
          color: fromUser ? scheme.primaryContainer : scheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(16),
        ),
        child: SelectableText(text),
      ),
    );
  }
}
