from django.db import models


class Author(models.Model):
    """A person who writes books."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class AuthorProfile(models.Model):
    """Biographical information attached one-to-one to an Author."""

    # One-to-one relation: each profile belongs to exactly one author.
    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)

    class Meta:
        verbose_name = 'Author profile'
        verbose_name_plural = 'Author profiles'
        ordering = ['author']

    def __str__(self):
        return f'Profile of {self.author}'


class Publisher(models.Model):
    """A company that publishes books."""

    name = models.CharField(max_length=200, unique=True)
    foundation_year = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """A thematic classification used to group books."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """A written work, related to authors, categories and publishers."""

    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True, unique=True)

    # Many-to-one relation: a book has one author, an author has many books.
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
    )

    # Many-to-many relation: a book can belong to several categories.
    categories = models.ManyToManyField(
        Category,
        related_name='books',
        blank=True,
    )

    # Many-to-many relation through an explicit intermediate model.
    publishers = models.ManyToManyField(
        Publisher,
        through='Publication',
        related_name='books',
    )

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']

    def __str__(self):
        return self.title


class Publication(models.Model):
    """Intermediate model that links a Book with a Publisher."""

    # The pair of foreign keys below builds the Book-Publisher relation.
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='publications',
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='publications',
    )

    publication_date = models.DateField()
    edition = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        ordering = ['-publication_date']

    def __str__(self):
        return f'{self.book} - {self.publisher} (edition {self.edition})'
