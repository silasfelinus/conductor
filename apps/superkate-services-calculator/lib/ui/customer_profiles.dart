import 'package:flutter/material.dart';

import '../data/persistence_service.dart';
import '../domain/validation.dart';
import '../models/customer.dart';
import 'superkate_style.dart';

class CustomerProfiles extends StatefulWidget {
  const CustomerProfiles({
    super.key,
    required this.service,
    this.onChanged,
  });

  final PersistenceService service;
  final VoidCallback? onChanged;

  @override
  State<CustomerProfiles> createState() => _CustomerProfilesState();
}

class _CustomerProfilesState extends State<CustomerProfiles> {
  final _name = TextEditingController();
  final _email = TextEditingController();

  late Future<List<Customer>> _customers;
  Customer? _editingCustomer;
  bool _saving = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _customers = widget.service.listCustomers();
  }

  @override
  void didUpdateWidget(CustomerProfiles oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.service != widget.service) {
      _reload();
    }
  }

  @override
  void dispose() {
    _name.dispose();
    _email.dispose();
    super.dispose();
  }

  void _reload() {
    if (!mounted) return;
    setState(() => _customers = widget.service.listCustomers());
  }

  void _startEditing(Customer customer) {
    setState(() {
      _editingCustomer = customer;
      _name.text = customer.name;
      _email.text = customer.email ?? '';
      _error = null;
    });
  }

  void _clearForm() {
    setState(() {
      _editingCustomer = null;
      _name.clear();
      _email.clear();
      _error = null;
    });
  }

  Future<void> _saveCustomer() async {
    setState(() {
      _saving = true;
      _error = null;
    });

    try {
      final customer = await widget.service.upsertCustomer(
        UpsertCustomerInput(
          id: _editingCustomer?.id,
          name: _name.text,
          email: _email.text,
        ),
      );
      if (!mounted) return;
      _clearForm();
      _reload();
      widget.onChanged?.call();
      ScaffoldMessenger.of(context)
        ..clearSnackBars()
        ..showSnackBar(
          SnackBar(content: Text('Saved ${customer.name}.')),
        );
    } on ValidationException catch (e) {
      if (mounted) setState(() => _error = e.message);
    } catch (_) {
      if (mounted) {
        setState(() => _error = 'Could not save that customer. Please try again.');
      }
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  Future<void> _confirmDelete(Customer customer) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: SuperkateStyle.cardStrong,
        shape: SuperkateStyle.cardShape(),
        title: Text('Delete ${customer.name}?'),
        content: const Text(
          'This removes the saved profile and email. Past appointments stay in history with their saved client name.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Keep profile'),
          ),
          FilledButton.tonalIcon(
            onPressed: () => Navigator.of(context).pop(true),
            icon: const Icon(Icons.delete_outline),
            label: const Text('Delete profile'),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    try {
      await widget.service.deleteCustomer(customer.id);
      if (!mounted) return;
      if (_editingCustomer?.id == customer.id) {
        _clearForm();
      }
      _reload();
      widget.onChanged?.call();
      ScaffoldMessenger.of(context)
        ..clearSnackBars()
        ..showSnackBar(
          SnackBar(content: Text('Deleted ${customer.name}. Appointments stayed put.')),
        );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
        ..clearSnackBars()
        ..showSnackBar(
          const SnackBar(content: Text('Could not delete that customer.')),
        );
    }
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
      children: [
        Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 740),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const _CustomerIntroCard(),
                const SizedBox(height: 16),
                _CustomerFormCard(
                  nameController: _name,
                  emailController: _email,
                  editingCustomer: _editingCustomer,
                  saving: _saving,
                  error: _error,
                  onSave: _saveCustomer,
                  onCancel: _clearForm,
                ),
                const SizedBox(height: 20),
                FutureBuilder<List<Customer>>(
                  future: _customers,
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(child: CircularProgressIndicator());
                    }
                    if (snapshot.hasError) {
                      return const _CustomerMessageCard(
                        message: 'Could not load customers. Please try again.',
                      );
                    }

                    final customers = snapshot.data ?? const <Customer>[];
                    if (customers.isEmpty) {
                      return const _CustomerMessageCard(
                        message: 'No saved customer profiles yet.',
                      );
                    }

                    return Column(
                      children: [
                        for (final customer in customers) ...[
                          _CustomerProfileCard(
                            customer: customer,
                            onEdit: () => _startEditing(customer),
                            onDelete: () => _confirmDelete(customer),
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
}

class _CustomerIntroCard extends StatelessWidget {
  const _CustomerIntroCard();

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return Container(
      decoration: BoxDecoration(
        borderRadius: const BorderRadius.all(Radius.circular(32)),
        gradient: palette.introGradient,
        border: Border.all(color: palette.cardBorder),
        boxShadow: palette.edgeGlow,
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const RainbowRail(),
            const SizedBox(height: 18),
            Row(
              children: [
                const RainbowBadge(icon: Icons.people_alt_outlined),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Customer profiles',
                        style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                              fontWeight: FontWeight.w900,
                              letterSpacing: -0.4,
                            ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        'Save names and receipt emails, then keep history safe even when a profile gets deleted.',
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              color: palette.muted,
                              height: 1.35,
                            ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _CustomerFormCard extends StatelessWidget {
  const _CustomerFormCard({
    required this.nameController,
    required this.emailController,
    required this.editingCustomer,
    required this.saving,
    required this.error,
    required this.onSave,
    required this.onCancel,
  });

  final TextEditingController nameController;
  final TextEditingController emailController;
  final Customer? editingCustomer;
  final bool saving;
  final String? error;
  final VoidCallback onSave;
  final VoidCallback onCancel;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);
    final editing = editingCustomer != null;

    return Card(
      color: palette.card,
      elevation: 0,
      shape: SuperkateStyle.cardShape(border: palette.cardBorder),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              editing ? 'Edit profile' : 'Add customer profile',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w900,
                  ),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: nameController,
              textCapitalization: TextCapitalization.words,
              decoration: const InputDecoration(
                labelText: 'Customer name',
                prefixIcon: Icon(Icons.person_outline),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: emailController,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'Receipt email (optional)',
                prefixIcon: Icon(Icons.alternate_email),
              ),
            ),
            if (error != null) ...[
              const SizedBox(height: 12),
              _CustomerErrorBanner(message: error!),
            ],
            const SizedBox(height: 16),
            Wrap(
              spacing: 10,
              runSpacing: 10,
              alignment: WrapAlignment.end,
              children: [
                if (editing)
                  TextButton.icon(
                    onPressed: saving ? null : onCancel,
                    icon: const Icon(Icons.close),
                    label: const Text('Cancel'),
                  ),
                FilledButton.icon(
                  key: const ValueKey('save-customer-button'),
                  onPressed: saving ? null : onSave,
                  icon: saving
                      ? const SizedBox.square(
                          dimension: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.save_outlined),
                  label: Text(saving ? 'Saving…' : editing ? 'Update profile' : 'Save profile'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _CustomerProfileCard extends StatelessWidget {
  const _CustomerProfileCard({
    required this.customer,
    required this.onEdit,
    required this.onDelete,
  });

  final Customer customer;
  final VoidCallback onEdit;
  final VoidCallback onDelete;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return Container(
      decoration: BoxDecoration(
        borderRadius: const BorderRadius.all(Radius.circular(28)),
        color: palette.card,
        border: Border.all(color: palette.cardBorder),
        boxShadow: palette.softGlow,
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const RainbowBadge(icon: Icons.person_outline, size: 44),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        customer.name,
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                              fontWeight: FontWeight.w900,
                            ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        customer.email ?? 'No receipt email saved',
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              color: palette.muted,
                            ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),
            const RainbowRail(height: 3),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              alignment: WrapAlignment.end,
              children: [
                FilledButton.tonalIcon(
                  key: ValueKey('edit-customer-${customer.id}'),
                  onPressed: onEdit,
                  icon: const Icon(Icons.edit_outlined),
                  label: const Text('Edit'),
                ),
                TextButton.icon(
                  key: ValueKey('delete-customer-${customer.id}'),
                  onPressed: onDelete,
                  icon: const Icon(Icons.delete_outline),
                  label: const Text('Delete'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _CustomerMessageCard extends StatelessWidget {
  const _CustomerMessageCard({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return Card(
      color: palette.card,
      elevation: 0,
      shape: SuperkateStyle.cardShape(border: palette.cardBorder),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Text(message),
      ),
    );
  }
}

class _CustomerErrorBanner extends StatelessWidget {
  const _CustomerErrorBanner({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: palette.error.withAlpha(35),
        borderRadius: const BorderRadius.all(Radius.circular(18)),
        border: Border.all(color: palette.error),
      ),
      child: Text(message, style: TextStyle(color: palette.soft)),
    );
  }
}
