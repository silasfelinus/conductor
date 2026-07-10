library;

import 'dart:io';

import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

import '../domain/csv_export.dart';
import '../models/appointment.dart';
import '../models/customer.dart';

/// Result of a completed export: where the two CSV files landed.
class CsvExportResult {
  const CsvExportResult({
    required this.customersPath,
    required this.appointmentsPath,
  });

  final String customersPath;
  final String appointmentsPath;
}

/// Local, user-initiated CSV export (SPEC.md). Nothing leaves the device:
/// files are written to app documents storage and the paths are shown to the
/// user. No analytics, no upload, no background exports.
abstract class CsvExportService {
  Future<CsvExportResult> exportAll({
    required List<Customer> customers,
    required List<Appointment> appointments,
  });
}

/// Writes `superkate-customers-<date>.csv` and
/// `superkate-appointments-<date>.csv` into an exports folder under the
/// app's documents directory.
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
    await appointmentsFile.writeAsString(appointmentsToCsv(appointments),
        flush: true);

    return CsvExportResult(
      customersPath: customersFile.path,
      appointmentsPath: appointmentsFile.path,
    );
  }
}

/// Test double that records what would have been written.
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
