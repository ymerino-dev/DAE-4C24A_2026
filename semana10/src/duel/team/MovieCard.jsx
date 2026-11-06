import Showtimes from "./Showtimes.jsx";
import Synopsis from "./Synopsis.jsx";
import Button from "./Button.jsx";

export default function MovieCard({ movie, onToggleFavorite, isFavorite = false }) {
  const handleToggle = () => {
    if (onToggleFavorite) onToggleFavorite(movie.id);
  };

  return (
    <article className="movie-card" id={`horarios-${movie.id}`}>
      <img src={movie.image} alt={movie.title} loading="lazy" />
      <div className="movie-card-content">
        <p className="classification">{movie.classification}</p>
        <h3>{movie.title}</h3>
        <p className="rating" aria-label={`Valoración ${movie.rating} de 5`}>★ {movie.rating}</p>
        <Synopsis text={movie.synopsis} />
        <h4>Horarios</h4>
        <Showtimes times={movie.showtimes} />
        <Button
          variant={isFavorite ? "danger" : "secondary"}
          onClick={handleToggle}
          className="favorite-button"
        >
          {isFavorite ? "Quitar de favoritas" : "Marcar favorita"}
        </Button>
        <p className="favorite-state">{isFavorite ? "En favoritas" : "No está en favoritas"}</p>
      </div>
    </article>
  );
}
