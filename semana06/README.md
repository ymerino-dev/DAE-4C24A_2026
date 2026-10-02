# Semana 06 — Portal de Noticias (News)

Proyecto Django que implementa un portal de noticias con modelos relacionales,
panel de administración personalizado, plantillas con herencia y componentes
reutilizables, y verificación de seguridad contra XSS.

## Estructura

```
semana06/
├── manage.py
├── requirements.txt
├── config/                    # settings, urls, wsgi, asgi
├── news/
│   ├── models.py              # Category, Author, Article
│   ├── admin.py               # ModelAdmin personalizados
│   ├── views.py               # home, article_detail, category_detail
│   ├── urls.py                # rutas nombradas (app_name='news')
│   ├── management/commands/seed_news.py
│   └── migrations/
├── templates/
│   ├── base.html              # plantilla base (bloques title/content/sidebar)
│   └── news/
│       ├── home.html
│       ├── article_detail.html
│       ├── category_detail.html
│       └── _article_card.html # fragmento reutilizable de tarjeta
├── static/css/styles.css      # hoja de estilos responsive
├── templates/                 # TEMPLATES['DIRS']
└── media/                     # MEDIA_ROOT (no versionada)
```

## Puesta en marcha

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_news
python manage.py runserver
```

- Panel de administración: http://127.0.0.1:8000/admin/
- Portada: http://127.0.0.1:8000/

## Paso 12 — Prueba de escapado automático (Auto-escaping) contra XSS

### Procedimiento

1. Se creó un artículo cuyo campo `body` contiene código malicioso:
   `<b>Noticia de Prueba</b> <script>alert("XSS")</script>`.
2. Se solicitó la página de detalle del artículo mediante el cliente de
   pruebas de Django (`django.test.Client`).

### Resultado observado

| Verificación | Resultado |
|---|---|
| Estado HTTP de la respuesta | `200 OK` |
| ¿Aparece `<script>alert` sin procesar en el HTML? | **No** |
| ¿Aparece escapado como `&lt;script&gt;`? | **Sí** |
| ¿Aparece `<b>` escapado como `&lt;b&gt;`? | **Sí** |

El navegador recibe texto plano (`&lt;script&gt;alert("XSS")&lt;/script&gt;`),
por lo que el código nunca se ejecuta como script.

### Explicación técnica

Django utiliza un motor de plantillas con **escapado automático (auto-escaping)**
activado por defecto. Cada vez que una variable se interpola en una plantilla
mediante la sintaxis `{{ variable }}`, el motor aplica la función `escape` de
`django.utils.html`, que convierte los caracteres con significado HTML en
entidades seguras:

| Carácter | Entidad generada |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |
| `&` | `&amp;` |

De esta forma, un atacante que inyecte `<script>alert("XSS")</script>` en un
campo de texto (por ejemplo, el cuerpo de una noticia) consigue únicamente que
el navegador **muestre literalmente** esos caracteres como texto visible, en
lugar de interpretarlos como código HTML ejecutable. La vulnerabilidad XSS
(Cross-Site Scripting), que permitiría robar cookies de sesión, suplantar la
identidad del usuario o realizar acciones en su nombre, queda neutralizada en
la capa de presentación.

Puntos clave del mecanismo:

- **Protección por defecto**: no requiere configuración adicional; cualquier
  `{{ }}` en una plantilla escapa su contenido salvo que se marque
  explícitamente como seguro con `|safe` o `{% autoescape off %}`.
- **Contexto de escapado**: el escapado se aplica a variables, no a la
  estructura de la plantilla, por lo que el HTML legítimo definido por el
  desarrollador se mantiene intacto.
- **Defensa en profundidad**: el auto-escaping complementa (no reemplaza) otras
  medidas como la validación de formularios, el uso de `get_object_or_404` y
  los permisos del panel de administración.
- **Excepciones conscientes**: cuando se necesita renderizar HTML de confianza
  (por ejemplo, contenido enriquecido sanitizado), debe hacerse de forma
  explícita y controlada, nunca con entrada directa del usuario.
