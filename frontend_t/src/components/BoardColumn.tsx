/**
 * @file BoardColumn.tsx
 * Componente visual para mostrar una columna/tablero en un sistema tipo Kanban.
 * Muestra el título de la columna y, eventualmente, las tarjetas asignadas.
 */
import React from "react";

/**
 * Props para el componente BoardColumn.
 * @property title - Título de la columna que se mostrará en el encabezado.
 */
interface BoardColumnProps {
  title: string;
}


/**
 * Componente BoardColumn
 *
 * Muestra una columna visual con un título y zona para tarjetas de tareas.
 * Si no hay tarjetas, muestra un mensaje informativo.
 *
 * @param {BoardColumnProps} props - Propiedades del componente.
 * @returns {JSX.Element} La columna del tablero renderizada.
 */

export const BoardColumn: React.FC<BoardColumnProps> = ({ title }) => {
  return (
    <div
      style={{
        flex: 1,
        background: "#1e293b",
        borderRadius: "0.5rem",
        padding: "1rem",
      }}
    >
      <h2 style={{ marginBottom: "1rem", fontSize: "1.25rem" }}>{title}</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {/* Aquí irán las tarjetas */}
        <p style={{ color: "#94a3b8", textAlign: "center", padding: "2rem" }}>
          No hay tarjetas
        </p>
      </div>
    </div>
  );
};
