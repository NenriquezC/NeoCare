/// Configuración de la API Backend
/// 
/// Para emulador Android: usa 10.0.2.2 (redirige a localhost de Windows)
/// Para dispositivo físico: usa tu IP local (ejemplo: 192.168.1.X)
class ApiConfig {
  // Cambia esto según tu entorno:
  // - Emulador Android: http://10.0.2.2:8000
  // - Dispositivo físico: http://192.168.1.X:8000 (tu IP local)
  // - Web (Chrome): http://localhost:8000
  // - Producción: https://tu-dominio.com
  
  static const String baseUrl = 'http://192.168.1.39:8000';
  
  // Endpoints
  static const String authRegister = '/auth/register';
  static const String authLogin = '/auth/login';
  static const String boards = '/boards';
  static const String cards = '/cards';
  static const String worklogs = '/worklogs';
  
  // Timeouts
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}
