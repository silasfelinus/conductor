library;

import 'dart:io';

import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

import 'onboarding_service.dart';

class FileOnboardingService implements OnboardingService {
  const FileOnboardingService._(this._file);

  static Future<FileOnboardingService> open({String? filename}) async {
    final supportDir = await getApplicationSupportDirectory();
    await supportDir.create(recursive: true);
    return FileOnboardingService._(
      File(p.join(supportDir.path, filename ?? 'superkate_onboarding.txt')),
    );
  }

  final File _file;

  @override
  Future<bool> hasCompletedOnboarding() async {
    try {
      return (await _file.readAsString()).trim() == 'completed';
    } on FileSystemException {
      return false;
    }
  }

  @override
  Future<void> completeOnboarding() async {
    await _file.parent.create(recursive: true);
    await _file.writeAsString('completed\n', flush: true);
  }

  @override
  Future<void> resetOnboarding() async {
    if (await _file.exists()) {
      await _file.delete();
    }
  }
}
