-- Agregar columnas created_at y updated_at a labels y subtasks
-- Ejecutar en PostgreSQL

BEGIN;

-- Agregar created_at a labels
ALTER TABLE labels 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Agregar created_at y updated_at a subtasks
ALTER TABLE subtasks 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE subtasks 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;

COMMIT;
