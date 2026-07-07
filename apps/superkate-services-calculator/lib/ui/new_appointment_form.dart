import 'package:flutter/material.dart';

import '../data/persistence_service.dart';
import '../domain/money.dart';
import '../domain/validation.dart';
import '../models/appointment.dart';

/// New Appointment / Calculator screen (roadmap t-004).
///
/// Collects client name, appointment date, hourly rate, time spent (hours +
/// minutes with preset chips), and optional product cost (defaults to $0), and
/// shows the **live total** as `hourly rate × time spent + product cost`
/// recomputed on every keystroke. Saving delegates to a [PersistenceService];
/// the total is always recalculated at save time and never trusted from the UI.
class NewAppointmentForm extends StatefulWidget {
  const NewAppointmentForm({
    super.key,
    required this.service,
    this.onSaved,
  });

  final PersistenceService service;
  final ValueChanged<Appointment>? onSaved;

  @override
  State<NewAppointmentForm> createState() => _NewAppointmentFormState();
}

/// Preset time chips (SPEC.md: "hours/minutes with preset chips").
const _timePresets = <({String label, int minutes})>[
  (label: '30m', minutes: 30),
  (label: '45m', minutes: 45),
  (label: '1h', minutes: 60),
  (label: '1h 30m', minutes: 90),
  (label: '2h', minutes: 120),
];

class _NewAppointmentFormState extends State<NewAppointmentForm> {
  final _clientName = TextEditingController();
  final _hourlyRate = TextEditingController();
  final _productCost = TextEditingController();

  DateTime _appointmentDate = _today();
  int _hours = 1;
  int _minutes = 0;

  bool _saving = false;
  String? _error;

  static DateTime _today() {
    final now = DateTime.now();
    return DateTime(now.year, now.month, now.day);
  }

  @override
  void initState() {
    super.initState();
    for (final c in [_clientName, _hourlyRate, _productCost]) {
      c.addListener(() => setState(() {}));
    }
  }

  @override
  void dispose() {
    _clientName.dispose();
    _hourlyRate.dispose();
    _productCost.dispose();
    super.dispose();
  }

  int get _timeSpentMinutes => toMinutes(hours: _hours, minutes: _minutes);

  /// Live total in cents, or `null` when inputs aren't yet a valid amount.
  int? get _liveTotalCents {
    final rateCents = parseDollarsToCents(_hourlyRate.text);
    final productCents = parseDollarsToCents(_productCost.text);
    if (rateCents == null || productCents == null) return null;
    if (_timeSpentMinutes <= 0) return null;
    return calculateAppointmentTotalCents(
      hourlyRateCents: rateCents,
      timeSpentMinutes: _timeSpentMinutes,
      productCostCents: productCents,
    );
  }

