from django.db import models


class Category(models.Model):
    """A thematic category an article can belong to."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    """A person who writes articles."""

    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    """A news article written by an author and tagged with categories."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    featured_image = models.ImageField(upload_to='articles/', blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    categories = models.ManyToManyField(
        Category,
        related_name='articles',
        blank=True,
    )

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-published_at']

    def __str__(self):
        return self.title
