from django.contrib import admin

from .models import Genre, Movie, Person, Rating


class RatingInline(admin.TabularInline):
    """Ratings shown as editable rows inside the Movie change form."""

    model = Rating
    extra = 1
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'created_at')
    list_filter = ('genres', 'release_year')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RatingInline]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    list_filter = ('role',)
    search_fields = ('name',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'score', 'created_at')
    list_filter = ('score',)
    readonly_fields = ('created_at', 'updated_at')
