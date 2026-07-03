import 'package:flutter/material.dart';

void main() => runApp(const StorymakerApp());

class StorymakerApp extends StatelessWidget {
  const StorymakerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Storymaker',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Storymaker')),
        body: const Center(child: Text('Storymaker — scaffolded by AppMaker')),
      ),
    );
  }
}
