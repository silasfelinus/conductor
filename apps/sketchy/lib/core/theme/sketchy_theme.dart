import 'package:flutter/material.dart';

/// Sketchy's shared theme: friendly, minimalist, encouraging (per
/// PRODUCT-SPEC.md's product-direction note) -- a warm coral seed rather than
/// a stark or clinical palette.
ThemeData buildSketchyTheme() {
  return ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFFFF7A59)),
    useMaterial3: true,
  );
}
