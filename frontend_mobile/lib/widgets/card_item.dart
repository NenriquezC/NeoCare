import 'package:flutter/material.dart';
import '../models/card.dart';
import '../widgets/label_chip.dart';

class CardItem extends StatelessWidget {
  final CardModel card;
  final VoidCallback onTap;

  const CardItem({
    super.key,
    required this.card,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(4),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Título
              Text(
                card.title,
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
              ),
              
              // Labels
              if (card.labels.isNotEmpty) ...[
                const SizedBox(height: 8),
                Wrap(
                  spacing: 4,
                  runSpacing: 4,
                  children: card.labels.take(3).map((label) {
                    return LabelChip(
                      label: label,
                      small: true,
                    );
                  }).toList(),
                ),
                if (card.labels.length > 3)
                  Padding(
                    padding: const EdgeInsets.only(top: 4),
                    child: Text(
                      '+${card.labels.length - 3} más',
                      style: TextStyle(
                        fontSize: 11,
                        color: Colors.grey[600],
                      ),
                    ),
                  ),
              ],
              
              // Subtasks progress
              if (card.subtasks.isNotEmpty) ...[
                const SizedBox(height: 8),
                Row(
                  children: [
                    Icon(
                      Icons.checklist,
                      size: 16,
                      color: card.subtaskProgress == 1.0 
                          ? Colors.green 
                          : Colors.grey[600],
                    ),
                    const SizedBox(width: 4),
                    Text(
                      '${card.completedSubtasksCount}/${card.subtasks.length}',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: LinearProgressIndicator(
                        value: card.subtaskProgress,
                        minHeight: 4,
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                  ],
                ),
              ],
              
              // Fecha límite
              if (card.dueDate != null) ...[
                const SizedBox(height: 8),
                Row(
                  children: [
                    Icon(
                      Icons.calendar_today,
                      size: 14,
                      color: Colors.grey[600],
                    ),
                    const SizedBox(width: 4),
                    Text(
                      _formatDate(card.dueDate!),
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    final now = DateTime.now();
    final difference = date.difference(now).inDays;
    
    if (difference < 0) {
      return 'Vencida hace ${-difference} días';
    } else if (difference == 0) {
      return 'Vence hoy';
    } else if (difference == 1) {
      return 'Vence mañana';
    } else {
      return 'Vence en $difference días';
    }
  }
}
