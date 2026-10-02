# Paso 12 — Experimento de Auto-Escapado (Seguridad XSS)

## Objetivo

Demostrar que el motor de plantillas de Django escapa automáticamente el
contenido HTML generado por los usuarios, previniendo ataques Cross-Site
Scripting (XSS).

## Procedimiento

1. Se creó un artículo en la base de datos con el siguiente contenido en el
   campo `body`:

   ```html
   <b>Noticia Importante</b>: Esta es una prueba de <script>alert('XSS')</script> seguridad.
   ```

2. Se verificó el renderizado en la plantilla de detalle
   (`templates/news/article_detail.html`) accediendo a la ruta
   `/article/noticia-importante/`.

## Resultado de la verificación

| Verificación | Resultado |
|---|---|
| Estado HTTP de la respuesta | `200 OK` |
| ¿Aparece `<script>alert` sin procesar en el HTML? | **No** |
| ¿Aparece escapado como `&lt;script&gt;`? | **Sí** |
| ¿Aparece `<b>` escapado como `&lt;b&gt;`? | **Sí** |

El navegador recibe entidades HTML (`&lt;script&gt;alert('XSS')&lt;/script&gt;`)
y las muestra como texto literal; el código nunca se ejecuta.

## Explicación técnica: por qué Django escapa automáticamente

### ¿Qué es el auto-escaping?

El motor de plantillas de Django tiene el **escapado automático
(auto-escaping)** activado por defecto. Cada vez que una variable se
interpola en una plantilla con la sintaxis `{{ variable }}`, el motor aplica
la función `escape` de `django.utils.html`, que convierte los caracteres con
significado especial en HTML por entidades seguras:

| Carácter | Entidad generada |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |
| `&` | `&amp;` |

### ¿Por qué es necesario? El ataque XSS

Cross-Site Scripting (XSS) es una vulnerabilidad que ocurre cuando una
aplicación web muestra datos proporcionados por un usuario sin validarlos ni
escaparlos. Un atacante puede inyectar código JavaScript malicioso en campos
de texto (como el cuerpo de una noticia) que luego se ejecuta en el navegador
de otros usuarios. Las consecuencias pueden incluir:

- **Robo de cookies de sesión**: el script puede leer `document.cookie` y
  enviarla al atacante, permitiendo el secuestro de sesiones.
- **Suplantación de identidad**: acciones realizadas en nombre del usuario
  legítimo (publicar contenido, cambiar contraseñas, realizar compras).
- **Defacement**: modificación del contenido visual de la página para todos
  los visitantes.
- **Redirección maliciosa**: envío de los usuarios a sitios de phishing.

Al escapar `<` y `>` (y el resto de caracteres especiales), Django garantiza
que cualquier etiqueta HTML escrita por un usuario se convierta en texto
plano visible. El navegador interpreta `&lt;script&gt;` como los caracteres
literales `<script>`, no como una etiqueta ejecutable, por lo que el ataque
queda neutralizado en la capa de presentación.

### Características del mecanismo

- **Protección por defecto**: no requiere configuración adicional; cualquier
  `{{ }}` escapa su contenido automáticamente.
- **Alcance correcto**: el escapado se aplica a los *datos* (variables), no a
  la *estructura* de la plantilla, por lo que el HTML legítimo escrito por el
  desarrollador se mantiene intacto.
- **Defensa en profundidad**: complementa otras medidas como la validación de
  formularios, el uso de `get_object_or_404` y los permisos del panel de
  administración.

## Riesgos del filtro `|safe`

El filtro `|safe` le indica al motor de plantillas que una variable **no**
debe escaparse, marcándola como "segura". Su uso es peligroso cuando la
variable contiene entrada de usuario:

```django
{{ article.body|safe }}   <!-- ¡PELIGROSO! El HTML se renderiza sin escapar -->
```

Con `|safe`, el contenido del ejemplo se renderizaría como:

```html
<b>Noticia Importante</b>: Esta es una prueba de <script>alert('XSS')</script> seguridad.
```

El navegador sí ejecutaría el `<script>`, materializando la vulnerabilidad XSS.
Un atacante con acceso al panel de administración (o a cualquier formulario
que alimente la base de datos) podría inyectar código que se ejecute en el
navegador de todos los visitantes.

**Buenas prácticas:**

1. **Nunca** aplicar `|safe` a contenido ingresado por usuarios.
2. Si se necesita HTML enriquecido (por ejemplo, un editor WYSIWYG), debe
   **sanitizarse previamente** con una librería como `bleach`, que elimina
   etiquetas y atributos peligrosos (`<script>`, `onclick`, `javascript:`,
   etc.) antes de marcar el contenido como seguro.
3. Desactivar el auto-escaping con `{% autoescape off %}` sigue la misma regla:
   solo para contenido de confianza absoluta, nunca para datos de usuario.
4. La regla de oro: **escapar por defecto, desescapar de forma explícita y
   justificada**.

## Conclusión

El experimento demuestra que Django protege automáticamente el portal de
noticias contra XSS: el contenido malicioso se almacena en la base de datos
pero se renderiza como texto inofensivo. Esta protección, combinada con el
uso responsable de `|safe`, mantiene la aplicación segura sin esfuerzo
adicional por parte del desarrollador.
