// Converts data from the cinema service shape into the application's movie model.
export function adaptMovie(source) {
  return {
    id: Number(source.id),
    title: source.title || source.name || "Película sin título",
    image: source.image || source.poster_path || "/posters/1.svg",
    classification: source.classification || source.rating_label || "Por definir",
    synopsis: source.synopsis || source.overview || "Sin sinopsis disponible.",
    rating: Number(source.rating ?? source.vote_average ?? 0),
    showtimes: Array.isArray(source.showtimes) ? source.showtimes : [],
  };
}
