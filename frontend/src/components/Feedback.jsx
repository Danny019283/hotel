export function Alert({ type = "error", children }) {
  if (!children) return null;
  return <div className={`alert alert-${type}`}>{children}</div>;
}

export function LoadingState() {
  return (
    <div className="loading-state">
      <span className="spinner" />
      Cargando informacion...
    </div>
  );
}
