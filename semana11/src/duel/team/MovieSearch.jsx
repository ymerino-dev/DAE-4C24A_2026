// Semana 10 — Buscador controlado.
// El texto vive en el estado local y onChange lo actualiza en cada pulsación.
// Un retardo (debounce) evita que el filtrado se dispare con cada letra.
import { useState, useRef, useEffect } from "react";

export default function MovieSearch({ onSearch, debounceMs = 400 }) {
  const [text, setText] = useState("");
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const handleChange = (event) => {
    const value = event.target.value;
    setText(value);
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      onSearch(value);
    }, debounceMs);
  };

  return (
    <div className="search">
      <label htmlFor="movie-search" className="label sr-only">
        Buscar película
      </label>
      <input
        id="movie-search"
        type="search"
        className="input search-input"
        value={text}
        onChange={handleChange}
        placeholder="Buscar por título…"
        aria-label="Buscar película"
      />
    </div>
  );
}
