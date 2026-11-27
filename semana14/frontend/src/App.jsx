import { BrowserRouter, Route, Routes } from 'react-router-dom';

import LoginPage from './components/LoginPage/LoginPage';
import NavBar from './components/NavBar/NavBar';
import ProductCatalog from './components/ProductCatalog/ProductCatalog';
import ProductForm from './components/ProductForm/ProductForm';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <NavBar />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<ProductCatalog />} />
            <Route path="/create" element={<ProductForm />} />
            <Route path="/edit/:id" element={<ProductForm />} />
            <Route path="/login" element={<LoginPage />} />
          </Routes>
        </main>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
