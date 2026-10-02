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

## Paso 13 — Matriz de casos de prueba

| Caso | Descripción | Procedimiento | Resultado esperado | Estado |
|---|---|---|---|---|
| 1 | Renderizado de portada con listado de noticias | Ejecutar `seed_news` y abrir `/` | La portada muestra las 6 noticias ordenadas de más reciente a más antigua, cada una con tarjeta (imagen, título, autor, fecha `d/m/Y H:i`, excerpt de 20 palabras y etiquetas) | ✅ Verificado |
| 2 | Renderizado del estado sin datos (`{% empty %}`) | Acceder a una categoría sin artículos (o vaciar la tabla `Article`) | Se muestra el mensaje "No articles in this category yet." en lugar de una página en blanco o error | ✅ Verificado |
| 3 | Filtrado de publicaciones por categoría reutilizando el componente tarjeta | Abrir `/category/technology/` | Solo se listan las 2 artículos de la categoría, renderizadas con el mismo fragmento `_article_card.html` que la portada | ✅ Verificado |
| 4 | Renderizado de detalle de noticia y verificación de protección XSS | Crear un artículo con `<script>alert("XSS")</script>` en `body` y abrir su detalle | La página responde `200 OK` y el script aparece escapado (`&lt;script&gt;`); nunca se ejecuta como código | ✅ Verificado |

## Conclusiones técnicas

1. **Herencia de plantillas y principio DRY.** La plantilla `base.html`
   define una única vez la estructura común del sitio (cabecera, hoja de
   estilos, layout de dos columnas, footer) y expone bloques (`title`,
   `content`, `sidebar`) que cada plantilla hija reutiliza y sobrescribe.
   Cualquier cambio visual o estructural se realiza en un solo punto y
   propaga automáticamente a todas las vistas, eliminando duplicación y
   reduciendo el riesgo de inconsistencias entre páginas.

2. **Componentes modulares reutilizables.** El fragmento
   `_article_card.html` encapsula la presentación completa de una noticia
   (imagen, metadatos, excerpt, etiquetas) y se reutiliza mediante
   `{% include %}` tanto en la portada como en el listado por categoría. Esto
   garantiza que la tarjeta se vea y se comporte idénticamente en cualquier
   contexto, y que futuras mejoras (por ejemplo, un badge de "destacada")
   se implementen una sola vez.

3. **Desacoplamiento de la gestión de contenido.** La capa de datos
   (modelos `Category`, `Author`, `Article` con sus relaciones), la capa de
   administración (`ModelAdmin` con buscado, filtros y slugs
   autocompletados) y la capa de presentación (vistas, URLs nombradas y
   plantillas) son independientes entre sí. El contenido se gestiona
   centralizadamente desde el panel de administración o mediante el comando
   `seed_news`, y el frontend lo consume sin conocer los detalles de
   almacenamiento. Esta separación permite escalar el proyecto (nuevas
   vistas, APIs o temas) sin modificar los modelos, y refuerza la seguridad:
   el contenido ingresado por usuarios se escapa automáticamente al
   renderizarse, mitigando XSS por diseño.
