# Laboratorio 12 — Catálogo de películas

Documentación de ejecución, estados de pantalla y pruebas del back-end con Django REST Framework y del front-end con React, Axios y React Router.

- Repositorio: `https://github.com/ymerino-dev/DAE-4C24A_2026.git`
- Rama: `main`
- Back-end: `semana12/backend`
- Front-end: `semana12/frontend`

---

## 1. Cómo levantar el proyecto

### 1.1 Back-end (Django REST Framework)

Ubicación: `semana12/backend`  
Puerto: `8000`  
Orígenes permitidos por CORS: `http://localhost:5173` y `http://127.0.0.1:5173`

```bash
cd semana12/backend
py -3.13 -m pip install -r requirements.txt
py -3.13 manage.py migrate
py -3.13 seed.py
py -3.13 manage.py runserver 8000
```

> En este equipo se usa `py -3.13` porque el alias `python` apunta a Microsoft Store. En otros equipos puede utilizarse `python`.

Datos de acceso:

- URL base de la API: `http://127.0.0.1:8000/api`
- Endpoint del catálogo: `http://127.0.0.1:8000/api/movies/`
- Raíz navegable de DRF: `http://127.0.0.1:8000/api/`

El archivo `config/settings.py` **no usa** `CORS_ALLOW_ALL_ORIGINS = True`. Solo declara:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

### 1.2 Front-end (React + Vite + Axios)

Ubicación: `semana12/frontend`  
Puerto: `5173`  
URL base de la API: `http://127.0.0.1:8000/api`

```bash
cd semana12/frontend
npm install
npm run dev
```

La configuración está en `.env` y `.env.example`:

```txt
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

> Si Vite asigna otro puerto porque el 5173 está ocupado, el back-end no autorizará ese origen. Para forzar el puerto:
>
> ```bash
> npm run dev -- --port 5173 --strictPort
> ```

Todas las rutas de API se concentran en `src/services/apiClient.js`; ningún componente escribe URLs de API manualmente.

---

## 2. Tabla de estados de la pantalla

Ruta `/` → componente `MovieList`.

| Momento / estado | Condición | Qué se muestra | Acción técnica |
|---|---|---|---|
| Entrar a `/` | `isLoading = true`, `error = null`, `movies = []` | Esqueleto de carga animado de 5 filas y el texto **`Loading movies from server...`** | `useEffect` ejecuta `getMovies()`, que hace `GET /movies/` |
| Respuesta correcta | `isLoading = false`, `error = null`, `movies = [...]` | Tabla con columnas `ID`, `Title`, `Director`, `Year`, `Genre` y botón `Delete` en cada fila | `setMovies(response.data)`. `Delete` llama a `deleteMovie(id)` y filtra el estado local, sin recargar la página |
| Error de petición | `isLoading = false`, `error !== null` | Caja de alerta roja con el mensaje técnico del error (por ejemplo, `Network Error`) y botón **`Retry`** | `setError(requestError)`. `Retry` reinicia `isLoading` y `error`, y vuelve a ejecutar la carga |

Ruta `/create` → componente `MovieForm`:

- Entradas controladas para `title`, `director`, `release_year` y `genre`.
- El `<form>` usa `noValidate`, por lo que se pueden enviar campos vacíos.
- Si Django responde `400 Bad Request`, se muestra `error.response.data` tal cual, campo por campo.
- Si la creación es exitosa, `useNavigate()` redirige a `/`.

---

## 3. Casos de prueba realizados

| # | Caso | Cómo se probó | Resultado | Commit relacionado |
|---|---|---|---|---|
| 1 | **CORS** | Con el back-end en `8000` y el front-end en `5173`, se envió `GET http://127.0.0.1:8000/api/movies/` con `Origin: http://localhost:5173`. | Respuesta `200` con `Access-Control-Allow-Origin: http://localhost:5173`. No se produjo bloqueo CORS en el navegador. | `283f08c` — configuración del back-end |
| 2 | **Validación HTTP 400** | Se envió `POST /api/movies/` con un payload vacío y se probó el formulario `/create` con todos los campos vacíos gracias a `noValidate`. | Django devolvió `400` con mensajes como `This field is required.` y `Title must not be empty.`; el formulario mostró esos mensajes exactos debajo de cada campo. | `283f08c` — serializer y `1d18755` — formulario |
| 3 | **Servidor apagado** | Se apuntó temporalmente el front-end a un puerto cerrado (`http://127.0.0.1:9999/api`) para simular que el back-end no responde, sin detener el servidor real. | `getMovies()` falló con `Network Error`; apareció la alerta roja **`Unable to load movies`** y el botón **`Retry`**. Al restaurar `.env`, la URL vuelve a ser la correcta y `Retry` permite repetir la petición. | `1d18755` — estados de carga/error del front-end |

### Verificación adicional

```text
python manage.py check        → sin problemas
npm run build                 → compilación correcta
npm run lint                  → sin errores ni advertencias
GET /api/movies/              → 200 con 4 películas sembradas
```

---

## 4. Commits subidos a GitHub

| Commit | Descripción |
|---|---|
| `283f08c` | `feat(semana12): agregar backend Django REST para catálogo de películas` |
| `1d18755` | `feat(semana12): agregar cliente React con Axios y estados de petición` |
| — | `docs(semana12): documentar ejecución, estados y pruebas` |

Los dos primeros commits corresponden a las implementaciones usadas en los casos de prueba. El tercer commit incorpora este documento.
