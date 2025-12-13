// src/pages/Boards.tsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";

/**
 * Componente principal del tablero "Boards".
 *
 * Muestra un tablero con columnas (Por hacer, En curso, Hecho), permite abrir
 * un modal para crear una nueva tarjeta y manejar el cierre de sesión.
 *
 * No modifica la lógica original del componente, los comentarios se han añadido
 * únicamente para documentar el comportamiento y las funciones internas.
 */
const Boards: React.FC = () => {
  const navigate = useNavigate();

  /**
   * handleLogout
   *
   * Elimina el token almacenado en localStorage y redirige al usuario a la pantalla
   * de login. No realiza llamadas externas, solo gestiona el estado local y la navegación.
   */
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  /**
   * showModal
   *
   * Estado booleano que controla si el modal de creación de tarjeta está visible.
   */
  const [showModal, setShowModal] = useState(false);

  /**
   * saving
   *
   * Estado booleano que indica si se está guardando (envío en curso) la tarjeta.
   * Se usa para deshabilitar el botón de envío y mostrar texto indicativo.
   */
  const [saving, setSaving] = useState(false);

  /**
   * form
   *
   * Estado que contiene los campos del formulario de creación/edición de tarjeta:
   * - title: título de la tarjeta
   * - description: descripción opcional
   * - due_date: fecha límite en formato YYYY-MM-DD (cadena vacía si no hay fecha)
   */
  const [form, setForm] = useState({ title: "", description: "", due_date: "" });

  /**
   * formError
   *
   * Mensaje de error relacionado con la validación o fallo del envío del formulario.
   * Puede ser null cuando no hay error.
   */
  const [formError, setFormError] = useState<string | null>(null);

  /**
   * selectedBoardId
   *
   * ID del tablero "activo" del usuario. Se carga desde el backend con GET /boards/.
   * Si es null, todavía no se ha podido determinar un tablero válido para operar.
   */
  const [selectedBoardId, setSelectedBoardId] = useState<number | null>(null);

  /**
   * selectedListId
   *
   * ID de la lista (columna) donde se creará la tarjeta.
   * Se asigna al abrir el modal desde una columna.
   */
  const [selectedListId, setSelectedListId] = useState<number | null>(null);

  /**
   * listIdByColumn
   *
   * Mapa nombre_columna -> id_lista real en BD.
   * Se carga desde el backend con GET /boards/{board_id}/lists
   */
  const [listIdByColumn, setListIdByColumn] = useState<Record<string, number>>({});

  /**
   * cards
   *
   * Tarjetas del tablero activo. Se renderizan por columna comparando card.list_id.
   */
  const [cards, setCards] = useState<any[]>([]);

  /**
   * editingCard
   *
   * Si contiene una tarjeta, el modal actúa en modo "editar".
   * Si es null, el modal actúa en modo "crear".
   */
  const [editingCard, setEditingCard] = useState<any | null>(null);

  /**
   * columns
   *
   * Array con los nombres de las columnas que se renderizan en el tablero.
   * Actualmente se usan nombres estáticos: "Por hacer", "En curso" y "Hecho".
   */
  const columns = ["Por hacer", "En curso", "Hecho"];

  /**
   * Helpers: badges por estado y por fecha límite.
   */
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

  // Convierte YYYY-MM-DD -> Date (00:00 local), o null si inválida
  function parseYMD(dateStr: string | null | undefined): Date | null {
    if (!dateStr) return null;
    const s = String(dateStr).trim();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return null;
    const [y, m, d] = s.split("-").map((x) => Number(x));
    if (!y || !m || !d) return null;
    const dt = new Date(y, m - 1, d);
    // Validación fuerte (evita 2025-02-31)
    if (dt.getFullYear() !== y || dt.getMonth() !== m - 1 || dt.getDate() !== d) return null;
    return dt;
  }

  // Diferencia en días entre "a" y "b" ignorando hora (a - b)
  function diffDays(a: Date, b: Date): number {
    const a0 = new Date(a.getFullYear(), a.getMonth(), a.getDate()).getTime();
    const b0 = new Date(b.getFullYear(), b.getMonth(), b.getDate()).getTime();
    return Math.round((a0 - b0) / (1000 * 60 * 60 * 24));
  }

  // Badge para due_date: vencida / hoy / pronto (<=2 días)
  function getDueBadge(dueDateStr: any) {
    const due = parseYMD(dueDateStr);
    if (!due) return null;

    const today = new Date();
    const days = diffDays(due, today); // due - today

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

  /**
   * Carga inicial de tablero (board_id) + listas del tablero (list_id) + tarjetas
   *
   * 1) GET /boards/ -> selecciona el primer board del usuario.
   * 2) GET /boards/{id}/lists -> crea el mapa nombre_columna -> list_id real.
   * 3) GET /cards/?board_id={id} -> trae tarjetas y las muestra por columna.
   */
  useEffect(() => {
    (async () => {
      try {
        // 1) Cargar tableros del usuario
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

        // 2) Cargar listas reales del tablero activo
        // Importante: backend acepta /lists y /lists/; usamos sin slash final por consistencia
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

        // 3) Cargar tarjetas del tablero activo
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

  /**
   * openCreate
   *
   * Abre el modal en modo "crear" y define el destino (list_id) según columna.
   */
  function openCreate(targetColumn: string = "Por hacer") {
    setEditingCard(null); // modo crear
    setForm({ title: "", description: "", due_date: "" });
    setFormError(null);

    if (!selectedBoardId) {
      setFormError("No hay un tablero activo (board_id). Primero carga/crea un tablero.");
      setShowModal(true);
      return;
    }

    const realListId = listIdByColumn[targetColumn];
    if (!realListId) {
      setFormError(`No existe la lista "${targetColumn}" en el tablero activo.`);
      setShowModal(true);
      return;
    }

    setSelectedListId(realListId);
    setShowModal(true);
  }

  /**
   * openEdit
   *
   * Abre el modal en modo "editar" precargando el formulario con la tarjeta.
   */
  function openEdit(card: any) {
    setEditingCard(card); // modo editar
    setForm({
      title: card?.title ?? "",
      description: card?.description ?? "",
      due_date: card?.due_date ?? "",
    });
    setFormError(null);

    // Para editar, fijamos selectedListId al list_id actual de la tarjeta
    setSelectedListId(card?.list_id ?? null);
    setShowModal(true);
  }

  /**
   * closeModal
   *
   * Oculta el modal y limpia el mensaje de error.
   */
  function closeModal() {
    setShowModal(false);
    setFormError(null);
  }

  /**
   * handleCreate
   *
   * Crea una tarjeta (POST /cards). Al crear correctamente, la añade al estado `cards`.
   */
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

    if (!selectedListId) {
      setFormError("No hay una columna/lista seleccionada (list_id).");
      return;
    }

    setSaving(true);
    try {
      const payload = {
        title: form.title.trim(),
        description: form.description.trim() || null,
        due_date: form.due_date || null,
        list_id: selectedListId,
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

  /**
   * handleUpdate
   *
   * Edita una tarjeta existente (PUT /cards/{id}).
   * Al editar correctamente, reemplaza la tarjeta en el estado `cards`.
   */
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

  // ✅ NUEVO: handleDelete (DELETE /cards/{id})
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

      // Quitamos del estado para que desaparezca del UI sin recargar
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
        background: "#020617",
        color: "white",
      }}
    >
      {/* Header */}
      <header
        style={{
          padding: "1rem 2rem",
          background: "#0f172a",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1>NeoCare – Tablero de Innovación</h1>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <button
            onClick={() => openCreate("Por hacer")}
            style={{
              padding: "0.5rem 1rem",
              background: "#1e40af",
              border: "none",
              borderRadius: "0.5rem",
              color: "white",
              cursor: "pointer",
            }}
          >
            + Nueva tarjeta
          </button>

          <button
            onClick={handleLogout}
            style={{
              padding: "0.5rem 1rem",
              background: "#f97316",
              border: "none",
              borderRadius: "0.5rem",
              color: "white",
              cursor: "pointer",
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
                background: "#0b1120",
                borderRadius: "0.75rem",
                padding: "1rem",
                boxShadow: "0 5px 15px rgba(0,0,0,0.4)",
                display: "flex",
                flexDirection: "column",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h2 style={{ marginBottom: "0.75rem" }}>{col}</h2>
                <button
                  onClick={() => openCreate(col)}
                  style={{
                    padding: "0.35rem 0.6rem",
                    background: "#1e40af",
                    border: "none",
                    borderRadius: "0.5rem",
                    color: "white",
                    cursor: "pointer",
                    fontSize: "0.85rem",
                  }}
                  title={`Crear tarjeta en "${col}"`}
                >
                  + Nueva
                </button>
              </div>

              <div
                style={{
                  flex: 1,
                  border: "2px dashed #1e293b",
                  borderRadius: "0.75rem",
                  padding: "0.75rem",
                  fontSize: "0.9rem",
                  color: "#94a3b8",
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
                          background: "#0f172a",
                          border: "1px solid #1e293b",
                          borderRadius: 10,
                          padding: 10,
                          color: "white",
                          cursor: "pointer",
                        }}
                        title="Click para editar"
                      >
                        {/* Título */}
                        <div style={{ fontWeight: 800, fontSize: 14 }}>{card.title}</div>

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
                          <div style={{ color: "#cbd5e1", marginTop: 8 }}>
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
              background: "#0b1220",
              color: "white",
              width: 540,
              borderRadius: 8,
              padding: 20,
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
              <h3 style={{ margin: 0 }}>{editingCard ? "Editar tarjeta" : "Nueva tarjeta"}</h3>
              <button
                onClick={closeModal}
                style={{
                  background: "transparent",
                  border: "none",
                  color: "white",
                  fontSize: 18,
                }}
              >
                ✕
              </button>
            </div>

            <form onSubmit={editingCard ? handleUpdate : handleCreate}>
              <label style={{ display: "block", marginBottom: 6 }}>Título</label>
              <input
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                style={{
                  width: "100%",
                  padding: 8,
                  marginBottom: 10,
                  borderRadius: 6,
                  border: "1px solid #334155",
                  background: "#071025",
                  color: "white",
                }}
              />

              <label style={{ display: "block", marginBottom: 6 }}>Descripción</label>
              <textarea
                rows={3}
                value={form.description}
                onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                style={{
                  width: "100%",
                  padding: 8,
                  marginBottom: 10,
                  borderRadius: 6,
                  border: "1px solid #334155",
                  background: "#071025",
                  color: "white",
                }}
              />

              <label style={{ display: "block", marginBottom: 6 }}>Fecha límite</label>
              <input
                type="date"
                value={form.due_date}
                onChange={(e) => setForm((f) => ({ ...f, due_date: e.target.value }))}
                style={{
                  padding: 8,
                  marginBottom: 12,
                  borderRadius: 6,
                  border: "1px solid #334155",
                  background: "#071025",
                  color: "white",
                }}
              />

              {formError && <div style={{ color: "#fecaca", marginBottom: 8 }}>{formError}</div>}

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

                {/* ✅ botón Eliminar SOLO en modo editar */}
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

/*
CAMBIOS REALIZADOS (PUNTO 2: EDITAR) Y POR QUÉ:

1) Se añadió estado `editingCard`:
   - Sirve para distinguir si el modal está creando o editando.

2) Se añadió `openEdit(card)`:
   - Abre el modal precargando title/description/due_date con la tarjeta clickeada.

3) Se añadió `handleUpdate()`:
   - Hace PUT /cards/{id} con los campos editados.
   - Actualiza `cards` reemplazando la tarjeta editada para que se vea al instante.

4) Se cambió el render de cada card a un <button> clickeable:
   - Click en la tarjeta => editar (sin agregar botones extra ni ensuciar UI).

5) El <form> del modal decide:
   - Si `editingCard` existe => submit llama a handleUpdate
   - Si no existe => submit llama a handleCreate
*/

/*
CAMBIOS REALIZADOS Y POR QUÉ:

1) Se añadió estado `cards` y una carga real:
   - GET /cards/?board_id=... para mostrar tarjetas en el UI.
   - Antes SIEMPRE se mostraba "(Sin tarjetas todavía)" aunque existieran.

2) En el useEffect se añadió el paso 3 (cargar cards) después de cargar board y listas.
   - Esto hace que al entrar al tablero se pinten tarjetas existentes.

3) En handleCreate, tras POST /cards, se hace `setCards((prev) => [created, ...prev])`.
   - Esto hace que la tarjeta aparezca inmediatamente sin refrescar.

4) Se dejó /boards/ con slash final (tu router es @get("/")) y /lists sin slash final.
   - Evita el 307 que tú mismo viste en backend (redirect /lists/ -> /lists).
*/

/*

5) IX: /boards -> /boards/ (evita 307 y posibles pérdidas del Authorization en redirect).
6) FIX: /boards/{id}/lists/ -> /boards/{id}/lists (evita 307, tu backend redirige justo al revés).
*/

/*

7) Se agregó botón "+ Nueva tarjeta" en header y "+ Nueva" en cada columna.
   - Tu archivo original no tenía creación de tarjetas.

8) Se agregó modal y POST /cards/ (apiFetch) para crear tarjeta.
   - Esto es la funcionalidad real que necesitas.

9) Se cargan board_id y listas reales desde backend:
   - GET /boards/ para elegir el primer tablero del usuario.
   - GET /boards/{boardId}/lists/ para mapear nombre -> list_id.
   - Sin hardcodear IDs (evita "No tienes permiso" / "Tablero no encontrado").

10) NO se deshabilita nada:
   - El modal abre siempre, y los errores se muestran dentro (sin “bloquear” la UI).
*/