import 'package:flutter/material.dart';

class Label {
  final int id;
  final int cardId;
  final String name;
  final String color;

  Label({
    required this.id,
    required this.cardId,
    required this.name,
    required this.color,
  });

  factory Label.fromJson(Map<String, dynamic> json) {
    return Label(
      id: json['id'] as int,
      cardId: json['card_id'] as int,
      name: json['name'] as String,
      color: json['color'] as String? ?? '#6b7280',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'color': color,
    };
  }

  Color get colorValue {
    try {
      return Color(int.parse(color.replaceFirst('#', '0xFF')));
    } catch (e) {
      return Colors.grey;
    }
  }

  // Colores predefinidos para labels
  static const Map<String, String> predefinedColors = {
    'Urgente': '#ef4444',
    'Media': '#f59e0b',
    'Baja': '#10b981',
    'Feature': '#3b82f6',
    'QA': '#8b5cf6',
    'Bloqueado': '#6b7280',
  };
}
