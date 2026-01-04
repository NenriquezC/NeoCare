/**
 * @file router.tsx
 * Define las rutas principales de la aplicación React, asociando cada ruta a su componente.
 * Integra protección de rutas para evitar acceso no autenticado y redirecciona rutas desconocidas al login.
 */
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Boards from "./pages/Boards";
import MyHours from "./pages/MyHours"; // SEMANA 4

import ProtectedRoute from "./components/ProtectedRoute";
import AppLayout from "./components/layout/AppLayout";
import ReportPage from "./pages/ReportPage"; //semana 5

/**
 * AppRouter
 *
 * Componente que gestiona el enrutamiento de la aplicación:
 * - Todas las rutas se renderizan dentro del layout central tipo Django
 * - "/login": Vista de autentificación.
 * - "/boards": Vista principal protegida; requiere autenticación.
 * - "/my-hours": Vista protegida de horas por semana.
 * - "*": Redirección de cualquier ruta desconocida al login.
 *
 * @returns {JSX.Element} Árbol de rutas de la aplicación.
 */
export const AppRouter: React.FC = () => {
  return (
    <Routes>
      <Route
        path="/login"
        element={
          <AppLayout>
            <Login />
          </AppLayout>
        }
      />

      <Route
        path="/boards"
        element={
          <ProtectedRoute>
            <AppLayout>
              <Boards />
            </AppLayout>
          </ProtectedRoute>
        }
      />

      {/* NUEVA RUTA SEMANA 4 */}
      <Route
        path="/my-hours"
        element={
          <ProtectedRoute>
            <AppLayout>
              <MyHours />
            </AppLayout>
          </ProtectedRoute>
        }
      />

      {/* NUEVA RUTA SEMANA 5 */}
      <Route
        path="/report/:boardId"
        element={
          <ProtectedRoute>
            <AppLayout>
              <ReportPage />
            </AppLayout>
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};