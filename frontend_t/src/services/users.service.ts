import { apiFetch } from "@/lib/api";

export interface BoardUser {
  id: number;
  name: string | null;
  email: string;
  role?: string | null;
}

export async function getBoardUsers(boardId: number): Promise<BoardUser[]> {
  const res = await apiFetch(`/boards/${boardId}/users`);
  if (!res.ok) throw new Error("No se pudo obtener la lista de usuarios del tablero");
  return res.json();
}

