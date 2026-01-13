import React, { useEffect, useState } from "react";
import {
  listWorklogsByCard,
  createWorklog,
  updateWorklog,
  deleteWorklog,
  hoursToNumber,
  type Worklog,
} from "@/lib/worklogs";

interface WorklogsSectionProps {
  cardId: number;
  currentUserId?: number;
}

export default function WorklogsSection({ cardId, currentUserId }: WorklogsSectionProps) {
  const [worklogs, setWorklogs] = useState<Worklog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Form state para crear
  const [showForm, setShowForm] = useState(false);
  const [formDate, setFormDate] = useState(new Date().toISOString().split("T")[0]);
  const [formHours, setFormHours] = useState<number>(0.25);
  const [formNote, setFormNote] = useState("");
  const [formLoading, setFormLoading] = useState(false);

  // Edit state
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editDate, setEditDate] = useState("");
  const [editHours, setEditHours] = useState<number>(0.25);
  const [editNote, setEditNote] = useState("");

  useEffect(() => {
    loadWorklogs();
  }, [cardId]);

  async function loadWorklogs() {
    setLoading(true);
    setError(null);
    try {
      const data = await listWorklogsByCard(cardId);
      setWorklogs(data);
    } catch (e: any) {
      setError(e?.message || "Error cargando registros de horas");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (formHours < 0.25) {
      setError("Las horas deben ser al menos 0.25");
      return;
    }
    if (formDate > new Date().toISOString().split("T")[0]) {
      setError("No se pueden registrar horas en fechas futuras");
      return;
    }

    setFormLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await createWorklog({
        card_id: cardId,
        date: formDate,
        hours: formHours,
        note: formNote.trim() || null,
      });
      setSuccess("✅ Registro guardado");
      setFormDate(new Date().toISOString().split("T")[0]);
      setFormHours(0.25);
      setFormNote("");
      setShowForm(false);
      await loadWorklogs();
      setTimeout(() => setSuccess(null), 3000);
    } catch (e: any) {
      setError(e?.message || "Error al guardar registro");
    } finally {
      setFormLoading(false);
    }
  }

  function startEdit(worklog: Worklog) {
    setEditingId(worklog.id);
    setEditDate(worklog.date);
    setEditHours(hoursToNumber(worklog.hours));
    setEditNote(worklog.note || "");
    setError(null);
  }

  function cancelEdit() {
    setEditingId(null);
    setEditDate("");
    setEditHours(0.25);
    setEditNote("");
    setError(null);
  }

  async function handleUpdate(id: number) {
    if (editHours < 0.25) {
      setError("Las horas deben ser al menos 0.25");
      return;
    }
    if (editDate > new Date().toISOString().split("T")[0]) {
      setError("No se pueden registrar horas en fechas futuras");
      return;
    }

    setError(null);
    try {
      await updateWorklog(id, {
        date: editDate,
        hours: editHours,
        note: editNote.trim() || null,
      });
      setSuccess("✅ Registro actualizado");
      cancelEdit();
      await loadWorklogs();
      setTimeout(() => setSuccess(null), 3000);
    } catch (e: any) {
      setError(e?.message || "Error al actualizar");
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("¿Seguro que deseas eliminar este registro?")) return;

    setError(null);
    try {
      await deleteWorklog(id);
      setSuccess("✅ Registro eliminado");
      await loadWorklogs();
      setTimeout(() => setSuccess(null), 3000);
    } catch (e: any) {
      setError(e?.message || "Error al eliminar");
    }
  }

  const totalHours = worklogs.reduce((sum, w) => sum + hoursToNumber(w.hours), 0);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">
            ⏱️ Horas Trabajadas
          </h4>
          <p className="text-xs text-gray-500 mt-1">
            Total: <span className="font-bold text-blue-600">{totalHours.toFixed(2)}h</span> en {worklogs.length} registro{worklogs.length !== 1 ? "s" : ""}
          </p>
        </div>

        {!showForm && (
          <button
            type="button"
            onClick={() => setShowForm(true)}
            className="px-3 py-1.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            + Registrar horas
          </button>
        )}
      </div>

      {/* Mensajes */}
      {error && (
        <div className="p-3 bg-red-50 text-red-800 rounded-lg border border-red-200 text-sm flex items-start gap-2">
          <span>⚠️</span>
          <p>{error}</p>
        </div>
      )}

      {success && (
        <div className="p-3 bg-green-50 text-green-800 rounded-lg border border-green-200 text-sm">
          {success}
        </div>
      )}

      {/* Formulario crear */}
      {showForm && (
        <form onSubmit={handleCreate} className="p-4 bg-blue-50 rounded-lg border-2 border-blue-200 space-y-3">
          <h5 className="font-semibold text-gray-800 text-sm">Nuevo registro</h5>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Fecha <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                value={formDate}
                max={new Date().toISOString().split("T")[0]}
                required
                onChange={(e) => setFormDate(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none text-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Horas <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                step="0.25"
                min="0.25"
                value={formHours}
                required
                onChange={(e) => setFormHours(parseFloat(e.target.value))}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none text-sm"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Nota (opcional, máx. 200 caracteres)
            </label>
            <textarea
              value={formNote}
              maxLength={200}
              rows={2}
              onChange={(e) => setFormNote(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none text-sm resize-none"
              placeholder="Describe qué trabajaste..."
            />
            <p className="text-xs text-gray-500 mt-1">{formNote.length}/200</p>
          </div>

          <div className="flex gap-2">
            <button
              type="submit"
              disabled={formLoading}
              className="flex-1 px-3 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition-colors"
            >
              {formLoading ? "Guardando..." : "Guardar"}
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              disabled={formLoading}
              className="flex-1 px-3 py-2 bg-gray-200 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-300 disabled:opacity-50 transition-colors"
            >
              Cancelar
            </button>
          </div>
        </form>
      )}

      {/* Lista de worklogs */}
      {loading ? (
        <div className="text-center py-4 text-gray-500 text-sm">Cargando...</div>
      ) : worklogs.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <svg className="w-12 h-12 mx-auto mb-2 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-sm">No hay registros de horas para esta tarjeta</p>
        </div>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {worklogs.map((worklog) => {
            const isOwn = currentUserId && worklog.user_id === currentUserId;
            const isEditing = editingId === worklog.id;

            if (isEditing) {
              return (
                <div key={worklog.id} className="p-3 bg-yellow-50 rounded-lg border-2 border-yellow-300 space-y-2">
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">Fecha</label>
                      <input
                        type="date"
                        value={editDate}
                        max={new Date().toISOString().split("T")[0]}
                        onChange={(e) => setEditDate(e.target.value)}
                        className="w-full px-2 py-1.5 rounded border border-gray-300 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">Horas</label>
                      <input
                        type="number"
                        step="0.25"
                        min="0.25"
                        value={editHours}
                        onChange={(e) => setEditHours(parseFloat(e.target.value))}
                        className="w-full px-2 py-1.5 rounded border border-gray-300 text-sm"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">Nota</label>
                    <textarea
                      value={editNote}
                      maxLength={200}
                      rows={2}
                      onChange={(e) => setEditNote(e.target.value)}
                      className="w-full px-2 py-1.5 rounded border border-gray-300 text-sm resize-none"
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleUpdate(worklog.id)}
                      className="flex-1 px-2 py-1.5 bg-green-600 text-white text-xs font-medium rounded hover:bg-green-700"
                    >
                      Guardar
                    </button>
                    <button
                      onClick={cancelEdit}
                      className="flex-1 px-2 py-1.5 bg-gray-300 text-gray-700 text-xs font-medium rounded hover:bg-gray-400"
                    >
                      Cancelar
                    </button>
                  </div>
                </div>
              );
            }

            return (
              <div
                key={worklog.id}
                className={`p-3 rounded-lg border ${
                  isOwn ? "bg-white border-blue-200" : "bg-gray-50 border-gray-200"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-semibold text-gray-900">
                        {new Date(worklog.date).toLocaleDateString("es-ES", {
                          weekday: "short",
                          day: "numeric",
                          month: "short",
                        })}
                      </span>
                      <span className="px-2 py-0.5 bg-blue-100 text-blue-800 text-xs font-bold rounded">
                        {hoursToNumber(worklog.hours).toFixed(2)}h
                      </span>
                    </div>
                    {worklog.note && (
                      <p className="text-sm text-gray-600 mt-1">{worklog.note}</p>
                    )}
                    <p className="text-xs text-gray-400 mt-1">
                      ID: {worklog.user_id} {isOwn && "· (tú)"}
                    </p>
                  </div>

                  {isOwn && (
                    <div className="flex gap-1 ml-2">
                      <button
                        onClick={() => startEdit(worklog)}
                        className="p-1.5 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                        title="Editar"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        onClick={() => handleDelete(worklog.id)}
                        className="p-1.5 text-red-600 hover:bg-red-50 rounded transition-colors"
                        title="Eliminar"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

