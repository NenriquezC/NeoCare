import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

export type CardListID = 1 | 2 | 3;

export interface Card {
  id: number;
  title: string;
  description?: string | null;
  due_date?: string | null;
  list_id: CardListID;
  board_id: number;
  labels?: Array<{ id: string; name: string; color: string }>;
  checklist?: Array<{ id: string; title: string; done: boolean }>;
  assignee_id?: string | null;
}

export type Label = {
  id: string;
  name: string;
  color: "red" | "blue" | "green" | "yellow" | "purple" | "pink" | "orange" | "indigo";
};

export type LabelColor = Label["color"];
export type ChecklistItem = { id: string; title: string; done: boolean };

interface CardsBoardProps {
  boardId: number;
}

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const LISTS: CardListID[] = [1, 2, 3];

const LIST_LABEL: Record<CardListID, string> = {
  1: "Por hacer",
  2: "En progreso",
  3: "Hecho",
};

const PRESET_LABELS: Label[] = [
  { id: "urgent", name: "Urgente", color: "red" },
  { id: "blocked", name: "Bloqueado", color: "yellow" },
  { id: "improve", name: "Mejora", color: "blue" },
  { id: "ready", name: "Listo", color: "green" },
  { id: "feature", name: "Feature", color: "purple" },
  { id: "bug", name: "Bug", color: "pink" },
  { id: "doc", name: "Documentación", color: "indigo" },
  { id: "review", name: "Review", color: "orange" },
];

