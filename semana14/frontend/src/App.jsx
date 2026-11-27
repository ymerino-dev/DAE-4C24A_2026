import { BrowserRouter, Route, Routes } from 'react-router-dom';

import CartPage from './components/CartPage/CartPage';
import LoginPage from './components/LoginPage/LoginPage';
import NavBar from './components/NavBar/NavBar';
import ProductCatalog from './components/ProductCatalog/ProductCatalog';
import ProductForm from './components/ProductForm/ProductForm';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <NavBar />
          <main className="app-main">
            <Routes>
              <Route path="/" element={<ProductCatalog />} />
              <Route path="/create" element={<ProductForm />} />
              <Route path="/edit/:id" element={<ProductForm />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/cart" element={<CartPage />} />
            </Routes>
          </main>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
