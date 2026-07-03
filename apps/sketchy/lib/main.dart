import 'package:flutter/material.dart';

void main() => runApp(const SketchyApp());

class SketchyApp extends StatelessWidget {
  const SketchyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sketchy',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Sketchy')),
        body: const Center(child: Text('Sketchy — scaffolded by AppMaker')),
      ),
    );
  }
}
