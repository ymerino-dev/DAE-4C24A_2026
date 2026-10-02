# ENTREGABLE — Laboratorio 06: Portal de Noticias (News)

**Curso:** DAE — Desarrollo de Aplicaciones Enterprise
**Tecnologías:** Django 5.2.16, Python 3.13, SQLite, Pillow
**Autor:** ymerino-dev (ana.merino@tecsup.edu.pe)

---

## a) Estructura completa de archivos y carpetas

```
DAE-4C24A_2026/
├── README.md                          # Índice general del repositorio
├── ENTREGABLE_LAB06.md                # Este informe
├── docs/
│   └── paso12_autoescaping.md         # Documentación del experimento XSS
└── semana06/
    ├── manage.py                      # Utilidad de línea de comandos de Django
    ├── requirements.txt               # Dependencias fijadas (Django, Pillow)
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py                # INSTALLED_APPS, TEMPLATES, STATIC, MEDIA
    │   ├── urls.py                    # Enrutado raíz + media en DEBUG
    │   ├── wsgi.py
    │   └── asgi.py
    ├── news/
    │   ├── __init__.py
    │   ├── apps.py                    # NewsConfig
    │   ├── models.py                  # Category, Author, Article
    │   ├── admin.py                   # ModelAdmin personalizados
    │   ├── views.py                   # home, article_detail, category_detail
    │   ├── urls.py                    # Rutas nombradas (app_name='news')
    │   ├── tests.py                   # 10 pruebas automatizadas
    │   ├── management/
    │   │   └── commands/
    │   │       └── seed_news.py      # Poblado de datos de prueba
    │   └── migrations/
    │       ├── __init__.py
    │       └── 0001_initial.py        # Migración inicial de los modelos
    ├── templates/
    │   ├── base.html                  # Plantilla base (bloques title/content/sidebar)
    │   └── news/
    │       ├── home.html              # Portada con listado de noticias
    │       ├── article_detail.html    # Detalle de noticia
    │       ├── category_detail.html   # Listado por categoría
    │       └── _article_card.html     # Fragmento reutilizable de tarjeta
    ├── static/
    │   └── css/
    │       └── styles.css             # Hoja de estilos responsive
    ├── media/                         # MEDIA_ROOT (imágenes subidas, no versionada)
    └── db.sqlite3                     # Base de datos SQLite (no versionada)
```

---

## b) Historial de commits (todos en español)

### Semanas anteriores (contexto del repositorio)

| Hash | Mensaje |
|---|---|
| `6fd69a4` | Add Django model relations lab for week 04 |
| `63be28f` | Redesign book detail page with a library catalog theme |
| `d12ab15` | feat: register movies app and media settings |
| `296ef8d` | feat: define Movie, Genre, Person, and Rating models |
| `42fa135` | chore: run initial migrations and superuser script |
| `96b97cb` | feat: customize Django Admin with ModelAdmin and inlines |
| `cbace50` | feat: configure editores group and restricted permissions |
| `b470330` | feat: añadir vista pública de recomendaciones con tema oscuro cinematográfico |
| `5d2f327` | docs: actualizar README con setup_roles y vista de recomendaciones |
| `a7536c8` | feat: añadir datos de ejemplo (12 películas, 50 valoraciones, 15 géneros) para visualizar recomendaciones |
| `f98763c` | chore: actualizar Django a versión compatible con Python 3.10 |

### Semana 06 — Portal de Noticias

