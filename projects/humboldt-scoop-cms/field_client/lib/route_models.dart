class RouteStop {
  const RouteStop({
    required this.id,
    required this.customerName,
    required this.addressLabel,
    required this.petNotes,
    required this.yardNotes,
    required this.latitude,
    required this.longitude,
    this.completed = false,
    this.crewNotes = '',
  });

  final String id;
  final String customerName;
  final String addressLabel;
  final String petNotes;
  final String yardNotes;
  final double latitude;
  final double longitude;
  final bool completed;
  final String crewNotes;

  RouteStop copyWith({bool? completed, String? crewNotes}) => RouteStop(
        id: id,
        customerName: customerName,
        addressLabel: addressLabel,
        petNotes: petNotes,
        yardNotes: yardNotes,
        latitude: latitude,
        longitude: longitude,
        completed: completed ?? this.completed,
        crewNotes: crewNotes ?? this.crewNotes,
      );

  factory RouteStop.fromJson(Map<String, dynamic> json) => RouteStop(
        id: json['id'] as String,
        customerName: json['customerName'] as String,
        addressLabel: json['addressLabel'] as String? ?? 'Address hidden',
        petNotes: json['petNotes'] as String? ?? '',
        yardNotes: json['yardNotes'] as String? ?? '',
        latitude: (json['latitude'] as num).toDouble(),
        longitude: (json['longitude'] as num).toDouble(),
      );
}

class CrewRoute {
  const CrewRoute({required this.date, required this.stops});

  final DateTime date;
  final List<RouteStop> stops;

  RouteStop? get nextStop {
    for (final stop in stops) {
      if (!stop.completed) return stop;
    }
    return null;
  }

  CrewRoute updateStop(RouteStop updated) => CrewRoute(
        date: date,
        stops: stops.map((stop) => stop.id == updated.id ? updated : stop).toList(),
      );
}
