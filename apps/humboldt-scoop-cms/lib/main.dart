import 'package:flutter/material.dart';

void main() => runApp(const HumboldtScoopCmsApp());

class HumboldtScoopCmsApp extends StatelessWidget {
  const HumboldtScoopCmsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Humboldt Scoop Solutions',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Humboldt Scoop Solutions')),
        body: const Center(child: Text('Humboldt Scoop Solutions — scaffolded by AppMaker')),
      ),
    );
  }
}
