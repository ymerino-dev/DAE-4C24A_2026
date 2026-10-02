import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image

from news.models import Article, Author, Category

CATEGORIES = [
    ('Technology', 'technology'),
    ('Sports', 'sports'),
    ('Culture', 'culture'),
]

AUTHORS = [
    ('Ada Lovelace', 'Writer and analyst covering science and technology.'),
    ('Alan Turing', 'Journalist focused on culture, games and society.'),
]

ARTICLES = [
    ('Quantum Computing Reaches New Milestone', 'technology',
     'Researchers announced a breakthrough in stable qubit design that could '
     'accelerate practical quantum computing within the decade.'),
    ('Local Team Wins Championship in Overtime', 'sports',
     'A dramatic overtime goal sealed the championship title in front of a '
     'record home crowd on Saturday night.'),
    ('City Museum Opens Interactive History Wing', 'culture',
     'The new wing features interactive exhibits that bring the city\'s '
     'industrial past to life for visitors of all ages.'),
    ('Open Source AI Models Gain Momentum', 'technology',
     'Community-driven AI projects are attracting contributors and '
     'enterprise adoption at an unprecedented pace.'),
    ('Marathon Participation Breaks Records', 'sports',
     'More than forty thousand runners took part in this year\'s marathon, '
     'making it the largest edition in the event\'s history.'),
    ('Independent Bookstores See a Revival', 'culture',
     'Independent bookshops are opening again across the country, driven by '
     'readers seeking curated recommendations and community events.'),
]

IMAGE_COLORS = {
    'technology': (37, 99, 235),
    'sports': (22, 163, 74),
    'culture': (190, 24, 93),
}


def make_sample_image(slug, color):
    """Build a small valid PNG in memory for the article featured image."""
    buffer = io.BytesIO()
    image = Image.new('RGB', (640, 360), color)
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'{slug}.png')


class Command(BaseCommand):
    help = 'Populate the news database with sample categories, authors and articles.'

    def handle(self, *args, **options):
        categories = {}
        for name, slug in CATEGORIES:
            category, created = Category.objects.get_or_create(
                slug=slug, defaults={'name': name}
            )
            categories[slug] = category
            self._report('Category', category.name, created)

        authors = {}
        for name, bio in AUTHORS:
            author, created = Author.objects.get_or_create(
                name=name, defaults={'bio': bio}
            )
            authors[name] = author
            self._report('Author', author.name, created)

        author_names = list(authors)
        for index, (title, category_slug, body) in enumerate(ARTICLES):
            slug = title.lower().replace(' ', '-')
            article, created = Article.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'body': body,
                    'author': authors[author_names[index % len(author_names)]],
                },
            )
            if created:
                article.categories.set([categories[category_slug]])
                article.featured_image = make_sample_image(
                    slug, IMAGE_COLORS[category_slug]
                )
                article.save()
            self._report('Article', article.title, created)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))

    def _report(self, model_name, obj_name, created):
        action = 'Created' if created else 'Already exists'
        self.stdout.write(f'{model_name}: {action} - {obj_name}')
