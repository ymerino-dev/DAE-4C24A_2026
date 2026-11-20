import { useCallback, useEffect, useState } from 'react';

import { deleteMovie, getMovies } from '../../services/apiClient';
import './MovieList.css';

const SKELETON_ROWS = [1, 2, 3, 4, 5];

function MovieList() {
  const [movies, setMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMovieData = useCallback(async () => {
    const response = await getMovies();
    return response.data;
  }, []);

  const loadMovies = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      setMovies(await fetchMovieData());
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsLoading(false);
    }
  }, [fetchMovieData]);

  useEffect(() => {
    fetchMovieData()
      .then((movieData) => setMovies(movieData))
      .catch((requestError) => setError(requestError))
      .finally(() => setIsLoading(false));
  }, [fetchMovieData]);

  const handleDelete = async (id) => {
    try {
      await deleteMovie(id);
      setMovies((currentMovies) =>
        currentMovies.filter((movie) => movie.id !== id),
      );
    } catch (requestError) {
      setError(requestError);
    }
  };

  if (isLoading) {
    return (
      <section className="movie-list" aria-busy="true">
        <div className="movie-list-header">
          <h1>Movies</h1>
        </div>
        <p className="loading-text">Loading movies from server...</p>
        <table className="movie-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Director</th>
              <th>Year</th>
              <th>Genre</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {SKELETON_ROWS.map((rowId) => (
              <tr className="skeleton-row" key={rowId}>
                <td><span className="skeleton-bar short" /></td>
                <td><span className="skeleton-bar" /></td>
                <td><span className="skeleton-bar" /></td>
                <td><span className="skeleton-bar short" /></td>
                <td><span className="skeleton-bar" /></td>
                <td><span className="skeleton-bar short" /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    );
  }

  if (error !== null) {
    const errorDetails = error.response
      ? `${error.message} - ${JSON.stringify(error.response.data)}`
      : error.message;

    return (
      <section className="error-box" role="alert">
        <h2>Unable to load movies</h2>
        <p className="error-details">{errorDetails}</p>
        <button className="retry-button" type="button" onClick={loadMovies}>
          Retry
        </button>
      </section>
    );
  }

  return (
    <section className="movie-list">
      <div className="movie-list-header">
        <h1>Movies</h1>
        <span className="movie-count">{movies.length} movies</span>
      </div>

      {movies.length === 0 ? (
        <p className="empty-message">No movies found.</p>
      ) : (
        <table className="movie-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Director</th>
              <th>Year</th>
              <th>Genre</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {movies.map((movie) => (
              <tr key={movie.id}>
                <td>{movie.id}</td>
                <td>{movie.title}</td>
                <td>{movie.director}</td>
                <td>{movie.release_year}</td>
                <td>{movie.genre}</td>
                <td>
                  <button
                    className="delete-button"
                    type="button"
                    onClick={() => handleDelete(movie.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

export default MovieList;
