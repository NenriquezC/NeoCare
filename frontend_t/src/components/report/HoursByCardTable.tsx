/**
 * Componente HoursByCardTable — Semana 5
 *
 * Muestra una tabla con el total de horas trabajadas
 * por tarjeta durante una semana específica.
 *
 * Responsabilidades:
 * - Representar datos agregados por tarjeta
 * - No realizar llamadas HTTP
 * - No contener lógica de negocio
 */

import type { HoursByCardItem } from "@/types/report";

interface HoursByCardTableProps {
  data: HoursByCardItem[];
}

export default function HoursByCardTable({ data }: HoursByCardTableProps) {
  if (data.length === 0) {
    return <p>No hay registros de horas por tarjeta para esta semana.</p>;
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
        <tr>
          <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
            Tarjeta
          </th>
          <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
            Responsable
          </th>
          <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
            Estado
          </th>
          <th style={{ textAlign: "right", borderBottom: "1px solid #ccc" }}>
            Horas
          </th>
        </tr>
      </thead>
      <tbody>
        {data.map((row) => (
          <tr key={row.card_id}>
            <td style={{ padding: "0.5rem 0" }}>{row.title}</td>
            <td style={{ padding: "0.5rem 0" }}>
              {row.responsible ?? "—"}
            </td>
            <td style={{ padding: "0.5rem 0" }}>{row.status}</td>
            <td style={{ padding: "0.5rem 0", textAlign: "right" }}>
              {row.total_hours.toFixed(2)}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}