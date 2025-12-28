
/**
 * @file router.tsx
 * Define las rutas principales de la aplicación React, asociando cada ruta a su componente.
 * Integra protección de rutas para evitar acceso no autenticado y redirecciona rutas desconocidas al login.
 */
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Boards from "./pages/Boards";
import ProtectedRoute from "./components/ProtectedRoute";
import MyHours from "./pages/MyHours"; //SEMANA 4

/**
 * AppRouter
 *
 * Componente que gestiona el enrutamiento de la aplicación:
 * - "/login": Vista de autentificación.
 * - "/boards": Vista principal protegida; requiere autenticación.
 * - "*": Redirección de cualquier ruta desconocida al login.
 *
 * @returns {JSX.Element} Árbol de rutas de la aplicación.
 */
export const AppRouter: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/boards"
        element={
          <ProtectedRoute>
            <Boards />
          </ProtectedRoute>
        }
      />

      {/*NUEVA RUTA SEMANA 4 */}
      <Route
        path="/my-hours"
        element={
          <ProtectedRoute>
            <MyHours />
          </ProtectedRoute>
        }
      />  

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};
