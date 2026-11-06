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
      <div className="hero-image">
        <img src={movie.image} alt={`Afiche de ${movie.title}`} loading="lazy" />
        <div className="hero-image-overlay" />
        <span className="hero-classification-chip">{movie.classification}</span>
      </div>
    </section>
  );
}
