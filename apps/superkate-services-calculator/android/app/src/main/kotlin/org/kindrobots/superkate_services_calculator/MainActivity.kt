package org.kindrobots.superkate_services_calculator

import android.content.ActivityNotFoundException
import android.content.Intent
import android.net.Uri
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            "superkate_services_calculator/receipt_email"
        ).setMethodCallHandler { call, result ->
            if (call.method != "prepareReceiptEmail") {
                result.notImplemented()
                return@setMethodCallHandler
            }

            val mailtoUri = call.argument<String>("mailtoUri")
            if (mailtoUri.isNullOrBlank()) {
                result.success(false)
                return@setMethodCallHandler
            }

            val intent = Intent(Intent.ACTION_SENDTO).apply {
                data = Uri.parse(mailtoUri)
            }

            try {
                startActivity(intent)
                result.success(true)
            } catch (_: ActivityNotFoundException) {
                result.success(false)
            }
        }
    }
}
