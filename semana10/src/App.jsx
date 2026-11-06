import { useState, useEffect } from "react";
import { Header, Hero, MovieList, Footer, MovieSearch } from "@cartelera/index.jsx";
import { contact, links, movies } from "./data/movies.js";

const FAV_KEY = "cine-favoritas";

export default function App() {
  const featuredMovie = movies[0];

  // Paso 4: estado de películas favoritas con useState.
  const [favorites, setFavorites] = useState([]);
  // Paso 9: texto del buscador.
  const [searchText, setSearchText] = useState("");

  // Paso 10: recuperar favoritas del almacenamiento del navegador al cargar.
  useEffect(() => {
    try {
      const saved = localStorage.getItem(FAV_KEY);
      if (saved) setFavorites(JSON.parse(saved));
    } catch {}
  }, []);

  // Paso 10: guardar favoritas en el almacenamiento del navegador al cambiar.
  useEffect(() => {
    try {
      localStorage.setItem(FAV_KEY, JSON.stringify(favorites));
    } catch {}
  }, [favorites]);

  // Paso 4: función que agrega o quita una película de la lista de favoritas.
  const toggleFavorite = (movieId) => {
    setFavorites((prev) =>
      prev.includes(movieId)
        ? prev.filter((id) => id !== movieId)
        : [...prev, movieId]
    );
  };

  const isFavorite = (movieId) => favorites.includes(movie.id);

  // Paso 9: manejador del buscador (recibe el texto ya debounceado de MovieSearch).
  const handleSearch = (text) => {
    setSearchText(text);
  };

  return (
    <>
      <Header name="Cine Tecsup" links={links} />
      <main>
        <Hero movie={featuredMovie} />
        <section id="cartelera" aria-labelledby="movies-title">
          <div className="section-heading">
            <p className="eyebrow">EN PANTALLA</p>
            <h2 id="movies-title">Nuestra cartelera</h2>
            <p>Elige tu próxima historia y encuentra el horario ideal.</p>
          </div>
          {/* Paso 9: buscador integrado en el banner con su llamada a la acción. */}
          <MovieSearch onSearch={handleSearch} />
          <MovieList
            movies={movies}
            searchText={searchText}
            onToggleFavorite={toggleFavorite}
            favorites={favorites}
          />
        </section>
        <section id="proximamente" className="coming-soon">
          <p className="eyebrow">PRÓXIMAMENTE</p>
          <p>Nuevas historias llegan muy pronto a nuestras salas.</p>
        </section>
      </main>
      <Footer contact={contact} />
    </>
  );
}
