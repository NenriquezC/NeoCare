
/**
 * @file index.tsx
 * Punto de entrada principal de la aplicación React.
 * Renderiza el árbol de componentes, habilita enrutamiento y modo estricto.
 */
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AppRouter } from "./router";
import "./index.css";

/**
 * Renderiza la aplicación React en el elemento con id 'root'.
 * Incluye soporte para rutas mediante react-router y habilita React.StrictMode
 * para mejores advertencias de desarrollo.
 */
ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  </React.StrictMode>
);
