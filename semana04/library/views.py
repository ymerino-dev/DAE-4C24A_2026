from django.shortcuts import get_object_or_404, render

from library.models import Book


def book_detail(request, pk):
    """Display a single book with its related objects.

    The query is built to avoid the N+1 problem: select_related follows
    the forward ForeignKey and the reverse OneToOne, while prefetch_related
    loads the many side of the relations in extra queries.
    """
    book = get_object_or_404(
        Book.objects.select_related(
            'author',
            'author__profile',
        ).prefetch_related(
            'categories',
            'publications',
            'publications__publisher',
        ),
        pk=pk,
    )
    return render(request, 'library/book_detail.html', {'book': book})
