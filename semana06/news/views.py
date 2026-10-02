from django.shortcuts import get_object_or_404, render

from news.models import Article, Category


def home(request):
    """List all articles, newest first."""
    articles = Article.objects.select_related('author').prefetch_related(
        'categories'
    ).order_by('-published_at')
    return render(request, 'news/home.html', {'articles': articles})


def article_detail(request, slug):
    """Show a single article identified by its slug."""
    article = get_object_or_404(
        Article.objects.select_related('author').prefetch_related('categories'),
        slug=slug,
    )
    return render(request, 'news/article_detail.html', {'article': article})


def category_detail(request, slug):
    """Show a category and all of its associated articles."""
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.select_related('author').order_by('-published_at')
    return render(
        request,
        'news/category_detail.html',
        {
            'category': category,
            'articles': articles,
            'categories': Category.objects.all(),
        },
    )
