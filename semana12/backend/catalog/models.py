from django.db import models


class Movie(models.Model):
    """A movie available in the catalog."""

    title = models.CharField(max_length=150, blank=False)
    director = models.CharField(max_length=100, blank=False)
    release_year = models.IntegerField(null=False)
    genre = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.title
