// src/pages/Boards.tsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";

const Boards: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const [showModal, setShowModal] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", due_date: "" });
  const [formError, setFormError] = useState<string | null>(null);
  const [selectedBoardId, setSelectedBoardId] = useState<number | null>(null);
  const [selectedListId, setSelectedListId] = useState<number | null>(null);
  const [selectedColumn, setSelectedColumn] = useState<string | null>(null);
  const [listIdByColumn, setListIdByColumn] = useState<Record<string, number>>({});
  const [cards, setCards] = useState<any[]>([]);
  const [editingCard, setEditingCard] = useState<any | null>(null);

  const columns = ["Por hacer", "En curso", "Hecho"];

  function badgeStyle(bg: string) {
    return {
      display: "inline-block",
      padding: "2px 8px",
      borderRadius: 999,
      fontSize: 12,
      fontWeight: 700 as const,
      background: bg,
      color: "white",
      border: "1px solid rgba(255,255,255,0.12)",
      lineHeight: 1.6,
    };
  }

  function parseYMD(dateStr: string | null | undefined): Date | null {
    if (!dateStr) return null;
    const s = String(dateStr).trim();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return null;
    const [y, m, d] = s.split("-").map((x) => Number(x));
    if (!y || !m || !d) return null;
    const dt = new Date(y, m - 1, d);
    if (dt.getFullYear() !== y || dt.getMonth() !== m - 1 || dt.getDate() !== d) return null;
    return dt;
  }

  function diffDays(a: Date, b: Date): number {
    const a0 = new Date(a.getFullYear(), a.getMonth(), a.getDate()).getTime();
    const b0 = new Date(b.getFullYear(), b.getMonth(), b.getDate()).getTime();
    return Math.round((a0 - b0) / (1000 * 60 * 60 * 24));
  }

  function getDueBadge(dueDateStr: any) {
    const due = parseYMD(dueDateStr);
    if (!due) return null;

    const today = new Date();
    const days = diffDays(due, today);

    if (days < 0) {
      return { text: "Vencida", style: badgeStyle("#7f1d1d") };
    }
    if (days === 0) {
      return { text: "Vence hoy", style: badgeStyle("#b45309") };
    }
    if (days <= 2) {
      return { text: "Vence pronto", style: badgeStyle("#1d4ed8") };
    }
    return { text: dueDateStr, style: badgeStyle("#334155") };
  }

  useEffect(() => {
    (async () => {
      try {
        const resBoards = await apiFetch("/boards/", { method: "GET" });
        if (!resBoards.ok) {
          const txt = await resBoards.text().catch(() => "");
          throw new Error(txt || `No se pudieron cargar boards (status ${resBoards.status})`);
        }
        const boards = await resBoards.json();

        if (!Array.isArray(boards) || boards.length === 0 || typeof boards[0]?.id !== "number") {
          setSelectedBoardId(null);
          setListIdByColumn({});
          setCards([]);
          setFormError(
            "No hay tablero disponible para tu usuario. Solución: inicia sesión con un usuario que tenga board o habilita creación automática en /auth/register."
          );
          return;
        }

        const boardId = boards[0].id as number;
        setSelectedBoardId(boardId);

        const resLists = await apiFetch(`/boards/${boardId}/lists`, { method: "GET" });
        if (!resLists.ok) {
          const txt = await resLists.text().catch(() => "");
          throw new Error(txt || `No se pudieron cargar lists (status ${resLists.status})`);
        }
        const lists = await resLists.json();

        const map: Record<string, number> = {};
        if (Array.isArray(lists)) {
          for (const l of lists) {
            if (l?.name && typeof l?.id === "number") map[l.name] = l.id;
          }
        }
        setListIdByColumn(map);

        const resCards = await apiFetch(`/cards/?board_id=${boardId}`, { method: "GET" });
        if (!resCards.ok) {
          const txt = await resCards.text().catch(() => "");
          throw new Error(txt || `No se pudieron cargar cards (status ${resCards.status})`);
        }
        const cardsData = await resCards.json();
        setCards(Array.isArray(cardsData) ? cardsData : []);
      } catch (err) {
        setSelectedBoardId(null);
        setListIdByColumn({});
        setCards([]);
        setFormError(err instanceof Error ? err.message : "Error cargando tableros/listas/tarjetas");
      }
    })();
  }, []);

  function openCreate(targetColumn: string = "Por hacer") {
    setEditingCard(null);
    setForm({ title: "", description: "", due_date: "" });
    setFormError(null);

    if (!selectedBoardId) {
      setFormError("No hay un tablero activo (board_id). Primero carga/crea un tablero.");
      setShowModal(true);
      return;
    }

    const mapEntries = Object.entries(listIdByColumn);
    const fallbackEntry = mapEntries.length > 0 ? mapEntries[0] : null;
    const realListId = listIdByColumn[targetColumn] ?? fallbackEntry?.[1];
    const realColumnName = listIdByColumn[targetColumn] ? targetColumn : fallbackEntry?.[0] ?? targetColumn;

    if (!realListId) {
      setFormError(`No existen listas cargadas para este tablero. Recarga la página o crea listas.`);
      setShowModal(true);
      return;
    }

    setSelectedListId(realListId);
    setSelectedColumn(realColumnName);
    setShowModal(true);
  }

  function openEdit(card: any) {
    setEditingCard(card);
    setForm({
      title: card?.title ?? "",
      description: card?.description ?? "",
      due_date: card?.due_date ?? "",
    });
    setFormError(null);

    setSelectedListId(card?.list_id ?? null);
    setShowModal(true);
  }

  function closeModal() {
    setShowModal(false);
    setFormError(null);
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);

    if (!form.title.trim()) {
      setFormError("El título es obligatorio.");
      return;
    }

    if (!selectedBoardId) {
      setFormError("No hay un tablero activo (board_id). Primero carga/crea un tablero.");
      return;
    }

    const targetColumn = selectedColumn || "Por hacer";
    const mapEntries = Object.entries(listIdByColumn);
    const fallbackEntry = mapEntries.length > 0 ? mapEntries[0] : null;
    const listId = listIdByColumn[targetColumn] ?? fallbackEntry?.[1] ?? null;
    if (!listId) {
      setFormError(`No existe la lista "${targetColumn}" en el tablero activo ni hay listas disponibles.`);
      return;
    }

    setSaving(true);
    try {
      const payload = {
        title: form.title.trim(),
        description: form.description.trim() || null,
        due_date: form.due_date || null,
        list_id: listId,
        board_id: selectedBoardId,
      };

      const res = await apiFetch("/cards", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(txt || `Error al crear tarjeta (status ${res.status})`);
      }

      const created = await res.json().catch(() => null);
      if (created) {
        setCards((prev) => [created, ...prev]);
      }

      closeModal();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Error creando tarjeta");
    } finally {
      setSaving(false);
    }
  }

  async function handleUpdate(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);

    if (!editingCard?.id) {
      setFormError("No hay tarjeta seleccionada para editar.");
      return;
    }

    if (!form.title.trim()) {
      setFormError("El título es obligatorio.");
      return;
    }

    setSaving(true);
    try {
      const payload = {
        title: form.title.trim(),
        description: form.description.trim() || null,
        due_date: form.due_date || null,
      };

      const res = await apiFetch(`/cards/${editingCard.id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(txt || `Error al editar tarjeta (status ${res.status})`);
      }

      const updated = await res.json().catch(() => null);
      if (updated) {
        setCards((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
      }

      closeModal();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Error editando tarjeta");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    setFormError(null);

    if (!editingCard?.id) {
      setFormError("No hay tarjeta seleccionada para eliminar.");
      return;
    }

    const ok = window.confirm("¿Eliminar esta tarjeta?");
    if (!ok) return;

    setSaving(true);
    try {
      const res = await apiFetch(`/cards/${editingCard.id}`, { method: "DELETE" });

      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(txt || `Error al eliminar tarjeta (status ${res.status})`);
      }

      setCards((prev) => prev.filter((c) => c.id !== editingCard.id));

      closeModal();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Error eliminando tarjeta");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        background: "linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%)",
        color: "#1e3a8a",
      }}
    >
      {/* Header */}
      <header
        style={{
          padding: "1rem 2rem",
          background: "linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        }}
      >
        <h1 style={{ color: "white", textShadow: "2px 2px 4px rgba(0, 0, 0, 0.6)" }}>NeoCare</h1>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <button
            onClick={() => openCreate("Por hacer")}
            style={{
              padding: "0.5rem 1rem",
              background: "linear-gradient(135deg, #0c4a6e 0%, #1e40af 100%)",
              border: "none",
              borderRadius: "0.5rem",
              color: "white",
              cursor: "pointer",
              textShadow: "1px 1px 2px rgba(0, 0, 0, 0.5)",
              fontWeight: "600",
              boxShadow: "0 4px 6px rgba(0, 0, 0, 0.2)",
            }}
          >
            + Nueva tarjeta
          </button>

          <button
            onClick={handleLogout}
            style={{
              padding: "0.5rem 1rem",
              background: "linear-gradient(135deg, #0c4a6e 0%, #1e40af 100%)",
              border: "none",
              borderRadius: "0.5rem",
              color: "white",
              cursor: "pointer",
              textShadow: "1px 1px 2px rgba(0, 0, 0, 0.5)",
              fontWeight: "600",
              boxShadow: "0 4px 6px rgba(0, 0, 0, 0.2)",
            }}
          >
            Cerrar sesión
          </button>
        </div>
      </header>

      {formError && <div style={{ padding: "10px 24px", color: "#fecaca" }}>{formError}</div>}

      {/* Contenido */}
      <main
        style={{
          flex: 1,
          display: "flex",
          gap: "1rem",
          padding: "1.5rem",
        }}
      >
        {columns.map((col) => {
          const listId = listIdByColumn[col];
          const colCards = listId ? cards.filter((c) => c?.list_id === listId) : [];

          return (
            <div
              key={col}
              style={{
                flex: 1,
                background: "rgba(255, 255, 255, 0.7)",
                borderRadius: "0.75rem",
                padding: "1rem",
                boxShadow: "0 8px 16px rgba(0, 0, 0, 0.15)",
                display: "flex",
                flexDirection: "column",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h2 style={{ marginBottom: "0.75rem", textShadow: "2px 2px 4px rgba(0, 0, 0, 0.6)", color: "white" }}>{col}</h2>
                <button
                  onClick={() => openCreate(col)}
                  style={{
                    padding: "0.35rem 0.6rem",
                    background: "linear-gradient(135deg, #0c4a6e 0%, #1e40af 100%)",
                    border: "none",
                    borderRadius: "0.5rem",
                    color: "white",
                    cursor: "pointer",
                    fontSize: "0.85rem",
                    textShadow: "1px 1px 2px rgba(0, 0, 0, 0.5)",
                    fontWeight: "600",
                    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.2)",
                  }}
                  title={`Crear tarjeta en "${col}"`}
                >
                  + Nueva
                </button>
              </div>

              <div
                style={{
                  flex: 1,
                  border: "2px dashed #93c5fd",
                  borderRadius: "0.75rem",
                  padding: "0.75rem",
                  fontSize: "0.9rem",
                  color: "#1e3a8a",
                  display: "flex",
                  flexDirection: "column",
                  gap: 8,
                }}
              >
                {!listId ? (
                  <div style={{ color: "#fecaca" }}>Listas aún no cargadas…</div>
                ) : colCards.length === 0 ? (
                  <div>(Sin tarjetas todavía)</div>
                ) : (
                  colCards.map((card) => {
                    const dueBadge = getDueBadge(card?.due_date);
                    return (
                      <button
                        key={card.id}
                        type="button"
                        onClick={() => openEdit(card)}
                        style={{
                          textAlign: "left",
                          background: "rgba(255, 255, 255, 0.9)",
                          border: "1px solid #93c5fd",
                          borderRadius: 10,
                          padding: 10,
                          color: "#1e3a8a",
                          cursor: "pointer",
                          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                        }}
                        title="Click para editar"
                      >
                        {/* Título */}
                        <div style={{ fontWeight: 800, fontSize: 14, textShadow: "1px 1px 2px rgba(128, 128, 128, 0.3)" }}>{card.title}</div>

                        {/* Badges: Estado + Fecha límite */}
                        <div style={{ marginTop: 8, display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
                          {/* Estado (columna actual) */}
                          <span style={badgeStyle("#1e40af")}>Estado: {col}</span>

                          {/* Fecha límite (badge) */}
                          {dueBadge ? (
                            <span style={dueBadge.style}>📅 {dueBadge.text}</span>
                          ) : (
                            <span style={badgeStyle("#334155")}>📅 Sin fecha</span>
                          )}
                        </div>

                        {/* Descripción */}
                        {card.description && (
                          <div style={{ color: "#1e3a8a", marginTop: 8, textShadow: "1px 1px 2px rgba(128, 128, 128, 0.2)" }}>
                            {card.description}
                          </div>
                        )}
                      </button>
                    );
                  })
                )}
              </div>
            </div>
          );
        })}
      </main>

      {/* Modal para crear/editar tarjeta */}
      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50">
          <div
            style={{
              background: "linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%)",
              color: "#1e3a8a",
              width: 540,
              borderRadius: 8,
              padding: 20,
              boxShadow: "0 10px 30px rgba(0, 0, 0, 0.2)",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
              <h3 style={{ margin: 0, textShadow: "1px 1px 2px rgba(128, 128, 128, 0.3)" }}>{editingCard ? "Editar tarjeta" : "Nueva tarjeta"}</h3>
              <button
                onClick={closeModal}
                style={{
                  background: "transparent",
                  border: "none",
                  color: "#1e3a8a",
                  fontSize: 18,
                }}
              >
                ✕
              </button>
            </div>

            <form onSubmit={editingCard ? handleUpdate : handleCreate}>
              <label style={{ display: "block", marginBottom: 6, color: "#1e40af", fontWeight: "600", textShadow: "1px 1px 2px rgba(128, 128, 128, 0.3)" }}>Título</label>
              <input
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                style={{
                  width: "100%",
                  padding: 8,
                  marginBottom: 10,
                  borderRadius: 6,
                  border: "1px solid #93c5fd",
                  background: "rgba(255, 255, 255, 0.8)",
                  color: "#1e3a8a",
                }}
              />

              <label style={{ display: "block", marginBottom: 6, color: "#1e40af", fontWeight: "600", textShadow: "1px 1px 2px rgba(128, 128, 128, 0.3)" }}>Descripción</label>
              <textarea
                rows={3}
                value={form.description}
                onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                style={{
                  width: "100%",
                  padding: 8,
                  marginBottom: 10,
                  borderRadius: 6,
                  border: "1px solid #93c5fd",
                  background: "rgba(255, 255, 255, 0.8)",
                  color: "#1e3a8a",
                }}
              />

              <label style={{ display: "block", marginBottom: 6, color: "#1e40af", fontWeight: "600", textShadow: "1px 1px 2px rgba(128, 128, 128, 0.3)" }}>Fecha límite</label>
              <input
                type="date"
                value={form.due_date}
                onChange={(e) => setForm((f) => ({ ...f, due_date: e.target.value }))}
                style={{
                  padding: 8,
                  marginBottom: 12,
                  borderRadius: 6,
                  border: "1px solid #93c5fd",
                  background: "rgba(255, 255, 255, 0.8)",
                  color: "#1e3a8a",
                }}
              />

              {formError && <div style={{ color: "#7f1d1d", marginBottom: 8, textShadow: "1px 1px 2px rgba(128, 128, 128, 0.3)" }}>{formError}</div>}

              <div style={{ display: "flex", gap: 8 }}>
                <button
                  type="submit"
                  disabled={saving}
                  style={{
                    padding: "0.5rem 1rem",
                    background: editingCard ? "#f59e0b" : "#10b981",
                    border: "none",
                    borderRadius: 6,
                    color: "white",
                  }}
                >
                  {saving ? (editingCard ? "Guardando…" : "Creando…") : editingCard ? "Guardar cambios" : "Crear tarjeta"}
                </button>

                <button
                  type="button"
                  onClick={closeModal}
                  style={{
                    padding: "0.5rem 1rem",
                    background: "#334155",
                    border: "none",
                    borderRadius: 6,
                    color: "white",
                  }}
                >
                  Cancelar
                </button>

                {editingCard && (
                  <button
                    type="button"
                    onClick={handleDelete}
                    disabled={saving}
                    style={{
                      padding: "0.5rem 1rem",
                      background: "#7f1d1d",
                      border: "none",
                      borderRadius: 6,
                      color: "white",
                    }}
                    title="Eliminar tarjeta"
                  >
                    Eliminar
                  </button>
                )}
              </div>

              <div style={{ marginTop: 10, fontSize: 12, color: "#94a3b8" }}>
                board_id: {selectedBoardId ?? "—"} | list_id: {selectedListId ?? "—"}
                {editingCard?.id ? ` | editing_card_id: ${editingCard.id}` : ""}
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Boards;
