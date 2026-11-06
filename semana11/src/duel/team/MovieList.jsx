import MovieCard from "./MovieCard.jsx";
import useWindowSize from "../../hooks/useWindowSize.js";

export default function MovieList({
  movies,
  searchText = "",
  onToggleFavorite,
  favorites = [],
}) {
  const width = useWindowSize();
  const columns = width < 560 ? 1 : width < 900 ? 2 : width < 1200 ? 3 : 4;
  const normalizedSearch = searchText.trim().toLowerCase();
  const filtered = movies.filter((movie) =>
    !searchText
      ? true
      : movie.title.toLowerCase().includes(normalizedSearch)
  );

  if (filtered.length === 0) {
    return (
      <div className="empty-state">
        <p>No se encontraron películas que coincidan con tu búsqueda.</p>
      </div>
    );
  }

  return (
    <ul className="movie-list" style={{ "--movie-columns": columns }}>
      {filtered.map((movie) => (
        <li key={movie.id}>
          <MovieCard
            movie={movie}
            onToggleFavorite={onToggleFavorite}
            isFavorite={favorites.includes(movie.id)}
          />
        </li>
      ))}
    </ul>
  );
}
