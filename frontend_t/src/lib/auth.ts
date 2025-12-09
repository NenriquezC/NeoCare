/**
 * @file auth.ts
 * Funciones y tipos utilitarios para autenticación de usuarios en el frontend.
 * Gestiona la petición de login al backend y la estructura de datos relevante.
 */
// src/lib/auth.ts
import { apiFetch } from "./api";

/**
 * Estructura de datos enviada en la petición de login.
 */
export interface LoginPayload {
  email: string;
  password: string;
}

/**
 * Estructura esperada en la respuesta de login del backend.
 */
export interface LoginResponse {
  access_token: string;
  token_type?: string;
}

/**
 * Realiza la petición de login al backend FastAPI.
 *
 * @param {LoginPayload} data - Email y contraseña del usuario.
 * @returns {Promise<LoginResponse>} Respuesta con el token JWT y tipo.
 * @throws {Error} Si el backend responde con error (por ejemplo, credenciales incorrectas).
 */
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
