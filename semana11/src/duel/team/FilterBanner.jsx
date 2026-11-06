import Button from "./Button.jsx";

export default function FilterBanner({ searchText, onClear }) {
  return (
    <aside className="filter-banner" aria-label="Filtro de cartelera">
      <div>
        <p className="eyebrow">ENCUENTRA TU PELÍCULA</p>
        <p>{searchText ? `Filtro activo: “${searchText}”` : "Explora la cartelera y los próximos estrenos."}</p>
      </div>
      <Button variant="outline" onClick={onClear} disabled={!searchText}>
        Limpiar filtro
      </Button>
    </aside>
  );
}
