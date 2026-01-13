// src/pages/MyHours.tsx
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createWorklog, hoursToNumber, listMyWorklogsByWeek, type Worklog } from "../lib/worklogs";
import { apiFetch } from "../lib/api";

function getISOWeekString(d = new Date()): string {
  const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  const dayNum = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil((((date.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  const year = date.getUTCFullYear();
  // Formato YYYY-WW (sin la letra W en el medio)
  return `${year}-${String(weekNo).padStart(2, "0")}`;
}

export default function MyHours() {
  const navigate = useNavigate();
  const [week, setWeek] = useState(getISOWeekString());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [items, setItems] = useState<Worklog[]>([]);

  // Estado para el formulario de registro de horas
  const [formDate, setFormDate] = useState(new Date().toISOString().split("T")[0]);
  const [formHours, setFormHours] = useState(0.25);
  const [formNote, setFormNote] = useState("");
  const [formLoading, setFormLoading] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [formSuccess, setFormSuccess] = useState<string | null>(null);

  // Boards y cards para selección
  const [boards, setBoards] = useState<{ id: number; name: string }[]>([]);
  const [cards, setCards] = useState<{ id: number; title: string; board_id: number }[]>([]);
  const [selectedBoardId, setSelectedBoardId] = useState<number | null>(null);
  const [selectedCardId, setSelectedCardId] = useState<number | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await listMyWorklogsByWeek(week);

      
    // 👇 el backend devuelve un objeto con `entries`
        setItems(Array.isArray(data.entries) ? data.entries : []);
        
    } catch (e: any) {
      if (e && e.error) setError(e.error);
      else setError(e instanceof Error ? e.message : "Error cargando mis horas");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [week]);

  const totalsByDay = useMemo(() => {
    const map = new Map<string, number>();
    for (const w of items) {
      map.set(w.date, (map.get(w.date) ?? 0) + hoursToNumber(w.hours));
    }
    return Array.from(map.entries()).sort((a, b) => a[0].localeCompare(b[0]));
  }, [items]);

  const totalWeek = useMemo(
    () => totalsByDay.reduce((acc, [, h]) => acc + h, 0),
    [totalsByDay]
  );

  // Cargar boards al montar
  useEffect(() => {
    async function loadBoards() {
      try {
        const res = await apiFetch("/boards/", { method: "GET" });
        const data = await res.json();
        setBoards(Array.isArray(data) ? data : []);
        if (data.length > 0) setSelectedBoardId(data[0].id);
      } catch {}
    }
    loadBoards();
  }, []);

  // Cargar cards cuando cambia el board seleccionado
  useEffect(() => {
    async function loadCards() {
      if (!selectedBoardId) return;
      try {
        const res = await apiFetch(`/cards/?board_id=${selectedBoardId}`, { method: "GET" });
        const data = await res.json();
        setCards(Array.isArray(data) ? data : []);
        if (data.length > 0) setSelectedCardId(data[0].id);
      } catch {}
    }
    loadCards();
  }, [selectedBoardId]);

  async function handleFormSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);
    setFormSuccess(null);
    if (!formDate || !formHours || !selectedCardId) {
      setFormError("Debes indicar fecha, horas y tarjeta");
      return;
    }
    setFormLoading(true);
    try {
      await createWorklog({ card_id: selectedCardId, date: formDate, hours: formHours, note: formNote });
      setFormSuccess("Registro guardado");
      setFormDate(new Date().toISOString().split("T")[0]);
      setFormHours(0.25);
      setFormNote("");
      await load();
    } catch (e: any) {
      setFormError(e?.error || e?.detail || e?.message || "Error guardando registro");
    } finally {
      setFormLoading(false);
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%)",
        color: "#1e3a8a",
      }}
    >
      {/* HEADER con botón Volver */}
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
        <h1
          style={{
            color: "white",
            textShadow: "2px 2px 4px rgba(0, 0, 0, 0.6)",
            margin: 0,
            fontWeight: 800,
          }}
        >
          Mis horas
        </h1>

        <button
          onClick={() => navigate(-1)}
          style={{
            padding: "0.5rem 1rem",
            background: "linear-gradient(135deg, #0c4a6e 0%, #1e40af 100%)",
            border: "none",
            borderRadius: "0.5rem",
            color: "white",
            cursor: "pointer",
            fontWeight: 600,
            boxShadow: "0 4px 6px rgba(0, 0, 0, 0.2)",
          }}
        >
          ← Volver
        </button>
      </header>

      {/* CONTENIDO */}
      <div style={{ padding: "1.5rem" }}>
      {/* Formulario para registrar horas */}
      <form
        onSubmit={handleFormSubmit}
        style={{
          background: "rgba(255,255,255,0.95)",
          border: "1px solid #38bdf8",
          borderRadius: 12,
          padding: 16,
          marginBottom: 24,
          boxShadow: "0 4px 8px rgba(0,0,0,0.08)",
          display: "flex",
          gap: 12,
          alignItems: "end",
          flexWrap: "wrap",
        }}
      >
        <div>
          <label style={{ fontWeight: 700, fontSize: 13 }}>Board</label>
          <select
            value={selectedBoardId ?? ""}
            onChange={e => setSelectedBoardId(Number(e.target.value))}
            required
            style={{ padding: 8, borderRadius: 6, border: "1px solid #93c5fd" }}
          >
            {boards.map(b => (
              <option key={b.id} value={b.id}>{b.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label style={{ fontWeight: 700, fontSize: 13 }}>Tarjeta</label>
          <select
            value={selectedCardId ?? ""}
            onChange={e => setSelectedCardId(Number(e.target.value))}
            required
            style={{ padding: 8, borderRadius: 6, border: "1px solid #93c5fd", minWidth: 120 }}
          >
            {cards.map(c => (
              <option key={c.id} value={c.id}>{c.title}</option>
            ))}
          </select>
        </div>
        <div>
          <label style={{ fontWeight: 700, fontSize: 13 }}>Fecha</label>
          <input
            type="date"
            value={formDate}
            onChange={e => setFormDate(e.target.value)}
            required
            style={{ padding: 8, borderRadius: 6, border: "1px solid #93c5fd" }}
          />
        </div>
        <div>
          <label style={{ fontWeight: 700, fontSize: 13 }}>Horas</label>
          <input
            type="number"
            min={0.1}
            step={0.1}
            value={formHours}
            onChange={e => setFormHours(Number(e.target.value))}
            required
            style={{ padding: 8, borderRadius: 6, border: "1px solid #93c5fd", width: 80 }}
          />
        </div>
        <div>
          <label style={{ fontWeight: 700, fontSize: 13 }}>Nota</label>
          <input
            type="text"
            value={formNote}
            onChange={e => setFormNote(e.target.value)}
            placeholder="(opcional)"
            style={{ padding: 8, borderRadius: 6, border: "1px solid #93c5fd", minWidth: 180 }}
          />
        </div>
        <button
          type="submit"
          disabled={formLoading}
          style={{
            padding: "8px 16px",
            borderRadius: 6,
            border: "none",
            background: "linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)",
            color: "white",
            fontWeight: 700,
            boxShadow: "0 4px 6px rgba(0,0,0,0.13)",
            cursor: "pointer",
          }}
        >
          {formLoading ? "Guardando…" : "Registrar horas"}
        </button>
        {formError && <div style={{ color: "#b91c1c", fontWeight: 700 }}>{formError}</div>}
        {formSuccess && <div style={{ color: "#15803d", fontWeight: 700 }}>{formSuccess}</div>}
      </form>

      {/* Card: Filtro y total */}
      <div
        style={{
          background: "rgba(255,255,255,0.8)",
          border: "1px solid #93c5fd",
          borderRadius: 12,
          padding: 16,
          boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
          display: "flex",
          gap: 12,
          alignItems: "end",
          flexWrap: "wrap",
        }}
      >
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 800 }}>
            Semana (ISO)
          </label>
          <input
            value={week}
            onChange={(e) => setWeek(e.target.value)}
            placeholder="2026-03"
            style={{
              padding: 8,
              borderRadius: 6,
              border: "1px solid #93c5fd",
              background: "rgba(255,255,255,0.95)",
              color: "#1e3a8a",
              minWidth: 140,
            }}
          />
          <div style={{ fontSize: 12, opacity: 0.75 }}>Ej: 2026-03</div>
        </div>

        <button
          onClick={load}
          disabled={loading}
          style={{
            padding: "8px 12px",
            borderRadius: 6,
            border: "none",
            background: "linear-gradient(135deg, #0c4a6e 0%, #1e40af 100%)",
            color: "white",
            fontWeight: 600,
            boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
            cursor: "pointer",
          }}
        >
          {loading ? "Cargando…" : "Actualizar"}
        </button>

        <div style={{ marginLeft: "auto", fontWeight: 900 }}>
          Total semana: {totalWeek.toFixed(2)} h
        </div>
      </div>

      {error && (
        <div style={{ marginTop: 12, color: "#7f1d1d", fontWeight: 700 }}>
          {error}
        </div>
      )}

      {/* Totales por día */}
      <div style={{ marginTop: 24 }}>
        <h3 style={{ marginBottom: 8, fontWeight: 800 }}>Totales por día</h3>

        {totalsByDay.length === 0 ? (
          <div style={{ opacity: 0.8 }}>(Sin horas registradas esta semana)</div>
        ) : (
          <div style={{ display: "grid", gap: 8, maxWidth: 520 }}>
            {totalsByDay.map(([day, h]) => (
              <div
                key={day}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  padding: 10,
                  borderRadius: 10,
                  background: "rgba(255,255,255,0.9)",
                  border: "1px solid #93c5fd",
                  boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
                }}
              >
                <div style={{ fontWeight: 800 }}>{day}</div>
                <div style={{ fontWeight: 900 }}>{h.toFixed(2)} h</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Registros */}
      <div style={{ marginTop: 24 }}>
        <h3 style={{ marginBottom: 8, fontWeight: 800 }}>Registros</h3>

        {items.length === 0 ? null : (
          <div style={{ display: "grid", gap: 8 }}>
            {items.map((w) => (
              <div
                key={w.id}
                style={{
                  padding: 10,
                  borderRadius: 10,
                  background: "rgba(255,255,255,0.85)",
                  border: "1px solid #93c5fd",
                  boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
                }}
              >
                <div style={{ fontWeight: 900 }}>
                  {w.date} — {hoursToNumber(w.hours).toFixed(2)} h (card_id: {w.card_id})
                </div>
                {w.note && <div style={{ opacity: 0.85, marginTop: 6 }}>{w.note}</div>}
              </div>
            ))}
          </div>
        )}
      </div>
      </div> {/* Cierre del div de contenido */}
    </div>
  );
}