# Laboratorio 14 — Pedidos, autenticación por token y carrito persistente

Documentación técnica del laboratorio 14. El back-end está implementado con
**Django 6.1.3 + Django REST Framework** y el cliente con
**React 19 + Vite + Axios**.

- Repositorio: `https://github.com/ymerino-dev/DAE-4C24A_2026.git`
- Rama de trabajo: `main`
- Servidor: `http://127.0.0.1:8000`
- Cliente: `http://localhost:5173`
- Idioma: el código, los identificadores y los comentarios están en inglés;
  esta documentación y las explicaciones entregables están en español.
- Estilo: PEP 8 en Python; componentes React en PascalCase, una carpeta por
  componente y hooks personalizados con prefijo `use`.

---

## 1. Estructura final de `semana14`

```text
semana14/
├── README.md                         # Este documento (entregable en español)
├── backend/
│   ├── .gitignore
│   ├── manage.py
│   ├── requirements.txt
│   ├── create_superuser.py           # Superusuario desde variables de entorno
│   ├── seed.py                       # Categorías, productos y PNG de ejemplo
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py               # DB, CORS, media, DRF y authtoken
│   │   ├── urls.py                   # Router + login + pedidos
│   │   ├── asgi.py
│   │   └── wsgi.py
│   └── catalog/
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py                 # Category, Product, Order, OrderItem
│       ├── serializers.py            # Serializadores y creación atómica
│       ├── views.py                  # ViewSets, LoginView, OrderListCreateView
│       ├── admin.py                  # Admin con OrderItemInline
│       ├── tests.py
│       ├── migrations/
│       │   ├── __init__.py
│       │   ├── 0001_initial.py
│       │   └── 0002_order_orderitem.py
│       └── management/
│           ├── __init__.py
│           └── commands/
│               ├── __init__.py
│               └── create_test_users.py
└── frontend/
    ├── .env.example
    ├── .gitignore
    ├── .oxlintrc.json
    ├── README.md                     # Notas de arranque del cliente
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    ├── public/
    │   ├── favicon.svg
    │   └── icons.svg
    └── src/
        ├── App.jsx                   # BrowserRouter, providers y rutas
        ├── main.jsx
        ├── index.css
        ├── components/
        │   ├── CartPage/
        │   │   ├── CartPage.jsx
        │   │   └── CartPage.css
        │   ├── LoginPage/
        │   │   ├── LoginPage.jsx
        │   │   └── LoginPage.css
        │   ├── MyOrdersPage/
        │   │   ├── MyOrdersPage.jsx
        │   │   └── MyOrdersPage.css
        │   ├── NavBar/
        │   │   ├── NavBar.jsx
        │   │   └── NavBar.css
        │   ├── ProductCatalog/
        │   │   ├── ProductCatalog.jsx
        │   │   └── ProductCatalog.css
        │   ├── ProductDetailPage/
        │   │   ├── ProductDetailPage.jsx
        │   │   └── ProductDetailPage.css
        │   ├── ProductForm/
        │   │   ├── ProductForm.jsx
        │   │   └── ProductForm.css
        │   └── ProtectedRoute/
        │       └── ProtectedRoute.jsx
        ├── context/
        │   ├── AuthContext.jsx       # AuthProvider + useAuth
        │   └── CartContext.jsx       # CartProvider + useCart
        └── services/
            ├── api.js                # Axios + interceptor Token
            ├── apiClient.js          # Re-exportación de api.js
            ├── authService.js
            ├── categoryService.js
            ├── orderService.js
            └── productService.js
```

No se versionan `venv`, `node_modules`, `dist`, `__pycache__`, `db.sqlite3`,
`media/`, `.env` ni la carpeta `.git` anidada. Estos artefactos son
reproducibles o contienen configuración local.

---

## 2. Tabla comparativa Servidor vs. Cliente

