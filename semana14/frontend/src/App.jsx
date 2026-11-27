import { BrowserRouter, Route, Routes } from 'react-router-dom';

import CartPage from './components/CartPage/CartPage';
import LoginPage from './components/LoginPage/LoginPage';
import MyOrdersPage from './components/MyOrdersPage/MyOrdersPage';
import NavBar from './components/NavBar/NavBar';
import ProductCatalog from './components/ProductCatalog/ProductCatalog';
import ProductDetailPage from './components/ProductDetailPage/ProductDetailPage';
import ProductForm from './components/ProductForm/ProductForm';
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';
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
              <Route path="/products/:id" element={<ProductDetailPage />} />
              <Route path="/create" element={<ProductForm />} />
              <Route path="/edit/:id" element={<ProductForm />} />
              <Route path="/cart" element={<CartPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route element={<ProtectedRoute />}>
                <Route path="/my-orders" element={<MyOrdersPage />} />
              </Route>
            </Routes>
          </main>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
