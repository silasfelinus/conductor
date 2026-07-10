library;

import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:crypto/crypto.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

import 'app_lock_service.dart';

/// Stores the app-lock state as a small JSON file in the app support
/// directory: `{"salt": "<base64>", "hash": "<hex sha256(salt + pin)>"}`.
/// A missing or unreadable file simply means the lock is off.
class FileAppLockService implements AppLockService {
  const FileAppLockService.forFile(this._file);

  static Future<FileAppLockService> open({String? filename}) async {
    final supportDir = await getApplicationSupportDirectory();
    await supportDir.create(recursive: true);
    return FileAppLockService.forFile(
      File(p.join(supportDir.path, filename ?? 'superkate_app_lock.json')),
    );
  }

  final File _file;

  @override
  Future<bool> isEnabled() async => await _readRecord() != null;

  @override
  Future<void> enable(String pin) async {
    ensureValidAppLockPin(pin);
    final saltBytes =
        List<int>.generate(16, (_) => Random.secure().nextInt(256));
    final salt = base64Encode(saltBytes);
    await _file.parent.create(recursive: true);
    await _file.writeAsString(
      jsonEncode({'salt': salt, 'hash': _digest(salt, pin)}),
      flush: true,
    );
  }

  @override
  Future<void> disable() async {
    if (await _file.exists()) {
      await _file.delete();
    }
  }

  @override
  Future<bool> verifyPin(String pin) async {
    final record = await _readRecord();
    if (record == null) return false;
    return _digest(record.salt, pin) == record.hash;
  }

  static String _digest(String salt, String pin) =>
      sha256.convert(utf8.encode('$salt:$pin')).toString();

  Future<({String salt, String hash})?> _readRecord() async {
    try {
      final raw = jsonDecode(await _file.readAsString());
      if (raw is! Map) return null;
      final salt = raw['salt'];
      final hash = raw['hash'];
      if (salt is! String || hash is! String || salt.isEmpty || hash.isEmpty) {
        return null;
      }
      return (salt: salt, hash: hash);
    } on FileSystemException {
      return null;
    } on FormatException {
      return null;
    }
  }
}
