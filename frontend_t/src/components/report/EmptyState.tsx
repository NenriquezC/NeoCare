/**
 * Componente EmptyState para mostrar cuando no hay datos en el informe semanal
 */

interface EmptyStateProps {
  message: string;
  icon?: string;
}

export default function EmptyState({ message, icon = "📭" }: EmptyStateProps) {
  return (
    <div
      style={{
        padding: "3rem 2rem",
        textAlign: "center",
        background: "rgba(255, 255, 255, 0.9)",
        borderRadius: "12px",
        border: "2px dashed #93c5fd",
        color: "#1e40af",
      }}
    >
      <div style={{ fontSize: "3rem", marginBottom: "1rem" }}>{icon}</div>
      <p style={{ fontSize: "1.125rem", fontWeight: 600, marginBottom: "0.5rem" }}>
        {message}
      </p>
      <p style={{ fontSize: "0.875rem", color: "#64748b" }}>
        Intenta seleccionar otra semana o verifica que haya actividad registrada.
      </p>
    </div>
  );
}

