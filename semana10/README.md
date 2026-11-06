# Cartelera Cine Tecsup — componentes y eventos

## Desarrollo del laboratorio S10 — Componentes reutilizables, estado y eventos

**Alumno:** (completar con el nombre del alumno)  
**Título del desarrollo:** Cartelera de cine con componentes reutilizables, useState y eventos

### Evidencia del desarrollo

**Código principal:** `src/App.jsx` compone las partes de la página, gestiona el estado de las películas favoritas con `useState` e integra el buscador:

```jsx
<Header name="Cine Tecsup" links={links} />
<Hero movie={featuredMovie} />
<MovieSearch onSearch={handleSearch} />
<MovieList
  movies={movies}
  searchText={searchText}
  onToggleFavorite={toggleFavorite}
  favorites={favorites}
/>
<Footer contact={contact} />
```

**Nuevos componentes de la semana 10:**

| Componente | Props | Responsabilidad |
|---|---|---|
| `Button` | `children`, `variant`, `onClick` | Botón reutilizable; el contenido viene por `children` y el aspecto por `variant` (`primary`, `secondary`, `outline`, `ghost`, `danger`). |
| `MovieSearch` | `onSearch`, `debounceMs` | Entrada controlada: el texto vive en estado y `onChange` lo actualiza en cada pulsación; un retardo (debounce) evita disparar el filtrado con cada letra. |
| `MovieCard` | `movie`, `onToggleFavorite`, `isFavorite` | Tarjeta de película con botón de favorita que comunica al padre mediante una función recibida por props. |
| `MovieList` | `movies`, `searchText`, `onToggleFavorite`, `favorites` | Filtra la cartelera por el texto del buscador y dibuja un estado vacío cuando ninguna película coincide. |

**Estado y almacenamiento (pasos 4, 5 y 10 de la guía):**
- `App` mantiene el array `favorites` con `useState` y expone `toggleFavorite(id)` para agregar o quitar una película.
- `toggleFavorite` se pasa a `MovieCard` por props; la tarjeta lo invoca al hacer clic y muestra el estado actual ("En favoritas" / "No está en favoritas").
- Las favoritas se guardan en `localStorage` bajo la clave `cine-favoritas` y se recuperan al cargar la página, por lo que sobreviven a una recarga.

**Buscador (pasos 6, 7, 8 y 9):**
- `MovieSearch` es una entrada controlada: `value` ligado a estado y `onChange` actualizando en cada tecla.
- Se aplica un retardo de 400 ms para comparar en consola la diferencia entre filtrar por letra y filtrar tras el retardo.
- `MovieList` filtra la cartelera por el texto del buscador y dibuja un estado vacío cuando no hay coincidencias.
- El buscador se integra en el cartelera (banner) con su llamada a la acción.

**Casos de prueba considerados:**

| Caso | Resultado esperado | Estado |
|---|---|---|
| Cargar la cartelera | Aparecen las ocho tarjetas con sus datos | Implementado |
| Película sin horarios | Se lee «Sin funciones hoy» | Incluido (película 5) |
| Botón de favorita | Agrega/quita la película y muestra el estado actual | Implementado |
| Favoritas persisten | Sobreviven a una recarga de la página | Implementado (`localStorage`) |
| Buscar por título | Filtra la cartelera; estado vacío si no hay coincidencias | Implementado |
| Debounce del buscador | El filtrado no se dispara con cada letra | Implementado (400 ms) |
| Botón reutilizable | Mismo componente con distintas variantes (`variant`) | Implementado |
| Compilar para producción | Vite genera `dist/` sin errores | `npm run build` |

**Estructura del proyecto:**

```text
semana10/
├── public/posters/          # Afiches de las ocho películas
├── src/
│   ├── data/movies.js       # Cartelera, navegación y contacto
│   ├── duel/team/           # Componentes funcionales del laboratorio
│   │   ├── Button.jsx       # Botón reutilizable (children + variant)
│   │   ├── MovieSearch.jsx  # Buscador controlado con debounce
│   │   ├── Header.jsx
│   │   ├── Hero.jsx
│   │   ├── MovieCard.jsx    # Tarjeta con botón de favorita
│   │   ├── MovieList.jsx    # Filtrado por búsqueda + estado vacío
│   │   ├── Showtimes.jsx
│   │   ├── Synopsis.jsx
│   │   ├── AgentMessage.jsx
│   │   └── index.jsx
│   ├── duel/tests/          # Pruebas automatizadas del repositorio
│   ├── styles/index.css     # Estilos adaptables + botón/formulario
│   ├── App.jsx              # Composición: estado favoritas + buscador
│   └── main.jsx             # Punto de entrada de React
├── README.md                # Evidencia y explicación
├── index.html
├── package.json
├── vite.config.js
└── .env.team                # VITE_DUEL_SOURCE=team
```

### Ejecución

Requisitos: Node.js 20 o superior. En PowerShell, desde la carpeta del repositorio:

```powershell
cd semana10
npm install
npm run dev
```

Vite muestra la dirección local en la terminal. Para generar la versión de producción: `npm run build`.

### Convenciones del curso

Código, nombres y comentarios en inglés; explicaciones y entregables en español.

**Nota:** este laboratorio se parte del resultado de la semana 9 (cartelera de cine) y lo extiende con componentes reutilizables, estado con `useState`, eventos y persistencia en `localStorage`, tal como pide la guía de la semana 10 ("Componentes y eventos").
