/**
 * Modal para mostrar detalle de worklogs de un usuario específico en la semana
 */

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

interface UserDetailModalProps {
  userId: number;
  userName: string;
  week: string;
  boardId: number;
  onClose: () => void;
}

interface WorklogDetail {
  id: number;
  card_id: number;
  card_title?: string;
  date: string;
  hours: string | number;
  note?: string | null;
}

export default function UserDetailModal({
  userId,
  userName,
  week,
  boardId,
  onClose,
}: UserDetailModalProps) {
  const [worklogs, setWorklogs] = useState<WorklogDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUserWorklogs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function loadUserWorklogs() {
    setLoading(true);
    setError(null);
    try {
      // Obtener todas las horas por tarjeta de la semana
      const res = await apiFetch(`/report/${boardId}/hours-by-card?week=${week}`, {
        method: "GET",
      });

      if (!res.ok) {
        throw new Error("Error cargando detalles");
      }

      const allCards = await res.json();

      // Luego obtener worklogs del usuario de esas tarjetas
      // Por simplicidad, hacemos una petición por cada tarjeta
      // (En producción, mejor crear endpoint específico /report/{board_id}/user/{user_id}/worklogs?week=)

      // Para demo, mostramos info básica
      const userWorklogs: WorklogDetail[] = allCards.map((card: any) => ({
        id: card.card_id,
        card_id: card.card_id,
        card_title: card.title,
        date: "N/A", // Necesitaríamos endpoint específico
        hours: card.total_hours,
        note: "Detalle completo requiere endpoint adicional",
      }));

      setWorklogs(userWorklogs);
    } catch (err: any) {
      setError(err.message || "Error cargando detalles");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: "white",
          borderRadius: "12px",
          padding: "2rem",
          maxWidth: "600px",
          width: "90%",
          maxHeight: "80vh",
          overflow: "auto",
          boxShadow: "0 20px 60px rgba(0, 0, 0, 0.3)",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "1.5rem",
            borderBottom: "2px solid #e5e7eb",
            paddingBottom: "1rem",
          }}
        >
          <h2 style={{ margin: 0, color: "#1e3a8a" }}>
            Detalle de {userName}
          </h2>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "none",
              fontSize: "1.5rem",
              cursor: "pointer",
              color: "#64748b",
            }}
          >
            ✕
          </button>
        </div>

        <p style={{ color: "#64748b", marginBottom: "1rem" }}>
          Semana: <strong>{week}</strong>
        </p>

        {loading && <p>Cargando detalles...</p>}
        {error && <p style={{ color: "#dc2626" }}>{error}</p>}

        {!loading && !error && (
          <>
            {worklogs.length === 0 ? (
              <p style={{ color: "#64748b", fontStyle: "italic" }}>
                No hay registros de horas para este usuario en la semana seleccionada.
              </p>
            ) : (
              <div>
                <p style={{ marginBottom: "1rem", fontSize: "0.875rem", color: "#64748b" }}>
                  <strong>Nota:</strong> Este es un detalle básico. Para ver worklogs completos
                  (fecha, nota por cada registro), se requiere un endpoint adicional en el backend.
                </p>
                <table
                  style={{
                    width: "100%",
                    borderCollapse: "collapse",
                    marginTop: "1rem",
                  }}
                >
                  <thead>
                    <tr style={{ background: "#f1f5f9", textAlign: "left" }}>
                      <th style={{ padding: "0.75rem", borderBottom: "2px solid #cbd5e1" }}>
                        Tarjeta
                      </th>
                      <th style={{ padding: "0.75rem", borderBottom: "2px solid #cbd5e1" }}>
                        Horas
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {worklogs.map((wl) => (
                      <tr key={wl.id} style={{ borderBottom: "1px solid #e5e7eb" }}>
                        <td style={{ padding: "0.75rem" }}>{wl.card_title || `Card ${wl.card_id}`}</td>
                        <td style={{ padding: "0.75rem", fontWeight: 600, color: "#2563eb" }}>
                          {typeof wl.hours === "string" ? wl.hours : wl.hours.toFixed(2)}h
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}

        <div style={{ marginTop: "2rem", textAlign: "right" }}>
          <button
            onClick={onClose}
            style={{
              padding: "0.75rem 1.5rem",
              background: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
}

