// src/lib/auth.ts
import { apiFetch } from "./api";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type?: string;
}

export async function loginRequest(
  data: LoginPayload
): Promise<LoginResponse> {
  const response = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });

  // Si la API devuelve 401 u otro error, lanzamos excepción
  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(
      text || `Error en login (status ${response.status})`
    );
  }

  // Devolvemos el JSON (access_token, etc.)
  return response.json();
}
