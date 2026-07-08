import 'package:flutter/services.dart';

typedef ReceiptEmailLauncher = Future<bool> Function(Uri uri);

class PlatformReceiptEmailLauncher {
  const PlatformReceiptEmailLauncher();

  static const _channel = MethodChannel(
    'superkate_services_calculator/receipt_email',
  );

  Future<bool> launch(Uri uri) async {
    final opened = await _channel.invokeMethod<bool>(
      'prepareReceiptEmail',
      {'mailtoUri': uri.toString()},
    );
    return opened ?? false;
  }
}
