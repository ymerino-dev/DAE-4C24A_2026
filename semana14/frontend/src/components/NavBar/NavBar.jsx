import { NavLink } from 'react-router-dom';

import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import './NavBar.css';

function NavBar() {
  const { user, logout } = useAuth();
  const { totalItems } = useCart();

  return (
    <header className="navbar">
      <NavLink className="navbar-brand" to="/">
        Product Catalog
      </NavLink>
      <nav className="navbar-links" aria-label="Main navigation">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            isActive ? 'nav-link active' : 'nav-link'
          }
        >
          Products
        </NavLink>
        <NavLink
          to="/create"
          className={({ isActive }) =>
            isActive ? 'nav-link active' : 'nav-link'
          }
        >
          New Product
        </NavLink>
        <NavLink
          to="/cart"
          className={({ isActive }) =>
            isActive ? 'nav-link active' : 'nav-link'
          }
        >
          Cart <span className="cart-count">{totalItems}</span>
        </NavLink>
        {user ? (
          <>
            <span className="navbar-user">{user.username}</span>
            <button
              className="nav-link logout-button"
              type="button"
              onClick={logout}
            >
              Logout
            </button>
          </>
        ) : (
          <NavLink
            to="/login"
            className={({ isActive }) =>
              isActive ? 'nav-link active' : 'nav-link'
            }
          >
            Login
          </NavLink>
        )}
      </nav>
    </header>
  );
}

export default NavBar;
