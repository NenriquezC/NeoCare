// src/pages/Login.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginRequest } from "../lib/auth";

const Login: React.FC = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email || !password) {
      setError("Introduce email y contraseña");
      return;
    }

    setLoading(true);
    try {
      // 🔹 Llamada REAL a FastAPI
      const data = await loginRequest({ email, password });

      // Guardamos el token devuelto por el backend
      localStorage.setItem("token", data.access_token);

      // Navegamos al tablero
      navigate("/boards");
    } catch (err) {
      console.error(err);
      setError(
        "No se ha podido iniciar sesión (API no disponible o credenciales incorrectas)"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#020617",
        color: "white",
      }}
    >
      <div
        style={{
          background: "#020617",
          padding: "3rem",
          borderRadius: "1rem",
          width: "420px",
          boxShadow: "0 10px 30px rgba(15,23,42,0.8)",
          border: "1px solid #1e293b",
        }}
      >
        <h1
          style={{
            fontSize: "2.5rem",
            marginBottom: "2rem",
            fontWeight: "700",
          }}
        >
          NeoCare – Login
        </h1>

        <form onSubmit={handleSubmit}>
          <label style={{ display: "block", marginBottom: "0.5rem" }}>
            Email
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
              width: "100%",
              padding: "0.75rem 1rem",
              borderRadius: "0.5rem",
              border: "1px solid #1f2937",
              marginBottom: "1.25rem",
              background: "#111827",
              color: "white",
            }}
          />

          <label style={{ display: "block", marginBottom: "0.5rem" }}>
            Contraseña
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: "100%",
              padding: "0.75rem 1rem",
              borderRadius: "0.5rem",
              border: "1px solid #1f2937",
              marginBottom: "1.5rem",
              background: "#111827",
              color: "white",
            }}
          />

          {error && (
            <div
              style={{
                marginBottom: "1rem",
                color: "#fecaca",
                background: "#7f1d1d",
                padding: "0.5rem 0.75rem",
                borderRadius: "0.5rem",
                fontSize: "0.9rem",
              }}
            >
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "0.75rem 1rem",
              background: loading ? "#3b82f6aa" : "#2563eb",
              borderRadius: "0.75rem",
              border: "none",
              color: "white",
              fontWeight: "600",
              cursor: loading ? "default" : "pointer",
              fontSize: "1rem",
            }}
          >
            {loading ? "Iniciando sesión..." : "Iniciar sesión"}
          </button>
        </form>
      </div>
    </div>
  );
};

// 👇 Esto es lo que faltaba
export default Login;
