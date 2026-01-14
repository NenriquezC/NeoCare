import { apiFetch } from "@/lib/api";

import type {
  WeeklySummaryResponse,
  HoursByCardItem,
  HoursByUserItem,
} from "@/types/report";

/**
 * GET /report/{board_id}/summary?week=YYYY-WW
 */
export async function getWeeklySummary(
  boardId: number,
  week: string
): Promise<WeeklySummaryResponse> {
  const response = await apiFetch(
    `/report/${boardId}/summary?week=${week}`
  );

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json();
}

/**
 * GET /report/{board_id}/hours-by-card?week=YYYY-WW
 */
export async function getHoursByCard(
  boardId: number,
  week: string
): Promise<HoursByCardItem[]> {
  const response = await apiFetch(
    `/report/${boardId}/hours-by-card?week=${week}`
  );

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json();
}

/**
 * GET /report/{board_id}/hours-by-user?week=YYYY-WW
 */
export async function getHoursByUser(
  boardId: number,
  week: string
): Promise<HoursByUserItem[]> {
  const response = await apiFetch(
    `/report/${boardId}/hours-by-user?week=${week}`
  );

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json();
}
