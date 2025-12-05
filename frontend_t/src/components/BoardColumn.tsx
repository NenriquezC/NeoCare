// src/pages/Boards.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import { BoardColumn } from "../components/BoardColumn";

export const Boards: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

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
          <BoardColumn key={col} title={col} />
        ))}
      </main>
    </div>
  );
};
