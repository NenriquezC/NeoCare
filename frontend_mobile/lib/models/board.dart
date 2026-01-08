class Board {
  final int id;
  final String name;
  final int userId;
  final DateTime createdAt;

  Board({
    required this.id,
    required this.name,
    required this.userId,
    required this.createdAt,
  });

  factory Board.fromJson(Map<String, dynamic> json) {
    return Board(
      id: json['id'] as int,
      name: json['name'] as String,
      userId: json['user_id'] as int,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
    };
  }
}

class BoardList {
  final int id;
  final int boardId;
  final String name;
  final int position;
  final DateTime createdAt;

  BoardList({
    required this.id,
    required this.boardId,
    required this.name,
    required this.position,
    required this.createdAt,
  });

  factory BoardList.fromJson(Map<String, dynamic> json) {
    return BoardList(
      id: json['id'] as int,
      boardId: json['board_id'] as int,
      name: json['name'] as String,
      position: json['position'] as int,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}
