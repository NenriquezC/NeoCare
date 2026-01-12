// src/pages/Boards.tsx
import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";
import { BoardColumn } from "../components/BoardColumn";
import {
  DndContext,
  type DragEndEvent,
  DragOverlay,
  type DragStartEvent,
  useSensor,
  useSensors,
  PointerSensor,
  closestCorners,
  useDroppable,
} from "@dnd-kit/core";
import {
  SortableContext,
  useSortable,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

// ==========================
// Extras (frontend-only)
// ==========================
type Label = { id: string; name: string; color: string };
type ChecklistItem = { id: string; text: string; done: boolean };
type CardExtras = {
  labels: Label[];
  assignee: string | null;
  checklist: ChecklistItem[];
};

const LABEL_PRESETS: Label[] = [
  { id: "blue", name: "Azul", color: "#2563eb" },
  { id: "red", name: "Rojo", color: "#dc2626" },
  { id: "green", name: "Verde", color: "#16a34a" },
  { id: "yellow", name: "Amarillo", color: "#f59e0b" },
];

const TEAM_MEMBERS: string[] = [
  "Sin asignar",
  "Helen",
  "Ana",
  "Carlos",
  "María",
  "David",
];

const EXTRAS_STORAGE_KEY = "neocare_card_extras_v1";

function safeParseJSON<T>(raw: string | null, fallback: T): T {
  if (!raw) return fallback;
  try {
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}

function loadExtrasMap(): Record<number, CardExtras> {
  return safeParseJSON<Record<number, CardExtras>>(
    localStorage.getItem(EXTRAS_STORAGE_KEY),
    {}
  );
}

function saveExtrasMap(map: Record<number, CardExtras>) {
  localStorage.setItem(EXTRAS_STORAGE_KEY, JSON.stringify(map));
}

function makeId(prefix = "id") {
  return `${prefix}_${Math.random().toString(16).slice(2)}_${Date.now().toString(16)}`;
}

function normalizeExtras(e?: Partial<CardExtras> | null): CardExtras {
  return {
    labels: Array.isArray(e?.labels) ? (e!.labels as Label[]) : [],
    assignee: typeof e?.assignee === "string" ? (e!.assignee as string) : null,
    checklist: Array.isArray(e?.checklist) ? (e!.checklist as ChecklistItem[]) : [],
  };
}

function checklistProgress(items: ChecklistItem[]) {
  const total = items.length;
  const done = items.filter((i) => i.done).length;
  const pct = total === 0 ? 0 : Math.round((done / total) * 100);
  return { total, done, pct };
}

function matchesQuery(card: any, q: string) {
  const s = (q || "").trim().toLowerCase();
  if (!s) return true;
  const t = String(card?.title ?? "").toLowerCase();
  const d = String(card?.description ?? "").toLowerCase();
  return t.includes(s) || d.includes(s);
}

function ymdFromAnyDateString(raw: any): string {
  if (!raw) return "";
  const s = String(raw);
  // si viene "2026-03-03T00:00:00", nos quedamos con la parte YYYY-MM-DD
  if (s.includes("T")) return s.split("T")[0];
  return s;
}

// ==========================
// Component
// ==========================
const Boards: React.FC = () => {
  const navigate = useNavigate();

  console.log("✅ ESTOY EN Boards.tsx (KANBAN con extras)");

  useEffect(() => {
    console.log("✅ BOARDS NUEVO CARGADO", new Date().toISOString());
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const handleBoardClick = (boardId: number) => {
    navigate(`/kanban/${boardId}`);
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
  const [activeCard, setActiveCard] = useState<any | null>(null);

  // ✅ Extras persistentes
  const [extrasByCardId, setExtrasByCardId] = useState<Record<number, CardExtras>>(
    () => loadExtrasMap()
  );

  // ✅ filtros/búsqueda
  const [query, setQuery] = useState("");
  const [labelFilter, setLabelFilter] = useState<string>("all");
  const [assigneeFilter, setAssigneeFilter] = useState<string>("all");

  // ✅ estado del modal (extras)
  const [modalLabels, setModalLabels] = useState<Label[]>([]);
  const [modalAssignee, setModalAssignee] = useState<string>("Sin asignar");
  const [modalChecklist, setModalChecklist] = useState<ChecklistItem[]>([]);
  const [newChecklistText, setNewChecklistText] = useState("");

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } })
  );

  const columns = ["Por hacer", "En curso", "Hecho"];

  // ==========================
  // UI helpers
  // ==========================
  const primaryBtn: React.CSSProperties = {
    height: 40,
    padding: "0 14px",
    background: "linear-gradient(135deg, #0b2a5a 0%, #1e3a8a 100%)",
    border: "1px solid rgba(255,255,255,0.18)",
    borderRadius: 12,
    color: "white",
    cursor: "pointer",
    fontWeight: 900,
    boxShadow: "0 6px 14px rgba(2, 6, 23, 0.18)",
    transition: "transform .15s ease, box-shadow .15s ease",
  };

  const secondaryBtn: React.CSSProperties = {
    height: 40,
    padding: "0 14px",
    background: "rgba(255,255,255,0.55)",
    border: "1px solid rgba(15, 23, 42, 0.12)",
    borderRadius: 12,
    color: "#0f172a",
    cursor: "pointer",
    fontWeight: 900,
    transition: "transform .15s ease",
  };

  const dangerBtn: React.CSSProperties = {
    height: 40,
    padding: "0 14px",
    background: "rgba(255,255,255,0.55)",
    border: "1px solid rgba(127, 29, 29, 0.25)",
    borderRadius: 12,
    color: "#7f1d1d",
    cursor: "pointer",
    fontWeight: 900,
    transition: "transform .15s ease",
  };

  function badgeStyle(bg: string) {
    return {
      display: "inline-block",
      padding: "2px 8px",
      borderRadius: 999,
      fontSize: 12,
      fontWeight: 800 as const,
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
    if (dt.getFullYear() !== y || dt.getMonth() !== m - 1 || dt.getDate() !== d)
      return null;
    return dt;
  }

  function diffDays(a: Date, b: Date): number {
    const a0 = new Date(a.getFullYear(), a.getMonth(), a.getDate()).getTime();
    const b0 = new Date(b.getFullYear(), b.getMonth(), b.getDate()).getTime();
    return Math.round((a0 - b0) / (1000 * 60 * 60 * 24));
  }

  function getDueBadge(dueDateStr: any) {
    const due = parseYMD(ymdFromAnyDateString(dueDateStr));
    if (!due) return null;

    const today = new Date();
    const days = diffDays(due, today);

    if (days < 0) return { text: "Vencida", style: badgeStyle("#7f1d1d") };
    if (days === 0) return { text: "Vence hoy", style: badgeStyle("#b45309") };
    if (days <= 2) return { text: "Vence pronto", style: badgeStyle("#1d4ed8") };
    return { text: ymdFromAnyDateString(dueDateStr), style: badgeStyle("#334155") };
  }

  // ==========================
  // Extras helpers
  // ==========================
  const labelOptions = useMemo(
    () => [{ id: "all", name: "Todas" }, ...LABEL_PRESETS.map((l) => ({ id: l.id, name: l.name }))],
    []
  );

  const assigneeOptions = useMemo(() => ["all", ...TEAM_MEMBERS], []);

  function getExtras(cardId: number | undefined): CardExtras {
    if (!cardId) return normalizeExtras(null);
    return normalizeExtras(extrasByCardId[cardId] ?? null);
  }

  function setExtras(cardId: number, extras: CardExtras) {
    setExtrasByCardId((prev) => {
      const next = { ...prev, [cardId]: normalizeExtras(extras) };
      saveExtrasMap(next);
      return next;
    });
  }

  // ==========================
  // Load boards/lists/cards
  // ==========================
  useEffect(() => {
    (async () => {
      try {
        const resBoards = await apiFetch("/boards/", { method: "GET" });
        if (!resBoards.ok) throw new Error(`No se pudieron cargar boards (${resBoards.status})`);
        const boards = await resBoards.json();

        if (!Array.isArray(boards) || boards.length === 0 || typeof boards[0]?.id !== "number") {
          setSelectedBoardId(null);
          setListIdByColumn({});
          setCards([]);
          setFormError("No hay tablero disponible para tu usuario.");
          return;
        }

        const boardId = boards[0].id as number;
        setSelectedBoardId(boardId);

        const resLists = await apiFetch(`/boards/${boardId}/lists`, { method: "GET" });
        if (!resLists.ok) throw new Error(`No se pudieron cargar lists (${resLists.status})`);
        const lists = await resLists.json();

        const map: Record<string, number> = {};
        if (Array.isArray(lists)) {
          for (const l of lists) {
            if (l?.name && typeof l?.id === "number") map[l.name] = l.id;
          }
        }
        setListIdByColumn(map);

        // ✅ IMPORTANTE: sin "/" antes del "?"
        const resCards = await apiFetch(`/cards?board_id=${boardId}`, { method: "GET" });
        if (!resCards.ok) throw new Error(`No se pudieron cargar cards (${resCards.status})`);
        const cardsData = await resCards.json();
        const arr = Array.isArray(cardsData) ? cardsData : [];
        setCards(arr);

        // asegurar extras (no pisa lo guardado)
        setExtrasByCardId((prev) => {
          const next = { ...prev };
          const stored = loadExtrasMap();
          for (const c of arr) {
            if (c?.id && typeof c.id === "number") {
              next[c.id] = normalizeExtras(next[c.id] ?? stored[c.id] ?? null);
            }
          }
          saveExtrasMap(next);
          return next;
        });
      } catch (err) {
        setSelectedBoardId(null);
        setListIdByColumn({});
        setCards([]);
        setFormError(err instanceof Error ? err.message : "Error cargando datos");
      }
    })();
  }, []);

  // ==========================
  // Modal open/close
  // ==========================
  function openCreate(targetColumn: string = "Por hacer") {
    setEditingCard(null);
    setForm({ title: "", description: "", due_date: "" });
    setFormError(null);

    setModalLabels([]);
    setModalAssignee("Sin asignar");
    setModalChecklist([]);
    setNewChecklistText("");

    if (!selectedBoardId) {
      setFormError("No hay un tablero activo.");
      setShowModal(true);
      return;
    }

    const mapEntries = Object.entries(listIdByColumn);
    const fallbackEntry = mapEntries.length > 0 ? mapEntries[0] : null;
    const realListId = listIdByColumn[targetColumn] ?? fallbackEntry?.[1];
    const realColumnName = listIdByColumn[targetColumn]
      ? targetColumn
      : fallbackEntry?.[0] ?? targetColumn;

    if (!realListId) {
      setFormError("No existen listas para este tablero.");
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
      // ✅ FIX: input type=date necesita YYYY-MM-DD
      due_date: ymdFromAnyDateString(card?.due_date ?? ""),
    });
    setFormError(null);

    setSelectedListId(card?.list_id ?? null);

    const e = getExtras(card?.id);
    setModalLabels(e.labels);
    setModalAssignee(e.assignee ?? "Sin asignar");
    setModalChecklist(e.checklist);
    setNewChecklistText("");

    setShowModal(true);
  }

  function closeModal() {
    setShowModal(false);
    setFormError(null);
  }

  // ==========================
  // Checklist actions (modal)
  // ==========================
  function addChecklistItem() {
    const text = newChecklistText.trim();
    if (!text) return;
    setModalChecklist((prev) => [...prev, { id: makeId("chk"), text, done: false }]);
    setNewChecklistText("");
  }

  function toggleChecklistItem(id: string) {
    setModalChecklist((prev) =>
      prev.map((it) => (it.id === id ? { ...it, done: !it.done } : it))
    );
  }

  function deleteChecklistItem(id: string) {
    setModalChecklist((prev) => prev.filter((it) => it.id !== id));
  }

  // ==========================
  // Labels actions (modal)
  // ==========================
  function toggleLabel(label: Label) {
    setModalLabels((prev) => {
      const exists = prev.some((l) => l.id === label.id);
      return exists ? prev.filter((l) => l.id !== label.id) : [...prev, label];
    });
  }

  // ==========================
  // Create/Update/Delete
  // ==========================
  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);

    if (!form.title.trim()) {
      setFormError("El título es obligatorio.");
      return;
    }
    if (!selectedBoardId) {
      setFormError("No hay un tablero activo.");
      return;
    }

    const targetColumn = selectedColumn || "Por hacer";
    const mapEntries = Object.entries(listIdByColumn);
    const fallbackEntry = mapEntries.length > 0 ? mapEntries[0] : null;
    const listId = listIdByColumn[targetColumn] ?? fallbackEntry?.[1] ?? null;

    if (!listId) {
      setFormError(`No existe la lista "${targetColumn}".`);
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
        throw new Error(txt || `Error al crear tarjeta (${res.status})`);
      }

      const created = await res.json().catch(() => null);
      if (created) {
        const createdId = created?.id;
        if (typeof createdId === "number") {
          setExtras(createdId, {
            labels: modalLabels,
            assignee: modalAssignee === "Sin asignar" ? null : modalAssignee,
            checklist: modalChecklist,
          });
        }
      }

      closeModal();
      
      // ✅ Recargar tarjetas después de crear
      setTimeout(() => {
        const boardId = selectedBoardId;
        if (boardId) {
          (async () => {
            try {
              const resCards = await apiFetch(`/cards?board_id=${boardId}`, { method: "GET" });
              if (resCards.ok) {
                const cardsData = await resCards.json();
                const arr = Array.isArray(cardsData) ? cardsData : [];
                setCards(arr);
              }
            } catch (err) {
              console.error("Error recargando tarjetas:", err);
            }
          })();
        }
      }, 300);
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
      setFormError("No hay tarjeta seleccionada.");
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
        method: "PATCH",
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(txt || `Error al editar tarjeta (${res.status})`);
      }

      const updated = await res.json().catch(() => null);
      if (updated) {
        setCards((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));

        setExtras(updated.id, {
          labels: modalLabels,
          assignee: modalAssignee === "Sin asignar" ? null : modalAssignee,
          checklist: modalChecklist,
        });
      }

      closeModal();
      // ✅ IMPORTANTE: Recargar tarjetas para sincronizar
      setTimeout(() => {
        const boardId = selectedBoardId;
        if (boardId) {
          (async () => {
            try {
              const resCards = await apiFetch(`/cards?board_id=${boardId}`, { method: "GET" });
              if (resCards.ok) {
                const cardsData = await resCards.json();
                const arr = Array.isArray(cardsData) ? cardsData : [];
                setCards(arr);
              }
            } catch (err) {
              console.error("Error recargando tarjetas:", err);
            }
          })();
        }
      }, 500);
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Error editando tarjeta");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    setFormError(null);

    if (!editingCard?.id) {
      setFormError("No hay tarjeta seleccionada.");
      return;
    }

    const ok = window.confirm("¿Eliminar esta tarjeta?");
    if (!ok) return;

    setSaving(true);
    try {
      const res = await apiFetch(`/cards/${editingCard.id}`, { method: "DELETE" });

      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(txt || `Error al eliminar tarjeta (${res.status})`);
      }

      setCards((prev) => prev.filter((c) => c.id !== editingCard.id));

      setExtrasByCardId((prev) => {
        const next = { ...prev };
        delete next[editingCard.id];
        saveExtrasMap(next);
        return next;
      });

      closeModal();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Error eliminando tarjeta");
    } finally {
      setSaving(false);
    }
  }

  // ==========================
  // Drag start/end
  // ==========================
  function handleDragStart(event: DragStartEvent) {
    const { active } = event;
    const card = cards.find((c) => c.id === active.id);
    setActiveCard(card);
  }

  async function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    setActiveCard(null);
    if (!over) return;

    const cardId = active.id as number;
    let targetListId: number | null = null;

    const targetCard = cards.find((c) => c.id === over.id);
    if (targetCard) {
      targetListId = targetCard.list_id;
    } else if (typeof over.id === "number") {
      targetListId = over.id;
    } else if (typeof over.id === "string" && over.id.startsWith("column-")) {
      const colName = over.id.replace("column-", "");
      targetListId = listIdByColumn[colName] || null;
    }

    if (!targetListId) return;

    const card = cards.find((c) => c.id === cardId);
    if (!card) return;

    if (card.list_id === targetListId && active.id === over.id) return;

    const oldCards = [...cards];
    const cardsInTargetList = cards.filter((c) => c.list_id === targetListId);
    const newPosition = cardsInTargetList.length;

    // UI optimista
    setCards((prev) =>
      prev.map((c) =>
        c.id === cardId ? { ...c, list_id: targetListId, position: newPosition } : c
      )
    );

    try {
      const res = await apiFetch(`/cards/${cardId}`, {
        method: "PATCH",
        body: JSON.stringify({ list_id: targetListId, position: newPosition }),
      });

      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(txt || `Error al mover tarjeta (${res.status})`);
      }

      const updated = await res.json().catch(() => null);
      if (updated) {
        setCards((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
      }
    } catch (err) {
      setCards(oldCards);
      setFormError(err instanceof Error ? err.message : "Error moviendo tarjeta");
    }
  }

  // ==========================
  // filtros tablero
  // ==========================
  function passesLabelFilter(cardId: number) {
    if (labelFilter === "all") return true;
    const e = getExtras(cardId);
    return e.labels.some((l) => l.id === labelFilter);
  }

  function passesAssigneeFilter(cardId: number) {
    if (assigneeFilter === "all") return true;
    const e = getExtras(cardId);
    const name = e.assignee ?? "Sin asignar";
    return name === assigneeFilter;
  }

  // ==========================
  // Render
  // ==========================
  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          background: "linear-gradient(135deg, #020617 0%, #0b2a5a 45%, #1e3a8a 100%)",
        }}
      >
        {/* Header */}
        <header
          style={{
            padding: "14px 24px",
            background: "rgba(255,255,255,0.22)",
            backdropFilter: "blur(10px)",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderBottom: "1px solid rgba(255,255,255,0.12)",
            gap: 14,
          }}
        >
          <h1 style={{ margin: 0, color: "white", fontSize: 28, fontWeight: 900 }}>
            NeoCare
          </h1>

          <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Buscar tarjetas…"
              style={{
                height: 40,
                width: 240,
                borderRadius: 12,
                border: "1px solid rgba(255,255,255,0.18)",
                background: "rgba(255,255,255,0.18)",
                color: "white",
                padding: "0 12px",
                outline: "none",
              }}
            />

            <select
              value={labelFilter}
              onChange={(e) => setLabelFilter(e.target.value)}
              style={{
                height: 40,
                borderRadius: 12,
                border: "1px solid rgba(255,255,255,0.18)",
                background: "rgba(255,255,255,0.18)",
                color: "white",
                padding: "0 10px",
                outline: "none",
                cursor: "pointer",
              }}
            >
              {labelOptions.map((o) => (
                <option key={o.id} value={o.id} style={{ color: "#0f172a" }}>
                  {o.name}
                </option>
              ))}
            </select>

            <select
              value={assigneeFilter}
              onChange={(e) => setAssigneeFilter(e.target.value)}
              style={{
                height: 40,
                borderRadius: 12,
                border: "1px solid rgba(255,255,255,0.18)",
                background: "rgba(255,255,255,0.18)",
                color: "white",
                padding: "0 10px",
                outline: "none",
                cursor: "pointer",
              }}
            >
              {assigneeOptions.map((name) => (
                <option key={name} value={name} style={{ color: "#0f172a" }}>
                  {name === "all" ? "Todos" : name}
                </option>
              ))}
            </select>

            <button onClick={() => openCreate("Por hacer")} style={primaryBtn}>
              + Nueva tarjeta
            </button>

            <button onClick={() => navigate("/my-hours")} style={secondaryBtn}>
              Mis horas
            </button>

            <button
              onClick={() => {
                if (!selectedBoardId) return;
                navigate(`/report/${selectedBoardId}`);
              }}
              disabled
              title="Reporte semanal aún no está implementado"
              style={{ ...secondaryBtn, opacity: 0.55, cursor: "not-allowed" }}
            >
              Reporte semanal
            </button>

            <button onClick={handleLogout} style={dangerBtn}>
              Cerrar sesión
            </button>
          </div>
        </header>

        {formError && (
          <div style={{ padding: "10px 24px", color: "#fecaca", fontWeight: 800 }}>
            {formError}
          </div>
        )}

        {/* Tablero */}
        <main style={{ flex: 1, display: "flex", gap: 18, padding: 18 }}>
          {columns.map((col) => {
            const listId = listIdByColumn[col];
            const colCardsRaw = listId ? cards.filter((c) => c?.list_id === listId) : [];

            const colCards = colCardsRaw
              .filter((c) => matchesQuery(c, query))
              .filter((c) => passesLabelFilter(c.id))
              .filter((c) => passesAssigneeFilter(c.id));

            return (
              <DroppableColumn
                key={col}
                listId={listId}
                columnName={col}
                cards={colCards}
                count={colCards.length}
                onCreateCard={() => openCreate(col)}
                onEditCard={openEdit}
                badgeStyle={badgeStyle}
                getDueBadge={getDueBadge}
                getExtras={getExtras}
              />
            );
          })}
        </main>

        {/* Modal */}
        {showModal && (
          <div
            role="dialog"
            aria-modal="true"
            onMouseDown={(e) => {
              if (e.target === e.currentTarget) closeModal();
            }}
            style={{
              position: "fixed",
              inset: 0,
              zIndex: 9999,
              background: "rgba(0,0,0,0.45)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: 16,
            }}
          >
            <div
              style={{
                width: 760,
                maxWidth: "95vw",
                maxHeight: "92vh",
                overflow: "auto",
                background: "rgba(255,255,255,0.96)",
                borderRadius: 14,
                padding: 18,
                border: "1px solid rgba(15,23,42,0.10)",
                boxShadow: "0 18px 50px rgba(0,0,0,0.35)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: 12,
                }}
              >
                <h3 style={{ margin: 0, fontWeight: 900 }}>
                  {editingCard ? "Editar tarjeta" : "Nueva tarjeta"}
                </h3>

                <button
                  onClick={closeModal}
                  style={{
                    background: "transparent",
                    border: "none",
                    fontSize: 22,
                    cursor: "pointer",
                    color: "#0f172a",
                    fontWeight: 900,
                  }}
                  aria-label="Cerrar"
                  title="Cerrar"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={editingCard ? handleUpdate : handleCreate}>
                <div style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: 16 }}>
                  {/* IZQ */}
                  <div>
                    <label style={{ display: "block", marginBottom: 6, fontWeight: 900 }}>
                      Título
                    </label>
                    <input
                      value={form.title}
                      onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                      style={{
                        width: "100%",
                        padding: 10,
                        marginBottom: 10,
                        borderRadius: 10,
                        border: "1px solid rgba(15,23,42,0.14)",
                        background: "white",
                        color: "#0f172a",
                      }}
                    />

                    <label style={{ display: "block", marginBottom: 6, fontWeight: 900 }}>
                      Descripción
                    </label>
                    <textarea
                      rows={4}
                      value={form.description}
                      onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                      style={{
                        width: "100%",
                        padding: 10,
                        marginBottom: 10,
                        borderRadius: 10,
                        border: "1px solid rgba(15,23,42,0.14)",
                        background: "white",
                        color: "#0f172a",
                      }}
                    />

                    <label style={{ display: "block", marginBottom: 6, fontWeight: 900 }}>
                      Fecha límite
                    </label>
                    <input
                      type="date"
                      value={form.due_date}
                      onChange={(e) => setForm((f) => ({ ...f, due_date: e.target.value }))}
                      style={{
                        width: "fit-content",
                        padding: 10,
                        marginBottom: 12,
                        borderRadius: 10,
                        border: "1px solid rgba(15,23,42,0.14)",
                        background: "white",
                        color: "#0f172a",
                      }}
                    />

                    {/* Checklist */}
                    <div style={{ marginTop: 12 }}>
                      <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <div style={{ fontWeight: 900 }}>Checklist</div>
                        <div style={{ fontSize: 12, color: "rgba(15,23,42,0.65)", fontWeight: 900 }}>
                          {checklistProgress(modalChecklist).done}/{checklistProgress(modalChecklist).total} (
                          {checklistProgress(modalChecklist).pct}%)
                        </div>
                      </div>

                      <div
                        style={{
                          marginTop: 8,
                          height: 8,
                          borderRadius: 999,
                          background: "rgba(15,23,42,0.10)",
                          overflow: "hidden",
                        }}
                      >
                        <div
                          style={{
                            height: "100%",
                            width: `${checklistProgress(modalChecklist).pct}%`,
                            background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                            transition: "width .2s ease",
                          }}
                        />
                      </div>

                      <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
                        <input
                          value={newChecklistText}
                          onChange={(e) => setNewChecklistText(e.target.value)}
                          placeholder="Añadir subtarea…"
                          style={{
                            flex: 1,
                            padding: 10,
                            borderRadius: 10,
                            border: "1px solid rgba(15,23,42,0.14)",
                            background: "white",
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter") {
                              e.preventDefault();
                              addChecklistItem();
                            }
                          }}
                        />
                        <button
                          type="button"
                          onClick={addChecklistItem}
                          style={{
                            height: 40,
                            padding: "0 14px",
                            borderRadius: 12,
                            border: "1px solid rgba(15,23,42,0.12)",
                            background: "rgba(15,23,42,0.06)",
                            fontWeight: 900,
                            cursor: "pointer",
                          }}
                        >
                          Añadir
                        </button>
                      </div>

                      <div style={{ marginTop: 10, display: "flex", flexDirection: "column", gap: 8 }}>
                        {modalChecklist.length === 0 ? (
                          <div style={{ fontSize: 13, color: "rgba(15,23,42,0.55)" }}>
                            No hay subtareas todavía.
                          </div>
                        ) : (
                          modalChecklist.map((it) => (
                            <div
                              key={it.id}
                              style={{
                                display: "flex",
                                alignItems: "center",
                                gap: 10,
                                padding: "8px 10px",
                                borderRadius: 12,
                                border: "1px solid rgba(15,23,42,0.10)",
                                background: "white",
                              }}
                            >
                              <input
                                type="checkbox"
                                checked={it.done}
                                onChange={() => toggleChecklistItem(it.id)}
                              />
                              <div
                                style={{
                                  flex: 1,
                                  fontSize: 13,
                                  fontWeight: 900,
                                  textDecoration: it.done ? "line-through" : "none",
                                  color: it.done ? "rgba(15,23,42,0.55)" : "#0f172a",
                                }}
                              >
                                {it.text}
                              </div>
                              <button
                                type="button"
                                onClick={() => deleteChecklistItem(it.id)}
                                style={{
                                  border: "none",
                                  background: "transparent",
                                  cursor: "pointer",
                                  color: "#7f1d1d",
                                  fontWeight: 900,
                                }}
                                title="Eliminar"
                              >
                                ✕
                              </button>
                            </div>
                          ))
                        )}
                      </div>
                    </div>
                  </div>

                  {/* DER */}
                  <div>
                    <div style={{ marginBottom: 14 }}>
                      <div style={{ fontWeight: 900, marginBottom: 6 }}>Responsable</div>
                      <select
                        value={modalAssignee}
                        onChange={(e) => setModalAssignee(e.target.value)}
                        style={{
                          width: "100%",
                          height: 40,
                          borderRadius: 12,
                          border: "1px solid rgba(15,23,42,0.12)",
                          background: "white",
                          padding: "0 10px",
                          cursor: "pointer",
                          fontWeight: 900,
                        }}
                      >
                        {TEAM_MEMBERS.map((m) => (
                          <option key={m} value={m}>
                            {m}
                          </option>
                        ))}
                      </select>
                      <div style={{ marginTop: 6, fontSize: 12, color: "rgba(15,23,42,0.55)" }}>
                        (Se guarda en frontend/localStorage)
                      </div>
                    </div>

                    <div style={{ marginBottom: 14 }}>
                      <div style={{ fontWeight: 900, marginBottom: 6 }}>Etiquetas</div>
                      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                        {LABEL_PRESETS.map((l) => {
                          const active = modalLabels.some((x) => x.id === l.id);
                          return (
                            <button
                              key={l.id}
                              type="button"
                              onClick={() => toggleLabel(l)}
                              style={{
                                height: 30,
                                padding: "0 10px",
                                borderRadius: 999,
                                border: active
                                  ? "1px solid rgba(15,23,42,0.18)"
                                  : "1px solid rgba(15,23,42,0.10)",
                                background: active ? l.color : "rgba(15,23,42,0.06)",
                                color: active ? "white" : "#0f172a",
                                fontWeight: 900,
                                cursor: "pointer",
                                fontSize: 12,
                              }}
                            >
                              {l.name}
                            </button>
                          );
                        })}
                      </div>

                      <div style={{ marginTop: 10, display: "flex", gap: 8, flexWrap: "wrap" }}>
                        {modalLabels && modalLabels.length > 0 ? (
                          modalLabels.map((l) => (
                            <span
                              key={l.id}
                              style={{
                                display: "inline-flex",
                                alignItems: "center",
                                padding: "4px 10px",
                                borderRadius: 999,
                                background: l.color,
                                color: "white",
                                fontSize: 12,
                                fontWeight: 900,
                              }}
                            >
                              {l.name}
                            </span>
                          ))
                        ) : (
                          <div style={{ fontSize: 13, color: "rgba(15,23,42,0.55)" }}>
                            Sin etiquetas.
                          </div>
                        )}
                      </div>
                    </div>

                    <div
                      style={{
                        marginTop: 12,
                        padding: 12,
                        borderRadius: 14,
                        background: "rgba(15,23,42,0.06)",
                        border: "1px solid rgba(15,23,42,0.10)",
                        fontSize: 12,
                        color: "rgba(15,23,42,0.65)",
                      }}
                    >
                      <div style={{ fontWeight: 900, marginBottom: 6 }}>Info</div>
                      <div>board_id: {selectedBoardId ?? "—"}</div>
                      <div>list_id: {selectedListId ?? "—"}</div>
                      {editingCard?.id ? <div>editing_card_id: {editingCard.id}</div> : null}
                    </div>
                  </div>
                </div>

                {formError && (
                  <div style={{ color: "#7f1d1d", marginTop: 12, fontWeight: 900 }}>
                    {formError}
                  </div>
                )}

                <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginTop: 16 }}>
                  <button
                    type="submit"
                    disabled={saving}
                    style={{
                      height: 40,
                      padding: "0 14px",
                      background: editingCard
                        ? "linear-gradient(135deg, #f59e0b 0%, #b45309 100%)"
                        : "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                      border: "none",
                      borderRadius: 12,
                      color: "white",
                      fontWeight: 900,
                      cursor: "pointer",
                    }}
                  >
                    {saving
                      ? editingCard
                        ? "Guardando…"
                        : "Creando…"
                      : editingCard
                      ? "Guardar cambios"
                      : "Crear tarjeta"}
                  </button>

                  <button
                    type="button"
                    onClick={closeModal}
                    style={{
                      height: 40,
                      padding: "0 14px",
                      background: "rgba(15,23,42,0.08)",
                      border: "1px solid rgba(15,23,42,0.12)",
                      borderRadius: 12,
                      color: "#0f172a",
                      fontWeight: 900,
                      cursor: "pointer",
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
                        height: 40,
                        padding: "0 14px",
                        background: "rgba(127,29,29,0.10)",
                        border: "1px solid rgba(127,29,29,0.25)",
                        borderRadius: 12,
                        color: "#7f1d1d",
                        fontWeight: 900,
                        cursor: "pointer",
                      }}
                    >
                      Eliminar
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>
        )}

        <DragOverlay>
          {activeCard ? (
            <DragPreview card={activeCard} extras={getExtras(activeCard.id)} />
          ) : null}
        </DragOverlay>
      </div>
    </DndContext>
  );
};

