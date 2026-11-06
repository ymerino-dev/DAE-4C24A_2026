<div align="center">

# Laboratorio 11 · Comunicación entre componentes en ReactJS

**Desarrollo de Aplicaciones Empresariales · 2026-2**
Cartelera Cine Tecsup · Continuación del proyecto de la semana 10

![React](https://img.shields.io/badge/React-19-149ECA?logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)
![Estado](https://img.shields.io/badge/estado-laboratorio%20individual-8C3B2E)

</div>

---

## Datos del laboratorio

| Campo | Detalle |
|---|---|
| Alumna | Ana Yanira Merino Ramos |
| Curso | Desarrollo de Aplicaciones Empresariales |
| Actividad | DAE · Lab 11 · Comunicación entre componentes |
| Semana / semestre | 11 / 4.º |
| Modalidad | Individual |
| Docente | Michael Montgomery Rosell |
| Capacidad terminal | Implementar ejercicios para visualizar la comunicación entre distintos componentes en ReactJS |

## Objetivo

Comunicar componentes hermanos elevando el estado compartido al ancestro común necesario; extraer lógica reutilizable a hooks propios; integrar una biblioteca de interfaz; y representar los estados de carga, éxito y error.

## Arquitectura y flujo de datos

```mermaid
flowchart TD
  App[App · favoritas, filtro y persistencia]
  Header[Header · recibe solo favoriteCount]
  Search[MovieSearch · entrada controlada]
  Banner[FilterBanner · puede limpiar el filtro]
  List[MovieList · filtra y mide columnas]
  Card[MovieCard · emite id de favorita]
  HookDebounce[useDebounce]
  HookSize[useWindowSize]
  Premiere[PremiereSection · hermanos del listado]
  HookPremieres[usePremieres · loading / success / error]
  Adapt[adaptMovie · normaliza datos]
  Toast[React Toastify · aviso emergente]

  App --> Header
  App --> Search
  App --> Banner
  App --> List
  App --> Premiere
  Search -->|onSearch(text)| App
  Banner -->|onClear()| App
  List --> Card
  Card -->|onToggleFavorite(id)| App
  App -->|favoriteCount| Header
  App -->|usa filtro con retardo| HookDebounce
  Premiere --> HookDebounce
  List --> HookSize
  Premiere --> HookPremieres
  HookPremieres --> Adapt
  App -->|notificación| Toast
```

### Estado por nivel

| Nivel | Dato que vive ahí | Motivo |
|---|---|---|
| `App` | IDs de favoritas y texto del filtro | `Header`, `MovieList` y `FilterBanner` son hermanos que necesitan consultar o cambiar parte de esos datos. `App` es el ancestro común más cercano en esta composición. |
| `Header` | Ningún arreglo de favoritas; recibe `favoriteCount` | Solo presenta el total. Mantener el arreglo aquí acoplaría la cabecera a las películas y obligaría a pasar información que no necesita. |
| `MovieSearch` | Ninguno; recibe `value` y comunica cambios por `onSearch` | El valor se mantiene sincronizado con el botón de limpieza del banner. |
| `MovieList` | Ningún estado de favoritas; recibe la lista y callbacks | Presenta las tarjetas y adapta el número de columnas usando `useWindowSize`. |
| `MovieCard` | Estado visual derivado por props | Envía el ID a su padre. No conoce Toastify ni decide cómo se muestra el aviso. |
| `PremiereSection` | Estado de petición encapsulado en `usePremieres` | Es independiente de la cartelera actual y muestra carga, error o resultados. |

**¿Por qué el contador no vive en la cabecera?** La cabecera y las tarjetas son componentes hermanos. La cabecera no puede leer el estado local de las tarjetas. Al mantener la lista en `App`, las tarjetas envían el ID que cambió y `App` calcula el total; la cabecera recibe solo el número que necesita. Así no recibe la lista completa ni gestiona datos de películas.

## Desarrollo realizado

1. Se continuó sobre el proyecto de cartelera de Semana 10, conservando componentes, datos y estilos existentes.
2. Se normalizó el modelo de película con `adaptMovie`, que acepta las claves de la aplicación y las claves típicas de un servicio (`name`, `poster_path`, `overview`, `vote_average`).
3. `App` conserva favoritas y filtro compartido. El filtro tiene un retardo de 400 ms antes de actualizar el listado. El banner puede limpiar el mismo valor controlado del buscador.
4. `MovieCard` emite la acción al ancestro mediante props. `App` actualiza `localStorage` y presenta el aviso emergente con React Toastify.
5. `useDebounce` se reutiliza en `App` y `PremiereSection`; `useWindowSize` responde a cambios del ancho y determina las columnas de la cartelera.
6. `usePremieres` simula una petición y expone `loading`, `success` y `error`. La sección presenta un esqueleto accesible, estrenos adaptados, mensaje de error y botón de reintento.
7. El caso de error puede observarse agregando `?fallarEstrenos=1` a la dirección local. Al reintentar, la petición simulada devuelve los datos.

### Estructura relevante

```text
semana11/
├── public/posters/                 # Afiches de películas
├── src/
│   ├── adapters/movieAdapter.js    # Adaptador de datos de películas
│   ├── data/movies.js              # Cartelera base del laboratorio
│   ├── duel/team/                  # Componentes de la aplicación
│   │   ├── FilterBanner.jsx        # Limpia el filtro compartido
│   │   ├── Header.jsx              # Presenta el contador recibido
│   │   ├── LoadingSkeleton.jsx     # Estado visual de carga
│   │   ├── MovieCard.jsx           # Acción de favorita por callback
│   │   ├── MovieList.jsx           # Filtrado y columnas adaptables
│   │   └── PremiereSection.jsx     # Carrusel/rejilla de próximos estrenos
│   ├── hooks/
│   │   ├── useDebounce.js          # Retardo reutilizable
│   │   ├── usePremieres.js         # Carga, datos, error y reintento
│   │   └── useWindowSize.js        # Ancho de ventana y limpieza del listener
│   ├── styles/index.css            # Diseño adaptable y estados visuales
│   ├── App.jsx                      # Estado compartido e integración Toastify
│   └── main.jsx                     # Entrada de React
├── package.json
└── README.md                        # Este entregable
```

## Instalación y ejecución

Requisitos: Windows 10 o superior, Node.js 20 o superior, Git, Visual Studio Code y acceso a internet.

```powershell
cd semana11
npm install
npm run dev
```

Vite indicará la dirección local en la terminal. Para revisar la compilación de producción:

```powershell
npm run build
```

La interfaz se muestra en español; el código, nombres de variables y comentarios se mantienen en inglés.

## Casos de comprobación

| Caso | Resultado esperado |
|---|---|
| Marcar y quitar una favorita | Cambia el estado de la tarjeta, el contador del encabezado y la persistencia local; aparece un aviso emergente. |
| Buscar un título | La lista se actualiza luego del retardo de 400 ms. |
| Limpiar desde el banner | El campo de búsqueda y la cartelera vuelven a mostrar todos los títulos. |
| Redimensionar la ventana | La cartelera cambia entre una, dos, tres y cuatro columnas según el ancho. |
| Cargar estrenos | Se muestra el esqueleto y luego las tarjetas adaptadas. |
| Simular error de estrenos | Con `?fallarEstrenos=1` aparece un mensaje explicativo y un botón de reintento. |
| Datos de estreno sin campos opcionales | El adaptador asigna valores de respaldo y la sección mantiene un modelo consistente. |

## Evidencias para el entregable

Al ejecutar la aplicación, agregar capturas de la cartelera, contador de favoritas, aviso emergente, estado de carga/estrenos y estructura de carpetas en el editor. La guía de evaluación solicita registrar nombre, título, captura, código, explicación y casos de prueba en el entregable del campus virtual.

## Rúbrica (20 puntos)

| Criterio | Puntaje |
|---|---:|
| Comunicación de hermanos elevando el estado al ancestro común | 5 |
| Extracción de lógica reutilizable a hooks propios | 5 |
| Biblioteca de interfaz y estados de carga/error | 5 |
| Entrega del repositorio con hooks y observaciones | 5 |
| **Total** | **20** |

## Conclusiones

1. Elevar las favoritas y el filtro a `App` permite que sus componentes hermanos se mantengan sincronizados por props y callbacks.
2. `useDebounce`, `useWindowSize` y `usePremieres` concentran lógica reutilizable y dejan componentes dedicados a presentar la interfaz.
3. Los estados explícitos de carga, éxito y error informan a la persona usuaria qué ocurre durante la simulación de la petición.
