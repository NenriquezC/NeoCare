import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../models/board.dart';
import '../models/card.dart';
import '../widgets/card_item.dart';
import 'card_detail_screen.dart';
import 'login_screen.dart';

class BoardsScreen extends StatefulWidget {
  const BoardsScreen({super.key});

  @override
  State<BoardsScreen> createState() => _BoardsScreenState();
}

class _BoardsScreenState extends State<BoardsScreen> {
  Board? _selectedBoard;
  List<BoardList> _lists = [];
  Map<int, List<CardModel>> _cardsByList = {};
  bool _isLoading = true;
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);

    final apiService = context.read<ApiService>();
    
    // Cargar boards
    final boards = await apiService.getBoards();
    
    if (boards.isEmpty) {
      // Si no hay boards, crear uno por defecto
      final newBoard = await apiService.createBoard('Mi Board');
      if (newBoard != null) {
        _selectedBoard = newBoard;
      }
    } else {
      _selectedBoard = boards.first;
    }

    if (_selectedBoard != null) {
      // Cargar listas del board
      _lists = await apiService.getBoardLists(_selectedBoard!.id);
      
      // Cargar todas las cards
      await _loadCards();
    }

    setState(() => _isLoading = false);
  }

  Future<void> _loadCards() async {
    final apiService = context.read<ApiService>();
    final allCards = await apiService.getCards(search: _searchQuery.isEmpty ? null : _searchQuery);
    
    // Agrupar cards por lista
    _cardsByList.clear();
    for (var list in _lists) {
      _cardsByList[list.id] = allCards.where((c) => c.listId == list.id).toList();
    }
    
    setState(() {});
  }

  Future<void> _createCard(int listId) async {
    final titleController = TextEditingController();
    
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Nueva Tarjeta'),
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
            child: const Text('Crear'),
          ),
        ],
      ),
    );

    if (result == true && titleController.text.isNotEmpty) {
      final apiService = context.read<ApiService>();
      await apiService.createCard(
        boardId: _selectedBoard!.id,
        listId: listId,
        title: titleController.text,
      );
      await _loadCards();
    }
  }

  Future<void> _logout() async {
    final apiService = context.read<ApiService>();
    await apiService.logout();
    
    if (mounted) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_selectedBoard?.name ?? 'NeoCare'),
        actions: [
          // Búsqueda
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () async {
              final query = await showDialog<String>(
                context: context,
                builder: (context) {
                  final controller = TextEditingController(text: _searchQuery);
                  return AlertDialog(
                    title: const Text('Buscar tarjetas'),
                    content: TextField(
                      controller: controller,
                      decoration: const InputDecoration(
                        labelText: 'Buscar...',
                        border: OutlineInputBorder(),
                      ),
                      autofocus: true,
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context, ''),
                        child: const Text('Limpiar'),
                      ),
                      ElevatedButton(
                        onPressed: () => Navigator.pop(context, controller.text),
                        child: const Text('Buscar'),
                      ),
                    ],
                  );
                },
              );
              
              if (query != null) {
                _searchQuery = query;
                await _loadCards();
              }
            },
          ),
          // Cerrar sesión
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadData,
              child: _lists.isEmpty
                  ? const Center(child: Text('No hay listas disponibles'))
                  : ListView.builder(
                      scrollDirection: Axis.horizontal,
                      itemCount: _lists.length,
                      itemBuilder: (context, index) {
                        final list = _lists[index];
                        final cards = _cardsByList[list.id] ?? [];
                        
                        return Container(
                          width: 300,
                          margin: const EdgeInsets.all(8),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              // Encabezado de lista
                              Container(
                                padding: const EdgeInsets.all(12),
                                decoration: BoxDecoration(
                                  color: Colors.grey[200],
                                  borderRadius: const BorderRadius.vertical(
                                    top: Radius.circular(8),
                                  ),
                                ),
                                child: Row(
                                  children: [
                                    Expanded(
                                      child: Text(
                                        list.name,
                                        style: const TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 16,
                                        ),
                                      ),
                                    ),
                                    Container(
                                      padding: const EdgeInsets.symmetric(
                                        horizontal: 8,
                                        vertical: 2,
                                      ),
                                      decoration: BoxDecoration(
                                        color: Colors.grey[400],
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                      child: Text(
                                        '${cards.length}',
                                        style: const TextStyle(fontSize: 12),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              
                              // Cards
                              Expanded(
                                child: Container(
                                  decoration: BoxDecoration(
                                    color: Colors.grey[100],
                                    borderRadius: const BorderRadius.vertical(
                                      bottom: Radius.circular(8),
                                    ),
                                  ),
                                  child: ListView.builder(
                                    padding: const EdgeInsets.all(8),
                                    itemCount: cards.length + 1,
                                    itemBuilder: (context, cardIndex) {
                                      if (cardIndex == cards.length) {
                                        // Botón añadir card
                                        return TextButton.icon(
                                          onPressed: () => _createCard(list.id),
                                          icon: const Icon(Icons.add),
                                          label: const Text('Añadir tarjeta'),
                                        );
                                      }
                                      
                                      final card = cards[cardIndex];
                                      return CardItem(
                                        card: card,
                                        onTap: () async {
                                          await Navigator.push(
                                            context,
                                            MaterialPageRoute(
                                              builder: (_) => CardDetailScreen(
                                                cardId: card.id,
                                              ),
                                            ),
                                          );
                                          await _loadCards();
                                        },
                                      );
                                    },
                                  ),
                                ),
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
