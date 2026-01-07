/**
 * Componente SummaryCards — Semana 5
 *
 * Muestra un resumen visual del estado semanal del tablero:
 * - tareas completadas
 * - tareas nuevas
 * - tareas vencidas
 *
 * Responsabilidades:
 * - Representar datos ya calculados por el backend
 * - No contener lógica de negocio
 */

import type { WeeklySummaryResponse } from "@/types/report";

interface SummaryCardsProps {
  summary: WeeklySummaryResponse;
}

export default function SummaryCards({ summary }: SummaryCardsProps) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: "1rem",
        marginBottom: "2rem",
      }}
    >
      {/* COMPLETADAS */}
      <div
        style={{
          padding: "1rem",
          borderRadius: "8px",
          backgroundColor: "#e6f4ea",
        }}
      >
        <h3>Completadas</h3>
        <p style={{ fontSize: "2rem", margin: 0 }}>
          {summary.completed.count}
        </p>
      </div>

      {/* NUEVAS */}
      <div
        style={{
          padding: "1rem",
          borderRadius: "8px",
          backgroundColor: "#e8f0fe",
        }}
      >
        <h3>Nuevas</h3>
        <p style={{ fontSize: "2rem", margin: 0 }}>
          {summary.new.count}
        </p>
      </div>

      {/* VENCIDAS */}
      <div
        style={{
          padding: "1rem",
          borderRadius: "8px",
          backgroundColor: "#fdecea",
        }}
      >
        <h3>Vencidas</h3>
        <p style={{ fontSize: "2rem", margin: 0 }}>
          {summary.overdue.count}
        </p>
      </div>
    </div>
  );
}