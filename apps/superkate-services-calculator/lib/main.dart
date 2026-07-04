import 'package:flutter/material.dart';

void main() => runApp(const SuperkateServicesCalculatorApp());

class SuperkateServicesCalculatorApp extends StatelessWidget {
  const SuperkateServicesCalculatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    const purple = Color(0xFF8B5CF6);
    const teal = Color(0xFF14B8A6);
    const surface = Color(0xFF171224);

    return MaterialApp(
      title: 'Superkate Services Calculator',
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: purple,
          brightness: Brightness.dark,
          primary: purple,
          secondary: teal,
          surface: surface,
        ),
        scaffoldBackgroundColor: const Color(0xFF0B0712),
        useMaterial3: true,
      ),
      home: const SuperkateHomePage(),
    );
  }
}

class SuperkateHomePage extends StatelessWidget {
  const SuperkateHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Superkate Services Calculator'),
        backgroundColor: Colors.transparent,
        foregroundColor: colorScheme.onSurface,
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Text(
              'Client appointment math without the salon brain fog.',
              style: textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            Text(
              'Hourly rate × time spent + product cost = appointment total',
              style: textTheme.bodyLarge?.copyWith(color: colorScheme.secondary),
            ),
            const SizedBox(height: 24),
            const _FeatureCard(
              title: 'Appointment calculator',
              body: 'Enter client name, appointment date, hourly rate, time spent, and product cost.',
            ),
            const _FeatureCard(
              title: 'Private client database',
              body: 'Store appointment totals and search by client name or date.',
            ),
            const _FeatureCard(
              title: 'Receipt email composer',
              body: 'Generate a client receipt with the formula and total ready to send.',
            ),
          ],
        ),
      ),
    );
  }
}

class _FeatureCard extends StatelessWidget {
  const _FeatureCard({required this.title, required this.body});

  final String title;
  final String body;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Card(
      margin: const EdgeInsets.only(bottom: 14),
      color: colorScheme.surface,
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: colorScheme.primary,
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 8),
            Text(body),
          ],
        ),
      ),
    );
  }
}
