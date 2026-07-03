import 'package:flutter/material.dart';

void main() => runApp(const KindRobotsApp());

class KindRobotsApp extends StatelessWidget {
  const KindRobotsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Kind Robots',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Kind Robots')),
        body: const Center(child: Text('Kind Robots — scaffolded by AppMaker')),
      ),
    );
  }
}
