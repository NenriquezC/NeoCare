import 'package:flutter/material.dart';
import '../models/label.dart';

class LabelChip extends StatelessWidget {
  final Label label;
  final VoidCallback? onDelete;
  final bool small;

  const LabelChip({
    super.key,
    required this.label,
    this.onDelete,
    this.small = false,
  });

  @override
  Widget build(BuildContext context) {
    if (small) {
      // Versión pequeña para las tarjetas
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
        decoration: BoxDecoration(
          color: label.colorValue,
          borderRadius: BorderRadius.circular(3),
        ),
        child: Text(
          label.name,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 10,
            fontWeight: FontWeight.bold,
          ),
        ),
      );
    }

    // Versión normal con opción de eliminar
    return Chip(
      label: Text(
        label.name,
        style: const TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
        ),
      ),
      backgroundColor: label.colorValue,
      deleteIcon: onDelete != null
          ? const Icon(Icons.close, size: 18, color: Colors.white)
          : null,
      onDeleted: onDelete,
    );
  }
}