| Bloque | Servidor (Django / DRF) | Cliente (React / Vite) |
|---|---|---|
| Modelos | `Category`, `Product`, `Order` y `OrderItem` en `catalog/models.py`. `Order.user` usa `settings.AUTH_USER_MODEL`; `OrderItem` guarda `unit_price` congelado. | No existen modelos de dominio persistentes. Los productos y pedidos se consumen como JSON; el único estado local de dominio es el carrito. |
| Serializadores | `CategorySerializer`, `ProductSerializer`, `UserSerializer`, `LoginSerializer`, `OrderItemSerializer` y `OrderSerializer`. El serializer de pedidos calcula `total` y descuenta stock. | No hay serializadores. Las funciones de `src/services/` envían y reciben JSON; los contexts convierten esas respuestas en estado de la interfaz. |
| Autenticación | `rest_framework.authtoken` en `INSTALLED_APPS`; `TokenAuthentication` por defecto; `LoginView` usa `authenticate()` y `Token.objects.get_or_create()`. | `api.js` adjunta `Authorization: Token <token>`; `authService.js` consume `/auth/login/`; `AuthContext` guarda `token` y `user`; `ProtectedRoute` redirige a `/login`. |
| Vistas y endpoints | `CategoryViewSet` y `ProductViewSet` (`ModelViewSet`); `LoginView` (`APIView`, `AllowAny`); `OrderListCreateView` (`APIView`, `IsAuthenticated`). | Pantallas que consumen esos endpoints: catálogo, detalle, formulario, carrito, login y mis pedidos. |
| Rutas HTTP | `/api/categories/`, `/api/products/`, `/api/auth/login/`, `/api/orders/`, `/admin/` y `/media/` con `DEBUG=True`. | `/`, `/products/:id`, `/create`, `/edit/:id`, `/cart`, `/login`, `/my-orders`. |
| Servicios / lógica | `OrderSerializer.create()` encapsula la regla de negocio: bloqueo de filas, validación de stock, precios actuales y descuento atómico. `ProductViewSet.get_queryset()` evita el problema N+1 con `select_related`. | `api.js`, `apiClient.js`, `authService.js`, `orderService.js`, `productService.js` y `categoryService.js` concentran todo el acceso HTTP. Ningún componente construye URLs ni importa Axios directamente. |
| Contextos | El estado se mantiene en la base de datos; el token vive en la tabla `authtoken`. | `AuthContext` para sesión y `CartContext` para carrito global persistente. Ambos se montan una sola vez en `App.jsx`. |
| Pantallas / administración | `/admin/` registra los cuatro modelos; `OrderAdmin` incluye `OrderItemInline` para editar líneas dentro del pedido. | Componentes con carpeta propia: `ProductCatalog`, `ProductDetailPage`, `ProductForm`, `CartPage`, `LoginPage`, `MyOrdersPage`, `NavBar` y `ProtectedRoute`. |
| Persistencia | SQLite (`db.sqlite3`) y archivos subidos en `media/products/`. | `localStorage` con claves `token`, `user` y `cart`. |
| Validación y errores | Los serializers devuelven `400`; el login inválido devuelve `401 {"detail": "Invalid credentials"}`; los endpoints de pedido exigen autenticación. | Estados de carga/error en cada pantalla; mensaje exacto de la API en `CartPage`; redirección a `/login` cuando no hay sesión. |

### 2.1 Endpoints implementados

