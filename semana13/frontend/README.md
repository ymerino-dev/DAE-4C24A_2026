# Product Catalog Front-End

React + Vite client for the Lab 13 e-commerce API. It consumes the Django REST
backend at `http://127.0.0.1:8000/api` and runs at `http://localhost:5173`.

## Setup

```bash
npm install
npm run dev
```

On Windows PowerShell, use `npm.cmd` if `npm.ps1` is blocked by the execution
policy. To force the port expected by CORS:

```bash
npm.cmd run dev -- --port 5173 --strictPort
```

Copy `.env.example` to `.env` if the local file is missing. The only setting is
`VITE_API_BASE_URL=http://127.0.0.1:8000/api`.

## Structure

- `src/services/apiClient.js`: base Axios instance with `baseURL`.
- `src/services/categoryService.js`: category endpoints.
- `src/services/productService.js`: product endpoints and multipart uploads.
- `src/components/ProductCatalog/`: catalog, filtering, loading/error states.
- `src/components/ProductForm/`: create and edit form with `FormData`.
- `src/components/NavBar/`: navigation bar.

Components never import Axios and never hardcode API URLs. All API access goes
through the service layer.

## Scripts

```bash
npm run dev
npm run build
npm run lint
```
