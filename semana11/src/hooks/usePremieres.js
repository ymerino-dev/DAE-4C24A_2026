import { useCallback, useEffect, useState } from "react";
import { adaptMovie } from "../adapters/movieAdapter.js";

const premiereResponse = [
  { id: 101, name: "El mapa de las estrellas", poster_path: "/posters/6.svg", rating_label: "APT", overview: "Una astrónoma encuentra un mapa que conecta el cielo con su ciudad.", vote_average: 4.6 },
  { id: 102, name: "Código de invierno", poster_path: "/posters/3.svg", rating_label: "14+", overview: "Un equipo intenta descifrar una señal antes de la última nevada.", vote_average: 4.3 },
  { id: 103, name: "La casa del faro", poster_path: "/posters/4.svg", rating_label: "APT", overview: "Una familia vuelve a la costa para reconstruir el faro del pueblo.", vote_average: 4.1 },
  { id: 104, name: "Último tren al sur", poster_path: "/posters/8.svg", rating_label: "14+", overview: "Dos desconocidos comparten un viaje que cambia sus planes.", vote_average: 4.4 },
];

export default function usePremieres() {
  const [status, setStatus] = useState("loading");
  const [premieres, setPremieres] = useState([]);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);

  const retry = useCallback(() => setAttempt((value) => value + 1), []);

  useEffect(() => {
    let active = true;
    setStatus("loading");
    setError("");
    const timeoutId = window.setTimeout(() => {
      if (!active) return;
      if (new URLSearchParams(window.location.search).get("fallarEstrenos") === "1" && attempt === 0) {
        setStatus("error");
        setError("No se pudieron cargar los estrenos. Revisa tu conexión e inténtalo de nuevo.");
        return;
      }
      setPremieres(premiereResponse.map(adaptMovie));
      setStatus("success");
    }, 700);
    return () => {
      active = false;
      window.clearTimeout(timeoutId);
    };
  }, [attempt]);

  return { status, premieres, error, retry };
}
