import { apiFetch } from "@/lib/api";

import type {
  WeeklySummaryResponse,
  HoursByCardItem,
} from "@/types/report";

/**
 * Backend REAL (según Swagger):
 * GET /api/boards/report/{board_id}/summary?week=YYYY-WW
 */
export async function getWeeklySummary(
  boardId: number,
  week: string
): Promise<WeeklySummaryResponse> {
  const response = await apiFetch(
    `/boards/report/${boardId}/summary?week=${week}`
  );

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json();
}

/**
 * Backend REAL (según Swagger):
 * GET /api/boards/report/{board_id}/hours-by-card?week=YYYY-WW
 */
export async function getHoursByCard(
  boardId: number,
  week: string
): Promise<HoursByCardItem[]> {
  const response = await apiFetch(
    `/boards/report/${boardId}/hours-by-card?week=${week}`
  );

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json();
}