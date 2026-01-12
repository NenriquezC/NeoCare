-- =====================================================
-- Script para añadir/modificar Foreign Keys con CASCADE
-- Basado en la estructura REAL de la base de datos NeoCare
-- Fecha: 8 de enero de 2026
-- =====================================================

-- IMPORTANTE: Este script primero elimina las foreign keys existentes
-- y luego las vuelve a crear con ON DELETE CASCADE

BEGIN;

-- =====================================================
-- 1. PERMITIR NULL EN COLUMNAS CON SET NULL
-- =====================================================

-- Permitir NULL en columnas que usan ON DELETE SET NULL
ALTER TABLE cards ALTER COLUMN created_by_id DROP NOT NULL;
ALTER TABLE cards ALTER COLUMN responsible_id DROP NOT NULL;

-- =====================================================
-- 2. ELIMINAR FOREIGN KEYS EXISTENTES (si existen)
-- =====================================================

-- boards table
ALTER TABLE IF EXISTS boards 
    DROP CONSTRAINT IF EXISTS boards_user_id_fkey;

-- lists table
ALTER TABLE IF EXISTS lists 
    DROP CONSTRAINT IF EXISTS lists_board_id_fkey;

-- cards table
ALTER TABLE IF EXISTS cards 
    DROP CONSTRAINT IF EXISTS cards_list_id_fkey,
    DROP CONSTRAINT IF EXISTS cards_board_id_fkey,
    DROP CONSTRAINT IF EXISTS cards_responsible_id_fkey,
    DROP CONSTRAINT IF EXISTS cards_created_by_id_fkey;

-- time_entries table
ALTER TABLE IF EXISTS time_entries 
    DROP CONSTRAINT IF EXISTS time_entries_card_id_fkey,
    DROP CONSTRAINT IF EXISTS time_entries_user_id_fkey;

-- board_members table
ALTER TABLE IF EXISTS board_members 
    DROP CONSTRAINT IF EXISTS board_members_board_id_fkey,
    DROP CONSTRAINT IF EXISTS board_members_user_id_fkey;

-- labels table
ALTER TABLE IF EXISTS labels 
    DROP CONSTRAINT IF EXISTS labels_card_id_fkey;

-- subtasks table
ALTER TABLE IF EXISTS subtasks 
    DROP CONSTRAINT IF EXISTS subtasks_card_id_fkey;

-- =====================================================
-- 2. CREAR FOREIGN KEYS CON CASCADE DELETE
-- =====================================================

-- boards -> users
-- Cuando se elimina un usuario, se eliminan todos sus boards
ALTER TABLE boards
    ADD CONSTRAINT boards_user_id_fkey 
    FOREIGN KEY (user_id) 
    REFERENCES users(id) 
    ON DELETE CASCADE;

-- lists -> boards
-- Cuando se elimina un board, se eliminan todas sus listas
ALTER TABLE lists
    ADD CONSTRAINT lists_board_id_fkey 
    FOREIGN KEY (board_id) 
    REFERENCES boards(id) 
    ON DELETE CASCADE;

-- cards -> boards
-- Cuando se elimina un board, se eliminan todas sus tarjetas
ALTER TABLE cards
    ADD CONSTRAINT cards_board_id_fkey 
    FOREIGN KEY (board_id) 
    REFERENCES boards(id) 
    ON DELETE CASCADE;

-- cards -> lists
-- Cuando se elimina una lista, se eliminan todas sus tarjetas
ALTER TABLE cards
    ADD CONSTRAINT cards_list_id_fkey 
    FOREIGN KEY (list_id) 
    REFERENCES lists(id) 
    ON DELETE CASCADE;

-- cards -> users (responsible)
-- Cuando se elimina un usuario responsable, se pone NULL (opcional)
ALTER TABLE cards
    ADD CONSTRAINT cards_responsible_id_fkey 
    FOREIGN KEY (responsible_id) 
    REFERENCES users(id) 
    ON DELETE SET NULL;

-- cards -> users (creator)
-- Cuando se elimina un usuario creador, se pone NULL (opcional)
ALTER TABLE cards
    ADD CONSTRAINT cards_created_by_id_fkey 
    FOREIGN KEY (created_by_id) 
    REFERENCES users(id) 
    ON DELETE SET NULL;