| Método | Ruta | Permiso | Vista | Resultado principal |
|---|---|---|---|---|
| `GET`, `POST` | `/api/categories/` | Público | `CategoryViewSet` | Lista y crea categorías. |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/api/categories/{id}/` | Público | `CategoryViewSet` | Detalle y CRUD de una categoría. |
| `GET`, `POST` | `/api/products/` | Público | `ProductViewSet` | Lista con categoría anidada; filtro opcional `?category=<id>`; creación multipart. |
| `GET`, `PATCH`, `DELETE` | `/api/products/{id}/` | Público | `ProductViewSet` | Detalle, edición parcial y borrado. |
| `POST` | `/api/auth/login/` | `AllowAny` | `LoginView` | `200` con `{ token, user }`; `401` si las credenciales fallan. |
| `GET` | `/api/orders/` | `IsAuthenticated` | `OrderListCreateView` | Pedidos de `request.user`, ordenados por `created_at` descendente, con `items`. |
| `POST` | `/api/orders/` | `IsAuthenticated` | `OrderListCreateView` | Crea el pedido con `201`; descuenta stock de forma atómica; `400` si falta stock. |

### 2.2 Rutas del cliente

| Ruta | Pantalla | Protección | Responsabilidad |
|---|---|---|---|
| `/` | `ProductCatalog` | No | Catálogo, filtro por categoría, alta rápida al carrito y acceso al detalle. |
| `/products/:id` | `ProductDetailPage` | No | Detalle del producto y botón `Add to Cart`. |
| `/create` | `ProductForm` | No | Alta de productos con `FormData`. |
| `/edit/:id` | `ProductForm` | No | Edición de productos. |
| `/cart` | `CartPage` | No, pero el checkout exige sesión | Líneas del carrito, cantidades, total provisional y `Place Order`. |
| `/login` | `LoginPage` | No | Formulario controlado con mensaje de error y retorno a la ruta solicitada. |
| `/my-orders` | `MyOrdersPage` | Sí, mediante `ProtectedRoute` | Pedidos del usuario con ID, fecha, estado, total confirmado y desglose. |

---

## 3. Dónde vive el carrito y por qué

El carrito vive en dos capas complementarias:

1. **Estado React global:** `CartProvider`, definido en
   `src/context/CartContext.jsx`, mantiene el arreglo `items`. Se monta una sola
   vez en `App.jsx`, por encima de `NavBar` y de las rutas, por lo que todas las
   pantallas comparten la misma instancia sin propagar props.
2. **Persistencia local:** la clave `cart` de `localStorage` guarda el arreglo
   como JSON. `getStoredCart()` lo lee al iniciar, valida que sea un arreglo y
   un `useEffect` vuelve a escribirlo después de cada cambio. Las claves
   `token` y `user` se gestionan de forma análoga en `AuthContext`.

La API expuesta por `useCart()` es:

- `addToCart(product, quantity)`: agrega o acumula un producto por `id`.
- `updateQuantity(productId, quantity)`: ajusta la cantidad, con mínimo 1.
- `removeFromCart(productId)`: elimina la línea.
- `clearCart()`: vacía el carrito tras un pedido confirmado.
- `totalItems` y `provisionalTotal`: valores derivados con `useMemo`.

### ¿Por qué este diseño?

- **Supervivencia a recargas:** un visitante anónimo puede llenar el carrito,
  recargar la página o navegar a otro módulo sin perderlo. No hace falta crear
  una cuenta ni una sesión de servidor solo para guardar la selección.
- **Única fuente de estado en la UI:** el contexto evita duplicar arreglos en
  `ProductCatalog`, `ProductDetailPage`, `CartPage` y `NavBar`. El contador de la
  cabecera se actualiza en tiempo real porque consume el mismo contexto.
- **Desacoplamiento:** los componentes no conocen `localStorage`; solo llaman
  al hook. La persistencia es un detalle de implementación del proveedor.
- **Total explícitamente provisional:** el precio mostrado se usa solo para la
  vista previa. El cliente envía únicamente `product_id` y `quantity` a
  `POST /api/orders/`; el servidor consulta el precio vigente y vuelve a
  calcular `unit_price` y `total`. Por eso la interfaz indica que el monto es
  provisional hasta la validación del servidor.
- **Checkout coherente:** si la API responde `201`, se limpia el carrito y se
  redirige a `/my-orders` con la confirmación. Si responde error, el carrito se
  conserva para que el usuario corrija cantidades sin perder su selección.

---

## 4. Descuento de stock y concurrencia

### 4.1 ¿Por qué descontar al crear el pedido y no al pagarlo?

En el paso 10 del laboratorio se descuenta el stock durante la **creación del
pedido**, dentro de `OrderSerializer.create()`. El pago se trata como un paso
posterior y separado. Esta decisión tiene varias ventajas:

- **La base de datos es la fuente de verdad.** En cuanto el pedido nace, la
  existencia queda reservada. Otro cliente que consulte `Product.stock` ve el
  valor real y no puede comprar una unidad que ya fue comprometida.
- **Evita venta por encima del stock.** Si el descuento se dejara para el pago,
  dos clientes podrían ver `stock = 1`, iniciar dos pagos y terminar con dos
  pedidos pagados por una sola unidad. El sistema tendría que reembolsar y
  explicar la incidencia al cliente.
- **Congela el acuerdo comercial.** `unit_price` se guarda por línea con el
  precio vigente y `Order.total` se calcula en el servidor. Un cambio posterior
  en `Product.price` no altera pedidos ya creados.
- **Permite compensación controlada.** El pedido nace con estado `PENDING`. Si
  el pago falla, se cancela el pedido y se devuelve el stock; si se confirma,
  se cambia el estado a `CONFIRMED`. La cancelación y la devolución deben
  ejecutarse juntas, preferiblemente en la misma transacción o mediante una
  saga con eventos de compensación.
- **Simplifica la auditoría.** Cada pedido conserva fecha, usuario, estado,
  total y líneas; no depende de un evento de pago externo para reconstruir qué
  se vendió.

Descontar solo al pagar dejaría una ventana de inconsistencia entre “pedido
creado” y “pago confirmado”. Esa ventana es precisamente donde aparece el caso
de la última unidad.

### 4.2 Mecanismos implementados para el caso de la última unidad

La implementación actual combina tres mecanismos:

1. **Transacción atómica:** `create()` está decorado con
   `@transaction.atomic`. Si cualquier validación falla, se revierte todo:
   no se crea el `Order`, no se crean los `OrderItem` y no se modifica el stock.
2. **Bloqueo pesimista:** `Product.objects.select_for_update().filter(...)`
   bloquea las filas de los productos involucrados dentro de la transacción.
3. **Validación y actualización dentro de la transacción:** se suman las
   cantidades repetidas de un mismo producto, se compara con `product.stock`,
   se calcula el total y se guarda el stock con `save(update_fields=['stock'])`.

Con dos pedidos simultáneos por la única unidad disponible, el primero adquiere
el bloqueo, valida, descuenta a `0` y hace `commit`. El segundo queda esperando;
cuando obtiene el bloqueo, relee `stock = 0` y responde
`400` con `Insufficient stock...`. No se crea un segundo pedido ni se descuenta
por debajo de cero.

> En SQLite, `select_for_update()` no produce bloqueos de fila reales; el
> motor serializa las escrituras. En producción con PostgreSQL o MySQL el
> bloqueo de fila sí es efectivo y conviene ordenar los `product_id` antes de
> bloquear para evitar interbloqueos.

### 4.3 Mecanismos adicionales para mayor escala

Cuando el volumen crece o el pago es asíncrono, conviene añadir:

- **Reservas temporales:** una tabla de reservas con `product_id`, `quantity`,
  `expires_at` y `order_id`. El pedido consume el stock disponible menos las
  reservas vigentes; la reserva se libera si expira o si el pago falla.
- **Colas de mensajes:** publicar los comandos de creación de pedidos en una
  cola y procesarlos de forma serializada por producto. Esto reduce la
  contención en la base de datos y permite reintentos controlados.
- **Control optimista:** un campo `version` o una actualización condicional con
  `F('stock')` y un filtro `stock__gte=quantity`; si no afecta filas, otro
  pedido ganó la carrera y se devuelve `400`.
- **Idempotencia:** una clave de idempotencia por checkout evita duplicar
  pedidos si el cliente reintenta tras un timeout de red.
- **Saga de pago:** eventos de `payment_failed` y `payment_confirmed` que
  cancelan/restauran o confirman el pedido, con un estado final coherente.

---

## 5. Auditoría de normas de código

| Norma | Comprobación | Resultado |
|---|---|---|
| Inglés en código y comentarios | Revisión de nombres, docstrings y comentarios en `.py`, `.js` y `.jsx`. | Correcto. No se encontraron identificadores ni comentarios en español. |
| PEP 8 en Python | Longitud máxima de 79 caracteres en todos los `.py`, ausencia de tabuladores y de whitespace final. | Correcto. Las dos migraciones generadas se ajustaron sin cambiar sus operaciones. |
| Modelos en singular | `Category`, `Product`, `Order`, `OrderItem`. | Correcto. |
| Migraciones versionadas | `0001_initial.py` y `0002_order_orderitem.py`. | Correcto; `makemigrations --check --dry-run` no detecta cambios. |
| Sin credenciales en `settings.py` | `SECRET_KEY` y `DEBUG` se leen desde variables de entorno. | Correcto. |
| Componentes PascalCase y una carpeta por componente | `CartPage`, `LoginPage`, `MyOrdersPage`, `NavBar`, `ProductCatalog`, `ProductDetailPage`, `ProductForm`, `ProtectedRoute`. | Correcto. |
| Hooks con prefijo `use` | `useAuth` y `useCart`, además de los hooks nativos. | Correcto. |
| Capa de servicios | Solo `src/services/` importa Axios y construye URLs de API. | Correcto. |
| Lint y build del cliente | `npm.cmd run lint` y `npm.cmd run build`. | Sin errores ni advertencias. |
| Verificación del servidor | `manage.py check` y `makemigrations --check --dry-run`. | Sin problemas y sin cambios pendientes. |

Pruebas funcionales ejecutadas durante el laboratorio:

- Login válido: `200` con `token` y `user`; credenciales inválidas: `401`.
- Pedido con stock 1: `201`, `total` recalculado por el servidor y stock `1 → 0`.
- Segundo pedido por la misma unidad: `400` con mensaje de stock insuficiente,
  sin pedido adicional y sin descuento negativo.
- `GET /api/orders/`: solo los pedidos del usuario autenticado.
- Checkout sin sesión: redirección a `/login`; con sesión y `201`:
  redirección a `/my-orders` con confirmación y carrito vacío.

---

## 6. Puesta en marcha

Servidor:

```powershell
cd semana14/backend
$env:DJANGO_SECRET_KEY = [guid]::NewGuid().ToString()
py -3.13 -m pip install -r requirements.txt
py -3.13 manage.py migrate
py -3.13 manage.py create_test_users
py -3.13 manage.py runserver 8000
```

Las contraseñas de los usuarios de prueba se leen desde
`DJANGO_TEST_USER_PASSWORD` y `DJANGO_TEST_ADMIN_PASSWORD`; no se escriben en
`settings.py`.

Cliente:

```powershell
cd semana14/frontend
npm install
Copy-Item .env.example .env
npm.cmd run dev -- --port 5173 --strictPort
```

La URL base de la API se define en `.env` mediante
`VITE_API_BASE_URL=http://127.0.0.1:8000/api`.
