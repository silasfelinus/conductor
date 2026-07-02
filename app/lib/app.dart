import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'core/theme.dart';
import 'features/agent_ops/agent_ops_repository.dart';
import 'features/agent_ops/approvals_screen.dart';
import 'features/auth/auth_controller.dart';
import 'features/auth/login_screen.dart';
import 'features/onboarding/server_picker_screen.dart';
import 'features/projects/dashboard_screen.dart';
import 'features/projects/project_detail_screen.dart';
import 'features/settings/settings_screen.dart';
import 'features/todos/todos_repository.dart';
import 'features/todos/todos_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final config = ref.watch(serverConfigProvider);
  final auth = ref.watch(authControllerProvider);

  return GoRouter(
    initialLocation: '/projects',
    redirect: (context, state) {
      if (config == null) return '/welcome';
      final authState = auth.valueOrNull;
      final needsLogin = !config.isLocal && authState is! SignedIn;
      if (needsLogin && auth.isLoading) return null;
      if (needsLogin) return '/login';
      if (state.matchedLocation == '/welcome' ||
          state.matchedLocation == '/login') {
        return '/projects';
      }
      return null;
    },
    routes: [
      GoRoute(
          path: '/welcome',
          builder: (context, state) => const ServerPickerScreen()),
      GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
      ShellRoute(
        builder: (context, state, child) => _AppShell(child: child),
        routes: [
          GoRoute(
              path: '/projects',
              builder: (context, state) => const DashboardScreen()),
          GoRoute(
            path: '/projects/:id',
            builder: (context, state) => ProjectDetailScreen(
                projectId:
                    int.tryParse(state.pathParameters['id'] ?? '') ?? 0),
          ),
          GoRoute(
              path: '/todos', builder: (context, state) => const TodosScreen()),
          GoRoute(
              path: '/approvals',
              builder: (context, state) => const ApprovalsScreen()),
          GoRoute(
              path: '/settings',
              builder: (context, state) => const SettingsScreen()),
        ],
      ),
    ],
  );
});

class ConductorApp extends ConsumerWidget {
  const ConductorApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    return MaterialApp.router(
      title: 'Conductor',
      theme: conductorTheme(Brightness.light),
      darkTheme: conductorTheme(Brightness.dark),
      routerConfig: router,
    );
  }
}

class _AppShell extends ConsumerStatefulWidget {
  const _AppShell({required this.child});

  final Widget child;

  @override
  ConsumerState<_AppShell> createState() => _AppShellState();
}

class _AppShellState extends ConsumerState<_AppShell> {
  Timer? _refreshTimer;

  @override
  void initState() {
    super.initState();
    // Foreground polling (MVP notification strategy): re-fetch on an interval
    // so the Approvals badge stays honest without push infrastructure.
    _refreshTimer = Timer.periodic(const Duration(minutes: 5), (_) {
      ref.invalidate(agentOpsDataProvider);
      ref.invalidate(todosControllerProvider);
    });
  }

  @override
  void dispose() {
    _refreshTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    final user = ref.watch(currentUserProvider);
    final approvalsCount =
        ref.watch(agentOpsDataProvider).valueOrNull?.approvals.length ?? 0;
    final destinations = [
      const NavigationDestination(
          icon: Icon(Icons.folder_outlined),
          selectedIcon: Icon(Icons.folder),
          label: 'Projects'),
      const NavigationDestination(
          icon: Icon(Icons.check_circle_outline),
          selectedIcon: Icon(Icons.check_circle),
          label: 'Todos'),
      if (user?.isAdmin == true)
        NavigationDestination(
            icon: Badge.count(
              count: approvalsCount,
              isLabelVisible: approvalsCount > 0,
              child: const Icon(Icons.approval_outlined),
            ),
            selectedIcon: const Icon(Icons.approval),
            label: 'Approvals'),
      const NavigationDestination(
          icon: Icon(Icons.settings_outlined),
          selectedIcon: Icon(Icons.settings),
          label: 'Settings'),
    ];
    final paths = [
      '/projects',
      '/todos',
      if (user?.isAdmin == true) '/approvals',
      '/settings',
    ];
    var selected = paths.indexWhere((p) => location.startsWith(p));
    if (selected < 0) selected = 0;

    return Scaffold(
      body: widget.child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: selected,
        destinations: destinations,
        onDestinationSelected: (i) => context.go(paths[i]),
      ),
    );
  }
}
