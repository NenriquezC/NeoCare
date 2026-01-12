/**
 * @file api.ts
 * Utilidades para consumir el backend FastAPI desde el frontend.
 * Centraliza la URL del backend y automatiza la gestión del token para autenticación.
 */

/**
 * URL base donde se encuentra desplegado el backend FastAPI.
 * Se toma de la variable de entorno VITE_API_URL
 */
export const BACKEND_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Hace una petición HTTP al backend, agregando automáticamente el token JWT del usuario (si existe).
 *
 * @param {string} path - Ruta relativa a la URL base del backend.
 * @param {RequestInit} [options={}] - Opciones para la función fetch (método, body, headers, etc).
 * @returns {Promise<Response>} - Respuesta HTTP del backend.
 *
 * Si hay un token en localStorage, se añade como cabecera Authorization.
 */
export async function apiFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = localStorage.getItem("token");

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${BACKEND_URL}${path}`, {
    ...options,
    headers,
  });

  return response;
}
