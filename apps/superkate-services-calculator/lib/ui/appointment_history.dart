import 'package:flutter/material.dart';

import '../data/persistence_service.dart';
import '../domain/money.dart';
import '../domain/receipt_email.dart';
import '../models/appointment.dart';
import '../models/customer.dart';
import 'receipt_email_launcher.dart';

const _cardColor = Color(0xFF171224);
const _cardBorder = Color(0xFF3B2A5B);
const _softText = Color(0xFFCAC2DF);

Future<bool> _launchReceiptEmail(Uri uri) =>
    const PlatformReceiptEmailLauncher().launch(uri);

class AppointmentHistory extends StatefulWidget {
  const AppointmentHistory({
    super.key,
    required this.service,
    this.refreshToken = 0,
    this.launchReceiptEmail,
  });

  final PersistenceService service;
  final int refreshToken;
  final ReceiptEmailLauncher? launchReceiptEmail;

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
    final launcher = widget.launchReceiptEmail ?? _launchReceiptEmail;

    return ListView(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
      children: [
        Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 720),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const _HistoryIntroCard(),
                const SizedBox(height: 16),
                _FilterCard(
                  clientNameQuery: _clientNameQuery,
                  from: _from,
                  to: _to,
                  onPickFromDate: _pickFromDate,
                  onPickToDate: _pickToDate,
                  onClearFilters: _clearFilters,
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
                        color: _cardColor,
                        elevation: 0,
                        shape: const RoundedRectangleBorder(
                          borderRadius: BorderRadius.all(Radius.circular(24)),
                          side: BorderSide(color: _cardBorder),
                        ),
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
                          _AppointmentResultCard(
                            appointment: appointment,
                            service: widget.service,
                            launchReceiptEmail: launcher,
                          ),
                          const SizedBox(height: 12),
                        ],
                      ],
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  bool get _hasFilters =>
      _clientNameQuery.text.trim().isNotEmpty || _from != null || _to != null;

  static String _formatDate(DateTime date) => formatReceiptDate(date);
}

class _HistoryIntroCard extends StatelessWidget {
  const _HistoryIntroCard();

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF201633),
      elevation: 0,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(28)),
        side: BorderSide(color: _cardBorder),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          children: [
            Container(
              width: 54,
              height: 54,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: [Color(0xFF14B8A6), Color(0xFF8B5CF6)],
                ),
              ),
              child: const Icon(Icons.history, color: Color(0xFF0B0712)),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Appointment history',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.w800,
                        ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Find a visit, review the total, and prepare a polished receipt.',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: _softText,
                        ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _FilterCard extends StatelessWidget {
  const _FilterCard({
    required this.clientNameQuery,
    required this.from,
    required this.to,
    required this.onPickFromDate,
    required this.onPickToDate,
    required this.onClearFilters,
  });

  final TextEditingController clientNameQuery;
  final DateTime? from;
  final DateTime? to;
  final VoidCallback onPickFromDate;
  final VoidCallback onPickToDate;
  final VoidCallback onClearFilters;

  @override
  Widget build(BuildContext context) {
    return Card(
      color: _cardColor,
      elevation: 0,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(24)),
        side: BorderSide(color: _cardBorder),
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: clientNameQuery,
              textCapitalization: TextCapitalization.words,
              decoration: const InputDecoration(
                labelText: 'Search by client name',
                prefixIcon: Icon(Icons.search),
              ),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                OutlinedButton.icon(
                  onPressed: onPickFromDate,
                  icon: const Icon(Icons.event_available_outlined),
                  label: Text(from == null
                      ? 'From any date'
                      : 'From ${_AppointmentHistoryState._formatDate(from!)}'),
                ),
                OutlinedButton.icon(
                  onPressed: onPickToDate,
                  icon: const Icon(Icons.event_outlined),
                  label: Text(to == null
                      ? 'To any date'
                      : 'To ${_AppointmentHistoryState._formatDate(to!)}'),
                ),
                TextButton.icon(
                  onPressed: onClearFilters,
                  icon: const Icon(Icons.filter_alt_off_outlined),
                  label: const Text('Clear filters'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _AppointmentResultCard extends StatelessWidget {
  const _AppointmentResultCard({
    required this.appointment,
    required this.service,
    required this.launchReceiptEmail,
  });

  final Appointment appointment;
  final PersistenceService service;
  final ReceiptEmailLauncher launchReceiptEmail;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;

    return Card(
      color: _cardColor,
      elevation: 0,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(24)),
        side: BorderSide(color: _cardBorder),
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        appointment.clientNameSnapshot,
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.w800,
                            ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        formatReceiptDate(appointment.appointmentDate),
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              color: _softText,
                            ),
                      ),
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
            const SizedBox(height: 14),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                _DetailPill(
                  icon: Icons.schedule_outlined,
                  label: formatDurationMinutes(appointment.timeSpentMinutes),
                ),
                _DetailPill(
                  icon: Icons.payments_outlined,
                  label: '${formatCents(appointment.hourlyRateCents)}/hour',
                ),
                _DetailPill(
                  icon: Icons.inventory_2_outlined,
                  label: 'Products ${formatCents(appointment.productCostCents)}',
                ),
              ],
            ),
            const SizedBox(height: 14),
            Align(
              alignment: Alignment.centerRight,
              child: FilledButton.tonalIcon(
                onPressed: () => _prepareReceipt(context),
                icon: const Icon(Icons.mail_outline),
                label: const Text('Prepare receipt'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _prepareReceipt(BuildContext context) async {
    Customer? customer;
    if (appointment.customerId != null) {
      customer = await service.getCustomer(appointment.customerId!);
    }

    final draft = buildReceiptEmail(
      appointment: appointment,
      customer: customer,
    );

    var opened = false;
    try {
      opened = await launchReceiptEmail(draft.mailtoUri);
    } catch (_) {
      opened = false;
    }

    if (!context.mounted) return;
    if (!opened) _showReceiptFallback(context, draft);
  }

  void _showReceiptFallback(BuildContext context, ReceiptEmailDraft draft) {
    showDialog<void>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Receipt ready'),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'Email composer was not available. Copy this receipt instead.',
              ),
              const SizedBox(height: 16),
              SelectableText('${draft.subject}\n\n${draft.body}'),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }
}

class _DetailPill extends StatelessWidget {
  const _DetailPill({required this.icon, required this.label});

  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFF201633),
        borderRadius: const BorderRadius.all(Radius.circular(999)),
        border: Border.all(color: const Color(0xFF3B2A5B)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: colors.secondary),
          const SizedBox(width: 6),
          Text(
            label,
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: _softText,
                  fontWeight: FontWeight.w600,
                ),
          ),
        ],
      ),
    );
  }
}
