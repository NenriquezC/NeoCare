/**
 * Página Report — Semana 5
 *
 * Informe semanal de un tablero Kanban.
 */

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getWeeklySummary, getHoursByCard } from "@/services/report.service";
import { parseApiError } from "@/lib/apiError";

import type {
  WeeklySummaryResponse,
  HoursByCardItem,
} from "@/types/report";

import SummaryCards from "@/components/report/SummaryCards";
import HoursByCardTable from "@/components/report/HoursByCardTable";

/**
 * Devuelve la semana actual en formato ISO YYYY-WW.
 */
function getCurrentWeek(): string {
  const now = new Date();
  const firstDayOfYear = new Date(now.getFullYear(), 0, 1);
  const pastDaysOfYear =
    (now.getTime() - firstDayOfYear.getTime()) / 86400000;

  const week = Math.ceil(
    (pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7
  );

  return `${now.getFullYear()}-W${String(week).padStart(2, "0")}`;
}

export default function ReportPage() {
  const navigate = useNavigate();
  const { boardId } = useParams<{ boardId: string }>();

  if (!boardId) {
    return <p>Tablero no encontrado</p>;
  }

  const numericBoardId = Number(boardId);

  /* =========================
     STATE
     ========================= */
  const [week, setWeek] = useState<string>(getCurrentWeek());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [summary, setSummary] = useState<WeeklySummaryResponse | null>(null);
  const [hoursByCard, setHoursByCard] = useState<HoursByCardItem[]>([]);

  /* =========================
     DATA LOADING
     ========================= */
  async function loadReport() {
    setLoading(true);
    setError(null);

    try {
      const [summaryData, byCardData] = await Promise.all([
        getWeeklySummary(numericBoardId, week),
        getHoursByCard(numericBoardId, week),
      ]);

      setSummary(summaryData);
      setHoursByCard(byCardData);
    } catch (err: any) {
      if (err && err.error) setError(err.error);
      else if (err instanceof Error && (err.message.includes('{"detail":"Not Found"}') || err.message.includes('Not Found')))
        setError("No hay datos para la semana seleccionada o el reporte no está disponible.");
      else setError(err instanceof Error ? err.message : "Error inesperado al cargar el reporte");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadReport();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [numericBoardId, week]);

  /* =========================
     RENDER
     ========================= */
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        background:
          "linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%)",
        color: "#1e3a8a",
      }}
    >
      {/* HEADER — MISMO QUE BOARDS */}
      <header
        style={{
          padding: "1rem 2rem",
          background:
            "linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        }}
      >
        <h1
          style={{
            color: "white",
            textShadow: "2px 2px 4px rgba(0, 0, 0, 0.6)",
          }}
        >
          NeoCare
        </h1>

        <div style={{ display: "flex", gap: 12 }}>
          <button
            onClick={() => navigate(-1)}
            style={{
              padding: "0.5rem 1rem",
              background:
                "linear-gradient(135deg, #0c4a6e 0%, #1e40af 100%)",
              border: "none",
              borderRadius: "0.5rem",
              color: "white",
              cursor: "pointer",
              fontWeight: 600,
              boxShadow: "0 4px 6px rgba(0, 0, 0, 0.2)",
            }}
          >
            ← Volver
          </button>
        </div>
      </header>

      {/* CONTENIDO — MISMO ESTILO */}
      <main
        style={{
          flex: 1,
          padding: "1.5rem",
          display: "flex",
          flexDirection: "column",
          gap: "1.5rem",
        }}
      >
        {/* Selector de semana */}
        <div>
          <label style={{ fontWeight: 600 }}>
            Semana:&nbsp;
            <input
              type="week"
              value={week}
              onChange={(e) => setWeek(e.target.value)}
              style={{
                marginLeft: 8,
                padding: 6,
                borderRadius: 6,
                border: "1px solid #93c5fd",
              }}
            />
          </label>
        </div>

        {loading && <p>Cargando reporte…</p>}
        {error && <p style={{ color: "#7f1d1d" }}>{error}</p>}

        {!loading && !error && summary && (
          <>
            <SummaryCards summary={summary} />

            <h2>Horas por tarjeta</h2>
            <HoursByCardTable data={hoursByCard} />
          </>
        )}
      </main>
    </div>
  );
}