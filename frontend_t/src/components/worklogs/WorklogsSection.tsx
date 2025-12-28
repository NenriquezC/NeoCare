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

return (
    <section style={{ marginTop: 16, paddingTop: 16, borderTop: "1px solid rgba(0,0,0,0.15)" }}>
    <h4 style={{ margin: "0 0 8px 0" }}>Horas trabajadas</h4>

    {loading ? (
        <div style={{ fontSize: 14 }}>Cargando horas…</div>
    ) : null}

    {error ? (
        <div style={{ marginTop: 8, marginBottom: 8, color: "#7f1d1d" }}>
        {error}
        </div>
    ) : null}

      {/* Formulario crear */}
    <form onSubmit={handleCreate} style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <div>
        <label style={{ display: "block", fontSize: 12, fontWeight: 700 }}>Fecha</label>
        <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            style={{ width: "100%", padding: 8, borderRadius: 6, border: "1px solid #93c5fd" }}
        />
        </div>

        <div>
        <label style={{ display: "block", fontSize: 12, fontWeight: 700 }}>Horas</label>
        <input
            inputMode="decimal"
            value={hours}
            onChange={(e) => setHours(e.target.value)}
            style={{ width: "100%", padding: 8, borderRadius: 6, border: "1px solid #93c5fd" }}
        />
        <div style={{ fontSize: 12, opacity: 0.75 }}>Ej: 0.5, 1, 2.25</div>
        </div>

        <div style={{ gridColumn: "1 / -1" }}>
        <label style={{ display: "block", fontSize: 12, fontWeight: 700 }}>
            Nota <span style={{ fontWeight: 400 }}>(máx 200)</span>
        </label>
        <input
            value={note}
            maxLength={200}
            onChange={(e) => setNote(e.target.value)}
            style={{ width: "100%", padding: 8, borderRadius: 6, border: "1px solid #93c5fd" }}
        />
        </div>

        <div style={{ gridColumn: "1 / -1", display: "flex", gap: 8 }}>
        <button
            type="submit"
            disabled={saving}
            style={{ padding: "8px 12px", borderRadius: 6, border: "none", background: "#10b981", color: "white" }}
        >
            {saving ? "Guardando…" : "Añadir horas"}
        </button>

        <button
            type="button"
            onClick={load}
            disabled={saving}
            style={{ padding: "8px 12px", borderRadius: 6, border: "none", background: "#334155", color: "white" }}
        >
            Actualizar lista
        </button>

        <div style={{ marginLeft: "auto", fontWeight: 800 }}>
            Total tarjeta: {totalHours.toFixed(2)} h
        </div>
        </div>
    </form>

      {/* Listado */}
    <div style={{ marginTop: 12 }}>
        {items.length === 0 ? (
        <div style={{ fontSize: 14, opacity: 0.8 }}>(Sin registros aún)</div>
        ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {items.map((w) => (
            <div
                key={w.id}
                style={{
                background: "rgba(255,255,255,0.75)",
                border: "1px solid rgba(147,197,253,0.9)",
                borderRadius: 10,
                padding: 10,
                }}
            >
                <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                <div style={{ fontWeight: 800 }}>
                    {w.date} — {hoursToNumber(w.hours).toFixed(2)} h
                </div>

                {canEdit(w) ? (
                    <div style={{ display: "flex", gap: 8 }}>
                    {editingId === w.id ? (
                        <>
                        <button type="button" onClick={() => saveEdit(w)} disabled={saving}>
                            Guardar
                        </button>
                        <button type="button" onClick={cancelEdit} disabled={saving}>
                            Cancelar
                        </button>
                        </>
                    ) : (
                        <>
                        <button type="button" onClick={() => startEdit(w)} disabled={saving}>
                            Editar
                        </button>
                        <button type="button" onClick={() => remove(w)} disabled={saving}>
                            Eliminar
                        </button>
                        </>
                    )}
                    </div>
                ) : null}
                </div>

                {editingId === w.id ? (
                <div style={{ marginTop: 8, display: "grid", gridTemplateColumns: "1fr 2fr", gap: 8 }}>
                    <input
                    value={editHours}
                    onChange={(e) => setEditHours(e.target.value)}
                    style={{ padding: 8, borderRadius: 6, border: "1px solid #93c5fd" }}
                    />
                    <input
                    value={editNote}
                    maxLength={200}
                    onChange={(e) => setEditNote(e.target.value)}
                    style={{ padding: 8, borderRadius: 6, border: "1px solid #93c5fd" }}
                    />
                </div>
                ) : (
                w.note ? <div style={{ marginTop: 6, opacity: 0.85 }}>{w.note}</div> : null
                )}
            </div>
            ))}
        </div>
        )}
    </div>
    </section>
);
}