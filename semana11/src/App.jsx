import { useEffect, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {
  Header,
  Hero,
  MovieList,
  Footer,
  MovieSearch,
  PremiereSection,
  FilterBanner,
} from "@cartelera/index.jsx";
import { contact, links, movies } from "./data/movies.js";
import { adaptMovie } from "./adapters/movieAdapter.js";
import useDebounce from "./hooks/useDebounce.js";

const FAV_KEY = "cine-favoritas";
const adaptedMovies = movies.map(adaptMovie);

export default function App() {
  const [favorites, setFavorites] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem(FAV_KEY) || "[]");
    } catch {
      return [];
    }
  });
  const [searchText, setSearchText] = useState("");
  const debouncedSearch = useDebounce(searchText, 400);

  useEffect(() => {
    try {
      localStorage.setItem(FAV_KEY, JSON.stringify(favorites));
    } catch {
      // The page remains usable when browser storage is unavailable.
    }
  }, [favorites]);

  const toggleFavorite = (movieId) => {
    const movie = adaptedMovies.find((item) => item.id === movieId);
    const wasFavorite = favorites.includes(movieId);
    setFavorites((current) => (
      current.includes(movieId)
        ? current.filter((id) => id !== movieId)
        : [...current, movieId]
    ));
    toast(wasFavorite ? `${movie.title} se quitó de favoritas.` : `${movie.title} se agregó a favoritas.`, {
      type: wasFavorite ? "info" : "success",
      position: "bottom-right",
      autoClose: 2500,
    });
  };

  return (
    <>
      <Header name="Cine Tecsup" links={links} favoriteCount={favorites.length}>
        <MovieSearch value={searchText} onSearch={setSearchText} />
      </Header>
      <main>
        <Hero movie={adaptedMovies[0]} />
        <FilterBanner searchText={searchText} onClear={() => setSearchText("")} />
        <section id="cartelera" aria-labelledby="movies-title">
          <div className="section-heading">
            <p className="eyebrow">EN PANTALLA</p>
            <h2 id="movies-title">Nuestra cartelera</h2>
            <p>Elige tu próxima historia y encuentra el horario ideal.</p>
          </div>
          <MovieList
            movies={adaptedMovies}
            searchText={debouncedSearch}
            onToggleFavorite={toggleFavorite}
            favorites={favorites}
          />
        </section>
        <PremiereSection searchText={searchText} />
      </main>
      <Footer contact={contact} />
      <ToastContainer newestOnTop closeOnClick pauseOnFocusLoss />
    </>
  );
}
