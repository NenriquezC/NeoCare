import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/api_config.dart';
import '../models/user.dart';
import '../models/board.dart';
import '../models/card.dart';
import '../models/label.dart';
import '../models/subtask.dart';

class ApiService {
  String? _token;

  // Headers base
  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (_token != null) 'Authorization': 'Bearer $_token',
      };

  // ==================== AUTH ====================

  Future<bool> register(String email, String password, String name) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.authRegister}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
          'name': name,
        }),
      );

      return response.statusCode == 201;
    } catch (e) {
      print('Error en register: $e');
      return false;
    }
  }

  Future<Map<String, dynamic>?> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.authLogin}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _token = data['access_token'];
        
        // Guardar token en SharedPreferences
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('token', _token!);
        
        return data;
      }
      return null;
    } catch (e) {
      print('Error en login: $e');
      return null;
    }
  }

  Future<void> logout() async {
    _token = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
  }

  Future<bool> loadToken() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('token');
    return _token != null;
  }

  bool get isAuthenticated => _token != null;

  // ==================== BOARDS ====================

  Future<List<Board>> getBoards() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.boards}'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Board.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error en getBoards: $e');
      return [];
    }
  }

  Future<Board?> createBoard(String name) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.boards}'),
        headers: _headers,
        body: jsonEncode({'name': name}),
      );

      if (response.statusCode == 201) {
        return Board.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print('Error en createBoard: $e');
      return null;
    }
  }

  Future<List<BoardList>> getBoardLists(int boardId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.boards}/$boardId/lists'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => BoardList.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error en getBoardLists: $e');
      return [];
    }
  }

  // ==================== CARDS ====================

  Future<List<CardModel>> getCards({
    String? search,
    int? responsibleId,
    int? listId,
  }) async {
    try {
      var url = '${ApiConfig.baseUrl}${ApiConfig.cards}';
      final queryParams = <String, String>{};
      
      if (search != null && search.isNotEmpty) queryParams['search'] = search;
      if (responsibleId != null) queryParams['responsible_id'] = responsibleId.toString();
      if (listId != null) queryParams['list_id'] = listId.toString();
      
      if (queryParams.isNotEmpty) {
        url += '?${Uri(queryParameters: queryParams).query}';
      }

      final response = await http.get(
        Uri.parse(url),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => CardModel.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error en getCards: $e');
      return [];
    }
  }

  Future<CardModel?> getCard(int cardId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/$cardId'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        return CardModel.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print('Error en getCard: $e');
      return null;
    }
  }

  Future<CardModel?> createCard({
    required int boardId,
    required int listId,
    required String title,
    String? description,
    String? dueDate,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}'),
        headers: _headers,
        body: jsonEncode({
          'board_id': boardId,
          'list_id': listId,
          'title': title,
          if (description != null) 'description': description,
          if (dueDate != null) 'due_date': dueDate,
        }),
      );

      if (response.statusCode == 201) {
        return CardModel.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print('Error en createCard: $e');
      return null;
    }
  }

  Future<CardModel?> updateCard(int cardId, Map<String, dynamic> updates) async {
    try {
      final response = await http.put(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/$cardId'),
        headers: _headers,
        body: jsonEncode(updates),
      );

      if (response.statusCode == 200) {
        return CardModel.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print('Error en updateCard: $e');
      return null;
    }
  }

  Future<bool> deleteCard(int cardId) async {
    try {
      final response = await http.delete(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/$cardId'),
        headers: _headers,
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error en deleteCard: $e');
      return false;
    }
  }

  // ==================== LABELS ====================

  Future<List<Label>> getCardLabels(int cardId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/$cardId/labels'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Label.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error en getCardLabels: $e');
      return [];
    }
  }

  Future<Label?> addLabel(int cardId, String name, String color) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/$cardId/labels'),
        headers: _headers,
        body: jsonEncode({
          'name': name,
          'color': color,
        }),
      );

      if (response.statusCode == 201) {
        return Label.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print('Error en addLabel: $e');
      return null;
    }
  }

  Future<bool> deleteLabel(int labelId) async {
    try {
      final response = await http.delete(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/labels/$labelId'),
        headers: _headers,
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error en deleteLabel: $e');
      return false;
    }
  }

  // ==================== SUBTASKS ====================

  Future<List<Subtask>> getCardSubtasks(int cardId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/$cardId/subtasks'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Subtask.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error en getCardSubtasks: $e');
      return [];
    }
  }

  Future<Subtask?> addSubtask(int cardId, String title) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/$cardId/subtasks'),
        headers: _headers,
        body: jsonEncode({'title': title}),
      );

      if (response.statusCode == 201) {
        return Subtask.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print('Error en addSubtask: $e');
      return null;
    }
  }

  Future<Subtask?> updateSubtask(int subtaskId, {String? title, bool? completed}) async {
    try {
      final updates = <String, dynamic>{};
      if (title != null) updates['title'] = title;
      if (completed != null) updates['completed'] = completed;

      final response = await http.patch(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/subtasks/$subtaskId'),
        headers: _headers,
        body: jsonEncode(updates),
      );

      if (response.statusCode == 200) {
        return Subtask.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print('Error en updateSubtask: $e');
      return null;
    }
  }

  Future<bool> deleteSubtask(int subtaskId) async {
    try {
      final response = await http.delete(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.cards}/subtasks/$subtaskId'),
        headers: _headers,
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error en deleteSubtask: $e');
      return false;
    }
  }
}
