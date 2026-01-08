import 'package:flutter/material.dart';
import '../models/subtask.dart';

class SubtaskItem extends StatelessWidget {
  final Subtask subtask;
  final VoidCallback onToggle;
  final VoidCallback onDelete;

  const SubtaskItem({
    super.key,
    required this.subtask,
    required this.onToggle,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Checkbox(
          value: subtask.completed,
          onChanged: (_) => onToggle(),
        ),
        title: Text(
          subtask.title,
          style: TextStyle(
            decoration: subtask.completed 
                ? TextDecoration.lineThrough 
                : null,
            color: subtask.completed 
                ? Colors.grey 
                : null,
          ),
        ),
        trailing: IconButton(
          icon: const Icon(Icons.delete, color: Colors.red),
          onPressed: () {
            showDialog(
              context: context,
              builder: (context) => AlertDialog(
                title: const Text('Eliminar subtarea'),
                content: const Text('¿Estás seguro de eliminar esta subtarea?'),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('Cancelar'),
                  ),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.pop(context);
                      onDelete();
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                    ),
                    child: const Text('Eliminar'),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
