/**
 * Tipos del módulo Report — Semana 5
 *
 * Este archivo define los contratos TypeScript que representan
 * exactamente las respuestas del backend del módulo Report.
 *
 * Regla:
 * - Estos tipos deben reflejar el backend 1:1
 * - No contienen lógica
 * - No contienen llamadas HTTP
 */

/* =========================
   SUMMARY
   ========================= */

/**
 * Tarjeta básica usada en los listados del resumen semanal.
 */
export interface ReportCardItem {
  id: number;
  title: string;
  responsible_id: number | null;
}

/**
 * Bloque genérico del resumen semanal.
 */
export interface ReportSummaryBlock {
  count: number;
  items: ReportCardItem[];
}

/**
 * Respuesta completa del endpoint:
 * GET /report/{board_id}/summary
 */
export interface WeeklySummaryResponse {
  completed: ReportSummaryBlock;
  new: ReportSummaryBlock;
  overdue: ReportSummaryBlock;
}

/* =========================
   HOURS BY USER
   ========================= */

/**
 * Fila del reporte de horas por usuario.
 */
export interface HoursByUserItem {
  user_id: number;
  user_name: string;
  total_hours: number;
  tasks_count: number;
}

/* =========================
   HOURS BY CARD
   ========================= */

/**
 * Fila del reporte de horas por tarjeta.
 */
export interface HoursByCardItem {
  card_id: number;
  title: string;
  responsible: string | null;
  status: string;
  total_hours: number;
}