import useDebounce from "../../hooks/useDebounce.js";
import usePremieres from "../../hooks/usePremieres.js";
import LoadingSkeleton from "./LoadingSkeleton.jsx";
import Button from "./Button.jsx";

export default function PremiereSection({ searchText = "" }) {
  const { status, premieres, error, retry } = usePremieres();
  const debouncedFilter = useDebounce(searchText, 400).trim().toLowerCase();
  const visiblePremieres = premieres.filter((movie) => movie.title.toLowerCase().includes(debouncedFilter));

  return (
    <section id="proximamente" className="premieres" aria-labelledby="premieres-title">
      <div className="section-heading">
        <p className="eyebrow">PRÓXIMAMENTE</p>
        <h2 id="premieres-title">Estrenos que vienen</h2>
        <p>Una selección de historias que pronto llegarán a nuestras salas.</p>
      </div>
      {status === "loading" && <LoadingSkeleton />}
      {status === "error" && (
        <div className="premiere-error" role="alert">
          <p>{error}</p>
          <Button onClick={retry}>Intentar de nuevo</Button>
        </div>
      )}
      {status === "success" && (visiblePremieres.length ? (
        <div className="premiere-carousel" role="region" aria-label="Carrusel de estrenos" tabIndex={0} aria-live="polite">
          {visiblePremieres.map((movie) => (
            <article className="premiere-card" key={movie.id}>
              <img src={movie.image} alt="" loading="lazy" />
              <div><p className="classification">{movie.classification}</p><h3>{movie.title}</h3><p>{movie.synopsis}</p></div>
            </article>
          ))}
        </div>
      ) : <p className="empty-state">No hay estrenos que coincidan con este filtro.</p>)}
    </section>
  );
}
