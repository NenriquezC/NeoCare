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

    if (! email || !password) {
      setError("Introduce email y contraseña");
      return;
    }

    setLoading(true);
    try {
      console.log("🔄 Intentando login con:", { email, password: "***" });
      console.log("🔄 URL backend:", "http://127.0.0.1:8000/auth/login");
      
      const data = await loginRequest({ email, password });
      
      console.log("✅ Login exitoso:", data);
      localStorage.setItem("token", data. access_token);
      navigate("/boards");
    } catch (err) {
      console.error("❌ Error completo:", err);
      
      if (err instanceof Error) {
        console.error("❌ Mensaje:", err.message);
        setError(`Error: ${err.message}`);
      } else {
        setError("No se ha podido iniciar sesión (API no disponible o credenciales incorrectas)");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background:
          "linear-gradient(135deg, #020617 0%, #0b2a5a 45%, #1e3a8a 100%)",
        color: "white",
      }}
      >

      <div
        style={{
          background: "linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%)",
          padding: "3rem",
          borderRadius: "1rem",
          width: "420px",
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.2)",
          border: "1px solid rgba(255, 255, 255, 0.3)",
        }}
      >
        <h1
          style={{
            fontSize: "2.5rem",
            marginBottom: "2rem",
            fontWeight: "700",
            textShadow: "2px 2px 4px rgba(0, 0, 0, 0.6)",
            color: "white",
          }}
        >
          NeoCare
        </h1>

        <form onSubmit={handleSubmit}>
          <label style={{ display: "block", marginBottom: "0.5rem", color: "#1e40af", fontWeight: "600", textShadow: "1px 1px 2px rgba(0, 0, 0, 0.3)" }}>
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
              border: "1px solid rgba(30, 64, 175, 0.3)",
              marginBottom: "1.25rem",
              background: "rgba(255, 255, 255, 0.7)",
              color: "#1e3a8a",
            }}
          />

          <label style={{ display: "block", marginBottom: "0.5rem", color: "#1e40af", fontWeight:  "600", textShadow:  "1px 1px 2px rgba(0, 0, 0, 0.3)" }}>
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
              border: "1px solid rgba(30, 64, 175, 0.3)",
              marginBottom: "1.5rem",
              background: "rgba(255, 255, 255, 0.7)",
              color: "#1e3a8a",
            }}
          />

          {error && (
            <div
              style={{
                marginBottom: "1rem",
                color: "white",
                background: "rgba(127, 29, 29, 0.7)",
                padding: "0.5rem 0.75rem",
                borderRadius: "0.5rem",
                fontSize: "0.9rem",
                textShadow: "1px 1px 2px rgba(0, 0, 0, 0.5)",
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
              background: loading ? "linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)" : "linear-gradient(135deg, #0c4a6e 0%, #1e40af 100%)",
              borderRadius: "0.75rem",
              border: "none",
              color: "white",
              fontWeight: "600",
              cursor: loading ? "default" : "pointer",
              fontSize: "1rem",
              textShadow: "1px 1px 2px rgba(0, 0, 0, 0.5)",
              boxShadow: "0 4px 6px rgba(0, 0, 0, 0.2)",
            }}
          >
            {loading ?  "Iniciando sesión..." :  "Iniciar sesión"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
