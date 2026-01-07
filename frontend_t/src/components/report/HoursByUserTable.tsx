/**
 * Componente HoursByUserTable — Semana 5
 *
 * Muestra una tabla con el total de horas trabajadas
 * por usuario durante una semana específica.
 *
 * Responsabilidades:
 * - Representar datos agregados por usuario
 * - No realizar llamadas HTTP
 * - No contener lógica de negocio
 */

import type { HoursByUserItem } from "@/types/report";

interface HoursByUserTableProps {
  data: HoursByUserItem[];
}

export default function HoursByUserTable({ data }: HoursByUserTableProps) {
  if (data.length === 0) {
    return <p>No hay registros de horas por usuario para esta semana.</p>;
  }

  return (
    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
        marginBottom: "2rem",
      }}
    >
      <thead>
        <tr style={{ backgroundColor: "#f0f0f0" }}>
          <th style={{ padding: "0.5rem", textAlign: "left", border: "1px solid #ddd" }}>
            Usuario
          </th>
          <th style={{ padding: "0.5rem", textAlign: "right", border: "1px solid #ddd" }}>
            Horas totales
          </th>
          <th style={{ padding: "0.5rem", textAlign: "right", border: "1px solid #ddd" }}>
            Tareas
          </th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.user_id}>
            <td style={{ padding: "0.5rem", border: "1px solid #ddd" }}>
              {item.user_name}
            </td>
            <td style={{ padding: "0.5rem", textAlign: "right", border: "1px solid #ddd" }}>
              {item.total_hours.toFixed(2)}
            </td>
            <td style={{ padding: "0.5rem", textAlign: "right", border: "1px solid #ddd" }}>
              {item.tasks_count}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}