# DAE - Desarrollo de Aplicaciones Enterprise

Repositorio de las labs del curso. Cada carpeta corresponde a una semana.

| Carpana | Contenido |
| --- | --- |
| `semana01/` | Pendiente |
| `semana02/` | Pendiente |
| `semana03/` | Pendiente |
| `semana04/` | **Relacion de Modelos en Django** (proyecto Django) |

## Semana 04 - Relacion de Modelos en Django

Proyecto Django que demuestra las relaciones entre modelos: `ForeignKey`,
`OneToOneField`, `ManyToManyField` y un modelo intermedio con `through`.

### Estructura

```
semana04/
|-- manage.py
|-- requirements.txt
|-- config/                 # project settings, urls, wsgi, asgi
|-- library/                # the library application
|   |-- models.py           # Author, AuthorProfile, Publisher, Category,
|   |                       # Book, Publication
|   |-- views.py            # book_detail function based view
|   |-- urls.py
|   |-- admin.py
|   |-- templates/library/book_detail.html
|   |-- management/commands/seed_library.py
|   `-- migrations/
`-- scripts/test_relations.py
```

### Modelos y relaciones

| Modelo | Relaciones |
| --- | --- |
| `Author` | N a 1 con `Book`, 1 a 1 con `AuthorProfile` |
| `AuthorProfile` | `OneToOneField` a `Author`, `ImageField` para la foto |
| `Publisher` | N a N con `Book` mediante `Publication` |
| `Category` | N a N con `Book` |
| `Book` | `ForeignKey` a `Author`, `ManyToManyField` a `Category` y a `Publisher` (through `Publication`) |
| `Publication` | Modelo intermedio `Book` <-> `Publisher` con `publication_date` y `edition` |

### Puesta en marcha

```bash
cd semana04
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_library
python manage.py createsuperuser
python manage.py runserver
```

En Linux/macOS activating the virtual environment is `.venv/bin/activate`.

### Rutas

| URL | Descripcion |
| --- | --- |
| `/admin/` | Panel de administracion de Django |
| `/library/books/<pk>/` | Detalle de un libro |

### Comandos utiles

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py seed_library   # carga datos de muestra (idempotente)
python scripts/test_relations.py # pruebas de relaciones y on_delete
```

### Nota sobre `db.sqlite3`

La base de datos no se versiona. Tras clonar el repositorio hay que ejecutar
`python manage.py migrate` y `python manage.py seed_library`.
