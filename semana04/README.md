# Semana 04 &mdash; Relacion de Modelos en Django

Practica de laboratorio sobre relaciones entre modelos en Django
(`ForeignKey`, `OneToOneField`, `ManyToManyField` y modelo intermedio
`through`).

## Contenido

| Ruta | Descripcion |
|---|---|
| `config/` | Configuracion del proyecto Django |
| `library/models.py` | `Author`, `AuthorProfile`, `Publisher`, `Category`, `Book`, `Publication` |
| `library/views.py` | Vista `book_detail` con `select_related` / `prefetch_related` |
| `library/templates/` | Plantilla del detalle de libro |
| `library/static/` | Hoja de estilos del catalogo |
| `library/management/commands/seed_library.py` | Datos de muestra |
| `scripts/test_relations.py` | Pruebas de relaciones y `on_delete` |

## Inicio rapido

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_library
python manage.py runserver
```

Detalle de un libro: <http://127.0.0.1:8000/library/books/1/>

Ver el [README principal](../README.md) para el detalle completo.
