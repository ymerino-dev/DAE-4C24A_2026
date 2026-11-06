export default function Hero({ movie }) {
  return (
    <section className="hero" aria-label="Destacada" style={{ backgroundImage: `linear-gradient(90deg, rgb(8 12 25 / 92%), rgb(8 12 25 / 25%)), url(${movie.image})` }}>
      <p className="eyebrow">ESTRENO DESTACADO · {movie.classification}</p>
      <h2>{movie.title}</h2>
      <p className="hero-synopsis">{movie.synopsis}</p>
      <a href={`#horarios-${movie.id}`}>Ver horarios</a>
    </section>
  );
}
