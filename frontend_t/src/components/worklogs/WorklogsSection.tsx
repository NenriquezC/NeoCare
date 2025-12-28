// src/components/worklogs/WorklogsSection.tsx
import React, { useEffect, useMemo, useState } from "react";
import {
    createWorklog,
    deleteWorklog,
    getMe,
    hoursToNumber,
    listWorklogsByCard,
    updateWorklog,
    type Worklog,
} from "../../lib/worklogs";

function todayYMD(): string {
const d = new Date();
const y = d.getFullYear();
const m = String(d.getMonth() + 1).padStart(2, "0");
const day = String(d.getDate()).padStart(2, "0");
return `${y}-${m}-${day}`;
}

type Props = {
cardId: number;
};

export default function WorklogsSection({ cardId }: Props) {
const [meId, setMeId] = useState<number | null>(null);

const [loading, setLoading] = useState(false);
const [saving, setSaving] = useState(false);
const [error, setError] = useState<string | null>(null);

const [items, setItems] = useState<Worklog[]>([]);

  // formulario crear
const [date, setDate] = useState(todayYMD());
const [hours, setHours] = useState("1");
const [note, setNote] = useState("");

  // edición inline simple
const [editingId, setEditingId] = useState<number | null>(null);
const [editHours, setEditHours] = useState("");
const [editNote, setEditNote] = useState("");

const totalHours = useMemo(() => {
    return items.reduce((acc, w) => acc + hoursToNumber(w.hours), 0);
}, [items]);

async function load() {
    setLoading(true);
    setError(null);
    try {
    const [me, logs] = await Promise.all([getMe(), listWorklogsByCard(cardId)]);
    setMeId(me?.id ?? null);
    setItems(logs);
    } catch (e) {
    setError(e instanceof Error ? e.message : "Error cargando horas");
    } finally {
    setLoading(false);
    }
}

useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
}, [cardId]);

function validateCreate(): string | null {
    if (!date) return "La fecha es obligatoria.";
    const h = Number(hours.replace(",", "."));
    if (!Number.isFinite(h) || h <= 0) return "Horas inválidas (debe ser > 0).";
    if (note.length > 200) return "La nota no puede superar 200 caracteres.";
    return null;
}

async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    const msg = validateCreate();
    if (msg) {
    setError(msg);
    return;
    }

    setSaving(true);
    try {
    const created = await createWorklog({
        card_id: cardId,
        date,
        hours: Number(hours.replace(",", ".")),
        note: note.trim() || null,
    });

      // refresco simple (seguro)
    setItems((prev) => [created, ...prev]);
    setNote("");
    setHours("1");
    } catch (e) {
    setError(e instanceof Error ? e.message : "Error creando registro");
    } finally {
    setSaving(false);
    }
}

function canEdit(w: Worklog) {
    // Si no sabemos el usuario, no mostramos botones (el backend igual protege)
    if (meId == null) return false;
    return w.user_id === meId;
}

function startEdit(w: Worklog) {
    setEditingId(w.id);
    setEditHours(String(hoursToNumber(w.hours)));
    setEditNote(w.note ?? "");
}

function cancelEdit() {
    setEditingId(null);
    setEditHours("");
    setEditNote("");
}

async function saveEdit(w: Worklog) {
    setError(null);
    const h = Number(editHours.replace(",", "."));
    if (!Number.isFinite(h) || h <= 0) {
    setError("Horas inválidas (debe ser > 0).");
    return;
    }
    if (editNote.length > 200) {
    setError("La nota no puede superar 200 caracteres.");
    return;
    }

    setSaving(true);
    try {
    const updated = await updateWorklog(w.id, {
        hours: h,
        note: editNote.trim() || null,
    });

    setItems((prev) => prev.map((x) => (x.id === updated.id ? updated : x)));
    cancelEdit();
    } catch (e) {
    setError(e instanceof Error ? e.message : "Error editando registro");
    } finally {
    setSaving(false);
    }
}

async function remove(w: Worklog) {
    const ok = window.confirm("¿Eliminar este registro de horas?");
    if (!ok) return;

    setSaving(true);
    setError(null);
    try {
    await deleteWorklog(w.id);
    setItems((prev) => prev.filter((x) => x.id !== w.id));
    } catch (e) {
    setError(e instanceof Error ? e.message : "Error eliminando registro");
    } finally {
    setSaving(false);
    }
}

 // ========================
  // RENDER
  // ========================
