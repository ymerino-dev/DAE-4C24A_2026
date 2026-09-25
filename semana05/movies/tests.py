from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .admin import MovieAdmin, RatingInline
from .models import Genre, Movie, Person, Rating

VALID_PNG = bytes.fromhex(
    '89504e470d0a1a0a0000000d4948445200000001000000010806000000'
    '1f15c4890000000a49444154789c636000000200010005fe02fea7'
    '3b1a1e450000000049454e44ae426082'
)


class GenreModelTests(TestCase):
    def test_str_returns_name(self):
        genre = Genre.objects.create(name='Science Fiction')
        self.assertEqual(str(genre), 'Science Fiction')

    def test_name_is_unique(self):
        Genre.objects.create(name='Drama')
        with self.assertRaises(Exception):
            Genre.objects.create(name='Drama')

    def test_default_ordering_is_by_name(self):
        Genre.objects.create(name='Science Fiction')
        Genre.objects.create(name='Drama')
        self.assertEqual(
            [g.name for g in Genre.objects.all()],
            ['Drama', 'Science Fiction'],
        )


class PersonModelTests(TestCase):
    def test_role_choices(self):
        self.assertEqual(
            list(Person.Role.choices),
            [('ACTOR', 'Actor'), ('DIRECTOR', 'Director')],
        )

    def test_invalid_role_is_rejected(self):
        person = Person(name='Jane Roe', role='WRITER')
        with self.assertRaises(ValidationError) as ctx:
            person.full_clean()
        self.assertIn('role', ctx.exception.message_dict)

    def test_str_returns_name(self):
        person = Person.objects.create(
            name='Keanu Reeves',
            role=Person.Role.ACTOR,
        )
        self.assertEqual(str(person), 'Keanu Reeves')


class MovieModelTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Science Fiction')
        self.actor = Person.objects.create(
            name='Keanu Reeves',
            role=Person.Role.ACTOR,
        )
        self.movie = Movie.objects.create(
            title='The Matrix',
            release_year=1999,
            synopsis='A hacker discovers reality is a simulation.',
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.movie), 'The Matrix')

    def test_cover_is_optional(self):
        self.assertEqual(self.movie.cover.name, '')

    def test_cover_is_stored_under_covers(self):
        self.movie.cover = SimpleUploadedFile(
            'cover.png', VALID_PNG, content_type='image/png',
        )
        self.movie.save()
        self.assertTrue(self.movie.cover.name.startswith('covers/'))

    def test_timestamps_are_set_automatically(self):
        self.assertIsNotNone(self.movie.created_at)
        self.assertIsNotNone(self.movie.updated_at)

    def test_genres_and_cast_relations(self):
        self.movie.genres.set([self.genre])
        self.movie.cast.set([self.actor])
        self.assertEqual(list(self.movie.genres.all()), [self.genre])
        self.assertEqual(list(self.movie.cast.all()), [self.actor])
        self.assertEqual(list(self.genre.movies.all()), [self.movie])
        self.assertEqual(list(self.actor.movies.all()), [self.movie])


class RatingModelTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='The Matrix',
            release_year=1999,
            synopsis='A hacker discovers reality is a simulation.',
        )

    def test_str_includes_movie_and_score(self):
        rating = Rating(movie=self.movie, score=5, comment='Great')
        self.assertEqual(str(rating), 'The Matrix - 5/5')

    def test_score_boundaries_are_accepted(self):
        for score in (1, 5):
            with self.subTest(score=score):
                Rating(
                    movie=self.movie, score=score, comment='ok',
                ).full_clean()

    def test_score_out_of_range_is_rejected(self):
        for score in (0, 6):
            with self.subTest(score=score):
                rating = Rating(movie=self.movie, score=score, comment='no')
                with self.assertRaises(ValidationError) as ctx:
                    rating.full_clean()
                self.assertIn('score', ctx.exception.message_dict)

    def test_reverse_relation_from_movie(self):
        Rating.objects.create(movie=self.movie, score=4, comment='Solid')
        self.assertEqual(self.movie.ratings.count(), 1)

    def test_deleting_movie_cascades_to_ratings(self):
        Rating.objects.create(movie=self.movie, score=4, comment='Solid')
        self.movie.delete()
        self.assertEqual(Rating.objects.count(), 0)


class CreateAdminCommandTests(TestCase):
    command_name = 'create_admin'

    def test_creates_superuser_when_missing(self):
        from io import StringIO

        from django.core.management import call_command

        out = StringIO()
        call_command(self.command_name, stdout=out)

        user = get_user_model().objects.get(username='admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'admin@cine.com')
        self.assertTrue(user.check_password('AdminPassword123!'))
        self.assertIn('created', out.getvalue())

    def test_is_idempotent(self):
        from io import StringIO

        from django.core.management import call_command

        call_command(self.command_name, stdout=StringIO())
        call_command(self.command_name, stdout=StringIO())

        self.assertEqual(get_user_model().objects.count(), 1)


class AdminConfigTests(TestCase):
    def test_all_models_are_registered(self):
        from django.contrib import admin as django_admin

        for model in (Genre, Movie, Person, Rating):
            with self.subTest(model=model.__name__):
                self.assertIn(model, django_admin.site._registry)

    def test_movie_admin_options(self):
        self.assertEqual(
            MovieAdmin.list_display,
            ('title', 'release_year', 'created_at'),
        )
        self.assertEqual(MovieAdmin.list_filter, ('genres', 'release_year'))
        self.assertEqual(MovieAdmin.search_fields, ('title',))
        self.assertEqual(MovieAdmin.inlines, [RatingInline])
        self.assertEqual(
            MovieAdmin.readonly_fields, ('created_at', 'updated_at'),
        )

    def test_rating_inline_options(self):
        self.assertEqual(RatingInline.extra, 1)
        self.assertEqual(
            RatingInline.readonly_fields, ('created_at', 'updated_at'),
        )

    def test_movie_admin_index_is_reachable(self):
        url = reverse('admin:movies_movie_changelist')
        self.assertEqual(url, '/admin/movies/movie/')
