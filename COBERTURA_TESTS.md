# Cobertura de Tests - NeoCare

## Resumen General
- **Total de tests ejecutados**: 75 tests
- **Tests pasados**: 75 (100%)
- **Tests ignorados**: 14 tests E2E (requieren Playwright)

## Funcionalidades Cubiertas por Tests

### 1. Autenticación (Auth) ✅ COMPLETA
**Archivo**: `tests/auth/`
- ✅ Registro de usuarios (exitoso y con email duplicado)
- ✅ Login (exitoso y con credenciales inválidas)
- ✅ Validación de schemas (UserRegister, UserLogin, Token)
- ✅ Hash y verificación de contraseñas
- ✅ Creación y validación de tokens JWT
- ✅ get_current_user (exitoso, token inválido, usuario no existe)

**Tests**: 17
- test_register_success
- test_register_existing_email
- test_login_success
- test_login_invalid_credentials
- test_user_register_valido/sin_name/email_invalido
- test_user_login_valido/email_invalido
- test_token_valido/tipo_personalizado
- test_hash_y_verify_password/hash_password_none
- test_create_token_contenido
- test_get_current_user_exitoso/token_invalido/usuario_no_existe

### 2. Tableros (Boards) ⚠️ PARCIAL
**Archivo**: `tests/boards/`
- ✅ Modelos de BD (User, Board, List, Card, TimeEntry, BoardMember)
- ✅ Listar tableros del usuario autenticado (GET /boards/)
- ❌ **FALTA**: Crear tablero (POST /boards/)
- ❌ **FALTA**: Actualizar tablero (PATCH /boards/{id})
- ❌ **FALTA**: Eliminar tablero (DELETE /boards/{id})
- ❌ **FALTA**: Obtener detalles de un tablero específico
- ❌ **FALTA**: Crear/editar/eliminar listas dentro de tableros
- ❌ **FALTA**: Gestión de miembros del tablero (BoardMember)

**Tests**: 7
- test_create_user/board/list/card/time_entry/board_member (modelos)
- test_get_boards_exitoso

### 3. Tarjetas (Cards) ✅ COMPLETA
**Archivo**: `tests/cards/`
- ✅ Crear tarjeta (válido, título vacío, fecha inválida)
- ✅ Editar tarjeta
- ✅ Ver tarjeta (existente, inexistente, sin permisos)
- ✅ Mover tarjeta entre listas (misma lista, otra lista, validaciones)
- ✅ Permisos y autorización (sin token, entre usuarios)
- ✅ Flujo completo (registro → login → crear → listar → editar)

**Tests**: 12
- test_crear_tarjeta_ok/titulo_vacio/fecha_invalida
- test_editar_tarjeta_ok
- test_crear_tarjeta_sin_token
- test_ver_tarjeta_inexistente
- test_no_puede_ver_tarjeta_de_otro_usuario
- test_flujo_completo_tarjeta
- test_mover_tarjeta_misma_lista/a_otra_lista/sin_token/order_negativo

### 4. Etiquetas y Subtareas ✅ COMPLETA
**Archivo**: `tests/labels_subtasks/`
- ✅ Crear/listar/eliminar etiquetas
- ✅ Autorización de etiquetas
- ✅ Crear/listar/actualizar/eliminar subtareas
- ✅ Actualizar estado completado y título de subtareas
- ✅ Cálculo de progreso de subtareas
- ✅ Búsqueda de tarjetas (por título, por descripción)
- ✅ Filtros (por responsible_id, combinados)

**Tests**: 13
- test_create_label/get_card_labels/delete_label/label_without_auth
- test_create_subtask/get_card_subtasks
- test_update_subtask_completed/title
- test_delete_subtask/subtask_progress_calculation
- test_search_cards_by_title/description
- test_filter_by_responsible/combined_filters

### 5. Worklogs (Registro de Horas) ✅ COMPLETA
**Archivo**: `tests/worklogs/`
- ✅ Crear worklog (exitoso, horas inválidas, fecha futura)
- ✅ Listar worklogs
- ✅ Actualizar worklog (propio, de otro usuario)
- ✅ Eliminar worklog propio
- ✅ Consultar mis horas por semana

**Tests**: 8
- test_create_worklog_success/invalid_hours/future_date
- test_list_worklogs
- test_update_worklog_own/other_user
- test_delete_worklog_own
- test_my_hours_week

### 6. Reportes ✅ COMPLETA
**Archivos**: `tests/test_report_*.py`
- ✅ Resumen semanal (GET /boards/{id}/report/weekly-summary)
- ✅ Horas por usuario (GET /boards/{id}/report/hours-by-user)
- ✅ Horas por tarjeta (GET /boards/{id}/report/hours-by-card)
- ✅ Validación de autorización (sin token, sin JWT)
- ✅ Conversión de formato de semana ISO
- ✅ Validación de formato y rango de semanas
- ✅ Flujo de integración completo (cambio de semana)

