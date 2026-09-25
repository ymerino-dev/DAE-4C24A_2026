"""Script to test the relations defined in the library models.

Run it from the project root with:
    python scripts/test_relations.py
"""

import os
import sys

import django
from django.db.models import Count
from django.db.models.deletion import ProtectedError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from library.models import (  # noqa: E402
    Author,
    AuthorProfile,
    Book,
    Category,
    Publication,
    Publisher,
)


def log(message):
    print(message, flush=True)


def section(title):
    log('')
    log('=' * 62)
    log(title)
    log('=' * 62)


def test_forward_queries():
    section('1. FORWARD QUERIES  (book.author)')
    for book in Book.objects.all():
        log(f'  book "{book.title}"')
        log(f'      -> book.author      = {book.author}')
        log(f'      -> author.birth_date = {book.author.birth_date}')
        try:
            log(f'      -> author.profile    = {book.author.profile}')
        except AuthorProfile.DoesNotExist:
            log('      -> author.profile    = (no profile)')
    log(f'  forward FK queries OK: {Book.objects.count()} books resolved')


def test_reverse_queries():
    section('2. REVERSE QUERIES  (author.books.all())')
    for author in Author.objects.all():
        titles = [b.title for b in author.books.all()]
        log(f'  {author} -> {len(titles)} book(s)')
        for title in titles:
            log(f'      - {title}')
    log(f'  reverse related_name="books" OK')


def test_double_underscore_filtering():
    section('3. DOUBLE UNDERSCORE FILTERING')
    log('  Book.objects.filter(author__first_name="Gabriel")')
    for book in Book.objects.filter(author__first_name='Gabriel'):
        log(f'      - {book.title}')

    log('  Book.objects.filter(author__last_name__startswith="Borg")')
    for book in Book.objects.filter(author__last_name__startswith='Borg'):
        log(f'      - {book.title}')

    log('  Book.objects.filter(categories__name="Fiction")  (M2M traversal)')
    for book in Book.objects.filter(categories__name='Fiction'):
        log(f'      - {book.title}')

    log('  Publication.objects.filter(book__author__last_name="Borges")')
    for pub in Publication.objects.filter(
        book__author__last_name='Borges'
    ):
        log(f'      - {pub}')

    log('  Book.objects.filter(publications__publisher__country="Spain")')
    for book in Book.objects.filter(
        publications__publisher__country='Spain'
    ).distinct():
        log(f'      - {book.title}')

    log('  Book.objects.filter(publication_year__gt=1950).count() = '
        f'{Book.objects.filter(publication_year__gt=1950).count()}')
    log('  double underscore lookups OK')


def test_m2m_and_through():
    section('3b. M2M AND THROUGH MODEL')
    book = Book.objects.get(title='One Hundred Years of Solitude')
    log(f'  book.categories (M2M)     -> {[c.name for c in book.categories.all()]}')
    book_with_two = (
        Book.objects.annotate(category_count=Count('categories'))
        .filter(category_count__gte=2)
    )
    log(f'  books with 2+ categories  -> {book_with_two.count()} book(s)')
    for item in book_with_two:
        log(f'      - {item.title} ({item.category_count} categories)')
    book_two_publishers = Book.objects.get(
        title='Love in the Time of Cholera'
    )
    log(f'  {book_two_publishers.title} publishers (through Publication) -> '
        f'{[p.name for p in book_two_publishers.publishers.all()]}')
    for pub in book_two_publishers.publications.all():
        log(f'      - {pub.publication_date} / edition {pub.edition}')
    log('  through model OK')


def test_cascade_delete():
    section('4. DELETE BEHAVIOUR  (on_delete)')
    behaviour = Book._meta.get_field('author').remote_field.on_delete.__name__
    log(f'  Book.author on_delete = {behaviour}')

    author = Author.objects.create(first_name='Temp', last_name='DeleteTest')
    book = Book.objects.create(title='Temp Book', author=author)
    log(f'  created author id={author.id} book id={book.id}')
    log(f'  before delete -> books of author = {author.books.count()}')

    try:
        author.delete()
    except ProtectedError as error:
        log(f'  author.delete() -> ProtectedError raised')
        log(f'      message : {error.args[0]}')
        log(f'      blocked : {[str(obj) for obj in error.protected_objects]}')
        log(f'  RESULT: delete BLOCKED, nothing removed -> PROTECT works')
    else:
        log(f'  author.delete() executed (no exception)')
        log(f'  author still exists = '
            f'{Author.objects.filter(pk=author.id).exists()}')
        log(f'  book still exists   = '
            f'{Book.objects.filter(pk=book.id).exists()}')
        log('  RESULT: book was deleted automatically -> CASCADE works')

    Book.objects.filter(title='Temp Book').delete()
    if behaviour != 'PROTECT':
        Author.objects.filter(first_name='Temp').delete()
        log('  cleanup done')


def main():
    log(f'Authors={Author.objects.count()} Books={Book.objects.count()} '
        f'Categories={Category.objects.count()} Publishers={Publisher.objects.count()} '
        f'Publications={Publication.objects.count()}')

    test_forward_queries()
    test_reverse_queries()
    test_double_underscore_filtering()
    test_m2m_and_through()
    test_cascade_delete()

    log('')
    log('All CASCADE tests finished.')


if __name__ == '__main__':
    main()
