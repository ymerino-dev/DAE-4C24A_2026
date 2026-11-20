import { BrowserRouter, Route, Routes } from 'react-router-dom';

import NavBar from './components/NavBar/NavBar';
import ProductCatalog from './components/ProductCatalog/ProductCatalog';
import ProductForm from './components/ProductForm/ProductForm';

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<ProductCatalog />} />
          <Route path="/create" element={<ProductForm />} />
          <Route path="/edit/:id" element={<ProductForm />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