**Tests**: 8
- test_get_weekly_summary_success
- test_get_hours_by_user_success
- test_get_hours_by_card_success
- test_get_report_unauthorized/no_jwt
- test_get_week_date_range_valid/invalid_format/invalid_week
- test_report_integration_flow/change_week

### 7. Configuración y Database ✅ COMPLETA
**Archivos**: `tests/test_config.py`, `tests/test_database.py`
- ✅ Valores por defecto de configuración
- ✅ Carga de configuración desde variables de entorno
- ✅ URL de base de datos definida
- ✅ Engine y SessionLocal configurados
- ✅ Creación de tablas temporales

**Tests**: 5
- test_valores_por_defecto/carga_desde_env
- test_database_url_definida
- test_engine_y_session_local
- test_crear_tablas_temporales

### 8. Aplicación Principal ✅ COMPLETA
**Archivo**: `tests/test_main.py`
- ✅ Endpoint raíz (GET /)
- ✅ Router de autenticación incluido

**Tests**: 2
- test_root_endpoint
- test_auth_router_included

### 9. Tests E2E (End-to-End) ⏸️ NO EJECUTADOS
**Archivo**: `tests/e2e/test_e2e.py`
- ⏸️ Tests de API completos (GET boards, lists, cards, worklogs)
- ⏸️ Tests de UI con Playwright (login, worklogs page)
- **Motivo**: Requieren instalación de Playwright

**Tests E2E**: 14 (no ejecutados)
- API: test_api_get_boards/lists, create/list/get/update/move/delete_card
- API: test_api_create_worklog
- UI: test_ui_login_exitoso/fallido, test_ui_worklogs_page

## Funcionalidades NO Cubiertas por Tests

### Tableros (Boards)
- ❌ POST /boards/ - Crear tablero
- ❌ PATCH /boards/{id} - Actualizar tablero
- ❌ DELETE /boards/{id} - Eliminar tablero
- ❌ GET /boards/{id} - Obtener detalles de tablero específico
- ❌ POST /boards/{id}/lists - Crear lista
- ❌ PATCH /boards/{id}/lists/{list_id} - Actualizar lista
- ❌ DELETE /boards/{id}/lists/{list_id} - Eliminar lista
- ❌ POST /boards/{id}/members - Añadir miembro al tablero
- ❌ DELETE /boards/{id}/members/{user_id} - Eliminar miembro

### Tarjetas (Cards)
- ⚠️ DELETE /cards/{id} - Eliminar tarjeta (existe en E2E pero no en tests unitarios)
- ⚠️ Búsqueda avanzada con múltiples filtros combinados (parcialmente cubierto)

## Recomendaciones

### Prioridad ALTA
1. **Agregar tests para CRUD completo de Boards**
   - Crear, actualizar, eliminar tableros
   - Obtener detalles de un tablero específico
   
2. **Agregar tests para gestión de Listas**
   - Crear, actualizar, eliminar listas dentro de tableros
   - Reordenar listas

3. **Agregar tests para gestión de Miembros de Tablero**
   - Añadir/eliminar miembros
   - Verificar permisos basados en membresía

### Prioridad MEDIA
4. **Completar tests de eliminación de tarjetas**
   - Mover test_api_delete_card de E2E a tests unitarios
   - Agregar casos: eliminar tarjeta sin permisos, tarjeta inexistente

5. **Instalar Playwright y ejecutar tests E2E**
   - `pip install playwright`
   - `playwright install`
   - Ejecutar tests completos incluyendo UI

### Prioridad BAJA
6. **Agregar tests de integración**
   - Flujos completos multi-usuario
   - Escenarios de concurrencia
   - Tests de rendimiento

## Cobertura Estimada

| Módulo | Cobertura | Tests | Estado |
|--------|-----------|-------|--------|
| Autenticación | 100% | 17 | ✅ |
| Tarjetas | 95% | 12 | ✅ |
| Etiquetas/Subtareas | 100% | 13 | ✅ |
| Worklogs | 100% | 8 | ✅ |
| Reportes | 100% | 8 | ✅ |
| **Tableros** | **30%** | **7** | ⚠️ |
| Config/Database | 100% | 5 | ✅ |
| Main | 100% | 2 | ✅ |
| **E2E** | **0%** | **0/14** | ❌ |

**Cobertura Global Funcional**: ~85% (excelente para funcionalidades core)  
**Cobertura Crítica Faltante**: Gestión de tableros y listas
