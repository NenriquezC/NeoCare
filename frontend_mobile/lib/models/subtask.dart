class Subtask {
  final int id;
  final int cardId;
  final String title;
  final bool completed;
  final int position;

  Subtask({
    required this.id,
    required this.cardId,
    required this.title,
    required this.completed,
    required this.position,
  });

  factory Subtask.fromJson(Map<String, dynamic> json) {
    return Subtask(
      id: json['id'] as int,
      cardId: json['card_id'] as int,
      title: json['title'] as String,
      completed: json['completed'] as bool? ?? false,
      position: json['position'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'completed': completed,
    };
  }

  Subtask copyWith({
    int? id,
    int? cardId,
    String? title,
    bool? completed,
    int? position,
  }) {
    return Subtask(
      id: id ?? this.id,
      cardId: cardId ?? this.cardId,
      title: title ?? this.title,
      completed: completed ?? this.completed,
      position: position ?? this.position,
    );
  }
}