| Hash | Mensaje | Fase |
|---|---|---|
| `7ad31ec` | feat(news): declarar modelos Category, Author y Article con sus migraciones - paso 3 | Fase 2 |
| `486a164` | feat(admin): personalizar panel de administracion para news - paso 11 | Fase 2 |
| `7b5fb86` | feat(seed): agregar comando para poblar base de datos con noticias de prueba | Fase 2 |
| `e71591c` | style(css): agregar hoja de estilos estaticos para el portal - paso 10 | Fase 3 |
| `2c006d9` | feat(templates): crear plantilla base.html con bloques principal y lateral - paso 4 | Fase 3 |
| `4cb2a11` | feat(templates): crear fragmento reutilizable de tarjeta de noticia _article_card.html - paso 5 | Fase 3 |
| `b5b6773` | feat(urls): declarar vistas y rutas nombradas para el portal - paso 9 | Fase 4 |
| `422dda1` | feat(templates): crear plantilla de portada con control for, empty y filtros - paso 6 | Fase 4 |
| `563c2d4` | feat(templates): crear plantilla de detalle de noticia heredando de base - paso 7 | Fase 4 |
| `73a8cc7` | feat(templates): crear plantilla de listado por categoria reutilizando tarjeta - paso 8 | Fase 4 |
| `3e24670` | test(security): documentar prueba de escapado automatico contra XSS - paso 12 | Fase final |
| `e135e0e` | docs: agregar casos de prueba, documentacion del informe y conclusiones - paso 13 | Fase final |
| `80966f0` | chore(news): limpiar datos de prueba, crear superusuario y agregar tests automatizados | Fase final |
| `73757b7` | docs: registrar semana 06 en el README principal | Fase final |
| `63a7055` | test(seguridad): documentar prueba de escapado automatico contra XSS - paso 12 | Fase final |

---

## c) Código fuente principal

### `news/models.py`

```python
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
```

### `news/admin.py`

```python
from django.contrib import admin

from .models import Article, Author, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at')
    list_filter = ('published_at', 'categories', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
```

### `news/views.py`

```python
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
```

### `templates/base.html`

```django
{% load static %}<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}News Portal{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
  <header class="site-header">
    <div class="site-header__inner">
      <a class="site-header__brand" href="{% url 'news:home' %}">News Portal</a>
      <nav class="site-header__nav">
        <a href="{% url 'news:home' %}">Home</a>
      </nav>
    </div>
  </header>

  <div class="page">
    <main class="page__main">
      {% block content %}{% endblock %}
    </main>

    <aside class="page__sidebar">
      {% block sidebar %}{% endblock %}
    </aside>
  </div>

  <footer class="site-footer">
    <p>&copy; {% now "Y" %} News Portal. All rights reserved.</p>
  </footer>
</body>
</html>
```

### `templates/news/_article_card.html`

```django
<article class="article-card">
  {% if article.featured_image %}
    <img class="article-card__image" src="{{ article.featured_image.url }}"
         alt="Featured image of {{ article.title }}" loading="lazy">
  {% endif %}

  <div class="article-card__body">
    <h2 class="article-card__title">
      <a href="{% url 'news:article_detail' article.slug %}">{{ article.title }}</a>
    </h2>

    <p class="article-card__meta">
      By {{ article.author.name }} &middot;
      {{ article.published_at|date:"d/m/Y H:i" }}
    </p>

    <p class="article-card__excerpt">{{ article.body|truncatewords:20 }}</p>

    <ul class="tag-list">
      {% for category in article.categories.all %}
        <li><a class="tag" href="{% url 'news:category_detail' category.slug %}">{{ category.name }}</a></li>
      {% endfor %}
    </ul>
  </div>
</article>
```

---

## d) Experimento de auto-escapado XSS (Paso 12)

### Procedimiento

1. Se creó un artículo con el siguiente contenido en el campo `body`:

   ```html
   <b>Noticia Importante</b>: Esta es una prueba de <script>alert('XSS')</script> seguridad.
   ```

2. Se verificó el renderizado en `article_detail.html` accediendo a
   `/article/noticia-importante/`.

### Resultado

| Verificación | Resultado |
|---|---|
| Estado HTTP | `200 OK` |
| `<script>alert` sin procesar en el HTML | No aparece |
| Escapado como `&lt;script&gt;` | Sí |
| `<b>` escapado como `&lt;b&gt;` | Sí |

### Explicación técnica

El motor de plantillas de Django tiene el **escapado automático
(auto-escaping)** activado por defecto. Al interpolar una variable con
`{{ variable }}`, Django aplica la función `escape` de `django.utils.html`,
que convierte los caracteres con significado HTML en entidades seguras:

| Carácter | Entidad |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |
| `&` | `&amp;` |

**¿Por qué previene XSS?** En un ataque Cross-Site Scripting, un atacante
inyecta código JavaScript en campos de texto que luego se ejecuta en el
navegador de otros usuarios, permitiendo el robo de cookies de sesión, la
suplantación de identidad o la redirección maliciosa. Al escapar `<` y `>`,
las etiquetas inyectadas se convierten en texto literal: el navegador muestra
`&lt;script&gt;` como los caracteres visibles `<script>`, sin interpretarlos
como código ejecutable. La protección es automática, se aplica a los datos
(no a la estructura de la plantilla) y no requiere configuración adicional.

