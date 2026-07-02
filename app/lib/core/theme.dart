import 'package:flutter/material.dart';

const _seed = Color(0xFF6750A4);

ThemeData conductorTheme(Brightness brightness) {
  final scheme = ColorScheme.fromSeed(seedColor: _seed, brightness: brightness);
  return ThemeData(
    colorScheme: scheme,
    useMaterial3: true,
    cardTheme: const CardTheme(clipBehavior: Clip.antiAlias),
    inputDecorationTheme: const InputDecorationTheme(border: OutlineInputBorder()),
  );
}
