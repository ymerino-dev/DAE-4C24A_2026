import './MovieCard.css'

function MovieCard({ movie }) {
  return (
    <article className="movie-card">
      <img
        className="movie-card__image"
        src={movie.image}
        alt={`${movie.title} poster`}
        loading="lazy"
      />

      <div className="movie-card__body">
        <h3 className="movie-card__title">{movie.title}</h3>

        <div className="movie-card__meta">
          <span className="movie-card__classification">
            {movie.classification}
          </span>
          <span className="movie-card__rating">{movie.rating.toFixed(1)} / 10</span>
        </div>

        <p className="movie-card__synopsis">{movie.synopsis}</p>

        <div className="movie-card__showtimes">
          <p className="movie-card__showtimes-label">Showtimes</p>
          <ul className="movie-card__showtime-list">
            {movie.showtimes.map((showtime) => (
              <li className="movie-card__showtime" key={showtime}>
                {showtime}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </article>
  )
}

export default MovieCard
