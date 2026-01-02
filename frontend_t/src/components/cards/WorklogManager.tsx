import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";

interface Worklog {
  id: number;
  user_id: number;
  card_id: number;
  date: string;
  hours: number;
  note: string | null;
  created_at: string;
  updated_at: string;
}

interface WorklogManagerProps {
  cardId: number;
  currentUserId: number | null;
}

export default function WorklogManager({ cardId, currentUserId }: WorklogManagerProps) {
  const [worklogs, setWorklogs] = useState<Worklog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [form, setForm] = useState({
    date: new Date().toISOString().split("T")[0],
    hours: 1,
    note: "",
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchWorklogs();
  }, [cardId]);

  async function fetchWorklogs() {
    setLoading(true);
    try {
      const res = await apiFetch(`/cards/${cardId}/worklogs`);
      if (!res.ok) throw new Error("Error al obtener registros de tiempo");
      const data = await res.json();
      setWorklogs(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error cargando worklogs");
    } finally {
      setLoading(false);
    }
  }

  async function handleAddWorklog(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);

    try {
      const res = await apiFetch(`/cards/${cardId}/worklogs`, {
        method: "POST",
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Error al guardar registro");
      }

      setForm({
        date: new Date().toISOString().split("T")[0],
        hours: 1,
        note: "",
      });
      await fetchWorklogs();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error guardando registro");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("¿Estás seguro de eliminar este registro?")) return;

    try {
      const res = await apiFetch(`/worklogs/${id}`, {
        method: "DELETE",
      });

      if (!res.ok) throw new Error("No se pudo eliminar el registro");
      
      setWorklogs(worklogs.filter(w => w.id !== id));
    } catch (err) {
      alert(err instanceof Error ? err.message : "Error al eliminar");
    }
  }

  return (
    <div className="mt-6 border-t pt-4">
      <h4 className="text-lg font-semibold mb-3">Registros de Tiempo (Worklogs)</h4>

      {/* Formulario para añadir */}
      <form onSubmit={handleAddWorklog} className="bg-gray-50 p-3 rounded mb-4 space-y-3">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-700">Fecha</label>
            <input
              type="date"
              required
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              className="w-full text-sm border rounded px-2 py-1"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-700">Horas</label>
            <input
              type="number"
              step="0.25"
              min="0.25"
              required
              value={form.hours}
              onChange={(e) => setForm({ ...form, hours: parseFloat(e.target.value) })}
              className="w-full text-sm border rounded px-2 py-1"
            />
          </div>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-700">Nota (opcional)</label>
          <input
            type="text"
            maxLength={200}
            value={form.note}
            onChange={(e) => setForm({ ...form, note: e.target.value })}
            placeholder="¿En qué has trabajado?"
            className="w-full text-sm border rounded px-2 py-1"
          />
        </div>
        <button
          type="submit"
          disabled={saving}
          className="w-full bg-blue-600 text-white text-sm py-1 rounded hover:bg-blue-700 disabled:bg-blue-300"
        >
          {saving ? "Guardando..." : "Registrar Horas"}
        </button>
      </form>

      {/* Lista de registros */}
      {loading ? (
        <p className="text-sm text-gray-500">Cargando registros...</p>
      ) : worklogs.length === 0 ? (
        <p className="text-sm text-gray-500 italic">No hay horas registradas aún.</p>
      ) : (
        <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
          {worklogs.map((w) => (
            <div key={w.id} className="text-sm border-b pb-2 flex justify-between items-start">
              <div>
                <div className="font-medium">
                  {w.date} — <span className="text-blue-700">{w.hours}h</span>
                </div>
                {w.note && <p className="text-gray-600 text-xs">{w.note}</p>}
              </div>
              {currentUserId === w.user_id && (
                <button
                  onClick={() => handleDelete(w.id)}
                  className="text-red-500 hover:text-red-700 text-xs"
                >
                  Eliminar
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {error && <p className="text-red-600 text-xs mt-2">{error}</p>}
    </div>
  );
}
