// src/pages/Home.tsx
import React from "react";
import { useNavigate } from "react-router-dom";

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        background:
          "linear-gradient(135deg, #020617 0%, #0b2a5a 45%, #1e3a8a 100%)", // azul oscuro degradado
        color: "white",
      }}
    >
      <div style={{ maxWidth: "900px", width: "100%", textAlign: "center" }}>
        <h1
          style={{
            fontSize: "clamp(3rem, 7vw, 5.5rem)",
            margin: 0,
            fontWeight: 800,
            letterSpacing: "-0.02em",
          }}
        >
          NeoCare
        </h1>

        <p
          style={{
            marginTop: "1rem",
            fontSize: "clamp(1.1rem, 2vw, 1.5rem)",
            opacity: 0.9,
            lineHeight: 1.4,
          }}
        >
          Bienvenido a NeoCare, tu plataforma de trabajo.
        </p>

        <div
          style={{
            marginTop: "2.5rem",
            display: "flex",
            justifyContent: "center",
            gap: "1rem",
            flexWrap: "wrap",
          }}
        >
          <button
            onClick={() => navigate("/login")}
            style={{
              padding: "0.9rem 1.2rem",
              borderRadius: "999px",
              border: "1px solid rgba(255,255,255,0.25)",
              background: "rgba(255,255,255,0.12)",
              color: "white",
              fontWeight: 700,
              cursor: "pointer",
              backdropFilter: "blur(10px)",
            }}
          >
            Iniciar sesión
          </button>

          {/* Si luego quieres “Registrarse”, lo dejamos preparado */}
          <button
            onClick={() => navigate("/login")}
            style={{
              padding: "0.9rem 1.2rem",
              borderRadius: "999px",
              border: "1px solid rgba(255,255,255,0.18)",
              background: "transparent",
              color: "white",
              fontWeight: 700,
              cursor: "pointer",
            }}
          >
            Acceder
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
