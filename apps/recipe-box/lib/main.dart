import 'package:flutter/material.dart';

void main() => runApp(const RecipeBoxApp());

class RecipeBoxApp extends StatelessWidget {
  const RecipeBoxApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Recipe Box',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Recipe Box')),
        body: const Center(child: Text('Recipe Box — scaffolded by AppMaker')),
      ),
    );
  }
}
