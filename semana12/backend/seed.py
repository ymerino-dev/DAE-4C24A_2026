"""Seed the database with initial movie data."""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django  # noqa: E402

django.setup()

from catalog.models import Movie  # noqa: E402


INITIAL_MOVIES = [
    {
        'title': 'The Shawshank Redemption',
        'director': 'Frank Darabont',
        'release_year': 1994,
        'genre': 'Drama',
    },
    {
        'title': 'The Godfather',
        'director': 'Francis Ford Coppola',
        'release_year': 1972,
        'genre': 'Crime',
    },
    {
        'title': 'Inception',
        'director': 'Christopher Nolan',
        'release_year': 2010,
        'genre': 'Science Fiction',
    },
    {
        'title': 'Parasite',
        'director': 'Bong Joon-ho',
        'release_year': 2019,
        'genre': 'Thriller',
    },
]


def seed_movies():
    """Insert the initial movies without creating duplicates."""
    for movie_data in INITIAL_MOVIES:
        movie, created = Movie.objects.update_or_create(
            title=movie_data['title'],
            director=movie_data['director'],
            defaults={
                'release_year': movie_data['release_year'],
                'genre': movie_data['genre'],
            },
        )
        action = 'Created' if created else 'Updated'
        print(f'{action}: {movie.title} ({movie.release_year})')

    print(f'Total movies in database: {Movie.objects.count()}')


if __name__ == '__main__':
    seed_movies()
