import 'package:flutter/material.dart';

import '../data/persistence_service.dart';
import '../domain/money.dart';
import '../models/appointment.dart';

class AppointmentHistory extends StatefulWidget {
  const AppointmentHistory({
    super.key,
    required this.service,
    this.refreshToken = 0,
  });

  final PersistenceService service;
  final int refreshToken;

  @override
  State<AppointmentHistory> createState() => _AppointmentHistoryState();
}

class _AppointmentHistoryState extends State<AppointmentHistory> {
  final _clientNameQuery = TextEditingController();

  DateTime? _from;
  DateTime? _to;
  late Future<List<Appointment>> _appointments;

  @override
  void initState() {
    super.initState();
    _clientNameQuery.addListener(_reload);
    _appointments = _searchAppointments();
  }

  @override
  void didUpdateWidget(AppointmentHistory oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.service != widget.service ||
        oldWidget.refreshToken != widget.refreshToken) {
      _reload();
    }
  }

  @override
  void dispose() {
    _clientNameQuery.dispose();
    super.dispose();
  }

  Future<List<Appointment>> _searchAppointments() {
    return widget.service.listAppointments(
      AppointmentFilter(
        clientNameQuery: _clientNameQuery.text,
        appointmentDateFrom: _from,
        appointmentDateTo: _to,
      ),
    );
  }

  void _reload() {
    if (!mounted) return;
    setState(() {
      _appointments = _searchAppointments();
    });
  }

  Future<void> _pickFromDate() => _pickDate(
        initialDate: _from ?? _to ?? DateTime.now(),
        onPicked: (date) {
          _from = date;
          if (_to != null && _to!.isBefore(date)) _to = date;
        },
      );

  Future<void> _pickToDate() => _pickDate(
        initialDate: _to ?? _from ?? DateTime.now(),
        onPicked: (date) {
          _to = date;
          if (_from != null && _from!.isAfter(date)) _from = date;
        },
      );

  Future<void> _pickDate({
    required DateTime initialDate,
    required ValueChanged<DateTime> onPicked,
  }) async {
    final picked = await showDatePicker(
      context: context,
      initialDate: initialDate,
      firstDate: DateTime(2020),
      lastDate: DateTime(2100),
    );
    if (picked == null) return;
    onPicked(DateTime(picked.year, picked.month, picked.day));
    _reload();
  }

  void _clearFilters() {
    _clientNameQuery.clear();
    setState(() {
      _from = null;
      _to = null;
      _appointments = _searchAppointments();
    });
  }

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;

    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Text(
          'Appointment history',
          style: Theme.of(context)
              .textTheme
              .headlineSmall
              ?.copyWith(fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _clientNameQuery,
          textCapitalization: TextCapitalization.words,
          decoration: const InputDecoration(
            labelText: 'Search by client name',
            prefixIcon: Icon(Icons.search),
            border: OutlineInputBorder(),
          ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            OutlinedButton.icon(
              onPressed: _pickFromDate,
              icon: const Icon(Icons.event_available_outlined),
              label: Text(_from == null
                  ? 'From any date'
                  : 'From ${_formatDate(_from!)}'),
            ),
            OutlinedButton.icon(
              onPressed: _pickToDate,
              icon: const Icon(Icons.event_outlined),
              label:
                  Text(_to == null ? 'To any date' : 'To ${_formatDate(_to!)}'),
            ),
            TextButton.icon(
              onPressed: _clearFilters,
              icon: const Icon(Icons.filter_alt_off_outlined),
              label: const Text('Clear filters'),
            ),
          ],
        ),
        const SizedBox(height: 20),
        FutureBuilder<List<Appointment>>(
          future: _appointments,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snapshot.hasError) {
              return Text(
                'Could not load appointments. Please try again.',
                style: TextStyle(color: colors.error),
              );
            }

            final appointments = snapshot.data ?? const <Appointment>[];
            if (appointments.isEmpty) {
              return Card(
                child: Padding(
                  padding: const EdgeInsets.all(18),
                  child: Text(
                    _hasFilters
                        ? 'No appointments match those filters.'
                        : 'No saved appointments yet.',
                  ),
                ),
              );
            }

            return Column(
              children: [
                for (final appointment in appointments) ...[
                  _AppointmentResultCard(appointment: appointment),
                  const SizedBox(height: 12),
                ],
              ],
            );
          },
        ),
      ],
    );
  }

  bool get _hasFilters =>
      _clientNameQuery.text.trim().isNotEmpty || _from != null || _to != null;

  static String _formatDate(DateTime date) =>
      '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
}

class _AppointmentResultCard extends StatelessWidget {
  const _AppointmentResultCard({required this.appointment});

  final Appointment appointment;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    appointment.clientNameSnapshot,
                    style: Theme.of(context)
                        .textTheme
                        .titleMedium
                        ?.copyWith(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(_formatDate(appointment.appointmentDate)),
                ],
              ),
            ),
            Text(
              formatCents(appointment.appointmentTotalCents),
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    color: colors.secondary,
                    fontWeight: FontWeight.bold,
                  ),
            ),
          ],
        ),
      ),
    );
  }

  static String _formatDate(DateTime date) =>
      '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
}
