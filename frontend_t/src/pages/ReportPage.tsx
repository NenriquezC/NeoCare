/**
 * Página Report — Semana 5
 *
 * Informe semanal de un tablero Kanban.
 */

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  getWeeklySummary,
  getHoursByCard,
  getHoursByUser,
} from "@/services/report.service";

import type {
  WeeklySummaryResponse,
  HoursByCardItem,
  HoursByUserItem,
} from "@/types/report";

import SummaryCards from "@/components/report/SummaryCards";
import HoursByCardTable from "@/components/report/HoursByCardTable";
import HoursByUserTable from "@/components/report/HoursByUserTable";

/**
 * Devuelve la semana actual en formato ISO YYYY-WW según ISO 8601.
 * La semana ISO comienza en lunes y la semana 1 es la primera con jueves del año.
 */
function getCurrentWeek(): string {
  const now = new Date();

  // Copiar fecha para no mutar
  const target = new Date(now.valueOf());

  // Ajustar al jueves de la semana ISO (jueves = día 4)
  const dayNum = (target.getDay() + 6) % 7; // Lunes=0, Domingo=6
  target.setDate(target.getDate() - dayNum + 3);

  // Primer jueves del año
  const firstThursday = new Date(target.getFullYear(), 0, 4);
  const dayOffset = (firstThursday.getDay() + 6) % 7;
  firstThursday.setDate(firstThursday.getDate() - dayOffset + 3);

  // Calcular diferencia en semanas
  const weekNumber = Math.ceil((target.getTime() - firstThursday.getTime()) / (7 * 24 * 60 * 60 * 1000)) + 1;

  // El año ISO puede diferir del año calendario
  const isoYear = target.getFullYear();

  // Formato YYYY-WW (sin la letra W en el medio)
  return `${isoYear}-${String(weekNumber).padStart(2, "0")}`;
}

function exportToCsv(filename: string, rows: any[]) {
  if (!rows.length) return;
  const header = Object.keys(rows[0]);
  const csv = [
    header.join(","),
    ...rows.map((row) =>
      header
        .map((field) => {
          const value = (row as any)[field] ?? "";
          // Escape commas and quotes in CSV
          return typeof value === "string" && (value.includes(",") || value.includes('"'))
            ? `"${value.replace(/"/g, '""')}"`
            : JSON.stringify(value);
        })
        .join(",")
    ),
  ].join("\r\n");

  // UTF-8 BOM para Excel
  const blob = new Blob(["\ufeff" + csv], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
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
  const [hoursByUser, setHoursByUser] = useState<HoursByUserItem[]>([]);

  /* =========================
     DATA LOADING
     ========================= */
  async function loadReport() {
    setLoading(true);
    setError(null);

    try {
      const [summaryData, byCardData, byUserData] = await Promise.all([
        getWeeklySummary(numericBoardId, week),
        getHoursByCard(numericBoardId, week),
        getHoursByUser(numericBoardId, week),
      ]);

      setSummary(summaryData);
      setHoursByCard(byCardData);
      setHoursByUser(byUserData);
    } catch (err: any) {
      if (err && err.error) setError(err.error);
      else if (
        err instanceof Error &&
        (err.message.includes('{"detail":"Not Found"}') ||
          err.message.includes("Not Found"))
      )
        setError(
          "No hay datos para la semana seleccionada o el reporte no está disponible."
        );
      else
        setError(
          err instanceof Error ? err.message : "Error inesperado al cargar el reporte"
        );
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
            Semana (YYYY-WW):&nbsp;
            <input
              type="text"
              value={week}
              onChange={(e) => setWeek(e.target.value)}
              placeholder="2026-03"
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

            <h2>Horas por usuario</h2>
            <button
              onClick={() =>
                exportToCsv(`horas-por-usuario-${week}.csv`, hoursByUser)
              }
              style={{
                marginBottom: 12,
                padding: "0.5rem 1rem",
                background: "#2563eb",
                color: "white",
                border: "none",
                borderRadius: 6,
                cursor: "pointer",
                fontWeight: 600,
              }}
              disabled={!hoursByUser.length}
            >
              Exportar CSV
            </button>
            <HoursByUserTable data={hoursByUser} />

            <h2>Horas por tarjeta</h2>
            <button
              onClick={() =>
                exportToCsv(`horas-por-tarjeta-${week}.csv`, hoursByCard)
              }
              style={{
                marginBottom: 12,
                padding: "0.5rem 1rem",
                background: "#2563eb",
                color: "white",
                border: "none",
                borderRadius: 6,
                cursor: "pointer",
                fontWeight: 600,
              }}
              disabled={!hoursByCard.length}
            >
              Exportar CSV
            </button>
            <HoursByCardTable data={hoursByCard} />
          </>
        )}
      </main>
    </div>
  );
}