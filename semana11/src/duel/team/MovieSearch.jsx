// Controlled search field; the shared filter state is owned by App.
export default function MovieSearch({ value, onSearch }) {

  return (
    <div className="search">
      <label htmlFor="movie-search" className="label sr-only">
        Buscar película
      </label>
      <input
        id="movie-search"
        type="search"
        className="input search-input"
        value={value}
        onChange={(event) => onSearch(event.target.value)}
        placeholder="Buscar por título…"
        aria-label="Buscar película"
      />
    </div>
  );
}