-- time_entries -> cards
-- Cuando se elimina una tarjeta, se eliminan todos sus time entries
ALTER TABLE time_entries
    ADD CONSTRAINT time_entries_card_id_fkey 
    FOREIGN KEY (card_id) 
    REFERENCES cards(id) 
    ON DELETE CASCADE;

-- time_entries -> users
-- Cuando se elimina un usuario, se eliminan todos sus time entries
ALTER TABLE time_entries
    ADD CONSTRAINT time_entries_user_id_fkey 
    FOREIGN KEY (user_id) 
    REFERENCES users(id) 
    ON DELETE CASCADE;

-- board_members -> boards
-- Cuando se elimina un board, se eliminan todas sus membresías
ALTER TABLE board_members
    ADD CONSTRAINT board_members_board_id_fkey 
    FOREIGN KEY (board_id) 
    REFERENCES boards(id) 
    ON DELETE CASCADE;

-- board_members -> users
-- Cuando se elimina un usuario, se eliminan todas sus membresías
ALTER TABLE board_members
    ADD CONSTRAINT board_members_user_id_fkey 
    FOREIGN KEY (user_id) 
    REFERENCES users(id) 
    ON DELETE CASCADE;

-- labels -> cards
-- Cuando se elimina una tarjeta, se eliminan todas sus etiquetas
ALTER TABLE labels
    ADD CONSTRAINT labels_card_id_fkey 
    FOREIGN KEY (card_id) 
    REFERENCES cards(id) 
    ON DELETE CASCADE;

-- subtasks -> cards
-- Cuando se elimina una tarjeta, se eliminan todas sus subtareas
ALTER TABLE subtasks
    ADD CONSTRAINT subtasks_card_id_fkey 
    FOREIGN KEY (card_id) 
    REFERENCES cards(id) 
    ON DELETE CASCADE;

COMMIT;

-- =====================================================
-- 3. VERIFICAR FOREIGN KEYS CREADAS
-- =====================================================
-- Ejecuta esta consulta para verificar que las FK se crearon correctamente:
-- 
-- SELECT 
--     tc.table_name, 
--     kcu.column_name, 
--     ccu.table_name AS foreign_table_name,
--     ccu.column_name AS foreign_column_name,
--     rc.delete_rule
-- FROM information_schema.table_constraints AS tc 
-- JOIN information_schema.key_column_usage AS kcu
--     ON tc.constraint_name = kcu.constraint_name
--     AND tc.table_schema = kcu.table_schema
-- JOIN information_schema.constraint_column_usage AS ccu
--     ON ccu.constraint_name = tc.constraint_name
--     AND ccu.table_schema = tc.table_schema
-- JOIN information_schema.referential_constraints AS rc
--     ON rc.constraint_name = tc.constraint_name
-- WHERE tc.constraint_type = 'FOREIGN KEY'
--     AND tc.table_schema = 'public'
-- ORDER BY tc.table_name, kcu.column_name;

-- =====================================================
-- JERARQUÍA DE CASCADE DELETE
-- =====================================================
-- 
-- users
--   ├── boards (CASCADE)
--   │   ├── lists (CASCADE)
--   │   │   └── cards (CASCADE)
--   │   │       ├── time_entries (CASCADE)
--   │   │       ├── subtasks (CASCADE)
--   │   │       └── labels (CASCADE)
--   │   ├── cards (CASCADE directamente por board_id)
--   │   │   ├── time_entries (CASCADE)
--   │   │   ├── subtasks (CASCADE)
--   │   │   └── labels (CASCADE)
--   │   └── board_members (CASCADE)
--   ├── board_members (CASCADE)
--   ├── time_entries (CASCADE)
--   ├── cards.responsible_id (SET NULL)
--   └── cards.created_by_id (SET NULL)
-- 
-- EJEMPLO: Al eliminar un usuario se eliminan:
-- 1. Sus boards
-- 2. Las listas de esos boards
-- 3. Las tarjetas de esas listas (tanto por list_id como por board_id)
-- 4. Los time_entries de esas tarjetas
-- 5. Las subtasks de esas tarjetas
-- 6. Las labels de esas tarjetas
-- 7. Los board_members de esos boards
-- 8. Sus board_members directos
-- 9. Sus time_entries directos
-- 10. Se pone NULL en responsible_id y created_by_id donde era responsable/creador
