// src/pages/Boards.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";

const Boards: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  // Modal / form para crear nueva tarjeta
  const [showModal, setShowModal] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", due_date: "" });
  const [formError, setFormError] = useState<string | null>(null);

  function openCreate() {
    setForm({ title: "", description: "", due_date: "" });
    setFormError(null);
    setShowModal(true);
  }

  function closeModal() {
    setShowModal(false);
    setFormError(null);
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);
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
        list_id: 1, // "Por hacer"
        board_id: 1,
      };

      const res = await apiFetch("/cards", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(txt || `Error al crear tarjeta (status ${res.status})`);
      }

      closeModal();
      // opcional: podrías mostrar una notificación o refrescar datos
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Error creando tarjeta");
    } finally {
      setSaving(false);
    }
  }

  const columns = ["Por hacer", "En curso", "Hecho"];

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
            onClick={openCreate}
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

      {/* Contenido */}
      <main
        style={{
          flex: 1,
          display: "flex",
          gap: "1rem",
          padding: "1.5rem",
        }}
      >
        {columns.map((col) => (
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
            <h2 style={{ marginBottom: "0.75rem" }}>{col}</h2>
            <div
              style={{
                flex: 1,
                border: "2px dashed #1e293b",
                borderRadius: "0.75rem",
                padding: "0.75rem",
                fontSize: "0.9rem",
                color: "#94a3b8",
              }}
            >
              (Sin tarjetas todavía)
            </div>
          </div>
        ))}
      </main>

      {/* Modal para crear tarjeta */}
      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50">
          <div style={{ background: "#0b1220", color: "white", width: 540, borderRadius: 8, padding: 20 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
              <h3 style={{ margin: 0 }}>Nueva tarjeta (Por hacer)</h3>
              <button onClick={closeModal} style={{ background: "transparent", border: "none", color: "white", fontSize: 18 }}>✕</button>
            </div>

            <form onSubmit={handleCreate}>
              <label style={{ display: "block", marginBottom: 6 }}>Título</label>
              <input
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                style={{ width: "100%", padding: 8, marginBottom: 10, borderRadius: 6, border: "1px solid #334155", background: "#071025", color: "white" }}
              />

              <label style={{ display: "block", marginBottom: 6 }}>Descripción</label>
              <textarea
                rows={3}
                value={form.description}
                onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                style={{ width: "100%", padding: 8, marginBottom: 10, borderRadius: 6, border: "1px solid #334155", background: "#071025", color: "white" }}
              />

              <label style={{ display: "block", marginBottom: 6 }}>Fecha límite</label>
              <input
                type="date"
                value={form.due_date}
                onChange={(e) => setForm((f) => ({ ...f, due_date: e.target.value }))}
                style={{ padding: 8, marginBottom: 12, borderRadius: 6, border: "1px solid #334155", background: "#071025", color: "white" }}
              />

              {formError && <div style={{ color: "#fecaca", marginBottom: 8 }}>{formError}</div>}

              <div style={{ display: "flex", gap: 8 }}>
                <button type="submit" disabled={saving} style={{ padding: "0.5rem 1rem", background: "#10b981", border: "none", borderRadius: 6, color: "white" }}>
                  {saving ? "Creando…" : "Crear tarjeta"}
                </button>
                <button type="button" onClick={closeModal} style={{ padding: "0.5rem 1rem", background: "#334155", border: "none", borderRadius: 6, color: "white" }}>
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Boards;
