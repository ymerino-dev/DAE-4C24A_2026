<div align="center">

# DAE &mdash; Desarrollo de Aplicaciones Enterprise

### Laboratorios del curso

[![Django](https://img.shields.io/badge/Django-6.1.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-academic-8C3B2E?logo=opensourceinitiative&logoColor=white)](#)

</div>

---

## Estructura del repositorio

| Semana | Tema | Estado |
|:---:|---|:---:|
| `semana01` | — | *pendiente* |
| `semana02` | — | *pendiente* |
| `semana03` | — | *pendiente* |
| **`semana04`** | **Relacion de Modelos en Django** | **completo** |
| **`semana05`** | **Modelos de Peliculas y Django Admin** | **completo** |
| **`semana06`** | **Portal de Noticias (News)** | **completo** |

---

<div align="center">

## Semana 04 &mdash; Relacion de Modelos en Django

</div>

Proyecto Django que demuestra los cuatro tipos de relacion entre modelos:
`ForeignKey`, `OneToOneField`, `ManyToManyField` y un modelo intermedio
con `through`.

### Modelos y relaciones

| Modelo | Tipo | Relaciones |
|---|:---:|---|
| `Author` | autor | `1:N` con `Book` &middot; `1:1` con `AuthorProfile` |
| `AuthorProfile` | datos biograficos | `OneToOneField` &rarr; `Author` &middot; `ImageField` para la foto |
| `Publisher` | editorial | `N:N` con `Book` mediante `Publication` |
| `Category` | genero tematico | `N:N` con `Book` |
| `Book` | obra | `ForeignKey` &rarr; `Author` &middot; `M2M` &rarr; `Category` &middot; `M2M(through)` &rarr; `Publisher` |
| `Publication` | modelo intermedio | `FK` &rarr; `Book` &middot; `FK` &rarr; `Publisher` &middot; `publication_date` &middot; `edition` |

```
Author 1 ────< Book >──── 1 Author
Author 1 ───── 1 AuthorProfile
Book   >────< Category
Book   >────< Publication >────< Publisher
```

### Estructura del proyecto

```
semana04/
├── manage.py
├── requirements.txt
├── .gitignore
├── config/                          # settings, urls, wsgi, asgi
│   ├── settings.py                  # MEDIA_URL, MEDIA_ROOT, DEBUG
│   └── urls.py                      # incluye library.urls
├── library/
│   ├── models.py                    # los 6 modelos del laboratorio
│   ├── views.py                     # book_detail (function based view)
│   ├── urls.py                      # books/<int:pk>/
│   ├── admin.py                     # registros en el panel
│   ├── templates/library/
│   │   └── book_detail.html
│   ├── static/library/css/
│   │   └── book.css                 # tema visual del catalogo
│   ├── management/commands/
│   │   └── seed_library.py          # datos de muestra
│   └── migrations/
└── scripts/
    └── test_relations.py            # pruebas de relaciones y on_delete
```

### Puesta en marcha

```bash
cd semana04

# 1. Entorno virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

# 2. Dependencias
pip install -r requirements.txt

# 3. Base de datos y datos de muestra
python manage.py migrate
python manage.py seed_library

# 4. Superusuario (opcional)
python manage.py createsuperuser

# 5. Servidor
python manage.py runserver
```

### Rutas

| URL | Descripcion |
|---|---|
| `/admin/` | Panel de administracion de Django |
| `/library/books/&lt;pk&gt;/` | Detalle de un libro |

### Comandos utiles

```bash
python manage.py check                            # validar configuracion
python manage.py makemigrations                   # generar migraciones
python manage.py migrate                          # aplicar migraciones
python manage.py seed_library                     # datos de muestra (idempotente)
python scripts/test_relations.py                  # pruebas de relaciones
```

### Comportamiento de `on_delete` verificado

| Comportamiento | Resultado |
|---|---|
| `CASCADE` | al borrar el autor, sus libros se borran automaticamente |
| `PROTECT` | al borrar el autor, Django lanza `ProtectedError` y no borra nada |

### Notas

- `db.sqlite3` no se versiona. Tras clonar, ejecutar `migrate` y `seed_library`.
- `.venv/` tampoco se versiona.
- El servidor de medios se activa solo con `DEBUG = True` en `config/urls.py`.

---

<div align="center">

**Desarrollo de Aplicaciones Enterprise**

</div>
