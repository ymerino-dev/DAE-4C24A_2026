"""Management command to populate the database with sample library data."""

import datetime

from django.core.management.base import BaseCommand

from library.models import (
    Author,
    AuthorProfile,
    Book,
    Category,
    Publication,
    Publisher,
)

AUTHORS = [
    {
        'first_name': 'Gabriel',
        'last_name': 'Garcia Marquez',
        'birth_date': datetime.date(1927, 3, 6),
        'biography': (
            'Colombian novelist and journalist, Nobel Prize winner in '
            'Literature. Considered one of the most important Spanish '
            'language writers of the twentieth century.'
        ),
    },
    {
        'first_name': 'Jorge Luis',
        'last_name': 'Borges',
        'birth_date': datetime.date(1899, 8, 24),
        'biography': (
            'Argentine writer whose works combine fiction with philosophy, '
            'poetry and literature. He is considered the founder of the '
            'modern short story.'
        ),
    },
]

PUBLISHERS = [
    {
        'name': 'Editorial Alfaguara',
        'foundation_year': 1964,
        'country': 'Spain',
    },
    {
        'name': 'Editorial Planeta',
        'foundation_year': 1952,
        'country': 'Spain',
    },
]

CATEGORIES = [
    {
        'name': 'Magical Realism',
        'description': (
            'A literary movement that incorporates fantasy elements into '
            'an otherwise realistic environment.'
        ),
    },
    {
        'name': 'Fiction',
        'description': 'Narrative works, both short stories and novels.',
    },
    {
        'name': 'Essays',
        'description': 'Non-fiction works that present the author ideas.',
    },
]

BOOKS = [
    {
        'title': 'One Hundred Years of Solitude',
        'publication_year': 1967,
        'pages': 471,
        'isbn': '9780307474728',
        'author': ('Gabriel', 'Garcia Marquez'),
        'categories': ['Magical Realism', 'Fiction'],
        'publications': [
            ('Editorial Alfaguara', datetime.date(1967, 5, 30), 1),
        ],
    },
    {
        'title': 'Love in the Time of Cholera',
        'publication_year': 1985,
        'pages': 401,
        'isbn': '9780307389732',
        'author': ('Gabriel', 'Garcia Marquez'),
        'categories': ['Magical Realism'],
        'publications': [
            ('Editorial Alfaguara', datetime.date(1985, 1, 1), 5),
            ('Editorial Planeta', datetime.date(1986, 6, 15), 7),
        ],
    },
    {
        'title': 'Ficciones',
        'publication_year': 1944,
        'pages': 174,
        'isbn': '9788437604947',
        'author': ('Jorge Luis', 'Borges'),
        'categories': ['Fiction', 'Essays'],
        'publications': [
            ('Editorial Planeta', datetime.date(1944, 1, 1), 1),
        ],
    },
    {
        'title': 'The Aleph',
        'publication_year': 1949,
        'pages': 148,
        'isbn': '9788432318184',
        'author': ('Jorge Luis', 'Borges'),
        'categories': ['Fiction'],
        'publications': [
            ('Editorial Planeta', datetime.date(1949, 1, 1), 3),
        ],
    },
]


class Command(BaseCommand):
    help = 'Populate the database with sample library data.'

    def handle(self, *args, **options):
        authors = {}
        for data in AUTHORS:
            author, _ = Author.objects.get_or_create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                defaults={'birth_date': data['birth_date']},
            )
            AuthorProfile.objects.update_or_create(
                author=author,
                defaults={'biography': data['biography']},
            )
            authors[(author.first_name, author.last_name)] = author
            self.stdout.write(f'Author: {author}')

        publishers = {}
        for data in PUBLISHERS:
            publisher, _ = Publisher.objects.get_or_create(
                name=data['name'],
                defaults={
                    'foundation_year': data['foundation_year'],
                    'country': data['country'],
                },
            )
            publishers[publisher.name] = publisher
            self.stdout.write(f'Publisher: {publisher}')

        categories = {}
        for data in CATEGORIES:
            category, _ = Category.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']},
            )
            categories[category.name] = category
            self.stdout.write(f'Category: {category}')

        for data in BOOKS:
            book, _ = Book.objects.get_or_create(
                title=data['title'],
                defaults={
                    'publication_year': data['publication_year'],
                    'pages': data['pages'],
                    'isbn': data['isbn'],
                    'author': authors[data['author']],
                },
            )
            for name in data['categories']:
                book.categories.add(categories[name])
            for name, pub_date, edition in data['publications']:
                Publication.objects.get_or_create(
                    book=book,
                    publisher=publishers[name],
                    edition=edition,
                    defaults={'publication_date': pub_date},
                )
            self.stdout.write(
                f'Book: {book} | categories={data["categories"]} '
                f'| publications={len(data["publications"])}'
            )

        self.stdout.write(self.style.SUCCESS('Sample data loaded.'))
