import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const getMovies = () => apiClient.get('/movies/');

export const createMovie = (movieData) => apiClient.post('/movies/', movieData);

export const deleteMovie = (id) => apiClient.delete(`/movies/${id}/`);