return (
  <section style={{ marginTop: 24 }}>
    {/* Título sección */}
    <h4 style={{ marginBottom: 12, fontWeight: 800, color: "#0f172a" }}>
      Horas trabajadas
    </h4>

    {loading && <div style={{ fontSize: 14 }}>Cargando horas…</div>}

    {error && (
      <div style={{ marginBottom: 8, color: "#7f1d1d", fontWeight: 600 }}>
        {error}
      </div>
    )}

    {/* === CONTENEDOR ESTILO "EDITAR TARJETA" === */}
    <div
      style={{
        background: "#e8f2ff",
        padding: 16,
        borderRadius: 12,
        border: "1px solid #bfdbfe",
      }}
    >
      {/* Inputs */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <div>
          <label style={{ fontSize: 13, fontWeight: 700 }}>Fecha</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            style={{
              width: "100%",
              padding: 10,
              borderRadius: 8,
              border: "1px solid #93c5fd",
            }}
          />
        </div>

        <div>
          <label style={{ fontSize: 13, fontWeight: 700 }}>Horas</label>
          <input
            inputMode="decimal"
            value={hours}
            onChange={(e) => setHours(e.target.value)}
            style={{
              width: "100%",
              padding: 10,
              borderRadius: 8,
              border: "1px solid #93c5fd",
            }}
          />
          <div style={{ fontSize: 12, opacity: 0.75 }}>
            Ej: 0.5, 1, 2.25
          </div>
        </div>

        <div style={{ gridColumn: "1 / -1" }}>
          <label style={{ fontSize: 13, fontWeight: 700 }}>
            Nota <span style={{ fontWeight: 400 }}>(máx 200)</span>
          </label>
          <input
            value={note}
            maxLength={200}
            onChange={(e) => setNote(e.target.value)}
            style={{
              width: "100%",
              padding: 10,
              borderRadius: 8,
              border: "1px solid #93c5fd",
            }}
          />
        </div>
      </div>

      {/* Acciones */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          marginTop: 14,
        }}
      >
        <button
          type="button"
          onClick={handleCreate}
          disabled={saving}
          style={{
            background: "#22c55e",
            color: "white",
            fontWeight: 700,
            padding: "8px 14px",
            borderRadius: 8,
            border: "none",
          }}
        >
          {saving ? "Guardando…" : "Añadir horas"}
        </button>

        <button
          type="button"
          onClick={load}
          disabled={saving}
          style={{
            background: "#334155",
            color: "white",
            fontWeight: 700,
            padding: "8px 14px",
            borderRadius: 8,
            border: "none",
          }}
        >
          Actualizar lista
        </button>

        <div style={{ marginLeft: "auto", fontWeight: 800 }}>
          Total tarjeta: {totalHours.toFixed(2)} h
        </div>
      </div>
    </div>

    {/* === LISTADO === */}
    <div style={{ marginTop: 16 }}>
      {items.length === 0 ? (
        <div style={{ fontSize: 14, opacity: 0.8 }}>
          (Sin registros aún)
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {items.map((w) => (
            <div
              key={w.id}
              style={{
                background: "#f0f7ff",
                borderRadius: 10,
                padding: 12,
                border: "1px solid #c7ddff",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <strong>
                  {w.date} — {hoursToNumber(w.hours).toFixed(2)} h
                </strong>

                {canEdit(w) && (
                  <div style={{ display: "flex", gap: 8 }}>
                    {editingId === w.id ? (
                      <>
                        <button onClick={() => saveEdit(w)}>Guardar</button>
                        <button onClick={cancelEdit}>Cancelar</button>
                      </>
                    ) : (
                      <>
                        <button onClick={() => startEdit(w)}>Editar</button>
                        <button onClick={() => remove(w)}>Eliminar</button>
                      </>
                    )}
                  </div>
                )}
              </div>

              {editingId === w.id ? (
                <div
                  style={{
                    marginTop: 8,
                    display: "grid",
                    gridTemplateColumns: "1fr 2fr",
                    gap: 8,
                  }}
                >
                  <input
                    value={editHours}
                    onChange={(e) => setEditHours(e.target.value)}
                  />
                  <input
                    value={editNote}
                    maxLength={200}
                    onChange={(e) => setEditNote(e.target.value)}
                  />
                </div>
              ) : (
                w.note && (
                  <div style={{ marginTop: 6, opacity: 0.85 }}>
                    {w.note}
                  </div>
                )
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  </section>
);}