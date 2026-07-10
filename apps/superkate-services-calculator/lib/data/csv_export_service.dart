library;

import 'dart:io';

import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

import '../domain/csv_export.dart';
import '../models/appointment.dart';
import '../models/customer.dart';

class CsvExportResult {
  const CsvExportResult({
    required this.customersPath,
    required this.appointmentsPath,
  });

  final String customersPath;
  final String appointmentsPath;
}

abstract class CsvExportService {
  Future<CsvExportResult> exportAll({
    required List<Customer> customers,
    required List<Appointment> appointments,
  });
}

class FileCsvExportService implements CsvExportService {
  FileCsvExportService({Directory? directory, DateTime Function()? clock})
      : _directory = directory,
        _clock = clock ?? (() => DateTime.now());

  final Directory? _directory;
  final DateTime Function() _clock;

  Future<Directory> _exportDir() async {
    if (_directory != null) return _directory;
    final docs = await getApplicationDocumentsDirectory();
    return Directory(p.join(docs.path, 'superkate_exports'));
  }

  @override
  Future<CsvExportResult> exportAll({
    required List<Customer> customers,
    required List<Appointment> appointments,
  }) async {
    final dir = await _exportDir();
    await dir.create(recursive: true);
    final stamp = _clock().toIso8601String().substring(0, 10);

    final customersFile = File(p.join(dir.path, 'superkate-customers-$stamp.csv'));
    final appointmentsFile =
        File(p.join(dir.path, 'superkate-appointments-$stamp.csv'));

    await customersFile.writeAsString(customersToCsv(customers), flush: true);
    await appointmentsFile.writeAsString(
      appointmentsToCsv(appointments),
      flush: true,
    );

    final result = CsvExportResult(
      customersPath: customersFile.path,
      appointmentsPath: appointmentsFile.path,
    );

    if (_directory == null) {
      await SharePlus.instance.share(
        ShareParams(
          subject: 'Superkate customer and appointment exports',
          text: 'Two local CSV exports from Superkate Services Calculator.',
          files: [
            XFile(result.customersPath, mimeType: 'text/csv'),
            XFile(result.appointmentsPath, mimeType: 'text/csv'),
          ],
        ),
      );
    }

    return result;
  }
}

class InMemoryCsvExportService implements CsvExportService {
  String? lastCustomersCsv;
  String? lastAppointmentsCsv;
  int exportCount = 0;

  @override
  Future<CsvExportResult> exportAll({
    required List<Customer> customers,
    required List<Appointment> appointments,
  }) async {
    exportCount++;
    lastCustomersCsv = customersToCsv(customers);
    lastAppointmentsCsv = appointmentsToCsv(appointments);
    return const CsvExportResult(
      customersPath: '/fake/superkate-customers.csv',
      appointmentsPath: '/fake/superkate-appointments.csv',
    );
  }
}
