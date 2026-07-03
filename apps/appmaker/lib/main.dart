import 'package:flutter/material.dart';

void main() => runApp(const AppmakerApp());

class AppmakerApp extends StatelessWidget {
  const AppmakerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AppMaker',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('AppMaker')),
        body: const Center(child: Text('AppMaker — scaffolded by AppMaker')),
      ),
    );
  }
}
