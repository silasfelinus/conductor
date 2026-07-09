library;

abstract class OnboardingService {
  Future<bool> hasCompletedOnboarding();
  Future<void> completeOnboarding();
  Future<void> resetOnboarding();
}
