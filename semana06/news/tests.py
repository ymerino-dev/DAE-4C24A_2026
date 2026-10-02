from django.test import Client, TestCase

from news.models import Article, Author, Category


class HomeViewTest(TestCase):
    """Case 1: the home page lists all articles, newest first."""

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name='Test Author')
        cls.category = Category.objects.create(name='Technology', slug='technology')
        for i in range(3):
            article = Article.objects.create(
                title=f'Article {i}',
                slug=f'article-{i}',
                body='Body text.',
                author=cls.author,
            )
            article.categories.add(cls.category)

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_lists_all_articles(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context['articles']), 3)

    def test_home_orders_by_published_at_desc(self):
        response = self.client.get('/')
        articles = list(response.context['articles'])
        self.assertEqual(articles[0].title, 'Article 2')


class EmptyStateTest(TestCase):
    """Case 2: the {% empty %} block renders when there is no content."""

    def test_home_empty_state(self):
        response = self.client.get('/')
        self.assertContains(response, 'No articles have been published yet.')

    def test_category_empty_state(self):
        Category.objects.create(name='Empty', slug='empty')
        response = self.client.get('/category/empty/')
        self.assertContains(response, 'No articles in this category yet.')


class CategoryDetailTest(TestCase):
    """Case 3: articles are filtered by category using the card fragment."""

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name='Test Author')
        cls.tech = Category.objects.create(name='Technology', slug='technology')
        cls.sports = Category.objects.create(name='Sports', slug='sports')
        for i in range(2):
            article = Article.objects.create(
                title=f'Tech {i}', slug=f'tech-{i}', body='Body.', author=cls.author
            )
            article.categories.add(cls.tech)
        other = Article.objects.create(
            title='Sport 1', slug='sport-1', body='Body.', author=cls.author
        )
        other.categories.add(cls.sports)

    def test_category_filters_articles(self):
        response = self.client.get('/category/technology/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 2)

    def test_category_uses_article_card_fragment(self):
        response = self.client.get('/category/technology/')
        self.assertTemplateUsed(response, 'news/_article_card.html')
        self.assertContains(response, 'article-card__title')


class ArticleDetailTest(TestCase):
    """Case 4: article detail renders and XSS payloads are auto-escaped."""

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name='Test Author')
        cls.article = Article.objects.create(
            title='Detail',
            slug='detail',
            body='<b>Bold</b> <script>alert("XSS")</script>',
            author=cls.author,
        )

    def test_detail_status_code(self):
        response = self.client.get('/article/detail/')
        self.assertEqual(response.status_code, 200)

    def test_detail_escapes_html(self):
        response = self.client.get('/article/detail/')
        self.assertNotContains(response, '<script>alert', status_code=200)
        self.assertContains(response, '&lt;script&gt;')

    def test_detail_unknown_slug_returns_404(self):
        response = self.client.get('/article/does-not-exist/')
        self.assertEqual(response.status_code, 404)
