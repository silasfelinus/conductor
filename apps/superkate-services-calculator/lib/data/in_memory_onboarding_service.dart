library;

import 'onboarding_service.dart';

class InMemoryOnboardingService implements OnboardingService {
  InMemoryOnboardingService({bool completed = false}) : _completed = completed;

  bool _completed;

  @override
  Future<bool> hasCompletedOnboarding() async => _completed;

  @override
  Future<void> completeOnboarding() async {
    _completed = true;
  }

  @override
  Future<void> resetOnboarding() async {
    _completed = false;
  }
}
