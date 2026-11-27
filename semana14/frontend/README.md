# Cliente React — Laboratorio 14

Cliente de React 19 + Vite para la API del laboratorio 14. Consume el servidor
Django REST en `http://127.0.0.1:8000/api` y se ejecuta en
`http://localhost:5173`.

La documentación arquitectónica completa está en `semana14/README.md`.

## Arranque

```powershell
npm install
Copy-Item .env.example .env
npm.cmd run dev -- --port 5173 --strictPort
```

En PowerShell se usa `npm.cmd` porque la política de ejecución puede bloquear
`npm.ps1`. El puerto 5173 debe respetarse porque es el origen permitido por
CORS en el servidor.

## Variables de entorno

```txt
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Scripts

```bash
npm run dev
npm run build
npm run lint
```

## Estructura resumida

- `src/services/`: capa HTTP con Axios y el interceptor de token.
- `src/context/`: `AuthContext` y `CartContext`.
- `src/components/`: una carpeta por componente, en PascalCase.
- `src/App.jsx`: proveedores globales, rutas públicas y ruta protegida.

Los componentes no importan Axios ni construyen URLs de API: toda petición
pasa por `src/services/`.
