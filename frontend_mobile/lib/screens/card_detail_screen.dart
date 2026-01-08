import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../models/card.dart';
import '../models/label.dart';
import '../models/subtask.dart';
import '../widgets/label_chip.dart';
import '../widgets/subtask_item.dart';

class CardDetailScreen extends StatefulWidget {
  final int cardId;

  const CardDetailScreen({super.key, required this.cardId});

  @override
  State<CardDetailScreen> createState() => _CardDetailScreenState();
}

class _CardDetailScreenState extends State<CardDetailScreen> {
  CardModel? _card;
  bool _isLoading = true;
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadCard();
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  Future<void> _loadCard() async {
    setState(() => _isLoading = true);
    
    final apiService = context.read<ApiService>();
    final card = await apiService.getCard(widget.cardId);
    
    if (card != null) {
      _card = card;
      _titleController.text = card.title;
      _descriptionController.text = card.description ?? '';
    }
    
    setState(() => _isLoading = false);
  }

  Future<void> _saveCard() async {
    if (_card == null) return;

    final apiService = context.read<ApiService>();
    await apiService.updateCard(
      _card!.id,
      {
        'title': _titleController.text,
        'description': _descriptionController.text.isEmpty 
            ? null 
            : _descriptionController.text,
      },
    );

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Tarjeta actualizada')),
    );
  }

  Future<void> _addLabel() async {
    if (_card == null) return;

    final nameController = TextEditingController();
    Color selectedColor = Colors.blue;
    String? selectedPreset;

    final result = await showDialog<bool>(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('Añadir Etiqueta'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: nameController,
                  decoration: const InputDecoration(
                    labelText: 'Nombre',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                
                // Colores predefinidos
                const Text('Etiquetas rápidas:'),
                const SizedBox(height: 8),
                Wrap(
                  spacing: 8,
                  children: Label.predefinedColors.entries.map((entry) {
                    final isSelected = selectedPreset == entry.key;
                    return FilterChip(
                      label: Text(entry.key),
                      selected: isSelected,
                      avatar: CircleAvatar(
                        backgroundColor: Color(
                          int.parse(entry.value.replaceFirst('#', '0xFF')),
                        ),
                      ),
                      onSelected: (selected) {
                        setState(() {
                          if (selected) {
                            selectedPreset = entry.key;
                            nameController.text = entry.key;
                            selectedColor = Color(
                              int.parse(entry.value.replaceFirst('#', '0xFF')),
                            );
                          } else {
                            selectedPreset = null;
                          }
                        });
                      },
                    );
                  }).toList(),
                ),
                const SizedBox(height: 16),
                
                // Selector de color personalizado
                const Text('O elige un color personalizado:'),
                const SizedBox(height: 8),
                BlockPicker(
                  pickerColor: selectedColor,
                  onColorChanged: (color) {
                    selectedColor = color;
                    selectedPreset = null;
                  },
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancelar'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.pop(context, true),
              child: const Text('Añadir'),
            ),
          ],
        ),
      ),
    );

    if (result == true && nameController.text.isNotEmpty) {
      final apiService = context.read<ApiService>();
      final colorHex = '#${selectedColor.value.toRadixString(16).substring(2)}';
      
      await apiService.addLabel(_card!.id, nameController.text, colorHex);
      await _loadCard();
    }
  }

  Future<void> _deleteLabel(int labelId) async {
    final apiService = context.read<ApiService>();
    await apiService.deleteLabel(labelId);
    await _loadCard();
  }

  Future<void> _addSubtask() async {
    if (_card == null) return;

    final titleController = TextEditingController();
    
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Nueva Subtarea'),
        content: TextField(
          controller: titleController,
          decoration: const InputDecoration(
            labelText: 'Título',
            border: OutlineInputBorder(),
          ),
          autofocus: true,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Añadir'),
          ),
        ],
      ),
    );

    if (result == true && titleController.text.isNotEmpty) {
      final apiService = context.read<ApiService>();
      await apiService.addSubtask(_card!.id, titleController.text);
      await _loadCard();
    }
  }

  Future<void> _toggleSubtask(Subtask subtask) async {
    final apiService = context.read<ApiService>();
    await apiService.updateSubtask(subtask.id, completed: !subtask.completed);
    await _loadCard();
  }

  Future<void> _deleteSubtask(int subtaskId) async {
    final apiService = context.read<ApiService>();
    await apiService.deleteSubtask(subtaskId);
    await _loadCard();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detalle de Tarjeta'),
        actions: [
          IconButton(
            icon: const Icon(Icons.save),
            onPressed: _saveCard,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _card == null
              ? const Center(child: Text('Tarjeta no encontrada'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Título
                      TextField(
                        controller: _titleController,
                        decoration: const InputDecoration(
                          labelText: 'Título',
                          border: OutlineInputBorder(),
                        ),
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 16),

                      // Descripción
                      TextField(
                        controller: _descriptionController,
                        decoration: const InputDecoration(
                          labelText: 'Descripción',
                          border: OutlineInputBorder(),
                          alignLabelWithHint: true,
                        ),
                        maxLines: 5,
                      ),
                      const SizedBox(height: 24),

                      // Labels
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Etiquetas',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          IconButton(
                            icon: const Icon(Icons.add),
                            onPressed: _addLabel,
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      if (_card!.labels.isEmpty)
                        const Text(
                          'No hay etiquetas',
                          style: TextStyle(color: Colors.grey),
                        )
                      else
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: _card!.labels.map((label) {
                            return LabelChip(
                              label: label,
                              onDelete: () => _deleteLabel(label.id),
                            );
                          }).toList(),
                        ),
                      const SizedBox(height: 24),

                      // Subtasks
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Subtareas',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          IconButton(
                            icon: const Icon(Icons.add),
                            onPressed: _addSubtask,
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      
                      // Progreso
                      if (_card!.subtasks.isNotEmpty) ...[
                        Row(
                          children: [
                            Expanded(
                              child: LinearProgressIndicator(
                                value: _card!.subtaskProgress,
                                minHeight: 8,
                                borderRadius: BorderRadius.circular(4),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Text(
                              '${_card!.completedSubtasksCount}/${_card!.subtasks.length}',
                              style: const TextStyle(fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                      ],
                      
                      if (_card!.subtasks.isEmpty)
                        const Text(
                          'No hay subtareas',
                          style: TextStyle(color: Colors.grey),
                        )
                      else
                        Column(
                          children: _card!.subtasks.map((subtask) {
                            return SubtaskItem(
                              subtask: subtask,
                              onToggle: () => _toggleSubtask(subtask),
                              onDelete: () => _deleteSubtask(subtask.id),
                            );
                          }).toList(),
                        ),
                    ],
                  ),
                ),
    );
  }
}
