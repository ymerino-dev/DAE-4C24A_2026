from django.contrib import admin

from library.models import (
    Author,
    AuthorProfile,
    Book,
    Category,
    Publication,
    Publisher,
)


class AuthorProfileInline(admin.StackedInline):
    """Edit the one-to-one profile directly from the Author page."""

    model = AuthorProfile
    can_delete = False
    extra = 0


class PublicationInline(admin.TabularInline):
    """Edit the Book-Publisher intermediate rows from the Book page."""

    model = Publication
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    inlines = [AuthorProfileInline]


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('author', 'has_photo')
    list_filter = ('author',)
    search_fields = ('author__first_name', 'author__last_name')

    @admin.display(boolean=True, description='Has photo')
    def has_photo(self, obj):
        return bool(obj.photo)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'foundation_year', 'country')
    search_fields = ('name', 'country')
    list_filter = ('country',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'pages', 'isbn')
    search_fields = ('title', 'isbn', 'author__first_name', 'author__last_name')
    list_filter = ('publication_year', 'categories', 'author')
    filter_horizontal = ('categories',)
    inlines = [PublicationInline]


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('book', 'publisher', 'publication_date', 'edition')
    search_fields = ('book__title', 'publisher__name')
    list_filter = ('publisher', 'edition')
    autocomplete_fields = ('book', 'publisher')