**Riesgos del filtro `|safe`:** marca una variable como "segura" y la
renderiza **sin escapar**. Aplicado a contenido de usuario
(`{{ article.body|safe }}`), el `<script>` sí se ejecutaría, materializando la
vulnerabilidad. Solo debe usarse con contenido de confianza absoluta o
previamente sanitizado (por ejemplo, con `bleach`). La regla de oro: **escapar
por defecto, desescapar de forma explícita y justificada**.

> Documentación completa en [`docs/paso12_autoescaping.md`](docs/paso12_autoescaping.md).

---

## e) Matriz de Casos de Prueba

| # | Caso de prueba | Procedimiento | Resultado esperado | Estado |
|---|---|---|---|---|
| 1 | **Portada con noticias** — renderizado del listado | Ejecutar `seed_news` y abrir `/` | Las 6 noticias aparecen ordenadas de más reciente a más antigua, cada una con tarjeta (imagen, título, autor, fecha `d/m/Y H:i`, excerpt de 20 palabras y etiquetas) | ✅ Verificado |
| 2 | **Portada vacía con `{% empty %}`** — estado sin datos | Acceder a una categoría sin artículos | Se muestra "No articles in this category yet." en lugar de una página en blanco o error | ✅ Verificado |
| 3 | **Filtrado por categoría reutilizando la tarjeta** | Abrir `/category/technology/` | Solo se listan los 2 artículos de la categoría, renderizados con el mismo fragmento `_article_card.html` de la portada | ✅ Verificado |
| 4 | **Detalle de noticia con prueba XSS** | Crear un artículo con `<script>alert('XSS')</script>` en `body` y abrir su detalle | Respuesta `200 OK`; el script aparece escapado (`&lt;script&gt;`) y nunca se ejecuta | ✅ Verificado |

Además, los 4 escenarios están cubiertos por pruebas automatizadas en
`news/tests.py` (10 tests en total: listado, orden, estados vacíos, filtro por
categoría, uso del fragmento, escape XSS y 404), ejecutables con:

```bash
python manage.py test
```

---

## f) Conclusiones técnicas

### 1. Herencia de plantillas y principio DRY

La plantilla `base.html` define una única vez la estructura común del sitio
(cabecera, hoja de estilos, layout de dos columnas, footer) y expone bloques
(`title`, `content`, `sidebar`) que cada plantilla hija reutiliza y
sobrescribe. Cualquier cambio visual o estructural se realiza en un solo punto
y se propaga automáticamente a todas las vistas, eliminando la duplicación de
código y reduciendo el riesgo de inconsistencias entre páginas. Esto es una
aplicación directa del principio DRY (Don't Repeat Yourself).

### 2. Componentes modulares reutilizables

El fragmento `_article_card.html` encapsula la presentación completa de una
noticia (imagen destacada, metadatos, excerpt, etiquetas) y se reutiliza
mediante `{% include %}` tanto en la portada como en el listado por categoría.
Esto garantiza que la tarjeta se vea y se comporte idénticamente en cualquier
contexto, y que futuras mejoras (por ejemplo, un badge de "destacada" o un
botón de lectura rápida) se implementen una sola vez. La modularidad también
facilita las pruebas: el componente se verifica una vez y se asume correcto en
todos los lugares donde se incluye.

### 3. Gestión de contenido desacoplada desde el administrador

La capa de datos (modelos `Category`, `Author`, `Article` con sus
relaciones), la capa de administración (`ModelAdmin` con buscado, filtros y
slugs autocompletados) y la capa de presentación (vistas, URLs nombradas y
plantillas) son independientes entre sí. El contenido se gestiona
centralizadamente desde el panel de administración o mediante el comando
`seed_news`, y el frontend lo consume sin conocer los detalles de
almacenamiento. Esta separación permite escalar el proyecto (nuevas vistas,
APIs o temas) sin modificar los modelos, y refuerza la seguridad: el contenido
ingresado por usuarios se escapa automáticamente al renderizarse, mitigando
XSS por diseño, mientras que el filtro `|safe` queda reservado a contenido de
confianza absoluta.

---

**Fin del informe — Laboratorio 06: Portal de Noticias (News)**
