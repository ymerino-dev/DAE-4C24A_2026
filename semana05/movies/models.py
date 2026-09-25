from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    """A genre a movie can be classified into (e.g. Action, Drama)."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Person(models.Model):
    """Someone involved in a movie, either as an actor or as a director."""

    class Role(models.TextChoices):
        ACTOR = 'ACTOR', 'Actor'
        DIRECTOR = 'DIRECTOR', 'Director'

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=Role.choices)

    class Meta:
        ordering = ['name']
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        return self.name


class Movie(models.Model):
    """A movie, its metadata and the people involved in it."""

    title = models.CharField(max_length=255, verbose_name='Title')
    release_year = models.IntegerField(verbose_name='Release Year')
    synopsis = models.TextField(verbose_name='Synopsis')
    cover = models.ImageField(
        upload_to='covers/',
        blank=True,
        verbose_name='Cover',
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='movies',
        verbose_name='Genres',
    )
    cast = models.ManyToManyField(
        Person,
        related_name='movies',
        verbose_name='Cast',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title


class Rating(models.Model):
    """A 1-to-5 score a user gives to a movie, with a short note."""

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f'{self.movie} - {self.score}/5'
