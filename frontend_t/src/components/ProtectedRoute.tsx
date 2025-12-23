/**
 * @file ProtectedRoute.tsx
 * Componente para proteger rutas: sólo usuarios autenticados pueden acceder.
 * Redirige al login si no hay token presente en el almacenamiento local.
 */
import React from "react";
import { Navigate } from "react-router-dom";

/**
 * Props para ProtectedRoute.
 * @property children - Componente hijo que se renderiza si el usuario está autenticado.
 */
interface ProtectedRouteProps {
  children: React.ReactElement;
}

/**
 * ProtectedRoute
 *
 * Componente de alto nivel que verifica la existencia de un token de autenticación.
 * Si el token no está presente, redirige al usuario a la página de login.
 * Si el token está presente, renderiza los componentes hijos proporcionados.
 *
 * @param {ProtectedRouteProps} props - Propiedades: children a proteger.
 * @returns {JSX.Element} El componente hijo si está autenticado, o <Navigate /> si no lo está.
 */
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