// ==========================
// Drag preview
// ==========================
function DragPreview({ card, extras }: { card: any; extras: CardExtras }) {
  const prog = checklistProgress(extras.checklist);
  return (
    <div
      style={{
        textAlign: "left",
        background: "rgba(255, 255, 255, 0.96)",
        border: "1px solid rgba(15,23,42,0.14)",
        borderRadius: 14,
        padding: 12,
        color: "#0f172a",
        cursor: "grabbing",
        boxShadow: "0 18px 40px rgba(0, 0, 0, 0.35)",
        transform: "scale(1.04)",
        opacity: 0.95,
        minWidth: 260,
      }}
    >
      <div style={{ fontWeight: 900, fontSize: 14 }}>{card.title}</div>
    </div>
  );
}

// ==========================
// DraggableCard
// ==========================
interface DraggableCardProps {
  card: any;
  columnName: string;
  onEdit: (card: any) => void;
  badgeStyle: (bg: string) => any;
  getDueBadge: (date: any) => any;
  extras: CardExtras;
}

function DraggableCard({ card, columnName, onEdit, badgeStyle, getDueBadge, extras }: DraggableCardProps) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: card.id });

  const style: React.CSSProperties = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.6 : 1,
  };
  const dueBadge = getDueBadge(card?.due_date);
  const prog = checklistProgress(extras.checklist);
  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <button
        type="button"
        onClick={() => onEdit(card)}
        style={{
          width: "100%",
          textAlign: "left",
          background: "rgba(255, 255, 255, 0.92)",
          border: "1px solid rgba(15,23,42,0.10)",
          borderRadius: 14,
          padding: 12,
          color: "#0f172a",
          cursor: isDragging ? "grabbing" : "grab",
          boxShadow: isDragging
            ? "0 14px 28px rgba(0, 0, 0, 0.22)"
            : "0 8px 16px rgba(0, 0, 0, 0.12)",
          transition: "transform .15s ease, box-shadow .15s ease",
        }}
        title="Arrastra para mover o click para editar"
      >
        <div style={{ fontWeight: 900, fontSize: 14 }}>{card.title}</div>

        <div style={{ marginTop: 10, display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
          <span style={badgeStyle("#1e40af")}>Estado: {columnName}</span>

          {dueBadge ? (
            <span style={dueBadge.style}>📅 {dueBadge.text}</span>
          ) : (
            <span style={badgeStyle("#334155")}>📅 Sin fecha</span>
          )}
        </div>
      </button>
    </div>
  );
}

