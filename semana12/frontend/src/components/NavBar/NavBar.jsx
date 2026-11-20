import { NavLink } from 'react-router-dom';

import './NavBar.css';

function NavBar() {
  return (
    <header className="navbar">
      <NavLink className="navbar-brand" to="/">
        Movie Catalog
      </NavLink>
      <nav className="navbar-links" aria-label="Main navigation">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            isActive ? 'nav-link active' : 'nav-link'
          }
        >
          Movies
        </NavLink>
        <NavLink
          to="/create"
          className={({ isActive }) =>
            isActive ? 'nav-link active' : 'nav-link'
          }
        >
          New Movie
        </NavLink>
      </nav>
    </header>
  );
}

export default NavBar;
