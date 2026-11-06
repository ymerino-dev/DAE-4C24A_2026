import MovieCard from "./MovieCard.jsx";

export default function MovieList({
  movies,
  searchText = "",
  onToggleFavorite,
  favorites = [],
}) {
  const filtered = movies.filter((movie) =>
    !searchText
      ? true
      : movie.title.toLowerCase().includes(searchText.toLowerCase())
  );

  if (filtered.length === 0) {
    return (
      <div className="empty-state">
        <p>No se encontraron películas que coincidan con tu búsqueda.</p>
      </div>
    );
  }

  return (
    <ul className="movie-list">
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
