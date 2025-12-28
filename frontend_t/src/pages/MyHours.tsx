// src/pages/MyHours.tsx
import { useEffect, useMemo, useState } from "react";
import { hoursToNumber, listMyWorklogsByWeek, type Worklog } from "../lib/worklogs";

function getISOWeekString(d = new Date()): string {
  const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  const dayNum = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil((((date.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  const year = date.getUTCFullYear();
  return `${year}-W${String(weekNo).padStart(2, "0")}`;
}

export default function MyHours() {
  const [week, setWeek] = useState(getISOWeekString());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [items, setItems] = useState<Worklog[]>([]);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await listMyWorklogsByWeek(week);

      
    // 👇 el backend devuelve un objeto con `entries`
        setItems(Array.isArray(data.entries) ? data.entries : []);
        
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error cargando mis horas");
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

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "1.5rem",
        background: "linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%)",
        color: "#1e3a8a",
      }}
    >
      <h2
        style={{
          marginTop: 0,
          fontWeight: 800,
          color: "white",
          textShadow: "2px 2px 4px rgba(0,0,0,0.4)",
        }}
      >
        Mis horas
      </h2>

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
            placeholder="2025-W52"
            style={{
              padding: 8,
              borderRadius: 6,
              border: "1px solid #93c5fd",
              background: "rgba(255,255,255,0.95)",
              color: "#1e3a8a",
              minWidth: 140,
            }}
          />
          <div style={{ fontSize: 12, opacity: 0.75 }}>Ej: 2025-W52</div>
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
    </div>
  );
}