import { apiFetch } from "./api";

/**
 * TIPOS
 * Ajusta nombres/campos si tu backend usa otros.
 */
export interface Worklog {
    id: number;
    user_id: number;
    card_id: number;
    date: string;      // "YYYY-MM-DD"
    hours: number;     // puede llegar como string si backend usa Decimal
    note?: string | null;
    created_at?: string;
    updated_at?: string;
}

export interface WorklogCreatePayload {
    card_id: number;
    date: string;     // "YYYY-MM-DD"
    hours: number;
    note?: string | null;
}

export interface WorklogUpdatePayload {
    date?: string;
    hours?: number;
    note?: string | null;
}

/**
 * ENDPOINTS
 * ⚠️ Esto puede variar según tu backend.
 * Lo dejé centralizado para que cambies aquí y no en 5 archivos.
 */
const ENDPOINTS = {
  // Lista worklogs de una tarjeta
    listByCard: (cardId: number) => `/cards/${cardId}/time-entries`,
  // Crear worklog
    create: () => `/time-entries`,
  // Editar / borrar worklog
    update: (id: number) => `/time-entries/${id}`,
    remove: (id: number) => `/time-entries/${id}`,

  // “Mis horas” por semana
  // Ej: /time-entries/me?week=2025-W52
  //myWeek: (week: string) => `/time-entries/me?week=${encodeURIComponent(week)}`,
    myWeek: (week: string) => `/worklogs/me/week?week=${encodeURIComponent(week)}`,




  // Obtener mi usuario (para saber si puedo editar/borrar)
    me: () => `/users/me`,
};

async function readJsonOrTextError(res: Response) {
    if (res.ok) return;
    const txt = await res.text().catch(() => "");
    throw new Error(txt || `Error HTTP ${res.status}`);
}

export async function getMe(): Promise<{ id: number } | null> {
    const res = await apiFetch(ENDPOINTS.me(), { method: "GET" });
    if (!res.ok) return null;
    const data = await res.json().catch(() => null);
    if (data && typeof data.id === "number") return { id: data.id };
    return null;
}

export async function listWorklogsByCard(cardId: number): Promise<Worklog[]> {
    const res = await apiFetch(ENDPOINTS.listByCard(cardId), { method: "GET" });
    await readJsonOrTextError(res);
    const data = await res.json().catch(() => []);
    return Array.isArray(data) ? data : [];
}

export async function createWorklog(payload: WorklogCreatePayload): Promise<Worklog> {
    const res = await apiFetch(ENDPOINTS.create(), {
            method: "POST",
        body: JSON.stringify(payload),
    });
    await readJsonOrTextError(res);
    return res.json();
}

export async function updateWorklog(id: number, payload: WorklogUpdatePayload): Promise<Worklog> {
    const res = await apiFetch(ENDPOINTS.update(id), {
        method: "PATCH",
        body: JSON.stringify(payload),
    });
    await readJsonOrTextError(res);
    return res.json();
}

export async function deleteWorklog(id: number): Promise<void> {
    const res = await apiFetch(ENDPOINTS.remove(id), { method: "DELETE" });
    await readJsonOrTextError(res);
}

export async function listMyWorklogsByWeek(week: string): Promise<Worklog[]> {
    const res = await apiFetch(ENDPOINTS.myWeek(week), { method: "GET" });
    await readJsonOrTextError(res);
    const data = await res.json().catch(() => []);
    return Array.isArray(data) ? data : [];
}

/**
 * Utilidad: convertir hours a number aunque venga como string/Decimal.
 */
export function hoursToNumber(v: unknown): number {
    if (typeof v === "number") return v;
    if (typeof v === "string") {
        const n = Number(v.replace(",", "."));
        return Number.isFinite(n) ? n : 0;
    }
    return 0;
}