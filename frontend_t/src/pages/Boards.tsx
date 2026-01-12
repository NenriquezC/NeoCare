import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";

// ==========================
// Tipos y constantes
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

function loadExtrasMap(): Record<number, CardExtras> {
  try {
    const raw = localStorage.getItem(EXTRAS_STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveExtrasMap(map: Record<number, CardExtras>) {
  localStorage.setItem(EXTRAS_STORAGE_KEY, JSON.stringify(map));
}

interface Card {
  id: number;
  title: string;
  description?: string;
  list_id: number;
  board_id: number;
  position?: number;
  due_date?: string;
  created_at?: string;
  updated_at?: string;
}

interface List {
  id: number;
  name: string;
  position: number;
  board_id: number;
}

interface Board {
  id: number;
  name: string;
  description?: string;
}

export default function Boards() {
  const navigate = useNavigate();
  const [boards, setBoards] = useState<Board[]>([]);
  const [selectedBoardId, setSelectedBoardId] = useState<number | null>(null);
  const [lists, setLists] = useState<List[]>([]);
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Extras persistentes
  const [extrasByCardId, setExtrasByCardId] = useState<Record<number, CardExtras>>(() => loadExtrasMap());
  
  // Filtros y búsqueda
  const [searchQuery, setSearchQuery] = useState("");
  const [labelFilter, setLabelFilter] = useState("all");
  const [assigneeFilter, setAssigneeFilter] = useState("all");
  
  // Modal para crear/editar tarjeta
  const [showModal, setShowModal] = useState(false);
  const [editingCard, setEditingCard] = useState<Card | null>(null);
  const [newCard, setNewCard] = useState({ title: "", description: "", list_id: 1, due_date: "" });
  
  // Estado modal extras
  const [modalLabels, setModalLabels] = useState<Label[]>([]);
  const [modalAssignee, setModalAssignee] = useState<string>("Sin asignar");
  const [modalChecklist, setModalChecklist] = useState<ChecklistItem[]>([]);
  const [newChecklistText, setNewChecklistText] = useState("");

  // Opciones para filtros
  const labelOptions = [
    { id: "all", name: "Todas las etiquetas" },
    ...LABEL_PRESETS.map((l) => ({ id: l.id, name: l.name })),
  ];

  const assigneeOptions = ["all", ...TEAM_MEMBERS];

  useEffect(() => {
    loadBoards();
  }, []);

  async function loadBoards() {
    try {
      setLoading(true);
      const res = await apiFetch("/boards/", { method: "GET" });
      if (!res.ok) throw new Error("Error al cargar boards");
      const data = await res.json();
      
      if (Array.isArray(data) && data.length > 0) {
        setBoards(data);
        const firstBoard = data[0];
        setSelectedBoardId(firstBoard.id);
        await loadBoardData(firstBoard.id);
      } else {
        setError("No hay tableros disponibles");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  async function loadBoardData(boardId: number) {
    try {
      // Cargar listas
      const resLists = await apiFetch(`/boards/${boardId}/lists`, { method: "GET" });
      if (!resLists.ok) throw new Error("Error al cargar listas");
      const listsData = await resLists.json();
      setLists(Array.isArray(listsData) ? listsData.sort((a, b) => a.position - b.position) : []);

      // Cargar tarjetas
      const resCards = await apiFetch(`/cards/?board_id=${boardId}`, { method: "GET" });
      if (!resCards.ok) throw new Error("Error al cargar tarjetas");
      const cardsData = await resCards.json();
      console.log("📌 Tarjetas cargadas:", cardsData);
      setCards(Array.isArray(cardsData) ? cardsData : []);
      
      // Asegurar extras (no pisa lo guardado)
      setExtrasByCardId((prev) => {
        const next = { ...prev };
        const stored = loadExtrasMap();
        for (const c of (Array.isArray(cardsData) ? cardsData : [])) {
          if (!next[c.id]) {
            next[c.id] = stored[c.id] || { labels: [], assignee: null, checklist: [] };
          }
        }
        return next;
      });
    } catch (err) {
      console.error("Error cargando datos del board:", err);
      setError(err instanceof Error ? err.message : "Error cargando datos");
    }
  }

  async function handleCreateCard() {
    if (!newCard.title.trim()) {
      alert("El título es obligatorio");
      return;
    }

    try {
      if (editingCard) {
        // Editar tarjeta existente
        const res = await apiFetch(`/cards/${editingCard.id}`, {
          method: "PATCH",
          body: JSON.stringify({
            title: newCard.title,
            description: newCard.description,
            due_date: newCard.due_date || null,
          }),
        });

        if (!res.ok) throw new Error("Error al editar tarjeta");
        
        // Actualizar extras
        setExtrasByCardId((prev) => {
          const next = {
            ...prev,
            [editingCard.id]: {
              labels: modalLabels,
              assignee: modalAssignee === "Sin asignar" ? null : modalAssignee,
              checklist: modalChecklist,
            },
          };
          saveExtrasMap(next);
          return next;
        });
      } else {
        // Crear tarjeta nueva
        const res = await apiFetch("/cards/", {
          method: "POST",
          body: JSON.stringify({
            title: newCard.title,
            description: newCard.description,
            list_id: newCard.list_id,
            board_id: selectedBoardId,
            due_date: newCard.due_date || null,
          }),
        });

        if (!res.ok) throw new Error("Error al crear tarjeta");
        
        const created = await res.json();
        
        // Guardar extras
        setExtrasByCardId((prev) => {
          const next = {
            ...prev,
            [created.id]: {
              labels: modalLabels,
              assignee: modalAssignee === "Sin asignar" ? null : modalAssignee,
              checklist: modalChecklist,
            },
          };
          saveExtrasMap(next);
          return next;
        });
      }
      
      // Recargar tarjetas
      if (selectedBoardId) {
        await loadBoardData(selectedBoardId);
      }
      
      setShowModal(false);
      setEditingCard(null);
      setNewCard({ title: "", description: "", list_id: 1, due_date: "" });
      setModalLabels([]);
      setModalAssignee("Sin asignar");
      setModalChecklist([]);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Error al procesar tarjeta");
    }
  }

  function openEdit(card: Card) {
    setEditingCard(card);
    setNewCard({
      title: card.title,
      description: card.description || "",
      list_id: card.list_id,
      due_date: card.due_date || "",
    });
    
    const extras = extrasByCardId[card.id] || { labels: [], assignee: null, checklist: [] };
    setModalLabels(extras.labels);
    setModalAssignee(extras.assignee || "Sin asignar");
    setModalChecklist(extras.checklist);
    setShowModal(true);
  }

  function getCardsForList(listId: number): Card[] {
    let filtered = cards.filter((c) => c.list_id === listId);
    
    // Aplicar filtro de búsqueda
    if (searchQuery.trim()) {
      const q = searchQuery.trim().toLowerCase();
      filtered = filtered.filter((c) => 
        c.title.toLowerCase().includes(q) || 
        (c.description || "").toLowerCase().includes(q)
      );
    }
    
    // Aplicar filtro de etiquetas
    if (labelFilter !== "all") {
      filtered = filtered.filter((c) => {
        const extras = extrasByCardId[c.id];
        return extras?.labels.some((l) => l.id === labelFilter);
      });
    }
    
    // Aplicar filtro de asignados
    if (assigneeFilter !== "all") {
      filtered = filtered.filter((c) => {
        const extras = extrasByCardId[c.id];
        const assignee = extras?.assignee || "Sin asignar";
        return assignee === assigneeFilter;
      });
    }
    
    console.log(`📌 Lista ${listId}:`, filtered.length, "tarjetas");
    return filtered;
  }

  function getExtras(cardId: number): CardExtras {
    return extrasByCardId[cardId] || { labels: [], assignee: null, checklist: [] };
  }

  function toggleLabel(label: Label) {
    setModalLabels((prev) =>
      prev.some((l) => l.id === label.id)
        ? prev.filter((l) => l.id !== label.id)
        : [...prev, label]
    );
  }

  function addChecklistItem() {
    if (!newChecklistText.trim()) return;
    setModalChecklist((prev) => [
      ...prev,
      { id: `ck_${Date.now()}`, text: newChecklistText.trim(), done: false },
    ]);
    setNewChecklistText("");
  }

  function toggleChecklistItem(id: string) {
    setModalChecklist((prev) =>
      prev.map((item) => (item.id === id ? { ...item, done: !item.done } : item))
    );
  }

  function removeChecklistItem(id: string) {
    setModalChecklist((prev) => prev.filter((item) => item.id !== id));
  }

  function checklistProgress(items: ChecklistItem[]) {
    const total = items.length;
    const done = items.filter((i) => i.done).length;
    const pct = total === 0 ? 0 : Math.round((done / total) * 100);
    return { total, done, pct };
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h2 className="text-red-800 font-bold text-lg mb-2">Error</h2>
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      background: "linear-gradient(135deg, #020617 0%, #0b2a5a 45%, #1e3a8a 100%)",
    }}>
      {/* Header */}
      <header style={{
        padding: "14px 24px",
        background: "rgba(255,255,255,0.22)",
        backdropFilter: "blur(10px)",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderBottom: "1px solid rgba(255,255,255,0.12)",
        gap: 14,
        flexWrap: "wrap",
      }}>
        <h1 style={{ margin: 0, color: "white", fontSize: 28, fontWeight: 900 }}>
          NeoCare
        </h1>

        <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          {/* Búsqueda */}
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
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
              fontSize: 14,
              fontWeight: 600,
            }}
          />

          {/* Filtro Etiquetas */}
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
              fontWeight: 700,
              fontSize: 14,
            }}
          >
            {labelOptions.map((o) => (
              <option key={o.id} value={o.id} style={{ color: "#0f172a" }}>
                {o.name}
              </option>
            ))}
          </select>

          {/* Filtro Asignados */}
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
              fontWeight: 700,
              fontSize: 14,
            }}
          >
            {assigneeOptions.map((name) => (
              <option key={name} value={name} style={{ color: "#0f172a" }}>
                {name === "all" ? "Todos" : name}
              </option>
            ))}
          </select>

          <button
            onClick={() => setShowModal(true)}
            style={{
              height: 40,
              padding: "0 16px",
              borderRadius: 12,
              border: "none",
              background: "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
              color: "white",
              fontWeight: 900,
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(37, 99, 235, 0.4)",
              transition: "all 0.2s",
              fontSize: 14,
            }}
          >
            + Nueva tarjeta
          </button>

          <button
            onClick={() => navigate("/my-hours")}
            style={{
              height: 40,
              padding: "0 16px",
              borderRadius: 12,
              border: "1px solid rgba(255,255,255,0.28)",
              background: "rgba(255,255,255,0.16)",
              color: "white",
              fontWeight: 900,
              cursor: "pointer",
              transition: "all 0.2s",
            }}
          >
            Mis horas
          </button>

          <button
            onClick={() => {
              if (selectedBoardId) {
                navigate(`/report/${selectedBoardId}`);
              }
            }}
            style={{
              height: 40,
              padding: "0 16px",
              borderRadius: 12,
              border: "1px solid rgba(255,255,255,0.28)",
              background: "rgba(255,255,255,0.16)",
              color: "white",
              fontWeight: 900,
              cursor: "pointer",
              transition: "all 0.2s",
            }}
          >
            Reporte semanal
          </button>

          <button
            onClick={() => {
              localStorage.removeItem("token");
              navigate("/login");
            }}
            style={{
              height: 40,
              padding: "0 16px",
              borderRadius: 12,
              border: "none",
              background: "linear-gradient(135deg, #dc2626 0%, #991b1b 100%)",
              color: "white",
              fontWeight: 900,
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(220, 38, 38, 0.4)",
              transition: "all 0.2s",
            }}
          >
            Cerrar sesión
          </button>
        </div>
      </header>

      {/* Board */}
      <main style={{ flex: 1, display: "flex", gap: 18, padding: 18 }}>
        {lists.map((list) => {
          const listCards = getCardsForList(list.id);
          return (
            <div key={list.id} style={{
              flex: 1,
              minWidth: 320,
              maxWidth: 420,
              display: "flex",
              flexDirection: "column",
              background: "rgba(255,255,255,0.12)",
              backdropFilter: "blur(10px)",
              borderRadius: 16,
              border: "1px solid rgba(255,255,255,0.18)",
              overflow: "hidden",
            }}>
              {/* List Header */}
              <div style={{
                padding: "14px 18px",
                background: "rgba(255,255,255,0.16)",
                borderBottom: "1px solid rgba(255,255,255,0.12)",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}>
                <h3 style={{ margin: 0, color: "white", fontWeight: 900, fontSize: 16 }}>
                  {list.name}
                </h3>
                <span style={{
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  minWidth: 28,
                  height: 28,
                  padding: "0 10px",
                  borderRadius: 999,
                  background: "rgba(59, 130, 246, 0.9)",
                  color: "white",
                  fontSize: 13,
                  fontWeight: 900,
                }}>
                  {listCards.length}
                </span>
              </div>

              {/* Cards */}
              <div style={{
                flex: 1,
                padding: 14,
                display: "flex",
                flexDirection: "column",
                gap: 12,
                overflowY: "auto",
                minHeight: 400,
              }}>
                {listCards.length === 0 ? (
                  <div style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: "48px 12px",
                    color: "rgba(255,255,255,0.65)",
                    textAlign: "center",
                  }}>
                    <svg style={{ width: 48, height: 48, marginBottom: 12, opacity: 0.5 }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                    </svg>
                    <p style={{ fontSize: 14, fontWeight: 900 }}>No hay tarjetas</p>
                  </div>
                ) : (
                  listCards.map((card) => {
                    const extras = getExtras(card.id);
                    const progress = checklistProgress(extras.checklist);
                    
                    return (
                      <div
                        key={card.id}
                        onClick={() => openEdit(card)}
                        style={{
                          background: "rgba(255,255,255,0.96)",
                          borderRadius: 12,
                          padding: 14,
                          border: "1px solid rgba(15,23,42,0.08)",
                          boxShadow: "0 2px 8px rgba(0,0,0,0.12)",
                          cursor: "pointer",
                          transition: "all 0.2s",
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.boxShadow = "0 4px 16px rgba(0,0,0,0.18)";
                          e.currentTarget.style.transform = "translateY(-2px)";
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.12)";
                          e.currentTarget.style.transform = "translateY(0)";
                        }}
                      >
                        <h4 style={{ margin: 0, fontWeight: 900, fontSize: 15, color: "#0f172a", marginBottom: 8 }}>
                          {card.title}
                        </h4>
                        
                        {card.description && (
                          <p style={{
                            margin: 0,
                            fontSize: 13,
                            color: "rgba(15,23,42,0.65)",
                            lineHeight: 1.5,
                            marginBottom: 8,
                            display: "-webkit-box",
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: "vertical",
                            overflow: "hidden",
                          }}>
                            {card.description}
                          </p>
                        )}
                        
                        {/* Etiquetas */}
                        {extras.labels.length > 0 && (
                          <div style={{ display: "flex", gap: 4, flexWrap: "wrap", marginBottom: 8 }}>
                            {extras.labels.map((label) => (
                              <span
                                key={label.id}
                                style={{
                                  display: "inline-block",
                                  padding: "2px 8px",
                                  borderRadius: 999,
                                  background: label.color,
                                  color: "white",
                                  fontSize: 10,
                                  fontWeight: 900,
                                }}
                              >
                                {label.name}
                              </span>
                            ))}
                          </div>
                        )}
                        
                        {/* Asignado */}
                        {extras.assignee && (
                          <div style={{
                            fontSize: 11,
                            color: "rgba(15,23,42,0.65)",
                            marginBottom: 8,
                            display: "flex",
                            alignItems: "center",
                            gap: 4,
                          }}>
                            <span>👤</span>
                            <span style={{ fontWeight: 700 }}>{extras.assignee}</span>
                          </div>
                        )}
                        
                        {/* Checklist progress */}
                        {progress.total > 0 && (
                          <div style={{
                            fontSize: 11,
                            color: "rgba(15,23,42,0.65)",
                            marginBottom: 8,
                            display: "flex",
                            alignItems: "center",
                            gap: 6,
                          }}>
                            <span>✓</span>
                            <span style={{ fontWeight: 700 }}>{progress.done}/{progress.total}</span>
                            <div style={{
                              flex: 1,
                              height: 4,
                              background: "rgba(15,23,42,0.1)",
                              borderRadius: 999,
                              overflow: "hidden",
                            }}>
                              <div style={{
                                width: `${progress.pct}%`,
                                height: "100%",
                                background: progress.pct === 100 ? "#16a34a" : "#3b82f6",
                                transition: "width 0.3s",
                              }} />
                            </div>
                          </div>
                        )}
                        
                        <div style={{
                          marginTop: 10,
                          display: "flex",
                          alignItems: "center",
                          gap: 8,
                          fontSize: 11,
                          color: "rgba(15,23,42,0.55)",
                          fontWeight: 600,
                        }}>
                          <span>ID: {card.id}</span>
                          {card.due_date && (
                            <>
                              <span>•</span>
                              <span>📅 {new Date(card.due_date).toLocaleDateString()}</span>
                            </>
                          )}
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          );
        })}
      </main>

      {/* Modal para crear tarjeta */}
      {showModal && (
        <div
          role="dialog"
          aria-modal="true"
          onMouseDown={(e) => {
            if (e.target === e.currentTarget) setShowModal(false);
          }}
          style={{
            position: "fixed",
            inset: 0,
            zIndex: 9999,
            background: "rgba(0,0,0,0.55)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: 16,
          }}
        >
          <div style={{
            width: 520,
            maxWidth: "95vw",
            background: "rgba(255,255,255,0.98)",
            borderRadius: 16,
            padding: 24,
            border: "1px solid rgba(15,23,42,0.08)",
            boxShadow: "0 20px 60px rgba(0,0,0,0.4)",
          }}>
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: 20,
            }}>
              <h3 style={{ margin: 0, fontWeight: 900, fontSize: 20, color: "#0f172a" }}>
                {editingCard ? "Editar tarjeta" : "Nueva tarjeta"}
              </h3>
              <button
                onClick={() => setShowModal(false)}
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: "50%",
                  border: "none",
                  background: "rgba(15,23,42,0.08)",
                  color: "#0f172a",
                  fontSize: 20,
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontWeight: 900,
                }}
              >
                ×
              </button>
            </div>
            
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div>
                <label style={{
                  display: "block",
                  fontSize: 13,
                  fontWeight: 900,
                  color: "#0f172a",
                  marginBottom: 6,
                }}>
                  Título *
                </label>
                <input
                  type="text"
                  value={newCard.title}
                  onChange={(e) => setNewCard({ ...newCard, title: e.target.value })}
                  style={{
                    width: "100%",
                    height: 42,
                    borderRadius: 10,
                    border: "1px solid rgba(15,23,42,0.14)",
                    background: "white",
                    padding: "0 12px",
                    fontSize: 14,
                    fontWeight: 600,
                    outline: "none",
                  }}
                  placeholder="Escribe el título..."
                  autoFocus
                  onFocus={(e) => e.target.style.borderColor = "#3b82f6"}
                  onBlur={(e) => e.target.style.borderColor = "rgba(15,23,42,0.14)"}
                />
              </div>

              <div>
                <label style={{
                  display: "block",
                  fontSize: 13,
                  fontWeight: 900,
                  color: "#0f172a",
                  marginBottom: 6,
                }}>
                  Descripción
                </label>
                <textarea
                  value={newCard.description}
                  onChange={(e) => setNewCard({ ...newCard, description: e.target.value })}
                  style={{
                    width: "100%",
                    minHeight: 80,
                    borderRadius: 10,
                    border: "1px solid rgba(15,23,42,0.14)",
                    background: "white",
                    padding: 12,
                    fontSize: 14,
                    fontWeight: 500,
                    outline: "none",
                    resize: "vertical",
                    fontFamily: "inherit",
                  }}
                  placeholder="Escribe una descripción..."
                  onFocus={(e) => e.target.style.borderColor = "#3b82f6"}
                  onBlur={(e) => e.target.style.borderColor = "rgba(15,23,42,0.14)"}
                />
              </div>

              <div>
                <label style={{
                  display: "block",
                  fontSize: 13,
                  fontWeight: 900,
                  color: "#0f172a",
                  marginBottom: 6,
                }}>
                  Lista
                </label>
                <select
                  value={newCard.list_id}
                  onChange={(e) => setNewCard({ ...newCard, list_id: Number(e.target.value) })}
                  style={{
                    width: "100%",
                    height: 42,
                    borderRadius: 10,
                    border: "1px solid rgba(15,23,42,0.14)",
                    background: "white",
                    padding: "0 12px",
                    fontSize: 14,
                    fontWeight: 900,
                    outline: "none",
                    cursor: "pointer",
                  }}
                >
                  {lists.map((list) => (
                    <option key={list.id} value={list.id}>
                      {list.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{
                  display: "block",
                  fontSize: 13,
                  fontWeight: 900,
                  color: "#0f172a",
                  marginBottom: 6,
                }}>
                  Fecha de vencimiento
                </label>
                <input
                  type="date"
                  value={newCard.due_date}
                  onChange={(e) => setNewCard({ ...newCard, due_date: e.target.value })}
                  style={{
                    width: "100%",
                    height: 42,
                    borderRadius: 10,
                    border: "1px solid rgba(15,23,42,0.14)",
                    background: "white",
                    padding: "0 12px",
                    fontSize: 14,
                    fontWeight: 600,
                    outline: "none",
                    cursor: "pointer",
                  }}
                />
              </div>

              <div>
                <label style={{
                  display: "block",
                  fontSize: 13,
                  fontWeight: 900,
                  color: "#0f172a",
                  marginBottom: 6,
                }}>
                  Asignar a
                </label>
                <select
                  value={modalAssignee}
                  onChange={(e) => setModalAssignee(e.target.value)}
                  style={{
                    width: "100%",
                    height: 42,
                    borderRadius: 10,
                    border: "1px solid rgba(15,23,42,0.14)",
                    background: "white",
                    padding: "0 12px",
                    fontSize: 14,
                    fontWeight: 900,
                    outline: "none",
                    cursor: "pointer",
                  }}
                >
                  {TEAM_MEMBERS.map((m) => (
                    <option key={m} value={m}>
                      {m}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{
                  display: "block",
                  fontSize: 13,
                  fontWeight: 900,
                  color: "#0f172a",
                  marginBottom: 6,
                }}>
                  Etiquetas
                </label>
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
                          padding: "0 12px",
                          borderRadius: 999,
                          border: active ? "2px solid rgba(15,23,42,0.3)" : "1px solid rgba(15,23,42,0.12)",
                          background: active ? l.color : "rgba(15,23,42,0.06)",
                          color: active ? "white" : "#0f172a",
                          fontWeight: 900,
                          cursor: "pointer",
                          fontSize: 12,
                          transition: "all 0.2s",
                        }}
                      >
                        {l.name}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div>
                <label style={{
                  display: "block",
                  fontSize: 13,
                  fontWeight: 900,
                  color: "#0f172a",
                  marginBottom: 6,
                }}>
                  Lista de tareas
                </label>
                <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
                  <input
                    type="text"
                    value={newChecklistText}
                    onChange={(e) => setNewChecklistText(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && addChecklistItem()}
                    placeholder="Nueva tarea..."
                    style={{
                      flex: 1,
                      height: 36,
                      borderRadius: 8,
                      border: "1px solid rgba(15,23,42,0.14)",
                      background: "white",
                      padding: "0 10px",
                      fontSize: 13,
                      outline: "none",
                    }}
                  />
                  <button
                    type="button"
                    onClick={addChecklistItem}
                    style={{
                      height: 36,
                      padding: "0 14px",
                      borderRadius: 8,
                      border: "none",
                      background: "#3b82f6",
                      color: "white",
                      fontSize: 12,
                      fontWeight: 900,
                      cursor: "pointer",
                    }}
                  >
                    +
                  </button>
                </div>
                {modalChecklist.length > 0 && (
                  <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                    {modalChecklist.map((item) => (
                      <div
                        key={item.id}
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 8,
                          padding: 8,
                          background: "rgba(15,23,42,0.04)",
                          borderRadius: 8,
                        }}
                      >
                        <input
                          type="checkbox"
                          checked={item.done}
                          onChange={() => toggleChecklistItem(item.id)}
                          style={{ cursor: "pointer" }}
                        />
                        <span
                          style={{
                            flex: 1,
                            fontSize: 13,
                            textDecoration: item.done ? "line-through" : "none",
                            color: item.done ? "rgba(15,23,42,0.45)" : "#0f172a",
                          }}
                        >
                          {item.text}
                        </span>
                        <button
                          type="button"
                          onClick={() => removeChecklistItem(item.id)}
                          style={{
                            width: 24,
                            height: 24,
                            borderRadius: "50%",
                            border: "none",
                            background: "rgba(220, 38, 38, 0.1)",
                            color: "#dc2626",
                            fontSize: 16,
                            cursor: "pointer",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                          }}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div style={{
              marginTop: 24,
              display: "flex",
              justifyContent: "flex-end",
              gap: 10,
            }}>
              <button
                onClick={() => {
                  setShowModal(false);
                  setEditingCard(null);
                  setNewCard({ title: "", description: "", list_id: 1, due_date: "" });
                  setModalLabels([]);
                  setModalAssignee("Sin asignar");
                  setModalChecklist([]);
                }}
                style={{
                  height: 40,
                  padding: "0 20px",
                  borderRadius: 10,
                  border: "1px solid rgba(15,23,42,0.14)",
                  background: "white",
                  color: "#0f172a",
                  fontWeight: 900,
                  cursor: "pointer",
                  fontSize: 14,
                }}
              >
                Cancelar
              </button>
              <button
                onClick={handleCreateCard}
                style={{
                  height: 40,
                  padding: "0 20px",
                  borderRadius: 10,
                  border: "none",
                  background: "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
                  color: "white",
                  fontWeight: 900,
                  cursor: "pointer",
                  fontSize: 14,
                  boxShadow: "0 4px 12px rgba(37, 99, 235, 0.35)",
                }}
              >
                {editingCard ? "Guardar cambios" : "Crear tarjeta"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