// ==========================
// DroppableColumn
// ==========================
interface DroppableColumnProps {
  listId: number | undefined;
  columnName: string;
  cards: any[];
  count: number;
  onCreateCard: () => void;
  onEditCard: (card: any) => void;
  badgeStyle: (bg: string) => any;
  getDueBadge: (date: any) => any;
  getExtras: (cardId: number | undefined) => CardExtras;
}

function DroppableColumn({
  listId,
  columnName,
  cards,
  count,
  onCreateCard,
  onEditCard,
  badgeStyle,
  getDueBadge,
  getExtras,
}: DroppableColumnProps) {
  const { setNodeRef, isOver } = useDroppable({
    id: listId || `column-${columnName}`,
  });
  return (
    <BoardColumn title={columnName} count={count} isOver={isOver} onCreate={onCreateCard}>
      <div
        ref={setNodeRef}
        style={{
          flex: 1,
          border: "1px dashed rgba(255,255,255,0.25)",
          borderRadius: 14,
          padding: 12,
          fontSize: 14,
          color: "white",
          display: "flex",
          flexDirection: "column",
          gap: 10,
          minHeight: 240,
          background: isOver ? "rgba(2, 6, 23, 0.24)" : "rgba(2, 6, 23, 0.18)",
          transition: "background .15s ease",
        }}
      >
        {!listId ? (
          <div style={{ color: "#fecaca", fontWeight: 900 }}>Listas aún no cargadas…</div>
        ) : cards.length === 0 ? (
          <div style={{ margin: "auto", textAlign: "center", color: "rgba(255,255,255,0.82)" }}>
            <div style={{ fontWeight: 900, marginBottom: 6 }}>Sin tarjetas</div>
          </div>
        ) : (
          <SortableContext items={cards.map((c) => c.id)} strategy={verticalListSortingStrategy}>
            {cards.map((card) => (
              <DraggableCard
                key={card.id}
                card={card}
                columnName={columnName}
                onEdit={onEditCard}
                badgeStyle={badgeStyle}
                getDueBadge={getDueBadge}
                extras={getExtras(card.id)}
              />
            ))}
          </SortableContext>
        )}
      </div>
    </BoardColumn>
  );
}

export default Boards;