  Future<void> _save() async {
    final rateCents = parseDollarsToCents(_hourlyRate.text);
    final productCents = parseDollarsToCents(_productCost.text);
    if (rateCents == null) {
      setState(() => _error = 'Hourly rate must be a valid amount.');
      return;
    }
    if (productCents == null) {
      setState(() => _error = 'Product cost must be a valid amount.');
      return;
    }

    setState(() {
      _saving = true;
      _error = null;
    });

    try {
      final appointment = await widget.service.createAppointment(
        CreateAppointmentInput(
          clientName: _clientName.text,
          appointmentDate: _appointmentDate,
          hourlyRateCents: rateCents,
          timeSpentMinutes: _timeSpentMinutes,
          productCostCents: productCents,
        ),
      );
      if (!mounted) return;
      widget.onSaved?.call(appointment);
      _resetForm();
    } on ValidationException catch (e) {
      if (mounted) setState(() => _error = e.message);
    } catch (_) {
      // Never surface raw errors / customer data (SPEC.md security baseline).
      if (mounted) {
        setState(() => _error = 'Could not save the appointment. Please try again.');
      }
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  void _resetForm() {
    _clientName.clear();
    _hourlyRate.clear();
    _productCost.clear();
    setState(() {
      _appointmentDate = _today();
      _hours = 1;
      _minutes = 0;
    });
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _appointmentDate,
      firstDate: DateTime(2020),
      lastDate: DateTime(2100),
    );
    if (picked != null) setState(() => _appointmentDate = picked);
  }

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final totalCents = _liveTotalCents;

    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Text('New appointment',
            style: Theme.of(context)
                .textTheme
                .headlineSmall
                ?.copyWith(fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        TextField(
          controller: _clientName,
          textCapitalization: TextCapitalization.words,
          decoration: const InputDecoration(
            labelText: 'Client name',
            border: OutlineInputBorder(),
          ),
        ),
        const SizedBox(height: 16),
        _DateField(date: _appointmentDate, onTap: _pickDate),
        const SizedBox(height: 16),
        TextField(
          controller: _hourlyRate,
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
          decoration: const InputDecoration(
            labelText: 'Hourly rate',
            prefixText: '\$ ',
            border: OutlineInputBorder(),
          ),
        ),
        const SizedBox(height: 20),
        Text('Time spent', style: Theme.of(context).textTheme.labelLarge),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          children: [
            for (final preset in _timePresets)
              ChoiceChip(
                label: Text(preset.label),
                selected: _timeSpentMinutes == preset.minutes,
                onSelected: (_) => setState(() {
                  _hours = preset.minutes ~/ 60;
                  _minutes = preset.minutes % 60;
                }),
              ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _Stepper(
                label: 'Hours',
                value: _hours,
                onChanged: (v) => setState(() => _hours = v.clamp(0, 24)),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _Stepper(
                label: 'Minutes',
                value: _minutes,
                step: 5,
                onChanged: (v) => setState(() => _minutes = v.clamp(0, 55)),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _productCost,
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
          decoration: const InputDecoration(
            labelText: 'Product cost (optional)',
            prefixText: '\$ ',
            hintText: '0.00',
            border: OutlineInputBorder(),
          ),
        ),
        const SizedBox(height: 24),
        _TotalCard(
          totalCents: totalCents,
          secondary: colors.secondary,
        ),
        if (_error != null) ...[
          const SizedBox(height: 12),
          Text(_error!, style: TextStyle(color: colors.error)),
        ],
        const SizedBox(height: 16),
        FilledButton.icon(
          onPressed: _saving ? null : _save,
          icon: _saving
              ? const SizedBox(
                  width: 16,
                  height: 16,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Icon(Icons.save_outlined),
          label: Text(_saving ? 'Saving…' : 'Save appointment'),
        ),
      ],
    );
  }
}

class _DateField extends StatelessWidget {
  const _DateField({required this.date, required this.onTap});

  final DateTime date;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final label =
        '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
    return InkWell(
      onTap: onTap,
      child: InputDecorator(
        decoration: const InputDecoration(
          labelText: 'Appointment date',
          border: OutlineInputBorder(),
          suffixIcon: Icon(Icons.calendar_today_outlined),
        ),
        child: Text(label),
      ),
    );
  }
}

class _Stepper extends StatelessWidget {
  const _Stepper({
    required this.label,
    required this.value,
    required this.onChanged,
    this.step = 1,
  });

  final String label;
  final int value;
  final int step;
  final ValueChanged<int> onChanged;

  @override
  Widget build(BuildContext context) {
    return InputDecorator(
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            icon: const Icon(Icons.remove),
            onPressed: () => onChanged(value - step),
          ),
          Text('$value', style: Theme.of(context).textTheme.titleMedium),
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => onChanged(value + step),
          ),
        ],
      ),
    );
  }
}

class _TotalCard extends StatelessWidget {
  const _TotalCard({required this.totalCents, required this.secondary});

  final int? totalCents;
  final Color secondary;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Appointment total',
                style: Theme.of(context).textTheme.labelLarge),
            const SizedBox(height: 4),
            Text(
              totalCents == null ? '—' : formatCents(totalCents!),
              style: Theme.of(context).textTheme.displaySmall?.copyWith(
                    color: secondary,
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 4),
            Text('hourly rate × time spent + product cost',
                style: Theme.of(context).textTheme.bodySmall),
          ],
        ),
      ),
    );
  }
}
