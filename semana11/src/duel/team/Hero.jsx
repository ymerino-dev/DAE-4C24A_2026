export default function Hero({ movie }) {
  return (
    <section className="hero" aria-label="Destacada">
      <div className="hero-content">
        <div className="hero-badge">
          <span>✦</span> Estreno destacado
        </div>
        <p className="eyebrow">{movie.classification}</p>
        <h2>{movie.title}</h2>
        <p className="hero-synopsis">{movie.synopsis}</p>
        <a href={`#horarios-${movie.id}`} className="hero-cta">
          Ver horarios
        </a>
      </div>
    </section>
  );
}
