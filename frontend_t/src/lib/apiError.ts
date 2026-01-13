// Centraliza el parseo y manejo de errores de la API NeoCare
export interface ApiError {
  error: string;
  [key: string]: any;
}

export async function parseApiError(response: Response): Promise<ApiError> {
  let data: any = {};
  try {
    data = await response.json();
  } catch {
    data = { error: response.statusText || "Error desconocido" };
  }
  return {
    error: data.error || data.detail || "Error desconocido",
    ...data,
  };
}

// Lanza si la respuesta no es ok, para usar en flujos async/await
export async function throwIfError(response: Response): Promise<Response> {
  if (!response.ok) {
    const err = await parseApiError(response);
    throw err;
  }
  return response;
}
