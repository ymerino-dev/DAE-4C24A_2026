from django.db.models import Avg, Count
from django.views.generic import TemplateView
from movies.models import Genre, Movie


class MovieRecommendationView(TemplateView):
    """Public view showing top-rated movies organized by genre."""

    template_name = 'movies/recommendations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        genres_with_movies = (
            Genre.objects.annotate(
                movie_count=Count('movies', distinct=True)
            )
            .filter(movie_count__gt=0)
            .prefetch_related(
                'movies__ratings'
            )
        )

        genre_data = []
        for genre in genres_with_movies:
            top_movies = (
                Movie.objects.filter(genres=genre)
                .annotate(avg_rating=Avg('ratings__score'), rating_count=Count('ratings'))
                .filter(rating_count__gt=0)
                .order_by('-avg_rating', '-rating_count')[:5]
            )
            if top_movies:
                genre_data.append({
                    'genre': genre,
                    'movies': top_movies,
                })

        context['genre_data'] = genre_data
        return context