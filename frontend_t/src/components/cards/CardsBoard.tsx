import React, { useEffect, useState } from "react";

// ---------------------- Tipos ----------------------

export type CardListID = 1 | 2 | 3;

export interface Card {
  id: number;
  title: string;
  description?: string | null;
  due_date?: string | null;
  list_id: CardListID;
  board_id: number;
}

interface CardsBoardProps {
  boardId: number;
}

// ---------------------- Constantes ----------------------

const BASE_URL = "http://localhost:8000";

const LISTS: CardListID[] = [1, 2, 3];

const LIST_LABEL: Record<CardListID, string> = {
  1: "Por hacer",
  2: "En progreso",
  3: "Hecho",
};

// ---------------------- Componente principal ----------------------

export default function CardsBoard({ boardId }: CardsBoardProps) {
  // Estados
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tokenMissing, setTokenMissing] = useState(false);

  const [showModal, setShowModal] = useState(false);
  const [editingCard, setEditingCard] = useState<Card | null>(null);

  const [form, setForm] = useState({
    title: "",
    description: "",
    due_date: "",
    list_id: 1 as CardListID,
  });

  const [formErrors, setFormErrors] = useState<{
    title?: string;
    due_date?: string;
  }>({});

  // ---------------------- Obtener token ----------------------

  function getToken() {
    return localStorage.getItem("token");
  }

  // ---------------------- Obtener tarjetas ----------------------

  useEffect(() => {
    fetchCards();
  }, [boardId]);

  async function fetchCards() {
    setLoading(true);
    setError(null);

    const token = getToken();
    if (!token) {
      setTokenMissing(true);
      setLoading(false);
      return;
    }

    setTokenMissing(false);

    try {
      const res = await fetch(
        `${BASE_URL}/cards?board_id=${encodeURIComponent(boardId)}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (!res.ok) throw new Error("Error al obtener tarjetas");

      const data = await res.json();
      setCards(data || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error cargando tarjetas");
    } finally {
      setLoading(false);
    }
  }

  // ---------------------- Crear tarjeta ----------------------

  function openCreate() {
    setEditingCard(null);
    setForm({
      title: "",
      description: "",
      due_date: "",
      list_id: 1,
    });
    setFormErrors({});
    setShowModal(true);
  }

  // ---------------------- Editar tarjeta ----------------------

  function openEdit(card: Card) {
    setEditingCard(card);
    setForm({
      title: card.title,
      description: card.description || "",
      due_date: card.due_date ? card.due_date.split("T")[0] : "",
      list_id: card.list_id,
    });
    setShowModal(true);
  }

  function closeModal() {
    setShowModal(false);
    setEditingCard(null);
    setFormErrors({});
  }

  // ---------------------- Validación ----------------------

  function validateForm() {
    const errors: any = {};

    if (!form.title.trim()) {
      errors.title = "El título es obligatorio.";
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  }

  // ---------------------- Guardar tarjeta ----------------------

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!validateForm()) return;

    setSaving(true);
    setError(null);

    const token = getToken();
    if (!token) {
      setTokenMissing(true);
      setSaving(false);
      return;
    }

    const payload = {
      title: form.title.trim(),
      description: form.description.trim() || null,
      due_date: form.due_date || null,
      list_id: form.list_id,
      board_id: boardId,
    };

    try {
      const url = editingCard
        ? `${BASE_URL}/cards/${editingCard.id}`
        : `${BASE_URL}/cards`;

      const method = editingCard ? "PATCH" : "POST";

      const res = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Error al guardar tarjeta");

      await fetchCards();
      closeModal();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error guardando tarjeta");
    } finally {
      setSaving(false);
    }
  }

  // ---------------------- Cálculo de badges ----------------------

  function calculateDaysUntil(dateStr: string | null | undefined) {
    if (!dateStr) return null;
    const now = new Date();
    const due = new Date(dateStr);
    return Math.ceil((due.getTime() - now.getTime()) / 86400000);
  }

  function deadlineBadge(dateStr: string | null | undefined) {
    const days = calculateDaysUntil(dateStr);
    if (days === null) return null;

    if (days < 0)
      return (
        <span className="px-2 py-0.5 text-xs rounded-full bg-red-600 text-white">
          Vencida
        </span>
      );

    if (days <= 3)
      return (
        <span className="px-2 py-0.5 text-xs rounded-full bg-yellow-500 text-white">
          {days} d
        </span>
      );

    return (
      <span className="px-2 py-0.5 text-xs rounded-full bg-gray-200 text-gray-800">
        {days} d
      </span>
    );
  }

  // ---------------------- Agrupar tarjetas ----------------------

  const grouped: Record<CardListID, Card[]> = LISTS.reduce<
    Record<CardListID, Card[]>
  >(
    (acc, list) => {
      acc[list] = cards.filter((c) => c.list_id === list);
      return acc;
    },
    { 1: [], 2: [], 3: [] } as Record<CardListID, Card[]>
  );

  // ---------------------- Render ----------------------

  return (
    <div className="p-4">
      {/* HEADER */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold">Tarjetas</h2>

        <div className="flex items-center gap-3">
          <button
            className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
            onClick={openCreate}
          >
            + Nueva tarjeta
          </button>

          <button
            className="px-3 py-1 bg-gray-200 text-gray-700 rounded"
            onClick={fetchCards}
            disabled={loading}
          >
            {loading ? "Cargando..." : "Actualizar"}
          </button>
        </div>
      </div>

      {/* TOKEN FALTANTE */}
      {tokenMissing && (
        <div className="mb-4 p-3 bg-yellow-100 text-yellow-800 rounded border border-yellow-300">
          No se encontró el token JWT. Inicia sesión para continuar.
        </div>
      )}

      {/* ERROR */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded border border-red-300">
          {error}
        </div>
      )}

      {/* COLUMNAS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {LISTS.map((list) => (
          <div key={list} className="bg-white rounded shadow p-3">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-medium text-lg">{LIST_LABEL[list]}</h3>
              <span className="text-sm text-gray-500">
                {grouped[list].length}
              </span>
            </div>

            <div className="flex flex-col gap-3">
              {grouped[list].length === 0 ? (
                <p className="text-sm text-gray-500">No hay tarjetas.</p>
              ) : (
                grouped[list].map((card) => (
                  <article
                    key={card.id}
                    className="p-3 border rounded hover:shadow cursor-pointer"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-semibold">{card.title}</h4>
                        {card.description && (
                          <p className="text-sm text-gray-600 mt-1">
                            {card.description}
                          </p>
                        )}
                      </div>

                      <div className="flex flex-col items-end gap-1">
                        {deadlineBadge(card.due_date)}

                        <button
                          className="text-blue-600 underline text-sm"
                          onClick={() => openEdit(card)}
                        >
                          Editar
                        </button>
                      </div>
                    </div>
                  </article>
                ))
              )}
            </div>
          </div>
        ))}
      </div>

      {/* MODAL */}
      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50">
          <div className="bg-white w-full max-w-xl rounded shadow-lg">
            <div className="flex justify-between items-center p-4 border-b">
              <h3 className="text-lg font-medium">
                {editingCard ? "Editar tarjeta" : "Nueva tarjeta"}
              </h3>
              <button
                onClick={closeModal}
                className="text-gray-500 text-xl leading-none"
              >
                ✕
              </button>
            </div>

            <form className="p-4 space-y-4" onSubmit={handleSave}>
              {/* TITULO */}
              <div>
                <label className="block text-sm font-medium">
                  Título <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={form.title}
                  maxLength={80}
                  required
                  onChange={(e) =>
                    setForm((f) => ({ ...f, title: e.target.value }))
                  }
                  className={`mt-1 w-full border rounded px-3 py-2 ${
                    formErrors.title ? "border-red-500" : "border-gray-300"
                  }`}
                />
                {formErrors.title && (
                  <p className="text-sm text-red-600 mt-1">
                    {formErrors.title}
                  </p>
                )}
              </div>

              {/* DESCRIPCION */}
              <div>
                <label className="block text-sm font-medium">Descripción</label>
                <textarea
                  rows={3}
                  value={form.description}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, description: e.target.value }))
                  }
                  className="mt-1 w-full border rounded px-3 py-2 border-gray-300"
                />
              </div>

              {/* FECHA + LISTA */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium">Fecha límite</label>
                  <input
                    type="date"
                    value={form.due_date}
                    onChange={(e) =>
                      setForm((f) => ({ ...f, due_date: e.target.value }))
                    }
                    className="mt-1 w-full border rounded px-3 py-2 border-gray-300"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium">Estado</label>
                  <select
                    value={form.list_id}
                    onChange={(e) =>
                      setForm((f) => ({
                        ...f,
                        list_id: Number(e.target.value) as CardListID,
                      }))
                    }
                    className="mt-1 w-full border rounded px-3 py-2 border-gray-300"
                  >
                    {LISTS.map((id) => (
                      <option key={id} value={id}>
                        {LIST_LABEL[id]}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* BOTONES */}
              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={saving}
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  {saving
                    ? "Guardando…"
                    : editingCard
                    ? "Guardar cambios"
                    : "Crear tarjeta"}
                </button>

                <button
                  type="button"
                  onClick={closeModal}
                  disabled={saving}
                  className="px-4 py-2 bg-gray-200 rounded"
                >
                  Cancelar
                </button>
              </div>

              {error && (
                <p className="text-red-600 text-sm mt-2">{error}</p>
              )}
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
