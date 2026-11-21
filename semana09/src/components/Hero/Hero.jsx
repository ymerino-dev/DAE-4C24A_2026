import './Hero.css'

function Hero({ featuredMovie }) {
  return (
    <section className="hero" aria-labelledby="hero-title">
      <div className="hero__content">
        <p className="hero__eyebrow">Featured today</p>
        <h1 className="hero__title" id="hero-title">
          {featuredMovie.title}
        </h1>
        <p className="hero__synopsis">{featuredMovie.synopsis}</p>
        <div className="hero__meta">
          <span className="hero__classification">
            {featuredMovie.classification}
          </span>
          <span className="hero__rating">{featuredMovie.rating.toFixed(1)} / 10</span>
        </div>
      </div>

      <img
        className="hero__image"
        src={featuredMovie.image}
        alt={`${featuredMovie.title} poster`}
      />
    </section>
  )
}

export default Hero
