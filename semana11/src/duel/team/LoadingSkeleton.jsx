export default function LoadingSkeleton() {
  return (
    <div className="premiere-grid" aria-label="Cargando estrenos" aria-busy="true">
      {[1, 2, 3, 4].map((item) => (
        <div className="skeleton-card" key={item}>
          <div className="skeleton-poster" />
          <div className="skeleton-line" />
          <div className="skeleton-line skeleton-line--short" />
        </div>
      ))}
      <p className="sr-only" role="status">Cargando próximos estrenos…</p>
    </div>
  );
}
