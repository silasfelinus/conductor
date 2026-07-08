import '../models/appointment.dart';
import '../models/customer.dart';
import 'money.dart';

class ReceiptEmailDraft {
  const ReceiptEmailDraft({
    required this.toEmail,
    required this.subject,
    required this.body,
  });

  final String? toEmail;
  final String subject;
  final String body;

  Uri get mailtoUri => Uri(
        scheme: 'mailto',
        path: toEmail?.trim() ?? '',
        queryParameters: {
          'subject': subject,
          'body': body,
        },
      );
}

ReceiptEmailDraft buildReceiptEmail({
  required Appointment appointment,
  Customer? customer,
}) {
  final clientName = appointment.clientNameSnapshot;
  final date = formatReceiptDate(appointment.appointmentDate);
  final hourlyRate = formatCents(appointment.hourlyRateCents);
  final timeSpent = formatDurationMinutes(appointment.timeSpentMinutes);
  final productCost = formatCents(appointment.productCostCents);
  final total = formatCents(appointment.appointmentTotalCents);
  final toEmail = customer?.email?.trim();

  return ReceiptEmailDraft(
    toEmail: toEmail == null || toEmail.isEmpty ? null : toEmail,
    subject: 'Hair by Superkate receipt for $clientName',
    body: [
      'Hair by Superkate',
      '',
      'Hi $clientName,',
      '',
      'Thank you for your appointment on $date.',
      '',
      'Receipt details:',
      'Client: $clientName',
      'Appointment date: $date',
      'Hourly rate: $hourlyRate/hour',
      'Time spent: $timeSpent',
      'Product cost: $productCost',
      'Total price: $total',
      '',
      'Formula:',
      '$hourlyRate × $timeSpent + $productCost = $total',
      '',
      'Superkate loves you!',
    ].join('\n'),
  );
}

String formatReceiptDate(DateTime date) =>
    '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';

String formatDurationMinutes(int minutes) {
  final hours = minutes ~/ 60;
  final remainingMinutes = minutes % 60;

  if (hours <= 0) return '${remainingMinutes}m';
  if (remainingMinutes == 0) return '${hours}h';
  return '${hours}h ${remainingMinutes}m';
}
