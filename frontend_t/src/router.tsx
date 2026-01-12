/**
 * @file router.tsx
 * Define las rutas principales de la aplicación React, asociando cada ruta a su componente.
 * Integra protección de rutas para evitar acceso no autenticado y redirecciona rutas desconocidas a la home.
 */
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";

// ✅ IMPORT EXPLÍCITO AL ARCHIVO EXACTO (evita que tome otro Boards por error)
import Boards from "./pages/Boards.tsx";

import ProtectedRoute from "./components/ProtectedRoute";
import MyHours from "./pages/MyHours";
import KanbanBoard from "./pages/KanbanBoard";
import ReportPage from "./pages/ReportPage";

/**
 * AppRouter
 *
 * Rutas:
 * - "/": Landing (Home)
 * - "/login": Login
 * - "/boards": Vista protegida
 * - "/my-hours": Vista protegida
 * - "*": Redirección a Home
 */
export const AppRouter: React.FC = () => {
  console.log("✅ ROUTER CARGADO (AppRouter)");
  return (
    <Routes>
      {/* Página inicial */}
      <Route path="/" element={<Home />} />

      {/* Login */}
      <Route path="/login" element={<Login />} />

      {/* Protegidas */}
      <Route
        path="/boards"
        element={
          <ProtectedRoute>
            <Boards />
          </ProtectedRoute>
        }
      />

      <Route
        path="/kanban/:boardId"
        element={
          <ProtectedRoute>
            <KanbanBoard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/my-hours"
        element={
          <ProtectedRoute>
            <MyHours />
          </ProtectedRoute>
        }
      />

      <Route
        path="/reporte"
        element={
          <ProtectedRoute>
            <ReportPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/report/:boardId"
        element={
          <ProtectedRoute>
            <ReportPage />
          </ProtectedRoute>
        }
      />

      {/* Cualquier otra ruta -> Home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};
