import MovieCard from '../MovieCard/MovieCard.jsx'
import './MovieList.css'

function MovieList({ movies }) {
  return (
    <section className="movie-list" id="movies" aria-labelledby="movie-list-title">
      <h2 className="movie-list__title" id="movie-list-title">
        Now showing
      </h2>

      <div className="movie-list__grid">
        {movies.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </section>
  )
}

export default MovieList
