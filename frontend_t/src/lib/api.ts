// src/lib/api.ts

// URL donde tienes arrancado FastAPI
export const BACKEND_URL = "http://127.0.0.1:8000";
// (si prefieres, puedes usar "http://localhost:8000")

export async function apiFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = localStorage.getItem("token");

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
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
