import 'label.dart';
import 'subtask.dart';

class CardModel {
  final int id;
  final int boardId;
  final int listId;
  final int order;
  final String title;
  final String? description;
  final DateTime? dueDate;
  final int createdById;
  final int? responsibleId;
  final DateTime createdAt;
  final DateTime updatedAt;
  final bool archived;
  final List<Label> labels;
  final List<Subtask> subtasks;

  CardModel({
    required this.id,
    required this.boardId,
    required this.listId,
    required this.order,
    required this.title,
    this.description,
    this.dueDate,
    required this.createdById,
    this.responsibleId,
    required this.createdAt,
    required this.updatedAt,
    required this.archived,
    this.labels = const [],
    this.subtasks = const [],
  });

  factory CardModel.fromJson(Map<String, dynamic> json) {
    return CardModel(
      id: json['id'] as int,
      boardId: json['board_id'] as int,
      listId: json['list_id'] as int,
      order: json['order'] as int? ?? 0,
      title: json['title'] as String,
      description: json['description'] as String?,
      dueDate: json['due_date'] != null 
          ? DateTime.parse(json['due_date'] as String)
          : null,
      createdById: json['created_by_id'] as int,
      responsibleId: json['responsible_id'] as int?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      archived: json['archived'] as bool? ?? false,
      labels: (json['labels'] as List<dynamic>?)
              ?.map((e) => Label.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      subtasks: (json['subtasks'] as List<dynamic>?)
              ?.map((e) => Subtask.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'board_id': boardId,
      'list_id': listId,
      'title': title,
      'description': description,
      'due_date': dueDate?.toIso8601String().split('T')[0],
    };
  }

  // Calcular progreso de subtasks
  double get subtaskProgress {
    if (subtasks.isEmpty) return 0.0;
    final completed = subtasks.where((s) => s.completed).length;
    return completed / subtasks.length;
  }

  int get completedSubtasksCount {
    return subtasks.where((s) => s.completed).length;
  }
}
