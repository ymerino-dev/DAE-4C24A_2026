# Semana 05 &mdash; Modelos de Peliculas y Django Admin

Practica de laboratorio sobre la definicion de modelos en Django
(`CharField`, `TextField`, `ImageField`, `ManyToManyField`, `ForeignKey`),
la migracion de una base de datos SQLite y la personalizacion del panel de
administracion con clases `ModelAdmin` e inlines.

## Contenido

| Ruta | Descripcion |
|---|---|
| `config/` | Configuracion del proyecto Django |
| `config/settings.py` | `INSTALLED_APPS` con `movies`, `MEDIA_URL` y `MEDIA_ROOT` |
| `config/urls.py` | Enrutado de `/media/` solo cuando `DEBUG` es `True` |
| `movies/models.py` | `Genre`, `Person`, `Movie`, `Rating` |
| `movies/admin.py` | `ModelAdmin` para los cuatro modelos e inline de ratings |
| `movies/tests.py` | 22 pruebas de modelos, comando y configuracion del admin |
| `movies/migrations/0001_initial.py` | Esquema inicial de la base de datos |
| `movies/management/commands/create_admin.py` | Crea el superusuario `admin` si no existe |
| `requirements.txt` | Dependencias fijadas |

## Modelos

| Modelo | Campos | Relaciones |
|---|---|---|
| `Genre` | `name` (unico) | `M:N` con `Movie` |
| `Person` | `name`, `role` (`ACTOR` / `DIRECTOR`) | `M:N` con `Movie` |
| `Movie` | `title`, `release_year`, `synopsis`, `cover`, `created_at`, `updated_at` | `M:N` con `Genre` y `Person` |
| `Rating` | `movie`, `score` (1-5), `comment`, `created_at`, `updated_at` | `N:1` con `Movie` (`related_name='ratings'`) |

## Inicio rapido

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create_admin
python manage.py test
python manage.py runserver
```

Panel de administracion: <http://127.0.0.1:8000/admin/>

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Correo | `admin@cine.com` |
| Contrasena | `AdminPassword123!` |

> `create_admin` es idempotente: si el superusuario ya existe no lo modifica.

## Pruebas

```bash
python manage.py test
```

Ver el [README principal](../README.md) para el detalle completo.
