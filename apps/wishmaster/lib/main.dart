import 'package:flutter/material.dart';

void main() => runApp(const WishmasterApp());

class WishmasterApp extends StatelessWidget {
  const WishmasterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Wishmaster',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Wishmaster')),
        body: const Center(child: Text('Wishmaster — scaffolded by AppMaker')),
      ),
    );
  }
}
