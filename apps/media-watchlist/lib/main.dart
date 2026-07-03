import 'package:flutter/material.dart';

void main() => runApp(const MediaWatchlistApp());

class MediaWatchlistApp extends StatelessWidget {
  const MediaWatchlistApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Media Watchlist',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Media Watchlist')),
        body: const Center(child: Text('Media Watchlist — scaffolded by AppMaker')),
      ),
    );
  }
}
