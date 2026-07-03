class Todo {
  const Todo({
    required this.id,
    required this.title,
    this.description,
    this.status = 'OPEN', // OPEN | DONE | ARCHIVED
    this.priority = 'NORMAL', // LOW | NORMAL | HIGH
    this.category = 'HONEYDO', // AGENT | KAIZEN | HONEYDO | DESIRED_FEATURE
    this.dueDate,
    this.dreamId,
    this.order,
  });

  final int id;
  final String title;
  final String? description;
  final String status;
  final String priority;
  final String category;
  final DateTime? dueDate;

  /// Links the todo to a project (Dream). Null = global.
  final int? dreamId;
  final int? order;

  bool get isOpen => status == 'OPEN';
  bool get isDone => status == 'DONE';

  factory Todo.fromJson(Map<String, dynamic> json) => Todo(
        id: (json['id'] as num).toInt(),
        title: (json['title'] as String?) ?? '',
        description: json['description'] as String?,
        status: (json['status'] as String?) ?? 'OPEN',
        priority: (json['priority'] as String?) ?? 'NORMAL',
        category: (json['category'] as String?) ?? 'HONEYDO',
        dueDate: json['dueDate'] != null
            ? DateTime.tryParse(json['dueDate'] as String)
            : null,
        dreamId: (json['dreamId'] as num?)?.toInt(),
        order: (json['order'] as num?)?.toInt(),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'description': description,
        'status': status,
        'priority': priority,
        'category': category,
        'dueDate': dueDate?.toIso8601String(),
        'dreamId': dreamId,
        'order': order,
      };

  Todo copyWith({String? status, String? priority, String? title}) => Todo(
        id: id,
        title: title ?? this.title,
        description: description,
        status: status ?? this.status,
        priority: priority ?? this.priority,
        category: category,
        dueDate: dueDate,
        dreamId: dreamId,
        order: order,
      );
}