const TEAM_MEMBERS = [
  { id: "user1", name: "Juan Pérez", avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=user1" },
  { id: "user2", name: "María García", avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=user2" },
  { id: "user3", name: "Carlos López", avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=user3" },
  { id: "user4", name: "Ana Martínez", avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=user4" },
];

// ==================== COMPONENTE: SearchBar ====================
function SearchBar({ value, onChange, placeholder = "Buscar…", resultsCount, totalCount }: any) {
  return (
    <div className="relative">
      <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-10 pr-4 py-2.5 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:bg-blue-50 focus:outline-none transition-colors"
      />
      {value && (
        <button onClick={() => onChange("")} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      )}
      {resultsCount !== undefined && totalCount !== undefined && (
        <p className="text-xs text-gray-500 mt-1">{resultsCount} de {totalCount} resultados</p>
      )}
    </div>
  );
}

// ==================== COMPONENTE: LabelFilter ====================
function LabelFilter({ selectedLabels, onLabelToggle, availableLabels }: any) {
  const colorMap: Record<string, string> = {
    red: "bg-red-100 text-red-800 border-red-300 hover:bg-red-200",
    blue: "bg-blue-100 text-blue-800 border-blue-300 hover:bg-blue-200",
    green: "bg-green-100 text-green-800 border-green-300 hover:bg-green-200",
    yellow: "bg-yellow-100 text-yellow-800 border-yellow-300 hover:bg-yellow-200",
    purple: "bg-purple-100 text-purple-800 border-purple-300 hover:bg-purple-200",
    pink: "bg-pink-100 text-pink-800 border-pink-300 hover:bg-pink-200",
    orange: "bg-orange-100 text-orange-800 border-orange-300 hover:bg-orange-200",
    indigo: "bg-indigo-100 text-indigo-800 border-indigo-300 hover:bg-indigo-200",
  };

  return (
    <div className="flex flex-wrap gap-2">
      {availableLabels.map((label: Label) => {
        const isSelected = selectedLabels.includes(label.id);
        return (
          <button
            key={label.id}
            onClick={() => onLabelToggle(label.id)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium border-2 transition-all ${
              isSelected ? `${colorMap[label.color] || "bg-gray-100"} ring-2 ring-offset-1` : "bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200"
            }`}
          >
            {label.name} {isSelected && "✓"}
          </button>
        );
      })}
    </div>
  );
}

// ==================== COMPONENTE: AssigneeFilter ====================
function AssigneeFilter({ selectedAssignee, onAssigneeChange, teamMembers }: any) {
  const [showDropdown, setShowDropdown] = useState(false);
  const selectedMember = teamMembers.find((m: any) => m.id === selectedAssignee);

  return (
    <div className="relative">
      <button onClick={() => setShowDropdown(!showDropdown)} className="flex items-center gap-2 px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm font-medium">
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
        </svg>
        <span>{selectedMember ? selectedMember.name : "Todos"}</span>
      </button>

      {showDropdown && (
        <div className="absolute z-10 mt-1 w-48 bg-white border border-gray-300 rounded-lg shadow-lg">
          <button onClick={() => { onAssigneeChange(null); setShowDropdown(false); }} className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 ${!selectedAssignee ? "bg-blue-50 font-semibold" : ""}`}>
            Todos
          </button>
          {teamMembers.map((member: any) => (
            <button
              key={member.id}
              onClick={() => { onAssigneeChange(member.id); setShowDropdown(false); }}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 flex items-center gap-2 ${selectedAssignee === member.id ? "bg-blue-50 font-semibold" : ""}`}
            >
              <img src={member.avatar} alt={member.name} className="w-5 h-5 rounded-full" />
              {member.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

// ==================== COMPONENTE: CardItem ====================
function CardItem({ card, onEdit }: any) {
  const checklistProgress = card.checklist ? Math.round((card.checklist.filter((i: any) => i.done).length / card.checklist.length) * 100) : 0;
  const daysUntil = card.due_date ? Math.ceil((new Date(card.due_date).getTime() - new Date().getTime()) / 86400000) : null;

  const colorMap: Record<string, string> = {
    red: "bg-red-100 text-red-800",
    blue: "bg-blue-100 text-blue-800",
    green: "bg-green-100 text-green-800",
    yellow: "bg-yellow-100 text-yellow-800",
    purple: "bg-purple-100 text-purple-800",
    pink: "bg-pink-100 text-pink-800",
    orange: "bg-orange-100 text-orange-800",
    indigo: "bg-indigo-100 text-indigo-800",
  };

  const getDueBadgeColor = (days: number | null) => {
    if (!days) return "";
    if (days < 0) return "bg-red-600 text-white";
    if (days === 0) return "bg-red-500 text-white";
    if (days <= 3) return "bg-orange-500 text-white";
    return "bg-blue-500 text-white";
  };

  return (
    <button onClick={() => onEdit(card)} className="w-full text-left bg-white border border-gray-200 rounded-lg p-3 hover:shadow-lg hover:border-blue-300 transition-all duration-200 group">
      <h4 className="font-semibold text-gray-900 text-sm mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{card.title}</h4>
      {card.description && <p className="text-xs text-gray-600 mb-2 line-clamp-2">{card.description}</p>}
      {card.labels && card.labels.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {card.labels.map((label: any) => (
            <span key={label.id} className={`text-xs px-2 py-1 rounded-full font-medium ${colorMap[label.color] || "bg-gray-100"}`}>
              {label.name}
            </span>
          ))}
        </div>
      )}
      {card.checklist && card.checklist.length > 0 && (
        <div className="mb-2 space-y-1">
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-600">{card.checklist.filter((i: any) => i.done).length}/{card.checklist.length}</span>
            <span className="font-semibold text-gray-700">{checklistProgress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-1.5">
            <div className="bg-green-500 h-1.5 rounded-full transition-all" style={{ width: `${checklistProgress}%` }} />
          </div>
        </div>
      )}
      <div className="flex items-center justify-between text-xs pt-2 border-t border-gray-100">
        {card.due_date ? (
          <span className={`px-2 py-1 rounded-md font-medium ${getDueBadgeColor(daysUntil)}`}>
            {daysUntil && daysUntil < 0 ? `Vencido hace ${Math.abs(daysUntil)} días` : daysUntil === 0 ? "Hoy" : `${daysUntil} días`}
          </span>
        ) : (
          <span className="text-gray-400">Sin fecha</span>
        )}
        {card.assignee_id && <div className="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-bold">{card.assignee_id.charAt(0).toUpperCase()}</div>}
      </div>
    </button>
  );
}

// ==================== COMPONENTE PRINCIPAL ====================
export default function CardsBoard({ boardId }: CardsBoardProps) {
  const navigate = useNavigate();
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
    labels: [] as Label[],
    checklist: [] as ChecklistItem[],
    assignee_id: null as string | null,
  });

  const [formErrors, setFormErrors] = useState<{ title?: string }>({});
  const [searchText, setSearchText] = useState("");
  const [selectedLabels, setSelectedLabels] = useState<string[]>([]);
  const [selectedAssignee, setSelectedAssignee] = useState<string | null>(null);

  function getToken() {
    return localStorage.getItem("token");
  }

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
      const res = await fetch(`${BASE_URL}/cards?board_id=${encodeURIComponent(boardId)}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Error al obtener tarjetas");
      const data = await res.json();
      setCards(data || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error cargando tarjetas");
    } finally {
      setLoading(false);
    }
  }

  function openCreate() {
    setEditingCard(null);
    setForm({ title: "", description: "", due_date: "", list_id: 1, labels: [], checklist: [], assignee_id: null });
    setFormErrors({});
    setShowModal(true);
  }

  function openEdit(card: Card) {
    setEditingCard(card);
    setForm({
      title: card.title,
      description: card.description || "",
      due_date: card.due_date ? card.due_date.split("T")[0] : "",
      list_id: card.list_id,
      labels: card.labels || [],
      checklist: card.checklist || [],
      assignee_id: card.assignee_id || null,
    });
    setShowModal(true);
  }

  function closeModal() {
    setShowModal(false);
    setEditingCard(null);
    setFormErrors({});
  }

  function validateForm() {
    const errors: any = {};
    if (!form.title.trim()) errors.title = "El título es obligatorio.";
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  }

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
      labels: form.labels,
      checklist: form.checklist,
      assignee_id: form.assignee_id,
    };

    try {
      const url = editingCard ? `${BASE_URL}/cards/${editingCard.id}` : `${BASE_URL}/cards`;
      const method = editingCard ? "PATCH" : "POST";
      const res = await fetch(url, {
        method,
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
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

  const filteredCards = useMemo(() => {
    let result = [...cards];
    const q = searchText.trim().toLowerCase();
    if (q) {
      result = result.filter((c) => c.title.toLowerCase().includes(q) || (c.description || "").toLowerCase().includes(q));
    }
    if (selectedLabels.length > 0) {
      result = result.filter((c) => {
        const cardLabelIds = (c.labels || []).map((l) => l.id);
        return selectedLabels.some((labelId) => cardLabelIds.includes(labelId));
      });
    }
    if (selectedAssignee) {
      result = result.filter((c) => c.assignee_id === selectedAssignee);
    }
    return result;
  }, [cards, searchText, selectedLabels, selectedAssignee]);

  const grouped: Record<CardListID, Card[]> = useMemo(() => {
    return LISTS.reduce<Record<CardListID, Card[]>>((acc, list) => {
      acc[list] = filteredCards.filter((c) => c.list_id === list);
      return acc;
    }, { 1: [], 2: [], 3: [] });
  }, [filteredCards]);

  return (
    <div className="p-4 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate("/boards")}
              className="px-3 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium text-sm flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Volver a Tableros
            </button>
            <div>
              <h2 className="text-3xl font-bold text-gray-900">Tablero Kanban</h2>
              <p className="text-sm text-gray-600 mt-1">
                {searchText || selectedLabels.length > 0 || selectedAssignee ? (
                  <>Mostrando <span className="font-semibold">{filteredCards.length}</span> tarjeta{filteredCards.length !== 1 ? "s" : ""}</>
                ) : (
                  <>Total: <span className="font-semibold">{cards.length}</span> tarjeta{cards.length !== 1 ? "s" : ""}</>
                )}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-200 shadow-sm hover:shadow-md font-medium" onClick={openCreate}>
              + Nueva tarjeta
            </button>
            <button className="px-4 py-2 bg-white text-gray-700 rounded-lg border border-gray-300 hover:bg-gray-50 transition-all duration-200 font-medium" onClick={fetchCards} disabled={loading}>
              {loading ? "Cargando…" : "Actualizar"}
            </button>
          </div>
        </div>

        {tokenMissing && (
          <div className="mb-4 p-4 bg-yellow-50 text-yellow-800 rounded-lg border border-yellow-200 flex items-start gap-3">
            <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p>No se encontró el token JWT. Inicia sesión para continuar.</p>
          </div>
        )}

        {error && (
          <div className="mb-4 p-4 bg-red-50 text-red-800 rounded-lg border border-red-200 flex items-start gap-3">
            <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <p>{error}</p>
          </div>
        )}
      </div>

      <div className="mb-6 bg-white rounded-lg shadow-sm p-4">
        <div className="space-y-4">
          <SearchBar value={searchText} onChange={setSearchText} placeholder="Buscar por título o descripción…" resultsCount={filteredCards.length} totalCount={cards.length} />

          <div className="flex flex-wrap gap-3 items-center">
            <LabelFilter
              selectedLabels={selectedLabels}
              onLabelToggle={(labelId: string) => {
                setSelectedLabels((prev) => (prev.includes(labelId) ? prev.filter((id) => id !== labelId) : [...prev, labelId]));
              }}
              availableLabels={PRESET_LABELS}
            />

            <AssigneeFilter selectedAssignee={selectedAssignee} onAssigneeChange={setSelectedAssignee} teamMembers={TEAM_MEMBERS} />

            {(searchText || selectedLabels.length > 0 || selectedAssignee) && (
              <button
                onClick={() => {
                  setSearchText("");
                  setSelectedLabels([]);
                  setSelectedAssignee(null);
                }}
                className="px-3 py-2 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded border border-red-200 font-medium transition-colors"
              >
                Limpiar filtros
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {LISTS.map((list) => (
          <div key={list} className="flex flex-col bg-white rounded-lg shadow-md overflow-hidden transition-all duration-200 hover:shadow-lg">
            <div className="bg-gradient-to-r from-blue-50 to-blue-100 px-4 py-3 border-b border-blue-200">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-gray-900">{LIST_LABEL[list]}</h3>
                <span className="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-sm font-semibold bg-blue-600 text-white">{grouped[list].length}</span>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-3 space-y-3 bg-gray-50/50 min-h-96">
              {grouped[list].length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 text-gray-500">
                  <svg className="w-12 h-12 mb-2 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                  </svg>
                  <p className="text-sm font-medium">No hay tarjetas</p>
                </div>
              ) : (
                grouped[list].map((card) => <CardItem key={card.id} card={card} onEdit={openEdit} />)
              )}
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50 backdrop-blur-sm">
          <div className="bg-white w-full max-w-2xl rounded-lg shadow-xl max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 flex justify-between items-center px-6 py-4 border-b bg-gradient-to-r from-blue-50 to-blue-100">
              <h3 className="text-xl font-bold text-gray-900">{editingCard ? "✏️ Editar tarjeta" : "➕ Nueva tarjeta"}</h3>
              <button onClick={closeModal} className="text-gray-400 hover:text-gray-600 transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <form className="p-6 space-y-5" onSubmit={handleSave}>
              <div className="space-y-4">
                <h4 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Información General</h4>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Título <span className="text-red-500">*</span></label>
                  <input
                    type="text"
                    value={form.title}
                    maxLength={80}
                    required
                    onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                    className={`w-full px-4 py-2.5 rounded-lg border-2 transition-colors focus:outline-none ${
                      formErrors.title ? "border-red-500 focus:border-red-600" : "border-gray-300 focus:border-blue-500 focus:bg-blue-50"
                    }`}
                    placeholder="Ingresa el título de la tarjeta…"
                  />
                  {formErrors.title && <p className="text-sm text-red-600 mt-1 flex items-center gap-1"><span>⚠️</span> {formErrors.title}</p>}
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Descripción</label>
                  <textarea rows={3} value={form.description} onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))} className="w-full px-4 py-2.5 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:bg-blue-50 focus:outline-none transition-colors" placeholder="Añade detalles sobre esta tarjeta…" />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Fecha límite</label>
                    <input type="date" value={form.due_date} onChange={(e) => setForm((f) => ({ ...f, due_date: e.target.value }))} className="w-full px-4 py-2.5 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:bg-blue-50 focus:outline-none transition-colors" />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Estado</label>
                    <select value={form.list_id} onChange={(e) => setForm((f) => ({ ...f, list_id: Number(e.target.value) as CardListID }))} className="w-full px-4 py-2.5 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:bg-blue-50 focus:outline-none transition-colors">
                      {LISTS.map((id) => (
                        <option key={id} value={id}>
                          {LIST_LABEL[id]}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              <div className="border-t border-gray-200" />

              <div>
                <h4 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Etiquetas & Prioridad</h4>
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    {form.labels.length === 0 ? (
                      <p className="text-sm text-gray-500">Sin etiquetas</p>
                    ) : form.labels.map((label) => (
                      <div key={label.id} className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 border border-blue-300">
                        <span>{label.name}</span>
                        <button type="button" onClick={() => setForm((f) => ({ ...f, labels: f.labels.filter((l) => l.id !== label.id) }))} className="hover:opacity-70 transition-opacity">
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>

                  {form.labels.length < PRESET_LABELS.length && (
                    <button
                      type="button"
                      onClick={() => {
                        const available = PRESET_LABELS.find((p) => !form.labels.find((l) => l.id === p.id));
                        if (available) {
                          setForm((f) => ({ ...f, labels: [...f.labels, available] }));
                        }
                      }}
                      className="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
                    >
                      + Añadir etiqueta
                    </button>
                  )}
                </div>
              </div>

              <div className="border-t border-gray-200" />

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Responsable</label>
                <select value={form.assignee_id || ""} onChange={(e) => setForm((f) => ({ ...f, assignee_id: e.target.value || null }))} className="w-full px-4 py-2.5 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:bg-blue-50 focus:outline-none transition-colors">
                  <option value="">Sin asignar</option>
                  {TEAM_MEMBERS.map((member) => (
                    <option key={member.id} value={member.id}>{member.name}</option>
                  ))}
                </select>
              </div>

              <div className="flex gap-3 pt-4 border-t">
                <button type="submit" disabled={saving} className="flex-1 px-4 py-2.5 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400">
                  {saving ? "Guardando…" : editingCard ? "Guardar cambios" : "Crear tarjeta"}
                </button>

                <button type="button" onClick={closeModal} disabled={saving} className="flex-1 px-4 py-2.5 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50">
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
