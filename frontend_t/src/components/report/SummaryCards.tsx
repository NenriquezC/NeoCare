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
        gap: "1.5rem",
        marginBottom: "2rem",
      }}
    >
      {/* COMPLETADAS */}
      <div
        style={{
          padding: "1.5rem",
          borderRadius: "8px",
          backgroundColor: "#e6f4ea",
          border: "2px solid #34a853",
        }}
      >
        <h3 style={{ marginTop: 0, color: "#1e7e34" }}>✅ Completadas</h3>
        <p style={{ fontSize: "2.5rem", margin: "0.5rem 0", fontWeight: "bold" }}>
          {summary.completed.count}
        </p>

        {summary.completed.count === 0 ? (
          <p style={{ fontSize: "0.9rem", color: "#666", marginTop: "1rem" }}>
            No hubo tareas completadas esta semana
          </p>
        ) : (
          <div style={{ marginTop: "1rem" }}>
            <p style={{ fontSize: "0.85rem", fontWeight: 600, marginBottom: "0.5rem" }}>
              Top {Math.min(5, summary.completed.items.length)} tareas:
            </p>
            <ul style={{ margin: 0, paddingLeft: "1.2rem", fontSize: "0.9rem" }}>
              {summary.completed.items.slice(0, 5).map((item) => (
                <li key={item.id} style={{ marginBottom: "0.3rem" }}>
                  <span
                    style={{
                      background: "#34a853",
                      color: "white",
                      padding: "2px 6px",
                      borderRadius: "4px",
                      fontSize: "0.75rem",
                      marginRight: "0.5rem",
                    }}
                  >
                    #{item.id}
                  </span>
                  {item.title}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* NUEVAS */}
      <div
        style={{
          padding: "1.5rem",
          borderRadius: "8px",
          backgroundColor: "#e8f0fe",
          border: "2px solid #4285f4",
        }}
      >
        <h3 style={{ marginTop: 0, color: "#1967d2" }}>🆕 Nuevas</h3>
        <p style={{ fontSize: "2.5rem", margin: "0.5rem 0", fontWeight: "bold" }}>
          {summary.new.count}
        </p>

        {summary.new.count === 0 ? (
          <p style={{ fontSize: "0.9rem", color: "#666", marginTop: "1rem" }}>
            No hubo tareas nuevas esta semana
          </p>
        ) : (
          <div style={{ marginTop: "1rem" }}>
            <p style={{ fontSize: "0.85rem", fontWeight: 600, marginBottom: "0.5rem" }}>
              Top {Math.min(5, summary.new.items.length)} tareas:
            </p>
            <ul style={{ margin: 0, paddingLeft: "1.2rem", fontSize: "0.9rem" }}>
              {summary.new.items.slice(0, 5).map((item) => (
                <li key={item.id} style={{ marginBottom: "0.3rem" }}>
                  <span
                    style={{
                      background: "#4285f4",
                      color: "white",
                      padding: "2px 6px",
                      borderRadius: "4px",
                      fontSize: "0.75rem",
                      marginRight: "0.5rem",
                    }}
                  >
                    #{item.id}
                  </span>
                  {item.title}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* VENCIDAS */}
      <div
        style={{
          padding: "1.5rem",
          borderRadius: "8px",
          backgroundColor: "#fdecea",
          border: "2px solid #ea4335",
        }}
      >
        <h3 style={{ marginTop: 0, color: "#c5221f" }}>⚠️ Vencidas</h3>
        <p style={{ fontSize: "2.5rem", margin: "0.5rem 0", fontWeight: "bold" }}>
          {summary.overdue.count}
        </p>

        {summary.overdue.count === 0 ? (
          <p style={{ fontSize: "0.9rem", color: "#666", marginTop: "1rem" }}>
            No hubo tareas vencidas esta semana
          </p>
        ) : (
          <div style={{ marginTop: "1rem" }}>
            <p style={{ fontSize: "0.85rem", fontWeight: 600, marginBottom: "0.5rem" }}>
              Top {Math.min(5, summary.overdue.items.length)} tareas:
            </p>
            <ul style={{ margin: 0, paddingLeft: "1.2rem", fontSize: "0.9rem" }}>
              {summary.overdue.items.slice(0, 5).map((item) => (
                <li key={item.id} style={{ marginBottom: "0.3rem" }}>
                  <span
                    style={{
                      background: "#ea4335",
                      color: "white",
                      padding: "2px 6px",
                      borderRadius: "4px",
                      fontSize: "0.75rem",
                      marginRight: "0.5rem",
                    }}
                  >
                    #{item.id}
                  </span>
                  {item.title}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}