// Componente Spinner reutilizable
export function Spinner({ size = 'md', className = '' }: { size?: 'sm' | 'md' | 'lg', className?: string }) {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4'
  };

  return (
    <div className={`inline-block animate-spin rounded-full border-solid border-blue-600 border-t-transparent ${sizeClasses[size]} ${className}`}></div>
  );
}

// Loading Overlay para operaciones en progreso
export function LoadingOverlay({ message = 'Cargando...' }: { message?: string }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 flex flex-col items-center gap-4">
        <Spinner size="lg" />
        <p className="text-gray-700 font-medium">{message}</p>
      </div>
    </div>
  );
}

// Loading para páginas completas
export function PageLoader() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <Spinner size="lg" className="mx-auto mb-4" />
        <p className="text-gray-600">Cargando datos...</p>
      </div>
    </div>
  );
}

// Button con estado de loading
interface LoadingButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
  children: React.ReactNode;
}

export function LoadingButton({ loading, children, disabled, className = '', ...props }: LoadingButtonProps) {
  return (
    <button
      disabled={loading || disabled}
      className={`inline-flex items-center justify-center gap-2 ${loading ? 'opacity-70 cursor-not-allowed' : ''} ${className}`}
      {...props}
    >
      {loading && <Spinner size="sm" />}
      {children}
    </button>
  );
}
