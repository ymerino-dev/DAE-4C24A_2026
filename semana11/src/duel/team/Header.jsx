export default function Header({ name, links, children, favoriteCount = 0 }) {
  return (
    <header>
      <h1>{name}</h1>
      <div className="header-right">
        <nav aria-label="Principal">
          <ul>
            {links.map((link) => (
              <li key={link.href}>
                <a href={link.href}>{link.label}</a>
              </li>
            ))}
          </ul>
        </nav>
        <p className="favorite-counter" aria-live="polite">
          Favoritas <span>{favoriteCount}</span>
        </p>
        {children}
      </div>
    </header>
  );
}
